#!/usr/bin/env python3
from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable, List


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".py", ".json", ".csv", ".toml", ".txt", ""}


def main() -> int:
    checks = [
        check_required_files,
        check_no_workflows,
        check_public_hygiene,
        check_no_runtime_dependencies,
        check_tests,
        check_cli_smoke,
    ]
    failures: List[str] = []
    for check in checks:
        try:
            failures.extend(check())
        except Exception as exc:
            failures.append(f"{check.__name__}: {exc}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print("selfcheck passed")
    return 0


def check_required_files() -> List[str]:
    required = [
        "LICENSE",
        "README.md",
        "pyproject.toml",
        "leveraged_etp_risk_lab/__main__.py",
        "examples/fixtures/leveraged_nasdaq_3x.json",
        "examples/fixtures/single_stock_2x.json",
        "examples/fixtures/portfolio_manifest.json",
        "examples/fixtures/thesis_note.md",
        "examples/fixtures/factsheet_note.txt",
        "examples/fixtures/recipe_thesis_review.json",
        "examples/fixtures/product_snapshot_tqqq_case_study.json",
        "examples/outputs/pretrade_plan.json",
        "examples/outputs/pretrade_plan.md",
        "examples/outputs/position_size.json",
        "examples/outputs/position_size.md",
        "examples/outputs/stress_matrix.json",
        "examples/outputs/stress_matrix.md",
        "examples/outputs/sensitivity_grid.json",
        "examples/outputs/sensitivity_grid.md",
        "examples/outputs/portfolio_sensitivity.json",
        "examples/outputs/portfolio_sensitivity.md",
        "examples/outputs/compare_runs.json",
        "examples/outputs/compare_runs.md",
        "examples/outputs/run_ledger.jsonl",
        "examples/outputs/thesis_impact.json",
        "examples/outputs/thesis_impact.md",
        "examples/outputs/watchlist.json",
        "examples/outputs/watchlist.md",
        "examples/outputs/factsheet_check.json",
        "examples/outputs/factsheet_check.md",
        "examples/outputs/risk_profiles.json",
        "examples/outputs/risk_profiles.md",
        "examples/outputs/recipe_run.json",
        "examples/outputs/recipe_run.md",
        "examples/outputs/report_card.json",
        "examples/outputs/report_card.md",
        "examples/outputs/thesis_dashboard_data.json",
        "examples/outputs/thesis_dashboard_data.md",
        "examples/outputs/investment_memo.json",
        "examples/outputs/investment_memo.md",
        "examples/outputs/audit_trail.json",
        "examples/outputs/audit_trail.md",
        "examples/outputs/investment_memo_review.json",
        "examples/outputs/investment_memo_review.md",
        "examples/outputs/cycle_state.json",
        "examples/outputs/cycle_state.md",
        "examples/outputs/cycle_update.json",
        "examples/outputs/cycle_update.md",
        "examples/outputs/guardrail_policy.json",
        "examples/outputs/guardrail_policy.md",
        "examples/outputs/guardrail_check.json",
        "examples/outputs/guardrail_check.md",
        "examples/outputs/order_ticket.json",
        "examples/outputs/order_ticket.md",
        "examples/outputs/order_review.json",
        "examples/outputs/order_review.md",
        "examples/outputs/asset_hub.json",
        "examples/outputs/asset_hub.md",
        "examples/outputs/schema_inventory.json",
        "examples/outputs/schema_inventory.md",
        "examples/outputs/artifact_validation.json",
        "examples/outputs/artifact_validation.md",
        "examples/outputs/scenario_pack.json",
        "examples/outputs/scenario_pack.md",
        "examples/outputs/daily_reset_path_decay.json",
        "examples/outputs/daily_reset_path_decay.md",
        "examples/outputs/drawdown_risk.json",
        "examples/outputs/drawdown_risk.md",
        "examples/outputs/pretrade_guardrails.json",
        "examples/outputs/pretrade_guardrails.md",
        "examples/outputs/release_manifest.json",
        "examples/outputs/release_manifest.md",
        "examples/outputs/docs_export.html",
        "examples/outputs/docs_export.json",
        "examples/outputs/docs_export.md",
        "examples/outputs/demo_story.json",
        "examples/outputs/demo_story.md",
        "examples/outputs/package_audit.json",
        "examples/outputs/package_audit.md",
        "examples/outputs/glossary.json",
        "examples/outputs/glossary.md",
        "examples/outputs/product_snapshot_tqqq_case_study.json",
        "examples/outputs/product_snapshot_tqqq_case_study.md",
        "examples/outputs/product_family_walkthrough.json",
        "examples/outputs/product_family_walkthrough.md",
        "examples/outputs/gallery_index.json",
        "examples/outputs/gallery_index.md",
        "examples/outputs/dashboard.html",
        "examples/outputs/template_gallery.json",
        "examples/outputs/template_gallery.md",
        "examples/outputs/regime_gallery.json",
        "examples/outputs/regime_gallery.md",
        "examples/outputs/regime_trend_up.csv",
        "examples/outputs/regime_trend_down.csv",
        "examples/outputs/regime_chop.csv",
        "examples/outputs/regime_gap_down.csv",
        "examples/outputs/regime_rebound.csv",
        "examples/outputs/regime_volatility_cluster.csv",
        "docs/schema.md",
        "docs/pretrade-plan.schema.json",
        "docs/position-size.schema.json",
        "docs/stress-matrix.schema.json",
        "docs/sensitivity-grid.schema.json",
        "docs/portfolio-sensitivity.schema.json",
        "docs/template-gallery.schema.json",
        "docs/regime-gallery.schema.json",
        "docs/compare-runs.schema.json",
        "docs/run-ledger.schema.json",
        "docs/thesis-impact.schema.json",
        "docs/watchlist.schema.json",
        "docs/factsheet-check.schema.json",
        "docs/risk-profile.schema.json",
        "docs/recipe-run.schema.json",
        "docs/report-card.schema.json",
        "docs/thesis-dashboard-data.schema.json",
        "docs/audit-trail.schema.json",
        "docs/investment-memo.schema.json",
        "docs/investment-memo-review.schema.json",
        "docs/cycle-state.schema.json",
        "docs/cycle-update.schema.json",
        "docs/guardrail-policy.schema.json",
        "docs/guardrail-check.schema.json",
        "docs/order-ticket.schema.json",
        "docs/order-review.schema.json",
        "docs/asset-hub.schema.json",
        "docs/schema-inventory.schema.json",
        "docs/artifact-validation.schema.json",
        "docs/scenario-pack.schema.json",
        "docs/scenario-case-study.schema.json",
        "docs/release-manifest.schema.json",
        "docs/docs-export.schema.json",
        "docs/package-audit.schema.json",
        "docs/glossary.schema.json",
        "docs/product-snapshot-case-study.schema.json",
        "docs/product-family-walkthrough.schema.json",
        "docs/demo-story.schema.json",
        "docs/gallery-index.schema.json",
        "scripts/selfcheck.py",
        "scripts/sync_local_skill.py",
        "skills/agent/leveraged-etp-risk-lab/SKILL.md",
    ]
    return [f"missing required file: {path}" for path in required if not (ROOT / path).exists()]


def check_no_workflows() -> List[str]:
    workflows = ROOT / ".github" / "workflows"
    if workflows.exists() and any(workflows.iterdir()):
        return ["workflow files are not allowed for this repo"]
    return []


def check_public_hygiene() -> List[str]:
    failures: List[str] = []
    private_terms = ["Her" + "mes", "Fei" + "shu"]
    regexes = [
        re.compile("/" + "Users" + "/"),
        re.compile("/" + "home" + r"/[A-Za-z0-9_.-]+/"),
        re.compile("github" + "-assets"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"(?i)(api|secret|token)[_-]?key\s*[:=]\s*['\"][^'\"]+['\"]"),
    ]
    for path in public_text_files():
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for term in private_terms:
            if term in text:
                failures.append(f"private term in {rel}")
        for regex in regexes:
            if regex.search(text):
                failures.append(f"private pattern {regex.pattern!r} in {rel}")
    return failures


def check_no_runtime_dependencies() -> List[str]:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    if "dependencies = []" not in pyproject:
        return ["pyproject must declare an empty dependency list"]
    imported = set()
    for path in (ROOT / "leveraged_etp_risk_lab").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                imported.add(node.module.split(".")[0])
    allowed = {"__future__", "argparse", "csv", "dataclasses", "hashlib", "html", "json", "pathlib", "re", "subprocess", "sys", "typing"}
    extras = sorted(name for name in imported if name not in allowed and name != "leveraged_etp_risk_lab")
    return [f"unexpected runtime import: {name}" for name in extras]


def check_tests() -> List[str]:
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode:
        return ["unit tests failed:\n" + result.stdout]
    return []


def check_cli_smoke() -> List[str]:
    commands = [
        [sys.executable, "-m", "leveraged_etp_risk_lab", "version-report"],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "checklist"],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "exposure-report",
            "--manifest",
            "examples/fixtures/portfolio_manifest.json",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "pretrade-plan",
            "--product",
            "examples/fixtures/leveraged_nasdaq_3x.json",
            "--path",
            "examples/fixtures/nasdaq_chop_path.csv",
            "--thesis-file",
            "examples/fixtures/thesis_note.md",
            "--max-loss-budget",
            "750",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "compare-runs",
            "--base",
            "examples/outputs/leveraged_nasdaq_3x.json",
            "--candidate",
            "examples/outputs/single_stock_2x.json",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "position-size",
            "--pretrade-plan",
            "examples/outputs/pretrade_plan.json",
            "--account-value",
            "50000",
            "--max-loss-budget",
            "750",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "thesis-impact",
            "--thesis-file",
            "examples/fixtures/thesis_note.md",
            "--artifact",
            "examples/outputs/pretrade_plan.json",
            "--artifact",
            "examples/outputs/portfolio_exposure.json",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "stress-matrix",
            "--product",
            "examples/fixtures/leveraged_nasdaq_3x.json",
            "--regime",
            "trend_down",
            "--stop-loss",
            "0.15",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "sensitivity-grid",
            "--product",
            "examples/fixtures/leveraged_nasdaq_3x.json",
            "--stop-loss",
            "none,0.15",
            "--take-profit",
            "none,0.20",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "portfolio-sensitivity",
            "--manifest",
            "examples/fixtures/portfolio_manifest.json",
            "--stop-loss",
            "none,0.15",
            "--take-profit",
            "none,0.20",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "watchlist-build",
            "--thesis-impact",
            "examples/outputs/thesis_impact.json",
            "--stress-matrix",
            "examples/outputs/stress_matrix.json",
        ],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "template-list"],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "regime-list"],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "demo-story", "--input-dir", "examples/outputs"],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "gallery-index", "--input-dir", "examples/outputs"],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "asset-hub", "--input-dir", "examples/outputs"],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "schema-inventory"],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "artifact-validate"],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "scenario-pack",
            "--input-dir",
            "examples/outputs",
            "--fixtures-dir",
            "examples/fixtures",
            "--output-dir",
            "examples/outputs",
        ],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "release-manifest", "--no-git"],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "docs-export"],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "package-audit"],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "product-snapshot"],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "product-family-walkthrough"],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "glossary-list"],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "explain-term", "daily_reset"],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "factsheet-check",
            "--product",
            "examples/fixtures/leveraged_nasdaq_3x.json",
            "--factsheet-file",
            "examples/fixtures/factsheet_note.txt",
        ],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "risk-profile"],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "recipe-run",
            "--recipe",
            "examples/fixtures/recipe_thesis_review.json",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "report-card",
            "--artifact",
            "examples/outputs/pretrade_plan.json",
            "--artifact",
            "examples/outputs/position_size.json",
            "--artifact",
            "examples/outputs/stress_matrix.json",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "thesis-dashboard-data",
            "--recipe-run",
            "examples/outputs/recipe_run.json",
            "--report-card",
            "examples/outputs/report_card.json",
            "--watchlist",
            "examples/outputs/watchlist.json",
            "--sensitivity-grid",
            "examples/outputs/sensitivity_grid.json",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "memo-draft",
            "--recipe-run",
            "examples/outputs/recipe_run.json",
            "--thesis-dashboard-data",
            "examples/outputs/thesis_dashboard_data.json",
            "--report-card",
            "examples/outputs/report_card.json",
            "--factsheet-check",
            "examples/outputs/factsheet_check.json",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "memo-review",
            "--memo",
            "examples/outputs/investment_memo.json",
            "--report-card",
            "examples/outputs/report_card.json",
            "--watchlist",
            "examples/outputs/watchlist.json",
            "--audit-trail",
            "examples/outputs/audit_trail.json",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "cycle-init",
            "--memo",
            "examples/outputs/investment_memo.json",
            "--watchlist",
            "examples/outputs/watchlist.json",
            "--report-card",
            "examples/outputs/report_card.json",
            "--sensitivity-grid",
            "examples/outputs/sensitivity_grid.json",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "cycle-update",
            "--cycle-state",
            "examples/outputs/cycle_state.json",
            "--report-card",
            "examples/outputs/report_card.json",
            "--watchlist",
            "examples/outputs/watchlist.json",
            "--audit-trail",
            "examples/outputs/audit_trail.json",
        ],
        [sys.executable, "-m", "leveraged_etp_risk_lab", "guardrail-policy", "--policy", "default"],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "guardrail-check",
            "--policy",
            "examples/outputs/guardrail_policy.json",
            "--portfolio-sensitivity",
            "examples/outputs/portfolio_sensitivity.json",
            "--position-size",
            "examples/outputs/position_size.json",
            "--investment-memo",
            "examples/outputs/investment_memo.json",
            "--cycle-update",
            "examples/outputs/cycle_update.json",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "order-ticket",
            "--guardrail-check",
            "examples/outputs/guardrail_check.json",
            "--investment-memo",
            "examples/outputs/investment_memo.json",
            "--position-size",
            "examples/outputs/position_size.json",
            "--factsheet-check",
            "examples/outputs/factsheet_check.json",
            "--thesis-dashboard-data",
            "examples/outputs/thesis_dashboard_data.json",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "order-review",
            "--order-ticket",
            "examples/outputs/order_ticket.json",
            "--guardrail-check",
            "examples/outputs/guardrail_check.json",
            "--cycle-update",
            "examples/outputs/cycle_update.json",
            "--audit-trail",
            "examples/outputs/audit_trail.json",
        ],
        [
            sys.executable,
            "-m",
            "leveraged_etp_risk_lab",
            "audit-trail",
            "--ledger",
            "examples/outputs/run_ledger.jsonl",
            "--artifact",
            "examples/outputs/pretrade_plan.json",
            "--artifact",
            "examples/outputs/stress_matrix.json",
        ],
    ]
    failures = []
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if result.returncode:
            failures.append(f"command failed: {' '.join(command)}\n{result.stderr}")
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "leveraged_etp_risk_lab",
                "generate-scenario",
                "--kind",
                "trend",
                "--days",
                "3",
                "--output",
                str(Path(tmp) / "trend.csv"),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode:
            failures.append(f"generate-scenario smoke failed:\n{result.stderr}")
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "leveraged_etp_risk_lab",
                "static-dashboard",
                "--manifest",
                "examples/fixtures/portfolio_manifest.json",
                "--output",
                str(Path(tmp) / "dashboard.html"),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode:
            failures.append(f"static-dashboard smoke failed:\n{result.stderr}")
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "leveraged_etp_risk_lab",
                "template-export",
                "--template",
                "generic-2x-single-stock",
                "--output",
                str(Path(tmp) / "single_stock_template.json"),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode:
            failures.append(f"template-export smoke failed:\n{result.stderr}")
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "leveraged_etp_risk_lab",
                "regime-export",
                "--regime",
                "volatility_cluster",
                "--days",
                "4",
                "--output",
                str(Path(tmp) / "volatility_cluster.csv"),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode:
            failures.append(f"regime-export smoke failed:\n{result.stderr}")
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "leveraged_etp_risk_lab",
                "run-ledger",
                "--ledger",
                str(Path(tmp) / "ledger.jsonl"),
                "--artifact",
                "examples/outputs/leveraged_nasdaq_3x.json",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode:
            failures.append(f"run-ledger smoke failed:\n{result.stderr}")
        result = subprocess.run(
            [
                sys.executable,
                "scripts/sync_local_skill.py",
                "--target-dir",
                str(Path(tmp) / "local-skill"),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode:
            failures.append(f"sync-local-skill smoke failed:\n{result.stderr}")
        elif not (Path(tmp) / "local-skill" / "SKILL.md").exists():
            failures.append("sync-local-skill smoke did not write SKILL.md")
    return failures


def public_text_files() -> Iterable[Path]:
    skip_dirs = {".git", "__pycache__", ".pytest_cache", "build", "dist", "*.egg-info"}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [name for name in dirnames if name not in skip_dirs and not name.endswith(".egg-info")]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix in TEXT_SUFFIXES:
                yield path


if __name__ == "__main__":
    raise SystemExit(main())
