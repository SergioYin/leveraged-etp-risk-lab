from __future__ import annotations

from typing import Any, Dict, List, Optional

from .models import ScenarioDay


REGIME_SCHEMA_VERSION = "0.7"


_REGIMES: List[Dict[str, Any]] = [
    {
        "id": "trend_up",
        "name": "Trend Up",
        "description": "Orderly rising market with shallow pauses and positive drift.",
        "default_days": 12,
        "tags": ["trend", "bullish", "low_chop"],
        "risk_notes": [
            "Leveraged long products may compound favorably, but late pullbacks can erase gains quickly.",
            "Inverse products can lose value steadily even without a single large up day.",
        ],
        "use_cases": [
            "Testing positive compounding in a persistent advance.",
            "Comparing stop and take-profit bands after a favorable start.",
        ],
        "path": [
            ("Opening bid", 0.006),
            ("Orderly advance", 0.008),
            ("Shallow pause", -0.002),
            ("Breakout follow-through", 0.011),
            ("Consolidation", 0.001),
            ("Momentum close", 0.007),
        ],
    },
    {
        "id": "trend_down",
        "name": "Trend Down",
        "description": "Persistent selloff with brief relief rallies that fail.",
        "default_days": 12,
        "tags": ["trend", "bearish", "drawdown"],
        "risk_notes": [
            "Long leveraged products can compound losses faster than a simple multiple suggests.",
            "Brief relief rallies can materially hurt inverse daily reset exposure sizing.",
        ],
        "use_cases": [
            "Stress testing long leveraged drawdown paths.",
            "Reviewing inverse product behavior during failed bounces.",
        ],
        "path": [
            ("Risk-off open", -0.007),
            ("Follow-through selling", -0.012),
            ("Weak relief", 0.004),
            ("Lower low", -0.015),
            ("Failed bounce", 0.003),
            ("De-risking close", -0.009),
        ],
    },
    {
        "id": "chop",
        "name": "Chop",
        "description": "Alternating up and down sessions with limited net direction.",
        "default_days": 12,
        "tags": ["sideways", "volatility_decay", "mean_reversion"],
        "risk_notes": [
            "Alternating returns can create path decay even when the underlying ends near flat.",
            "Stop and take-profit bands may trigger repeatedly in both directions.",
        ],
        "use_cases": [
            "Demonstrating volatility decay from daily reset leverage.",
            "Comparing trend assumptions against sideways whipsaw conditions.",
        ],
        "path": [
            ("Risk-on swing", 0.022),
            ("Risk-off swing", -0.021),
            ("Relief bid", 0.018),
            ("Fade", -0.017),
        ],
    },
    {
        "id": "gap_down",
        "name": "Gap Down",
        "description": "Large downside gap followed by unstable trading and a partial attempt to stabilize.",
        "default_days": 8,
        "tags": ["gap", "event_risk", "single_stock"],
        "risk_notes": [
            "Gap moves can bypass planning bands and create modeled losses before any exit is possible.",
            "Single-name event risk can dominate management-fee or ordinary volatility assumptions.",
        ],
        "use_cases": [
            "Single-stock earnings or regulatory event stress tests.",
            "Checking whether a loss budget survives a discontinuous first move.",
        ],
        "path": [
            ("Event gap lower", -0.085),
            ("Forced selling", -0.032),
            ("Volatile bounce", 0.026),
            ("Second wave", -0.021),
            ("Stabilization attempt", 0.012),
        ],
    },
    {
        "id": "rebound",
        "name": "Rebound",
        "description": "Initial drawdown followed by stabilization and a sharp recovery attempt.",
        "default_days": 10,
        "tags": ["reversal", "recovery", "short_covering"],
        "risk_notes": [
            "Losses early in the path reduce the NAV base that participates in a later rebound.",
            "Inverse products can give back gains quickly if the recovery accelerates.",
        ],
        "use_cases": [
            "Testing whether a leveraged position can recover after an early stop zone.",
            "Reviewing inverse hedge exit rules after an initial selloff.",
        ],
        "path": [
            ("Capitulation", -0.032),
            ("Base building", -0.011),
            ("Stabilization", 0.009),
            ("Short-cover rally", 0.027),
            ("Follow-through", 0.019),
        ],
    },
    {
        "id": "volatility_cluster",
        "name": "Volatility Cluster",
        "description": "Sequence of large moves in both directions, modeling clustered high volatility.",
        "default_days": 12,
        "tags": ["high_volatility", "cluster", "stress"],
        "risk_notes": [
            "Large alternating moves can produce material decay even if the final underlying move is modest.",
            "Modeled NAV can become highly sensitive to the order of daily returns.",
        ],
        "use_cases": [
            "Stress testing path dependence during high-volatility regimes.",
            "Comparing risk bands under clustered large-move conditions.",
        ],
        "path": [
            ("Volatility shock", -0.041),
            ("Sharp relief", 0.036),
            ("Renewed pressure", -0.029),
            ("Fast squeeze", 0.033),
            ("Liquidity fade", -0.024),
            ("Wide-range close", 0.018),
        ],
    },
]


def regime_gallery() -> Dict[str, Any]:
    return {
        "schema_version": REGIME_SCHEMA_VERSION,
        "document_type": "regime_gallery",
        "regimes": [_public_regime(item) for item in _REGIMES],
    }


def regime_ids() -> List[str]:
    return [item["id"] for item in _REGIMES]


def get_regime(regime_id: str) -> Dict[str, Any]:
    for item in _REGIMES:
        if item["id"] == regime_id:
            return _public_regime(item)
    raise ValueError(f"unknown regime id: {regime_id}")


def regime_path(regime_id: str, days: Optional[int] = None) -> List[ScenarioDay]:
    source = _private_regime(regime_id)
    count = int(days if days is not None else source["default_days"])
    if count <= 0:
        raise ValueError("days must be positive")
    pattern = source["path"]
    rows: List[ScenarioDay] = []
    for index in range(count):
        label, underlying_return = pattern[index % len(pattern)]
        rows.append(ScenarioDay(day=index + 1, label=label, underlying_return=underlying_return))
    return rows


def _private_regime(regime_id: str) -> Dict[str, Any]:
    for item in _REGIMES:
        if item["id"] == regime_id:
            return item
    raise ValueError(f"unknown regime id: {regime_id}")


def _public_regime(item: Dict[str, Any]) -> Dict[str, Any]:
    path = item["path"]
    return {
        "id": item["id"],
        "name": item["name"],
        "description": item["description"],
        "default_days": item["default_days"],
        "tags": list(item["tags"]),
        "risk_notes": list(item["risk_notes"]),
        "use_cases": list(item["use_cases"]),
        "sample_path": [
            {"day": index + 1, "label": label, "underlying_return": underlying_return}
            for index, (label, underlying_return) in enumerate(path)
        ],
    }
