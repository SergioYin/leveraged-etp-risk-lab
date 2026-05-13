from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from . import __version__
from .engine import exposure_report, generate_scenario, simulate
from .io import load_path, load_portfolio_manifest, load_product, write_path_csv, write_text
from .models import RiskBand, SimulationConfig
from .render import (
    checklist_json,
    checklist_markdown,
    dashboard_html,
    default_pretrade_assumptions,
    exposure_markdown,
    load_demo_outputs,
    pretrade_plan_markdown,
    pretrade_plan_packet,
    simulation_markdown,
    to_json,
    version_report,
)


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
        if args.command == "static-dashboard":
            return command_static_dashboard(args)
        if args.command == "demo-bundle":
            return command_demo_bundle(args)
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

    dashboard = sub.add_parser("static-dashboard", help="render a self-contained no-JS HTML risk dashboard")
    dashboard_source = dashboard.add_mutually_exclusive_group(required=True)
    dashboard_source.add_argument("--input-dir", help="directory containing demo output JSON files")
    dashboard_source.add_argument("--manifest", help="portfolio manifest JSON file")
    dashboard.add_argument("--title", default="Leveraged ETP Risk Dashboard")
    dashboard.add_argument("--output", required=True, help="HTML output path")

    demo = sub.add_parser("demo-bundle", help="generate deterministic demo outputs")
    demo.add_argument("--output-dir", default="examples/outputs")

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


def command_static_dashboard(args: argparse.Namespace) -> int:
    if args.manifest:
        data = exposure_report(load_portfolio_manifest(args.manifest), args.manifest)
        provenance = {"command": "static-dashboard", "source": "portfolio_manifest", "manifest": args.manifest}
    else:
        data = load_demo_outputs(Path(args.input_dir))
        provenance = {"command": "static-dashboard", "source": "demo_outputs", "input_dir": args.input_dir}
    text = dashboard_html(data, args.title, provenance)
    return emit(text, args.output)


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
    write_text(root / "checklist.md", checklist_markdown("risk-review"))
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
    command_static_dashboard(
        argparse.Namespace(
            input_dir=None,
            manifest=str(manifest),
            title="Leveraged ETP Risk Dashboard",
            output=str(root / "dashboard.html"),
        )
    )
    sys.stdout.write(f"wrote demo bundle to {root}\n")
    return 0


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
