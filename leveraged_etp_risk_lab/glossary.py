from __future__ import annotations

from typing import Any, Dict, List


SCHEMA_VERSION = "0.14"
NOT_INVESTMENT_ADVICE = (
    "This glossary is for leveraged product education and scenario planning only. "
    "It is not investment advice, a recommendation, or a suitability determination."
)


TERMS: List[Dict[str, Any]] = [
    {
        "id": "daily_reset",
        "term": "Daily reset",
        "plain_language": (
            "A daily-reset product targets its stated leverage for one trading day at a time, then resets "
            "exposure for the next day."
        ),
        "why_it_matters": (
            "Multi-day returns compound from the sequence of daily moves, so they can differ from a simple "
            "multiple of the underlying's total return."
        ),
        "example": (
            "A 3x product that gains 3% on day one does not keep the same dollar exposure on day two; "
            "the next day's target is reset from the new NAV."
        ),
        "related_terms": ["leverage_factor", "path_decay", "volatility_decay"],
    },
    {
        "id": "path_decay",
        "term": "Path decay",
        "plain_language": (
            "Path decay is the difference between a leveraged product's compounded path return and a simple "
            "leverage multiple of the underlying's start-to-end return."
        ),
        "why_it_matters": (
            "It highlights that order, reversals, and compounding can dominate the headline leverage factor "
            "over more than one day."
        ),
        "example": (
            "A choppy underlying path can finish close to flat while a daily-reset leveraged product loses "
            "value because gains and losses compound from changing bases."
        ),
        "related_terms": ["daily_reset", "volatility_decay", "leverage_factor"],
    },
    {
        "id": "volatility_decay",
        "term": "Volatility decay",
        "plain_language": (
            "Volatility decay is the drag that can appear when alternating up and down moves compound in a "
            "daily-reset leveraged product."
        ),
        "why_it_matters": (
            "Higher leverage and larger daily swings can make the drag more visible, especially in sideways "
            "or mean-reverting markets."
        ),
        "example": (
            "After a -5% underlying day followed by a +5% day, the underlying is not fully back to even; "
            "a leveraged product magnifies that compounding effect."
        ),
        "related_terms": ["path_decay", "daily_reset", "leverage_factor"],
    },
    {
        "id": "leverage_factor",
        "term": "Leverage factor",
        "plain_language": (
            "The leverage factor is the stated daily exposure target, such as 2x, 3x, or -2x for inverse exposure."
        ),
        "why_it_matters": (
            "It scales daily underlying moves before fees and compounding, but it is not a guarantee of the "
            "same multiple over longer holding periods."
        ),
        "example": (
            "If the underlying rises 1% in one day, a 3x daily product targets roughly +3% before fees and "
            "tracking differences."
        ),
        "related_terms": ["daily_reset", "path_decay", "gap_risk"],
    },
    {
        "id": "stop_loss_band",
        "term": "Stop-loss band",
        "plain_language": (
            "A stop-loss band is a planning threshold for reviewing or exiting a position after modeled losses."
        ),
        "why_it_matters": (
            "It helps translate risk tolerance into a preplanned level, but actual execution can differ in "
            "fast or gapping markets."
        ),
        "example": (
            "A 15% stop-loss band on a 100 NAV scenario flags review if modeled NAV reaches 85 or lower."
        ),
        "related_terms": ["take_profit_band", "gap_risk", "max_loss_budget"],
    },
    {
        "id": "take_profit_band",
        "term": "Take-profit band",
        "plain_language": (
            "A take-profit band is a planning threshold for reviewing gains or reducing exposure after a "
            "modeled favorable move."
        ),
        "why_it_matters": (
            "It supports disciplined scenario planning, but it does not predict where liquidity or execution "
            "will be available."
        ),
        "example": (
            "A 20% take-profit band on a 100 NAV scenario flags review if modeled NAV reaches 120 or higher."
        ),
        "related_terms": ["stop_loss_band", "premium_discount", "iNAV"],
    },
    {
        "id": "gap_risk",
        "term": "Gap risk",
        "plain_language": (
            "Gap risk is the risk that a product or its underlying opens sharply away from the prior price, "
            "skipping over planned review levels."
        ),
        "why_it_matters": (
            "Stop-loss bands and sizing assumptions may not cap losses if prices move discontinuously or "
            "liquidity is thin."
        ),
        "example": (
            "A product may move from above a stop-loss band to well below it between sessions after an "
            "earnings, macro, or regulatory event."
        ),
        "related_terms": ["stop_loss_band", "max_loss_budget", "leverage_factor"],
    },
    {
        "id": "iNAV",
        "term": "Indicative NAV (iNAV)",
        "plain_language": (
            "Indicative NAV is an intraday estimate of a fund's net asset value based on available underlying "
            "market data."
        ),
        "why_it_matters": (
            "It can help compare market price with estimated portfolio value, while still being an estimate "
            "that may lag or be less reliable in stressed markets."
        ),
        "example": (
            "If market price is above iNAV, the product may be trading at a premium to the estimated value "
            "of its holdings."
        ),
        "related_terms": ["premium_discount", "take_profit_band", "gap_risk"],
    },
    {
        "id": "premium_discount",
        "term": "Premium/discount",
        "plain_language": (
            "Premium or discount compares a product's market price with its NAV or indicative NAV."
        ),
        "why_it_matters": (
            "Large differences can signal trading friction, stale estimates, stressed liquidity, or creation "
            "and redemption constraints."
        ),
        "example": (
            "A product trading at 101 when estimated NAV is 100 is trading at about a 1% premium."
        ),
        "related_terms": ["iNAV", "gap_risk", "take_profit_band"],
    },
    {
        "id": "max_loss_budget",
        "term": "Maximum loss budget",
        "plain_language": (
            "A maximum loss budget is the amount of account value a user decides to put at risk in a scenario plan."
        ),
        "why_it_matters": (
            "It connects position size, stop-loss assumptions, and portfolio concentration in one explicit "
            "planning constraint."
        ),
        "example": (
            "With a 750 currency-unit loss budget and a 15% modeled stop, the corresponding notional basis "
            "is 5,000 before considering execution and gap risk."
        ),
        "related_terms": ["stop_loss_band", "gap_risk", "leverage_factor"],
    },
]


def glossary_packet() -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "document_type": "glossary",
        "not_investment_advice": NOT_INVESTMENT_ADVICE,
        "summary": {"terms": len(TERMS)},
        "terms": [dict(term) for term in TERMS],
        "provenance": {"command": "glossary-list"},
    }


def explain_term(term_id: str) -> Dict[str, Any]:
    normalized = term_id.strip()
    for term in TERMS:
        if term["id"] == normalized:
            return {
                "schema_version": SCHEMA_VERSION,
                "document_type": "glossary_term",
                "not_investment_advice": NOT_INVESTMENT_ADVICE,
                "term": dict(term),
                "provenance": {"command": "explain-term", "term": normalized},
            }
    valid = ", ".join(term["id"] for term in TERMS)
    raise ValueError(f"unknown glossary term {term_id!r}; valid terms: {valid}")


def term_ids() -> List[str]:
    return [term["id"] for term in TERMS]
