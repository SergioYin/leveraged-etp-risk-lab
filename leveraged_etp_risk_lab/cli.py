from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from . import __version__
from .engine import exposure_report, generate_scenario, position_size_plan, simulate, stress_matrix
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
    position_size_markdown,
    regime_gallery_markdown,
    simulation_markdown,
    stress_matrix_markdown,
    template_gallery_markdown,
    to_json,
    version_report,
)
from .reports import (
    append_ledger,
    compare_reports,
    compare_reports_markdown,
    gallery_index,
    gallery_index_markdown,
    load_json_report,
    thesis_impact,
    thesis_impact_markdown,
    watchlist_build,
    watchlist_markdown,
)
from .regimes import regime_gallery, regime_ids, regime_path
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
        if args.command == "package-audit":
            return command_package_audit(args)
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

    audit = sub.add_parser("package-audit", help="emit a package readiness checklist")
    audit.add_argument("--format", choices=["json", "markdown"], default="json")
    audit.add_argument("--run-tests", action="store_true", help="run listed test commands while auditing")
    audit.add_argument("--output", help="write output to a file instead of stdout")

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
    append_ledger(
        str(ledger_path),
        [
            str(root / "leveraged_nasdaq_3x.json"),
            str(root / "single_stock_2x.json"),
            str(root / "portfolio_exposure.json"),
            str(root / "pretrade_plan.json"),
            str(root / "position_size.json"),
            str(root / "stress_matrix.json"),
            str(root / "compare_runs.json"),
        ],
    )
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
    glossary = glossary_packet()
    write_text(root / "glossary.json", to_json(glossary))
    write_text(root / "glossary.md", glossary_markdown(glossary))
    audit = package_audit(__version__)
    write_text(root / "package_audit.json", to_json(audit))
    write_text(root / "package_audit.md", package_audit_markdown(audit))
    story = demo_story_packet(root)
    write_text(root / "demo_story.json", to_json(story))
    write_text(root / "demo_story.md", demo_story_markdown(story))
    index = gallery_index(str(root))
    write_text(root / "gallery_index.json", to_json(index))
    write_text(root / "gallery_index.md", gallery_index_markdown(index))
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


def command_package_audit(args: argparse.Namespace) -> int:
    result = package_audit(__version__, run_tests=args.run_tests)
    text = to_json(result) if args.format == "json" else package_audit_markdown(result)
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
