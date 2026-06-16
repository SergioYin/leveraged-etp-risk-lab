from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from . import __version__
from .docs_export import docs_export, docs_export_html, docs_export_markdown
from .engine import exposure_report, generate_scenario, portfolio_sensitivity, position_size_plan, sensitivity_grid, simulate, stress_matrix
from .factsheet import factsheet_check, factsheet_check_markdown
from .glossary import explain_term, glossary_packet, term_ids
from .io import load_path, load_portfolio_manifest, load_product, write_path_csv, write_text
from .models import RiskBand, SimulationConfig
from .package_audit import package_audit, package_audit_markdown
from .render import (
    checklist_json,
    checklist_markdown,
    dashboard_html,
    default_pretrade_assumptions,
    demo_story_markdown,
    demo_story_packet,
    exposure_markdown,
    glossary_markdown,
    glossary_term_markdown,
    load_demo_outputs,
    pretrade_plan_markdown,
    pretrade_plan_packet,
    portfolio_sensitivity_markdown,
    position_size_markdown,
    regime_gallery_markdown,
    sensitivity_grid_markdown,
    simulation_markdown,
    stress_matrix_markdown,
    template_gallery_markdown,
    to_json,
    version_report,
)
from .reports import (
    append_ledger,
    asset_hub,
    asset_hub_markdown,
    audit_trail,
    audit_trail_markdown,
    compare_reports,
    compare_reports_markdown,
    cycle_init,
    cycle_init_markdown,
    cycle_update,
    cycle_update_markdown,
    gallery_index,
    gallery_index_markdown,
    guardrail_check,
    guardrail_check_markdown,
    guardrail_policy,
    guardrail_policy_markdown,
    load_json_report,
    memo_draft,
    memo_draft_markdown,
    memo_review,
    memo_review_markdown,
    order_review,
    order_review_markdown,
    order_ticket,
    order_ticket_markdown,
    report_card,
    report_card_markdown,
    thesis_dashboard_data,
    thesis_dashboard_markdown,
    thesis_impact,
    thesis_impact_markdown,
    watchlist_build,
    watchlist_markdown,
)
from .regimes import regime_gallery, regime_ids, regime_path
from .release import release_manifest, release_manifest_markdown
from .recipe import recipe_run, recipe_run_markdown
from .risk_profile import PROFILE_IDS, risk_profile_markdown, risk_profile_packet
from .schema_validation import artifact_validate, artifact_validation_markdown, schema_inventory, schema_inventory_markdown
from .scenario_pack import scenario_pack_markdown, scenario_pack_review_receipt_markdown, write_scenario_pack, write_scenario_pack_review_receipt
from .templates import get_template, template_gallery, template_ids, template_product


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "simulate":
            return command_simulate(args)
        if args.command == "checklist":
            return command_checklist(args)
        if args.command == "generate-scenario":
            return command_generate_scenario(args)
        if args.command == "exposure-report":
            return command_exposure_report(args)
        if args.command == "pretrade-plan":
            return command_pretrade_plan(args)
        if args.command == "position-size":
            return command_position_size(args)
        if args.command == "stress-matrix":
            return command_stress_matrix(args)
        if args.command == "sensitivity-grid":
            return command_sensitivity_grid(args)
        if args.command == "portfolio-sensitivity":
            return command_portfolio_sensitivity(args)
        if args.command == "compare-runs":
            return command_compare_runs(args)
        if args.command == "run-ledger":
            return command_run_ledger(args)
        if args.command == "thesis-impact":
            return command_thesis_impact(args)
        if args.command == "watchlist-build":
            return command_watchlist_build(args)
        if args.command == "factsheet-check":
            return command_factsheet_check(args)
        if args.command == "risk-profile":
            return command_risk_profile(args)
        if args.command == "recipe-run":
            return command_recipe_run(args)
        if args.command == "report-card":
            return command_report_card(args)
        if args.command == "thesis-dashboard-data":
            return command_thesis_dashboard_data(args)
        if args.command == "audit-trail":
            return command_audit_trail(args)
        if args.command == "memo-draft":
            return command_memo_draft(args)
        if args.command == "memo-review":
            return command_memo_review(args)
        if args.command == "cycle-init":
            return command_cycle_init(args)
        if args.command == "cycle-update":
            return command_cycle_update(args)
        if args.command == "guardrail-policy":
            return command_guardrail_policy(args)
        if args.command == "guardrail-check":
            return command_guardrail_check(args)
        if args.command == "order-ticket":
            return command_order_ticket(args)
        if args.command == "order-review":
            return command_order_review(args)
        if args.command == "static-dashboard":
            return command_static_dashboard(args)
        if args.command == "template-list":
            return command_template_list(args)
        if args.command == "template-export":
            return command_template_export(args)
        if args.command == "regime-list":
            return command_regime_list(args)
        if args.command == "regime-export":
            return command_regime_export(args)
        if args.command == "demo-bundle":
            return command_demo_bundle(args)
        if args.command == "demo-story":
            return command_demo_story(args)
        if args.command == "gallery-index":
            return command_gallery_index(args)
        if args.command == "asset-hub":
            return command_asset_hub(args)
        if args.command == "scenario-pack":
            return command_scenario_pack(args)
        if args.command == "scenario-pack-reviewer-receipt":
            return command_scenario_pack_reviewer_receipt(args)
        if args.command == "package-audit":
            return command_package_audit(args)
        if args.command == "schema-inventory":
            return command_schema_inventory(args)
        if args.command == "artifact-validate":
            return command_artifact_validate(args)
        if args.command == "release-manifest":
            return command_release_manifest(args)
        if args.command == "docs-export":
            return command_docs_export(args)
        if args.command == "explain-term":
            return command_explain_term(args)
        if args.command == "glossary-list":
            return command_glossary_list(args)
        if args.command == "selfcheck":
            return command_selfcheck()
        if args.command == "version-report":
            sys.stdout.write(version_report(__version__))
            return 0
        parser.print_help()
        return 2
    except Exception as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="leveraged-etp-risk-lab")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    simulate_parser = sub.add_parser("simulate", help="run a deterministic leveraged ETP path simulation")
    simulate_parser.add_argument("--product", required=True, help="product JSON file")
    simulate_parser.add_argument("--path", required=True, help="scenario path CSV file")
    simulate_parser.add_argument("--initial-nav", type=float, default=100.0)
    simulate_parser.add_argument("--stop-loss", type=float, default=None, help="decimal stop-loss threshold, e.g. 0.15")
    simulate_parser.add_argument("--take-profit", type=float, default=None, help="decimal take-profit threshold, e.g. 0.20")
    simulate_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    simulate_parser.add_argument("--output", help="write output to a file instead of stdout")

    checklist = sub.add_parser("checklist", help="emit a leveraged ETP risk checklist")
    checklist.add_argument("--profile", choices=["default", "active-trader", "risk-review"], default="default")
    checklist.add_argument("--format", choices=["json", "markdown"], default="markdown")
    checklist.add_argument("--output", help="write output to a file instead of stdout")

    scenario = sub.add_parser("generate-scenario", help="write a deterministic scenario path CSV")
    scenario.add_argument("--kind", choices=["trend", "chop", "crash", "rebound"], required=True)
    scenario.add_argument("--days", type=int, default=10)
    scenario.add_argument("--output", required=True, help="CSV output path")

    exposure = sub.add_parser("exposure-report", help="aggregate portfolio exposure from a JSON manifest")
    exposure.add_argument("--manifest", required=True, help="portfolio manifest JSON file")
    exposure.add_argument("--format", choices=["json", "markdown"], default="json")
    exposure.add_argument("--output", help="write output to a file instead of stdout")

    plan = sub.add_parser("pretrade-plan", help="build a Markdown or JSON pretrade decision packet")
    plan.add_argument("--product", required=True, help="product JSON file")
    plan.add_argument("--path", required=True, help="scenario path CSV file")
    plan.add_argument("--thesis-file", help="Markdown/plain-text thesis note")
    plan.add_argument("--thesis-text", help="inline thesis text")
    plan.add_argument("--max-loss-budget", type=float, required=True, help="user-defined maximum loss budget")
    plan.add_argument("--initial-nav", type=float, default=100.0)
    plan.add_argument("--stop-loss", type=float, default=None, help="decimal stop-loss threshold, e.g. 0.15")
    plan.add_argument("--take-profit", type=float, default=None, help="decimal take-profit threshold, e.g. 0.20")
    plan.add_argument("--checklist-profile", choices=["default", "active-trader", "risk-review"], default="risk-review")
    plan.add_argument("--format", choices=["json", "markdown"], default="markdown")
    plan.add_argument("--output", help="write output to a file instead of stdout")

    sizing = sub.add_parser("position-size", help="build a deterministic position sizing plan")
    sizing.add_argument("--product", help="product JSON file")
    sizing.add_argument("--path", help="scenario path CSV file")
    sizing.add_argument("--pretrade-plan", help="pretrade-plan JSON file")
    sizing.add_argument("--account-value", type=float, required=True, help="account value used for risk-budget sizing")
    budget = sizing.add_mutually_exclusive_group(required=True)
    budget.add_argument("--risk-budget-pct", type=float, help="decimal account risk budget, e.g. 0.01")
    budget.add_argument("--max-loss-budget", type=float, help="absolute maximum loss budget")
    sizing.add_argument("--stop-loss", type=float, default=None, help="decimal stop-loss threshold, e.g. 0.15")
    sizing.add_argument("--format", choices=["json", "markdown"], default="json")
    sizing.add_argument("--output", help="write output to a file instead of stdout")

    stress = sub.add_parser("stress-matrix", help="run product terms across built-in market regimes")
    stress.add_argument("--product", required=True, help="product JSON file")
    stress.add_argument("--regime", action="append", choices=regime_ids(), help="built-in regime id; repeatable")
    stress.add_argument("--initial-nav", type=float, default=100.0)
    stress.add_argument("--stop-loss", type=float, default=None, help="decimal stop-loss threshold, e.g. 0.15")
    stress.add_argument("--take-profit", type=float, default=None, help="decimal take-profit threshold, e.g. 0.20")
    stress.add_argument("--format", choices=["json", "markdown"], default="json")
    stress.add_argument("--output", help="write output to a file instead of stdout")

    sensitivity = sub.add_parser("sensitivity-grid", help="run built-in regimes across leverage and risk-band grids")
    sensitivity.add_argument("--product", required=True, help="product JSON file")
    sensitivity.add_argument("--regime", action="append", choices=regime_ids(), help="built-in regime id; repeatable")
    sensitivity.add_argument("--initial-nav", type=float, default=100.0)
    sensitivity.add_argument(
        "--leverage-multiplier",
        action="append",
        help="leverage grid value such as 1, 2, 3, -2, or comma-separated values; default is 1,2,3 with product sign",
    )
    sensitivity.add_argument(
        "--stop-loss",
        action="append",
        help="stop-loss grid decimal such as 0.10, or none; repeatable or comma-separated",
    )
    sensitivity.add_argument(
        "--take-profit",
        action="append",
        help="take-profit grid decimal such as 0.25, or none; repeatable or comma-separated",
    )
    sensitivity.add_argument("--format", choices=["json", "markdown"], default="json")
    sensitivity.add_argument("--output", help="write output to a file instead of stdout")

    portfolio_sensitivity_parser = sub.add_parser(
        "portfolio-sensitivity",
        help="run sensitivity-grid style summaries for every manifest position and aggregate worst-case exposure",
    )
    portfolio_sensitivity_parser.add_argument("--manifest", required=True, help="portfolio manifest JSON file")
    portfolio_sensitivity_parser.add_argument("--regime", action="append", choices=regime_ids(), help="built-in regime id; repeatable")
    portfolio_sensitivity_parser.add_argument("--initial-nav", type=float, default=100.0)
    portfolio_sensitivity_parser.add_argument(
        "--leverage-multiplier",
        action="append",
        help="leverage grid value such as 1, 2, 3, -2, or comma-separated values; default is 1,2,3 with product sign",
    )
    portfolio_sensitivity_parser.add_argument(
        "--stop-loss",
        action="append",
        help="stop-loss grid decimal such as 0.10, or none; repeatable or comma-separated",
    )
    portfolio_sensitivity_parser.add_argument(
        "--take-profit",
        action="append",
        help="take-profit grid decimal such as 0.25, or none; repeatable or comma-separated",
    )
    portfolio_sensitivity_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    portfolio_sensitivity_parser.add_argument("--output", help="write output to a file instead of stdout")

    compare = sub.add_parser("compare-runs", help="compare two simulation, pretrade, or exposure JSON outputs")
    compare.add_argument("--base", required=True, help="base JSON output")
    compare.add_argument("--candidate", required=True, help="candidate JSON output")
    compare.add_argument("--format", choices=["json", "markdown"], default="json")
    compare.add_argument("--output", help="write output to a file instead of stdout")

    ledger = sub.add_parser("run-ledger", help="append deterministic metadata rows for generated outputs")
    ledger.add_argument("--ledger", required=True, help="JSONL ledger file to append")
    ledger.add_argument("--artifact", action="append", required=True, help="generated output file to record; repeatable")

    impact = sub.add_parser("thesis-impact", help="map thesis claims to observed metrics, warnings, and actions")
    impact.add_argument("--thesis-file", required=True, help="Markdown thesis file")
    impact.add_argument("--artifact", action="append", required=True, help="generated JSON artifact to inspect; repeatable")
    impact.add_argument("--format", choices=["json", "markdown"], default="json")
    impact.add_argument("--output", help="write output to a file instead of stdout")

    watchlist = sub.add_parser("watchlist-build", help="build a thesis and regime trigger watchlist ledger")
    watchlist.add_argument("--thesis-impact", required=True, help="thesis-impact JSON output")
    watchlist.add_argument("--stress-matrix", required=True, help="stress-matrix JSON output")
    watchlist.add_argument("--format", choices=["json", "markdown"], default="json")
    watchlist.add_argument("--output", help="write output to a file instead of stdout")

    factsheet = sub.add_parser("factsheet-check", help="review product terms against an optional factsheet note")
    factsheet.add_argument("--product", required=True, help="product JSON file")
    factsheet.add_argument("--factsheet-file", help="plain-text factsheet note")
    factsheet.add_argument("--format", choices=["json", "markdown"], default="json")
    factsheet.add_argument("--output", help="write output to a file instead of stdout")

    risk_profile = sub.add_parser("risk-profile", help="emit leveraged ETP risk-rule profile rules")
    risk_profile.add_argument("--profile", choices=PROFILE_IDS, help="emit one profile instead of all profiles")
    risk_profile.add_argument("--format", choices=["json", "markdown"], default="json")
    risk_profile.add_argument("--output", help="write output to a file instead of stdout")

    recipe = sub.add_parser("recipe-run", help="run a deterministic JSON workflow recipe without shelling out")
    recipe.add_argument("--recipe", required=True, help="recipe JSON file")
    recipe.add_argument("--format", choices=["json", "markdown"], default="json")
    recipe.add_argument("--output", help="write output to a file instead of stdout")

    card = sub.add_parser("report-card", help="summarize generated artifacts into a decision-readiness card")
    card.add_argument("--artifact", action="append", required=True, help="generated JSON artifact to inspect; repeatable")
    card.add_argument("--format", choices=["json", "markdown"], default="json")
    card.add_argument("--output", help="write output to a file instead of stdout")

    thesis_dashboard = sub.add_parser(
        "thesis-dashboard-data",
        help="merge recipe-run, report-card, watchlist, and sensitivity-grid outputs into a dashboard packet",
    )
    thesis_dashboard.add_argument("--recipe-run", required=True, help="recipe-run JSON output")
    thesis_dashboard.add_argument("--report-card", required=True, help="report-card JSON output")
    thesis_dashboard.add_argument("--watchlist", required=True, help="watchlist JSON output")
    thesis_dashboard.add_argument("--sensitivity-grid", required=True, help="sensitivity-grid JSON output")
    thesis_dashboard.add_argument("--format", choices=["json", "markdown"], default="json")
    thesis_dashboard.add_argument("--output", help="write output to a file instead of stdout")

    audit_trail_parser = sub.add_parser(
        "audit-trail",
        help="check run-ledger rows against artifact hashes and provenance metadata",
    )
    audit_trail_parser.add_argument("--ledger", required=True, help="run-ledger JSONL file")
    audit_trail_parser.add_argument("--artifact", action="append", required=True, help="generated artifact to verify; repeatable")
    audit_trail_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    audit_trail_parser.add_argument("--output", help="write output to a file instead of stdout")

    memo_draft_parser = sub.add_parser(
        "memo-draft",
        help="compose recipe, dashboard, report-card, and optional factsheet outputs into an investment memo packet",
    )
    memo_draft_parser.add_argument("--recipe-run", required=True, help="recipe-run JSON output")
    memo_draft_parser.add_argument("--thesis-dashboard-data", required=True, help="thesis-dashboard-data JSON output")
    memo_draft_parser.add_argument("--report-card", required=True, help="report-card JSON output")
    memo_draft_parser.add_argument("--factsheet-check", help="optional factsheet-check JSON output")
    memo_draft_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    memo_draft_parser.add_argument("--output", help="write output to a file instead of stdout")

    memo_review_parser = sub.add_parser(
        "memo-review",
        help="review a memo packet against latest report-card, watchlist, and audit-trail outputs",
    )
    memo_review_parser.add_argument("--memo", required=True, help="memo-draft JSON output")
    memo_review_parser.add_argument("--report-card", required=True, help="latest report-card JSON output")
    memo_review_parser.add_argument("--watchlist", required=True, help="latest watchlist JSON output")
    memo_review_parser.add_argument("--audit-trail", required=True, help="latest audit-trail JSON output")
    memo_review_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    memo_review_parser.add_argument("--output", help="write output to a file instead of stdout")

    cycle_init_parser = sub.add_parser(
        "cycle-init",
        help="create a persistent watch cycle state from baseline memo, watchlist, report-card, and sensitivity-grid outputs",
    )
    cycle_init_parser.add_argument("--memo", required=True, help="investment memo JSON output")
    cycle_init_parser.add_argument("--watchlist", required=True, help="watchlist JSON output")
    cycle_init_parser.add_argument("--report-card", required=True, help="report-card JSON output")
    cycle_init_parser.add_argument("--sensitivity-grid", required=True, help="sensitivity-grid JSON output")
    cycle_init_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    cycle_init_parser.add_argument("--output", help="write output to a file instead of stdout")

    cycle_update_parser = sub.add_parser(
        "cycle-update",
        help="compare a cycle state with latest report-card, watchlist, and audit-trail outputs",
    )
    cycle_update_parser.add_argument("--cycle-state", required=True, help="cycle_state JSON output")
    cycle_update_parser.add_argument("--report-card", required=True, help="latest report-card JSON output")
    cycle_update_parser.add_argument("--watchlist", required=True, help="latest watchlist JSON output")
    cycle_update_parser.add_argument("--audit-trail", required=True, help="latest audit-trail JSON output")
    cycle_update_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    cycle_update_parser.add_argument("--output", help="write output to a file instead of stdout")

    guardrail_policy_parser = sub.add_parser(
        "guardrail-policy",
        help="emit a deterministic allocation guardrail policy",
    )
    guardrail_policy_parser.add_argument("--policy", choices=["default", "conservative", "aggressive"], default="default")
    guardrail_policy_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    guardrail_policy_parser.add_argument("--output", help="write output to a file instead of stdout")

    guardrail_check_parser = sub.add_parser(
        "guardrail-check",
        help="check allocation artifacts against a guardrail policy JSON",
    )
    guardrail_check_parser.add_argument("--policy", required=True, help="guardrail-policy JSON output")
    guardrail_check_parser.add_argument("--portfolio-sensitivity", required=True, help="portfolio-sensitivity JSON output")
    guardrail_check_parser.add_argument("--position-size", required=True, help="position-size JSON output")
    guardrail_check_parser.add_argument("--investment-memo", required=True, help="investment-memo JSON output")
    guardrail_check_parser.add_argument("--cycle-update", required=True, help="cycle-update JSON output")
    guardrail_check_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    guardrail_check_parser.add_argument("--output", help="write output to a file instead of stdout")

    order_ticket_parser = sub.add_parser(
        "order-ticket",
        help="compose a placeholder-only pre-order ticket from reviewed artifacts",
    )
    order_ticket_parser.add_argument("--guardrail-check", required=True, help="guardrail-check JSON output")
    order_ticket_parser.add_argument("--investment-memo", required=True, help="investment-memo JSON output")
    order_ticket_parser.add_argument("--position-size", required=True, help="position-size JSON output")
    order_ticket_parser.add_argument("--factsheet-check", required=True, help="factsheet-check JSON output")
    order_ticket_parser.add_argument("--thesis-dashboard-data", help="optional thesis-dashboard-data JSON output")
    order_ticket_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    order_ticket_parser.add_argument("--output", help="write output to a file instead of stdout")

    order_review_parser = sub.add_parser(
        "order-review",
        help="review an order ticket against guardrail, cycle, and audit artifacts without broker execution",
    )
    order_review_parser.add_argument("--order-ticket", required=True, help="order-ticket JSON output")
    order_review_parser.add_argument("--guardrail-check", required=True, help="guardrail-check JSON output")
    order_review_parser.add_argument("--cycle-update", required=True, help="cycle-update JSON output")
    order_review_parser.add_argument("--audit-trail", required=True, help="audit-trail JSON output")
    order_review_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    order_review_parser.add_argument("--output", help="write output to a file instead of stdout")

    dashboard = sub.add_parser("static-dashboard", help="render a self-contained no-JS HTML risk dashboard")
    dashboard_source = dashboard.add_mutually_exclusive_group(required=True)
    dashboard_source.add_argument("--input-dir", help="directory containing demo output JSON files")
    dashboard_source.add_argument("--manifest", help="portfolio manifest JSON file")
    dashboard.add_argument("--title", default="Leveraged ETP Risk Dashboard")
    dashboard.add_argument("--output", required=True, help="HTML output path")

    template_list = sub.add_parser("template-list", help="list built-in product templates")
    template_list.add_argument("--format", choices=["json", "markdown"], default="json")
    template_list.add_argument("--output", help="write output to a file instead of stdout")

    template_export = sub.add_parser("template-export", help="write a selected product template JSON")
    template_export.add_argument("--template", required=True, choices=template_ids(), help="template id")
    template_export.add_argument("--output", required=True, help="product JSON output path")

    regime_list = sub.add_parser("regime-list", help="list built-in market regimes")
    regime_list.add_argument("--format", choices=["json", "markdown"], default="json")
    regime_list.add_argument("--output", help="write output to a file instead of stdout")

    regime_export = sub.add_parser("regime-export", help="write a selected market regime path CSV")
    regime_export.add_argument("--regime", required=True, choices=regime_ids(), help="regime id")
    regime_export.add_argument("--days", type=int, default=None, help="override the regime default day count")
    regime_export.add_argument("--output", required=True, help="path CSV output")

    demo = sub.add_parser("demo-bundle", help="generate deterministic demo outputs")
    demo.add_argument("--output-dir", default="examples/outputs")

    story = sub.add_parser("demo-story", help="emit a public walkthrough from demo outputs")
    story.add_argument("--input-dir", default="examples/outputs", help="directory containing demo output JSON files")
    story.add_argument("--format", choices=["json", "markdown"], default="markdown")
    story.add_argument("--output", help="write output to a file instead of stdout")

    gallery = sub.add_parser("gallery-index", help="emit a public index of demo output artifacts")
    gallery.add_argument("--input-dir", default="examples/outputs", help="directory containing demo output artifacts")
    gallery.add_argument("--format", choices=["json", "markdown"], default="markdown")
    gallery.add_argument("--output", help="write output to a file instead of stdout")

    hub = sub.add_parser("asset-hub", help="emit a GitHub-facing public asset hub from checked demo artifacts")
    hub.add_argument("--input-dir", default="examples/outputs", help="directory containing demo output artifacts")
    hub.add_argument("--format", choices=["json", "markdown"], default="markdown")
    hub.add_argument("--output", help="write output to a file instead of stdout")

    scenario_pack_parser = sub.add_parser(
        "scenario-pack",
        help="write deterministic Markdown and JSON case-study packs from local example fixtures and reports",
    )
    scenario_pack_parser.add_argument("--input-dir", default="examples/outputs", help="directory containing generated JSON reports")
    scenario_pack_parser.add_argument("--fixtures-dir", default="examples/fixtures", help="directory containing example fixtures")
    scenario_pack_parser.add_argument("--output-dir", default="examples/outputs", help="directory where scenario-pack artifacts are written")
    scenario_pack_parser.add_argument("--format", choices=["json", "markdown"], default="markdown", help="stdout summary format")
    scenario_pack_parser.add_argument("--output", help="write stdout summary to a file instead of stdout")

    receipt = sub.add_parser(
        "scenario-pack-reviewer-receipt",
        help="write a deterministic reviewer receipt for scenario-pack fixtures, hashes, and safety boundaries",
    )
    receipt.add_argument("--input-dir", default="examples/outputs", help="directory containing generated JSON report inputs")
    receipt.add_argument("--fixtures-dir", default="examples/fixtures", help="directory containing example fixtures")
    receipt.add_argument("--artifact-dir", default="examples/outputs", help="directory containing generated scenario-pack artifacts")
    receipt.add_argument("--output-dir", default="examples/outputs", help="directory where reviewer receipt artifacts are written")
    receipt.add_argument("--format", choices=["json", "markdown"], default="markdown", help="stdout summary format")
    receipt.add_argument("--output", help="write stdout summary to a file instead of stdout")

    audit = sub.add_parser("package-audit", help="emit a package readiness checklist")
    audit.add_argument("--format", choices=["json", "markdown"], default="json")
    audit.add_argument("--run-tests", action="store_true", help="run listed test commands while auditing")
    audit.add_argument("--output", help="write output to a file instead of stdout")

    inventory = sub.add_parser("schema-inventory", help="list local JSON schemas and matching example artifacts")
    inventory.add_argument("--examples-dir", default="examples/outputs", help="directory containing example JSON outputs")
    inventory.add_argument("--format", choices=["json", "markdown"], default="json")
    inventory.add_argument("--output", help="write output to a file instead of stdout")

    artifact_validation = sub.add_parser("artifact-validate", help="validate JSON artifacts against local lightweight schemas")
    artifact_validation.add_argument("path", nargs="*", help="JSON or JSONL artifact paths; defaults to examples/outputs")
    artifact_validation.add_argument("--format", choices=["json", "markdown"], default="json")
    artifact_validation.add_argument("--output", help="write output to a file instead of stdout")

    manifest = sub.add_parser("release-manifest", help="emit a release manifest from public local artifacts")
    manifest.add_argument("--input-dir", default="examples/outputs", help="directory containing release source artifacts")
    manifest.add_argument("--format", choices=["json", "markdown"], default="json")
    manifest.add_argument("--no-git", action="store_true", help="skip optional git metadata collection")
    manifest.add_argument("--output", help="write output to a file instead of stdout")

    docs = sub.add_parser("docs-export", help="emit one self-contained no-JS static HTML documentation page")
    docs.add_argument("--input-dir", default="examples/outputs", help="directory containing release and demo artifacts")
    docs.add_argument("--title", default="Leveraged ETP Risk Lab Documentation")
    docs.add_argument("--format", choices=["html", "json", "markdown"], default="html")
    docs.add_argument("--output", help="write output to a file instead of stdout")

    explain = sub.add_parser("explain-term", help="explain a built-in leveraged product glossary term")
    explain.add_argument("term", choices=term_ids(), help="built-in glossary term id")
    explain.add_argument("--format", choices=["json", "markdown"], default="markdown")
    explain.add_argument("--output", help="write output to a file instead of stdout")

    glossary = sub.add_parser("glossary-list", help="list built-in leveraged product glossary terms")
    glossary.add_argument("--format", choices=["json", "markdown"], default="json")
    glossary.add_argument("--output", help="write output to a file instead of stdout")

    sub.add_parser("selfcheck", help="run repository selfcheck")
    sub.add_parser("version-report", help="emit deterministic version and command metadata")
    return parser


def command_simulate(args: argparse.Namespace) -> int:
    result = simulate(
        SimulationConfig(
            product=load_product(args.product),
            path=load_path(args.path),
            initial_nav=args.initial_nav,
            risk_band=RiskBand(stop_loss=args.stop_loss, take_profit=args.take_profit),
        )
    )
    text = to_json(result) if args.format == "json" else simulation_markdown(result)
    return emit(text, args.output)


def command_checklist(args: argparse.Namespace) -> int:
    text = checklist_json(args.profile) if args.format == "json" else checklist_markdown(args.profile)
    return emit(text, args.output)


def command_generate_scenario(args: argparse.Namespace) -> int:
    days = generate_scenario(args.kind, args.days)
    write_path_csv(Path(args.output), days)
    sys.stdout.write(f"wrote {args.kind} scenario with {args.days} days to {args.output}\n")
    return 0


def command_exposure_report(args: argparse.Namespace) -> int:
    result = exposure_report(load_portfolio_manifest(args.manifest), args.manifest)
    text = to_json(result) if args.format == "json" else exposure_markdown(result)
    return emit(text, args.output)


def command_pretrade_plan(args: argparse.Namespace) -> int:
    if args.max_loss_budget <= 0:
        raise ValueError("--max-loss-budget must be positive")
    thesis = _load_thesis(args.thesis_file, args.thesis_text)
    result = simulate(
        SimulationConfig(
            product=load_product(args.product),
            path=load_path(args.path),
            initial_nav=args.initial_nav,
            risk_band=RiskBand(stop_loss=args.stop_loss, take_profit=args.take_profit),
        )
    )
    packet = pretrade_plan_packet(
        simulation=result,
        thesis=thesis,
        max_loss_budget=args.max_loss_budget,
        checklist_profile=args.checklist_profile,
        assumptions=default_pretrade_assumptions(),
        provenance={
            "command": "pretrade-plan",
            "product": args.product,
            "path": args.path,
            "thesis_file": args.thesis_file or "",
            "max_loss_budget": args.max_loss_budget,
            "initial_nav": args.initial_nav,
            "stop_loss": args.stop_loss,
            "take_profit": args.take_profit,
            "checklist_profile": args.checklist_profile,
        },
    )
    text = to_json(packet) if args.format == "json" else pretrade_plan_markdown(packet)
    return emit(text, args.output)


def command_position_size(args: argparse.Namespace) -> int:
    if args.account_value <= 0:
        raise ValueError("--account-value must be positive")
    if args.risk_budget_pct is not None:
        if not 0 < args.risk_budget_pct <= 1:
            raise ValueError("--risk-budget-pct must be a decimal between 0 and 1")
        max_loss_budget = args.account_value * args.risk_budget_pct
    else:
        max_loss_budget = args.max_loss_budget
    if args.pretrade_plan:
        if args.product or args.path:
            raise ValueError("--pretrade-plan cannot be combined with --product or --path")
        source_data = load_json_report(args.pretrade_plan)
        if source_data.get("document_type") != "pretrade_plan":
            raise ValueError("--pretrade-plan must point to a pretrade_plan JSON output")
        source = {
            "command": "position-size",
            "source": "pretrade_plan",
            "pretrade_plan": args.pretrade_plan,
            "account_value": args.account_value,
            "risk_budget_pct": args.risk_budget_pct,
            "max_loss_budget": args.max_loss_budget,
            "stop_loss": args.stop_loss,
        }
        simulation = source_data
    else:
        if not args.product or not args.path:
            raise ValueError("provide --pretrade-plan or both --product and --path")
        simulation = simulate(
            SimulationConfig(
                product=load_product(args.product),
                path=load_path(args.path),
                initial_nav=100.0,
                risk_band=RiskBand(stop_loss=args.stop_loss),
            )
        )
        source = {
            "command": "position-size",
            "source": "product_path",
            "product": args.product,
            "path": args.path,
            "account_value": args.account_value,
            "risk_budget_pct": args.risk_budget_pct,
            "max_loss_budget": args.max_loss_budget,
            "stop_loss": args.stop_loss,
        }
    packet = position_size_plan(
        simulation=simulation,
        account_value=args.account_value,
        max_loss_budget=max_loss_budget,
        stop_loss=args.stop_loss,
        source=source,
    )
    text = to_json(packet) if args.format == "json" else position_size_markdown(packet)
    return emit(text, args.output)


def command_compare_runs(args: argparse.Namespace) -> int:
    result = compare_reports(args.base, args.candidate)
    text = to_json(result) if args.format == "json" else compare_reports_markdown(result)
    return emit(text, args.output)


def command_stress_matrix(args: argparse.Namespace) -> int:
    result = stress_matrix(
        product=load_product(args.product),
        selected_regimes=args.regime,
        initial_nav=args.initial_nav,
        risk_band=RiskBand(stop_loss=args.stop_loss, take_profit=args.take_profit),
        product_path=args.product,
    )
    text = to_json(result) if args.format == "json" else stress_matrix_markdown(result)
    return emit(text, args.output)


def command_sensitivity_grid(args: argparse.Namespace) -> int:
    result = sensitivity_grid(
        product=load_product(args.product),
        leverage_multipliers=_parse_float_grid(args.leverage_multiplier, "leverage-multiplier"),
        stop_losses=_parse_optional_float_grid(args.stop_loss, "stop-loss"),
        take_profits=_parse_optional_float_grid(args.take_profit, "take-profit"),
        selected_regimes=args.regime,
        initial_nav=args.initial_nav,
        product_path=args.product,
    )
    text = to_json(result) if args.format == "json" else sensitivity_grid_markdown(result)
    return emit(text, args.output)


def command_portfolio_sensitivity(args: argparse.Namespace) -> int:
    result = portfolio_sensitivity(
        manifest=load_portfolio_manifest(args.manifest),
        manifest_path=args.manifest,
        leverage_multipliers=_parse_float_grid(args.leverage_multiplier, "leverage-multiplier"),
        stop_losses=_parse_optional_float_grid(args.stop_loss, "stop-loss"),
        take_profits=_parse_optional_float_grid(args.take_profit, "take-profit"),
        selected_regimes=args.regime,
        initial_nav=args.initial_nav,
    )
    text = to_json(result) if args.format == "json" else portfolio_sensitivity_markdown(result)
    return emit(text, args.output)


def command_run_ledger(args: argparse.Namespace) -> int:
    result = append_ledger(args.ledger, args.artifact)
    sys.stdout.write(to_json(result))
    return 0


def command_thesis_impact(args: argparse.Namespace) -> int:
    result = thesis_impact(args.thesis_file, args.artifact)
    text = to_json(result) if args.format == "json" else thesis_impact_markdown(result)
    return emit(text, args.output)


def command_watchlist_build(args: argparse.Namespace) -> int:
    result = watchlist_build(args.thesis_impact, args.stress_matrix)
    text = to_json(result) if args.format == "json" else watchlist_markdown(result)
    return emit(text, args.output)


def command_factsheet_check(args: argparse.Namespace) -> int:
    result = factsheet_check(args.product, args.factsheet_file)
    text = to_json(result) if args.format == "json" else factsheet_check_markdown(result)
    return emit(text, args.output)


def command_risk_profile(args: argparse.Namespace) -> int:
    result = risk_profile_packet(args.profile)
    text = to_json(result) if args.format == "json" else risk_profile_markdown(result)
    return emit(text, args.output)


def command_recipe_run(args: argparse.Namespace) -> int:
    result = recipe_run(args.recipe)
    text = to_json(result) if args.format == "json" else recipe_run_markdown(result)
    return emit(text, args.output)


def command_report_card(args: argparse.Namespace) -> int:
    result = report_card(args.artifact)
    text = to_json(result) if args.format == "json" else report_card_markdown(result)
    return emit(text, args.output)


def command_thesis_dashboard_data(args: argparse.Namespace) -> int:
    result = thesis_dashboard_data(args.recipe_run, args.report_card, args.watchlist, args.sensitivity_grid)
    text = to_json(result) if args.format == "json" else thesis_dashboard_markdown(result)
    return emit(text, args.output)


def command_audit_trail(args: argparse.Namespace) -> int:
    result = audit_trail(args.ledger, args.artifact)
    text = to_json(result) if args.format == "json" else audit_trail_markdown(result)
    return emit(text, args.output)


def command_memo_draft(args: argparse.Namespace) -> int:
    result = memo_draft(args.recipe_run, args.thesis_dashboard_data, args.report_card, args.factsheet_check)
    text = to_json(result) if args.format == "json" else memo_draft_markdown(result)
    return emit(text, args.output)


def command_memo_review(args: argparse.Namespace) -> int:
    result = memo_review(args.memo, args.report_card, args.watchlist, args.audit_trail)
    text = to_json(result) if args.format == "json" else memo_review_markdown(result)
    return emit(text, args.output)


def command_cycle_init(args: argparse.Namespace) -> int:
    result = cycle_init(args.memo, args.watchlist, args.report_card, args.sensitivity_grid)
    text = to_json(result) if args.format == "json" else cycle_init_markdown(result)
    return emit(text, args.output)


def command_cycle_update(args: argparse.Namespace) -> int:
    result = cycle_update(args.cycle_state, args.report_card, args.watchlist, args.audit_trail)
    text = to_json(result) if args.format == "json" else cycle_update_markdown(result)
    return emit(text, args.output)


def command_guardrail_policy(args: argparse.Namespace) -> int:
    result = guardrail_policy(args.policy)
    text = to_json(result) if args.format == "json" else guardrail_policy_markdown(result)
    return emit(text, args.output)


def command_guardrail_check(args: argparse.Namespace) -> int:
    result = guardrail_check(
        args.policy,
        args.portfolio_sensitivity,
        args.position_size,
        args.investment_memo,
        args.cycle_update,
    )
    text = to_json(result) if args.format == "json" else guardrail_check_markdown(result)
    return emit(text, args.output)


def command_order_ticket(args: argparse.Namespace) -> int:
    result = order_ticket(
        args.guardrail_check,
        args.investment_memo,
        args.position_size,
        args.factsheet_check,
        args.thesis_dashboard_data,
    )
    text = to_json(result) if args.format == "json" else order_ticket_markdown(result)
    return emit(text, args.output)


def command_order_review(args: argparse.Namespace) -> int:
    result = order_review(args.order_ticket, args.guardrail_check, args.cycle_update, args.audit_trail)
    text = to_json(result) if args.format == "json" else order_review_markdown(result)
    return emit(text, args.output)


def command_static_dashboard(args: argparse.Namespace) -> int:
    if args.manifest:
        data = exposure_report(load_portfolio_manifest(args.manifest), args.manifest)
        provenance = {"command": "static-dashboard", "source": "portfolio_manifest", "manifest": args.manifest}
    else:
        data = load_demo_outputs(Path(args.input_dir))
        provenance = {"command": "static-dashboard", "source": "demo_outputs", "input_dir": args.input_dir}
    text = dashboard_html(data, args.title, provenance)
    return emit(text, args.output)


def command_template_list(args: argparse.Namespace) -> int:
    gallery = template_gallery()
    text = to_json(gallery) if args.format == "json" else template_gallery_markdown(gallery)
    return emit(text, args.output)


def command_template_export(args: argparse.Namespace) -> int:
    get_template(args.template)
    return emit(to_json(template_product(args.template)), args.output)


def command_regime_list(args: argparse.Namespace) -> int:
    gallery = regime_gallery()
    text = to_json(gallery) if args.format == "json" else regime_gallery_markdown(gallery)
    return emit(text, args.output)


def command_regime_export(args: argparse.Namespace) -> int:
    rows = regime_path(args.regime, args.days)
    write_path_csv(Path(args.output), rows)
    sys.stdout.write(f"wrote {args.regime} regime with {len(rows)} days to {args.output}\n")
    return 0


def command_demo_bundle(args: argparse.Namespace) -> int:
    root = Path(args.output_dir)
    examples = Path("examples/fixtures")
    jobs = [
        (
            "leveraged_nasdaq_3x",
            examples / "leveraged_nasdaq_3x.json",
            examples / "nasdaq_chop_path.csv",
            RiskBand(stop_loss=0.15, take_profit=0.20),
        ),
        (
            "single_stock_2x",
            examples / "single_stock_2x.json",
            examples / "single_stock_gap_path.csv",
            RiskBand(stop_loss=0.25, take_profit=0.30),
        ),
    ]
    for name, product_path, path_file, band in jobs:
        result = simulate(SimulationConfig(load_product(str(product_path)), load_path(str(path_file)), 100.0, band))
        write_text(root / f"{name}.json", to_json(result))
        write_text(root / f"{name}.md", simulation_markdown(result))
    manifest = examples / "portfolio_manifest.json"
    if manifest.exists():
        result = exposure_report(load_portfolio_manifest(str(manifest)), str(manifest))
        write_text(root / "portfolio_exposure.json", to_json(result))
        write_text(root / "portfolio_exposure.md", exposure_markdown(result))
    gallery = template_gallery()
    write_text(root / "template_gallery.json", to_json(gallery))
    write_text(root / "template_gallery.md", template_gallery_markdown(gallery))
    regimes = regime_gallery()
    write_text(root / "regime_gallery.json", to_json(regimes))
    write_text(root / "regime_gallery.md", regime_gallery_markdown(regimes))
    for regime_id in regime_ids():
        write_path_csv(root / f"regime_{regime_id}.csv", regime_path(regime_id))
    write_text(root / "checklist.md", checklist_markdown("risk-review"))
    comparison = compare_reports(str(root / "leveraged_nasdaq_3x.json"), str(root / "single_stock_2x.json"))
    write_text(root / "compare_runs.json", to_json(comparison))
    write_text(root / "compare_runs.md", compare_reports_markdown(comparison))
    command_pretrade_plan(
        argparse.Namespace(
            product=str(examples / "leveraged_nasdaq_3x.json"),
            path=str(examples / "nasdaq_chop_path.csv"),
            thesis_file=str(examples / "thesis_note.md"),
            thesis_text=None,
            max_loss_budget=750.0,
            initial_nav=100.0,
            stop_loss=0.15,
            take_profit=0.20,
            checklist_profile="risk-review",
            format="json",
            output=str(root / "pretrade_plan.json"),
        )
    )
    command_pretrade_plan(
        argparse.Namespace(
            product=str(examples / "leveraged_nasdaq_3x.json"),
            path=str(examples / "nasdaq_chop_path.csv"),
            thesis_file=str(examples / "thesis_note.md"),
            thesis_text=None,
            max_loss_budget=750.0,
            initial_nav=100.0,
            stop_loss=0.15,
            take_profit=0.20,
            checklist_profile="risk-review",
            format="markdown",
            output=str(root / "pretrade_plan.md"),
        )
    )
    command_position_size(
        argparse.Namespace(
            product=str(examples / "leveraged_nasdaq_3x.json"),
            path=str(examples / "nasdaq_chop_path.csv"),
            pretrade_plan=None,
            account_value=50000.0,
            risk_budget_pct=0.015,
            max_loss_budget=None,
            stop_loss=0.15,
            format="json",
            output=str(root / "position_size.json"),
        )
    )
    command_position_size(
        argparse.Namespace(
            product=str(examples / "leveraged_nasdaq_3x.json"),
            path=str(examples / "nasdaq_chop_path.csv"),
            pretrade_plan=None,
            account_value=50000.0,
            risk_budget_pct=0.015,
            max_loss_budget=None,
            stop_loss=0.15,
            format="markdown",
            output=str(root / "position_size.md"),
        )
    )
    command_stress_matrix(
        argparse.Namespace(
            product=str(examples / "leveraged_nasdaq_3x.json"),
            regime=None,
            initial_nav=100.0,
            stop_loss=0.15,
            take_profit=0.20,
            format="json",
            output=str(root / "stress_matrix.json"),
        )
    )
    command_stress_matrix(
        argparse.Namespace(
            product=str(examples / "leveraged_nasdaq_3x.json"),
            regime=None,
            initial_nav=100.0,
            stop_loss=0.15,
            take_profit=0.20,
            format="markdown",
            output=str(root / "stress_matrix.md"),
        )
    )
    command_sensitivity_grid(
        argparse.Namespace(
            product=str(examples / "leveraged_nasdaq_3x.json"),
            regime=None,
            initial_nav=100.0,
            leverage_multiplier=None,
            stop_loss=["none", "0.15", "0.25"],
            take_profit=["none", "0.20", "0.35"],
            format="json",
            output=str(root / "sensitivity_grid.json"),
        )
    )
    command_sensitivity_grid(
        argparse.Namespace(
            product=str(examples / "leveraged_nasdaq_3x.json"),
            regime=None,
            initial_nav=100.0,
            leverage_multiplier=None,
            stop_loss=["none", "0.15", "0.25"],
            take_profit=["none", "0.20", "0.35"],
            format="markdown",
            output=str(root / "sensitivity_grid.md"),
        )
    )
    command_portfolio_sensitivity(
        argparse.Namespace(
            manifest=str(manifest),
            regime=None,
            initial_nav=100.0,
            leverage_multiplier=None,
            stop_loss=["none", "0.15", "0.25"],
            take_profit=["none", "0.20", "0.35"],
            format="json",
            output=str(root / "portfolio_sensitivity.json"),
        )
    )
    command_portfolio_sensitivity(
        argparse.Namespace(
            manifest=str(manifest),
            regime=None,
            initial_nav=100.0,
            leverage_multiplier=None,
            stop_loss=["none", "0.15", "0.25"],
            take_profit=["none", "0.20", "0.35"],
            format="markdown",
            output=str(root / "portfolio_sensitivity.md"),
        )
    )
    command_static_dashboard(
        argparse.Namespace(
            input_dir=None,
            manifest=str(manifest),
            title="Leveraged ETP Risk Dashboard",
            output=str(root / "dashboard.html"),
        )
    )
    ledger_path = root / "run_ledger.jsonl"
    if ledger_path.exists():
        ledger_path.unlink()
    impact = thesis_impact(
        str(examples / "thesis_note.md"),
        [str(root / "pretrade_plan.json"), str(root / "compare_runs.json"), str(root / "portfolio_exposure.json")],
    )
    write_text(root / "thesis_impact.json", to_json(impact))
    write_text(root / "thesis_impact.md", thesis_impact_markdown(impact))
    watchlist = watchlist_build(str(root / "thesis_impact.json"), str(root / "stress_matrix.json"))
    write_text(root / "watchlist.json", to_json(watchlist))
    write_text(root / "watchlist.md", watchlist_markdown(watchlist))
    factsheet = factsheet_check(str(examples / "leveraged_nasdaq_3x.json"), str(examples / "factsheet_note.txt"))
    write_text(root / "factsheet_check.json", to_json(factsheet))
    write_text(root / "factsheet_check.md", factsheet_check_markdown(factsheet))
    profiles = risk_profile_packet()
    write_text(root / "risk_profiles.json", to_json(profiles))
    write_text(root / "risk_profiles.md", risk_profile_markdown(profiles))
    recipe = recipe_run(str(examples / "recipe_thesis_review.json"))
    write_text(root / "recipe_run.json", to_json(recipe))
    write_text(root / "recipe_run.md", recipe_run_markdown(recipe))
    card = report_card(
        [
            str(root / "pretrade_plan.json"),
            str(root / "position_size.json"),
            str(root / "stress_matrix.json"),
            str(root / "sensitivity_grid.json"),
            str(root / "portfolio_sensitivity.json"),
            str(root / "factsheet_check.json"),
            str(root / "risk_profiles.json"),
            str(root / "recipe_run.json"),
        ]
    )
    write_text(root / "report_card.json", to_json(card))
    write_text(root / "report_card.md", report_card_markdown(card))
    dashboard_packet = thesis_dashboard_data(
        str(root / "recipe_run.json"),
        str(root / "report_card.json"),
        str(root / "watchlist.json"),
        str(root / "sensitivity_grid.json"),
    )
    write_text(root / "thesis_dashboard_data.json", to_json(dashboard_packet))
    write_text(root / "thesis_dashboard_data.md", thesis_dashboard_markdown(dashboard_packet))
    memo = memo_draft(
        str(root / "recipe_run.json"),
        str(root / "thesis_dashboard_data.json"),
        str(root / "report_card.json"),
        str(root / "factsheet_check.json"),
    )
    write_text(root / "investment_memo.json", to_json(memo))
    write_text(root / "investment_memo.md", memo_draft_markdown(memo))
    cycle_state = cycle_init(
        str(root / "investment_memo.json"),
        str(root / "watchlist.json"),
        str(root / "report_card.json"),
        str(root / "sensitivity_grid.json"),
    )
    write_text(root / "cycle_state.json", to_json(cycle_state))
    write_text(root / "cycle_state.md", cycle_init_markdown(cycle_state))
    glossary = glossary_packet()
    write_text(root / "glossary.json", to_json(glossary))
    write_text(root / "glossary.md", glossary_markdown(glossary))
    ledger_artifacts = [
        str(root / "leveraged_nasdaq_3x.json"),
        str(root / "single_stock_2x.json"),
        str(root / "portfolio_exposure.json"),
        str(root / "pretrade_plan.json"),
        str(root / "position_size.json"),
        str(root / "stress_matrix.json"),
        str(root / "sensitivity_grid.json"),
        str(root / "portfolio_sensitivity.json"),
        str(root / "compare_runs.json"),
        str(root / "thesis_impact.json"),
        str(root / "watchlist.json"),
        str(root / "factsheet_check.json"),
        str(root / "risk_profiles.json"),
        str(root / "recipe_run.json"),
        str(root / "report_card.json"),
        str(root / "thesis_dashboard_data.json"),
        str(root / "investment_memo.json"),
        str(root / "cycle_state.json"),
    ]
    append_ledger(str(ledger_path), ledger_artifacts)
    trail = audit_trail(str(ledger_path), ledger_artifacts)
    write_text(root / "audit_trail.json", to_json(trail))
    write_text(root / "audit_trail.md", audit_trail_markdown(trail))
    memo_review_packet = memo_review(
        str(root / "investment_memo.json"),
        str(root / "report_card.json"),
        str(root / "watchlist.json"),
        str(root / "audit_trail.json"),
    )
    write_text(root / "investment_memo_review.json", to_json(memo_review_packet))
    write_text(root / "investment_memo_review.md", memo_review_markdown(memo_review_packet))
    cycle_update_packet = cycle_update(
        str(root / "cycle_state.json"),
        str(root / "report_card.json"),
        str(root / "watchlist.json"),
        str(root / "audit_trail.json"),
    )
    write_text(root / "cycle_update.json", to_json(cycle_update_packet))
    write_text(root / "cycle_update.md", cycle_update_markdown(cycle_update_packet))
    policy = guardrail_policy("default")
    write_text(root / "guardrail_policy.json", to_json(policy))
    write_text(root / "guardrail_policy.md", guardrail_policy_markdown(policy))
    guardrail = guardrail_check(
        str(root / "guardrail_policy.json"),
        str(root / "portfolio_sensitivity.json"),
        str(root / "position_size.json"),
        str(root / "investment_memo.json"),
        str(root / "cycle_update.json"),
    )
    write_text(root / "guardrail_check.json", to_json(guardrail))
    write_text(root / "guardrail_check.md", guardrail_check_markdown(guardrail))
    ticket = order_ticket(
        str(root / "guardrail_check.json"),
        str(root / "investment_memo.json"),
        str(root / "position_size.json"),
        str(root / "factsheet_check.json"),
        str(root / "thesis_dashboard_data.json"),
    )
    write_text(root / "order_ticket.json", to_json(ticket))
    write_text(root / "order_ticket.md", order_ticket_markdown(ticket))
    review = order_review(
        str(root / "order_ticket.json"),
        str(root / "guardrail_check.json"),
        str(root / "cycle_update.json"),
        str(root / "audit_trail.json"),
    )
    write_text(root / "order_review.json", to_json(review))
    write_text(root / "order_review.md", order_review_markdown(review))
    write_scenario_pack(str(root), str(examples), str(root))
    release_surface = [
        root / "package_audit.json",
        root / "package_audit.md",
        root / "demo_story.json",
        root / "demo_story.md",
        root / "gallery_index.json",
        root / "gallery_index.md",
        root / "asset_hub.json",
        root / "asset_hub.md",
        root / "schema_inventory.json",
        root / "schema_inventory.md",
        root / "artifact_validation.json",
        root / "artifact_validation.md",
        root / "release_manifest.json",
        root / "release_manifest.md",
        root / "docs_export.json",
        root / "docs_export.md",
        root / "docs_export.html",
        root / "scenario_pack.json",
        root / "scenario_pack.md",
        root / "daily_reset_path_decay.json",
        root / "daily_reset_path_decay.md",
        root / "drawdown_risk.json",
        root / "drawdown_risk.md",
        root / "pretrade_guardrails.json",
        root / "pretrade_guardrails.md",
        root / "scenario_pack_reviewer_receipt.json",
        root / "scenario_pack_reviewer_receipt.md",
    ]
    previous_snapshot = None
    release_surface_converged = False
    for _ in range(8):
        audit = package_audit(__version__)
        write_text(root / "package_audit.json", to_json(audit))
        write_text(root / "package_audit.md", package_audit_markdown(audit))
        story = demo_story_packet(root)
        write_text(root / "demo_story.json", to_json(story))
        write_text(root / "demo_story.md", demo_story_markdown(story))
        index = gallery_index(str(root))
        write_text(root / "gallery_index.json", to_json(index))
        write_text(root / "gallery_index.md", gallery_index_markdown(index))
        hub = asset_hub(str(root), __version__)
        write_text(root / "asset_hub.json", to_json(hub))
        write_text(root / "asset_hub.md", asset_hub_markdown(hub))
        inventory = schema_inventory(examples_dir=root)
        write_text(root / "schema_inventory.json", to_json(inventory))
        write_text(root / "schema_inventory.md", schema_inventory_markdown(inventory))
        validation_paths = [str(path) for path in sorted(root.glob("*.json"))] + [str(path) for path in sorted(root.glob("*.jsonl"))]
        validation = artifact_validate(validation_paths)
        write_text(root / "artifact_validation.json", to_json(validation))
        write_text(root / "artifact_validation.md", artifact_validation_markdown(validation))
        manifest = release_manifest(str(root), __version__, include_git=False)
        write_text(root / "release_manifest.json", to_json(manifest))
        write_text(root / "release_manifest.md", release_manifest_markdown(manifest))
        docs_packet = docs_export(str(root))
        write_text(root / "docs_export.json", to_json(docs_packet))
        write_text(root / "docs_export.md", docs_export_markdown(docs_packet))
        write_text(root / "docs_export.html", docs_export_html(docs_packet))
        snapshot = {path.name: path.read_text(encoding="utf-8") for path in release_surface if path.exists()}
        if snapshot == previous_snapshot:
            release_surface_converged = True
            break
        previous_snapshot = snapshot
    if not release_surface_converged:
        raise RuntimeError("release artifact generation did not converge")
    sys.stdout.write(f"wrote demo bundle to {root}\n")
    return 0


def command_demo_story(args: argparse.Namespace) -> int:
    result = demo_story_packet(Path(args.input_dir))
    text = to_json(result) if args.format == "json" else demo_story_markdown(result)
    return emit(text, args.output)


def command_gallery_index(args: argparse.Namespace) -> int:
    result = gallery_index(args.input_dir)
    text = to_json(result) if args.format == "json" else gallery_index_markdown(result)
    return emit(text, args.output)


def command_asset_hub(args: argparse.Namespace) -> int:
    result = asset_hub(args.input_dir, __version__)
    text = to_json(result) if args.format == "json" else asset_hub_markdown(result)
    return emit(text, args.output)


def command_scenario_pack(args: argparse.Namespace) -> int:
    result = write_scenario_pack(args.input_dir, args.fixtures_dir, args.output_dir)
    result.pop("_cases", None)
    text = to_json(result) if args.format == "json" else scenario_pack_markdown(result)
    return emit(text, args.output)


def command_scenario_pack_reviewer_receipt(args: argparse.Namespace) -> int:
    result = write_scenario_pack_review_receipt(args.input_dir, args.fixtures_dir, args.artifact_dir, args.output_dir)
    text = to_json(result) if args.format == "json" else scenario_pack_review_receipt_markdown(result)
    return emit(text, args.output)


def command_package_audit(args: argparse.Namespace) -> int:
    result = package_audit(__version__, run_tests=args.run_tests)
    text = to_json(result) if args.format == "json" else package_audit_markdown(result)
    return emit(text, args.output)


def command_schema_inventory(args: argparse.Namespace) -> int:
    result = schema_inventory(examples_dir=Path(args.examples_dir))
    text = to_json(result) if args.format == "json" else schema_inventory_markdown(result)
    return emit(text, args.output)


def command_artifact_validate(args: argparse.Namespace) -> int:
    result = artifact_validate(args.path or None)
    text = to_json(result) if args.format == "json" else artifact_validation_markdown(result)
    return emit(text, args.output)


def command_release_manifest(args: argparse.Namespace) -> int:
    result = release_manifest(args.input_dir, __version__, include_git=not args.no_git)
    text = to_json(result) if args.format == "json" else release_manifest_markdown(result)
    return emit(text, args.output)


def command_docs_export(args: argparse.Namespace) -> int:
    result = docs_export(args.input_dir, args.title)
    if args.format == "json":
        text = to_json(result)
    elif args.format == "markdown":
        text = docs_export_markdown(result)
    else:
        text = docs_export_html(result)
    return emit(text, args.output)


def command_explain_term(args: argparse.Namespace) -> int:
    result = explain_term(args.term)
    text = to_json(result) if args.format == "json" else glossary_term_markdown(result)
    return emit(text, args.output)


def command_glossary_list(args: argparse.Namespace) -> int:
    result = glossary_packet()
    text = to_json(result) if args.format == "json" else glossary_markdown(result)
    return emit(text, args.output)


def command_selfcheck() -> int:
    script = Path("scripts/selfcheck.py")
    if not script.exists():
        raise FileNotFoundError("scripts/selfcheck.py")
    completed = subprocess.run([sys.executable, str(script)], check=False)
    return completed.returncode


def emit(text: str, output: Optional[str]) -> int:
    if output:
        write_text(Path(output), text)
    else:
        sys.stdout.write(text)
    return 0


def _load_thesis(thesis_file: Optional[str], thesis_text: Optional[str]) -> str:
    parts = []
    if thesis_file:
        parts.append(Path(thesis_file).read_text(encoding="utf-8").strip())
    if thesis_text:
        parts.append(thesis_text.strip())
    return "\n\n".join(part for part in parts if part)


def _parse_float_grid(values: Optional[List[str]], label: str) -> Optional[List[float]]:
    parsed = _parse_optional_float_grid(values, label)
    if parsed is None:
        return None
    if any(value is None for value in parsed):
        raise ValueError(f"--{label} does not accept none")
    return [float(value) for value in parsed if value is not None]


def _parse_optional_float_grid(values: Optional[List[str]], label: str) -> Optional[List[Optional[float]]]:
    if not values:
        return None
    parsed: List[Optional[float]] = []
    for raw in values:
        for part in raw.split(","):
            item = part.strip()
            if not item:
                continue
            if item.lower() in {"none", "null", "na", "n/a"}:
                parsed.append(None)
            else:
                parsed.append(float(item))
    if not parsed:
        raise ValueError(f"--{label} grid must contain at least one value")
    return parsed
