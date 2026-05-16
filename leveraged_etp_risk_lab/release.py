from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


RELEASE_MANIFEST_SCHEMA_VERSION = "0.30"
ROOT = Path(__file__).resolve().parents[1]
EXPECTED_INPUTS = {
    "asset_hub": "asset_hub.json",
    "package_audit": "package_audit.json",
    "artifact_validation": "artifact_validation.json",
    "schema_inventory": "schema_inventory.json",
    "demo_story": "demo_story.json",
    "gallery_index": "gallery_index.json",
}
AGENT_SKILL_PATH = "skills/agent/leveraged-etp-risk-lab/SKILL.md"


def release_manifest(input_dir: str, version: str, include_git: bool = True, root: Path = ROOT) -> Dict[str, Any]:
    source_root = Path(input_dir)
    if not source_root.is_absolute():
        source_root = root / source_root
    inputs = {name: _optional_artifact(source_root / filename, root) for name, filename in EXPECTED_INPUTS.items()}
    loaded = {name: item["data"] for name, item in inputs.items() if item.get("status") == "present"}
    inventory = _public_artifact_inventory(loaded.get("gallery_index"), loaded.get("asset_hub"))
    validation = _validation_summary(loaded.get("package_audit"), loaded.get("artifact_validation"), loaded.get("schema_inventory"))
    readiness = _release_readiness(inputs, validation)
    git = _git_metadata(root) if include_git else _git_unavailable("disabled")
    notes = _github_release_notes(version, inventory, validation, readiness)
    checklist = _post_release_checklist(version)
    sync = _skill_sync_recommendation(root)
    return {
        "schema_version": RELEASE_MANIFEST_SCHEMA_VERSION,
        "document_type": "release_manifest",
        "version": version,
        "inputs": _input_summary(inputs),
        "git": git,
        "public_artifact_inventory": inventory,
        "validation_summary": validation,
        "release_readiness": readiness,
        "agent_skill_path": AGENT_SKILL_PATH,
        "local_skill_sync_recommendation": sync,
        "github_release_notes_draft": notes,
        "post_release_verification_checklist": checklist,
        "provenance": {
            "command": "release-manifest",
            "input_dir": _display_path(source_root, root),
            "live_market_data": False,
            "private_context": False,
            "workflow_files_read": False,
        },
    }


def release_manifest_markdown(data: Dict[str, Any]) -> str:
    readiness = data["release_readiness"]
    validation = data["validation_summary"]
    lines = [
        "# Release Manifest",
        "",
        f"- Version: {data['version']}",
        f"- Status: {readiness['status']}",
        f"- Agent skill: `{data['agent_skill_path']}`",
        f"- Local skill sync: {data['local_skill_sync_recommendation']['recommendation']}",
        "",
        "## Inputs",
        "",
        "| Input | Status | Path | Document type |",
        "| --- | --- | --- | --- |",
    ]
    for item in data["inputs"]:
        lines.append(f"| {item['name']} | {item['status']} | {item['path']} | {item.get('document_type') or 'n/a'} |")
    lines.extend(
        [
            "",
            "## Public Artifact Inventory",
            "",
            f"- Total artifacts: {data['public_artifact_inventory']['total_artifacts']}",
            f"- Total bytes: {data['public_artifact_inventory']['total_bytes']}",
            "",
            "| Stage | Artifacts | Key artifacts |",
            "| --- | ---: | --- |",
        ]
    )
    for stage in data["public_artifact_inventory"]["stages"]:
        lines.append(f"| {stage['stage']} | {stage['artifact_count']} | {', '.join(stage['key_artifacts']) or 'None'} |")
    lines.extend(
        [
            "",
            "## Validation Summary",
            "",
            f"- Package ready: {_yes_no(validation['package_ready'])}",
            f"- Artifact validation ready: {_yes_no(validation['artifact_validation_ready'])}",
            f"- Schemas indexed: {validation['schemas_indexed']}",
            f"- Validation issues: {validation['issues']}",
            "",
            "## Release Readiness",
            "",
        ]
    )
    for item in readiness["checks"]:
        lines.append(f"- {item['status']}: {item['item']}")
    lines.extend(["", "## GitHub Release Notes Draft", "", data["github_release_notes_draft"]["markdown"].rstrip(), "", "## Post-Release Verification"])
    for item in data["post_release_verification_checklist"]:
        lines.append(f"- [{item['status']}] {item['item']}")
    return "\n".join(lines) + "\n"


def _optional_artifact(path: Path, root: Path) -> Dict[str, Any]:
    rel = _display_path(path, root)
    if not path.exists():
        return {"path": rel, "status": "missing", "data": None, "error": None}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {"path": rel, "status": "invalid", "data": None, "error": str(exc)}
    if not isinstance(data, dict):
        return {"path": rel, "status": "invalid", "data": None, "error": "artifact is not a JSON object"}
    return {"path": rel, "status": "present", "data": data, "error": None}


def _input_summary(inputs: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for name in sorted(inputs):
        item = inputs[name]
        data = item.get("data") or {}
        rows.append(
            {
                "name": name,
                "path": item["path"],
                "status": item["status"],
                "document_type": data.get("document_type"),
                "schema_version": data.get("schema_version"),
                "error": item.get("error"),
            }
        )
    return rows


def _public_artifact_inventory(gallery: Optional[Dict[str, Any]], asset_hub: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if isinstance(gallery, dict):
        summary = gallery.get("summary", {})
        stages = [
            {
                "stage": stage.get("stage", "unknown"),
                "artifact_count": int(stage.get("artifact_count", len(stage.get("artifacts", [])))),
                "key_artifacts": [str(item.get("filename") or item.get("path")) for item in stage.get("artifacts", [])[:5]],
                "suggested_next_command": str(stage.get("suggested_next_command", "")),
            }
            for stage in gallery.get("stages", [])
        ]
        return {
            "source": "gallery_index",
            "total_artifacts": int(summary.get("artifacts", sum(item["artifact_count"] for item in stages))),
            "total_bytes": int(summary.get("bytes", summary.get("total_bytes", 0)) or 0),
            "stages": stages,
        }
    if isinstance(asset_hub, dict):
        stages = [
            {
                "stage": item.get("stage", "unknown"),
                "artifact_count": int(item.get("artifact_count", 0)),
                "key_artifacts": [str(value) for value in item.get("key_artifacts", [])],
                "suggested_next_command": str(item.get("suggested_next_command", "")),
            }
            for item in asset_hub.get("demo_artifact_map", [])
        ]
        return {
            "source": "asset_hub",
            "total_artifacts": sum(item["artifact_count"] for item in stages),
            "total_bytes": 0,
            "stages": stages,
        }
    return {"source": "none", "total_artifacts": 0, "total_bytes": 0, "stages": []}


def _validation_summary(
    package_audit: Optional[Dict[str, Any]],
    artifact_validation: Optional[Dict[str, Any]],
    schema_inventory: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    package_summary = package_audit.get("summary", {}) if isinstance(package_audit, dict) else {}
    artifact_summary = artifact_validation.get("summary", {}) if isinstance(artifact_validation, dict) else {}
    schema_summary = schema_inventory.get("summary", {}) if isinstance(schema_inventory, dict) else {}
    issues = int(package_summary.get("failed", 0) or 0) + int(artifact_summary.get("failed", 0) or 0)
    return {
        "package_ready": package_summary.get("ready") if package_summary else None,
        "package_checks": int(package_summary.get("checks", 0) or 0),
        "package_failed": int(package_summary.get("failed", 0) or 0),
        "artifact_validation_ready": artifact_summary.get("ready") if artifact_summary else None,
        "artifacts_validated": int(artifact_summary.get("artifacts", 0) or 0),
        "artifact_validation_failed": int(artifact_summary.get("failed", 0) or 0),
        "schemas_indexed": int(schema_summary.get("schemas", 0) or 0),
        "schema_examples": int(schema_summary.get("examples", 0) or 0),
        "issues": issues,
    }


def _release_readiness(inputs: Dict[str, Dict[str, Any]], validation: Dict[str, Any]) -> Dict[str, Any]:
    checks = []
    missing = [name for name, item in sorted(inputs.items()) if item["status"] != "present"]
    checks.append(_readiness_check("source_artifacts", "All release source artifacts are present", "pass" if not missing else "review", missing))
    package_ready = validation["package_ready"]
    checks.append(_readiness_check("package_audit", "Package audit is ready", "pass" if package_ready is True else "review", []))
    artifact_ready = validation["artifact_validation_ready"]
    checks.append(_readiness_check("artifact_validation", "Artifact validation is ready", "pass" if artifact_ready is True else "review", []))
    checks.append(
        _readiness_check(
            "public_inventory",
            "Public artifact inventory is populated",
            "pass" if validation["artifacts_validated"] > 0 or not missing else "review",
            [],
        )
    )
    checks.append(_readiness_check("safety_boundaries", "No live data, workflow, or private context is required", "pass", []))
    blockers = [item for item in checks if item["status"] == "block"]
    reviews = [item for item in checks if item["status"] == "review"]
    status = "blocked" if blockers else "review" if reviews else "ready"
    return {"status": status, "checks": checks}


def _readiness_check(check_id: str, item: str, status: str, missing_inputs: List[str]) -> Dict[str, Any]:
    return {"id": check_id, "item": item, "status": status, "missing_inputs": missing_inputs}


def _git_metadata(root: Path) -> Dict[str, Any]:
    inside = _git(["rev-parse", "--is-inside-work-tree"], root)
    if inside is None or inside.strip() != "true":
        return _git_unavailable("not_a_git_worktree")
    return {
        "available": True,
        "status": "present",
        "commit": _git(["rev-parse", "HEAD"], root),
        "short_commit": _git(["rev-parse", "--short", "HEAD"], root),
        "branch": _git(["branch", "--show-current"], root) or None,
        "dirty": bool(_git(["status", "--porcelain"], root)),
    }


def _git_unavailable(reason: str) -> Dict[str, Any]:
    return {"available": False, "status": reason, "commit": None, "short_commit": None, "branch": None, "dirty": None}


def _git(args: List[str], root: Path) -> Optional[str]:
    try:
        completed = subprocess.run(["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False)
    except (OSError, FileNotFoundError):
        return None
    if completed.returncode:
        return None
    return completed.stdout.strip()


def _github_release_notes(version: str, inventory: Dict[str, Any], validation: Dict[str, Any], readiness: Dict[str, Any]) -> Dict[str, str]:
    title = f"v{version}"
    body = [
        f"## {title}",
        "",
        "### Highlights",
        "",
        "- Hardens deterministic release artifact generation for package audit, schema inventory, artifact validation, release manifest, and docs export.",
        "- Adds deterministic v0.30 scenario-pack case studies for new users comparing path decay, drawdown risk, and guardrails.",
        "- Carries safety caveats, command map, release notes, and local artifact links from checked public artifacts.",
        f"- Publishes {inventory['total_artifacts']} public demo artifacts across {len(inventory['stages'])} gallery stages.",
        f"- Tracks {validation['schemas_indexed']} local schemas and {validation['artifacts_validated']} validated artifacts.",
        "",
        "### Readiness",
        "",
        f"- Release status: {readiness['status']}",
        f"- Package audit ready: {_yes_no(validation['package_ready'])}",
        f"- Artifact validation ready: {_yes_no(validation['artifact_validation_ready'])}",
        "",
        "### Verification",
        "",
        "- `python -m unittest discover -s tests`",
        "- `python scripts/selfcheck.py`",
        "- `python -m leveraged_etp_risk_lab docs-export --input-dir examples/outputs --output examples/outputs/docs_export.html`",
        "- `python -m leveraged_etp_risk_lab package-audit --run-tests --format json`",
    ]
    return {"title": title, "markdown": "\n".join(body) + "\n"}


def _post_release_checklist(version: str) -> List[Dict[str, str]]:
    return [
        {"id": "tag", "item": f"Confirm release tag v{version} points at the intended commit.", "status": "todo"},
        {"id": "artifacts", "item": "Confirm JSON and Markdown release_manifest artifacts are attached or linked.", "status": "todo"},
        {"id": "schema", "item": "Confirm docs/release-manifest.schema.json and docs/docs-export.schema.json are visible in the published package.", "status": "todo"},
        {"id": "skill", "item": "Run scripts/sync_local_skill.py when a local Codex skill copy should be refreshed.", "status": "todo"},
        {"id": "smoke", "item": "Run version-report, release-manifest, artifact-validate, and package-audit from a clean checkout.", "status": "todo"},
    ]


def _skill_sync_recommendation(root: Path) -> Dict[str, str]:
    status = "available" if (root / AGENT_SKILL_PATH).exists() else "missing"
    return {
        "status": status,
        "source": AGENT_SKILL_PATH,
        "command": "python scripts/sync_local_skill.py",
        "recommendation": "sync after release if you use the local Codex skill copy" if status == "available" else "restore the checked-in skill before syncing",
    }


def _display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.name


def _yes_no(value: Any) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return "unknown"
