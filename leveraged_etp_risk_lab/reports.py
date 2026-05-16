from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


COMPARE_SCHEMA_VERSION = "0.5"
LEDGER_SCHEMA_VERSION = "0.5"
THESIS_IMPACT_SCHEMA_VERSION = "0.6"
WATCHLIST_SCHEMA_VERSION = "0.10"
GALLERY_INDEX_SCHEMA_VERSION = "0.13"
REPORT_CARD_SCHEMA_VERSION = "0.18"
THESIS_DASHBOARD_SCHEMA_VERSION = "0.20"
AUDIT_TRAIL_SCHEMA_VERSION = "0.20"
INVESTMENT_MEMO_SCHEMA_VERSION = "0.21"
MEMO_REVIEW_SCHEMA_VERSION = "0.21"
CYCLE_SCHEMA_VERSION = "0.22"
GUARDRAIL_SCHEMA_VERSION = "0.23"
ORDER_SCHEMA_VERSION = "0.24"
ASSET_HUB_SCHEMA_VERSION = "0.25"
COMPARABLE_REPORT_TYPES = {"simulation_output", "pretrade_plan", "exposure_report"}
REPORT_CARD_TYPES = {
    "simulation_output",
    "pretrade_plan",
    "position_size_plan",
    "stress_matrix",
    "sensitivity_grid",
    "factsheet_check",
    "risk_profile_rules",
    "recipe_run",
    "portfolio_sensitivity",
    "investment_memo_packet",
    "investment_memo_review",
    "cycle_state",
    "cycle_update",
    "guardrail_policy",
    "guardrail_check",
    "order_ticket",
    "order_review",
}
GALLERY_STAGE_ORDER = [
    "fixtures",
    "plans",
    "sizing",
    "stress",
    "thesis/watchlist",
    "audit/story",
    "dashboard",
    "validation",
]


def load_json_report(path: str) -> Dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a JSON object")
    return data


def compare_reports(base_path: str, candidate_path: str) -> Dict[str, Any]:
    base = load_json_report(base_path)
    candidate = load_json_report(candidate_path)
    base_summary = summarize_report(base)
    candidate_summary = summarize_report(candidate)
    for side, summary in [("base", base_summary), ("candidate", candidate_summary)]:
        if summary["document_type"] not in COMPARABLE_REPORT_TYPES:
            raise ValueError(f"{side} is not a supported simulation, pretrade, or exposure JSON output")
    warning_delta = _warning_delta(base_summary["warnings"], candidate_summary["warnings"])
    return {
        "schema_version": COMPARE_SCHEMA_VERSION,
        "document_type": "run_comparison",
        "inputs": {
            "base": _display_path(base_path),
            "candidate": _display_path(candidate_path),
        },
        "base": _comparison_side(base_summary),
        "candidate": _comparison_side(candidate_summary),
        "deltas": {
            "return_pct": _numeric_delta(base_summary["metrics"]["return_pct"], candidate_summary["metrics"]["return_pct"]),
            "path_decay_vs_simple_multiple": _numeric_delta(
                base_summary["metrics"]["path_decay_vs_simple_multiple"],
                candidate_summary["metrics"]["path_decay_vs_simple_multiple"],
            ),
            "weighted_exposure": _numeric_delta(
                base_summary["metrics"]["weighted_exposure"],
                candidate_summary["metrics"]["weighted_exposure"],
            ),
            "warnings": warning_delta,
        },
    }


def summarize_report(data: Dict[str, Any]) -> Dict[str, Any]:
    kind = detect_report_type(data)
    metrics = {
        "return_pct": None,
        "path_decay_vs_simple_multiple": None,
        "weighted_exposure": None,
    }
    label = kind
    if kind == "simulation_output":
        product = data.get("product", {})
        summary = data.get("summary", {})
        label = str(product.get("ticker") or product.get("name") or kind)
        metrics["return_pct"] = _optional_number(summary.get("etp_return_pct"))
        metrics["path_decay_vs_simple_multiple"] = _optional_number(summary.get("path_decay_vs_simple_multiple"))
    elif kind == "pretrade_plan":
        product = data.get("product", {})
        scenario = data.get("scenario", {})
        label = str(product.get("ticker") or product.get("name") or kind)
        metrics["return_pct"] = _optional_number(scenario.get("etp_return_pct"))
        metrics["path_decay_vs_simple_multiple"] = _optional_number(scenario.get("path_decay_vs_simple_multiple"))
    elif kind == "exposure_report":
        portfolio = data.get("portfolio", {})
        summary = data.get("summary", {})
        label = str(portfolio.get("name") or kind)
        metrics["return_pct"] = _optional_number(summary.get("return_pct"))
        metrics["weighted_exposure"] = _optional_number(summary.get("weighted_exposure"))
    else:
        summary = data.get("summary", {})
        metrics["return_pct"] = _optional_number(summary.get("return_pct"))
        metrics["path_decay_vs_simple_multiple"] = _optional_number(summary.get("path_decay_vs_simple_multiple"))
    return {
        "document_type": kind,
        "schema_version": data.get("schema_version"),
        "label": label,
        "metrics": metrics,
        "warnings": [str(item) for item in data.get("warnings", [])],
    }


def detect_report_type(data: Dict[str, Any]) -> str:
    if data.get("document_type") == "guardrail_policy":
        return "guardrail_policy"
    if data.get("document_type") == "guardrail_check":
        return "guardrail_check"
    if data.get("document_type") == "order_ticket":
        return "order_ticket"
    if data.get("document_type") == "order_review":
        return "order_review"
    if data.get("document_type") == "asset_hub":
        return "asset_hub"
    if data.get("document_type") == "pretrade_plan":
        return "pretrade_plan"
    if data.get("document_type") == "position_size_plan":
        return "position_size_plan"
    if data.get("document_type") == "stress_matrix":
        return "stress_matrix"
    if data.get("document_type") == "sensitivity_grid":
        return "sensitivity_grid"
    if data.get("document_type") == "thesis_impact":
        return "thesis_impact"
    if data.get("document_type") == "watchlist":
        return "watchlist"
    if data.get("document_type") == "factsheet_check":
        return "factsheet_check"
    if data.get("document_type") == "risk_profile_rules":
        return "risk_profile_rules"
    if data.get("document_type") == "recipe_run":
        return "recipe_run"
    if data.get("document_type") == "portfolio_sensitivity":
        return "portfolio_sensitivity"
    if data.get("document_type") == "thesis_dashboard_data":
        return "thesis_dashboard_data"
    if data.get("document_type") == "audit_trail":
        return "audit_trail"
    if data.get("document_type") == "investment_memo_packet":
        return "investment_memo_packet"
    if data.get("document_type") == "investment_memo_review":
        return "investment_memo_review"
    if data.get("document_type") == "cycle_state":
        return "cycle_state"
    if data.get("document_type") == "cycle_update":
        return "cycle_update"
    if "portfolio" in data and "positions" in data and "summary" in data:
        return "exposure_report"
    if "product" in data and "path" in data and "summary" in data:
        return "simulation_output"
    if data.get("document_type"):
        return str(data["document_type"])
    return "unknown_json_report"


def guardrail_policy(profile: str) -> Dict[str, Any]:
    policies = {
        "default": {
            "name": "Default allocation guardrail",
            "description": "Balanced public default for short-horizon leveraged ETP scenario review.",
            "max_leverage_exposure": 3.0,
            "max_loss_budget_pct": 1.5,
            "max_holding_days": 10,
            "review_conditions": [
                "Review if investment memo open checks remain unresolved.",
                "Review if cycle-update is not decision-ready.",
                "Review if latest cycle-update reports added, changed, or removed watch items.",
                "Review if critical or high memo invalidation triggers are present.",
                "Review if aggregate modeled portfolio loss exceeds the loss-budget percent.",
            ],
        },
        "conservative": {
            "name": "Conservative allocation guardrail",
            "description": "Tighter public default for lower tolerance review workflows.",
            "max_leverage_exposure": 2.0,
            "max_loss_budget_pct": 1.0,
            "max_holding_days": 3,
            "review_conditions": [
                "Review if any memo invalidation trigger is present.",
                "Review if investment memo open checks remain unresolved.",
                "Review if cycle-update is not decision-ready.",
                "Review if any cycle-update status transition is present.",
                "Review if aggregate modeled portfolio loss exceeds half the loss-budget percent.",
            ],
        },
        "aggressive": {
            "name": "Aggressive allocation guardrail",
            "description": "Wider public default for higher-volatility scenario review workflows.",
            "max_leverage_exposure": 4.0,
            "max_loss_budget_pct": 3.0,
            "max_holding_days": 15,
            "review_conditions": [
                "Review if critical memo invalidation triggers are present.",
                "Review if investment memo has more than five open checks.",
                "Review if cycle-update reports hash drift or changed watch items.",
                "Review if latest cycle-update has more than one status transition.",
                "Review if aggregate modeled portfolio loss exceeds the loss-budget percent.",
            ],
        },
    }
    if profile not in policies:
        raise ValueError("policy must be one of: aggressive, conservative, default")
    selected = policies[profile]
    return {
        "schema_version": GUARDRAIL_SCHEMA_VERSION,
        "document_type": "guardrail_policy",
        "not_investment_advice": (
            "This allocation guardrail policy is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "policy_id": profile,
        "name": selected["name"],
        "description": selected["description"],
        "limits": {
            "max_leverage_exposure": selected["max_leverage_exposure"],
            "max_loss_budget_pct": selected["max_loss_budget_pct"],
            "max_holding_days": selected["max_holding_days"],
        },
        "required_artifacts": [
            "portfolio_sensitivity",
            "position_size_plan",
            "investment_memo_packet",
            "cycle_update",
        ],
        "review_conditions": selected["review_conditions"],
        "provenance": {
            "command": "guardrail-policy",
            "profile": profile,
            "live_market_data": False,
            "shell_out": False,
        },
    }


def guardrail_policy_markdown(data: Dict[str, Any]) -> str:
    limits = data["limits"]
    lines = [
        f"# Allocation Guardrail Policy: {data['policy_id']}",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        data["description"],
        "",
        "## Limits",
        "",
        f"- Max leverage exposure: {limits['max_leverage_exposure']}x",
        f"- Max loss budget: {limits['max_loss_budget_pct']}%",
        f"- Max holding days: {limits['max_holding_days']}",
        "",
        "## Required Artifacts",
        "",
    ]
    lines.extend(f"- {item}" for item in data["required_artifacts"])
    lines.extend(["", "## Review Conditions", ""])
    lines.extend(f"- {item}" for item in data["review_conditions"])
    lines.extend(["", "## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def guardrail_check(
    policy_path: str,
    portfolio_sensitivity_path: str,
    position_size_path: str,
    investment_memo_path: str,
    cycle_update_path: str,
) -> Dict[str, Any]:
    policy = load_json_report(policy_path)
    portfolio = load_json_report(portfolio_sensitivity_path)
    position = load_json_report(position_size_path)
    memo = load_json_report(investment_memo_path)
    cycle = load_json_report(cycle_update_path)
    _require_type(policy, "guardrail_policy", policy_path)
    _require_type(portfolio, "portfolio_sensitivity", portfolio_sensitivity_path)
    _require_type(position, "position_size_plan", position_size_path)
    _require_type(memo, "investment_memo_packet", investment_memo_path)
    _require_type(cycle, "cycle_update", cycle_update_path)

    limits = _dict_value(policy.get("limits"))
    observed = _guardrail_observed_metrics(portfolio, position, memo, cycle)
    rules = [
        _guardrail_limit_rule(
            "max_leverage_exposure",
            "Maximum leverage exposure",
            observed["leverage_exposure"],
            limits.get("max_leverage_exposure"),
            "fail",
            "Reduce aggregate weighted exposure or choose a wider policy only after review.",
        ),
        _guardrail_limit_rule(
            "max_loss_budget_pct",
            "Maximum loss budget percent",
            observed["loss_budget_pct"],
            limits.get("max_loss_budget_pct"),
            "fail",
            "Lower risk budget percent or regenerate position-size with a smaller loss budget.",
        ),
        _guardrail_limit_rule(
            "max_holding_days",
            "Maximum holding days",
            observed["holding_days"],
            limits.get("max_holding_days"),
            "fail",
            "Shorten the planned holding period or regenerate memo evidence for the policy horizon.",
        ),
        _guardrail_artifact_rule(policy, portfolio, position, memo, cycle),
        _guardrail_modeled_loss_rule(observed, limits),
        _guardrail_memo_open_checks_rule(memo, policy.get("policy_id")),
        _guardrail_memo_trigger_rule(memo, policy.get("policy_id")),
        _guardrail_cycle_ready_rule(cycle),
        _guardrail_cycle_change_rule(cycle, policy.get("policy_id")),
    ]
    violated = [rule for rule in rules if rule["status"] != "pass"]
    overall = "fail" if any(rule["status"] == "fail" for rule in violated) else "review" if violated else "pass"
    return {
        "schema_version": GUARDRAIL_SCHEMA_VERSION,
        "document_type": "guardrail_check",
        "not_investment_advice": (
            "This allocation guardrail check is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "inputs": {
            "policy": _display_path(policy_path),
            "portfolio_sensitivity": _display_path(portfolio_sensitivity_path),
            "position_size": _display_path(position_size_path),
            "investment_memo": _display_path(investment_memo_path),
            "cycle_update": _display_path(cycle_update_path),
        },
        "policy": {
            "policy_id": policy.get("policy_id"),
            "name": policy.get("name"),
            "limits": limits,
        },
        "summary": {
            "result": overall,
            "rules": len(rules),
            "pass": sum(1 for rule in rules if rule["status"] == "pass"),
            "review": sum(1 for rule in rules if rule["status"] == "review"),
            "fail": sum(1 for rule in rules if rule["status"] == "fail"),
        },
        "observed": observed,
        "rules": rules,
        "violated_rules": violated,
        "next_actions": _guardrail_next_actions(overall, violated),
        "provenance": {
            "command": "guardrail-check",
            "artifacts": [
                _display_path(policy_path),
                _display_path(portfolio_sensitivity_path),
                _display_path(position_size_path),
                _display_path(investment_memo_path),
                _display_path(cycle_update_path),
            ],
            "live_market_data": False,
            "shell_out": False,
        },
    }


def guardrail_check_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Allocation Guardrail Check",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Summary",
        "",
        f"- Result: {summary['result']}",
        f"- Rules: {summary['pass']} pass, {summary['review']} review, {summary['fail']} fail",
        "",
        "## Observed Metrics",
        "",
    ]
    for key in sorted(data["observed"]):
        lines.append(f"- {key}: {_display_value(data['observed'][key])}")
    lines.extend(["", "## Rules", "", "| Rule | Status | Observed | Limit | Action |", "| --- | --- | --- | --- | --- |"])
    for rule in data["rules"]:
        lines.append(
            f"| {rule['id']} | {rule['status']} | {_display_value(rule.get('observed'))} | "
            f"{_display_value(rule.get('limit'))} | {rule['action']} |"
        )
    lines.extend(["", "## Next Actions", ""])
    lines.extend(f"- [ ] {item}" for item in data["next_actions"])
    return "\n".join(lines) + "\n"


def order_ticket(
    guardrail_check_path: str,
    investment_memo_path: str,
    position_size_path: str,
    factsheet_check_path: str,
    thesis_dashboard_data_path: Optional[str] = None,
) -> Dict[str, Any]:
    guardrail = load_json_report(guardrail_check_path)
    memo = load_json_report(investment_memo_path)
    position = load_json_report(position_size_path)
    factsheet = load_json_report(factsheet_check_path)
    dashboard = load_json_report(thesis_dashboard_data_path) if thesis_dashboard_data_path else None
    _require_type(guardrail, "guardrail_check", guardrail_check_path)
    _require_type(memo, "investment_memo_packet", investment_memo_path)
    _require_type(position, "position_size_plan", position_size_path)
    _require_type(factsheet, "factsheet_check", factsheet_check_path)
    if dashboard:
        _require_type(dashboard, "thesis_dashboard_data", thesis_dashboard_data_path or "thesis_dashboard_data")

    product = _dict_value(memo.get("product_terms")) or _dict_value(position.get("product"))
    risk_budget = _dict_value(memo.get("risk_budget"))
    recommendation = _dict_value(position.get("recommendation"))
    max_notional = _first_number(
        recommendation.get("recommended_notional"),
        risk_budget.get("recommended_notional"),
        dashboard.get("summary", {}).get("recommended_notional") if dashboard else None,
    )
    conditions = _order_do_not_trade_conditions(guardrail, memo, factsheet, dashboard)
    status = _order_ticket_status(guardrail, conditions)
    warnings = _unique_text(
        [
            "No live price, bid-ask spread, depth, halt, or broker availability check is performed.",
            "This order ticket is a pre-order educational checklist, not an instruction to trade.",
            "Broker fields remain placeholders and must be completed outside this package.",
        ]
        + [str(item) for item in position.get("warnings", [])[:4]]
        + [str(item) for item in memo.get("warnings", [])[:4]]
    )
    artifacts = [
        _display_path(guardrail_check_path),
        _display_path(investment_memo_path),
        _display_path(position_size_path),
        _display_path(factsheet_check_path),
    ]
    if thesis_dashboard_data_path:
        artifacts.append(_display_path(thesis_dashboard_data_path))
    return {
        "schema_version": ORDER_SCHEMA_VERSION,
        "document_type": "order_ticket",
        "not_investment_advice": (
            "This pre-order ticket is for scenario planning and education only. "
            "It is not investment advice, a recommendation, a suitability determination, or a broker order."
        ),
        "inputs": {
            "guardrail_check": _display_path(guardrail_check_path),
            "investment_memo": _display_path(investment_memo_path),
            "position_size": _display_path(position_size_path),
            "factsheet_check": _display_path(factsheet_check_path),
            "thesis_dashboard_data": _display_path(thesis_dashboard_data_path) if thesis_dashboard_data_path else None,
        },
        "summary": {
            "status": status,
            "ticker": product.get("ticker"),
            "max_notional": max_notional,
            "currency": product.get("currency") or position.get("inputs", {}).get("currency"),
            "guardrail_result": guardrail.get("summary", {}).get("result"),
            "do_not_trade_conditions": len(conditions),
        },
        "product": {
            "ticker": product.get("ticker"),
            "name": product.get("name"),
            "underlying": product.get("underlying"),
            "leverage": product.get("leverage"),
            "currency": product.get("currency") or position.get("inputs", {}).get("currency"),
        },
        "order_intent": {
            "side": "set-by-user",
            "order_type": "set-by-user",
            "time_in_force": "set-by-user",
            "limit_price": "set-by-user-no-live-price",
            "stop_or_exit_plan": "set-by-user",
            "planned_entry_window": "set-by-user",
            "notes": "placeholder-only; this package does not place, stage, route, or execute orders",
        },
        "sizing": {
            "max_notional": max_notional,
            "max_shares": None,
            "max_shares_placeholder": recommendation.get(
                "max_shares_placeholder",
                "Divide max_notional by the intended execution price outside this package.",
            ),
            "modeled_loss_at_stop": recommendation.get("modeled_loss_at_stop") or risk_budget.get("modeled_loss_at_stop"),
            "risk_budget_pct": position.get("inputs", {}).get("risk_budget_pct") or risk_budget.get("risk_budget_pct"),
            "exposure_multiple": recommendation.get("exposure_multiple") or risk_budget.get("exposure_multiple"),
        },
        "required_broker_fields": _order_required_broker_fields(),
        "no_live_price_warning": "No live or delayed market data is read; confirm quote, spread, liquidity, and broker order preview outside this package.",
        "do_not_trade_if": conditions,
        "warnings": warnings,
        "provenance": {
            "command": "order-ticket",
            "artifacts": artifacts,
            "live_market_data": False,
            "shell_out": False,
            "broker_execution": False,
        },
    }


def order_ticket_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    sizing = data["sizing"]
    lines = [
        f"# Pre-Order Ticket: {_display_value(summary.get('ticker'))}",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Summary",
        "",
        f"- Status: {summary['status']}",
        f"- Max notional: {_display_value(sizing.get('max_notional'))} {_display_value(summary.get('currency'))}",
        f"- Max shares: n/a",
        f"- Guardrail result: {_display_value(summary.get('guardrail_result'))}",
        "",
        "## Order Intent Placeholders",
        "",
    ]
    for key in sorted(data["order_intent"]):
        lines.append(f"- {key}: {data['order_intent'][key]}")
    lines.extend(["", "## Required Broker Fields", ""])
    lines.extend(f"- [ ] {item['field']}: {item['reason']}" for item in data["required_broker_fields"])
    lines.extend(["", "## No Live Price Warning", "", data["no_live_price_warning"], "", "## Do Not Trade If", ""])
    lines.extend(f"- [ ] {item['condition']}" for item in data["do_not_trade_if"] or [{"condition": "No generated condition."}])
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in data["warnings"])
    return "\n".join(lines) + "\n"


def order_review(order_ticket_path: str, guardrail_check_path: str, cycle_update_path: str, audit_trail_path: str) -> Dict[str, Any]:
    ticket = load_json_report(order_ticket_path)
    guardrail = load_json_report(guardrail_check_path)
    cycle = load_json_report(cycle_update_path)
    audit = load_json_report(audit_trail_path)
    _require_type(ticket, "order_ticket", order_ticket_path)
    _require_type(guardrail, "guardrail_check", guardrail_check_path)
    _require_type(cycle, "cycle_update", cycle_update_path)
    _require_type(audit, "audit_trail", audit_trail_path)

    checklist = _order_review_checklist(ticket, guardrail, cycle, audit)
    status = "ready"
    if any(item["status"] == "blocked" for item in checklist):
        status = "blocked"
    elif any(item["status"] == "review" for item in checklist):
        status = "review"
    return {
        "schema_version": ORDER_SCHEMA_VERSION,
        "document_type": "order_review",
        "not_investment_advice": (
            "This final order review checklist is for education only. It is not investment advice, "
            "a recommendation, a suitability determination, or broker execution authorization."
        ),
        "inputs": {
            "order_ticket": _display_path(order_ticket_path),
            "guardrail_check": _display_path(guardrail_check_path),
            "cycle_update": _display_path(cycle_update_path),
            "audit_trail": _display_path(audit_trail_path),
        },
        "summary": {
            "status": status,
            "blocked": sum(1 for item in checklist if item["status"] == "blocked"),
            "review": sum(1 for item in checklist if item["status"] == "review"),
            "ready": sum(1 for item in checklist if item["status"] == "ready"),
            "broker_execution": False,
        },
        "checklist": checklist,
        "final_notes": [
            "Do not use this output as a broker order or trade recommendation.",
            "Confirm all live broker, price, liquidity, and suitability requirements outside this package.",
            "No order has been placed, staged, routed, previewed, or transmitted.",
        ],
        "provenance": {
            "command": "order-review",
            "artifacts": [
                _display_path(order_ticket_path),
                _display_path(guardrail_check_path),
                _display_path(cycle_update_path),
                _display_path(audit_trail_path),
            ],
            "live_market_data": False,
            "shell_out": False,
            "broker_execution": False,
        },
    }


def order_review_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Final Educational Order Review",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Summary",
        "",
        f"- Status: {summary['status']}",
        f"- Checklist: {summary['ready']} ready, {summary['review']} review, {summary['blocked']} blocked",
        f"- Broker execution: {'yes' if summary['broker_execution'] else 'no'}",
        "",
        "## Checklist",
        "",
        "| id | status | item | action |",
        "| --- | --- | --- | --- |",
    ]
    for item in data["checklist"]:
        lines.append(f"| {item['id']} | {item['status']} | {item['item']} | {item['action']} |")
    lines.extend(["", "## Final Notes", ""])
    lines.extend(f"- {item}" for item in data["final_notes"])
    return "\n".join(lines) + "\n"


def report_card(artifact_paths: Iterable[str]) -> Dict[str, Any]:
    artifacts = list(artifact_paths)
    if not artifacts:
        raise ValueError("at least one --artifact is required")
    loaded = [(path, load_json_report(path)) for path in artifacts]
    cards = [_artifact_card(path, data) for path, data in loaded]
    unsupported = [card["document_type"] for card in cards if card["document_type"] not in REPORT_CARD_TYPES]
    if unsupported:
        raise ValueError("unsupported report-card artifact type: " + ", ".join(sorted(set(unsupported))))
    strengths = _unique_text([item for card in cards for item in card["strengths"]])[:8]
    unresolved = _unique_text([item for card in cards for item in card["unresolved_checks"]])[:10]
    warnings = _unique_text([item for card in cards for item in card["warnings"]])[:10]
    next_commands = _report_card_next_commands({card["document_type"] for card in cards}, warnings, unresolved)
    return {
        "schema_version": REPORT_CARD_SCHEMA_VERSION,
        "document_type": "report_card",
        "not_investment_advice": (
            "This report card is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "inputs": {"artifacts": [_display_path(path) for path in artifacts]},
        "summary": {
            "artifacts": len(cards),
            "document_types": sorted({card["document_type"] for card in cards}),
            "strengths": len(strengths),
            "unresolved_checks": len(unresolved),
            "warnings": len(warnings),
            "decision_ready": not unresolved and not warnings,
        },
        "artifact_cards": cards,
        "strengths": strengths,
        "unresolved_checks": unresolved,
        "warnings": warnings,
        "next_commands": next_commands,
        "provenance": {
            "command": "report-card",
            "artifacts": [_display_path(path) for path in artifacts],
            "live_market_data": False,
            "shell_out": False,
        },
    }


def report_card_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Decision Readiness Report Card",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Summary",
        "",
        f"- Artifacts: {summary['artifacts']}",
        f"- Document types: {', '.join(summary['document_types'])}",
        f"- Decision ready: {'yes' if summary['decision_ready'] else 'no'}",
        "",
        "## Strengths",
        "",
    ]
    lines.extend(f"- {item}" for item in data["strengths"] or ["None"])
    lines.extend(["", "## Unresolved Checks", ""])
    lines.extend(f"- {item}" for item in data["unresolved_checks"] or ["None"])
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in data["warnings"] or ["None"])
    lines.extend(["", "## Artifact Cards", "", "| Artifact | Type | Schema | Strengths | Checks | Warnings |", "| --- | --- | --- | --- | --- | --- |"])
    for card in data["artifact_cards"]:
        lines.append(
            f"| {card['path']} | {card['document_type']} | {_display_value(card['schema_version'])} | "
            f"{len(card['strengths'])} | {len(card['unresolved_checks'])} | {len(card['warnings'])} |"
        )
    lines.extend(["", "## Next Commands", ""])
    lines.extend(f"- `{item}`" for item in data["next_commands"] or ["No next command generated."])
    lines.extend(["", "## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def thesis_dashboard_data(
    recipe_run_path: str,
    report_card_path: str,
    watchlist_path: str,
    sensitivity_grid_path: str,
) -> Dict[str, Any]:
    recipe = load_json_report(recipe_run_path)
    card = load_json_report(report_card_path)
    watchlist = load_json_report(watchlist_path)
    sensitivity = load_json_report(sensitivity_grid_path)
    _require_type(recipe, "recipe_run", recipe_run_path)
    _require_type(card, "report_card", report_card_path)
    _require_type(watchlist, "watchlist", watchlist_path)
    _require_type(sensitivity, "sensitivity_grid", sensitivity_grid_path)

    top_entries = sorted(
        watchlist.get("entries", []),
        key=lambda item: (_severity_rank(str(item.get("severity", "low"))), str(item.get("id", ""))),
    )[:8]
    grid_summary = sensitivity.get("summary", {})
    card_summary = card.get("summary", {})
    recipe_summary = recipe.get("summary", {})
    return {
        "schema_version": THESIS_DASHBOARD_SCHEMA_VERSION,
        "document_type": "thesis_dashboard_data",
        "not_investment_advice": (
            "This dashboard packet is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "inputs": {
            "recipe_run": _display_path(recipe_run_path),
            "report_card": _display_path(report_card_path),
            "watchlist": _display_path(watchlist_path),
            "sensitivity_grid": _display_path(sensitivity_grid_path),
        },
        "summary": {
            "product": recipe_summary.get("product"),
            "scenario_return_pct": recipe_summary.get("scenario_return_pct"),
            "path_decay_vs_simple_multiple": recipe_summary.get("path_decay_vs_simple_multiple"),
            "recommended_notional": recipe_summary.get("recommended_notional"),
            "decision_ready": card_summary.get("decision_ready"),
            "watchlist_entries": watchlist.get("summary", {}).get("entries"),
            "critical_watchlist_entries": watchlist.get("summary", {}).get("critical"),
            "high_watchlist_entries": watchlist.get("summary", {}).get("high"),
            "sensitivity_combinations": grid_summary.get("combinations"),
            "worst_grid_return_pct": grid_summary.get("worst_return_pct"),
            "worst_grid_regime": grid_summary.get("worst_return_regime"),
        },
        "cards": {
            "recipe": _dashboard_recipe_card(recipe),
            "readiness": _dashboard_readiness_card(card),
            "watchlist": _dashboard_watchlist_card(watchlist, top_entries),
            "sensitivity": _dashboard_sensitivity_card(sensitivity),
        },
        "warnings": _unique_text(
            [str(item) for item in card.get("warnings", [])]
            + [str(item) for item in sensitivity.get("warnings", [])[:5]]
        ),
        "provenance": {
            "command": "thesis-dashboard-data",
            "artifacts": [
                _display_path(recipe_run_path),
                _display_path(report_card_path),
                _display_path(watchlist_path),
                _display_path(sensitivity_grid_path),
            ],
            "live_market_data": False,
            "shell_out": False,
        },
    }


def thesis_dashboard_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    cards = data["cards"]
    lines = [
        "# Thesis Dashboard Data",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Summary",
        "",
        f"- Product: {_display_value(summary['product'])}",
        f"- Scenario return: {_display_value(summary['scenario_return_pct'])}%",
        f"- Path decay vs simple multiple: {_display_value(summary['path_decay_vs_simple_multiple'])}",
        f"- Recommended notional: {_display_value(summary['recommended_notional'])}",
        f"- Decision ready: {'yes' if summary['decision_ready'] else 'no'}",
        f"- Watchlist entries: {_display_value(summary['watchlist_entries'])}",
        f"- Worst grid return: {_display_value(summary['worst_grid_return_pct'])}% in {_display_value(summary['worst_grid_regime'])}",
        "",
        "## Readiness",
        "",
        f"- Strengths: {cards['readiness']['strengths']}",
        f"- Unresolved checks: {cards['readiness']['unresolved_checks']}",
        f"- Warnings: {cards['readiness']['warnings']}",
        "",
        "## Watchlist",
        "",
        "| id | severity | status | title |",
        "| --- | --- | --- | --- |",
    ]
    for item in cards["watchlist"]["top_entries"]:
        lines.append(f"| {item['id']} | {item['severity']} | {item['status']} | {item['title']} |")
    lines.extend(["", "## Sensitivity", ""])
    for key in sorted(cards["sensitivity"]):
        lines.append(f"- {key}: {cards['sensitivity'][key]}")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in data["warnings"] or ["None"])
    lines.extend(["", "## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def memo_draft(
    recipe_run_path: str,
    thesis_dashboard_data_path: str,
    report_card_path: str,
    factsheet_check_path: Optional[str] = None,
) -> Dict[str, Any]:
    recipe = load_json_report(recipe_run_path)
    dashboard = load_json_report(thesis_dashboard_data_path)
    card = load_json_report(report_card_path)
    factsheet = load_json_report(factsheet_check_path) if factsheet_check_path else _recipe_artifact(recipe, "factsheet_check")
    _require_type(recipe, "recipe_run", recipe_run_path)
    _require_type(dashboard, "thesis_dashboard_data", thesis_dashboard_data_path)
    _require_type(card, "report_card", report_card_path)
    if factsheet:
        _require_type(factsheet, "factsheet_check", factsheet_check_path or "recipe_run.artifacts.factsheet_check")

    artifacts = recipe.get("artifacts", {})
    pretrade = _dict_value(artifacts.get("pretrade_plan"))
    position = _dict_value(artifacts.get("position_size"))
    stress = _dict_value(artifacts.get("stress_matrix"))
    thesis_impact_data = _dict_value(artifacts.get("thesis_impact"))
    watchlist = _dict_value(artifacts.get("watchlist"))
    product = _dict_value(pretrade.get("product") if pretrade else position.get("product") if position else {})
    scenario = _dict_value(pretrade.get("scenario") if pretrade else {})
    budget = _dict_value(pretrade.get("budget") if pretrade else {})
    recommendation = _dict_value(position.get("recommendation") if position else {})
    risk_inputs = _dict_value(position.get("inputs") if position else {})
    dashboard_summary = _dict_value(dashboard.get("summary"))

    watch_entries = _memo_watch_entries(watchlist or dashboard.get("cards", {}).get("watchlist", {}))
    open_checks = _memo_open_checks(card, factsheet)
    invalidation = _memo_invalidation_triggers(watch_entries, card, dashboard)
    return {
        "schema_version": INVESTMENT_MEMO_SCHEMA_VERSION,
        "document_type": "investment_memo_packet",
        "not_investment_advice": (
            "This investment memo packet is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "inputs": {
            "recipe_run": _display_path(recipe_run_path),
            "thesis_dashboard_data": _display_path(thesis_dashboard_data_path),
            "report_card": _display_path(report_card_path),
            "factsheet_check": _display_path(factsheet_check_path) if factsheet_check_path else None,
        },
        "thesis": {
            "summary": str(pretrade.get("thesis", "No thesis text provided.") if pretrade else "No thesis text provided."),
            "claims": _dict_value(thesis_impact_data.get("thesis") if thesis_impact_data else {}).get("claims", []),
            "decision_ready": card.get("summary", {}).get("decision_ready"),
        },
        "product_terms": {
            "ticker": product.get("ticker"),
            "name": product.get("name"),
            "underlying": product.get("underlying"),
            "leverage": product.get("leverage"),
            "reset_frequency": product.get("reset_frequency"),
            "annual_fee_pct": product.get("annual_fee_pct"),
            "currency": product.get("currency") or budget.get("currency") or risk_inputs.get("currency"),
            "factsheet_summary": _factsheet_summary(factsheet),
        },
        "scenario_evidence": {
            "base_case": {
                "days": scenario.get("days") or dashboard_summary.get("scenario_days"),
                "etp_return_pct": scenario.get("etp_return_pct") or dashboard_summary.get("scenario_return_pct"),
                "underlying_return_pct": scenario.get("underlying_return_pct"),
                "path_decay_vs_simple_multiple": scenario.get("path_decay_vs_simple_multiple")
                or dashboard_summary.get("path_decay_vs_simple_multiple"),
            },
            "stress": _memo_stress_summary(stress),
            "dashboard": dashboard_summary,
            "watchlist_top_entries": watch_entries,
        },
        "risk_budget": {
            "max_loss_budget": budget.get("max_loss_budget") or risk_inputs.get("max_loss_budget"),
            "currency": budget.get("currency") or risk_inputs.get("currency"),
            "recommended_notional": recommendation.get("recommended_notional") or dashboard_summary.get("recommended_notional"),
            "modeled_loss_at_stop": recommendation.get("modeled_loss_at_stop"),
            "risk_budget_pct": risk_inputs.get("risk_budget_pct"),
            "exposure_multiple": recommendation.get("exposure_multiple"),
            "stop_loss_pct": (
                risk_inputs.get("stop_loss_pct")
                or (pretrade.get("risk_bands", {}).get("stop_loss_pct") if pretrade else None)
            ),
            "take_profit_pct": pretrade.get("risk_bands", {}).get("take_profit_pct") if pretrade else None,
        },
        "open_checks": open_checks,
        "invalidation_triggers": invalidation,
        "warnings": _unique_text([str(item) for item in card.get("warnings", [])] + [str(item) for item in dashboard.get("warnings", [])])[:12],
        "provenance": {
            "command": "memo-draft",
            "artifacts": [
                _display_path(recipe_run_path),
                _display_path(thesis_dashboard_data_path),
                _display_path(report_card_path),
            ]
            + ([_display_path(factsheet_check_path)] if factsheet_check_path else []),
            "live_market_data": False,
            "shell_out": False,
        },
    }


def memo_draft_markdown(data: Dict[str, Any]) -> str:
    product = data["product_terms"]
    scenario = data["scenario_evidence"]["base_case"]
    budget = data["risk_budget"]
    lines = [
        f"# Investment Memo: {_display_value(product.get('ticker'))}",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Thesis",
        "",
        data["thesis"]["summary"],
        "",
        "## Product Terms",
        "",
        f"- Product: {_display_value(product.get('name'))}",
        f"- Underlying: {_display_value(product.get('underlying'))}",
        f"- Daily leverage: {_display_value(product.get('leverage'))}x",
        f"- Reset frequency: {_display_value(product.get('reset_frequency'))}",
        f"- Annual fee: {_display_value(product.get('annual_fee_pct'))}%",
        "",
        "## Scenario Evidence",
        "",
        f"- Days: {_display_value(scenario.get('days'))}",
        f"- ETP return: {_display_value(scenario.get('etp_return_pct'))}%",
        f"- Underlying return: {_display_value(scenario.get('underlying_return_pct'))}%",
        f"- Path decay vs simple multiple: {_display_value(scenario.get('path_decay_vs_simple_multiple'))}",
        f"- Worst grid return: {_display_value(data['scenario_evidence']['dashboard'].get('worst_grid_return_pct'))}%",
        "",
        "## Risk Budget",
        "",
        f"- Maximum loss budget: {_display_value(budget.get('max_loss_budget'))} {_display_value(budget.get('currency'))}",
        f"- Recommended notional: {_display_value(budget.get('recommended_notional'))}",
        f"- Modeled loss at stop: {_display_value(budget.get('modeled_loss_at_stop'))}",
        f"- Stop-loss: {_display_value(budget.get('stop_loss_pct'))}%",
        f"- Take-profit: {_display_value(budget.get('take_profit_pct'))}%",
        "",
        "## Open Checks",
        "",
    ]
    lines.extend(f"- [ ] {item['text']}" for item in data["open_checks"] or [{"text": "None"}])
    lines.extend(["", "## Invalidation Triggers", ""])
    lines.extend(f"- {item['severity']}: {item['trigger']}" for item in data["invalidation_triggers"] or [{"severity": "none", "trigger": "None"}])
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in data["warnings"] or ["None"])
    lines.extend(["", "## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def memo_review(memo_path: str, report_card_path: str, watchlist_path: str, audit_trail_path: str) -> Dict[str, Any]:
    memo = load_json_report(memo_path)
    card = load_json_report(report_card_path)
    watchlist = load_json_report(watchlist_path)
    audit = load_json_report(audit_trail_path)
    _require_type(memo, "investment_memo_packet", memo_path)
    _require_type(card, "report_card", report_card_path)
    _require_type(watchlist, "watchlist", watchlist_path)
    _require_type(audit, "audit_trail", audit_trail_path)

    memo_triggers = {str(item.get("id") or item.get("trigger")): item for item in memo.get("invalidation_triggers", [])}
    latest_entries = {str(item.get("id")): item for item in watchlist.get("entries", [])}
    changed = _memo_changed_risks(memo_triggers, latest_entries)
    checklist = _memo_review_checklist(memo, card, watchlist, audit, changed)
    next_actions = _memo_next_actions(checklist, changed, card, audit)
    return {
        "schema_version": MEMO_REVIEW_SCHEMA_VERSION,
        "document_type": "investment_memo_review",
        "not_investment_advice": (
            "This memo review is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "inputs": {
            "memo": _display_path(memo_path),
            "report_card": _display_path(report_card_path),
            "watchlist": _display_path(watchlist_path),
            "audit_trail": _display_path(audit_trail_path),
        },
        "summary": {
            "checklist_items": len(checklist),
            "pass": sum(1 for item in checklist if item["status"] == "pass"),
            "review": sum(1 for item in checklist if item["status"] == "review"),
            "changed_risks": len(changed),
            "decision_ready": card.get("summary", {}).get("decision_ready") and not changed,
        },
        "changed_risks": changed,
        "checklist": checklist,
        "next_actions": next_actions,
        "provenance": {
            "command": "memo-review",
            "artifacts": [_display_path(memo_path), _display_path(report_card_path), _display_path(watchlist_path), _display_path(audit_trail_path)],
            "live_market_data": False,
            "shell_out": False,
        },
    }


def memo_review_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Investment Memo Review",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Summary",
        "",
        f"- Decision ready: {'yes' if summary['decision_ready'] else 'no'}",
        f"- Checklist: {summary['pass']} pass, {summary['review']} review",
        f"- Changed risks: {summary['changed_risks']}",
        "",
        "## Checklist",
        "",
        "| id | status | item | action |",
        "| --- | --- | --- | --- |",
    ]
    for item in data["checklist"]:
        lines.append(f"| {item['id']} | {item['status']} | {item['item']} | {item['action']} |")
    lines.extend(["", "## Changed Risks", ""])
    for item in data["changed_risks"] or [{"id": "none", "change": "none", "detail": "None"}]:
        lines.append(f"- {item['id']}: {item['change']} - {item['detail']}")
    lines.extend(["", "## Next Actions", ""])
    lines.extend(f"- [ ] {item}" for item in data["next_actions"] or ["No next action generated."])
    return "\n".join(lines) + "\n"


def cycle_init(memo_path: str, watchlist_path: str, report_card_path: str, sensitivity_grid_path: str) -> Dict[str, Any]:
    memo = load_json_report(memo_path)
    watchlist = load_json_report(watchlist_path)
    card = load_json_report(report_card_path)
    sensitivity = load_json_report(sensitivity_grid_path)
    _require_type(memo, "investment_memo_packet", memo_path)
    _require_type(watchlist, "watchlist", watchlist_path)
    _require_type(card, "report_card", report_card_path)
    _require_type(sensitivity, "sensitivity_grid", sensitivity_grid_path)

    artifact_hashes = [
        _artifact_hash(memo_path, memo),
        _artifact_hash(watchlist_path, watchlist),
        _artifact_hash(report_card_path, card),
        _artifact_hash(sensitivity_grid_path, sensitivity),
    ]
    state_id = "cycle_" + hashlib.sha256(
        "|".join(f"{item['artifact_name']}:{item['sha256']}" for item in artifact_hashes).encode("utf-8")
    ).hexdigest()[:16]
    watch_items = _cycle_watch_items(watchlist)
    open_checks = _cycle_open_checks(memo, card)
    baseline_risks = _cycle_baseline_risks(memo, watchlist, card, sensitivity)
    return {
        "schema_version": CYCLE_SCHEMA_VERSION,
        "document_type": "cycle_state",
        "not_investment_advice": (
            "This watch cycle state is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "state_id": state_id,
        "inputs": {
            "investment_memo": _display_path(memo_path),
            "watchlist": _display_path(watchlist_path),
            "report_card": _display_path(report_card_path),
            "sensitivity_grid": _display_path(sensitivity_grid_path),
        },
        "summary": {
            "watch_items": len(watch_items),
            "open_checks": len(open_checks),
            "baseline_risks": len(baseline_risks),
            "decision_ready": bool(card.get("summary", {}).get("decision_ready")),
        },
        "baseline_artifact_hashes": artifact_hashes,
        "baseline_watch_items": watch_items,
        "baseline_risks": baseline_risks,
        "open_checks": open_checks,
        "review_cadence": {
            "cadence": "placeholder",
            "next_review": "set-by-user",
            "review_owner": "set-by-user",
            "review_inputs": ["latest report_card", "latest watchlist", "latest audit_trail"],
        },
        "provenance": {
            "command": "cycle-init",
            "artifacts": [_display_path(memo_path), _display_path(watchlist_path), _display_path(report_card_path), _display_path(sensitivity_grid_path)],
            "live_market_data": False,
            "shell_out": False,
        },
    }


def cycle_init_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Watch Cycle State",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Summary",
        "",
        f"- State id: {data['state_id']}",
        f"- Watch items: {summary['watch_items']}",
        f"- Open checks: {summary['open_checks']}",
        f"- Baseline risks: {summary['baseline_risks']}",
        f"- Decision ready: {'yes' if summary['decision_ready'] else 'no'}",
        "",
        "## Baseline Artifact Hashes",
        "",
        "| Artifact | Type | Schema | SHA-256 |",
        "| --- | --- | --- | --- |",
    ]
    for item in data["baseline_artifact_hashes"]:
        lines.append(f"| {item['artifact_name']} | {item['document_type']} | {_display_value(item['schema_version'])} | {item['sha256']} |")
    lines.extend(["", "## Baseline Risks", ""])
    lines.extend(f"- {item['id']} ({item['severity']}): {item['trigger']}" for item in data["baseline_risks"] or [{"id": "none", "severity": "none", "trigger": "None"}])
    lines.extend(["", "## Open Checks", ""])
    lines.extend(f"- [ ] {item['text']}" for item in data["open_checks"] or [{"text": "None"}])
    lines.extend(["", "## Review Cadence", ""])
    for key in sorted(data["review_cadence"]):
        lines.append(f"- {key}: {data['review_cadence'][key]}")
    return "\n".join(lines) + "\n"


def cycle_update(cycle_state_path: str, report_card_path: str, watchlist_path: str, audit_trail_path: str) -> Dict[str, Any]:
    state = load_json_report(cycle_state_path)
    card = load_json_report(report_card_path)
    watchlist = load_json_report(watchlist_path)
    audit = load_json_report(audit_trail_path)
    _require_type(state, "cycle_state", cycle_state_path)
    _require_type(card, "report_card", report_card_path)
    _require_type(watchlist, "watchlist", watchlist_path)
    _require_type(audit, "audit_trail", audit_trail_path)

    current_hashes = [_artifact_hash(report_card_path, card), _artifact_hash(watchlist_path, watchlist)]
    hash_drift = _cycle_hash_drift(state.get("baseline_artifact_hashes", []), current_hashes, audit)
    baseline_items = {str(item.get("id")): item for item in state.get("baseline_watch_items", [])}
    current_items = {str(item.get("id")): item for item in _cycle_watch_items(watchlist)}
    added = [current_items[key] for key in sorted(set(current_items) - set(baseline_items))]
    removed = [baseline_items[key] for key in sorted(set(baseline_items) - set(current_items))]
    changed = _cycle_changed_watch_items(baseline_items, current_items)
    transitions = _cycle_status_transitions(baseline_items, current_items, hash_drift, card, audit)
    next_actions = _cycle_next_actions(hash_drift, added, removed, changed, transitions, card, audit)
    return {
        "schema_version": CYCLE_SCHEMA_VERSION,
        "document_type": "cycle_update",
        "not_investment_advice": (
            "This watch cycle update is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "state_id": state.get("state_id"),
        "inputs": {
            "cycle_state": _display_path(cycle_state_path),
            "report_card": _display_path(report_card_path),
            "watchlist": _display_path(watchlist_path),
            "audit_trail": _display_path(audit_trail_path),
        },
        "summary": {
            "added_watch_items": len(added),
            "removed_watch_items": len(removed),
            "changed_watch_items": len(changed),
            "hash_drift": sum(1 for item in hash_drift if item["status"] != "unchanged"),
            "status_transitions": len(transitions),
            "decision_ready": bool(card.get("summary", {}).get("decision_ready")) and not added and not changed and not any(item["status"] != "unchanged" for item in hash_drift),
        },
        "watch_items": {"added": added, "removed": removed, "changed": changed},
        "hash_drift": hash_drift,
        "status_transitions": transitions,
        "next_review_actions": next_actions,
        "provenance": {
            "command": "cycle-update",
            "artifacts": [_display_path(cycle_state_path), _display_path(report_card_path), _display_path(watchlist_path), _display_path(audit_trail_path)],
            "live_market_data": False,
            "shell_out": False,
        },
    }


def cycle_update_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Watch Cycle Update",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Summary",
        "",
        f"- State id: {data['state_id']}",
        f"- Added watch items: {summary['added_watch_items']}",
        f"- Removed watch items: {summary['removed_watch_items']}",
        f"- Changed watch items: {summary['changed_watch_items']}",
        f"- Hash drift: {summary['hash_drift']}",
        f"- Decision ready: {'yes' if summary['decision_ready'] else 'no'}",
        "",
        "## Watch Item Changes",
        "",
    ]
    for kind in ["added", "removed", "changed"]:
        lines.extend([f"### {kind.title()}", ""])
        values = data["watch_items"][kind]
        if values:
            for item in values:
                detail = item.get("changes") if kind == "changed" else item.get("title")
                lines.append(f"- {item['id']}: {detail}")
        else:
            lines.append("- None")
        lines.append("")
    lines.extend(["## Hash Drift", "", "| Artifact | Baseline | Current | Status |", "| --- | --- | --- | --- |"])
    for item in data["hash_drift"]:
        lines.append(f"| {item['artifact_name']} | {_display_value(item.get('baseline_sha256'))} | {_display_value(item.get('current_sha256'))} | {item['status']} |")
    lines.extend(["", "## Status Transitions", ""])
    lines.extend(f"- {item['id']}: {item['from']} -> {item['to']}" for item in data["status_transitions"] or [{"id": "none", "from": "none", "to": "none"}])
    lines.extend(["", "## Next Review Actions", ""])
    lines.extend(f"- [ ] {item}" for item in data["next_review_actions"] or ["No next action generated."])
    return "\n".join(lines) + "\n"


def audit_trail(ledger_path: str, artifact_paths: Iterable[str]) -> Dict[str, Any]:
    artifacts = list(artifact_paths)
    if not artifacts:
        raise ValueError("at least one --artifact is required")
    ledger_rows = _load_ledger_rows(ledger_path)
    artifact_entries = [_audit_artifact(path) for path in artifacts]
    ledger_by_name = {str(row.get("artifact_name")): row for row in ledger_rows}
    checklist = []
    for entry in artifact_entries:
        ledger_row = ledger_by_name.get(entry["artifact_name"])
        matched = bool(ledger_row) and ledger_row.get("sha256") == entry["sha256"] and ledger_row.get("bytes") == entry["bytes"]
        checklist.append(
            {
                "artifact_name": entry["artifact_name"],
                "status": "pass" if matched else "review",
                "ledger_present": bool(ledger_row),
                "hash_matches_ledger": bool(ledger_row) and ledger_row.get("sha256") == entry["sha256"],
                "bytes_match_ledger": bool(ledger_row) and ledger_row.get("bytes") == entry["bytes"],
                "document_type": entry["document_type"],
                "schema_version": entry["schema_version"],
                "sha256": entry["sha256"],
            }
        )
    missing = [item for item in checklist if item["status"] != "pass"]
    return {
        "schema_version": AUDIT_TRAIL_SCHEMA_VERSION,
        "document_type": "audit_trail",
        "inputs": {
            "ledger": _display_path(ledger_path),
            "artifacts": [_display_path(path) for path in artifacts],
        },
        "summary": {
            "ledger_rows": len(ledger_rows),
            "artifacts": len(artifact_entries),
            "passed": len(checklist) - len(missing),
            "review": len(missing),
            "deterministic": True,
        },
        "artifacts": artifact_entries,
        "checklist": checklist,
        "ledger_rows": ledger_rows,
        "provenance": {
            "command": "audit-trail",
            "ledger": _display_path(ledger_path),
            "artifacts": [_display_path(path) for path in artifacts],
            "live_market_data": False,
            "shell_out": False,
        },
    }


def audit_trail_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Audit Trail",
        "",
        f"- Ledger: {data['inputs']['ledger']}",
        f"- Artifacts: {summary['artifacts']}",
        f"- Ledger rows: {summary['ledger_rows']}",
        f"- Passed: {summary['passed']}",
        f"- Review: {summary['review']}",
        "",
        "## Checklist",
        "",
        "| Artifact | Status | Type | Schema | Bytes | SHA-256 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    artifacts = {item["artifact_name"]: item for item in data["artifacts"]}
    for item in data["checklist"]:
        artifact = artifacts[item["artifact_name"]]
        lines.append(
            f"| {item['artifact_name']} | {item['status']} | {item['document_type']} | "
            f"{_display_value(item['schema_version'])} | {artifact['bytes']} | {item['sha256']} |"
        )
    lines.extend(["", "## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def compare_reports_markdown(data: Dict[str, Any]) -> str:
    lines = [
        "# Run Comparison",
        "",
        f"- Base: {data['inputs']['base']}",
        f"- Candidate: {data['inputs']['candidate']}",
        "",
        "## Metrics",
        "",
        "| metric | base | candidate | delta |",
        "| --- | --- | --- | --- |",
    ]
    for metric in ["return_pct", "path_decay_vs_simple_multiple", "weighted_exposure"]:
        base_value = data["base"]["metrics"][metric]
        candidate_value = data["candidate"]["metrics"][metric]
        delta_value = data["deltas"][metric]
        lines.append(
            f"| {metric} | {_display_value(base_value)} | {_display_value(candidate_value)} | {_display_value(delta_value)} |"
        )
    warnings = data["deltas"]["warnings"]
    lines.extend(["", "## Warnings Added", ""])
    lines.extend(f"- {item}" for item in warnings["added"] or ["None"])
    lines.extend(["", "## Warnings Removed", ""])
    lines.extend(f"- {item}" for item in warnings["removed"] or ["None"])
    return "\n".join(lines) + "\n"


def ledger_entry(path: str) -> Dict[str, Any]:
    artifact = Path(path)
    payload = artifact.read_bytes()
    detected_type = "file"
    detected_schema = None
    if artifact.suffix == ".json":
        try:
            data = json.loads(payload.decode("utf-8"))
            if isinstance(data, dict):
                detected_type = detect_report_type(data)
                detected_schema = data.get("schema_version")
        except json.JSONDecodeError:
            detected_type = "json_parse_error"
        except UnicodeDecodeError:
            detected_type = "binary_file"
    return {
        "schema_version": LEDGER_SCHEMA_VERSION,
        "document_type": "run_ledger_entry",
        "artifact_name": artifact.name,
        "artifact_type": detected_type,
        "artifact_schema_version": detected_schema,
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def _gallery_artifact_metadata(path: Path, root: Path, stage: str) -> Dict[str, Any]:
    document_type = None
    schema_version = None
    format_name = _format_name(path)
    if path.suffix == ".json":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                document_type = detect_report_type(data)
                schema_version = data.get("schema_version")
        except (json.JSONDecodeError, UnicodeDecodeError):
            document_type = "json_parse_error"
    elif path.suffix == ".jsonl":
        document_type = "run_ledger"
        schema_version = _jsonl_schema_version(path)
    else:
        companion = path.with_suffix(".json")
        if companion.exists() and companion.name not in {"gallery_index.json", "gallery_index.md"}:
            try:
                data = json.loads(companion.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    document_type = detect_report_type(data)
                    schema_version = data.get("schema_version")
            except (json.JSONDecodeError, UnicodeDecodeError):
                document_type = None
    return {
        "name": path.name,
        "path": _relative_display_path(path, root),
        "stage": stage,
        "format": format_name,
        "document_type": document_type,
        "schema_version": schema_version,
        "bytes": path.stat().st_size,
        "suggested_next_command": _artifact_next_command(path.name, stage),
    }


def _jsonl_schema_version(path: Path) -> Optional[str]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                text = line.strip()
                if not text:
                    continue
                data = json.loads(text)
                if isinstance(data, dict):
                    value = data.get("schema_version")
                    return str(value) if value is not None else None
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return None


def _format_name(path: Path) -> str:
    if path.suffix:
        return path.suffix.lstrip(".")
    return "file"


def _relative_display_path(path: Path, root: Path) -> str:
    return f"{root.as_posix().rstrip('/')}/{path.name}" if not root.is_absolute() else path.name


def _gallery_stage(name: str) -> str:
    if name in {
        "leveraged_nasdaq_3x.json",
        "leveraged_nasdaq_3x.md",
        "single_stock_2x.json",
        "single_stock_2x.md",
        "portfolio_exposure.json",
        "portfolio_exposure.md",
        "template_gallery.json",
        "template_gallery.md",
        "regime_gallery.json",
        "regime_gallery.md",
        "checklist.md",
        "risk_profiles.json",
        "risk_profiles.md",
    } or name.startswith("regime_"):
        return "fixtures"
    if (
        name.startswith("pretrade_plan")
        or name.startswith("compare_runs")
        or name.startswith("recipe_run")
        or name.startswith("report_card")
        or name == "run_ledger.jsonl"
    ):
        return "plans"
    if name.startswith("position_size"):
        return "sizing"
    if name.startswith("stress_matrix") or name.startswith("sensitivity_grid") or name.startswith("portfolio_sensitivity"):
        return "stress"
    if name.startswith("thesis_impact") or name.startswith("watchlist"):
        return "thesis/watchlist"
    if (
        name.startswith("package_audit")
        or name.startswith("demo_story")
        or name.startswith("asset_hub")
        or name.startswith("scenario_pack")
        or name.startswith("daily_reset_path_decay")
        or name.startswith("drawdown_risk")
        or name.startswith("pretrade_guardrails")
        or name.startswith("factsheet_check")
        or name.startswith("audit_trail")
    ):
        return "audit/story"
    if name.startswith("thesis_dashboard_data"):
        return "dashboard"
    if name.startswith("investment_memo"):
        return "dashboard"
    if name.startswith("cycle_"):
        return "dashboard"
    if name.startswith("guardrail_"):
        return "dashboard"
    if name.startswith("order_"):
        return "dashboard"
    if name.startswith("schema_inventory") or name.startswith("artifact_validation") or name.startswith("release_manifest") or name.startswith("docs_export"):
        return "validation"
    if name.endswith(".html"):
        return "dashboard"
    return "fixtures"


def _stage_next_command(stage: str) -> str:
    commands = {
        "fixtures": "python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --format markdown",
        "plans": "python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015 --format markdown",
        "sizing": "python -m leveraged_etp_risk_lab stress-matrix --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss 0.15 --take-profit 0.20 --format markdown",
        "stress": "python -m leveraged_etp_risk_lab thesis-impact --thesis-file examples/fixtures/thesis_note.md --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/stress_matrix.json --format markdown",
        "thesis/watchlist": "python -m leveraged_etp_risk_lab demo-story --input-dir examples/outputs --format markdown",
        "audit/story": "python -m leveraged_etp_risk_lab static-dashboard --input-dir examples/outputs --output examples/outputs/dashboard.html",
        "dashboard": "python -m leveraged_etp_risk_lab package-audit --format markdown",
        "validation": "python -m leveraged_etp_risk_lab artifact-validate --format markdown",
    }
    return commands[stage]


def _artifact_next_command(name: str, stage: str) -> str:
    if name.startswith("template_gallery"):
        return "python -m leveraged_etp_risk_lab template-export --template generic-3x-long-index --output generic_index_3x.json"
    if name.startswith("regime_") or name.startswith("regime_gallery"):
        return "python -m leveraged_etp_risk_lab regime-export --regime volatility_cluster --output volatility_cluster_path.csv"
    if name.startswith("pretrade_plan"):
        return "python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015"
    if name.startswith("position_size"):
        return "python -m leveraged_etp_risk_lab stress-matrix --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss 0.15 --take-profit 0.20"
    if name.startswith("stress_matrix"):
        return "python -m leveraged_etp_risk_lab watchlist-build --thesis-impact examples/outputs/thesis_impact.json --stress-matrix examples/outputs/stress_matrix.json"
    if name.startswith("sensitivity_grid"):
        return "python -m leveraged_etp_risk_lab report-card --artifact examples/outputs/sensitivity_grid.json --format markdown"
    if name.startswith("portfolio_sensitivity"):
        return "python -m leveraged_etp_risk_lab portfolio-sensitivity --manifest examples/fixtures/portfolio_manifest.json --format markdown"
    if name.startswith("thesis_impact"):
        return "python -m leveraged_etp_risk_lab watchlist-build --thesis-impact examples/outputs/thesis_impact.json --stress-matrix examples/outputs/stress_matrix.json"
    if name.startswith("watchlist"):
        return "python -m leveraged_etp_risk_lab demo-story --input-dir examples/outputs --format markdown"
    if name.startswith("factsheet_check"):
        return "python -m leveraged_etp_risk_lab factsheet-check --product examples/fixtures/leveraged_nasdaq_3x.json --factsheet-file examples/fixtures/factsheet_note.txt --format markdown"
    if name.startswith("risk_profiles"):
        return "python -m leveraged_etp_risk_lab risk-profile --format markdown"
    if name.startswith("recipe_run"):
        return "python -m leveraged_etp_risk_lab recipe-run --recipe examples/fixtures/recipe_thesis_review.json --format markdown"
    if name.startswith("report_card"):
        return "python -m leveraged_etp_risk_lab report-card --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/position_size.json --artifact examples/outputs/stress_matrix.json --format markdown"
    if name.startswith("thesis_dashboard_data"):
        return "python -m leveraged_etp_risk_lab thesis-dashboard-data --recipe-run examples/outputs/recipe_run.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --sensitivity-grid examples/outputs/sensitivity_grid.json --format markdown"
    if name.startswith("investment_memo_review"):
        return "python -m leveraged_etp_risk_lab memo-review --memo examples/outputs/investment_memo.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --audit-trail examples/outputs/audit_trail.json --format markdown"
    if name.startswith("investment_memo"):
        return "python -m leveraged_etp_risk_lab memo-draft --recipe-run examples/outputs/recipe_run.json --thesis-dashboard-data examples/outputs/thesis_dashboard_data.json --report-card examples/outputs/report_card.json --factsheet-check examples/outputs/factsheet_check.json --format markdown"
    if name.startswith("cycle_state"):
        return "python -m leveraged_etp_risk_lab cycle-update --cycle-state examples/outputs/cycle_state.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --audit-trail examples/outputs/audit_trail.json --format markdown"
    if name.startswith("cycle_update"):
        return "python -m leveraged_etp_risk_lab cycle-init --memo examples/outputs/investment_memo.json --watchlist examples/outputs/watchlist.json --report-card examples/outputs/report_card.json --sensitivity-grid examples/outputs/sensitivity_grid.json --format markdown"
    if name.startswith("guardrail_policy"):
        return "python -m leveraged_etp_risk_lab guardrail-check --policy examples/outputs/guardrail_policy.json --portfolio-sensitivity examples/outputs/portfolio_sensitivity.json --position-size examples/outputs/position_size.json --investment-memo examples/outputs/investment_memo.json --cycle-update examples/outputs/cycle_update.json --format markdown"
    if name.startswith("guardrail_check"):
        return "python -m leveraged_etp_risk_lab order-ticket --guardrail-check examples/outputs/guardrail_check.json --investment-memo examples/outputs/investment_memo.json --position-size examples/outputs/position_size.json --factsheet-check examples/outputs/factsheet_check.json --thesis-dashboard-data examples/outputs/thesis_dashboard_data.json --format markdown"
    if name.startswith("order_ticket"):
        return "python -m leveraged_etp_risk_lab order-review --order-ticket examples/outputs/order_ticket.json --guardrail-check examples/outputs/guardrail_check.json --cycle-update examples/outputs/cycle_update.json --audit-trail examples/outputs/audit_trail.json --format markdown"
    if name.startswith("order_review"):
        return "python -m leveraged_etp_risk_lab guardrail-policy --policy conservative --format markdown"
    if name.startswith("audit_trail"):
        return "python -m leveraged_etp_risk_lab audit-trail --ledger examples/outputs/run_ledger.jsonl --artifact examples/outputs/pretrade_plan.json --format markdown"
    if name.startswith("asset_hub"):
        return "python -m leveraged_etp_risk_lab asset-hub --input-dir examples/outputs --format markdown"
    if name.startswith("release_manifest"):
        return "python -m leveraged_etp_risk_lab release-manifest --input-dir examples/outputs --format markdown"
    if name.startswith("docs_export"):
        return "python -m leveraged_etp_risk_lab docs-export --input-dir examples/outputs --output examples/outputs/docs_export.html"
    if name.startswith("package_audit") or name.startswith("demo_story"):
        return "python -m leveraged_etp_risk_lab gallery-index --input-dir examples/outputs --format markdown"
    if name.endswith(".html"):
        return "python -m leveraged_etp_risk_lab gallery-index --input-dir examples/outputs --format markdown"
    return _stage_next_command(stage)


def append_ledger(ledger_path: str, artifact_paths: Iterable[str]) -> Dict[str, Any]:
    ledger = Path(ledger_path)
    rows = [ledger_entry(path) for path in artifact_paths]
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    return {
        "schema_version": LEDGER_SCHEMA_VERSION,
        "document_type": "run_ledger_append",
        "ledger": _display_path(ledger_path),
        "rows_appended": len(rows),
        "artifacts": [row["artifact_name"] for row in rows],
    }


def gallery_index(input_dir: str) -> Dict[str, Any]:
    root = Path(input_dir)
    if not root.exists():
        raise FileNotFoundError(root)
    if not root.is_dir():
        raise ValueError(f"{input_dir} is not a directory")
    groups = {stage: [] for stage in GALLERY_STAGE_ORDER}
    for path in sorted(item for item in root.iterdir() if item.is_file()):
        if path.name in {"gallery_index.json", "gallery_index.md"}:
            continue
        stage = _gallery_stage(path.name)
        metadata = _gallery_artifact_metadata(path, root, stage)
        groups[stage].append(metadata)
    stages = [
        {
            "stage": stage,
            "artifact_count": len(groups[stage]),
            "artifacts": groups[stage],
            "suggested_next_command": _stage_next_command(stage),
        }
        for stage in GALLERY_STAGE_ORDER
    ]
    total_bytes = sum(item["bytes"] for stage in stages for item in stage["artifacts"])
    return {
        "schema_version": GALLERY_INDEX_SCHEMA_VERSION,
        "document_type": "gallery_index",
        "input_dir": _display_path(input_dir),
        "summary": {
            "stages": len(stages),
            "artifacts": sum(stage["artifact_count"] for stage in stages),
            "bytes": total_bytes,
        },
        "stages": stages,
        "provenance": {
            "command": "gallery-index",
            "input_dir": _display_path(input_dir),
        },
    }


def gallery_index_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Public Gallery Index",
        "",
        f"- Schema version: {data['schema_version']}",
        f"- Input directory: {data['input_dir']}",
        f"- Artifacts: {summary['artifacts']}",
        f"- Bytes: {summary['bytes']}",
        "",
    ]
    for stage in data["stages"]:
        lines.extend(
            [
                f"## {stage['stage']}",
                "",
                f"- Artifacts: {stage['artifact_count']}",
                f"- Suggested next command: `{stage['suggested_next_command']}`",
                "",
                "| Artifact | Format | Document type | Schema version | Bytes | Suggested next command |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        if stage["artifacts"]:
            for item in stage["artifacts"]:
                lines.append(
                    f"| {item['path']} | {item['format']} | {_display_value(item['document_type'])} | "
                    f"{_display_value(item['schema_version'])} | {item['bytes']} | "
                    f"`{item['suggested_next_command']}` |"
                )
        else:
            lines.append("| None | n/a | n/a | n/a | 0 | n/a |")
        lines.append("")
    lines.extend(["## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def asset_hub(input_dir: str, version: str, readme_path: str = "README.md") -> Dict[str, Any]:
    root = Path(input_dir)
    required = {
        "package_audit": root / "package_audit.json",
        "gallery_index": root / "gallery_index.json",
        "demo_story": root / "demo_story.json",
        "order_review": root / "order_review.json",
        "guardrail_check": root / "guardrail_check.json",
        "cycle_update": root / "cycle_update.json",
    }
    data = {name: load_json_report(str(path)) for name, path in required.items()}
    _require_type(data["package_audit"], "package_audit", str(required["package_audit"]))
    _require_type(data["gallery_index"], "gallery_index", str(required["gallery_index"]))
    _require_type(data["demo_story"], "demo_story", str(required["demo_story"]))
    _require_type(data["order_review"], "order_review", str(required["order_review"]))
    _require_type(data["guardrail_check"], "guardrail_check", str(required["guardrail_check"]))
    _require_type(data["cycle_update"], "cycle_update", str(required["cycle_update"]))

    readme = _read_readme_metadata(readme_path)
    audit_summary = data["package_audit"].get("summary", {})
    gallery_summary = data["gallery_index"].get("summary", {})
    demo_sections = data["demo_story"].get("sections", {})
    return {
        "schema_version": ASSET_HUB_SCHEMA_VERSION,
        "document_type": "asset_hub",
        "not_investment_advice": data["demo_story"].get(
            "not_investment_advice",
            "This public asset hub is for scenario planning and education only. It is not investment advice.",
        ),
        "product_positioning": {
            "name": readme["title"] or "leveraged-etp-risk-lab",
            "version": version,
            "tagline": readme["description"]
            or "Zero-dependency Python CLI for daily-reset leveraged ETF/ETP risk scenario planning.",
            "audience": [
                "Developers and agents validating deterministic leveraged ETP examples.",
                "Risk reviewers who need public, reproducible scenario artifacts.",
                "Educators explaining daily-reset leverage, path decay, and review checklists.",
            ],
            "proof_points": [
                f"{gallery_summary.get('artifacts', 0)} checked demo artifacts indexed from {data['gallery_index'].get('input_dir')}.",
                f"Package audit ready={audit_summary.get('ready')} with {audit_summary.get('passed', 0)} passed checks.",
                "No runtime dependencies, workflow files, private context, broker execution, or live market data.",
            ],
        },
        "command_map": _asset_hub_command_map(demo_sections.get("commands", [])),
        "demo_artifact_map": _asset_hub_artifact_map(data["gallery_index"]),
        "readiness_checklist": _asset_hub_readiness(data["package_audit"], data["guardrail_check"], data["order_review"], data["cycle_update"]),
        "safety_boundaries": _asset_hub_safety_boundaries(data["demo_story"], data["guardrail_check"], data["order_review"]),
        "agent_skill_path": "skills/agent/leveraged-etp-risk-lab/SKILL.md",
        "release_checklist": _asset_hub_release_checklist(data["package_audit"]),
        "roadmap": [
            {
                "version": "0.27.x",
                "theme": "Release manifest hardening",
                "items": [
                    "Keep release-manifest, package-audit, schema-inventory, and artifact-validation aligned.",
                    "Use release notes drafts and post-release checks for deterministic public release preparation.",
                ],
            },
            {
                "version": "0.28.x",
                "theme": "Static documentation export",
                "items": [
                    "Publish docs-export HTML alongside JSON and Markdown artifacts without JavaScript or external assets.",
                    "Keep command maps, release notes, safety caveats, and local artifact links sourced from checked outputs.",
                ],
            },
            {
                "version": "0.30.x",
                "theme": "Scenario case-study packs",
                "items": [
                    "Publish deterministic case studies for path decay, drawdown risk, and pretrade guardrails.",
                    "Keep scenario packs, schema validation, docs export, package audit, README, and agent skill guidance aligned.",
                ],
            },
        ],
        "inputs": {name: _display_path(str(path)) for name, path in required.items()},
        "provenance": {
            "command": "asset-hub",
            "input_dir": _display_path(input_dir),
            "readme": _display_path(readme_path) if Path(readme_path).exists() else None,
            "live_market_data": False,
            "shell_out": False,
            "private_context": False,
        },
    }


def asset_hub_markdown(data: Dict[str, Any]) -> str:
    positioning = data["product_positioning"]
    lines = [
        f"# {positioning['name']} Public Asset Hub",
        "",
        f"**Version:** {positioning['version']}",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        positioning["tagline"],
        "",
        "## Product Positioning",
        "",
    ]
    lines.extend(f"- {item}" for item in positioning["audience"])
    lines.extend(["", "### Proof Points", ""])
    lines.extend(f"- {item}" for item in positioning["proof_points"])
    lines.extend(["", "## Command Map", "", "| Command | Purpose | Example |", "| --- | --- | --- |"])
    for item in data["command_map"]:
        lines.append(f"| `{item['name']}` | {item['purpose']} | `{item['example']}` |")
    lines.extend(["", "## Demo Artifact Map", "", "| Stage | Artifacts | Key artifacts |", "| --- | --- | --- |"])
    for item in data["demo_artifact_map"]:
        lines.append(f"| {item['stage']} | {item['artifact_count']} | {', '.join(item['key_artifacts']) or 'None'} |")
    lines.extend(["", "## Readiness Checklist", ""])
    lines.extend(f"- [{'x' if item['status'] == 'pass' else ' '}] {item['item']} ({item['status']})" for item in data["readiness_checklist"])
    lines.extend(["", "## Safety Boundaries", ""])
    lines.extend(f"- {item}" for item in data["safety_boundaries"])
    lines.extend(["", "## Agent Skill Path", "", f"- `{data['agent_skill_path']}`", "", "## Release Checklist", ""])
    lines.extend(f"- [{'x' if item['status'] == 'pass' else ' '}] {item['item']} ({item['status']})" for item in data["release_checklist"])
    lines.extend(["", "## Three-Version Roadmap", ""])
    for item in data["roadmap"]:
        lines.extend([f"### {item['version']}: {item['theme']}", ""])
        lines.extend(f"- {entry}" for entry in item["items"])
        lines.append("")
    lines.extend(["## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines).rstrip() + "\n"


def _read_readme_metadata(readme_path: str) -> Dict[str, Optional[str]]:
    path = Path(readme_path)
    if not path.exists():
        return {"title": None, "description": None}
    title = None
    description = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("# ") and title is None:
            title = line[2:].strip()
            continue
        if not line.startswith("#") and description is None:
            description = line.replace("`", "")
            break
    return {"title": title, "description": description}


def _asset_hub_command_map(commands: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    purpose_by_name = {
        "pretrade-plan": "Build the base thesis, budget, and risk-band packet.",
        "stress-matrix": "Run the product across built-in deterministic regimes.",
        "sensitivity-grid": "Compare leverage, stop-loss, and take-profit grids.",
        "watchlist-build": "Turn thesis and stress results into review triggers.",
        "recipe-run": "Compose the public workflow from one JSON recipe.",
        "report-card": "Summarize artifact strengths, warnings, and unresolved checks.",
        "memo-draft": "Package thesis, scenario evidence, and risk budget into a memo.",
        "memo-review": "Compare the memo against latest review artifacts.",
        "cycle-init": "Create a persistent public watch-cycle state.",
        "cycle-update": "Detect watch-cycle hash drift and watchlist changes.",
        "guardrail-policy": "Emit explicit allocation review limits.",
        "guardrail-check": "Gate artifacts against exposure, budget, horizon, and review rules.",
        "order-ticket": "Create placeholder-only broker field and do-not-trade checklists.",
        "order-review": "Run a final educational order review without execution.",
        "demo-story": "Render the public walkthrough from checked demo artifacts.",
        "gallery-index": "Index checked demo artifacts by stage.",
        "package-audit": "Check public sharing readiness and validation commands.",
        "schema-inventory": "List local schemas, required fields, matching examples, and public safety notes.",
        "artifact-validate": "Validate example JSON artifacts against the local lightweight schema inventory.",
        "asset-hub": "Emit the GitHub-facing public asset hub.",
        "scenario-pack": "Write new-user case-study packs for path decay, drawdowns, and guardrails.",
        "release-manifest": "Emit release readiness, public artifact inventory, and release notes.",
        "docs-export": "Render one self-contained static HTML documentation page from public artifacts.",
    }
    rows = []
    seen = set()
    for item in commands:
        name = str(item.get("name", ""))
        if not name or name in seen:
            continue
        seen.add(name)
        rows.append(
            {
                "name": name,
                "purpose": purpose_by_name.get(name, "Run a deterministic public workflow command."),
                "example": str(item.get("command", "")),
            }
        )
    for name, example in [
        ("asset-hub", "python -m leveraged_etp_risk_lab asset-hub --input-dir examples/outputs --format markdown"),
        ("docs-export", "python -m leveraged_etp_risk_lab docs-export --input-dir examples/outputs --output examples/outputs/docs_export.html"),
    ]:
        if name not in seen:
            rows.append({"name": name, "purpose": purpose_by_name[name], "example": example})
            seen.add(name)
    return rows


def _asset_hub_artifact_map(gallery: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = []
    for stage in gallery.get("stages", []):
        artifacts = stage.get("artifacts", [])
        key_artifacts = [
            item["path"]
            for item in artifacts
            if item.get("format") in {"json", "md", "html"} and item.get("document_type") is not None
        ][:6]
        rows.append(
            {
                "stage": stage.get("stage"),
                "artifact_count": stage.get("artifact_count", 0),
                "key_artifacts": key_artifacts,
                "suggested_next_command": stage.get("suggested_next_command"),
            }
        )
    return rows


def _asset_hub_readiness(
    audit: Dict[str, Any],
    guardrail: Dict[str, Any],
    order_review_data: Dict[str, Any],
    cycle: Dict[str, Any],
) -> List[Dict[str, str]]:
    audit_summary = audit.get("summary", {})
    guardrail_summary = guardrail.get("summary", {})
    order_summary = order_review_data.get("summary", {})
    cycle_summary = cycle.get("summary", {})
    return [
        _hub_check("package_audit_ready", "Package audit reports public readiness.", bool(audit_summary.get("ready"))),
        _hub_check("zero_dependencies", "Runtime dependency list is empty.", _audit_check_passed(audit, "zero_dependencies")),
        _hub_check("no_workflows", "No workflow files are present.", _audit_check_passed(audit, "no_workflows")),
        _hub_check("public_hygiene", "No private names, local paths, or secret-like values were found.", _audit_check_passed(audit, "no_private_terms")),
        _hub_check("guardrail_reviewed", "Guardrail check completed without a fail result.", guardrail_summary.get("result") != "fail"),
        _hub_check("order_no_execution", "Order review confirms no broker execution.", order_summary.get("broker_execution") is False),
        _hub_check("cycle_update_present", "Cycle update artifact is present and deterministic.", cycle_summary.get("status_transitions") is not None),
    ]


def _asset_hub_safety_boundaries(demo: Dict[str, Any], guardrail: Dict[str, Any], order_review_data: Dict[str, Any]) -> List[str]:
    boundaries = [
        "Do not present generated artifacts as investment advice, recommendations, suitability determinations, or broker orders.",
        "Do not fetch live or delayed market prices, quotes, spreads, depth, halts, or broker availability.",
        "Do not use private context, organization-specific messaging, secrets, environment variables, or workflow files.",
        "Treat position-size, guardrail, order-ticket, and order-review outputs as educational review aids only.",
    ]
    boundaries.extend(str(item) for item in demo.get("sections", {}).get("safety_caveats", []))
    boundaries.extend(str(item.get("action")) for item in guardrail.get("violated_rules", [])[:4] if item.get("action"))
    boundaries.extend(str(item) for item in order_review_data.get("final_notes", []))
    return _unique_text(boundaries)


def _asset_hub_release_checklist(audit: Dict[str, Any]) -> List[Dict[str, str]]:
    items = [
        _hub_check("readme", "README documents the public workflow.", _audit_check_passed(audit, "readme")),
        _hub_check("license", "License is present.", _audit_check_passed(audit, "license")),
        _hub_check("schemas", "Schema files are present.", _audit_check_passed(audit, "schemas")),
        _hub_check("examples", "Checked example outputs are present.", _audit_check_passed(audit, "examples")),
        _hub_check("skill_file", "Agent skill file is present.", _audit_check_passed(audit, "skill_file")),
        _hub_check("version_consistency", "Version fields agree.", _audit_check_passed(audit, "version_consistency")),
        _hub_check("tests", "Validation commands are listed or passing.", _audit_check_passed(audit, "test_commands")),
    ]
    return items


def _audit_check_passed(audit: Dict[str, Any], check_id: str) -> bool:
    for check in audit.get("checks", []):
        if check.get("id") == check_id:
            return check.get("status") == "pass"
    return False


def _hub_check(check_id: str, item: str, passed: bool) -> Dict[str, str]:
    return {"id": check_id, "item": item, "status": "pass" if passed else "review"}


def thesis_impact(thesis_path: str, artifact_paths: Iterable[str]) -> Dict[str, Any]:
    artifacts = list(artifact_paths)
    if not artifacts:
        raise ValueError("at least one --artifact is required")
    thesis_text = Path(thesis_path).read_text(encoding="utf-8")
    artifact_data = [(path, load_json_report(path)) for path in artifacts]
    return thesis_impact_from_reports(thesis_text, _display_path(thesis_path), artifact_data, "thesis-impact")


def thesis_impact_from_reports(
    thesis_text: str,
    thesis_label: str,
    artifacts: Iterable[tuple[str, Dict[str, Any]]],
    command: str = "thesis-impact",
) -> Dict[str, Any]:
    artifact_items = list(artifacts)
    if not artifact_items:
        raise ValueError("at least one artifact is required")
    claims = extract_thesis_claims(thesis_text)
    if not claims:
        claims = [{"id": "claim_1", "text": "No explicit thesis claims found."}]
    artifact_summaries = []
    warning_pool: List[str] = []
    for path, data in artifact_items:
        summary = summarize_report(data)
        artifact_summaries.append(
            {
                "path": _display_path(path),
                "document_type": summary["document_type"],
                "schema_version": summary["schema_version"],
                "label": summary["label"],
                "metrics": summary["metrics"],
                "warnings_count": len(summary["warnings"]),
            }
        )
        warning_pool.extend(summary["warnings"])
    mappings = [_map_claim_to_artifacts(claim, artifact_summaries, warning_pool) for claim in claims]
    checklist = _unique_text([item for mapping in mappings for item in mapping["checklist"]])
    return {
        "schema_version": THESIS_IMPACT_SCHEMA_VERSION,
        "document_type": "thesis_impact",
        "inputs": {
            "thesis_file": thesis_label,
            "artifacts": [_display_path(path) for path, _data in artifact_items],
        },
        "thesis": {
            "claim_count": len(claims),
            "claims": claims,
        },
        "artifacts": artifact_summaries,
        "claim_mappings": mappings,
        "warnings": _unique_text(warning_pool),
        "action_checklist": checklist,
        "provenance": {
            "command": command,
            "thesis_file": thesis_label,
            "artifacts": [_display_path(path) for path, _data in artifact_items],
        },
    }


def extract_thesis_claims(text: str) -> List[Dict[str, str]]:
    claims: List[str] = []
    paragraph: List[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            _flush_claim_paragraph(paragraph, claims)
            continue
        if line.startswith("#"):
            continue
        bullet = line.lstrip("-*0123456789. )")
        if line.startswith(("-", "*")) or bullet != line:
            _flush_claim_paragraph(paragraph, claims)
            if bullet:
                claims.append(bullet)
        else:
            paragraph.append(line)
    _flush_claim_paragraph(paragraph, claims)
    return [{"id": f"claim_{index}", "text": claim} for index, claim in enumerate(claims, start=1)]


def thesis_impact_markdown(data: Dict[str, Any]) -> str:
    lines = [
        "# Thesis Impact",
        "",
        f"- Thesis file: {data['inputs']['thesis_file']}",
        f"- Artifacts: {', '.join(data['inputs']['artifacts'])}",
        f"- Claims mapped: {data['thesis']['claim_count']}",
        "",
        "## Artifact Metrics",
        "",
        "| artifact | type | label | return_pct | path_decay_vs_simple_multiple | weighted_exposure | warnings |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for artifact in data["artifacts"]:
        metrics = artifact["metrics"]
        lines.append(
            f"| {artifact['path']} | {artifact['document_type']} | {artifact['label']} | "
            f"{_display_value(metrics['return_pct'])} | "
            f"{_display_value(metrics['path_decay_vs_simple_multiple'])} | "
            f"{_display_value(metrics['weighted_exposure'])} | {artifact['warnings_count']} |"
        )
    lines.extend(["", "## Claim Mapping", ""])
    for mapping in data["claim_mappings"]:
        lines.extend(
            [
                f"### {mapping['claim_id']}: {mapping['status']}",
                "",
                mapping["claim"],
                "",
                "Observed metrics:",
                "",
            ]
        )
        if mapping["observed_metrics"]:
            for metric in mapping["observed_metrics"]:
                lines.append(
                    f"- {metric['artifact']} {metric['metric']}: "
                    f"{_display_value(metric['value'])} ({metric['interpretation']})"
                )
        else:
            lines.append("- None")
        lines.extend(["", "Warnings:", ""])
        lines.extend(f"- {item}" for item in mapping["warnings"] or ["None"])
        lines.extend(["", "Checklist:", ""])
        lines.extend(f"- [ ] {item}" for item in mapping["checklist"])
        lines.append("")
    lines.extend(["## Action Checklist", ""])
    lines.extend(f"- [ ] {item}" for item in data["action_checklist"] or ["No follow-up actions generated."])
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in data["warnings"] or ["None"])
    return "\n".join(lines) + "\n"


def watchlist_build(thesis_impact_path: str, stress_matrix_path: str) -> Dict[str, Any]:
    impact = load_json_report(thesis_impact_path)
    stress = load_json_report(stress_matrix_path)
    return watchlist_build_from_reports(
        impact,
        stress,
        _display_path(thesis_impact_path),
        _display_path(stress_matrix_path),
        "watchlist-build",
    )


def watchlist_build_from_reports(
    impact: Dict[str, Any],
    stress: Dict[str, Any],
    thesis_impact_label: str,
    stress_matrix_label: str,
    command: str = "watchlist-build",
) -> Dict[str, Any]:
    if impact.get("document_type") != "thesis_impact":
        raise ValueError("thesis impact input must be a thesis_impact JSON output")
    if stress.get("document_type") != "stress_matrix":
        raise ValueError("stress matrix input must be a stress_matrix JSON output")

    thesis_ref = _artifact_ref(thesis_impact_label, impact)
    stress_ref = _artifact_ref(stress_matrix_label, stress)
    entries = []
    entries.extend(_claim_watchlist_entries(impact, thesis_ref))
    entries.extend(_regime_watchlist_entries(stress, stress_ref))
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    entries = sorted(entries, key=lambda item: (severity_order[item["severity"]], item["id"]))
    return {
        "schema_version": WATCHLIST_SCHEMA_VERSION,
        "document_type": "watchlist",
        "not_investment_advice": (
            "This watchlist is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "inputs": {
            "thesis_impact": _display_path(thesis_impact_label),
            "stress_matrix": _display_path(stress_matrix_label),
        },
        "summary": {
            "entries": len(entries),
            "critical": sum(1 for item in entries if item["severity"] == "critical"),
            "high": sum(1 for item in entries if item["severity"] == "high"),
            "medium": sum(1 for item in entries if item["severity"] == "medium"),
            "low": sum(1 for item in entries if item["severity"] == "low"),
        },
        "entries": entries,
        "provenance": {
            "command": command,
            "thesis_impact": _display_path(thesis_impact_label),
            "stress_matrix": _display_path(stress_matrix_label),
        },
    }


def watchlist_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Thesis Watchlist",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        f"- Thesis impact: {data['inputs']['thesis_impact']}",
        f"- Stress matrix: {data['inputs']['stress_matrix']}",
        f"- Entries: {summary['entries']} (critical {summary['critical']}, high {summary['high']}, medium {summary['medium']}, low {summary['low']})",
        "",
        "## Entries",
        "",
        "| id | category | severity | status | title | sources |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for entry in data["entries"]:
        lines.append(
            f"| {entry['id']} | {entry['category']} | {entry['severity']} | {entry['status']} | "
            f"{entry['title']} | {_source_labels(entry['source_artifacts'])} |"
        )
    for entry in data["entries"]:
        lines.extend(["", f"### {entry['id']}: {entry['title']}", ""])
        lines.append(f"- Category: {entry['category']}")
        lines.append(f"- Severity: {entry['severity']}")
        lines.append(f"- Status: {entry['status']}")
        lines.append(f"- Trigger: {entry['trigger']}")
        lines.extend(["", "Next review questions:", ""])
        lines.extend(f"- [ ] {item}" for item in entry["next_review_questions"])
        lines.extend(["", "Source artifact refs:", ""])
        for ref in entry["source_artifacts"]:
            lines.append(f"- {ref['artifact']} ({ref['document_type']} {_display_value(ref['schema_version'])}): {ref['detail']}")
        if entry["warnings"]:
            lines.extend(["", "Warnings:", ""])
            lines.extend(f"- {item}" for item in entry["warnings"])
    return "\n".join(lines) + "\n"


def _claim_watchlist_entries(impact: Dict[str, Any], thesis_ref: Dict[str, Any]) -> List[Dict[str, Any]]:
    entries = []
    for mapping in impact.get("claim_mappings", []):
        warnings = [str(item) for item in mapping.get("warnings", [])]
        severity = _claim_severity(str(mapping.get("status", "")), warnings)
        metrics = [
            {
                "artifact": item["artifact"],
                "metric": item["metric"],
                "value": item["value"],
                "interpretation": item["interpretation"],
            }
            for item in mapping.get("observed_metrics", [])
        ]
        source_artifacts = [dict(thesis_ref, detail=f"claim mapping {mapping.get('claim_id', 'claim')}")]
        for metric in mapping.get("observed_metrics", []):
            source_artifacts.append(
                {
                    "artifact": metric["artifact"],
                    "document_type": "observed_metric_source",
                    "schema_version": None,
                    "detail": f"{metric['metric']} for {mapping.get('claim_id', 'claim')}",
                }
            )
        entries.append(
            {
                "id": str(mapping.get("claim_id", "claim_unknown")),
                "category": "claim",
                "title": _short_title(str(mapping.get("claim", ""))),
                "severity": severity,
                "status": str(mapping.get("status", "needs_review")),
                "trigger": str(mapping.get("claim", "")),
                "metrics": metrics,
                "warnings": warnings,
                "next_review_questions": _claim_review_questions(mapping),
                "source_artifacts": _unique_artifact_refs(source_artifacts),
            }
        )
    return entries


def _regime_watchlist_entries(stress: Dict[str, Any], stress_ref: Dict[str, Any]) -> List[Dict[str, Any]]:
    entries = []
    for row in stress.get("rows", []):
        severity = _regime_severity(row)
        trigger = _regime_trigger(row)
        entries.append(
            {
                "id": f"regime_{row.get('regime', 'unknown')}",
                "category": "regime_trigger",
                "title": f"{row.get('name', row.get('regime', 'Regime'))} stress trigger",
                "severity": severity,
                "status": "triggered" if severity in {"critical", "high", "medium"} else "monitor",
                "trigger": trigger,
                "metrics": {
                    "regime": row.get("regime"),
                    "return_pct": row.get("return_pct"),
                    "path_decay_vs_simple_multiple": row.get("path_decay_vs_simple_multiple"),
                    "worst_drawdown_pct": row.get("worst_drawdown_pct"),
                    "stop_events": row.get("stop_events"),
                    "warnings_count": row.get("warnings_count"),
                },
                "warnings": [f"{row.get('warnings_count', 0)} stress-matrix warning(s) observed for this regime."],
                "next_review_questions": _regime_review_questions(row),
                "source_artifacts": [
                    dict(stress_ref, detail=f"stress row {row.get('regime', 'unknown')}"),
                ],
            }
        )
    return entries


def _claim_severity(status: str, warnings: List[str]) -> str:
    if status == "challenged":
        return "high"
    if status == "needs_review" and len(warnings) >= 3:
        return "medium"
    if status == "needs_review":
        return "medium"
    if warnings:
        return "medium"
    return "low"


def _regime_severity(row: Dict[str, Any]) -> str:
    return_pct = float(row.get("return_pct", 0.0))
    drawdown = float(row.get("worst_drawdown_pct", 0.0))
    decay = float(row.get("path_decay_vs_simple_multiple", 0.0))
    stop_events = int(row.get("stop_events", 0))
    if return_pct <= -25 or drawdown <= -25:
        return "critical"
    if (stop_events > 0 and return_pct <= -15) or return_pct <= -10 or drawdown <= -15 or decay <= -2:
        return "high"
    if stop_events > 0 or return_pct < 0 or drawdown <= -5 or decay < 0:
        return "medium"
    return "low"


def _regime_trigger(row: Dict[str, Any]) -> str:
    labels = row.get("stop_event_labels", [])
    parts = [
        f"return {row.get('return_pct')}%",
        f"worst drawdown {row.get('worst_drawdown_pct')}%",
        f"path decay {row.get('path_decay_vs_simple_multiple')}",
    ]
    if labels:
        parts.append("band events: " + "; ".join(str(item) for item in labels))
    return "; ".join(parts)


def _claim_review_questions(mapping: Dict[str, Any]) -> List[str]:
    questions = [
        f"What evidence would change the status of {mapping.get('claim_id', 'this claim')} from {mapping.get('status', 'needs_review')}?",
        "Which observed metrics are most relevant to the claim, and are any expected metrics missing?",
    ]
    for item in mapping.get("checklist", [])[:3]:
        questions.append(str(item))
    if mapping.get("warnings"):
        questions.append("Which warning would invalidate the thesis if it appears in live review?")
    return _unique_text(questions)


def _regime_review_questions(row: Dict[str, Any]) -> List[str]:
    questions = [
        f"Would the thesis still be acceptable under the {row.get('regime', 'selected')} regime?",
        "What pre-defined action follows if this regime starts to resemble the current market path?",
    ]
    if int(row.get("stop_events", 0)) > 0:
        questions.append("Are modeled stop or take-profit band events acceptable after accounting for execution and gap risk?")
    if float(row.get("path_decay_vs_simple_multiple", 0.0)) < 0:
        questions.append("Does modeled path decay weaken the expected holding-period thesis?")
    if float(row.get("return_pct", 0.0)) < 0:
        questions.append("Is the loss budget still valid under this modeled return?")
    return _unique_text(questions)


def _artifact_ref(path: str, data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "artifact": _display_path(path),
        "document_type": str(data.get("document_type", "unknown_json_report")),
        "schema_version": data.get("schema_version"),
        "detail": "source artifact",
    }


def _unique_artifact_refs(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    result = []
    for item in items:
        key = (item.get("artifact"), item.get("document_type"), item.get("schema_version"), item.get("detail"))
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def _source_labels(refs: List[Dict[str, Any]]) -> str:
    return ", ".join(_unique_text([str(ref["artifact"]) for ref in refs]))


def _short_title(text: str) -> str:
    stripped = " ".join(text.split())
    if len(stripped) <= 80:
        return stripped
    return stripped[:77].rstrip() + "..."


def _comparison_side(summary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "document_type": summary["document_type"],
        "schema_version": summary["schema_version"],
        "label": summary["label"],
        "metrics": summary["metrics"],
        "warnings_count": len(summary["warnings"]),
    }


def _artifact_card(path: str, data: Dict[str, Any]) -> Dict[str, Any]:
    document_type = detect_report_type(data)
    strengths = _artifact_strengths(document_type, data)
    unresolved = _artifact_unresolved_checks(document_type, data)
    warnings = _artifact_warnings(document_type, data)
    return {
        "path": _display_path(path),
        "document_type": document_type,
        "schema_version": data.get("schema_version"),
        "label": _artifact_label(document_type, data),
        "metrics": _artifact_metrics(document_type, data),
        "strengths": strengths,
        "unresolved_checks": unresolved,
        "warnings": warnings,
    }


def _artifact_label(document_type: str, data: Dict[str, Any]) -> str:
    if document_type in {"simulation_output", "pretrade_plan", "position_size_plan", "stress_matrix", "sensitivity_grid"}:
        product = data.get("product", {})
        return str(product.get("ticker") or product.get("name") or document_type)
    if document_type == "portfolio_sensitivity":
        portfolio = data.get("portfolio", {})
        return str(portfolio.get("name") or document_type)
    if document_type == "factsheet_check":
        product = data.get("product", {})
        return str(product.get("ticker") or product.get("name") or document_type)
    if document_type == "risk_profile_rules":
        profiles = data.get("profiles", [])
        return "profiles:" + ",".join(str(profile.get("id")) for profile in profiles if profile.get("id"))
    if document_type == "recipe_run":
        return str(data.get("summary", {}).get("product") or document_type)
    if document_type == "guardrail_policy":
        return str(data.get("policy_id") or document_type)
    if document_type == "guardrail_check":
        return str(data.get("summary", {}).get("result") or document_type)
    if document_type == "order_ticket":
        return str(data.get("summary", {}).get("ticker") or data.get("summary", {}).get("status") or document_type)
    if document_type == "order_review":
        return str(data.get("summary", {}).get("status") or document_type)
    return document_type


def _artifact_metrics(document_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    if document_type == "simulation_output":
        summary = data.get("summary", {})
        return {
            "days": data.get("inputs", {}).get("days"),
            "return_pct": summary.get("etp_return_pct"),
            "path_decay_vs_simple_multiple": summary.get("path_decay_vs_simple_multiple"),
            "band_events": len(data.get("band_events", [])),
        }
    if document_type == "pretrade_plan":
        scenario = data.get("scenario", {})
        return {
            "days": scenario.get("days"),
            "return_pct": scenario.get("etp_return_pct"),
            "path_decay_vs_simple_multiple": scenario.get("path_decay_vs_simple_multiple"),
            "max_loss_budget": data.get("budget", {}).get("max_loss_budget"),
            "band_events": len(data.get("risk_bands", {}).get("band_events", [])),
        }
    if document_type == "position_size_plan":
        recommendation = data.get("recommendation", {})
        return {
            "recommended_notional": recommendation.get("recommended_notional"),
            "modeled_loss_at_stop": recommendation.get("modeled_loss_at_stop"),
            "exposure_multiple": recommendation.get("exposure_multiple"),
        }
    if document_type == "stress_matrix":
        rows = data.get("rows", [])
        worst = _lowest_report_card_row(rows, "return_pct")
        drawdown = _lowest_report_card_row(rows, "worst_drawdown_pct")
        return {
            "regimes": len(rows),
            "weakest_return_regime": worst.get("regime"),
            "weakest_return_pct": worst.get("return_pct"),
            "largest_drawdown_regime": drawdown.get("regime"),
            "largest_drawdown_pct": drawdown.get("worst_drawdown_pct"),
        }
    if document_type == "sensitivity_grid":
        summary = data.get("summary", {})
        return {
            "combinations": summary.get("combinations"),
            "worst_return_regime": summary.get("worst_return_regime"),
            "worst_return_pct": summary.get("worst_return_pct"),
            "worst_path_decay_vs_simple_multiple": summary.get("worst_path_decay_vs_simple_multiple"),
            "max_stop_events": summary.get("max_stop_events"),
        }
    if document_type == "factsheet_check":
        return dict(data.get("summary", {}))
    if document_type == "risk_profile_rules":
        return {"profiles": len(data.get("profiles", []))}
    if document_type == "recipe_run":
        return dict(data.get("summary", {}))
    if document_type == "portfolio_sensitivity":
        return dict(data.get("summary", {}))
    if document_type == "investment_memo_packet":
        return {
            "open_checks": len(data.get("open_checks", [])),
            "invalidation_triggers": len(data.get("invalidation_triggers", [])),
            "recommended_notional": data.get("risk_budget", {}).get("recommended_notional"),
            "decision_ready": data.get("thesis", {}).get("decision_ready"),
        }
    if document_type == "investment_memo_review":
        return dict(data.get("summary", {}))
    if document_type in {"cycle_state", "cycle_update"}:
        return dict(data.get("summary", {}))
    if document_type == "guardrail_policy":
        return dict(data.get("limits", {}))
    if document_type == "guardrail_check":
        return dict(data.get("summary", {}))
    if document_type in {"order_ticket", "order_review"}:
        return dict(data.get("summary", {}))
    return {}


def _artifact_strengths(document_type: str, data: Dict[str, Any]) -> List[str]:
    if document_type == "simulation_output":
        product = data.get("product", {})
        summary = data.get("summary", {})
        return [
            f"{product.get('ticker', 'Product')} has a deterministic scenario with {data.get('inputs', {}).get('days')} modeled days.",
            f"Modeled ETP return is {summary.get('etp_return_pct')}% with path-decay metric {summary.get('path_decay_vs_simple_multiple')}.",
        ]
    if document_type == "pretrade_plan":
        product = data.get("product", {})
        budget = data.get("budget", {})
        return [
            f"{product.get('ticker', 'Product')} pretrade plan records thesis, risk bands, and a {budget.get('max_loss_budget')} {budget.get('currency', '')} loss budget.".strip(),
            f"Checklist profile is {data.get('checklist', {}).get('profile', 'n/a')}.",
        ]
    if document_type == "position_size_plan":
        recommendation = data.get("recommendation", {})
        return [
            f"Position sizing converts the loss budget into {recommendation.get('recommended_notional')} notional.",
            "Max-share count is intentionally left as a placeholder because no live price is fetched.",
        ]
    if document_type == "stress_matrix":
        rows = data.get("rows", [])
        return [f"Stress matrix covers {len(rows)} deterministic regime rows."]
    if document_type == "sensitivity_grid":
        summary = data.get("summary", {})
        return [f"Sensitivity grid covers {summary.get('combinations', 0)} leverage and risk-band combinations."]
    if document_type == "factsheet_check":
        summary = data.get("summary", {})
        return [f"Factsheet checklist has {summary.get('passed', 0)} passed checks out of {summary.get('checks', 0)}."]
    if document_type == "risk_profile_rules":
        return [f"Risk profile rules are available for {len(data.get('profiles', []))} profile(s)."]
    if document_type == "recipe_run":
        summary = data.get("summary", {})
        return [
            f"Recipe bundle composes {summary.get('components', 0)} components without shelling out.",
            f"Recipe summary includes recommended notional {summary.get('recommended_notional')} and {summary.get('watchlist_entries')} watchlist entries.",
        ]
    if document_type == "portfolio_sensitivity":
        summary = data.get("summary", {})
        return [
            f"Portfolio sensitivity covers {summary.get('positions', 0)} position(s).",
            f"Aggregate worst-case modeled loss is {summary.get('aggregate_worst_case_modeled_loss')}.",
        ]
    if document_type == "investment_memo_packet":
        return [
            f"Investment memo records {len(data.get('open_checks', []))} open check(s).",
            f"Investment memo records {len(data.get('invalidation_triggers', []))} invalidation trigger(s).",
        ]
    if document_type == "investment_memo_review":
        summary = data.get("summary", {})
        return [f"Memo review has {summary.get('pass', 0)} passing checklist item(s)."]
    if document_type == "cycle_state":
        summary = data.get("summary", {})
        return [f"Watch cycle state tracks {summary.get('watch_items', 0)} baseline watch item(s)."]
    if document_type == "cycle_update":
        summary = data.get("summary", {})
        return [f"Watch cycle update records {summary.get('changed_watch_items', 0)} changed watch item(s)."]
    if document_type == "guardrail_policy":
        limits = data.get("limits", {})
        return [f"Guardrail policy sets max exposure {limits.get('max_leverage_exposure')}x and max loss budget {limits.get('max_loss_budget_pct')}%."]
    if document_type == "guardrail_check":
        summary = data.get("summary", {})
        return [f"Guardrail check result is {summary.get('result')} across {summary.get('rules', 0)} rule(s)."]
    if document_type == "order_ticket":
        summary = data.get("summary", {})
        return [
            f"Order ticket status is {summary.get('status')} with max notional {summary.get('max_notional')}.",
            "Order intent and broker fields are placeholders with broker execution disabled.",
        ]
    if document_type == "order_review":
        summary = data.get("summary", {})
        return [f"Order review status is {summary.get('status')} with broker execution disabled."]
    return []


def _artifact_unresolved_checks(document_type: str, data: Dict[str, Any]) -> List[str]:
    if document_type == "simulation_output":
        return [
            "Convert scenario output into a pretrade plan with thesis, budget, and checklist before decision review.",
            "Complete factsheet, liquidity, execution, tax, and suitability checks outside this simulation.",
        ]
    if document_type == "pretrade_plan":
        checks = [f"Checklist item: {item}" for item in data.get("checklist", {}).get("items", [])[:5]]
        checks.append("Confirm liquidity, execution quality, tax treatment, and suitability outside this model.")
        return checks
    if document_type == "position_size_plan":
        checks = [f"Checklist item: {item}" for item in data.get("checklist", [])[:5]]
        checks.append("Translate max-shares placeholder using an intended execution price outside this model.")
        return checks
    if document_type == "stress_matrix":
        rows = data.get("rows", [])
        worst = _lowest_report_card_row(rows, "return_pct")
        checks = ["Review whether the weakest regime remains inside the stated loss budget."]
        if worst:
            checks.append(f"Weakest modeled return regime is {worst.get('regime')} at {worst.get('return_pct')}%.")
        return checks
    if document_type == "sensitivity_grid":
        summary = data.get("summary", {})
        return [
            "Review whether the worst grid combination remains inside the stated loss budget.",
            f"Worst modeled return is {summary.get('worst_return_pct')}% in {summary.get('worst_return_regime')}.",
            f"Maximum stop/take events across a combination is {summary.get('max_stop_events')}.",
        ]
    if document_type == "factsheet_check":
        missing = [f"Missing factsheet field: {field}" for field in data.get("missing_fields", [])]
        review = [f"Review factsheet field: {item['field']}" for item in data.get("checks", []) if item.get("status") == "review"]
        return missing + review
    if document_type == "risk_profile_rules":
        return ["Apply the selected profile's required factsheet fields, regimes, and checklist questions to the trade packet."]
    if document_type == "recipe_run":
        components = data.get("components", [])
        return [f"Review embedded component: {item.get('id')}" for item in components[:6]]
    if document_type == "portfolio_sensitivity":
        summary = data.get("summary", {})
        return [
            "Review whether the aggregate worst-case modeled loss remains inside the portfolio loss budget.",
            f"Weakest position is {summary.get('weakest_position_id')} in {summary.get('weakest_position_regime')}.",
        ]
    if document_type == "investment_memo_packet":
        return [str(item.get("text")) for item in data.get("open_checks", [])[:8]]
    if document_type == "investment_memo_review":
        return [str(item.get("action")) for item in data.get("checklist", []) if item.get("status") != "pass"]
    if document_type == "cycle_state":
        return [str(item.get("text")) for item in data.get("open_checks", [])[:8]]
    if document_type == "cycle_update":
        return [str(item) for item in data.get("next_review_actions", [])[:8]]
    if document_type == "guardrail_policy":
        return [f"Apply required artifact: {item}" for item in data.get("required_artifacts", [])]
    if document_type == "guardrail_check":
        return [str(item.get("action")) for item in data.get("violated_rules", [])[:8]]
    if document_type == "order_ticket":
        return [str(item.get("condition")) for item in data.get("do_not_trade_if", [])[:8]]
    if document_type == "order_review":
        return [str(item.get("action")) for item in data.get("checklist", []) if item.get("status") != "ready"]
    return []


def _artifact_warnings(document_type: str, data: Dict[str, Any]) -> List[str]:
    if document_type == "stress_matrix":
        row_warnings = []
        for row in data.get("rows", []):
            if row.get("warnings_count", 0):
                row_warnings.append(f"{row.get('regime')} has {row.get('warnings_count')} modeled warning(s).")
            if row.get("stop_events", 0):
                row_warnings.append(f"{row.get('regime')} has {row.get('stop_events')} stop/take event(s).")
        return _unique_text([str(item) for item in data.get("warnings", [])] + row_warnings)
    if document_type == "sensitivity_grid":
        row_warnings = []
        for row in data.get("rows", []):
            if row.get("stop_events", 0):
                row_warnings.append(
                    f"{row.get('leverage')}x stop {row.get('stop_loss_pct')} take {row.get('take_profit_pct')} has {row.get('stop_events')} stop/take event(s)."
                )
        return _unique_text([str(item) for item in data.get("warnings", [])] + row_warnings)[:10]
    if document_type == "factsheet_check":
        warnings = []
        summary = data.get("summary", {})
        if summary.get("missing", 0):
            warnings.append(f"Factsheet checklist has {summary.get('missing')} missing field(s).")
        if summary.get("review", 0):
            warnings.append(f"Factsheet checklist has {summary.get('review')} review field(s).")
        return warnings
    if document_type == "recipe_run":
        warnings = []
        for artifact in data.get("artifacts", {}).values():
            if isinstance(artifact, dict):
                warnings.extend(str(item) for item in artifact.get("warnings", []))
        return _unique_text(warnings)
    if document_type == "portfolio_sensitivity":
        return [str(item) for item in data.get("warnings", [])]
    return [str(item) for item in data.get("warnings", [])]


def _artifact_hash(path: str, data: Dict[str, Any]) -> Dict[str, Any]:
    artifact = Path(path)
    payload = artifact.read_bytes()
    return {
        "artifact_name": artifact.name,
        "path": _display_path(path),
        "document_type": detect_report_type(data),
        "schema_version": data.get("schema_version"),
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def _cycle_watch_items(watchlist: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = []
    for item in watchlist.get("entries", []):
        rows.append(
            {
                "id": str(item.get("id")),
                "category": str(item.get("category")),
                "severity": str(item.get("severity")),
                "status": str(item.get("status")),
                "title": str(item.get("title")),
                "trigger": str(item.get("trigger")),
            }
        )
    unique = {}
    for row in rows:
        unique.setdefault(row["id"], row)
    return sorted(unique.values(), key=lambda item: (_severity_rank(item["severity"]), item["id"]))


def _cycle_open_checks(memo: Dict[str, Any], card: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = []
    for item in memo.get("open_checks", []):
        rows.append({"id": str(item.get("id")), "source": str(item.get("source", "investment_memo")), "text": str(item.get("text")), "status": "open"})
    offset = len(rows)
    for index, text in enumerate(card.get("unresolved_checks", [])[:12], start=1):
        rows.append({"id": f"report_card_{offset + index}", "source": "report_card", "text": str(text), "status": "open"})
    unique = {}
    for row in rows:
        unique.setdefault(row["text"], row)
    return list(unique.values())


def _cycle_baseline_risks(
    memo: Dict[str, Any],
    watchlist: Dict[str, Any],
    card: Dict[str, Any],
    sensitivity: Dict[str, Any],
) -> List[Dict[str, Any]]:
    rows = []
    for item in memo.get("invalidation_triggers", [])[:10]:
        rows.append(
            {
                "id": str(item.get("id")),
                "source": str(item.get("source", "investment_memo")),
                "severity": str(item.get("severity", "medium")),
                "status": str(item.get("status", "review")),
                "trigger": str(item.get("trigger")),
            }
        )
    known = {item["id"] for item in rows}
    for item in _cycle_watch_items(watchlist):
        if item["id"] not in known and item["severity"] in {"critical", "high"}:
            rows.append({key: item[key] for key in ["id", "severity", "status", "trigger"]} | {"source": "watchlist"})
            known.add(item["id"])
    summary = sensitivity.get("summary", {})
    if summary.get("worst_return_pct") is not None:
        rows.append(
            {
                "id": "sensitivity_worst_return",
                "source": "sensitivity_grid",
                "severity": "high" if float(summary.get("worst_return_pct", 0)) < -20 else "medium",
                "status": "review",
                "trigger": f"Worst grid return is {summary.get('worst_return_pct')}% in {summary.get('worst_return_regime')}.",
            }
        )
    if not card.get("summary", {}).get("decision_ready"):
        rows.append(
            {
                "id": "decision_not_ready",
                "source": "report_card",
                "severity": "medium",
                "status": "review",
                "trigger": "Report card is not decision-ready.",
            }
        )
    unique = {}
    for row in rows:
        unique.setdefault(row["id"], row)
    return sorted(unique.values(), key=lambda item: (_severity_rank(item["severity"]), item["id"]))


def _cycle_hash_drift(baseline_hashes: List[Dict[str, Any]], current_hashes: List[Dict[str, Any]], audit: Dict[str, Any]) -> List[Dict[str, Any]]:
    current_by_name = {item["artifact_name"]: item for item in current_hashes}
    for item in audit.get("artifacts", []):
        current_by_name.setdefault(str(item.get("artifact_name")), item)
    rows = []
    for baseline in baseline_hashes:
        name = str(baseline.get("artifact_name"))
        current = current_by_name.get(name)
        if not current:
            status = "missing_latest"
            current_sha = None
            current_bytes = None
        else:
            current_sha = current.get("sha256")
            current_bytes = current.get("bytes")
            status = "unchanged" if current_sha == baseline.get("sha256") and current_bytes == baseline.get("bytes") else "changed"
        rows.append(
            {
                "artifact_name": name,
                "document_type": baseline.get("document_type"),
                "baseline_sha256": baseline.get("sha256"),
                "current_sha256": current_sha,
                "baseline_bytes": baseline.get("bytes"),
                "current_bytes": current_bytes,
                "status": status,
            }
        )
    return rows


def _cycle_changed_watch_items(
    baseline_items: Dict[str, Dict[str, Any]],
    current_items: Dict[str, Dict[str, Any]],
) -> List[Dict[str, Any]]:
    changed = []
    for key in sorted(set(baseline_items).intersection(current_items)):
        fields = {}
        for field in ["severity", "status", "title", "trigger"]:
            if baseline_items[key].get(field) != current_items[key].get(field):
                fields[field] = {"from": baseline_items[key].get(field), "to": current_items[key].get(field)}
        if fields:
            changed.append({"id": key, "category": current_items[key].get("category"), "changes": fields})
    return changed


def _cycle_status_transitions(
    baseline_items: Dict[str, Dict[str, Any]],
    current_items: Dict[str, Dict[str, Any]],
    hash_drift: List[Dict[str, Any]],
    card: Dict[str, Any],
    audit: Dict[str, Any],
) -> List[Dict[str, Any]]:
    rows = []
    for key in sorted(set(baseline_items).intersection(current_items)):
        old = baseline_items[key].get("status")
        new = current_items[key].get("status")
        if old != new:
            rows.append({"id": key, "from": old, "to": new, "reason": "watchlist status changed"})
    if any(item["status"] != "unchanged" for item in hash_drift):
        rows.append({"id": "artifact_hashes", "from": "unchanged", "to": "review", "reason": "baseline artifact hash drift detected"})
    if not card.get("summary", {}).get("decision_ready"):
        rows.append({"id": "report_card", "from": "decision_ready_unknown", "to": "review", "reason": "latest report card is not decision-ready"})
    if audit.get("summary", {}).get("review", 0):
        rows.append({"id": "audit_trail", "from": "pass", "to": "review", "reason": "latest audit trail has review items"})
    return rows


def _cycle_next_actions(
    hash_drift: List[Dict[str, Any]],
    added: List[Dict[str, Any]],
    removed: List[Dict[str, Any]],
    changed: List[Dict[str, Any]],
    transitions: List[Dict[str, Any]],
    card: Dict[str, Any],
    audit: Dict[str, Any],
) -> List[str]:
    actions = []
    if added:
        actions.append("Review newly added watchlist items before relying on the memo.")
    if removed:
        actions.append("Confirm removed watchlist items are intentionally resolved or out of scope.")
    if changed:
        actions.append("Re-read changed watchlist severity, status, and trigger text.")
    if any(item["status"] != "unchanged" for item in hash_drift):
        actions.append("Reconcile baseline artifact hash drift against the latest audit trail.")
    if not card.get("summary", {}).get("decision_ready"):
        actions.append("Close latest report-card unresolved checks before the next review signoff.")
    if audit.get("summary", {}).get("review", 0):
        actions.append("Fix or explain audit-trail review rows before treating artifacts as current.")
    if transitions:
        actions.append("Record status transitions in the next cycle update.")
    return _unique_text(actions or ["Continue the existing review cadence placeholders."])


def _guardrail_observed_metrics(
    portfolio: Dict[str, Any],
    position: Dict[str, Any],
    memo: Dict[str, Any],
    cycle: Dict[str, Any],
) -> Dict[str, Any]:
    portfolio_summary = portfolio.get("summary", {})
    position_inputs = position.get("inputs", {})
    scenario = position.get("scenario", {})
    memo_risk = memo.get("risk_budget", {})
    memo_base = memo.get("scenario_evidence", {}).get("base_case", {})
    cycle_summary = cycle.get("summary", {})
    holding_days = _first_number(memo_base.get("days"), scenario.get("days"))
    loss_budget_pct = _first_number(position_inputs.get("risk_budget_pct"), memo_risk.get("risk_budget_pct"))
    return {
        "leverage_exposure": _first_number(
            portfolio_summary.get("aggregate_worst_case_weighted_exposure"),
            portfolio_summary.get("base_weighted_exposure"),
        ),
        "loss_budget_pct": loss_budget_pct,
        "holding_days": holding_days,
        "aggregate_worst_case_loss_pct": _first_number(portfolio_summary.get("aggregate_worst_case_loss_pct")),
        "position_exposure_multiple": _first_number(position.get("recommendation", {}).get("exposure_multiple")),
        "memo_open_checks": len(memo.get("open_checks", [])),
        "memo_invalidation_triggers": len(memo.get("invalidation_triggers", [])),
        "memo_critical_triggers": _trigger_count(memo, {"critical"}),
        "memo_high_triggers": _trigger_count(memo, {"high"}),
        "cycle_decision_ready": bool(cycle_summary.get("decision_ready")),
        "cycle_hash_drift": _first_number(cycle_summary.get("hash_drift")) or 0,
        "cycle_changed_watch_items": _first_number(cycle_summary.get("changed_watch_items")) or 0,
        "cycle_added_watch_items": _first_number(cycle_summary.get("added_watch_items")) or 0,
        "cycle_removed_watch_items": _first_number(cycle_summary.get("removed_watch_items")) or 0,
        "cycle_status_transitions": _first_number(cycle_summary.get("status_transitions")) or 0,
    }


def _guardrail_limit_rule(
    rule_id: str,
    label: str,
    observed: Optional[float],
    limit: Any,
    violation_status: str,
    action: str,
) -> Dict[str, Any]:
    numeric_limit = _optional_number(limit)
    failed = observed is None or numeric_limit is None or float(observed) > numeric_limit
    return {
        "id": rule_id,
        "label": label,
        "status": violation_status if failed else "pass",
        "observed": observed,
        "limit": numeric_limit,
        "action": action if failed else "No action required.",
    }


def _guardrail_artifact_rule(
    policy: Dict[str, Any],
    portfolio: Dict[str, Any],
    position: Dict[str, Any],
    memo: Dict[str, Any],
    cycle: Dict[str, Any],
) -> Dict[str, Any]:
    required = [str(item) for item in policy.get("required_artifacts", [])]
    present = [detect_report_type(item) for item in [portfolio, position, memo, cycle]]
    missing = [item for item in required if item not in present]
    return {
        "id": "required_artifacts",
        "label": "Required artifact types",
        "status": "fail" if missing else "pass",
        "observed": ",".join(sorted(present)),
        "limit": ",".join(required),
        "action": "Regenerate or pass the missing required artifact type(s): " + ", ".join(missing)
        if missing
        else "No action required.",
    }


def _guardrail_modeled_loss_rule(observed: Dict[str, Any], limits: Dict[str, Any]) -> Dict[str, Any]:
    loss = _optional_number(observed.get("aggregate_worst_case_loss_pct"))
    budget = _optional_number(limits.get("max_loss_budget_pct"))
    breached = loss is not None and budget is not None and loss > budget
    return {
        "id": "aggregate_modeled_loss_review",
        "label": "Aggregate modeled loss review",
        "status": "review" if breached else "pass",
        "observed": loss,
        "limit": budget,
        "action": "Review aggregate modeled portfolio loss against the stated budget before proceeding."
        if breached
        else "No action required.",
    }


def _guardrail_memo_open_checks_rule(memo: Dict[str, Any], policy_id: Any) -> Dict[str, Any]:
    count = len(memo.get("open_checks", []))
    if policy_id == "aggressive":
        breached = count > 5
        limit = 5
    else:
        breached = count > 0
        limit = 0
    return {
        "id": "memo_open_checks",
        "label": "Investment memo open checks",
        "status": "review" if breached else "pass",
        "observed": count,
        "limit": limit,
        "action": "Close or explicitly accept memo open checks before relying on the allocation."
        if breached
        else "No action required.",
    }


def _guardrail_memo_trigger_rule(memo: Dict[str, Any], policy_id: Any) -> Dict[str, Any]:
    triggers = memo.get("invalidation_triggers", [])
    if policy_id == "conservative":
        count = len(triggers)
        limit = 0
        label = "Any memo invalidation trigger"
    elif policy_id == "aggressive":
        count = _trigger_count(memo, {"critical"})
        limit = 0
        label = "Critical memo invalidation triggers"
    else:
        count = _trigger_count(memo, {"critical", "high"})
        limit = 0
        label = "Critical or high memo invalidation triggers"
    return {
        "id": "memo_invalidation_triggers",
        "label": label,
        "status": "review" if count > limit else "pass",
        "observed": count,
        "limit": limit,
        "action": "Review memo invalidation triggers and regenerate memo artifacts if the thesis changed."
        if count > limit
        else "No action required.",
    }


def _guardrail_cycle_ready_rule(cycle: Dict[str, Any]) -> Dict[str, Any]:
    ready = bool(cycle.get("summary", {}).get("decision_ready"))
    return {
        "id": "cycle_decision_ready",
        "label": "Cycle update decision ready",
        "status": "pass" if ready else "review",
        "observed": ready,
        "limit": True,
        "action": "Resolve cycle-update next review actions before proceeding." if not ready else "No action required.",
    }


def _guardrail_cycle_change_rule(cycle: Dict[str, Any], policy_id: Any) -> Dict[str, Any]:
    summary = cycle.get("summary", {})
    changed = int(_first_number(summary.get("changed_watch_items")) or 0)
    added = int(_first_number(summary.get("added_watch_items")) or 0)
    removed = int(_first_number(summary.get("removed_watch_items")) or 0)
    drift = int(_first_number(summary.get("hash_drift")) or 0)
    transitions = int(_first_number(summary.get("status_transitions")) or 0)
    if policy_id == "conservative":
        observed = changed + added + removed + transitions
        breached = observed > 0
        label = "Any cycle watch or status transition"
    elif policy_id == "aggressive":
        observed = changed + drift + max(0, transitions - 1)
        breached = observed > 0
        label = "Cycle drift, changed watch items, or repeated transitions"
    else:
        observed = changed + added + removed
        breached = observed > 0
        label = "Cycle watch item changes"
    return {
        "id": "cycle_changes",
        "label": label,
        "status": "review" if breached else "pass",
        "observed": observed,
        "limit": 0,
        "action": "Review cycle-update watch item changes, hash drift, or status transitions."
        if breached
        else "No action required.",
    }


def _guardrail_next_actions(result: str, violated: List[Dict[str, Any]]) -> List[str]:
    if not violated:
        return ["Record guardrail pass with the reviewed artifact set."]
    actions = [str(rule.get("action")) for rule in violated if rule.get("action") and rule.get("action") != "No action required."]
    if result == "fail":
        actions.insert(0, "Do not treat the allocation as guardrail-compliant until failed rules are corrected.")
    else:
        actions.insert(0, "Complete review items before relying on the allocation packet.")
    return _unique_text(actions)[:10]


def _order_required_broker_fields() -> List[Dict[str, str]]:
    fields = [
        ("account", "Broker account must be selected outside this package."),
        ("symbol", "Confirm ticker and listing venue in broker UI."),
        ("side", "User must choose buy/sell or other permitted side."),
        ("quantity", "Convert notional to shares with an execution price outside this package."),
        ("order_type", "User must choose market, limit, stop, or other broker-supported type."),
        ("limit_or_stop_price", "Required when selected order type needs a price; no live price is provided here."),
        ("time_in_force", "User must choose day, GTC, or other broker-supported duration."),
        ("estimated_commission_and_fees", "Confirm broker preview costs outside this package."),
        ("liquidity_spread_halt_review", "Confirm spread, depth, halts, and trading status outside this package."),
    ]
    return [{"field": field, "status": "placeholder", "reason": reason} for field, reason in fields]


def _order_do_not_trade_conditions(
    guardrail: Dict[str, Any],
    memo: Dict[str, Any],
    factsheet: Dict[str, Any],
    dashboard: Optional[Dict[str, Any]],
) -> List[Dict[str, str]]:
    conditions = [
        {
            "id": "no_live_quote",
            "severity": "review",
            "condition": "No current broker quote, spread, liquidity, halt, and order preview has been reviewed.",
            "source": "order-ticket",
        },
        {
            "id": "broker_fields_incomplete",
            "severity": "review",
            "condition": "Any required broker field remains unset or inconsistent with the user's intent.",
            "source": "order-ticket",
        },
    ]
    result = str(guardrail.get("summary", {}).get("result"))
    if result == "fail":
        conditions.append(
            {
                "id": "guardrail_failed",
                "severity": "blocked",
                "condition": "Guardrail check result is fail.",
                "source": "guardrail_check",
            }
        )
    elif result == "review":
        conditions.append(
            {
                "id": "guardrail_review",
                "severity": "review",
                "condition": "Guardrail check has review items that have not been explicitly resolved.",
                "source": "guardrail_check",
            }
        )
    for rule in guardrail.get("violated_rules", [])[:6]:
        conditions.append(
            {
                "id": "guardrail_rule_" + str(rule.get("id", "unknown")),
                "severity": "blocked" if rule.get("status") == "fail" else "review",
                "condition": str(rule.get("action") or rule.get("label") or "Resolve guardrail rule."),
                "source": "guardrail_check",
            }
        )
    if memo.get("open_checks"):
        conditions.append(
            {
                "id": "memo_open_checks",
                "severity": "review",
                "condition": "Investment memo has open checks.",
                "source": "investment_memo",
            }
        )
    for trigger in memo.get("invalidation_triggers", [])[:4]:
        conditions.append(
            {
                "id": "memo_trigger_" + str(trigger.get("id") or trigger.get("severity") or "unknown"),
                "severity": "review",
                "condition": str(trigger.get("trigger") or "Review memo invalidation trigger."),
                "source": "investment_memo",
            }
        )
    missing = factsheet.get("missing_fields", [])
    if missing:
        conditions.append(
            {
                "id": "factsheet_missing_fields",
                "severity": "review",
                "condition": "Factsheet checklist has missing fields: " + ", ".join(str(item) for item in missing[:8]),
                "source": "factsheet_check",
            }
        )
    if dashboard and not dashboard.get("summary", {}).get("decision_ready"):
        conditions.append(
            {
                "id": "dashboard_not_ready",
                "severity": "review",
                "condition": "Thesis dashboard data is not decision-ready.",
                "source": "thesis_dashboard_data",
            }
        )
    return conditions


def _order_ticket_status(guardrail: Dict[str, Any], conditions: List[Dict[str, str]]) -> str:
    if guardrail.get("summary", {}).get("result") == "fail" or any(item["severity"] == "blocked" for item in conditions):
        return "blocked"
    if conditions:
        return "review"
    return "ready"


def _order_review_checklist(
    ticket: Dict[str, Any],
    guardrail: Dict[str, Any],
    cycle: Dict[str, Any],
    audit: Dict[str, Any],
) -> List[Dict[str, str]]:
    rows = [
        _order_review_row(
            "ticket_status",
            ticket.get("summary", {}).get("status") == "ready",
            "Order ticket status is ready.",
            "Review or block unresolved ticket conditions.",
            "blocked" if ticket.get("summary", {}).get("status") == "blocked" else "review",
        ),
        _order_review_row(
            "guardrail_status",
            guardrail.get("summary", {}).get("result") == "pass",
            "Guardrail check passed.",
            "Resolve guardrail review or failed rules.",
            "blocked" if guardrail.get("summary", {}).get("result") == "fail" else "review",
        ),
        _order_review_row(
            "cycle_current",
            bool(cycle.get("summary", {}).get("decision_ready")),
            "Cycle update is decision-ready.",
            "Resolve cycle update next review actions.",
            "review",
        ),
        _order_review_row(
            "audit_current",
            int(_first_number(audit.get("summary", {}).get("review")) or 0) == 0,
            "Audit trail has no review rows.",
            "Reconcile audit-trail review rows before final signoff.",
            "review",
        ),
        _order_review_row(
            "no_live_price_acknowledged",
            bool(ticket.get("no_live_price_warning")),
            "No-live-price warning is present.",
            "Regenerate ticket with no-live-price warning.",
            "blocked",
        ),
        _order_review_row(
            "broker_execution_disabled",
            ticket.get("provenance", {}).get("broker_execution") is False,
            "Package confirms no broker execution.",
            "Stop and inspect provenance before use.",
            "blocked",
        ),
    ]
    if ticket.get("do_not_trade_if"):
        rows.append(
            {
                "id": "do_not_trade_conditions",
                "status": "review",
                "item": f"{len(ticket.get('do_not_trade_if', []))} do-not-trade conditions require external signoff.",
                "action": "Resolve or explicitly reject every do-not-trade condition outside this package.",
            }
        )
    return rows


def _order_review_row(
    row_id: str,
    passed: bool,
    item: str,
    action: str,
    failure_status: str,
) -> Dict[str, str]:
    return {
        "id": row_id,
        "status": "ready" if passed else failure_status,
        "item": item,
        "action": "No action required." if passed else action,
    }


def _trigger_count(memo: Dict[str, Any], severities: set[str]) -> int:
    return sum(1 for item in memo.get("invalidation_triggers", []) if str(item.get("severity")) in severities)


def _first_number(*values: Any) -> Optional[float]:
    for value in values:
        parsed = _optional_number(value)
        if parsed is not None:
            return parsed
    return None


def _require_type(data: Dict[str, Any], document_type: str, path: str) -> None:
    detected = detect_report_type(data)
    if detected != document_type:
        raise ValueError(f"{_display_path(path)} must be a {document_type} JSON output")


def _severity_rank(value: str) -> int:
    return {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(value, 4)


def _dashboard_recipe_card(recipe: Dict[str, Any]) -> Dict[str, Any]:
    summary = recipe.get("summary", {})
    return {
        "product": summary.get("product"),
        "components": summary.get("components"),
        "scenario_days": summary.get("scenario_days"),
        "scenario_return_pct": summary.get("scenario_return_pct"),
        "recommended_notional": summary.get("recommended_notional"),
        "watchlist_entries": summary.get("watchlist_entries"),
    }


def _dashboard_readiness_card(card: Dict[str, Any]) -> Dict[str, Any]:
    summary = card.get("summary", {})
    return {
        "decision_ready": summary.get("decision_ready"),
        "artifact_count": summary.get("artifacts"),
        "document_types": summary.get("document_types", []),
        "strengths": summary.get("strengths"),
        "unresolved_checks": summary.get("unresolved_checks"),
        "warnings": summary.get("warnings"),
        "next_commands": card.get("next_commands", [])[:5],
    }


def _dashboard_watchlist_card(watchlist: Dict[str, Any], top_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "summary": dict(watchlist.get("summary", {})),
        "top_entries": [
            {
                "id": str(item.get("id")),
                "category": str(item.get("category")),
                "severity": str(item.get("severity")),
                "status": str(item.get("status")),
                "title": str(item.get("title")),
                "trigger": str(item.get("trigger")),
            }
            for item in top_entries
        ],
    }


def _dashboard_sensitivity_card(sensitivity: Dict[str, Any]) -> Dict[str, Any]:
    summary = sensitivity.get("summary", {})
    return {
        "combinations": summary.get("combinations"),
        "worst_return_pct": summary.get("worst_return_pct"),
        "worst_return_regime": summary.get("worst_return_regime"),
        "worst_return_leverage": summary.get("worst_return_leverage"),
        "worst_path_decay_vs_simple_multiple": summary.get("worst_path_decay_vs_simple_multiple"),
        "max_stop_events": summary.get("max_stop_events"),
    }


def _dict_value(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _recipe_artifact(recipe: Dict[str, Any], key: str) -> Optional[Dict[str, Any]]:
    value = recipe.get("artifacts", {}).get(key)
    return value if isinstance(value, dict) else None


def _factsheet_summary(factsheet: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not factsheet:
        return {"available": False, "passed": None, "review": None, "missing": None, "missing_fields": []}
    summary = factsheet.get("summary", {})
    return {
        "available": True,
        "passed": summary.get("passed"),
        "review": summary.get("review"),
        "missing": summary.get("missing"),
        "ready_for_review": summary.get("ready_for_review"),
        "missing_fields": factsheet.get("missing_fields", []),
    }


def _memo_watch_entries(source: Dict[str, Any]) -> List[Dict[str, Any]]:
    entries = source.get("entries") or source.get("top_entries") or []
    result = []
    for item in entries[:10]:
        if not isinstance(item, dict):
            continue
        result.append(
            {
                "id": str(item.get("id")),
                "category": str(item.get("category")),
                "severity": str(item.get("severity")),
                "status": str(item.get("status")),
                "title": str(item.get("title")),
                "trigger": str(item.get("trigger")),
            }
        )
    return sorted(result, key=lambda item: (_severity_rank(item["severity"]), item["id"]))


def _memo_open_checks(card: Dict[str, Any], factsheet: Optional[Dict[str, Any]]) -> List[Dict[str, str]]:
    checks = [{"source": "report_card", "text": str(item)} for item in card.get("unresolved_checks", [])[:12]]
    if factsheet:
        for field in factsheet.get("missing_fields", []):
            checks.append({"source": "factsheet_check", "text": f"Missing factsheet field: {field}"})
        for item in factsheet.get("checks", []):
            if item.get("status") == "review":
                checks.append({"source": "factsheet_check", "text": f"Review factsheet field: {item.get('field')}"})
    return [{"id": f"check_{index}", **item} for index, item in enumerate(_unique_check_items(checks), start=1)]


def _unique_check_items(items: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen = set()
    result = []
    for item in items:
        key = item.get("text", "")
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def _memo_invalidation_triggers(
    watch_entries: List[Dict[str, Any]], card: Dict[str, Any], dashboard: Dict[str, Any]
) -> List[Dict[str, str]]:
    triggers = []
    for entry in watch_entries:
        if entry["severity"] in {"critical", "high", "medium"}:
            triggers.append(
                {
                    "id": entry["id"],
                    "source": "watchlist",
                    "severity": entry["severity"],
                    "status": entry["status"],
                    "category": entry["category"],
                    "title": entry["title"],
                    "trigger": entry["trigger"],
                    "action": "re-review memo before any trade action.",
                }
            )
    summary = dashboard.get("summary", {})
    if summary.get("worst_grid_return_pct") is not None:
        triggers.append(
            {
                "id": "worst_grid_return",
                "source": "thesis_dashboard_data",
                "severity": "high" if float(summary.get("worst_grid_return_pct", 0.0)) <= -10 else "medium",
                "status": "review",
                "trigger": f"Worst grid return is {summary.get('worst_grid_return_pct')}% in {summary.get('worst_grid_regime')}.",
                "action": "confirm loss budget still covers the modeled adverse regime.",
            }
        )
    if not card.get("summary", {}).get("decision_ready"):
        triggers.append(
            {
                "id": "decision_not_ready",
                "source": "report_card",
                "severity": "medium",
                "status": "review",
                "trigger": "Report card is not decision-ready.",
                "action": "close open checks before relying on the memo.",
            }
        )
    return _unique_trigger_items(triggers)[:12]


def _unique_trigger_items(items: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen = set()
    result = []
    for item in items:
        key = item.get("id", "") or item.get("trigger", "")
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def _memo_stress_summary(stress: Dict[str, Any]) -> Dict[str, Any]:
    rows = stress.get("rows", [])
    worst = _lowest_report_card_row(rows, "return_pct")
    drawdown = _lowest_report_card_row(rows, "worst_drawdown_pct")
    return {
        "regimes": len(rows),
        "weakest_return_regime": worst.get("regime"),
        "weakest_return_pct": worst.get("return_pct"),
        "largest_drawdown_regime": drawdown.get("regime"),
        "largest_drawdown_pct": drawdown.get("worst_drawdown_pct"),
    }


def _memo_changed_risks(memo_triggers: Dict[str, Dict[str, Any]], latest_entries: Dict[str, Dict[str, Any]]) -> List[Dict[str, str]]:
    changed = []
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    for risk_id in sorted(set(memo_triggers) | set(latest_entries)):
        old = memo_triggers.get(risk_id)
        new = latest_entries.get(risk_id)
        if old and not new:
            changed.append({"id": risk_id, "change": "removed", "detail": str(old.get("trigger", ""))})
        elif new and not old:
            changed.append({"id": risk_id, "change": "added", "detail": str(new.get("trigger", ""))})
        elif old and new:
            old_sev = str(old.get("severity", "low"))
            new_sev = str(new.get("severity", "low"))
            if old_sev != new_sev or str(old.get("status", "")) != str(new.get("status", "")):
                direction = "worsened" if severity_order.get(new_sev, 9) < severity_order.get(old_sev, 9) else "changed"
                changed.append(
                    {
                        "id": risk_id,
                        "change": direction,
                        "detail": f"{old_sev}/{old.get('status', 'n/a')} -> {new_sev}/{new.get('status', 'n/a')}",
                    }
                )
    return changed


def _memo_review_checklist(
    memo: Dict[str, Any],
    card: Dict[str, Any],
    watchlist: Dict[str, Any],
    audit: Dict[str, Any],
    changed: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    items = [
        (
            "memo_not_investment_advice",
            "Memo contains not-investment-advice language.",
            "pass" if "not investment advice" in str(memo.get("not_investment_advice", "")).lower() else "review",
            "Keep explicit educational framing in the memo.",
        ),
        (
            "report_card_decision_ready",
            "Latest report-card is decision-ready.",
            "pass" if card.get("summary", {}).get("decision_ready") else "review",
            "Resolve latest report-card unresolved checks and warnings.",
        ),
        (
            "watchlist_risks_stable",
            "Watchlist has no added or changed memo risks.",
            "pass" if not changed else "review",
            "Update memo invalidation triggers from latest watchlist.",
        ),
        (
            "audit_trail_passed",
            "Audit trail hashes pass for reviewed artifacts.",
            "pass" if audit.get("summary", {}).get("review", 0) == 0 else "review",
            "Regenerate ledger or investigate artifacts with audit review status.",
        ),
        (
            "open_checks_closed",
            "Memo open checks are closed or accepted.",
            "pass" if not memo.get("open_checks") else "review",
            "Close or explicitly accept each memo open check.",
        ),
        (
            "critical_watchlist_clear",
            "Latest watchlist has no critical entries.",
            "pass" if watchlist.get("summary", {}).get("critical", 0) == 0 else "review",
            "Escalate critical watchlist triggers before any decision review.",
        ),
    ]
    return [{"id": item[0], "item": item[1], "status": item[2], "action": item[3]} for item in items]


def _memo_next_actions(
    checklist: List[Dict[str, str]], changed: List[Dict[str, str]], card: Dict[str, Any], audit: Dict[str, Any]
) -> List[str]:
    actions = [item["action"] for item in checklist if item["status"] != "pass"]
    if changed:
        actions.append("Regenerate memo-draft after reviewing changed watchlist risks.")
    actions.extend(str(item) for item in card.get("next_commands", [])[:2])
    if audit.get("summary", {}).get("review", 0):
        actions.append("Run audit-trail after regenerating the affected artifacts.")
    return _unique_text(actions)[:8]


def _load_ledger_rows(ledger_path: str) -> List[Dict[str, Any]]:
    rows = []
    with Path(ledger_path).open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            data = json.loads(text)
            if not isinstance(data, dict):
                raise ValueError(f"ledger line {line_number} is not a JSON object")
            rows.append(data)
    return rows


def _audit_artifact(path: str) -> Dict[str, Any]:
    artifact = Path(path)
    payload = artifact.read_bytes()
    document_type = "file"
    schema_version = None
    if artifact.suffix == ".json":
        try:
            data = json.loads(payload.decode("utf-8"))
            if isinstance(data, dict):
                document_type = detect_report_type(data)
                schema_version = data.get("schema_version")
        except json.JSONDecodeError:
            document_type = "json_parse_error"
        except UnicodeDecodeError:
            document_type = "binary_file"
    elif artifact.suffix == ".jsonl":
        document_type = "run_ledger"
        schema_version = _jsonl_schema_version(artifact)
    return {
        "artifact_name": artifact.name,
        "path": _display_path(path),
        "document_type": document_type,
        "schema_version": schema_version,
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def _report_card_next_commands(document_types: set[str], warnings: List[str], unresolved: List[str]) -> List[str]:
    commands = []
    if "pretrade_plan" not in document_types:
        commands.append(
            "python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --format markdown"
        )
    if "position_size_plan" not in document_types:
        commands.append(
            "python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015 --format markdown"
        )
    if "stress_matrix" not in document_types:
        commands.append(
            "python -m leveraged_etp_risk_lab stress-matrix --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss 0.15 --take-profit 0.20 --format markdown"
        )
    if "sensitivity_grid" not in document_types:
        commands.append(
            "python -m leveraged_etp_risk_lab sensitivity-grid --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss none,0.15,0.25 --take-profit none,0.20,0.35 --format markdown"
        )
    if "factsheet_check" not in document_types:
        commands.append(
            "python -m leveraged_etp_risk_lab factsheet-check --product examples/fixtures/leveraged_nasdaq_3x.json --factsheet-file examples/fixtures/factsheet_note.txt --format markdown"
        )
    if warnings or unresolved:
        commands.append(
            "python -m leveraged_etp_risk_lab report-card --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/position_size.json --artifact examples/outputs/stress_matrix.json --artifact examples/outputs/factsheet_check.json --format markdown"
        )
    commands.append("python -m leveraged_etp_risk_lab package-audit --format markdown --run-tests")
    return _unique_text(commands)[:6]


def _lowest_report_card_row(rows: List[Dict[str, Any]], key: str) -> Dict[str, Any]:
    numeric = [row for row in rows if isinstance(row.get(key), (int, float))]
    if not numeric:
        return {}
    return min(numeric, key=lambda row: row[key])


def _warning_delta(base: List[str], candidate: List[str]) -> Dict[str, Any]:
    base_set = set(base)
    candidate_set = set(candidate)
    return {
        "added": sorted(candidate_set - base_set),
        "removed": sorted(base_set - candidate_set),
        "unchanged_count": len(base_set.intersection(candidate_set)),
    }


def _numeric_delta(base: Optional[float], candidate: Optional[float]) -> Optional[float]:
    if base is None or candidate is None:
        return None
    return round(candidate - base, 6)


def _optional_number(value: Any) -> Optional[float]:
    if value is None:
        return None
    return round(float(value), 6)


def _flush_claim_paragraph(paragraph: List[str], claims: List[str]) -> None:
    if not paragraph:
        return
    claim = " ".join(paragraph).strip()
    if claim:
        claims.append(claim)
    paragraph.clear()


def _map_claim_to_artifacts(
    claim: Dict[str, str], artifacts: List[Dict[str, Any]], warnings: List[str]
) -> Dict[str, Any]:
    text = claim["text"]
    lower = text.lower()
    metric_names = _claim_metric_names(lower)
    observed = []
    statuses = []
    for artifact in artifacts:
        for metric_name in metric_names:
            value = artifact["metrics"].get(metric_name)
            if value is None:
                continue
            interpretation = _interpret_metric(lower, metric_name, value)
            observed.append(
                {
                    "artifact": artifact["path"],
                    "label": artifact["label"],
                    "metric": metric_name,
                    "value": value,
                    "interpretation": interpretation,
                }
            )
            statuses.append(interpretation)
    related_warnings = _related_warnings(lower, warnings)
    checklist = _claim_checklist(lower)
    status = _claim_status(statuses, related_warnings)
    return {
        "claim_id": claim["id"],
        "claim": text,
        "status": status,
        "observed_metrics": observed,
        "warnings": related_warnings,
        "checklist": checklist,
    }


def _claim_metric_names(lower: str) -> List[str]:
    metrics = []
    if any(word in lower for word in ["recover", "return", "upside", "rally", "flat"]):
        metrics.append("return_pct")
    if any(word in lower for word in ["choppy", "decay", "volatility", "daily-reset", "daily reset", "simple multiple"]):
        metrics.append("path_decay_vs_simple_multiple")
    if any(word in lower for word in ["leverage", "exposure", "portfolio", "concentration"]):
        metrics.append("weighted_exposure")
    if not metrics:
        metrics = ["return_pct", "path_decay_vs_simple_multiple", "weighted_exposure"]
    return metrics


def _interpret_metric(lower: str, metric_name: str, value: float) -> str:
    if metric_name == "return_pct":
        if any(word in lower for word in ["recover", "upside", "rally"]) and value <= 0:
            return "challenges positive-return claim"
        if any(word in lower for word in ["loss", "reject", "stop"]) and value < 0:
            return "confirms downside scenario is present"
        return "observed return metric"
    if metric_name == "path_decay_vs_simple_multiple":
        if value < 0:
            return "shows modeled path decay"
        if value > 0:
            return "does not show modeled decay in this artifact"
        return "no modeled path-decay difference"
    if metric_name == "weighted_exposure":
        if abs(value) >= 2:
            return "shows elevated leveraged exposure"
        return "shows limited aggregate exposure"
    return "observed metric"


def _related_warnings(lower: str, warnings: List[str]) -> List[str]:
    keywords = {
        "return": ["return", "forecast", "path"],
        "recover": ["return", "forecast", "path"],
        "loss": ["loss", "stop", "drawdown"],
        "stop": ["loss", "stop"],
        "decay": ["decay", "reset", "choppy", "volatility", "simple multiple"],
        "choppy": ["decay", "reset", "choppy", "volatility"],
        "leverage": ["leverage", "exposure", "daily reset"],
        "exposure": ["leverage", "exposure", "concentration"],
        "liquidity": ["liquidity", "execution"],
        "event": ["event", "earnings", "macro"],
    }
    selected_terms = []
    for token, terms in keywords.items():
        if token in lower:
            selected_terms.extend(terms)
    if not selected_terms:
        selected_terms = ["risk", "leverage", "path", "loss"]
    matched = []
    for warning in warnings:
        warning_lower = warning.lower()
        if any(term in warning_lower for term in selected_terms):
            matched.append(warning)
    return _unique_text(matched[:5])


def _claim_checklist(lower: str) -> List[str]:
    items = ["Record whether the observed artifact metrics support, challenge, or leave the claim unresolved."]
    if any(word in lower for word in ["recover", "return", "upside", "rally"]):
        items.append("Compare the thesis return expectation with modeled ETP and underlying returns.")
    if any(word in lower for word in ["choppy", "decay", "volatility", "daily-reset", "daily reset"]):
        items.append("Review path decay versus the simple multiple before relying on multi-day leverage.")
    if any(word in lower for word in ["loss", "budget", "stop", "reject"]):
        items.append("Confirm loss budget and stop band are acceptable before entry.")
    if any(word in lower for word in ["liquidity", "execution", "spread"]):
        items.append("Complete a liquidity and execution-quality review outside this model.")
    if any(word in lower for word in ["event", "earnings", "macro", "regulatory"]):
        items.append("Check event risk before treating the scenario as actionable.")
    if any(word in lower for word in ["leverage", "exposure", "portfolio", "concentration"]):
        items.append("Check aggregate exposure and concentration against portfolio limits.")
    return _unique_text(items)


def _claim_status(statuses: List[str], warnings: List[str]) -> str:
    if any(status.startswith("challenges") for status in statuses):
        return "challenged"
    if statuses and not warnings:
        return "observed"
    return "needs_review"


def _display_path(path: str) -> str:
    value = Path(path)
    return value.as_posix() if not value.is_absolute() else value.name


def _display_value(value: Any) -> str:
    if value is None:
        return "n/a"
    return str(value)


def _unique_text(items: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
