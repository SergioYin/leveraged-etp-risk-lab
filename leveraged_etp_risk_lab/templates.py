from __future__ import annotations

from typing import Any, Dict, List


TEMPLATE_SCHEMA_VERSION = "0.4"


_TEMPLATES: List[Dict[str, Any]] = [
    {
        "id": "generic-2x-long-equity",
        "name": "Generic 2x Long Equity Daily Reset ETP",
        "ticker": "EQTY2X",
        "underlying": "Broad equity reference basket",
        "leverage": 2,
        "annual_fee": 0.0095,
        "currency": "USD",
        "reset_frequency": "daily",
        "notes": "Generic educational template, not a listed product.",
        "risk_notes": [
            "Daily 2x compounding can diverge from twice the multi-day underlying return.",
            "Equity drawdowns can compound quickly when exposure is reset each day.",
            "Fee drag, spreads, liquidity, taxes, and tracking error are not modeled in the product file.",
        ],
        "use_cases": [
            "Broad-market bullish scenario planning.",
            "Comparing trend and chop paths before sizing a short holding-period trade.",
            "Educational examples where a moderate long leverage factor is needed.",
        ],
    },
    {
        "id": "generic-3x-long-index",
        "name": "Generic 3x Long Index Daily Reset ETP",
        "ticker": "IDX3X",
        "underlying": "Large-cap equity index reference",
        "leverage": 3,
        "annual_fee": 0.0095,
        "currency": "USD",
        "reset_frequency": "daily",
        "notes": "Generic educational template, not a listed product.",
        "risk_notes": [
            "3x exposure magnifies daily gains and losses and can produce large path-dependent decay.",
            "A one-day index loss near one third can drive modeled NAV toward zero before safeguards.",
            "Best modeled with explicit stop-loss and take-profit bands because losses accelerate.",
        ],
        "use_cases": [
            "High-conviction index trend stress tests.",
            "Volatility decay demonstrations in alternating up/down paths.",
            "Portfolio exposure aggregation with a high-beta long position.",
        ],
    },
    {
        "id": "generic--2x-inverse-index",
        "name": "Generic -2x Inverse Index Daily Reset ETP",
        "ticker": "INV2X",
        "underlying": "Large-cap equity index reference",
        "leverage": -2,
        "annual_fee": 0.0105,
        "currency": "USD",
        "reset_frequency": "daily",
        "notes": "Generic educational template, not a listed product.",
        "risk_notes": [
            "Inverse daily reset products can lose value in rising markets and in volatile sideways markets.",
            "Multi-day inverse returns are path dependent and should not be treated as a simple hedge ratio.",
            "Short-lived hedging assumptions can fail if the underlying rebounds sharply.",
        ],
        "use_cases": [
            "Generic bearish index scenario planning.",
            "Hedge-ratio education for daily reset inverse exposure.",
            "Stress testing rebound risk after a market selloff.",
        ],
    },
    {
        "id": "generic-2x-single-stock",
        "name": "Generic 2x Single-Stock Daily Reset ETP",
        "ticker": "STK2X",
        "underlying": "Single-stock reference share",
        "leverage": 2,
        "annual_fee": 0.0115,
        "currency": "USD",
        "reset_frequency": "daily",
        "notes": "Generic educational template, not a listed product.",
        "risk_notes": [
            "Single-stock gaps, earnings, halts, and idiosyncratic news can dominate modeled daily paths.",
            "2x daily reset exposure can compound losses rapidly when the reference share gaps lower.",
            "Scenario output does not model issuer call features, liquidity, spreads, taxes, or suitability.",
        ],
        "use_cases": [
            "Single-name event-risk stress testing.",
            "Gap-down and partial-recovery path examples.",
            "Educational comparison against broad-index leveraged products.",
        ],
    },
]


def template_gallery() -> Dict[str, Any]:
    return {
        "schema_version": TEMPLATE_SCHEMA_VERSION,
        "document_type": "template_gallery",
        "templates": [dict(item) for item in _TEMPLATES],
    }


def template_ids() -> List[str]:
    return [item["id"] for item in _TEMPLATES]


def get_template(template_id: str) -> Dict[str, Any]:
    for item in _TEMPLATES:
        if item["id"] == template_id:
            return dict(item)
    raise ValueError(f"unknown template id: {template_id}")


def template_product(template_id: str) -> Dict[str, Any]:
    template = get_template(template_id)
    return {
        "name": template["name"],
        "ticker": template["ticker"],
        "underlying": template["underlying"],
        "leverage": template["leverage"],
        "annual_fee": template["annual_fee"],
        "currency": template["currency"],
        "reset_frequency": template["reset_frequency"],
        "notes": template["notes"],
    }
