from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

DEMO_STORY_SCHEMA_VERSION = "0.12"


def to_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def simulation_markdown(data: Dict[str, Any]) -> str:
    product = data["product"]
    summary = data["summary"]
    lines: List[str] = [
        f"# Simulation: {product['ticker']}",
        "",
        f"- Product: {product['name']}",
        f"- Underlying: {product['underlying']}",
        f"- Leverage: {product['leverage']}x daily reset",
        f"- Annual fee: {product['annual_fee_pct']}%",
        f"- Ending ETP NAV: {summary['ending_etp_nav']}",
        f"- ETP return: {summary['etp_return_pct']}%",
        f"- Underlying return: {summary['underlying_return_pct']}%",
        f"- Simple multiple return: {summary['simple_multiple_return_pct']}%",
        f"- Path decay vs simple multiple: {summary['path_decay_vs_simple_multiple']}",
        "",
        "## Band Events",
        "",
    ]
    if data["band_events"]:
        for event in data["band_events"]:
            lines.append(f"- Day {event['day']} ({event['label']}): {event['event']} at NAV {event['nav']}")
    else:
        lines.append("- None")
    lines.extend(["", "## Path", "", _table(data["path"]), "", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in data["warnings"])
    return "\n".join(lines) + "\n"


def exposure_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    portfolio = data["portfolio"]
    lines: List[str] = [
        f"# Exposure Report: {portfolio['name']}",
        "",
        f"- Base currency: {portfolio['base_currency']}",
        f"- Starting value: {summary['starting_value']}",
        f"- Ending value: {summary['ending_value']}",
        f"- Return: {summary['return_pct']}%",
        f"- Weighted exposure: {summary['weighted_exposure']}x",
        f"- Worst drawdown approximation: {summary['worst_drawdown_pct']}%",
        "",
        "## Positions",
        "",
        _table_with_headers(
            data["positions"],
            ["id", "ticker", "notional", "notional_weight_pct", "leverage", "weighted_exposure", "ending_value", "return_pct"],
        ),
        "",
        "## Stop Events",
        "",
    ]
    if data["stop_events"]:
        for event in data["stop_events"]:
            lines.append(
                f"- {event['position_id']} ({event['ticker']}), day {event['day']} ({event['label']}): "
                f"{event['event']} at NAV {event['nav']}"
            )
    else:
        lines.append("- None")
    lines.extend(["", "## Portfolio Path", "", _table_with_headers(data["portfolio_path"], ["day", "value"]), "", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in data["warnings"])
    return "\n".join(lines) + "\n"


def pretrade_plan_packet(
    simulation: Dict[str, Any],
    thesis: str,
    max_loss_budget: float,
    checklist_profile: str,
    assumptions: List[str],
    provenance: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": "0.3",
        "document_type": "pretrade_plan",
        "not_investment_advice": (
            "This decision packet is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "product": simulation["product"],
        "scenario": {
            "days": simulation["inputs"]["days"],
            "ending_etp_nav": simulation["summary"]["ending_etp_nav"],
            "etp_return_pct": simulation["summary"]["etp_return_pct"],
            "underlying_return_pct": simulation["summary"]["underlying_return_pct"],
            "path_decay_vs_simple_multiple": simulation["summary"]["path_decay_vs_simple_multiple"],
        },
        "risk_bands": {
            "stop_loss_pct": simulation["inputs"]["stop_loss_pct"],
            "take_profit_pct": simulation["inputs"]["take_profit_pct"],
            "band_events": simulation["band_events"],
        },
        "budget": {
            "max_loss_budget": round(float(max_loss_budget), 6),
            "currency": simulation["product"]["currency"],
        },
        "thesis": thesis.strip() or "No thesis text provided.",
        "assumptions": assumptions,
        "checklist": {"profile": checklist_profile, "items": checklist_items(checklist_profile)},
        "warnings": _unique_text(
            simulation["warnings"]
            + [
                "A pretrade plan does not confirm liquidity, execution quality, tax treatment, or suitability.",
                "Stop-loss and take-profit bands are planning levels, not guaranteed execution prices.",
            ]
        ),
        "provenance": provenance,
    }


def pretrade_plan_markdown(data: Dict[str, Any]) -> str:
    product = data["product"]
    scenario = data["scenario"]
    budget = data["budget"]
    risk_bands = data["risk_bands"]
    lines: List[str] = [
        f"# Pretrade Plan: {product['ticker']}",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Product",
        "",
        f"- Product: {product['name']}",
        f"- Underlying: {product['underlying']}",
        f"- Daily leverage: {product['leverage']}x",
        f"- Reset frequency: {product['reset_frequency']}",
        f"- Annual fee: {product['annual_fee_pct']}%",
        "",
        "## Thesis",
        "",
        data["thesis"],
        "",
        "## Scenario Summary",
        "",
        f"- Scenario days: {scenario['days']}",
        f"- Ending ETP NAV: {scenario['ending_etp_nav']}",
        f"- ETP return: {scenario['etp_return_pct']}%",
        f"- Underlying return: {scenario['underlying_return_pct']}%",
        f"- Path decay vs simple multiple: {scenario['path_decay_vs_simple_multiple']}",
        "",
        "## Risk Budget And Bands",
        "",
        f"- Maximum loss budget: {budget['max_loss_budget']} {budget['currency']}",
        f"- Stop-loss band: {_display_pct(risk_bands['stop_loss_pct'])}",
        f"- Take-profit band: {_display_pct(risk_bands['take_profit_pct'])}",
        "",
        "### Band Events",
        "",
    ]
    if risk_bands["band_events"]:
        for event in risk_bands["band_events"]:
            lines.append(f"- Day {event['day']} ({event['label']}): {event['event']} at NAV {event['nav']}")
    else:
        lines.append("- None in modeled path")
    lines.extend(["", "## Assumptions", ""])
    lines.extend(f"- {item}" for item in data["assumptions"])
    lines.extend(["", "## Checklist", ""])
    lines.extend(f"- [ ] {item}" for item in data["checklist"]["items"])
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in data["warnings"])
    lines.extend(["", "## Command Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def position_size_markdown(data: Dict[str, Any]) -> str:
    product = data["product"]
    inputs = data["inputs"]
    recommendation = data["recommendation"]
    scenario = data["scenario"]
    lines: List[str] = [
        f"# Position Size Plan: {product['ticker']}",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Product",
        "",
        f"- Product: {product['name']}",
        f"- Underlying: {product['underlying']}",
        f"- Daily leverage: {product['leverage']}x",
        f"- Currency: {inputs['currency']}",
        "",
        "## Budget",
        "",
        f"- Account value: {inputs['account_value']} {inputs['currency']}",
        f"- Maximum loss budget: {inputs['max_loss_budget']} {inputs['currency']}",
        f"- Risk budget: {inputs['risk_budget_pct']}%",
        f"- Stop-loss: {_display_pct(inputs['stop_loss_pct'])}",
        f"- Loss basis: {inputs['loss_basis']}",
        "",
        "## Recommendation",
        "",
        f"- Recommended notional: {recommendation['recommended_notional']} {inputs['currency']}",
        "- Max shares: n/a",
        f"- Max shares placeholder: {recommendation['max_shares_placeholder']}",
        f"- Modeled loss at stop: {recommendation['modeled_loss_at_stop']} {inputs['currency']}",
        f"- Modeled loss as account percent: {recommendation['modeled_loss_pct_of_account']}%",
        f"- Exposure multiple: {recommendation['exposure_multiple']}x",
        "",
        "## Scenario",
        "",
        f"- Scenario days: {scenario['days']}",
        f"- Ending ETP NAV: {scenario['ending_etp_nav']}",
        f"- ETP return: {scenario['etp_return_pct']}%",
        f"- Underlying return: {scenario['underlying_return_pct']}%",
        f"- Path decay vs simple multiple: {scenario['path_decay_vs_simple_multiple']}",
        "",
        "## Checklist",
        "",
    ]
    lines.extend(f"- [ ] {item}" for item in data["checklist"])
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in data["warnings"])
    lines.extend(["", "## Command Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def stress_matrix_markdown(data: Dict[str, Any]) -> str:
    product = data["product"]
    inputs = data["inputs"]
    lines: List[str] = [
        f"# Stress Matrix: {product['ticker']}",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        f"- Product: {product['name']}",
        f"- Underlying: {product['underlying']}",
        f"- Daily leverage: {product['leverage']}x",
        f"- Initial NAV: {inputs['initial_nav']}",
        f"- Stop-loss: {_display_pct(inputs['stop_loss_pct'])}",
        f"- Take-profit: {_display_pct(inputs['take_profit_pct'])}",
        "",
        "## Matrix",
        "",
        _table_with_headers(
            data["rows"],
            [
                "regime",
                "name",
                "days",
                "underlying_return_pct",
                "return_pct",
                "path_decay_vs_simple_multiple",
                "worst_drawdown_pct",
                "stop_events",
                "warnings_count",
            ],
        ),
        "",
        "## Stop Events",
        "",
    ]
    for row in data["rows"]:
        labels = row["stop_event_labels"] or ["None"]
        lines.append(f"- {row['regime']}: {', '.join(labels)}")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in data["warnings"])
    lines.extend(["", "## Command Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def sensitivity_grid_markdown(data: Dict[str, Any]) -> str:
    product = data["product"]
    inputs = data["inputs"]
    summary = data["summary"]
    lines: List[str] = [
        f"# Sensitivity Grid: {product['ticker']}",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        f"- Product: {product['name']}",
        f"- Underlying: {product['underlying']}",
        f"- Base leverage: {product['base_leverage']}x",
        f"- Initial NAV: {inputs['initial_nav']}",
        f"- Regimes: {', '.join(inputs['regimes'])}",
        f"- Leverage grid: {', '.join(str(item) + 'x' for item in inputs['leverage_multipliers'])}",
        f"- Stop-loss grid: {', '.join(_display_pct(item) for item in inputs['stop_loss_pct_grid'])}",
        f"- Take-profit grid: {', '.join(_display_pct(item) for item in inputs['take_profit_pct_grid'])}",
        "",
        "## Summary",
        "",
        f"- Combinations: {summary['combinations']}",
        f"- Worst return: {summary['worst_return_pct']}% in {summary['worst_return_regime']} at {summary['worst_return_leverage']}x",
        f"- Worst path decay: {summary['worst_path_decay_vs_simple_multiple']} in {summary['worst_path_decay_regime']}",
        f"- Maximum stop/take events: {summary['max_stop_events']} at {summary['max_stop_events_leverage']}x",
        "",
        "## Matrix Summary",
        "",
        _table_with_headers(
            data["rows"],
            [
                "leverage",
                "stop_loss_pct",
                "take_profit_pct",
                "worst_return_regime",
                "worst_return_pct",
                "largest_drawdown_pct",
                "worst_path_decay_vs_simple_multiple",
                "stop_events",
                "warnings_count",
            ],
        ),
        "",
        "## Warnings",
        "",
    ]
    lines.extend(f"- {item}" for item in data["warnings"])
    lines.extend(["", "## Command Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def portfolio_sensitivity_markdown(data: Dict[str, Any]) -> str:
    portfolio = data["portfolio"]
    summary = data["summary"]
    lines = [
        f"# Portfolio Sensitivity: {portfolio['name']}",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Summary",
        "",
        f"- Base currency: {portfolio['base_currency']}",
        f"- Positions: {summary['positions']}",
        f"- Starting value: {summary['starting_value']}",
        f"- Base weighted exposure: {summary['base_weighted_exposure']}x",
        f"- Aggregate worst-case modeled loss: {summary['aggregate_worst_case_modeled_loss']}",
        f"- Aggregate worst-case loss: {summary['aggregate_worst_case_loss_pct']}%",
        f"- Aggregate worst-case weighted exposure: {summary['aggregate_worst_case_weighted_exposure']}x",
        f"- Weakest position: {_display_value(summary['weakest_position_id'])} in {_display_value(summary['weakest_position_regime'])}",
        "",
        "## Positions",
        "",
        "| id | ticker | notional | weight_pct | base_leverage | worst_return_pct | worst_regime | modeled_loss | weighted_exposure |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for position in data["positions"]:
        worst = position["worst_case"]
        lines.append(
            f"| {position['id']} | {position['ticker']} | {position['notional']} | "
            f"{position['notional_weight_pct']} | {position['base_leverage']} | "
            f"{_display_value(worst['return_pct'])} | {_display_value(worst['regime'])} | "
            f"{worst['modeled_loss']} | {worst['weighted_exposure']} |"
        )
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in data["warnings"])
    lines.extend(["", "## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def checklist_markdown(profile: str) -> str:
    items = checklist_items(profile)
    lines = [f"# Leveraged ETP Risk Checklist: {profile}", ""]
    lines.extend(f"- [ ] {item}" for item in items)
    return "\n".join(lines) + "\n"


def checklist_json(profile: str) -> str:
    return to_json({"schema_version": "0.2", "profile": profile, "items": checklist_items(profile)})


def template_gallery_markdown(data: Dict[str, Any]) -> str:
    lines: List[str] = [
        "# Product Template Gallery",
        "",
        f"- Schema version: {data['schema_version']}",
        f"- Templates: {len(data['templates'])}",
        "",
    ]
    for template in data["templates"]:
        lines.extend(
            [
                f"## {template['id']}",
                "",
                f"- Name: {template['name']}",
                f"- Ticker: {template['ticker']}",
                f"- Underlying: {template['underlying']}",
                f"- Leverage: {template['leverage']}x daily reset",
                f"- Annual fee: {round(float(template['annual_fee']) * 100.0, 4)}%",
                f"- Currency: {template['currency']}",
                "",
                "### Risk Notes",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in template["risk_notes"])
        lines.extend(["", "### Use Cases", ""])
        lines.extend(f"- {item}" for item in template["use_cases"])
        lines.append("")
    return "\n".join(lines) + "\n"


def regime_gallery_markdown(data: Dict[str, Any]) -> str:
    lines: List[str] = [
        "# Market Regime Gallery",
        "",
        f"- Schema version: {data['schema_version']}",
        f"- Regimes: {len(data['regimes'])}",
        "",
    ]
    for regime in data["regimes"]:
        lines.extend(
            [
                f"## {regime['id']}",
                "",
                f"- Name: {regime['name']}",
                f"- Description: {regime['description']}",
                f"- Default days: {regime['default_days']}",
                f"- Tags: {', '.join(regime['tags'])}",
                "",
                "### Sample Path",
                "",
                _table_with_headers(regime["sample_path"], ["day", "label", "underlying_return"]),
                "",
                "### Risk Notes",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in regime["risk_notes"])
        lines.extend(["", "### Use Cases", ""])
        lines.extend(f"- {item}" for item in regime["use_cases"])
        lines.append("")
    return "\n".join(lines) + "\n"


def glossary_markdown(data: Dict[str, Any]) -> str:
    lines: List[str] = [
        "# Leveraged Product Glossary",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        f"- Schema version: {data['schema_version']}",
        f"- Terms: {data['summary']['terms']}",
        "",
    ]
    for term in data["terms"]:
        lines.extend(
            [
                f"## {term['id']}",
                "",
                f"- Term: {term['term']}",
                f"- Plain language: {term['plain_language']}",
                f"- Why it matters: {term['why_it_matters']}",
                f"- Example: {term['example']}",
                f"- Related terms: {', '.join(term['related_terms'])}",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def glossary_term_markdown(data: Dict[str, Any]) -> str:
    term = data["term"]
    lines = [
        f"# {term['term']}",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        f"- Term id: {term['id']}",
        f"- Plain language: {term['plain_language']}",
        f"- Why it matters: {term['why_it_matters']}",
        f"- Example: {term['example']}",
        f"- Related terms: {', '.join(term['related_terms'])}",
        "",
        "## Provenance",
        "",
    ]
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def demo_story_packet(input_dir: Path) -> Dict[str, Any]:
    artifacts = {
        "stress_matrix": input_dir / "stress_matrix.json",
        "sensitivity_grid": input_dir / "sensitivity_grid.json",
        "watchlist": input_dir / "watchlist.json",
        "package_audit": input_dir / "package_audit.json",
        "pretrade_plan": input_dir / "pretrade_plan.json",
        "report_card": input_dir / "report_card.json",
        "investment_memo": input_dir / "investment_memo.json",
        "investment_memo_review": input_dir / "investment_memo_review.json",
        "cycle_state": input_dir / "cycle_state.json",
        "cycle_update": input_dir / "cycle_update.json",
        "guardrail_policy": input_dir / "guardrail_policy.json",
        "guardrail_check": input_dir / "guardrail_check.json",
        "order_ticket": input_dir / "order_ticket.json",
        "order_review": input_dir / "order_review.json",
    }
    data = {name: _load_required_json(path) for name, path in artifacts.items()}
    _require_document_type(data["stress_matrix"], "stress_matrix", artifacts["stress_matrix"])
    _require_document_type(data["sensitivity_grid"], "sensitivity_grid", artifacts["sensitivity_grid"])
    _require_document_type(data["watchlist"], "watchlist", artifacts["watchlist"])
    _require_document_type(data["package_audit"], "package_audit", artifacts["package_audit"])
    _require_document_type(data["pretrade_plan"], "pretrade_plan", artifacts["pretrade_plan"])
    _require_document_type(data["report_card"], "report_card", artifacts["report_card"])
    _require_document_type(data["investment_memo"], "investment_memo_packet", artifacts["investment_memo"])
    _require_document_type(data["investment_memo_review"], "investment_memo_review", artifacts["investment_memo_review"])
    _require_document_type(data["cycle_state"], "cycle_state", artifacts["cycle_state"])
    _require_document_type(data["cycle_update"], "cycle_update", artifacts["cycle_update"])
    _require_document_type(data["guardrail_policy"], "guardrail_policy", artifacts["guardrail_policy"])
    _require_document_type(data["guardrail_check"], "guardrail_check", artifacts["guardrail_check"])
    _require_document_type(data["order_ticket"], "order_ticket", artifacts["order_ticket"])
    _require_document_type(data["order_review"], "order_review", artifacts["order_review"])

    stress = data["stress_matrix"]
    sensitivity = data["sensitivity_grid"]
    watchlist = data["watchlist"]
    audit = data["package_audit"]
    plan = data["pretrade_plan"]
    card = data["report_card"]
    memo = data["investment_memo"]
    memo_review = data["investment_memo_review"]
    cycle_state = data["cycle_state"]
    cycle_update = data["cycle_update"]
    guardrail = data["guardrail_check"]
    ticket = data["order_ticket"]
    order_review = data["order_review"]
    product = plan["product"]
    scenario = plan["scenario"]
    worst_row = _lowest_row(stress.get("rows", []), "return_pct")
    highest_drawdown = _lowest_row(stress.get("rows", []), "worst_drawdown_pct")
    critical_entries = _entries_by_severity(watchlist, "critical")
    high_entries = _entries_by_severity(watchlist, "high")
    audit_summary = audit.get("summary", {})
    sections = {
        "problem": (
            "Daily-reset leveraged ETPs can diverge from a simple leverage multiple over multi-day paths. "
            "The public demo shows a generic product, deterministic paths, explicit risk bands, and review "
            "artifacts without using live prices or private context."
        ),
        "workflow": [
            "Start from generic product and path fixtures.",
            "Build a pretrade plan with thesis text, stop/take bands, a loss budget, and checklist items.",
            "Run the same product across built-in market regimes with stress-matrix.",
            "Use sensitivity-grid to compare leverage, stop-loss, and take-profit choices across every built-in regime.",
            "Convert thesis and regime results into a watchlist of review triggers.",
            "Use recipe-run when one JSON recipe should compose the public workflow into a single bundle.",
            "Use report-card to condense generated artifacts into strengths, unresolved checks, warnings, and next commands.",
            "Use memo-draft and memo-review to package the thesis and re-check it against latest public artifacts.",
            "Use cycle-init and cycle-update to persist a watch cycle, compare watchlist changes, and detect hash drift.",
            "Use guardrail-policy and guardrail-check to gate allocation artifacts against explicit exposure, loss-budget, holding-period, and review rules.",
            "Use order-ticket and order-review to create placeholder-only broker checklists without live prices or execution.",
            "Use schema-inventory and artifact-validate to inspect local schema coverage and validate example JSON artifacts.",
            "Use release-manifest to assemble artifact inventory, validation status, release notes, skill sync guidance, and post-release checks.",
            "Use docs-export to render one self-contained static HTML documentation page from local public artifacts.",
            "Run package-audit to confirm public sharing hygiene, schemas, examples, and zero dependencies.",
        ],
        "commands": [
            {
                "name": "pretrade-plan",
                "command": (
                    "python -m leveraged_etp_risk_lab pretrade-plan --product "
                    "examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv "
                    "--thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 "
                    "--stop-loss 0.15 --take-profit 0.20 --format markdown"
                ),
            },
            {
                "name": "stress-matrix",
                "command": (
                    "python -m leveraged_etp_risk_lab stress-matrix --product "
                    "examples/fixtures/leveraged_nasdaq_3x.json --stop-loss 0.15 --take-profit 0.20 "
                    "--format markdown"
                ),
            },
            {
                "name": "sensitivity-grid",
                "command": (
                    "python -m leveraged_etp_risk_lab sensitivity-grid --product "
                    "examples/fixtures/leveraged_nasdaq_3x.json --stop-loss none,0.15,0.25 "
                    "--take-profit none,0.20,0.35 --format markdown"
                ),
            },
            {
                "name": "watchlist-build",
                "command": (
                    "python -m leveraged_etp_risk_lab watchlist-build --thesis-impact "
                    "examples/outputs/thesis_impact.json --stress-matrix examples/outputs/stress_matrix.json "
                    "--format markdown"
                ),
            },
            {
                "name": "package-audit",
                "command": "python -m leveraged_etp_risk_lab package-audit --format markdown",
            },
            {
                "name": "recipe-run",
                "command": (
                    "python -m leveraged_etp_risk_lab recipe-run --recipe "
                    "examples/fixtures/recipe_thesis_review.json --format markdown"
                ),
            },
            {
                "name": "report-card",
                "command": (
                    "python -m leveraged_etp_risk_lab report-card --artifact examples/outputs/pretrade_plan.json "
                    "--artifact examples/outputs/position_size.json --artifact examples/outputs/stress_matrix.json "
                    "--artifact examples/outputs/factsheet_check.json --format markdown"
                ),
            },
            {
                "name": "memo-draft",
                "command": (
                    "python -m leveraged_etp_risk_lab memo-draft --recipe-run examples/outputs/recipe_run.json "
                    "--thesis-dashboard-data examples/outputs/thesis_dashboard_data.json "
                    "--report-card examples/outputs/report_card.json --factsheet-check examples/outputs/factsheet_check.json "
                    "--format markdown"
                ),
            },
            {
                "name": "memo-review",
                "command": (
                    "python -m leveraged_etp_risk_lab memo-review --memo examples/outputs/investment_memo.json "
                    "--report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json "
                    "--audit-trail examples/outputs/audit_trail.json --format markdown"
                ),
            },
            {
                "name": "cycle-init",
                "command": (
                    "python -m leveraged_etp_risk_lab cycle-init --memo examples/outputs/investment_memo.json "
                    "--watchlist examples/outputs/watchlist.json --report-card examples/outputs/report_card.json "
                    "--sensitivity-grid examples/outputs/sensitivity_grid.json --format markdown"
                ),
            },
            {
                "name": "cycle-update",
                "command": (
                    "python -m leveraged_etp_risk_lab cycle-update --cycle-state examples/outputs/cycle_state.json "
                    "--report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json "
                    "--audit-trail examples/outputs/audit_trail.json --format markdown"
                ),
            },
            {
                "name": "guardrail-policy",
                "command": "python -m leveraged_etp_risk_lab guardrail-policy --policy default --format markdown",
            },
            {
                "name": "guardrail-check",
                "command": (
                    "python -m leveraged_etp_risk_lab guardrail-check --policy examples/outputs/guardrail_policy.json "
                    "--portfolio-sensitivity examples/outputs/portfolio_sensitivity.json "
                    "--position-size examples/outputs/position_size.json "
                    "--investment-memo examples/outputs/investment_memo.json "
                    "--cycle-update examples/outputs/cycle_update.json --format markdown"
                ),
            },
            {
                "name": "order-ticket",
                "command": (
                    "python -m leveraged_etp_risk_lab order-ticket --guardrail-check examples/outputs/guardrail_check.json "
                    "--investment-memo examples/outputs/investment_memo.json "
                    "--position-size examples/outputs/position_size.json "
                    "--factsheet-check examples/outputs/factsheet_check.json "
                    "--thesis-dashboard-data examples/outputs/thesis_dashboard_data.json --format markdown"
                ),
            },
            {
                "name": "order-review",
                "command": (
                    "python -m leveraged_etp_risk_lab order-review --order-ticket examples/outputs/order_ticket.json "
                    "--guardrail-check examples/outputs/guardrail_check.json "
                    "--cycle-update examples/outputs/cycle_update.json "
                    "--audit-trail examples/outputs/audit_trail.json --format markdown"
                ),
            },
            {
                "name": "demo-story",
                "command": "python -m leveraged_etp_risk_lab demo-story --input-dir examples/outputs --format markdown",
            },
            {
                "name": "scenario-pack",
                "command": (
                    "python -m leveraged_etp_risk_lab scenario-pack --input-dir examples/outputs "
                    "--fixtures-dir examples/fixtures --output-dir examples/outputs --format markdown"
                ),
            },
            {
                "name": "schema-inventory",
                "command": "python -m leveraged_etp_risk_lab schema-inventory --format markdown",
            },
            {
                "name": "artifact-validate",
                "command": "python -m leveraged_etp_risk_lab artifact-validate --format markdown",
            },
            {
                "name": "release-manifest",
                "command": "python -m leveraged_etp_risk_lab release-manifest --input-dir examples/outputs --format markdown",
            },
            {
                "name": "docs-export",
                "command": "python -m leveraged_etp_risk_lab docs-export --input-dir examples/outputs --output examples/outputs/docs_export.html",
            },
        ],
        "key_outputs": [
            {
                "source": "pretrade_plan.json",
                "summary": (
                    f"{product['ticker']} modeled over {scenario['days']} days returns "
                    f"{scenario['etp_return_pct']}% with path decay {scenario['path_decay_vs_simple_multiple']}."
                ),
                "metrics": {
                    "ticker": product["ticker"],
                    "leverage": product["leverage"],
                    "etp_return_pct": scenario["etp_return_pct"],
                    "underlying_return_pct": scenario["underlying_return_pct"],
                    "path_decay_vs_simple_multiple": scenario["path_decay_vs_simple_multiple"],
                    "max_loss_budget": plan["budget"]["max_loss_budget"],
                },
            },
            {
                "source": "stress_matrix.json",
                "summary": (
                    f"{len(stress.get('rows', []))} regimes modeled; weakest return is "
                    f"{_row_label(worst_row)} at {_row_value(worst_row, 'return_pct')}%."
                ),
                "metrics": {
                    "regimes": len(stress.get("rows", [])),
                    "weakest_return_regime": _row_label(worst_row),
                    "weakest_return_pct": _row_value(worst_row, "return_pct"),
                    "largest_drawdown_regime": _row_label(highest_drawdown),
                    "largest_drawdown_pct": _row_value(highest_drawdown, "worst_drawdown_pct"),
                },
            },
            {
                "source": "sensitivity_grid.json",
                "summary": (
                    f"{sensitivity.get('summary', {}).get('combinations', 0)} grid combinations modeled; worst return is "
                    f"{sensitivity.get('summary', {}).get('worst_return_pct')}% in "
                    f"{sensitivity.get('summary', {}).get('worst_return_regime')}."
                ),
                "metrics": {
                    "combinations": sensitivity.get("summary", {}).get("combinations"),
                    "worst_return_pct": sensitivity.get("summary", {}).get("worst_return_pct"),
                    "worst_return_regime": sensitivity.get("summary", {}).get("worst_return_regime"),
                    "worst_path_decay_vs_simple_multiple": sensitivity.get("summary", {}).get(
                        "worst_path_decay_vs_simple_multiple"
                    ),
                    "max_stop_events": sensitivity.get("summary", {}).get("max_stop_events"),
                },
            },
            {
                "source": "watchlist.json",
                "summary": (
                    f"{watchlist.get('summary', {}).get('entries', 0)} watchlist entries, "
                    f"{len(critical_entries)} critical and {len(high_entries)} high severity."
                ),
                "metrics": {
                    "entries": watchlist.get("summary", {}).get("entries", 0),
                    "critical": len(critical_entries),
                    "high": len(high_entries),
                    "top_triggers": [entry["title"] for entry in (critical_entries + high_entries)[:3]],
                },
            },
            {
                "source": "package_audit.json",
                "summary": (
                    f"Package audit ready={audit_summary.get('ready')} with "
                    f"{audit_summary.get('passed', 0)} passed and {audit_summary.get('failed', 0)} failed checks."
                ),
                "metrics": {
                    "ready": audit_summary.get("ready"),
                    "checks": audit_summary.get("checks"),
                    "passed": audit_summary.get("passed"),
                    "failed": audit_summary.get("failed"),
                    "dependencies": audit.get("package", {}).get("dependencies", []),
                },
            },
            {
                "source": "report_card.json",
                "summary": (
                    f"Report card decision_ready={card.get('summary', {}).get('decision_ready')} with "
                    f"{card.get('summary', {}).get('strengths', 0)} strengths, "
                    f"{card.get('summary', {}).get('unresolved_checks', 0)} unresolved checks, and "
                    f"{card.get('summary', {}).get('warnings', 0)} warnings."
                ),
                "metrics": {
                    "decision_ready": card.get("summary", {}).get("decision_ready"),
                    "strengths": card.get("summary", {}).get("strengths"),
                    "unresolved_checks": card.get("summary", {}).get("unresolved_checks"),
                    "warnings": card.get("summary", {}).get("warnings"),
                    "next_commands": len(card.get("next_commands", [])),
                },
            },
            {
                "source": "investment_memo.json",
                "summary": (
                    f"Memo packet has {len(memo.get('open_checks', []))} open checks and "
                    f"{len(memo.get('invalidation_triggers', []))} invalidation triggers."
                ),
                "metrics": {
                    "open_checks": len(memo.get("open_checks", [])),
                    "invalidation_triggers": len(memo.get("invalidation_triggers", [])),
                    "recommended_notional": memo.get("risk_budget", {}).get("recommended_notional"),
                    "decision_ready": memo.get("thesis", {}).get("decision_ready"),
                },
            },
            {
                "source": "investment_memo_review.json",
                "summary": (
                    f"Memo review found {memo_review.get('summary', {}).get('changed_risks', 0)} changed risks and "
                    f"{memo_review.get('summary', {}).get('review', 0)} review checklist items."
                ),
                "metrics": dict(memo_review.get("summary", {})),
            },
            {
                "source": "cycle_state.json",
                "summary": (
                    f"Cycle state {cycle_state.get('state_id')} tracks "
                    f"{cycle_state.get('summary', {}).get('watch_items', 0)} watch items and "
                    f"{cycle_state.get('summary', {}).get('open_checks', 0)} open checks."
                ),
                "metrics": dict(cycle_state.get("summary", {})),
            },
            {
                "source": "cycle_update.json",
                "summary": (
                    f"Cycle update has {cycle_update.get('summary', {}).get('hash_drift', 0)} hash drift item(s), "
                    f"{cycle_update.get('summary', {}).get('changed_watch_items', 0)} changed watch item(s), and "
                    f"{cycle_update.get('summary', {}).get('status_transitions', 0)} status transition(s)."
                ),
                "metrics": dict(cycle_update.get("summary", {})),
            },
            {
                "source": "guardrail_check.json",
                "summary": (
                    f"Guardrail check result is {guardrail.get('summary', {}).get('result')} with "
                    f"{guardrail.get('summary', {}).get('review', 0)} review and "
                    f"{guardrail.get('summary', {}).get('fail', 0)} fail rule(s)."
                ),
                "metrics": dict(guardrail.get("summary", {})),
            },
            {
                "source": "order_ticket.json",
                "summary": (
                    f"Order ticket status is {ticket.get('summary', {}).get('status')} with "
                    f"{ticket.get('summary', {}).get('do_not_trade_conditions', 0)} do-not-trade condition(s) "
                    "and no broker execution."
                ),
                "metrics": dict(ticket.get("summary", {})),
            },
            {
                "source": "order_review.json",
                "summary": (
                    f"Order review status is {order_review.get('summary', {}).get('status')} with "
                    f"{order_review.get('summary', {}).get('blocked', 0)} blocked and "
                    f"{order_review.get('summary', {}).get('review', 0)} review item(s)."
                ),
                "metrics": dict(order_review.get("summary", {})),
            },
        ],
        "safety_caveats": _unique_text(
            [
                plan["not_investment_advice"],
                "The demo uses deterministic fixtures, not forecasts or live market data.",
                "Stop-loss and take-profit bands are planning levels, not guaranteed execution prices.",
                "Position sizing and watchlist severity are review aids, not recommendations.",
                "Order ticket and review outputs are educational checklists, not broker orders.",
                "The package intentionally avoids workflow files, secrets, live prices, and private context.",
            ]
            + [str(item) for item in stress.get("warnings", [])[:2]]
            + [str(item) for item in sensitivity.get("warnings", [])[:1]]
        ),
        "next_extension_ideas": [
            "Add more generic regime paths for rate-shock, overnight-gap, and prolonged-chop cases.",
            "Add optional user-supplied execution-price columns while keeping the core package dependency-free.",
            "Add a static public gallery page that links the JSON, Markdown, dashboard, and demo-story artifacts.",
            "Extend package-audit with schema example coverage checks for each public output type.",
            "Attach release-manifest JSON and Markdown to release notes for reproducible post-release verification.",
        ],
    }
    return {
        "schema_version": DEMO_STORY_SCHEMA_VERSION,
        "document_type": "demo_story",
        "not_investment_advice": plan["not_investment_advice"],
        "inputs": {name: _display_path(path) for name, path in artifacts.items()},
        "sections": sections,
        "provenance": {"command": "demo-story", "input_dir": _display_path(input_dir)},
    }


def demo_story_markdown(data: Dict[str, Any]) -> str:
    sections = data["sections"]
    lines = [
        "# Public Demo Story",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Problem",
        "",
        sections["problem"],
        "",
        "## Workflow",
        "",
    ]
    lines.extend(f"- {item}" for item in sections["workflow"])
    lines.extend(["", "## Commands", ""])
    for item in sections["commands"]:
        lines.extend([f"### {item['name']}", "", "```bash", item["command"], "```", ""])
    lines.extend(["## Key Outputs", ""])
    for item in sections["key_outputs"]:
        lines.append(f"- **{item['source']}:** {item['summary']}")
    lines.extend(["", "## Safety Caveats", ""])
    lines.extend(f"- {item}" for item in sections["safety_caveats"])
    lines.extend(["", "## Next Extension Ideas", ""])
    lines.extend(f"- {item}" for item in sections["next_extension_ideas"])
    lines.extend(["", "## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def checklist_items(profile: str) -> List[str]:
    base = [
        "Confirm the product uses daily reset leverage and identify the stated leverage factor.",
        "Compare the planned holding period with the product objective and risk disclosures.",
        "Run at least one trending path and one choppy path before sizing the trade.",
        "Record stop-loss and take-profit levels before entry.",
        "Review borrowing, financing, and management-fee drag assumptions.",
        "Check whether the underlying has event risk, earnings, regulatory decisions, or macro releases.",
        "Document why the scenario does not rely on a simple leverage multiple over several days.",
    ]
    if profile == "active-trader":
        base.append("Confirm intraday liquidity, spreads, and exit rules for fast markets.")
    elif profile == "risk-review":
        base.append("Record maximum tolerable loss, concentration, and portfolio correlation.")
    return base


def version_report(version: str) -> str:
    return to_json(
        {
            "name": "leveraged-etp-risk-lab",
            "version": version,
            "python": ">=3.9",
            "dependencies": [],
            "commands": [
                "explain-term",
                "glossary-list",
                "simulate",
                "generate-scenario",
                "exposure-report",
                "pretrade-plan",
                "position-size",
                "stress-matrix",
                "sensitivity-grid",
                "portfolio-sensitivity",
                "compare-runs",
                "run-ledger",
                "thesis-impact",
                "watchlist-build",
                "factsheet-check",
                "risk-profile",
                "recipe-run",
                "report-card",
                "thesis-dashboard-data",
                "audit-trail",
                "memo-draft",
                "memo-review",
                "cycle-init",
                "cycle-update",
                "guardrail-policy",
                "guardrail-check",
                "order-ticket",
                "order-review",
                "static-dashboard",
                "template-list",
                "template-export",
                "regime-list",
                "regime-export",
                "checklist",
                "demo-bundle",
                "demo-story",
                "gallery-index",
                "asset-hub",
                "scenario-pack",
                "scenario-pack-reviewer-receipt",
                "package-audit",
                "product-snapshot",
                "schema-inventory",
                "artifact-validate",
                "release-manifest",
                "docs-export",
                "selfcheck",
                "version-report",
            ],
        }
    )


def dashboard_html(data: Dict[str, Any], title: str, provenance: Dict[str, Any]) -> str:
    summary = data.get("summary", {})
    portfolio = data.get("portfolio", {"name": title, "base_currency": "USD"})
    positions = data.get("positions", [])
    warnings = data.get("warnings", [])
    simulations = data.get("simulations", [])
    cards = [
        ("Starting Value", summary.get("starting_value", "n/a")),
        ("Ending Value", summary.get("ending_value", "n/a")),
        ("Return", _suffix(summary.get("return_pct"), "%")),
        ("Weighted Exposure", _suffix(summary.get("weighted_exposure"), "x")),
        ("Worst Drawdown", _suffix(summary.get("worst_drawdown_pct"), "%")),
    ]
    if not positions:
        for simulation in simulations:
            product = simulation.get("product", {})
            scenario = simulation.get("summary", {})
            positions.append(
                {
                    "id": product.get("ticker", "simulation"),
                    "ticker": product.get("ticker", "n/a"),
                    "product": product.get("name", "Simulation"),
                    "notional": "n/a",
                    "leverage": product.get("leverage", "n/a"),
                    "ending_value": scenario.get("ending_etp_nav", "n/a"),
                    "return_pct": scenario.get("etp_return_pct", "n/a"),
                    "stop_loss_pct": simulation.get("inputs", {}).get("stop_loss_pct"),
                    "take_profit_pct": simulation.get("inputs", {}).get("take_profit_pct"),
                }
            )
            warnings.extend(simulation.get("warnings", []))
    warning_items = _unique_text([str(item) for item in warnings])
    rows = [
        [
            position.get("id", ""),
            position.get("ticker", ""),
            position.get("product", ""),
            position.get("notional", ""),
            _suffix(position.get("leverage"), "x"),
            position.get("ending_value", ""),
            _suffix(position.get("return_pct"), "%"),
            _display_pct(position.get("stop_loss_pct")),
            _display_pct(position.get("take_profit_pct")),
        ]
        for position in positions
    ]
    stop_events = data.get("stop_events", [])
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{_e(title)}</title>",
            "<style>",
            "body{margin:0;font-family:Arial,Helvetica,sans-serif;color:#182026;background:#f6f7f4;line-height:1.45}",
            "header{background:#15332f;color:#fff;padding:28px 32px}",
            "main{max-width:1120px;margin:0 auto;padding:28px 20px 44px}",
            "h1,h2{margin:0 0 12px} h1{font-size:30px} h2{font-size:20px;margin-top:28px}",
            ".meta{color:#d7e7df}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}",
            ".card{background:#fff;border:1px solid #d7ddd6;border-radius:8px;padding:14px}",
            ".label{font-size:12px;color:#5d6a66;text-transform:uppercase}.value{font-size:23px;font-weight:700;margin-top:6px}",
            "table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #d7ddd6;border-radius:8px;overflow:hidden}",
            "th,td{text-align:left;padding:10px;border-bottom:1px solid #e6eae5;font-size:14px}th{background:#e8eee8}",
            ".warn{background:#fff4d6;border-left:4px solid #b57900;padding:10px 12px;margin:8px 0}",
            ".provenance{background:#fff;border:1px solid #d7ddd6;border-radius:8px;padding:14px}",
            "</style>",
            "</head>",
            "<body>",
            "<header>",
            f"<h1>{_e(title)}</h1>",
            f"<div class=\"meta\">{_e(portfolio.get('name', title))} · {_e(portfolio.get('base_currency', 'USD'))} · No JavaScript</div>",
            "</header>",
            "<main>",
            "<section class=\"cards\">",
            "".join(f"<div class=\"card\"><div class=\"label\">{_e(label)}</div><div class=\"value\">{_e(value)}</div></div>" for label, value in cards),
            "</section>",
            "<h2>Positions</h2>",
            _html_table(["ID", "Ticker", "Product", "Notional", "Leverage", "Ending Value", "Return", "Stop", "Take"], rows),
            "<h2>Band Events</h2>",
            _event_list(stop_events),
            "<h2>Warnings</h2>",
            "".join(f"<div class=\"warn\">{_e(item)}</div>" for item in warning_items) or "<p>None.</p>",
            "<h2>Command Provenance</h2>",
            "<div class=\"provenance\">",
            "".join(f"<p><strong>{_e(key)}:</strong> {_e(provenance[key])}</p>" for key in sorted(provenance)),
            "</div>",
            "</main>",
            "</body>",
            "</html>",
            "",
        ]
    )


def _table(rows: Iterable[Dict[str, Any]]) -> str:
    headers = [
        "day",
        "label",
        "underlying_return_pct",
        "underlying_index",
        "daily_levered_return_pct",
        "etp_nav",
        "simple_multiple_nav",
        "path_decay",
    ]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[key]) for key in headers) + " |")
    return "\n".join(lines)


def load_demo_outputs(input_dir: Path) -> Dict[str, Any]:
    simulations: List[Dict[str, Any]] = []
    portfolio = None
    for path in sorted(input_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if "portfolio" in data and "positions" in data:
            portfolio = data
        elif "product" in data and "summary" in data:
            simulations.append(data)
    if portfolio is not None:
        portfolio = dict(portfolio)
        portfolio["simulations"] = simulations
        return portfolio
    return {
        "schema_version": "0.3",
        "portfolio": {"name": "Demo Simulation Outputs", "base_currency": "USD"},
        "summary": {
            "starting_value": "n/a",
            "ending_value": "n/a",
            "return_pct": "n/a",
            "weighted_exposure": "n/a",
            "worst_drawdown_pct": "n/a",
        },
        "positions": [],
        "stop_events": [],
        "warnings": [],
        "simulations": simulations,
    }


def _load_required_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a JSON object")
    return data


def _require_document_type(data: Dict[str, Any], expected: str, path: Path) -> None:
    if data.get("document_type") != expected:
        raise ValueError(f"{path} must be a {expected} JSON output")


def _lowest_row(rows: List[Dict[str, Any]], key: str) -> Dict[str, Any]:
    numeric = [row for row in rows if isinstance(row.get(key), (int, float))]
    if not numeric:
        return {}
    return min(numeric, key=lambda row: row[key])


def _row_label(row: Dict[str, Any]) -> str:
    return str(row.get("regime") or row.get("name") or "n/a")


def _row_value(row: Dict[str, Any], key: str) -> Any:
    return row.get(key) if row else None


def _entries_by_severity(data: Dict[str, Any], severity: str) -> List[Dict[str, Any]]:
    return [entry for entry in data.get("entries", []) if entry.get("severity") == severity]


def _display_path(path: Path) -> str:
    text = path.as_posix()
    if text.startswith("/"):
        return path.name
    return text


def default_pretrade_assumptions() -> List[str]:
    return [
        "Scenario path is deterministic fixture data, not a forecast.",
        "Modeled NAV starts at 100 and applies daily reset leverage once per scenario row.",
        "Fees are approximated as a constant daily deduction from leveraged daily return.",
        "Risk bands are evaluated on modeled end-of-day NAV values.",
        "The maximum loss budget is supplied by the user and is not a sizing recommendation.",
    ]


def _display_pct(value: Any) -> str:
    if value is None:
        return "not set"
    return f"{value}%"


def _display_value(value: Any) -> str:
    if value is None:
        return "n/a"
    return str(value)


def _suffix(value: Any, suffix: str) -> str:
    if value is None:
        return "n/a"
    if value == "n/a":
        return "n/a"
    return f"{value}{suffix}"


def _e(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _html_table(headers: List[str], rows: List[List[Any]]) -> str:
    head = "".join(f"<th>{_e(header)}</th>" for header in headers)
    if not rows:
        body = f"<tr><td colspan=\"{len(headers)}\">No positions found.</td></tr>"
    else:
        body = "".join("<tr>" + "".join(f"<td>{_e(value)}</td>" for value in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def _event_list(events: List[Dict[str, Any]]) -> str:
    if not events:
        return "<p>None.</p>"
    items = []
    for event in events:
        position = event.get("position_id", event.get("ticker", "position"))
        items.append(
            f"<div class=\"warn\">{_e(position)} day {_e(event.get('day', ''))}: "
            f"{_e(event.get('event', 'band_event'))} at NAV {_e(event.get('nav', ''))}</div>"
        )
    return "".join(items)


def _unique_text(items: List[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _table_with_headers(rows: Iterable[Dict[str, Any]], headers: List[str]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[key]) for key in headers) + " |")
    return "\n".join(lines)
