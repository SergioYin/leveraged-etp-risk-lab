from __future__ import annotations

from typing import Any, Dict, List, Optional

from .models import SimulationConfig


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
        "schema_version": "0.1",
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
