from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .io import load_path, load_product
from .models import PortfolioManifest, ScenarioDay, SimulationConfig


TRADING_DAYS = 252


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
