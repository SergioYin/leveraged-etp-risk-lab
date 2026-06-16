from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .io import load_path, load_product, write_text
from .render import to_json


SCENARIO_PACK_SCHEMA_VERSION = "0.30"
SCENARIO_CASE_SCHEMA_VERSION = "0.30"
SCENARIO_PACK_REVIEW_RECEIPT_SCHEMA_VERSION = "0.30"


def scenario_pack(input_dir: str, fixtures_dir: str) -> Dict[str, Any]:
    input_root = Path(input_dir)
    fixture_root = Path(fixtures_dir)
    reports = {
        "leveraged_nasdaq_3x": _load_json(input_root / "leveraged_nasdaq_3x.json"),
        "single_stock_2x": _load_json(input_root / "single_stock_2x.json"),
        "pretrade_plan": _load_json(input_root / "pretrade_plan.json"),
        "position_size": _load_json(input_root / "position_size.json"),
        "stress_matrix": _load_json(input_root / "stress_matrix.json"),
        "portfolio_sensitivity": _load_json(input_root / "portfolio_sensitivity.json"),
        "guardrail_check": _load_json(input_root / "guardrail_check.json"),
        "order_review": _load_json(input_root / "order_review.json"),
        "compare_runs": _load_json(input_root / "compare_runs.json"),
    }
    fixtures = _fixture_summaries(fixture_root)
    source_artifacts = _source_artifacts(
        [
            input_root / "leveraged_nasdaq_3x.json",
            input_root / "single_stock_2x.json",
            input_root / "pretrade_plan.json",
            input_root / "position_size.json",
            input_root / "stress_matrix.json",
            input_root / "portfolio_sensitivity.json",
            input_root / "guardrail_check.json",
            input_root / "order_review.json",
            input_root / "compare_runs.json",
            fixture_root / "leveraged_nasdaq_3x.json",
            fixture_root / "single_stock_2x.json",
            fixture_root / "nasdaq_chop_path.csv",
            fixture_root / "single_stock_gap_path.csv",
            fixture_root / "portfolio_manifest.json",
            fixture_root / "thesis_note.md",
        ]
    )
    cases = [
        _path_decay_case(reports, fixtures, source_artifacts),
        _drawdown_case(reports, fixtures, source_artifacts),
        _guardrail_case(reports, fixtures, source_artifacts),
    ]
    return {
        "schema_version": SCENARIO_PACK_SCHEMA_VERSION,
        "document_type": "scenario_pack",
        "not_investment_advice": _not_advice(),
        "pack_id": "v0.30-new-user-scenario-pack",
        "title": "New User Scenario Pack",
        "audience": "New users comparing daily-reset path decay, drawdown risk, and pretrade guardrails.",
        "summary": {
            "cases": len(cases),
            "source_artifacts": len(source_artifacts),
            "focus_areas": ["daily_reset_path_decay", "drawdown_risk", "pretrade_guardrails"],
            "live_market_data": False,
            "broker_execution": False,
        },
        "cases": [_case_index(case) for case in cases],
        "integration_notes": _integration_notes(),
        "cold_user_evidence": _cold_user_evidence(None),
        "source_artifacts": source_artifacts,
        "warnings": _unique(
            [
                "Scenario packs are deterministic educational artifacts and do not recommend trades.",
                "Daily reset, gap risk, liquidity, borrow, tax, and execution effects can differ from these local examples.",
                "Pretrade guardrails are review gates, not suitability determinations or broker instructions.",
            ]
        ),
        "provenance": {
            "command": "scenario-pack",
            "input_dir": str(input_root),
            "fixtures_dir": str(fixture_root),
            "live_market_data": False,
            "shell_out": False,
            "private_context": False,
            "broker_execution": False,
            "workflow_files_read": False,
        },
        "_cases": cases,
    }


def write_scenario_pack(input_dir: str, fixtures_dir: str, output_dir: str) -> Dict[str, Any]:
    packet = scenario_pack(input_dir, fixtures_dir)
    root = Path(output_dir)
    cases = list(packet.pop("_cases"))
    write_text(root / "scenario_pack.json", to_json(packet))
    write_text(root / "scenario_pack.md", scenario_pack_markdown(packet))
    for case in cases:
        case_id = str(case["case_id"])
        write_text(root / f"{case_id}.json", to_json(case))
        write_text(root / f"{case_id}.md", scenario_case_markdown(case))
    receipt = scenario_pack_review_receipt(input_dir, fixtures_dir, output_dir)
    write_text(root / "scenario_pack_reviewer_receipt.json", to_json(receipt))
    write_text(root / "scenario_pack_reviewer_receipt.md", scenario_pack_review_receipt_markdown(receipt))
    packet["_cases"] = cases
    return packet


def write_scenario_pack_review_receipt(input_dir: str, fixtures_dir: str, artifact_dir: str, output_dir: str) -> Dict[str, Any]:
    receipt = scenario_pack_review_receipt(input_dir, fixtures_dir, artifact_dir)
    root = Path(output_dir)
    write_text(root / "scenario_pack_reviewer_receipt.json", to_json(receipt))
    write_text(root / "scenario_pack_reviewer_receipt.md", scenario_pack_review_receipt_markdown(receipt))
    return receipt


def scenario_pack_markdown(data: Dict[str, Any]) -> str:
    lines = [
        f"# {data['title']}",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Summary",
        "",
        f"- Cases: {data['summary']['cases']}",
        f"- Source artifacts: {data['summary']['source_artifacts']}",
        f"- Live market data: {data['summary']['live_market_data']}",
        f"- Broker execution: {data['summary']['broker_execution']}",
        "",
        "## Case Studies",
        "",
        "| Case | Focus | Primary metric | Output |",
        "| --- | --- | --- | --- |",
    ]
    for case in data["cases"]:
        lines.append(f"| {case['title']} | {case['focus_area']} | {case['primary_metric']} | {case['markdown']} |")
    lines.extend(["", "## Integration Notes", ""])
    for item in data["integration_notes"]:
        lines.append(f"### {item['target_system']}")
        lines.append("")
        lines.append(f"- Complement: {item['complement']}")
        lines.append(f"- Handoff artifacts: {', '.join(item['handoff_artifacts'])}")
        lines.append(f"- Dependency boundary: {item['dependency_boundary']}")
        lines.append(f"- Public context: {item['public_context']}")
        lines.append("")
    lines.extend(_evidence_markdown(data["cold_user_evidence"]))
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in data["warnings"])
    lines.extend(["", "## Source Artifacts", ""])
    for item in data["source_artifacts"]:
        lines.append(f"- {item['path']} ({item['kind']}, sha256={item['sha256'][:12]})")
    return "\n".join(lines) + "\n"


def scenario_case_markdown(data: Dict[str, Any]) -> str:
    lines = [
        f"# {data['title']}",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## New User Question",
        "",
        data["cold_user_question"],
        "",
        "## Answer",
        "",
        data["plain_english_answer"],
        "",
        "## Key Metrics",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]
    for key, value in data["metrics"].items():
        lines.append(f"| {key} | {_display(value)} |")
    lines.extend(["", "## Takeaways", ""])
    lines.extend(f"- {item}" for item in data["takeaways"])
    lines.extend(["", "## Guardrails To Check", ""])
    lines.extend(f"- {item}" for item in data["guardrails"])
    lines.extend(_evidence_markdown(data["cold_user_evidence"]))
    lines.extend(["", "## Source Artifacts", ""])
    lines.extend(f"- {item['path']} ({item['kind']})" for item in data["source_artifacts"])
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in data["warnings"])
    return "\n".join(lines) + "\n"


def scenario_pack_review_receipt(input_dir: str, fixtures_dir: str, artifact_dir: str) -> Dict[str, Any]:
    input_root = Path(input_dir)
    fixture_root = Path(fixtures_dir)
    artifact_root = Path(artifact_dir)
    fixture_inputs = _source_artifacts(
        [
            fixture_root / "leveraged_nasdaq_3x.json",
            fixture_root / "single_stock_2x.json",
            fixture_root / "nasdaq_chop_path.csv",
            fixture_root / "single_stock_gap_path.csv",
            fixture_root / "portfolio_manifest.json",
            fixture_root / "thesis_note.md",
        ]
    )
    source_inputs = _source_artifacts(
        [
            input_root / "leveraged_nasdaq_3x.json",
            input_root / "single_stock_2x.json",
            input_root / "pretrade_plan.json",
            input_root / "position_size.json",
            input_root / "stress_matrix.json",
            input_root / "portfolio_sensitivity.json",
            input_root / "guardrail_check.json",
            input_root / "order_review.json",
            input_root / "compare_runs.json",
        ]
    )
    generated_artifacts = _source_artifacts(
        [
            artifact_root / "scenario_pack.json",
            artifact_root / "scenario_pack.md",
            artifact_root / "daily_reset_path_decay.json",
            artifact_root / "daily_reset_path_decay.md",
            artifact_root / "drawdown_risk.json",
            artifact_root / "drawdown_risk.md",
            artifact_root / "pretrade_guardrails.json",
            artifact_root / "pretrade_guardrails.md",
        ]
    )
    return {
        "schema_version": SCENARIO_PACK_REVIEW_RECEIPT_SCHEMA_VERSION,
        "document_type": "scenario_pack_reviewer_receipt",
        "not_investment_advice": _not_advice(),
        "receipt_id": "v0.30-scenario-pack-reviewer-receipt",
        "title": "Scenario Pack Reviewer Receipt",
        "summary": {
            "fixture_inputs": len(fixture_inputs),
            "source_inputs": len(source_inputs),
            "generated_artifacts": len(generated_artifacts),
            "hash_algorithm": "sha256",
            "live_market_data": False,
            "broker_execution": False,
            "trading_enabled": False,
            "personalized_recommendations": False,
        },
        "fixture_inputs": fixture_inputs,
        "source_inputs": source_inputs,
        "generated_artifacts": generated_artifacts,
        "reviewer_checks": [
            "Confirm every fixture path is under examples/fixtures or the supplied fixtures directory.",
            "Confirm every generated artifact path is under examples/outputs or the supplied artifact directory.",
            "Compare SHA-256 hashes after regeneration before reviewing the scenario-pack narrative.",
            "Verify safety boundaries remain false for live market data, broker execution, trading, and personalized recommendations.",
        ],
        "regeneration": {
            "demo_bundle_command": "python -m leveraged_etp_risk_lab demo-bundle --output-dir examples/outputs",
            "scenario_pack_command": "python -m leveraged_etp_risk_lab scenario-pack --input-dir examples/outputs --fixtures-dir examples/fixtures --output-dir examples/outputs --format markdown",
            "receipt_command": "python -m leveraged_etp_risk_lab scenario-pack-reviewer-receipt --input-dir examples/outputs --fixtures-dir examples/fixtures --artifact-dir examples/outputs --output-dir examples/outputs --format markdown",
            "validation_command": "python -m leveraged_etp_risk_lab artifact-validate examples/outputs/scenario_pack_reviewer_receipt.json examples/outputs/scenario_pack.json examples/outputs/daily_reset_path_decay.json examples/outputs/drawdown_risk.json examples/outputs/pretrade_guardrails.json --format markdown",
        },
        "safety_boundaries": [
            "No live market data is fetched or required.",
            "No broker, API, account, order, routing, staging, preview, or execution capability is used.",
            "No trading instruction, no personalized recommendation, no suitability determination, and no investment advice is produced.",
            "Receipt hashes cover deterministic local fixtures and generated artifacts only.",
        ],
        "provenance": {
            "command": "scenario-pack-reviewer-receipt",
            "input_dir": str(input_root),
            "fixtures_dir": str(fixture_root),
            "artifact_dir": str(artifact_root),
            "live_market_data": False,
            "shell_out": False,
            "private_context": False,
            "broker_execution": False,
            "workflow_files_read": False,
            "trading_enabled": False,
            "personalized_recommendations": False,
        },
    }


def scenario_pack_review_receipt_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        f"# {data['title']}",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Summary",
        "",
        f"- Fixture inputs: {summary['fixture_inputs']}",
        f"- Source inputs: {summary['source_inputs']}",
        f"- Generated artifacts: {summary['generated_artifacts']}",
        f"- Hash algorithm: {summary['hash_algorithm']}",
        f"- Live market data: {summary['live_market_data']}",
        f"- Broker execution: {summary['broker_execution']}",
        f"- Trading enabled: {summary['trading_enabled']}",
        f"- Personalized recommendations: {summary['personalized_recommendations']}",
        "",
        "## Regeneration",
        "",
    ]
    for key in ["demo_bundle_command", "scenario_pack_command", "receipt_command", "validation_command"]:
        lines.append(f"- {key}: `{data['regeneration'][key]}`")
    lines.extend(["", "## Reviewer Checks", ""])
    lines.extend(f"- {item}" for item in data["reviewer_checks"])
    lines.extend(["", "## Fixture Inputs", "", "| Path | Kind | Bytes | SHA-256 |", "| --- | --- | ---: | --- |"])
    lines.extend(_artifact_rows(data["fixture_inputs"]))
    lines.extend(["", "## Source Inputs", "", "| Path | Kind | Bytes | SHA-256 |", "| --- | --- | ---: | --- |"])
    lines.extend(_artifact_rows(data["source_inputs"]))
    lines.extend(["", "## Generated Artifacts", "", "| Path | Kind | Bytes | SHA-256 |", "| --- | --- | ---: | --- |"])
    lines.extend(_artifact_rows(data["generated_artifacts"]))
    lines.extend(["", "## Safety Boundaries", ""])
    lines.extend(f"- {item}" for item in data["safety_boundaries"])
    lines.extend(["", "## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def _path_decay_case(reports: Dict[str, Any], fixtures: Dict[str, Any], sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    nasdaq = reports["leveraged_nasdaq_3x"]
    single = reports["single_stock_2x"]
    compare = reports["compare_runs"]
    nasdaq_summary = nasdaq["summary"]
    single_summary = single["summary"]
    delta = compare.get("deltas", {})
    metrics = {
        "nasdaq_underlying_return_pct": nasdaq_summary["underlying_return_pct"],
        "nasdaq_etp_return_pct": nasdaq_summary["etp_return_pct"],
        "nasdaq_simple_multiple_return_pct": nasdaq_summary["simple_multiple_return_pct"],
        "nasdaq_path_decay_nav_points": nasdaq_summary["path_decay_vs_simple_multiple"],
        "single_stock_path_decay_nav_points": single_summary["path_decay_vs_simple_multiple"],
        "case_delta_path_decay_nav_points": delta.get("path_decay_vs_simple_multiple"),
        "nasdaq_path_days": nasdaq["inputs"]["days"],
        "nasdaq_fixture_days": fixtures["nasdaq_chop_path"]["days"],
    }
    return _case(
        "daily_reset_path_decay",
        "Daily Reset Path Decay",
        "daily_reset_path_decay",
        "If the underlying ends close to flat after a choppy path, why can a 3x daily-reset product still lag a simple 3x multiple?",
        (
            "The example decomposes the modeled ending NAV against the simple multiple. "
            "The path-decay field shows the multi-day compounding gap created by alternating daily returns and fee drag."
        ),
        metrics,
        [
            "Compare ending ETP return with the simple multiple before treating leverage as a linear multi-day exposure.",
            "A choppy path can make the daily reset product worse than the simple multiple even when the underlying move looks modest.",
            "The gap is expressed in NAV points so a new user can inspect it without live prices.",
        ],
        [
            "Limit holding period assumptions when daily swings dominate the thesis.",
            "Run compare-runs before replacing one leveraged product or path with another.",
            "Record path-decay tolerance in the pretrade plan before sizing the position.",
        ],
        ["leveraged_nasdaq_3x.json", "single_stock_2x.json", "compare_runs.json", "nasdaq_chop_path.csv"],
        sources,
    )


def _drawdown_case(reports: Dict[str, Any], fixtures: Dict[str, Any], sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    stress = reports["stress_matrix"]
    portfolio = reports["portfolio_sensitivity"]
    worst_return = _min_row(stress["rows"], "return_pct")
    worst_drawdown = _min_row(stress["rows"], "worst_drawdown_pct")
    summary = portfolio["summary"]
    metrics = {
        "worst_regime": worst_return.get("regime"),
        "worst_regime_return_pct": worst_return.get("return_pct"),
        "worst_regime_drawdown_pct": worst_drawdown.get("worst_drawdown_pct"),
        "aggregate_worst_case_modeled_loss": summary.get("aggregate_worst_case_modeled_loss"),
        "aggregate_worst_case_loss_pct": summary.get("aggregate_worst_case_loss_pct"),
        "aggregate_worst_case_weighted_exposure": summary.get("aggregate_worst_case_weighted_exposure"),
        "portfolio_positions": summary.get("positions"),
        "manifest_positions": fixtures["portfolio_manifest"]["positions"],
    }
    return _case(
        "drawdown_risk",
        "Drawdown Risk Under Regime Stress",
        "drawdown_risk",
        "Which deterministic regime hurts most, and what does that imply for a portfolio-level loss budget?",
        (
            "The stress matrix ranks built-in regimes by modeled return and drawdown, while portfolio sensitivity translates "
            "the weakest rows into aggregate modeled loss and weighted exposure."
        ),
        metrics,
        [
            "Worst return and worst drawdown can point to the same regime, but they are separate checks.",
            "Portfolio sensitivity converts product-level stress into a budget-sized loss number.",
            "Weighted exposure helps separate notional size from effective leveraged exposure.",
        ],
        [
            "Review aggregate modeled loss before adding exposure to an existing portfolio.",
            "Treat stop events as review triggers because gap risk and execution quality are not modeled.",
            "Use regime stress alongside, not instead of, thesis invalidation checks.",
        ],
        ["stress_matrix.json", "portfolio_sensitivity.json", "portfolio_manifest.json"],
        sources,
    )


def _guardrail_case(reports: Dict[str, Any], fixtures: Dict[str, Any], sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    plan = reports["pretrade_plan"]
    size = reports["position_size"]
    guardrail = reports["guardrail_check"]
    review = reports["order_review"]
    metrics = {
        "pretrade_loss_budget": plan["budget"]["max_loss_budget"],
        "scenario_etp_return_pct": plan["scenario"]["etp_return_pct"],
        "stop_loss_pct": plan["risk_bands"]["stop_loss_pct"],
        "recommended_notional": size["recommendation"]["recommended_notional"],
        "modeled_loss_at_stop": size["recommendation"]["modeled_loss_at_stop"],
        "exposure_multiple": size["recommendation"]["exposure_multiple"],
        "guardrail_status": guardrail["summary"].get("status", guardrail["summary"].get("result")),
        "order_review_status": review["summary"]["status"],
        "thesis_lines": fixtures["thesis_note"]["lines"],
    }
    return _case(
        "pretrade_guardrails",
        "Pretrade Guardrails Before An Order",
        "pretrade_guardrails",
        "How does a new user connect a thesis, loss budget, position size, and order review without sending a trade?",
        (
            "The pretrade artifacts keep the workflow in review mode. The size plan converts a loss budget into placeholder "
            "notional, then guardrail and order-review artifacts report whether required checks are ready."
        ),
        metrics,
        [
            "Sizing is derived from the modeled loss budget and stop assumption, not from a live recommendation.",
            "Guardrail status is an explicit gate for exposure, loss-budget, holding-period, and review conditions.",
            "Order review remains placeholder-only and records that no broker execution is modeled.",
        ],
        [
            "Resolve guardrail review items before treating an order ticket as complete.",
            "Convert notional to shares outside the model with the intended execution price.",
            "Keep factsheet, thesis, cycle, and audit artifacts attached to the pretrade record.",
        ],
        ["pretrade_plan.json", "position_size.json", "guardrail_check.json", "order_review.json", "thesis_note.md"],
        sources,
    )


def _case(
    case_id: str,
    title: str,
    focus_area: str,
    question: str,
    answer: str,
    metrics: Dict[str, Any],
    takeaways: List[str],
    guardrails: List[str],
    source_names: List[str],
    sources: List[Dict[str, Any]],
) -> Dict[str, Any]:
    selected_sources = [item for item in sources if Path(item["path"]).name in set(source_names)]
    return {
        "schema_version": SCENARIO_CASE_SCHEMA_VERSION,
        "document_type": "scenario_case_study",
        "not_investment_advice": _not_advice(),
        "case_id": case_id,
        "title": title,
        "focus_area": focus_area,
        "cold_user_question": question,
        "plain_english_answer": answer,
        "metrics": metrics,
        "takeaways": takeaways,
        "guardrails": guardrails,
        "cold_user_evidence": _cold_user_evidence(case_id),
        "source_artifacts": selected_sources,
        "warnings": _unique(
            [
                "This case study uses deterministic local examples only.",
                "It does not model live prices, spreads, liquidity, taxes, suitability, or broker execution.",
            ]
        ),
        "provenance": {
            "command": "scenario-pack",
            "case_id": case_id,
            "live_market_data": False,
            "shell_out": False,
            "private_context": False,
            "broker_execution": False,
            "workflow_files_read": False,
        },
    }


def _case_index(case: Dict[str, Any]) -> Dict[str, Any]:
    primary_key, primary_value = next(iter(case["metrics"].items()))
    return {
        "case_id": case["case_id"],
        "title": case["title"],
        "focus_area": case["focus_area"],
        "primary_metric": f"{primary_key}={_display(primary_value)}",
        "json": f"{case['case_id']}.json",
        "markdown": f"{case['case_id']}.md",
    }


def _cold_user_evidence(case_id: Optional[str]) -> Dict[str, Any]:
    case_artifacts = {
        "daily_reset_path_decay": [
            ("Daily reset path decay JSON", "examples/outputs/daily_reset_path_decay.json"),
            ("Daily reset path decay Markdown", "examples/outputs/daily_reset_path_decay.md"),
            ("NASDAQ simulation source", "examples/outputs/leveraged_nasdaq_3x.json"),
            ("Comparison source", "examples/outputs/compare_runs.json"),
        ],
        "drawdown_risk": [
            ("Drawdown risk JSON", "examples/outputs/drawdown_risk.json"),
            ("Drawdown risk Markdown", "examples/outputs/drawdown_risk.md"),
            ("Stress matrix source", "examples/outputs/stress_matrix.json"),
            ("Portfolio sensitivity source", "examples/outputs/portfolio_sensitivity.json"),
        ],
        "pretrade_guardrails": [
            ("Pretrade guardrails JSON", "examples/outputs/pretrade_guardrails.json"),
            ("Pretrade guardrails Markdown", "examples/outputs/pretrade_guardrails.md"),
            ("Pretrade plan source", "examples/outputs/pretrade_plan.json"),
            ("Order review source", "examples/outputs/order_review.json"),
        ],
    }
    case_commands = {
        "daily_reset_path_decay": "python -m leveraged_etp_risk_lab compare-runs --base examples/outputs/leveraged_nasdaq_3x.json --candidate examples/outputs/single_stock_2x.json --format markdown",
        "drawdown_risk": "python -m leveraged_etp_risk_lab portfolio-sensitivity --manifest examples/fixtures/portfolio_manifest.json --stop-loss none,0.15 --take-profit none,0.20 --format markdown",
        "pretrade_guardrails": "python -m leveraged_etp_risk_lab order-review --order-ticket examples/outputs/order_ticket.json --guardrail-check examples/outputs/guardrail_check.json --cycle-update examples/outputs/cycle_update.json --audit-trail examples/outputs/audit_trail.json --format markdown",
    }
    artifacts = [
        ("Scenario pack JSON", "examples/outputs/scenario_pack.json"),
        ("Scenario pack Markdown", "examples/outputs/scenario_pack.md"),
    ]
    commands = [
        {
            "purpose": "Regenerate the deterministic demo inputs used by the pack.",
            "command": "python -m leveraged_etp_risk_lab demo-bundle --output-dir examples/outputs",
        },
        {
            "purpose": "Regenerate the new-user scenario pack and case-study outputs.",
            "command": "python -m leveraged_etp_risk_lab scenario-pack --input-dir examples/outputs --fixtures-dir examples/fixtures --output-dir examples/outputs --format markdown",
        },
        {
            "purpose": "Validate the scenario-pack artifacts against local schemas.",
            "command": "python -m leveraged_etp_risk_lab artifact-validate examples/outputs/scenario_pack.json examples/outputs/daily_reset_path_decay.json examples/outputs/drawdown_risk.json examples/outputs/pretrade_guardrails.json --format markdown",
        },
    ]
    if case_id:
        artifacts = case_artifacts[case_id]
        commands.append({"purpose": "Inspect the source artifact behind this case.", "command": case_commands[case_id]})
    return {
        "exact_commands": commands,
        "artifact_links": [{"label": label, "path": path} for label, path in artifacts],
        "safety_boundaries": [
            "Uses checked-in fixtures and generated local examples only.",
            "Does not read live market data, private context, workflow files, environment variables, or command history.",
            "Does not place trades, contact brokers, determine suitability, or recommend buying, selling, or holding any product.",
            "Treats position sizing and guardrail outputs as educational review aids, not instructions.",
        ],
    }


def _integration_notes() -> List[Dict[str, Any]]:
    return [
        {
            "target_system": "portfolio-risk-compass",
            "complement": (
                "Scenario-pack outputs provide deterministic stress narratives and case-study metrics that can support "
                "a portfolio risk review as evidence for path decay, drawdown, and guardrail checks."
            ),
            "handoff_artifacts": [
                "scenario_pack.json",
                "daily_reset_path_decay.json",
                "drawdown_risk.json",
                "pretrade_guardrails.json",
            ],
            "dependency_boundary": (
                "No import, API call, shared storage, live-data feed, broker connection, or runtime dependency is required; "
                "another system can read or ignore these static files independently."
            ),
            "public_context": "Uses only checked-in fixtures and generated public examples; no private portfolio context is embedded.",
        },
        {
            "target_system": "invest-thesis-ledger",
            "complement": (
                "Scenario-pack case studies can be attached to thesis records as reproducible evidence for thesis pressure "
                "tests, invalidation checks, and pretrade review notes."
            ),
            "handoff_artifacts": [
                "scenario_pack.md",
                "daily_reset_path_decay.md",
                "drawdown_risk.md",
                "pretrade_guardrails.md",
            ],
            "dependency_boundary": (
                "No dependency, ledger schema change, plugin, workflow read, command history read, or bidirectional sync is assumed; "
                "the notes are portable references, not a required integration."
            ),
            "public_context": "Keeps examples generic and educational, with no account, broker, suitability, or private thesis data.",
        },
    ]


def _evidence_markdown(evidence: Dict[str, Any]) -> List[str]:
    lines = ["", "## New User Evidence", "", "### Exact Commands", ""]
    for item in evidence["exact_commands"]:
        lines.append(f"- {item['purpose']}")
        lines.append(f"  `{item['command']}`")
    lines.extend(["", "### Artifact Links", ""])
    lines.extend(f"- [{item['label']}]({_artifact_href(item['path'])}) (`{item['path']}`)" for item in evidence["artifact_links"])
    lines.extend(["", "### Safety Boundaries", ""])
    lines.extend(f"- {item}" for item in evidence["safety_boundaries"])
    return lines


def _artifact_href(path: str) -> str:
    artifact = Path(path)
    if path.startswith("examples/outputs/") or path.startswith("examples/fixtures/"):
        return artifact.name if path.startswith("examples/outputs/") else f"../fixtures/{artifact.name}"
    return path


def _artifact_rows(items: Iterable[Dict[str, Any]]) -> List[str]:
    return [f"| {item['path']} | {item['kind']} | {item['bytes']} | `{item['sha256']}` |" for item in items]


def _fixture_summaries(root: Path) -> Dict[str, Any]:
    nasdaq_product = load_product(str(root / "leveraged_nasdaq_3x.json"))
    single_product = load_product(str(root / "single_stock_2x.json"))
    nasdaq_path = load_path(str(root / "nasdaq_chop_path.csv"))
    single_path = load_path(str(root / "single_stock_gap_path.csv"))
    manifest = _load_json(root / "portfolio_manifest.json")
    thesis = (root / "thesis_note.md").read_text(encoding="utf-8")
    return {
        "leveraged_nasdaq_3x": {"ticker": nasdaq_product.ticker, "leverage": nasdaq_product.leverage},
        "single_stock_2x": {"ticker": single_product.ticker, "leverage": single_product.leverage},
        "nasdaq_chop_path": {"days": len(nasdaq_path), "sum_underlying_return_pct": _pct(sum(day.underlying_return for day in nasdaq_path))},
        "single_stock_gap_path": {"days": len(single_path), "sum_underlying_return_pct": _pct(sum(day.underlying_return for day in single_path))},
        "portfolio_manifest": {"name": manifest.get("name"), "positions": len(manifest.get("positions", []))},
        "thesis_note": {"lines": len([line for line in thesis.splitlines() if line.strip()])},
    }


def _source_artifacts(paths: Iterable[Path]) -> List[Dict[str, Any]]:
    rows = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(str(path))
        rows.append(
            {
                "path": path.as_posix(),
                "kind": path.suffix.lstrip(".") or "file",
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
            }
        )
    return rows


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a JSON object")
    return data


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _min_row(rows: List[Dict[str, Any]], key: str) -> Dict[str, Any]:
    if not rows:
        return {}
    return min(rows, key=lambda row: float(row.get(key, 0.0)))


def _not_advice() -> str:
    return (
        "This scenario pack is for scenario planning and education only. "
        "It is not investment advice, a recommendation, or a suitability determination."
    )


def _pct(value: float) -> float:
    return round(value * 100.0, 4)


def _display(value: Any) -> str:
    if value is None:
        return "n/a"
    return str(value)


def _unique(items: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
