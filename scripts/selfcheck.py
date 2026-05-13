#!/usr/bin/env python3
from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
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
        "docs/schema.md",
        "scripts/selfcheck.py",
        "skills/agent/leveraged-etp-risk-lab/SKILL.md",
    ]
    return [f"missing required file: {path}" for path in required if not (ROOT / path).exists()]


def check_no_workflows() -> List[str]:
    workflows = ROOT / ".github" / "workflows"
    if workflows.exists() and any(workflows.iterdir()):
        return ["workflow files are not allowed for this v0.1 repo"]
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
    allowed = {"__future__", "argparse", "csv", "dataclasses", "json", "pathlib", "subprocess", "sys", "typing"}
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
    ]
    failures = []
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if result.returncode:
            failures.append(f"command failed: {' '.join(command)}\n{result.stderr}")
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
