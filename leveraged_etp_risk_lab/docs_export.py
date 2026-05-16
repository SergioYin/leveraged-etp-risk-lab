from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


DOCS_EXPORT_SCHEMA_VERSION = "0.30"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_JSON = {
    "release_manifest": "release_manifest.json",
    "asset_hub": "asset_hub.json",
    "demo_story": "demo_story.json",
    "gallery_index": "gallery_index.json",
    "package_audit": "package_audit.json",
    "scenario_pack": "scenario_pack.json",
}
SKIP_MARKDOWN = {"docs_export.md"}


def docs_export(input_dir: str, title: str = "Leveraged ETP Risk Lab Documentation", root: Path = ROOT) -> Dict[str, Any]:
    source_root = Path(input_dir)
    if not source_root.is_absolute():
        source_root = root / source_root
    if not source_root.exists():
        raise FileNotFoundError(source_root)
    if not source_root.is_dir():
        raise ValueError(f"{input_dir} is not a directory")

    sources = {name: _load_source(source_root / filename, root) for name, filename in SOURCE_JSON.items()}
    present = {name: item["data"] for name, item in sources.items() if item["status"] == "present"}
    asset_hub = present.get("asset_hub") or {}
    release_manifest = present.get("release_manifest") or {}
    demo_story = present.get("demo_story") or {}
    gallery_index = present.get("gallery_index") or {}
    package_audit = present.get("package_audit") or {}
    scenario_pack = present.get("scenario_pack") or {}
    markdown_artifacts = _markdown_artifacts(source_root, root)
    command_map = _command_map(asset_hub, demo_story)
    safety = _safety_caveats(asset_hub, demo_story)
    release_notes = _release_notes(release_manifest)
    local_links = _local_links(gallery_index, markdown_artifacts)
    integration_notes = _integration_notes(scenario_pack)
    return {
        "schema_version": DOCS_EXPORT_SCHEMA_VERSION,
        "document_type": "docs_export",
        "title": title,
        "summary": {
            "source_artifacts": len(sources),
            "source_artifacts_present": sum(1 for item in sources.values() if item["status"] == "present"),
            "markdown_artifacts": len(markdown_artifacts),
            "commands": len(command_map),
            "local_links": len(local_links),
            "release_status": (release_manifest.get("release_readiness") or {}).get("status"),
            "package_ready": (package_audit.get("summary") or {}).get("ready"),
        },
        "sources": _source_summary(sources),
        "safety_caveats": safety,
        "command_map": command_map,
        "integration_notes": integration_notes,
        "release_notes": release_notes,
        "local_artifact_links": local_links,
        "markdown_artifacts": markdown_artifacts,
        "provenance": {
            "command": "docs-export",
            "input_dir": _display_path(source_root, root),
            "live_market_data": False,
            "external_assets": False,
            "javascript": False,
            "private_context": False,
            "workflow_files_read": False,
        },
    }


def docs_export_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        f"# {data['title']}",
        "",
        f"- Schema version: {data['schema_version']}",
        f"- Source artifacts: {summary['source_artifacts_present']}/{summary['source_artifacts']} present",
        f"- Markdown artifacts: {summary['markdown_artifacts']}",
        f"- Release status: {_display_value(summary['release_status'])}",
        f"- Package ready: {_yes_no(summary['package_ready'])}",
        "",
        "## Safety Caveats",
        "",
    ]
    lines.extend(f"- {item}" for item in data["safety_caveats"])
    lines.extend(["", "## Command Map", "", "| Command | Purpose | Example |", "| --- | --- | --- |"])
    for item in data["command_map"]:
        lines.append(f"| `{item['name']}` | {_md_cell(item['purpose'])} | `{_md_cell(item['example'])}` |")
    lines.extend(["", "## Integration Notes", "", "| System | Complement | Dependency Boundary |", "| --- | --- | --- |"])
    for item in data["integration_notes"]:
        lines.append(f"| `{item['target_system']}` | {_md_cell(item['complement'])} | {_md_cell(item['dependency_boundary'])} |")
    lines.extend(["", "## Release Notes", ""])
    if data["release_notes"]["markdown"]:
        lines.append(data["release_notes"]["markdown"].rstrip())
    else:
        lines.append("- No release notes source was available.")
    lines.extend(["", "## Local Artifact Links", "", "| Artifact | Type | Stage |", "| --- | --- | --- |"])
    for item in data["local_artifact_links"]:
        lines.append(f"| `{item['path']}` | {item['kind']} | {_display_value(item.get('stage'))} |")
    lines.extend(["", "## Markdown Artifacts", "", "| Artifact | Title | Bytes |", "| --- | --- | ---: |"])
    for item in data["markdown_artifacts"]:
        lines.append(f"| `{item['path']}` | {_md_cell(item['title'])} | {item['bytes']} |")
    lines.extend(["", "## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def docs_export_html(data: Dict[str, Any]) -> str:
    release_markdown = data["release_notes"]["markdown"].strip()
    html_parts = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{_e(data['title'])}</title>",
        "<style>",
        "body{margin:0;font:16px/1.5 Arial,Helvetica,sans-serif;color:#1f2933;background:#f7f7f2}",
        "main{max-width:1120px;margin:0 auto;padding:32px 20px 48px}",
        "header{border-bottom:3px solid #254d4d;padding-bottom:18px;margin-bottom:24px}",
        "h1{font-size:34px;line-height:1.15;margin:0 0 10px;color:#173f3f}",
        "h2{font-size:22px;margin:30px 0 10px;color:#263238}",
        "h3{font-size:17px;margin:18px 0 8px;color:#263238}",
        "p{margin:8px 0}",
        ".grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;margin:14px 0}",
        ".metric{border:1px solid #c7d2cc;background:#fff;padding:12px;border-radius:6px}",
        ".metric b{display:block;font-size:13px;color:#52615c;text-transform:uppercase}",
        ".metric span{font-size:20px;color:#173f3f}",
        "table{width:100%;border-collapse:collapse;background:#fff;margin:10px 0 18px}",
        "th,td{border:1px solid #d7ded9;padding:8px;vertical-align:top;text-align:left}",
        "th{background:#e9efeb;color:#263238}",
        "code{background:#eef1ee;padding:2px 4px;border-radius:4px}",
        "pre{white-space:pre-wrap;background:#fff;border:1px solid #d7ded9;padding:12px;overflow:auto}",
        "a{color:#175e63}",
        ".caveats{background:#fff7df;border:1px solid #d9bd72;padding:14px;border-radius:6px}",
        "footer{margin-top:32px;border-top:1px solid #c7d2cc;padding-top:14px;color:#52615c}",
        "</style>",
        "</head>",
        "<body>",
        "<main>",
        "<header>",
        f"<h1>{_e(data['title'])}</h1>",
        "<p>Self-contained static documentation export for checked local artifacts. No JavaScript, external assets, live data, broker execution, workflows, or private context are required.</p>",
        "</header>",
        _summary_html(data["summary"]),
        "<section><h2>Safety Caveats</h2><div class=\"caveats\"><ul>",
    ]
    html_parts.extend(f"<li>{_e(item)}</li>" for item in data["safety_caveats"])
    html_parts.extend(["</ul></div></section>", "<section><h2>Command Map</h2>", _table_html(data["command_map"], ["name", "purpose", "example"]), "</section>"])
    html_parts.extend(
        [
            "<section><h2>Integration Notes</h2>",
            _table_html(data["integration_notes"], ["target_system", "complement", "dependency_boundary"]),
            "</section>",
        ]
    )
    html_parts.extend(["<section><h2>Release Notes</h2>", f"<pre>{_e(release_markdown or 'No release notes source was available.')}</pre>", "</section>"])
    html_parts.extend(["<section><h2>Local Artifact Links</h2>", _artifact_links_html(data["local_artifact_links"]), "</section>"])
    html_parts.extend(["<section><h2>Markdown Artifacts</h2>", _table_html(data["markdown_artifacts"], ["path", "title", "bytes"]), "</section>"])
    html_parts.extend(["<section><h2>Source Artifacts</h2>", _table_html(data["sources"], ["name", "status", "path", "document_type", "schema_version"]), "</section>"])
    html_parts.extend(
        [
            "<footer>",
            f"<p>Generated by <code>{_e(data['provenance']['command'])}</code> from <code>{_e(data['provenance']['input_dir'])}</code>.</p>",
            "<p>Provenance flags: live_market_data=false, external_assets=false, javascript=false, private_context=false, workflow_files_read=false.</p>",
            "</footer>",
            "</main>",
            "</body>",
            "</html>",
            "",
        ]
    )
    return "\n".join(html_parts)


def _load_source(path: Path, root: Path) -> Dict[str, Any]:
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


def _source_summary(sources: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for name in sorted(sources):
        item = sources[name]
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


def _markdown_artifacts(source_root: Path, root: Path) -> List[Dict[str, Any]]:
    rows = []
    for path in sorted(source_root.glob("*.md")):
        if path.name in SKIP_MARKDOWN:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            text = ""
        rows.append(
            {
                "path": _display_path(path, root),
                "title": _markdown_title(text, path.stem.replace("_", " ").title()),
                "bytes": path.stat().st_size,
            }
        )
    return rows


def _markdown_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or fallback
    return fallback


def _command_map(asset_hub: Dict[str, Any], demo_story: Dict[str, Any]) -> List[Dict[str, str]]:
    source = asset_hub.get("command_map")
    if not isinstance(source, list):
        sections = demo_story.get("sections") if isinstance(demo_story, dict) else {}
        source = (sections or {}).get("commands", [])
    rows = []
    seen = set()
    for item in source:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or item.get("command") or "unknown")
        if name in seen:
            continue
        seen.add(name)
        rows.append(
            {
                "name": name,
                "purpose": str(item.get("purpose") or item.get("description") or ""),
                "example": str(item.get("example") or item.get("command") or ""),
            }
        )
    return rows


def _safety_caveats(asset_hub: Dict[str, Any], demo_story: Dict[str, Any]) -> List[str]:
    values: List[str] = []
    for item in [asset_hub.get("not_investment_advice"), demo_story.get("not_investment_advice")]:
        if isinstance(item, str) and item and item not in values:
            values.append(item)
    for source in [asset_hub.get("safety_boundaries"), demo_story.get("safety_caveats")]:
        if isinstance(source, list):
            for item in source:
                text = str(item)
                if text and text not in values:
                    values.append(text)
    defaults = [
        "This documentation is for deterministic scenario planning and education only.",
        "It is not investment advice, a recommendation, broker instruction, or suitability determination.",
        "The export is static HTML with no JavaScript, no external assets, no live market data, no workflow reads, and no private context.",
    ]
    for item in defaults:
        if item not in values:
            values.append(item)
    return values


def _release_notes(release_manifest: Dict[str, Any]) -> Dict[str, str]:
    notes = release_manifest.get("github_release_notes_draft") if isinstance(release_manifest, dict) else {}
    if not isinstance(notes, dict):
        notes = {}
    return {
        "title": str(notes.get("title") or ""),
        "markdown": str(notes.get("markdown") or ""),
    }


def _integration_notes(scenario_pack: Dict[str, Any]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    source = scenario_pack.get("integration_notes") if isinstance(scenario_pack, dict) else []
    if isinstance(source, list):
        for item in source:
            if not isinstance(item, dict):
                continue
            rows.append(
                {
                    "target_system": str(item.get("target_system") or ""),
                    "complement": str(item.get("complement") or ""),
                    "dependency_boundary": str(item.get("dependency_boundary") or ""),
                    "public_context": str(item.get("public_context") or ""),
                }
            )
    return rows


def _local_links(gallery_index: Dict[str, Any], markdown_artifacts: List[Dict[str, Any]]) -> List[Dict[str, Optional[str]]]:
    rows: List[Dict[str, Optional[str]]] = []
    seen = set()
    for stage in gallery_index.get("stages", []) if isinstance(gallery_index, dict) else []:
        if not isinstance(stage, dict):
            continue
        stage_name = str(stage.get("stage") or "")
        for item in stage.get("artifacts", []):
            if not isinstance(item, dict):
                continue
            path = str(item.get("path") or "")
            if not path or path in seen:
                continue
            rows.append({"path": path, "kind": str(item.get("format") or "artifact"), "stage": stage_name})
            seen.add(path)
    for item in markdown_artifacts:
        path = item["path"]
        if path not in seen:
            rows.append({"path": path, "kind": "markdown", "stage": "markdown"})
            seen.add(path)
    return rows


def _summary_html(summary: Dict[str, Any]) -> str:
    metrics = [
        ("Sources", f"{summary['source_artifacts_present']}/{summary['source_artifacts']}"),
        ("Markdown", summary["markdown_artifacts"]),
        ("Commands", summary["commands"]),
        ("Links", summary["local_links"]),
        ("Release", _display_value(summary.get("release_status"))),
        ("Package Ready", _yes_no(summary.get("package_ready"))),
    ]
    parts = ["<section><h2>Summary</h2><div class=\"grid\">"]
    for label, value in metrics:
        parts.append(f"<div class=\"metric\"><b>{_e(str(label))}</b><span>{_e(str(value))}</span></div>")
    parts.append("</div></section>")
    return "\n".join(parts)


def _artifact_links_html(rows: List[Dict[str, Optional[str]]]) -> str:
    parts = ["<table><thead><tr><th>Artifact</th><th>Type</th><th>Stage</th></tr></thead><tbody>"]
    for item in rows:
        path = str(item.get("path") or "")
        parts.append(
            "<tr>"
            f"<td><a href=\"{_attr(path)}\">{_e(path)}</a></td>"
            f"<td>{_e(str(item.get('kind') or 'artifact'))}</td>"
            f"<td>{_e(str(item.get('stage') or 'n/a'))}</td>"
            "</tr>"
        )
    parts.append("</tbody></table>")
    return "\n".join(parts)


def _table_html(rows: List[Dict[str, Any]], keys: List[str]) -> str:
    parts = ["<table><thead><tr>"]
    parts.extend(f"<th>{_e(key.replace('_', ' ').title())}</th>" for key in keys)
    parts.append("</tr></thead><tbody>")
    for row in rows:
        parts.append("<tr>")
        for key in keys:
            parts.append(f"<td>{_e(_display_value(row.get(key)))}</td>")
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "\n".join(parts)


def _display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.name


def _display_value(value: Any) -> str:
    if value is None:
        return "n/a"
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)


def _yes_no(value: Any) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return "unknown"


def _md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def _e(value: str) -> str:
    return html.escape(value, quote=False)


def _attr(value: str) -> str:
    return html.escape(value, quote=True)
