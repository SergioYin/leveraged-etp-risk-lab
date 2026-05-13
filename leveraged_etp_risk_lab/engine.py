from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .io import load_path, load_product
from .models import PortfolioManifest, ProductTerms, RiskBand, ScenarioDay, SimulationConfig


TRADING_DAYS = 252
POSITION_SIZE_SCHEMA_VERSION = "0.8"
STRESS_MATRIX_SCHEMA_VERSION = "0.9"
SENSITIVITY_GRID_SCHEMA_VERSION = "0.19"
PORTFOLIO_SENSITIVITY_SCHEMA_VERSION = "0.20"


def pct(value: float) -> float:
    return round(value * 100.0, 4)


def money(value: float) -> float:
    return round(value, 6)


def simulate(config: SimulationConfig) -> Dict[str, Any]:
    product = config.product
    daily_fee = product.annual_fee / TRADING_DAYS
    nav = config.initial_nav
    underlying_index = 100.0
    simple_multiple_nav = config.initial_nav
    rows: List[Dict[str, Any]] = []
    band_events: List[Dict[str, Any]] = []
    warnings = build_warnings(config)

    for item in sorted(config.path, key=lambda day: day.day):
        underlying_index *= 1 + item.underlying_return
        daily_levered_return = product.leverage * item.underlying_return - daily_fee
        nav *= 1 + daily_levered_return
        simple_multiple_nav = config.initial_nav * (1 + product.leverage * (underlying_index / 100.0 - 1))
        path_decay = nav - simple_multiple_nav

        stop_hit = _hit_stop(nav, config.risk_band.stop_loss, config.initial_nav)
        take_hit = _hit_take(nav, config.risk_band.take_profit, config.initial_nav)
        if stop_hit or take_hit:
            event = "stop_loss" if stop_hit else "take_profit"
            if not band_events or band_events[-1]["event"] != event:
                band_events.append({"day": item.day, "label": item.label, "event": event, "nav": money(nav)})

        rows.append(
            {
                "day": item.day,
                "label": item.label,
                "underlying_return_pct": pct(item.underlying_return),
                "underlying_index": money(underlying_index),
                "daily_levered_return_pct": pct(daily_levered_return),
                "etp_nav": money(nav),
                "simple_multiple_nav": money(simple_multiple_nav),
                "path_decay": money(path_decay),
            }
        )

    total_underlying_return = underlying_index / 100.0 - 1
    total_etp_return = nav / config.initial_nav - 1
    simple_multiple_return = product.leverage * total_underlying_return
    fee_drag = product.annual_fee * len(config.path) / TRADING_DAYS * config.initial_nav

    return {
        "schema_version": "0.2",
        "product": {
            "name": product.name,
            "ticker": product.ticker,
            "underlying": product.underlying,
            "leverage": product.leverage,
            "annual_fee_pct": pct(product.annual_fee),
            "currency": product.currency,
            "reset_frequency": product.reset_frequency,
        },
        "inputs": {
            "initial_nav": money(config.initial_nav),
            "days": len(config.path),
            "stop_loss_pct": _optional_pct(config.risk_band.stop_loss),
            "take_profit_pct": _optional_pct(config.risk_band.take_profit),
        },
        "summary": {
            "ending_underlying_index": money(underlying_index),
            "ending_etp_nav": money(nav),
            "underlying_return_pct": pct(total_underlying_return),
            "etp_return_pct": pct(total_etp_return),
            "simple_multiple_return_pct": pct(simple_multiple_return),
            "path_decay_vs_simple_multiple": money(nav - simple_multiple_nav),
            "estimated_fee_drag_nav_points": money(fee_drag),
        },
        "band_events": band_events,
        "warnings": warnings,
        "path": rows,
    }


def generate_scenario(kind: str, days: int) -> List[ScenarioDay]:
    if days <= 0:
        raise ValueError("days must be positive")
    patterns = {
        "trend": [
            ("Trend advance", 0.007),
            ("Orderly pullback", -0.002),
            ("Follow-through", 0.006),
            ("Consolidation", 0.001),
            ("Momentum close", 0.004),
        ],
        "chop": [
            ("Risk-on swing", 0.022),
            ("Risk-off swing", -0.021),
            ("Relief bid", 0.018),
            ("Fade", -0.017),
        ],
        "crash": [
            ("De-risking", -0.018),
            ("Liquidity break", -0.035),
            ("Gap lower", -0.055),
            ("Forced selling", -0.038),
            ("Weak bounce", 0.012),
        ],
        "rebound": [
            ("Capitulation", -0.032),
            ("Base building", -0.011),
            ("Stabilization", 0.009),
            ("Short-cover rally", 0.027),
            ("Follow-through", 0.019),
        ],
    }
    if kind not in patterns:
        raise ValueError(f"unknown scenario kind: {kind}")
    pattern = patterns[kind]
    generated: List[ScenarioDay] = []
    for index in range(days):
        label, underlying_return = pattern[index % len(pattern)]
        generated.append(ScenarioDay(day=index + 1, label=label, underlying_return=underlying_return))
    return generated


def exposure_report(manifest: PortfolioManifest, manifest_path: str) -> Dict[str, Any]:
    base_dir = Path(manifest_path).resolve().parent
    total_notional = sum(position.notional for position in manifest.positions)
    position_results: List[Dict[str, Any]] = []
    stop_events: List[Dict[str, Any]] = []
    warnings = [
        "Portfolio aggregation is scenario-based and does not model tax, borrow, spread, liquidity, or intraday stop execution.",
        "Weighted exposure uses starting notional weights and product daily leverage factors.",
    ]

    for position in manifest.positions:
        product_path = _resolve_fixture(base_dir, position.product_fixture)
        path_file = _resolve_fixture(base_dir, position.path_fixture)
        product = load_product(str(product_path))
        path = load_path(str(path_file))
        result = simulate(SimulationConfig(product, path, 100.0, position.risk_band))
        ending_nav = float(result["summary"]["ending_etp_nav"])
        ending_value = position.notional * ending_nav / 100.0
        position_path = []
        for row in result["path"]:
            value = position.notional * float(row["etp_nav"]) / 100.0
            day = int(row["day"])
            position_path.append({"day": day, "value": money(value)})
        for event in result["band_events"]:
            stop_events.append(
                {
                    "position_id": position.identifier,
                    "ticker": product.ticker,
                    "day": event["day"],
                    "label": event["label"],
                    "event": event["event"],
                    "nav": event["nav"],
                }
            )
        position_results.append(
            {
                "id": position.identifier,
                "ticker": product.ticker,
                "product": product.name,
                "notional": money(position.notional),
                "notional_weight_pct": pct(position.notional / total_notional),
                "leverage": product.leverage,
                "weighted_exposure": money(position.notional / total_notional * product.leverage),
                "ending_value": money(ending_value),
                "return_pct": result["summary"]["etp_return_pct"],
                "stop_loss_pct": _optional_pct(position.risk_band.stop_loss),
                "take_profit_pct": _optional_pct(position.risk_band.take_profit),
                "path": position_path,
            }
        )
        warnings.extend(result["warnings"])

    ending_value = sum(float(position["ending_value"]) for position in position_results)
    weighted_exposure = sum(float(position["weighted_exposure"]) for position in position_results)
    portfolio_path = _aggregate_position_paths(position_results, total_notional)
    return {
        "schema_version": "0.2",
        "portfolio": {"name": manifest.name, "base_currency": manifest.base_currency},
        "summary": {
            "starting_value": money(total_notional),
            "ending_value": money(ending_value),
            "return_pct": pct(ending_value / total_notional - 1),
            "weighted_exposure": money(weighted_exposure),
            "worst_drawdown_pct": pct(_worst_drawdown(portfolio_path, total_notional)),
        },
        "positions": position_results,
        "portfolio_path": [{"day": day, "value": money(portfolio_path[day])} for day in sorted(portfolio_path)],
        "stop_events": stop_events,
        "warnings": _unique(warnings),
    }


def stress_matrix(
    product: Any,
    selected_regimes: Optional[List[str]],
    initial_nav: float,
    risk_band: RiskBand,
    product_path: str,
) -> Dict[str, Any]:
    from .regimes import get_regime, regime_ids, regime_path

    if initial_nav <= 0:
        raise ValueError("--initial-nav must be positive")
    regime_selection = selected_regimes or regime_ids()
    rows: List[Dict[str, Any]] = []
    warning_pool: List[str] = []
    for regime_id in regime_selection:
        regime = get_regime(regime_id)
        result = simulate(SimulationConfig(product, regime_path(regime_id), initial_nav, risk_band))
        warnings = [str(item) for item in result["warnings"]]
        warning_pool.extend(warnings)
        band_events = list(result["band_events"])
        rows.append(
            {
                "regime": regime_id,
                "name": regime["name"],
                "days": result["inputs"]["days"],
                "underlying_return_pct": result["summary"]["underlying_return_pct"],
                "return_pct": result["summary"]["etp_return_pct"],
                "etp_return_pct": result["summary"]["etp_return_pct"],
                "path_decay_vs_simple_multiple": result["summary"]["path_decay_vs_simple_multiple"],
                "worst_drawdown_pct": pct(_nav_worst_drawdown(result["path"], initial_nav)),
                "stop_events": len(band_events),
                "stop_event_labels": [_band_event_label(event) for event in band_events],
                "warnings_count": len(warnings),
            }
        )
    return {
        "schema_version": STRESS_MATRIX_SCHEMA_VERSION,
        "document_type": "stress_matrix",
        "not_investment_advice": (
            "This stress matrix is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "product": {
            "name": product.name,
            "ticker": product.ticker,
            "underlying": product.underlying,
            "leverage": product.leverage,
            "annual_fee_pct": pct(product.annual_fee),
            "currency": product.currency,
            "reset_frequency": product.reset_frequency,
        },
        "inputs": {
            "product": product_path,
            "initial_nav": money(initial_nav),
            "regimes": list(regime_selection),
            "stop_loss_pct": _optional_pct(risk_band.stop_loss),
            "take_profit_pct": _optional_pct(risk_band.take_profit),
        },
        "rows": rows,
        "warnings": _unique(warning_pool),
        "provenance": {
            "command": "stress-matrix",
            "product": product_path,
            "regimes": list(regime_selection),
            "initial_nav": initial_nav,
            "stop_loss": risk_band.stop_loss,
            "take_profit": risk_band.take_profit,
        },
    }


def sensitivity_grid(
    product: ProductTerms,
    leverage_multipliers: Optional[List[float]],
    stop_losses: Optional[List[Optional[float]]],
    take_profits: Optional[List[Optional[float]]],
    selected_regimes: Optional[List[str]],
    initial_nav: float,
    product_path: str,
) -> Dict[str, Any]:
    from .regimes import get_regime, regime_ids, regime_path

    if initial_nav <= 0:
        raise ValueError("--initial-nav must be positive")
    leverage_values = leverage_multipliers or _default_leverage_grid(product.leverage)
    stop_values = stop_losses if stop_losses is not None else [None, 0.10, 0.15, 0.25]
    take_values = take_profits if take_profits is not None else [None, 0.15, 0.25, 0.40]
    regimes = selected_regimes or regime_ids()
    _validate_grid_values(leverage_values, stop_values, take_values)

    rows: List[Dict[str, Any]] = []
    cells: List[Dict[str, Any]] = []
    warning_pool: List[str] = []
    for leverage in leverage_values:
        scenario_product = ProductTerms(
            name=product.name,
            ticker=product.ticker,
            underlying=product.underlying,
            leverage=leverage,
            annual_fee=product.annual_fee,
            currency=product.currency,
            reset_frequency=product.reset_frequency,
            notes=product.notes,
        )
        for stop_loss in stop_values:
            for take_profit in take_values:
                combo_cells: List[Dict[str, Any]] = []
                for regime_id in regimes:
                    regime = get_regime(regime_id)
                    result = simulate(
                        SimulationConfig(
                            scenario_product,
                            regime_path(regime_id),
                            initial_nav,
                            RiskBand(stop_loss=stop_loss, take_profit=take_profit),
                        )
                    )
                    warnings = [str(item) for item in result["warnings"]]
                    warning_pool.extend(warnings)
                    band_events = list(result["band_events"])
                    cell = {
                        "leverage": money(leverage),
                        "stop_loss_pct": _optional_pct(stop_loss),
                        "take_profit_pct": _optional_pct(take_profit),
                        "regime": regime_id,
                        "name": regime["name"],
                        "days": result["inputs"]["days"],
                        "return_pct": result["summary"]["etp_return_pct"],
                        "worst_drawdown_pct": pct(_nav_worst_drawdown(result["path"], initial_nav)),
                        "path_decay_vs_simple_multiple": result["summary"]["path_decay_vs_simple_multiple"],
                        "stop_events": len(band_events),
                        "stop_event_labels": [_band_event_label(event) for event in band_events],
                        "warnings_count": len(warnings),
                    }
                    cells.append(cell)
                    combo_cells.append(cell)
                rows.append(_sensitivity_row(leverage, stop_loss, take_profit, combo_cells))
    return {
        "schema_version": SENSITIVITY_GRID_SCHEMA_VERSION,
        "document_type": "sensitivity_grid",
        "not_investment_advice": (
            "This sensitivity grid is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "product": {
            "name": product.name,
            "ticker": product.ticker,
            "underlying": product.underlying,
            "base_leverage": product.leverage,
            "annual_fee_pct": pct(product.annual_fee),
            "currency": product.currency,
            "reset_frequency": product.reset_frequency,
        },
        "inputs": {
            "product": product_path,
            "initial_nav": money(initial_nav),
            "regimes": list(regimes),
            "leverage_multipliers": [money(value) for value in leverage_values],
            "stop_loss_pct_grid": [_optional_pct(value) for value in stop_values],
            "take_profit_pct_grid": [_optional_pct(value) for value in take_values],
        },
        "summary": _sensitivity_summary(rows),
        "rows": rows,
        "cells": cells,
        "warnings": _unique(
            warning_pool
            + [
                "Sensitivity rows summarize deterministic built-in regimes and do not model execution, liquidity, tax, or suitability.",
                "Stop-loss and take-profit values are planning bands and do not guarantee fills.",
            ]
        ),
        "provenance": {
            "command": "sensitivity-grid",
            "product": product_path,
            "regimes": list(regimes),
            "initial_nav": initial_nav,
            "leverage_multipliers": leverage_values,
            "stop_losses": stop_values,
            "take_profits": take_values,
            "live_market_data": False,
            "shell_out": False,
        },
    }


def portfolio_sensitivity(
    manifest: PortfolioManifest,
    manifest_path: str,
    leverage_multipliers: Optional[List[float]],
    stop_losses: Optional[List[Optional[float]]],
    take_profits: Optional[List[Optional[float]]],
    selected_regimes: Optional[List[str]],
    initial_nav: float,
) -> Dict[str, Any]:
    if initial_nav <= 0:
        raise ValueError("--initial-nav must be positive")
    base_dir = Path(manifest_path).resolve().parent
    total_notional = sum(position.notional for position in manifest.positions)
    if total_notional <= 0:
        raise ValueError("portfolio manifest notional total must be positive")

    position_reports = []
    warning_pool = [
        "Portfolio sensitivity uses starting notional weights and deterministic built-in regimes.",
        "Aggregate worst-case exposure is a scenario-planning metric, not a margin, liquidity, tax, or suitability model.",
    ]
    for position in manifest.positions:
        product_path = _resolve_fixture(base_dir, position.product_fixture)
        product = load_product(str(product_path))
        grid = sensitivity_grid(
            product=product,
            leverage_multipliers=leverage_multipliers,
            stop_losses=stop_losses,
            take_profits=take_profits,
            selected_regimes=selected_regimes,
            initial_nav=initial_nav,
            product_path=_display_input_path(str(product_path), manifest_path),
        )
        weight = position.notional / total_notional
        summary = grid["summary"]
        weighted_base_exposure = weight * product.leverage
        worst_return_pct = _optional_float_value(summary.get("worst_return_pct"))
        modeled_loss = 0.0
        if worst_return_pct is not None and worst_return_pct < 0:
            modeled_loss = position.notional * -worst_return_pct / 100.0
        worst_leverage = _optional_float_value(summary.get("worst_return_leverage"))
        worst_weighted_exposure = weight * (worst_leverage if worst_leverage is not None else product.leverage)
        row = {
            "id": position.identifier,
            "ticker": product.ticker,
            "product": product.name,
            "notional": money(position.notional),
            "notional_weight_pct": pct(weight),
            "base_leverage": product.leverage,
            "weighted_base_exposure": money(weighted_base_exposure),
            "sensitivity_summary": summary,
            "worst_case": {
                "regime": summary.get("worst_return_regime"),
                "return_pct": summary.get("worst_return_pct"),
                "leverage": summary.get("worst_return_leverage"),
                "stop_loss_pct": summary.get("worst_return_stop_loss_pct"),
                "take_profit_pct": summary.get("worst_return_take_profit_pct"),
                "modeled_loss": money(modeled_loss),
                "weighted_exposure": money(worst_weighted_exposure),
                "path_decay_vs_simple_multiple": summary.get("worst_path_decay_vs_simple_multiple"),
                "max_stop_events": summary.get("max_stop_events"),
            },
            "grid_rows": grid["rows"],
        }
        position_reports.append(row)
        warning_pool.extend(str(item) for item in grid["warnings"])

    aggregate_worst_loss = sum(float(item["worst_case"]["modeled_loss"]) for item in position_reports)
    aggregate_worst_exposure = sum(float(item["worst_case"]["weighted_exposure"]) for item in position_reports)
    weakest = _portfolio_worst_position(position_reports)
    return {
        "schema_version": PORTFOLIO_SENSITIVITY_SCHEMA_VERSION,
        "document_type": "portfolio_sensitivity",
        "not_investment_advice": (
            "This portfolio sensitivity packet is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "portfolio": {"name": manifest.name, "base_currency": manifest.base_currency},
        "inputs": {
            "manifest": _display_input_path(manifest_path, manifest_path),
            "initial_nav": money(initial_nav),
            "regimes": selected_regimes or _all_regime_ids(),
            "leverage_multipliers": [money(value) for value in (leverage_multipliers or [])],
            "stop_loss_pct_grid": [_optional_pct(value) for value in stop_losses] if stop_losses is not None else None,
            "take_profit_pct_grid": [_optional_pct(value) for value in take_profits] if take_profits is not None else None,
        },
        "summary": {
            "positions": len(position_reports),
            "starting_value": money(total_notional),
            "base_weighted_exposure": money(sum(float(item["weighted_base_exposure"]) for item in position_reports)),
            "aggregate_worst_case_modeled_loss": money(aggregate_worst_loss),
            "aggregate_worst_case_loss_pct": pct(aggregate_worst_loss / total_notional),
            "aggregate_worst_case_weighted_exposure": money(aggregate_worst_exposure),
            "weakest_position_id": weakest.get("id"),
            "weakest_position_return_pct": weakest.get("worst_case", {}).get("return_pct"),
            "weakest_position_regime": weakest.get("worst_case", {}).get("regime"),
        },
        "positions": position_reports,
        "warnings": _unique(warning_pool),
        "provenance": {
            "command": "portfolio-sensitivity",
            "manifest": _display_input_path(manifest_path, manifest_path),
            "live_market_data": False,
            "shell_out": False,
        },
    }


def position_size_plan(
    simulation: Dict[str, Any],
    account_value: float,
    max_loss_budget: float,
    stop_loss: Optional[float],
    source: Dict[str, Any],
) -> Dict[str, Any]:
    if account_value <= 0:
        raise ValueError("--account-value must be positive")
    if max_loss_budget <= 0:
        raise ValueError("loss budget must be positive")
    if max_loss_budget > account_value:
        raise ValueError("loss budget must not exceed account value")

    effective_stop = stop_loss
    if effective_stop is None:
        effective_stop = _pct_to_decimal(simulation.get("inputs", {}).get("stop_loss_pct"))
    if effective_stop is None:
        effective_stop = _pct_to_decimal(simulation.get("risk_bands", {}).get("stop_loss_pct"))
    if effective_stop is not None and not 0 < effective_stop < 1:
        raise ValueError("--stop-loss must be a decimal between 0 and 1")

    loss_rate, loss_basis = _position_loss_rate(simulation, effective_stop)
    if loss_rate <= 0:
        raise ValueError("modeled loss is zero; provide --stop-loss or use a loss-making scenario")

    product = simulation["product"]
    recommended_notional = max_loss_budget / loss_rate
    modeled_loss = recommended_notional * loss_rate
    exposure_multiple = recommended_notional * float(product["leverage"]) / account_value
    currency = str(product.get("currency", "USD"))
    return {
        "schema_version": POSITION_SIZE_SCHEMA_VERSION,
        "document_type": "position_size_plan",
        "not_investment_advice": (
            "This position sizing planner is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "product": product,
        "inputs": {
            "account_value": money(account_value),
            "max_loss_budget": money(max_loss_budget),
            "risk_budget_pct": pct(max_loss_budget / account_value),
            "stop_loss_pct": _optional_pct(effective_stop),
            "loss_basis": loss_basis,
            "currency": currency,
        },
        "recommendation": {
            "recommended_notional": money(recommended_notional),
            "max_shares": None,
            "max_shares_placeholder": "Divide recommended_notional by the intended execution price; no live price is modeled.",
            "modeled_loss_at_stop": money(modeled_loss),
            "modeled_loss_pct_of_account": pct(modeled_loss / account_value),
            "exposure_multiple": money(exposure_multiple),
        },
        "scenario": _position_scenario_summary(simulation),
        "checklist": position_size_checklist(loss_basis),
        "warnings": _unique(
            list(simulation.get("warnings", []))
            + [
                "Recommended notional is a deterministic planning output, not a trade recommendation.",
                "Share count is a placeholder because no live or execution price is modeled.",
                "Stop-loss levels are planning inputs and do not guarantee execution at the modeled loss.",
            ]
        ),
        "provenance": source,
    }


def position_size_checklist(loss_basis: str) -> List[str]:
    items = [
        "Confirm account value and loss budget before using the notional figure.",
        "Convert notional to shares with the intended execution price outside this model.",
        "Check liquidity, spreads, trading halts, and gap risk before relying on a stop.",
        "Compare exposure multiple with portfolio concentration and leverage limits.",
        "Record that this output is for scenario planning and is not investment advice.",
    ]
    if loss_basis != "stop_loss":
        items.append("Add an explicit stop-loss if the scenario loss is only a rough sizing proxy.")
    return items


def build_warnings(config: SimulationConfig) -> List[str]:
    product = config.product
    warnings = [
        "Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.",
        "Scenario output is not investment advice and does not predict future returns.",
    ]
    if abs(product.leverage) >= 2:
        warnings.append("Large daily moves can compound quickly and may create losses larger than a simple one-day estimate.")
    if any(day.underlying_return <= -1 / abs(product.leverage) for day in config.path if product.leverage > 0):
        warnings.append("At least one scenario day can drive the modeled ETP NAV to zero or below before market safeguards.")
    if product.annual_fee > 0:
        warnings.append("Fee drag is approximated as a constant daily deduction from the leveraged daily return.")
    return warnings


def _resolve_fixture(base_dir: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    candidate = base_dir / path
    if candidate.exists():
        return candidate
    return path


def _worst_drawdown(portfolio_path: Dict[int, float], starting_value: float) -> float:
    peak = starting_value
    worst = 0.0
    for day in sorted(portfolio_path):
        value = portfolio_path[day]
        if value > peak:
            peak = value
        drawdown = value / peak - 1
        if drawdown < worst:
            worst = drawdown
    return worst


def _nav_worst_drawdown(path: List[Dict[str, Any]], initial_nav: float) -> float:
    peak = initial_nav
    worst = 0.0
    for row in path:
        value = float(row["etp_nav"])
        if value > peak:
            peak = value
        drawdown = value / peak - 1
        if drawdown < worst:
            worst = drawdown
    return worst


def _band_event_label(event: Dict[str, Any]) -> str:
    return f"day {event['day']} {event['event']} at NAV {event['nav']}"


def _aggregate_position_paths(position_results: List[Dict[str, Any]], starting_value: float) -> Dict[int, float]:
    max_day = 0
    for position in position_results:
        for row in position["path"]:
            max_day = max(max_day, int(row["day"]))
    aggregate: Dict[int, float] = {}
    last_values = {position["id"]: float(position["notional"]) for position in position_results}
    for day in range(1, max_day + 1):
        for position in position_results:
            for row in position["path"]:
                if int(row["day"]) == day:
                    last_values[position["id"]] = float(row["value"])
                    break
        aggregate[day] = sum(last_values.values()) if last_values else starting_value
    return aggregate


def _unique(items: List[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _hit_stop(nav: float, stop_loss: Optional[float], initial_nav: float) -> bool:
    if stop_loss is None:
        return False
    return nav <= initial_nav * (1 - stop_loss)


def _hit_take(nav: float, take_profit: Optional[float], initial_nav: float) -> bool:
    if take_profit is None:
        return False
    return nav >= initial_nav * (1 + take_profit)


def _optional_pct(value: Optional[float]) -> Optional[float]:
    if value is None:
        return None
    return pct(value)


def _default_leverage_grid(product_leverage: float) -> List[float]:
    sign = -1.0 if product_leverage < 0 else 1.0
    return [sign * 1.0, sign * 2.0, sign * 3.0]


def _all_regime_ids() -> List[str]:
    from .regimes import regime_ids

    return regime_ids()


def _validate_grid_values(
    leverage_values: List[float],
    stop_values: List[Optional[float]],
    take_values: List[Optional[float]],
) -> None:
    if not leverage_values:
        raise ValueError("leverage grid must contain at least one value")
    if not stop_values:
        raise ValueError("stop-loss grid must contain at least one value")
    if not take_values:
        raise ValueError("take-profit grid must contain at least one value")
    if any(value == 0 for value in leverage_values):
        raise ValueError("leverage multipliers must not include zero")
    for value in stop_values:
        if value is not None and not 0 < value < 1:
            raise ValueError("stop-loss grid values must be decimals between 0 and 1, or none")
    for value in take_values:
        if value is not None and value <= 0:
            raise ValueError("take-profit grid values must be positive decimals, or none")


def _sensitivity_row(
    leverage: float,
    stop_loss: Optional[float],
    take_profit: Optional[float],
    combo_cells: List[Dict[str, Any]],
) -> Dict[str, Any]:
    worst_return = _lowest_cell(combo_cells, "return_pct")
    worst_drawdown = _lowest_cell(combo_cells, "worst_drawdown_pct")
    worst_decay = _lowest_cell(combo_cells, "path_decay_vs_simple_multiple")
    return {
        "leverage": money(leverage),
        "stop_loss_pct": _optional_pct(stop_loss),
        "take_profit_pct": _optional_pct(take_profit),
        "regimes": len(combo_cells),
        "worst_return_regime": worst_return.get("regime"),
        "worst_return_pct": worst_return.get("return_pct"),
        "largest_drawdown_regime": worst_drawdown.get("regime"),
        "largest_drawdown_pct": worst_drawdown.get("worst_drawdown_pct"),
        "worst_path_decay_regime": worst_decay.get("regime"),
        "worst_path_decay_vs_simple_multiple": worst_decay.get("path_decay_vs_simple_multiple"),
        "stop_events": sum(int(cell.get("stop_events", 0)) for cell in combo_cells),
        "warnings_count": sum(int(cell.get("warnings_count", 0)) for cell in combo_cells),
    }


def _sensitivity_summary(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    worst_return = _lowest_cell(rows, "worst_return_pct")
    worst_decay = _lowest_cell(rows, "worst_path_decay_vs_simple_multiple")
    most_events = max(rows, key=lambda row: int(row.get("stop_events", 0))) if rows else {}
    return {
        "combinations": len(rows),
        "worst_return_pct": worst_return.get("worst_return_pct"),
        "worst_return_regime": worst_return.get("worst_return_regime"),
        "worst_return_leverage": worst_return.get("leverage"),
        "worst_return_stop_loss_pct": worst_return.get("stop_loss_pct"),
        "worst_return_take_profit_pct": worst_return.get("take_profit_pct"),
        "worst_path_decay_vs_simple_multiple": worst_decay.get("worst_path_decay_vs_simple_multiple"),
        "worst_path_decay_regime": worst_decay.get("worst_path_decay_regime"),
        "max_stop_events": most_events.get("stop_events"),
        "max_stop_events_leverage": most_events.get("leverage"),
        "max_stop_events_stop_loss_pct": most_events.get("stop_loss_pct"),
        "max_stop_events_take_profit_pct": most_events.get("take_profit_pct"),
    }


def _lowest_cell(rows: List[Dict[str, Any]], key: str) -> Dict[str, Any]:
    numeric = [row for row in rows if isinstance(row.get(key), (int, float))]
    if not numeric:
        return {}
    return min(numeric, key=lambda row: float(row[key]))


def _portfolio_worst_position(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    numeric = [
        row
        for row in rows
        if isinstance(row.get("worst_case", {}).get("return_pct"), (int, float))
    ]
    if not numeric:
        return {}
    return min(numeric, key=lambda row: float(row["worst_case"]["return_pct"]))


def _optional_float_value(value: Any) -> Optional[float]:
    if value is None:
        return None
    return float(value)


def _display_input_path(path: str, _anchor: str) -> str:
    value = Path(path)
    return value.as_posix() if not value.is_absolute() else value.name


def _pct_to_decimal(value: Any) -> Optional[float]:
    if value is None:
        return None
    return float(value) / 100.0


def _position_loss_rate(simulation: Dict[str, Any], stop_loss: Optional[float]) -> tuple[float, str]:
    if stop_loss is not None:
        return stop_loss, "stop_loss"
    path = simulation.get("path")
    initial_nav = float(simulation.get("inputs", {}).get("initial_nav", 100.0))
    if isinstance(path, list) and path:
        lowest_nav = min(float(row["etp_nav"]) for row in path)
        return max(0.0, 1 - lowest_nav / initial_nav), "scenario_worst_modeled_nav"
    scenario = simulation.get("scenario", {})
    etp_return_pct = scenario.get("etp_return_pct")
    if etp_return_pct is not None:
        return max(0.0, -float(etp_return_pct) / 100.0), "pretrade_scenario_return"
    summary = simulation.get("summary", {})
    etp_return_pct = summary.get("etp_return_pct")
    if etp_return_pct is not None:
        return max(0.0, -float(etp_return_pct) / 100.0), "scenario_return"
    return 0.0, "unknown"


def _position_scenario_summary(simulation: Dict[str, Any]) -> Dict[str, Any]:
    if "scenario" in simulation:
        scenario = simulation["scenario"]
        return {
            "days": scenario.get("days"),
            "ending_etp_nav": scenario.get("ending_etp_nav"),
            "etp_return_pct": scenario.get("etp_return_pct"),
            "underlying_return_pct": scenario.get("underlying_return_pct"),
            "path_decay_vs_simple_multiple": scenario.get("path_decay_vs_simple_multiple"),
        }
    summary = simulation.get("summary", {})
    inputs = simulation.get("inputs", {})
    return {
        "days": inputs.get("days"),
        "ending_etp_nav": summary.get("ending_etp_nav"),
        "etp_return_pct": summary.get("etp_return_pct"),
        "underlying_return_pct": summary.get("underlying_return_pct"),
        "path_decay_vs_simple_multiple": summary.get("path_decay_vs_simple_multiple"),
    }
