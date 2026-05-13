from __future__ import annotations

from typing import Any, Dict, List, Optional


SCHEMA_VERSION = "0.16"
PROFILE_IDS = ["default", "conservative", "active-trader", "thesis-review"]


REQUIRED_FACTSHEET_FIELDS = [
    "issuer",
    "exchange",
    "underlying",
    "leverage_factor",
    "daily_reset",
    "annual_fee",
    "currency",
    "liquidity_spread",
    "inav",
    "premium_discount",
]


PROFILES = {
    "default": {
        "name": "Default",
        "description": "Baseline review rules for generic daily-reset leveraged ETP scenario planning.",
        "max_holding_days": 5,
        "max_account_risk_pct_placeholder": "Set a user-defined account risk cap before sizing; no default is implied.",
        "required_scenario_regimes": ["trend_up", "trend_down", "chop", "gap_down"],
        "mandatory_checklist_questions": [
            "Have product objective, leverage factor, reset frequency, fees, and currency been verified?",
            "Does the planned holding period fit the product objective and modeled path risk?",
            "Has the scenario been tested against both trending and choppy paths?",
            "Are stop-loss and take-profit review levels recorded before entry?",
            "Is the maximum tolerable loss documented outside the model output?",
        ],
        "stop_take_review_defaults": {
            "stop_loss_pct": 15.0,
            "take_profit_pct": 20.0,
            "review_frequency": "daily close",
            "gap_review": "Review immediately after an overnight gap or modeled stop breach.",
        },
    },
    "conservative": {
        "name": "Conservative",
        "description": "Tighter holding-period and review rules for lower tolerance planning.",
        "max_holding_days": 2,
        "max_account_risk_pct_placeholder": "Use a smaller user-defined account risk cap; this package does not set suitability limits.",
        "required_scenario_regimes": ["trend_down", "chop", "gap_down", "volatility_cluster"],
        "mandatory_checklist_questions": [
            "Is there a documented reason to use a leveraged product instead of lower-leverage exposure?",
            "Can the position be exited if spreads widen or the product trades at a premium/discount?",
            "Does the modeled loss remain tolerable after applying gap-risk judgment outside this tool?",
            "Have concentration and correlated portfolio exposure been reviewed?",
            "Is there a same-day review trigger for adverse movement?",
        ],
        "stop_take_review_defaults": {
            "stop_loss_pct": 8.0,
            "take_profit_pct": 12.0,
            "review_frequency": "same day and daily close",
            "gap_review": "Review before adding exposure after any gap-down or volatility-cluster regime result.",
        },
    },
    "active-trader": {
        "name": "Active Trader",
        "description": "Intraday-oriented review rules for short planned holding periods and fast exits.",
        "max_holding_days": 1,
        "max_account_risk_pct_placeholder": "Set per-trade and per-day account risk caps outside this package before using the profile.",
        "required_scenario_regimes": ["trend_up", "trend_down", "gap_down", "rebound", "volatility_cluster"],
        "mandatory_checklist_questions": [
            "Are entry, exit, stop, and take-profit review levels defined before the trade?",
            "Have intraday liquidity, spreads, halt risk, and closing-auction exposure been reviewed?",
            "Is there a rule for not averaging down after a stop breach?",
            "Does the product have event risk during the intended trading window?",
            "Has position size been checked against both stop loss and worst modeled regime loss?",
        ],
        "stop_take_review_defaults": {
            "stop_loss_pct": 5.0,
            "take_profit_pct": 10.0,
            "review_frequency": "intraday and daily close",
            "gap_review": "Review immediately after market open gaps, halts, or fast spread widening.",
        },
    },
    "thesis-review": {
        "name": "Thesis Review",
        "description": "Rules for linking a written thesis to factsheet checks, stress regimes, and review questions.",
        "max_holding_days": 10,
        "max_account_risk_pct_placeholder": "Document a thesis-specific account risk cap before sizing; leave unset if no cap is approved.",
        "required_scenario_regimes": ["trend_up", "trend_down", "chop", "gap_down", "rebound", "volatility_cluster"],
        "mandatory_checklist_questions": [
            "What specific thesis claim would invalidate the trade or require size reduction?",
            "Which factsheet fields or product terms are critical to the thesis?",
            "Which stress-matrix regime most directly challenges the thesis?",
            "What metric, warning, or watchlist entry triggers the next review?",
            "Has the thesis been updated after modeled path decay, drawdown, and stop/take events?",
        ],
        "stop_take_review_defaults": {
            "stop_loss_pct": 12.0,
            "take_profit_pct": 18.0,
            "review_frequency": "daily close and thesis event",
            "gap_review": "Review thesis language after any gap, rebound failure, or volatility-cluster result.",
        },
    },
}


def risk_profile_packet(profile: Optional[str] = None) -> Dict[str, Any]:
    selected = [profile] if profile else PROFILE_IDS
    unknown = [item for item in selected if item not in PROFILES]
    if unknown:
        raise ValueError("unknown risk profile: " + ", ".join(unknown))
    profiles = [_profile_entry(profile_id) for profile_id in selected]
    return {
        "schema_version": SCHEMA_VERSION,
        "document_type": "risk_profile_rules",
        "not_investment_advice": (
            "These profile rules are for scenario planning and education only. "
            "They are not investment advice, recommendations, or suitability determinations."
        ),
        "summary": {
            "profiles": len(profiles),
            "available_profiles": PROFILE_IDS,
        },
        "profiles": profiles,
        "provenance": {
            "command": "risk-profile",
            "profile": profile,
        },
    }


def risk_profile_markdown(data: Dict[str, Any]) -> str:
    lines = [
        "# Risk Rule Profiles",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
    ]
    for profile in data["profiles"]:
        lines.extend(
            [
                f"## {profile['name']} ({profile['id']})",
                "",
                profile["description"],
                "",
                f"- Max holding days: {profile['max_holding_days']}",
                f"- Max account risk pct placeholder: {profile['max_account_risk_pct_placeholder']}",
                "",
                "### Required Factsheet Fields",
                "",
            ]
        )
        lines.extend(f"- {field}" for field in profile["required_factsheet_fields"])
        lines.extend(["", "### Required Scenario Regimes", ""])
        lines.extend(f"- {regime}" for regime in profile["required_scenario_regimes"])
        lines.extend(["", "### Mandatory Checklist Questions", ""])
        lines.extend(f"- [ ] {question}" for question in profile["mandatory_checklist_questions"])
        defaults = profile["stop_take_review_defaults"]
        lines.extend(
            [
                "",
                "### Stop/Take Review Defaults",
                "",
                f"- Stop-loss review: {defaults['stop_loss_pct']}%",
                f"- Take-profit review: {defaults['take_profit_pct']}%",
                f"- Review frequency: {defaults['review_frequency']}",
                f"- Gap review: {defaults['gap_review']}",
                "",
            ]
        )
    lines.extend(["## Provenance", ""])
    for key in sorted(data["provenance"]):
        value = data["provenance"][key]
        lines.append(f"- {key}: {value if value is not None else 'all'}")
    return "\n".join(lines).rstrip() + "\n"


def _profile_entry(profile_id: str) -> Dict[str, Any]:
    data = PROFILES[profile_id]
    return {
        "id": profile_id,
        "name": data["name"],
        "description": data["description"],
        "max_holding_days": data["max_holding_days"],
        "max_account_risk_pct_placeholder": data["max_account_risk_pct_placeholder"],
        "required_factsheet_fields": REQUIRED_FACTSHEET_FIELDS,
        "required_scenario_regimes": data["required_scenario_regimes"],
        "mandatory_checklist_questions": data["mandatory_checklist_questions"],
        "stop_take_review_defaults": data["stop_take_review_defaults"],
    }
