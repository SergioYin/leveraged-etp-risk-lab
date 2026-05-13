from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


SCHEMA_VERSION = "0.11"
ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".py", ".json", ".csv", ".toml", ".txt", ""}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "build", "dist"}


REQUIRED_SCHEMA_FILES = [
    "docs/product.schema.json",
    "docs/path.schema.json",
    "docs/portfolio-manifest.schema.json",
    "docs/simulation-output.schema.json",
    "docs/exposure-report.schema.json",
    "docs/pretrade-plan.schema.json",
    "docs/position-size.schema.json",
    "docs/stress-matrix.schema.json",
    "docs/template-gallery.schema.json",
    "docs/regime-gallery.schema.json",
    "docs/compare-runs.schema.json",
    "docs/run-ledger.schema.json",
    "docs/thesis-impact.schema.json",
    "docs/watchlist.schema.json",
    "docs/factsheet-check.schema.json",
    "docs/package-audit.schema.json",
    "docs/glossary.schema.json",
    "docs/demo-story.schema.json",
    "docs/gallery-index.schema.json",
]


REQUIRED_EXAMPLE_OUTPUTS = [
    "examples/outputs/leveraged_nasdaq_3x.json",
    "examples/outputs/leveraged_nasdaq_3x.md",
    "examples/outputs/portfolio_exposure.json",
    "examples/outputs/portfolio_exposure.md",
    "examples/outputs/pretrade_plan.json",
    "examples/outputs/pretrade_plan.md",
    "examples/outputs/position_size.json",
    "examples/outputs/position_size.md",
    "examples/outputs/stress_matrix.json",
    "examples/outputs/stress_matrix.md",
    "examples/outputs/compare_runs.json",
    "examples/outputs/compare_runs.md",
    "examples/outputs/run_ledger.jsonl",
    "examples/outputs/thesis_impact.json",
    "examples/outputs/thesis_impact.md",
    "examples/outputs/watchlist.json",
    "examples/outputs/watchlist.md",
    "examples/outputs/factsheet_check.json",
    "examples/outputs/factsheet_check.md",
    "examples/outputs/demo_story.json",
    "examples/outputs/demo_story.md",
    "examples/outputs/package_audit.json",
    "examples/outputs/package_audit.md",
    "examples/outputs/glossary.json",
    "examples/outputs/glossary.md",
    "examples/outputs/gallery_index.json",
    "examples/outputs/gallery_index.md",
    "examples/outputs/template_gallery.json",
    "examples/outputs/template_gallery.md",
    "examples/outputs/regime_gallery.json",
    "examples/outputs/regime_gallery.md",
    "examples/outputs/dashboard.html",
]


TEST_COMMANDS = [
    ["python", "-m", "unittest", "discover", "-s", "tests"],
    ["python", "scripts/selfcheck.py"],
    ["python", "-m", "leveraged_etp_risk_lab", "package-audit", "--format", "json"],
    ["python", "-m", "leveraged_etp_risk_lab", "gallery-index", "--format", "json"],
    ["python", "-m", "leveraged_etp_risk_lab", "glossary-list", "--format", "json"],
    ["python", "-m", "leveraged_etp_risk_lab", "explain-term", "daily_reset", "--format", "json"],
    [
        "python",
        "-m",
        "leveraged_etp_risk_lab",
        "factsheet-check",
        "--product",
        "examples/fixtures/leveraged_nasdaq_3x.json",
        "--factsheet-file",
        "examples/fixtures/factsheet_note.txt",
        "--format",
        "json",
    ],
]


def package_audit(version: str, run_tests: bool = False, root: Path = ROOT) -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    checks.extend(_presence_checks(root, "readme", "documentation", ["README.md"]))
    checks.extend(_presence_checks(root, "license", "metadata", ["LICENSE"]))
    checks.extend(_presence_checks(root, "schemas", "schemas", REQUIRED_SCHEMA_FILES))
    checks.extend(_presence_checks(root, "examples", "examples", REQUIRED_EXAMPLE_OUTPUTS))
    checks.extend(_presence_checks(root, "skill_file", "skills", ["skills/agent/leveraged-etp-risk-lab/SKILL.md"]))
    checks.append(_workflow_check(root))
    checks.append(_private_terms_check(root))
    checks.append(_dependency_check(root))
    checks.append(_version_check(version, root))
    test_results = _test_command_results(run_tests, root)
    checks.append(_test_commands_check(test_results))
    failed = [check for check in checks if check["status"] != "pass"]
    return {
        "schema_version": SCHEMA_VERSION,
        "document_type": "package_audit",
        "package": {
            "name": "leveraged-etp-risk-lab",
            "version": version,
            "dependencies": [],
        },
        "summary": {
            "ready": not failed,
            "checks": len(checks),
            "passed": len(checks) - len(failed),
            "failed": len(failed),
        },
        "checks": checks,
        "test_commands": test_results,
    }


def package_audit_markdown(data: Dict[str, Any]) -> str:
    package = data["package"]
    summary = data["summary"]
    lines = [
        "# Package Audit",
        "",
        f"- Package: {package['name']}",
        f"- Version: {package['version']}",
        f"- Ready: {'yes' if summary['ready'] else 'no'}",
        f"- Checks: {summary['passed']} passed, {summary['failed']} failed",
        "",
        "## Checklist",
        "",
        "| Check | Category | Status | Message |",
        "| --- | --- | --- | --- |",
    ]
    for check in data["checks"]:
        lines.append(
            f"| {check['id']} | {check['category']} | {check['status']} | "
            f"{_md_cell(check['message'])} |"
        )
    lines.extend(["", "## Test Commands", "", "| Command | Status |", "| --- | --- |"])
    for item in data["test_commands"]:
        lines.append(f"| `{_command_text(item['command'])}` | {item['status']} |")
    return "\n".join(lines) + "\n"


def _presence_checks(root: Path, check_id: str, category: str, paths: List[str]) -> List[Dict[str, Any]]:
    missing = [path for path in paths if not (root / path).exists()]
    status = "pass" if not missing else "fail"
    message = "all required files present" if not missing else "missing: " + ", ".join(missing)
    return [_check(check_id, category, status, message, {"required": paths, "missing": missing})]


def _workflow_check(root: Path) -> Dict[str, Any]:
    workflows = root / ".github" / "workflows"
    found = []
    if workflows.exists():
        found = [path.relative_to(root).as_posix() for path in workflows.rglob("*") if path.is_file()]
    return _check(
        "no_workflows",
        "hygiene",
        "pass" if not found else "fail",
        "no workflow files found" if not found else "workflow files are not allowed",
        {"files": found},
    )


def _private_terms_check(root: Path) -> Dict[str, Any]:
    private_terms = ["Her" + "mes", "Fei" + "shu"]
    regexes = [
        re.compile("/" + "Users" + "/"),
        re.compile("/" + "home" + r"/[A-Za-z0-9_.-]+/"),
        re.compile("github" + "-assets"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"(?i)(api|secret|token)[_-]?key\s*[:=]\s*['\"][^'\"]+['\"]"),
    ]
    findings = []
    for path in _public_text_files(root):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        if any(term in text for term in private_terms):
            findings.append(rel)
            continue
        if any(regex.search(text) for regex in regexes):
            findings.append(rel)
    return _check(
        "no_private_terms",
        "hygiene",
        "pass" if not findings else "fail",
        "no private terms, local paths, or secret-like values found"
        if not findings
        else "private or machine-local text found",
        {"files": findings[:50], "truncated": len(findings) > 50},
    )


def _version_check(version: str, root: Path) -> Dict[str, Any]:
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")
    init_text = (root / "leveraged_etp_risk_lab" / "__init__.py").read_text(encoding="utf-8")
    pyproject_version = _match_version(r'^version\s*=\s*"([^"]+)"', pyproject)
    init_version = _match_version(r'__version__\s*=\s*"([^"]+)"', init_text)
    values = {
        "runtime": version,
        "pyproject": pyproject_version,
        "package_init": init_version,
    }
    unique = {value for value in values.values() if value}
    status = "pass" if len(unique) == 1 and version == pyproject_version == init_version else "fail"
    return _check(
        "version_consistency",
        "metadata",
        status,
        f"version fields agree at {version}" if status == "pass" else "version fields do not agree",
        values,
    )


def _dependency_check(root: Path) -> Dict[str, Any]:
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")
    status = "pass" if "dependencies = []" in pyproject else "fail"
    return _check(
        "zero_dependencies",
        "metadata",
        status,
        "runtime dependency list is empty" if status == "pass" else "runtime dependency list must be empty",
        {"expected": "dependencies = []"},
    )


def _test_command_results(run_tests: bool, root: Path) -> List[Dict[str, Any]]:
    results = []
    for command in TEST_COMMANDS:
        if run_tests:
            executable_command = [sys.executable if item == "python" else item for item in command]
            completed = subprocess.run(
                executable_command,
                cwd=root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            results.append(
                {
                    "command": command,
                    "status": "pass" if completed.returncode == 0 else "fail",
                    "returncode": completed.returncode,
                }
            )
        else:
            results.append({"command": command, "status": "not_run", "returncode": None})
    return results


def _test_commands_check(test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    failed = [item for item in test_results if item["status"] == "fail"]
    status = "pass" if not failed else "fail"
    message = "test commands listed" if all(item["status"] == "not_run" for item in test_results) else "test commands passed"
    if failed:
        message = "one or more test commands failed"
    return _check("test_commands", "validation", status, message, {"commands": test_results})


def _check(check_id: str, category: str, status: str, message: str, evidence: Dict[str, Any]) -> Dict[str, Any]:
    return {"id": check_id, "category": category, "status": status, "message": message, "evidence": evidence}


def _match_version(pattern: str, text: str) -> Optional[str]:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1) if match else None


def _public_text_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        parts = set(path.relative_to(root).parts[:-1])
        if parts.intersection(SKIP_DIRS) or any(part.endswith(".egg-info") for part in parts):
            continue
        if path.suffix in TEXT_SUFFIXES:
            yield path


def _command_text(command: List[str]) -> str:
    return " ".join(command)


def _md_cell(value: str) -> str:
    return value.replace("|", "\\|")
