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
from .render import checklist_json, checklist_markdown, exposure_markdown, simulation_markdown, to_json, version_report


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
