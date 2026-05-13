from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


COMPARE_SCHEMA_VERSION = "0.5"
LEDGER_SCHEMA_VERSION = "0.5"
THESIS_IMPACT_SCHEMA_VERSION = "0.6"
WATCHLIST_SCHEMA_VERSION = "0.10"
GALLERY_INDEX_SCHEMA_VERSION = "0.13"
COMPARABLE_REPORT_TYPES = {"simulation_output", "pretrade_plan", "exposure_report"}
GALLERY_STAGE_ORDER = [
    "fixtures",
    "plans",
    "sizing",
    "stress",
    "thesis/watchlist",
    "audit/story",
    "dashboard",
]


def load_json_report(path: str) -> Dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a JSON object")
    return data


def compare_reports(base_path: str, candidate_path: str) -> Dict[str, Any]:
    base = load_json_report(base_path)
    candidate = load_json_report(candidate_path)
    base_summary = summarize_report(base)
    candidate_summary = summarize_report(candidate)
    for side, summary in [("base", base_summary), ("candidate", candidate_summary)]:
        if summary["document_type"] not in COMPARABLE_REPORT_TYPES:
            raise ValueError(f"{side} is not a supported simulation, pretrade, or exposure JSON output")
    warning_delta = _warning_delta(base_summary["warnings"], candidate_summary["warnings"])
    return {
        "schema_version": COMPARE_SCHEMA_VERSION,
        "document_type": "run_comparison",
        "inputs": {
            "base": _display_path(base_path),
            "candidate": _display_path(candidate_path),
        },
        "base": _comparison_side(base_summary),
        "candidate": _comparison_side(candidate_summary),
        "deltas": {
            "return_pct": _numeric_delta(base_summary["metrics"]["return_pct"], candidate_summary["metrics"]["return_pct"]),
            "path_decay_vs_simple_multiple": _numeric_delta(
                base_summary["metrics"]["path_decay_vs_simple_multiple"],
                candidate_summary["metrics"]["path_decay_vs_simple_multiple"],
            ),
            "weighted_exposure": _numeric_delta(
                base_summary["metrics"]["weighted_exposure"],
                candidate_summary["metrics"]["weighted_exposure"],
            ),
            "warnings": warning_delta,
        },
    }


def summarize_report(data: Dict[str, Any]) -> Dict[str, Any]:
    kind = detect_report_type(data)
    metrics = {
        "return_pct": None,
        "path_decay_vs_simple_multiple": None,
        "weighted_exposure": None,
    }
    label = kind
    if kind == "simulation_output":
        product = data.get("product", {})
        summary = data.get("summary", {})
        label = str(product.get("ticker") or product.get("name") or kind)
        metrics["return_pct"] = _optional_number(summary.get("etp_return_pct"))
        metrics["path_decay_vs_simple_multiple"] = _optional_number(summary.get("path_decay_vs_simple_multiple"))
    elif kind == "pretrade_plan":
        product = data.get("product", {})
        scenario = data.get("scenario", {})
        label = str(product.get("ticker") or product.get("name") or kind)
        metrics["return_pct"] = _optional_number(scenario.get("etp_return_pct"))
        metrics["path_decay_vs_simple_multiple"] = _optional_number(scenario.get("path_decay_vs_simple_multiple"))
    elif kind == "exposure_report":
        portfolio = data.get("portfolio", {})
        summary = data.get("summary", {})
        label = str(portfolio.get("name") or kind)
        metrics["return_pct"] = _optional_number(summary.get("return_pct"))
        metrics["weighted_exposure"] = _optional_number(summary.get("weighted_exposure"))
    else:
        summary = data.get("summary", {})
        metrics["return_pct"] = _optional_number(summary.get("return_pct"))
        metrics["path_decay_vs_simple_multiple"] = _optional_number(summary.get("path_decay_vs_simple_multiple"))
    return {
        "document_type": kind,
        "schema_version": data.get("schema_version"),
        "label": label,
        "metrics": metrics,
        "warnings": [str(item) for item in data.get("warnings", [])],
    }


def detect_report_type(data: Dict[str, Any]) -> str:
    if data.get("document_type") == "pretrade_plan":
        return "pretrade_plan"
    if data.get("document_type") == "position_size_plan":
        return "position_size_plan"
    if data.get("document_type") == "stress_matrix":
        return "stress_matrix"
    if data.get("document_type") == "thesis_impact":
        return "thesis_impact"
    if data.get("document_type") == "watchlist":
        return "watchlist"
    if "portfolio" in data and "positions" in data and "summary" in data:
        return "exposure_report"
    if "product" in data and "path" in data and "summary" in data:
        return "simulation_output"
    if data.get("document_type"):
        return str(data["document_type"])
    return "unknown_json_report"


def compare_reports_markdown(data: Dict[str, Any]) -> str:
    lines = [
        "# Run Comparison",
        "",
        f"- Base: {data['inputs']['base']}",
        f"- Candidate: {data['inputs']['candidate']}",
        "",
        "## Metrics",
        "",
        "| metric | base | candidate | delta |",
        "| --- | --- | --- | --- |",
    ]
    for metric in ["return_pct", "path_decay_vs_simple_multiple", "weighted_exposure"]:
        base_value = data["base"]["metrics"][metric]
        candidate_value = data["candidate"]["metrics"][metric]
        delta_value = data["deltas"][metric]
        lines.append(
            f"| {metric} | {_display_value(base_value)} | {_display_value(candidate_value)} | {_display_value(delta_value)} |"
        )
    warnings = data["deltas"]["warnings"]
    lines.extend(["", "## Warnings Added", ""])
    lines.extend(f"- {item}" for item in warnings["added"] or ["None"])
    lines.extend(["", "## Warnings Removed", ""])
    lines.extend(f"- {item}" for item in warnings["removed"] or ["None"])
    return "\n".join(lines) + "\n"


def ledger_entry(path: str) -> Dict[str, Any]:
    artifact = Path(path)
    payload = artifact.read_bytes()
    detected_type = "file"
    detected_schema = None
    if artifact.suffix == ".json":
        try:
            data = json.loads(payload.decode("utf-8"))
            if isinstance(data, dict):
                detected_type = detect_report_type(data)
                detected_schema = data.get("schema_version")
        except json.JSONDecodeError:
            detected_type = "json_parse_error"
        except UnicodeDecodeError:
            detected_type = "binary_file"
    return {
        "schema_version": LEDGER_SCHEMA_VERSION,
        "document_type": "run_ledger_entry",
        "artifact_name": artifact.name,
        "artifact_type": detected_type,
        "artifact_schema_version": detected_schema,
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def _gallery_artifact_metadata(path: Path, root: Path, stage: str) -> Dict[str, Any]:
    document_type = None
    schema_version = None
    format_name = _format_name(path)
    if path.suffix == ".json":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                document_type = detect_report_type(data)
                schema_version = data.get("schema_version")
        except (json.JSONDecodeError, UnicodeDecodeError):
            document_type = "json_parse_error"
    elif path.suffix == ".jsonl":
        document_type = "run_ledger"
        schema_version = _jsonl_schema_version(path)
    else:
        companion = path.with_suffix(".json")
        if companion.exists() and companion.name not in {"gallery_index.json", "gallery_index.md"}:
            try:
                data = json.loads(companion.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    document_type = detect_report_type(data)
                    schema_version = data.get("schema_version")
            except (json.JSONDecodeError, UnicodeDecodeError):
                document_type = None
    return {
        "name": path.name,
        "path": _relative_display_path(path, root),
        "stage": stage,
        "format": format_name,
        "document_type": document_type,
        "schema_version": schema_version,
        "bytes": path.stat().st_size,
        "suggested_next_command": _artifact_next_command(path.name, stage),
    }


def _jsonl_schema_version(path: Path) -> Optional[str]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                text = line.strip()
                if not text:
                    continue
                data = json.loads(text)
                if isinstance(data, dict):
                    value = data.get("schema_version")
                    return str(value) if value is not None else None
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return None


def _format_name(path: Path) -> str:
    if path.suffix:
        return path.suffix.lstrip(".")
    return "file"


def _relative_display_path(path: Path, root: Path) -> str:
    return f"{root.as_posix().rstrip('/')}/{path.name}" if not root.is_absolute() else path.name


def _gallery_stage(name: str) -> str:
    if name in {
        "leveraged_nasdaq_3x.json",
        "leveraged_nasdaq_3x.md",
        "single_stock_2x.json",
        "single_stock_2x.md",
        "portfolio_exposure.json",
        "portfolio_exposure.md",
        "template_gallery.json",
        "template_gallery.md",
        "regime_gallery.json",
        "regime_gallery.md",
        "checklist.md",
    } or name.startswith("regime_"):
        return "fixtures"
    if name.startswith("pretrade_plan") or name.startswith("compare_runs") or name == "run_ledger.jsonl":
        return "plans"
    if name.startswith("position_size"):
        return "sizing"
    if name.startswith("stress_matrix"):
        return "stress"
    if name.startswith("thesis_impact") or name.startswith("watchlist"):
        return "thesis/watchlist"
    if name.startswith("package_audit") or name.startswith("demo_story") or name.startswith("factsheet_check"):
        return "audit/story"
    if name.endswith(".html"):
        return "dashboard"
    return "fixtures"


def _stage_next_command(stage: str) -> str:
    commands = {
        "fixtures": "python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --format markdown",
        "plans": "python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015 --format markdown",
        "sizing": "python -m leveraged_etp_risk_lab stress-matrix --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss 0.15 --take-profit 0.20 --format markdown",
        "stress": "python -m leveraged_etp_risk_lab thesis-impact --thesis-file examples/fixtures/thesis_note.md --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/stress_matrix.json --format markdown",
        "thesis/watchlist": "python -m leveraged_etp_risk_lab demo-story --input-dir examples/outputs --format markdown",
        "audit/story": "python -m leveraged_etp_risk_lab static-dashboard --input-dir examples/outputs --output examples/outputs/dashboard.html",
        "dashboard": "python -m leveraged_etp_risk_lab package-audit --format markdown",
    }
    return commands[stage]


def _artifact_next_command(name: str, stage: str) -> str:
    if name.startswith("template_gallery"):
        return "python -m leveraged_etp_risk_lab template-export --template generic-3x-long-index --output generic_index_3x.json"
    if name.startswith("regime_") or name.startswith("regime_gallery"):
        return "python -m leveraged_etp_risk_lab regime-export --regime volatility_cluster --output volatility_cluster_path.csv"
    if name.startswith("pretrade_plan"):
        return "python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015"
    if name.startswith("position_size"):
        return "python -m leveraged_etp_risk_lab stress-matrix --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss 0.15 --take-profit 0.20"
    if name.startswith("stress_matrix"):
        return "python -m leveraged_etp_risk_lab watchlist-build --thesis-impact examples/outputs/thesis_impact.json --stress-matrix examples/outputs/stress_matrix.json"
    if name.startswith("thesis_impact"):
        return "python -m leveraged_etp_risk_lab watchlist-build --thesis-impact examples/outputs/thesis_impact.json --stress-matrix examples/outputs/stress_matrix.json"
    if name.startswith("watchlist"):
        return "python -m leveraged_etp_risk_lab demo-story --input-dir examples/outputs --format markdown"
    if name.startswith("factsheet_check"):
        return "python -m leveraged_etp_risk_lab factsheet-check --product examples/fixtures/leveraged_nasdaq_3x.json --factsheet-file examples/fixtures/factsheet_note.txt --format markdown"
    if name.startswith("package_audit") or name.startswith("demo_story"):
        return "python -m leveraged_etp_risk_lab gallery-index --input-dir examples/outputs --format markdown"
    if name.endswith(".html"):
        return "python -m leveraged_etp_risk_lab gallery-index --input-dir examples/outputs --format markdown"
    return _stage_next_command(stage)


def append_ledger(ledger_path: str, artifact_paths: Iterable[str]) -> Dict[str, Any]:
    ledger = Path(ledger_path)
    rows = [ledger_entry(path) for path in artifact_paths]
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    return {
        "schema_version": LEDGER_SCHEMA_VERSION,
        "document_type": "run_ledger_append",
        "ledger": _display_path(ledger_path),
        "rows_appended": len(rows),
        "artifacts": [row["artifact_name"] for row in rows],
    }


def gallery_index(input_dir: str) -> Dict[str, Any]:
    root = Path(input_dir)
    if not root.exists():
        raise FileNotFoundError(root)
    if not root.is_dir():
        raise ValueError(f"{input_dir} is not a directory")
    groups = {stage: [] for stage in GALLERY_STAGE_ORDER}
    for path in sorted(item for item in root.iterdir() if item.is_file()):
        if path.name in {"gallery_index.json", "gallery_index.md"}:
            continue
        stage = _gallery_stage(path.name)
        metadata = _gallery_artifact_metadata(path, root, stage)
        groups[stage].append(metadata)
    stages = [
        {
            "stage": stage,
            "artifact_count": len(groups[stage]),
            "artifacts": groups[stage],
            "suggested_next_command": _stage_next_command(stage),
        }
        for stage in GALLERY_STAGE_ORDER
    ]
    total_bytes = sum(item["bytes"] for stage in stages for item in stage["artifacts"])
    return {
        "schema_version": GALLERY_INDEX_SCHEMA_VERSION,
        "document_type": "gallery_index",
        "input_dir": _display_path(input_dir),
        "summary": {
            "stages": len(stages),
            "artifacts": sum(stage["artifact_count"] for stage in stages),
            "bytes": total_bytes,
        },
        "stages": stages,
        "provenance": {
            "command": "gallery-index",
            "input_dir": _display_path(input_dir),
        },
    }


def gallery_index_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Public Gallery Index",
        "",
        f"- Schema version: {data['schema_version']}",
        f"- Input directory: {data['input_dir']}",
        f"- Artifacts: {summary['artifacts']}",
        f"- Bytes: {summary['bytes']}",
        "",
    ]
    for stage in data["stages"]:
        lines.extend(
            [
                f"## {stage['stage']}",
                "",
                f"- Artifacts: {stage['artifact_count']}",
                f"- Suggested next command: `{stage['suggested_next_command']}`",
                "",
                "| Artifact | Format | Document type | Schema version | Bytes | Suggested next command |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        if stage["artifacts"]:
            for item in stage["artifacts"]:
                lines.append(
                    f"| {item['path']} | {item['format']} | {_display_value(item['document_type'])} | "
                    f"{_display_value(item['schema_version'])} | {item['bytes']} | "
                    f"`{item['suggested_next_command']}` |"
                )
        else:
            lines.append("| None | n/a | n/a | n/a | 0 | n/a |")
        lines.append("")
    lines.extend(["## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def thesis_impact(thesis_path: str, artifact_paths: Iterable[str]) -> Dict[str, Any]:
    artifacts = list(artifact_paths)
    if not artifacts:
        raise ValueError("at least one --artifact is required")
    thesis_text = Path(thesis_path).read_text(encoding="utf-8")
    claims = extract_thesis_claims(thesis_text)
    if not claims:
        claims = [{"id": "claim_1", "text": "No explicit thesis claims found."}]
    artifact_summaries = []
    warning_pool: List[str] = []
    for path in artifacts:
        data = load_json_report(path)
        summary = summarize_report(data)
        artifact_summaries.append(
            {
                "path": _display_path(path),
                "document_type": summary["document_type"],
                "schema_version": summary["schema_version"],
                "label": summary["label"],
                "metrics": summary["metrics"],
                "warnings_count": len(summary["warnings"]),
            }
        )
        warning_pool.extend(summary["warnings"])
    mappings = [_map_claim_to_artifacts(claim, artifact_summaries, warning_pool) for claim in claims]
    checklist = _unique_text([item for mapping in mappings for item in mapping["checklist"]])
    return {
        "schema_version": THESIS_IMPACT_SCHEMA_VERSION,
        "document_type": "thesis_impact",
        "inputs": {
            "thesis_file": _display_path(thesis_path),
            "artifacts": [_display_path(path) for path in artifacts],
        },
        "thesis": {
            "claim_count": len(claims),
            "claims": claims,
        },
        "artifacts": artifact_summaries,
        "claim_mappings": mappings,
        "warnings": _unique_text(warning_pool),
        "action_checklist": checklist,
        "provenance": {
            "command": "thesis-impact",
            "thesis_file": _display_path(thesis_path),
            "artifacts": [_display_path(path) for path in artifacts],
        },
    }


def extract_thesis_claims(text: str) -> List[Dict[str, str]]:
    claims: List[str] = []
    paragraph: List[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            _flush_claim_paragraph(paragraph, claims)
            continue
        if line.startswith("#"):
            continue
        bullet = line.lstrip("-*0123456789. )")
        if line.startswith(("-", "*")) or bullet != line:
            _flush_claim_paragraph(paragraph, claims)
            if bullet:
                claims.append(bullet)
        else:
            paragraph.append(line)
    _flush_claim_paragraph(paragraph, claims)
    return [{"id": f"claim_{index}", "text": claim} for index, claim in enumerate(claims, start=1)]


def thesis_impact_markdown(data: Dict[str, Any]) -> str:
    lines = [
        "# Thesis Impact",
        "",
        f"- Thesis file: {data['inputs']['thesis_file']}",
        f"- Artifacts: {', '.join(data['inputs']['artifacts'])}",
        f"- Claims mapped: {data['thesis']['claim_count']}",
        "",
        "## Artifact Metrics",
        "",
        "| artifact | type | label | return_pct | path_decay_vs_simple_multiple | weighted_exposure | warnings |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for artifact in data["artifacts"]:
        metrics = artifact["metrics"]
        lines.append(
            f"| {artifact['path']} | {artifact['document_type']} | {artifact['label']} | "
            f"{_display_value(metrics['return_pct'])} | "
            f"{_display_value(metrics['path_decay_vs_simple_multiple'])} | "
            f"{_display_value(metrics['weighted_exposure'])} | {artifact['warnings_count']} |"
        )
    lines.extend(["", "## Claim Mapping", ""])
    for mapping in data["claim_mappings"]:
        lines.extend(
            [
                f"### {mapping['claim_id']}: {mapping['status']}",
                "",
                mapping["claim"],
                "",
                "Observed metrics:",
                "",
            ]
        )
        if mapping["observed_metrics"]:
            for metric in mapping["observed_metrics"]:
                lines.append(
                    f"- {metric['artifact']} {metric['metric']}: "
                    f"{_display_value(metric['value'])} ({metric['interpretation']})"
                )
        else:
            lines.append("- None")
        lines.extend(["", "Warnings:", ""])
        lines.extend(f"- {item}" for item in mapping["warnings"] or ["None"])
        lines.extend(["", "Checklist:", ""])
        lines.extend(f"- [ ] {item}" for item in mapping["checklist"])
        lines.append("")
    lines.extend(["## Action Checklist", ""])
    lines.extend(f"- [ ] {item}" for item in data["action_checklist"] or ["No follow-up actions generated."])
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in data["warnings"] or ["None"])
    return "\n".join(lines) + "\n"


def watchlist_build(thesis_impact_path: str, stress_matrix_path: str) -> Dict[str, Any]:
    impact = load_json_report(thesis_impact_path)
    stress = load_json_report(stress_matrix_path)
    if impact.get("document_type") != "thesis_impact":
        raise ValueError("--thesis-impact must point to a thesis_impact JSON output")
    if stress.get("document_type") != "stress_matrix":
        raise ValueError("--stress-matrix must point to a stress_matrix JSON output")

    thesis_ref = _artifact_ref(thesis_impact_path, impact)
    stress_ref = _artifact_ref(stress_matrix_path, stress)
    entries = []
    entries.extend(_claim_watchlist_entries(impact, thesis_ref))
    entries.extend(_regime_watchlist_entries(stress, stress_ref))
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    entries = sorted(entries, key=lambda item: (severity_order[item["severity"]], item["id"]))
    return {
        "schema_version": WATCHLIST_SCHEMA_VERSION,
        "document_type": "watchlist",
        "not_investment_advice": (
            "This watchlist is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "inputs": {
            "thesis_impact": _display_path(thesis_impact_path),
            "stress_matrix": _display_path(stress_matrix_path),
        },
        "summary": {
            "entries": len(entries),
            "critical": sum(1 for item in entries if item["severity"] == "critical"),
            "high": sum(1 for item in entries if item["severity"] == "high"),
            "medium": sum(1 for item in entries if item["severity"] == "medium"),
            "low": sum(1 for item in entries if item["severity"] == "low"),
        },
        "entries": entries,
        "provenance": {
            "command": "watchlist-build",
            "thesis_impact": _display_path(thesis_impact_path),
            "stress_matrix": _display_path(stress_matrix_path),
        },
    }


def watchlist_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Thesis Watchlist",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        f"- Thesis impact: {data['inputs']['thesis_impact']}",
        f"- Stress matrix: {data['inputs']['stress_matrix']}",
        f"- Entries: {summary['entries']} (critical {summary['critical']}, high {summary['high']}, medium {summary['medium']}, low {summary['low']})",
        "",
        "## Entries",
        "",
        "| id | category | severity | status | title | sources |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for entry in data["entries"]:
        lines.append(
            f"| {entry['id']} | {entry['category']} | {entry['severity']} | {entry['status']} | "
            f"{entry['title']} | {_source_labels(entry['source_artifacts'])} |"
        )
    for entry in data["entries"]:
        lines.extend(["", f"### {entry['id']}: {entry['title']}", ""])
        lines.append(f"- Category: {entry['category']}")
        lines.append(f"- Severity: {entry['severity']}")
        lines.append(f"- Status: {entry['status']}")
        lines.append(f"- Trigger: {entry['trigger']}")
        lines.extend(["", "Next review questions:", ""])
        lines.extend(f"- [ ] {item}" for item in entry["next_review_questions"])
        lines.extend(["", "Source artifact refs:", ""])
        for ref in entry["source_artifacts"]:
            lines.append(f"- {ref['artifact']} ({ref['document_type']} {_display_value(ref['schema_version'])}): {ref['detail']}")
        if entry["warnings"]:
            lines.extend(["", "Warnings:", ""])
            lines.extend(f"- {item}" for item in entry["warnings"])
    return "\n".join(lines) + "\n"


def _claim_watchlist_entries(impact: Dict[str, Any], thesis_ref: Dict[str, Any]) -> List[Dict[str, Any]]:
    entries = []
    for mapping in impact.get("claim_mappings", []):
        warnings = [str(item) for item in mapping.get("warnings", [])]
        severity = _claim_severity(str(mapping.get("status", "")), warnings)
        metrics = [
            {
                "artifact": item["artifact"],
                "metric": item["metric"],
                "value": item["value"],
                "interpretation": item["interpretation"],
            }
            for item in mapping.get("observed_metrics", [])
        ]
        source_artifacts = [dict(thesis_ref, detail=f"claim mapping {mapping.get('claim_id', 'claim')}")]
        for metric in mapping.get("observed_metrics", []):
            source_artifacts.append(
                {
                    "artifact": metric["artifact"],
                    "document_type": "observed_metric_source",
                    "schema_version": None,
                    "detail": f"{metric['metric']} for {mapping.get('claim_id', 'claim')}",
                }
            )
        entries.append(
            {
                "id": str(mapping.get("claim_id", "claim_unknown")),
                "category": "claim",
                "title": _short_title(str(mapping.get("claim", ""))),
                "severity": severity,
                "status": str(mapping.get("status", "needs_review")),
                "trigger": str(mapping.get("claim", "")),
                "metrics": metrics,
                "warnings": warnings,
                "next_review_questions": _claim_review_questions(mapping),
                "source_artifacts": _unique_artifact_refs(source_artifacts),
            }
        )
    return entries


def _regime_watchlist_entries(stress: Dict[str, Any], stress_ref: Dict[str, Any]) -> List[Dict[str, Any]]:
    entries = []
    for row in stress.get("rows", []):
        severity = _regime_severity(row)
        trigger = _regime_trigger(row)
        entries.append(
            {
                "id": f"regime_{row.get('regime', 'unknown')}",
                "category": "regime_trigger",
                "title": f"{row.get('name', row.get('regime', 'Regime'))} stress trigger",
                "severity": severity,
                "status": "triggered" if severity in {"critical", "high", "medium"} else "monitor",
                "trigger": trigger,
                "metrics": {
                    "regime": row.get("regime"),
                    "return_pct": row.get("return_pct"),
                    "path_decay_vs_simple_multiple": row.get("path_decay_vs_simple_multiple"),
                    "worst_drawdown_pct": row.get("worst_drawdown_pct"),
                    "stop_events": row.get("stop_events"),
                    "warnings_count": row.get("warnings_count"),
                },
                "warnings": [f"{row.get('warnings_count', 0)} stress-matrix warning(s) observed for this regime."],
                "next_review_questions": _regime_review_questions(row),
                "source_artifacts": [
                    dict(stress_ref, detail=f"stress row {row.get('regime', 'unknown')}"),
                ],
            }
        )
    return entries


def _claim_severity(status: str, warnings: List[str]) -> str:
    if status == "challenged":
        return "high"
    if status == "needs_review" and len(warnings) >= 3:
        return "medium"
    if status == "needs_review":
        return "medium"
    if warnings:
        return "medium"
    return "low"


def _regime_severity(row: Dict[str, Any]) -> str:
    return_pct = float(row.get("return_pct", 0.0))
    drawdown = float(row.get("worst_drawdown_pct", 0.0))
    decay = float(row.get("path_decay_vs_simple_multiple", 0.0))
    stop_events = int(row.get("stop_events", 0))
    if return_pct <= -25 or drawdown <= -25:
        return "critical"
    if (stop_events > 0 and return_pct <= -15) or return_pct <= -10 or drawdown <= -15 or decay <= -2:
        return "high"
    if stop_events > 0 or return_pct < 0 or drawdown <= -5 or decay < 0:
        return "medium"
    return "low"


def _regime_trigger(row: Dict[str, Any]) -> str:
    labels = row.get("stop_event_labels", [])
    parts = [
        f"return {row.get('return_pct')}%",
        f"worst drawdown {row.get('worst_drawdown_pct')}%",
        f"path decay {row.get('path_decay_vs_simple_multiple')}",
    ]
    if labels:
        parts.append("band events: " + "; ".join(str(item) for item in labels))
    return "; ".join(parts)


def _claim_review_questions(mapping: Dict[str, Any]) -> List[str]:
    questions = [
        f"What evidence would change the status of {mapping.get('claim_id', 'this claim')} from {mapping.get('status', 'needs_review')}?",
        "Which observed metrics are most relevant to the claim, and are any expected metrics missing?",
    ]
    for item in mapping.get("checklist", [])[:3]:
        questions.append(str(item))
    if mapping.get("warnings"):
        questions.append("Which warning would invalidate the thesis if it appears in live review?")
    return _unique_text(questions)


def _regime_review_questions(row: Dict[str, Any]) -> List[str]:
    questions = [
        f"Would the thesis still be acceptable under the {row.get('regime', 'selected')} regime?",
        "What pre-defined action follows if this regime starts to resemble the current market path?",
    ]
    if int(row.get("stop_events", 0)) > 0:
        questions.append("Are modeled stop or take-profit band events acceptable after accounting for execution and gap risk?")
    if float(row.get("path_decay_vs_simple_multiple", 0.0)) < 0:
        questions.append("Does modeled path decay weaken the expected holding-period thesis?")
    if float(row.get("return_pct", 0.0)) < 0:
        questions.append("Is the loss budget still valid under this modeled return?")
    return _unique_text(questions)


def _artifact_ref(path: str, data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "artifact": _display_path(path),
        "document_type": str(data.get("document_type", "unknown_json_report")),
        "schema_version": data.get("schema_version"),
        "detail": "source artifact",
    }


def _unique_artifact_refs(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    result = []
    for item in items:
        key = (item.get("artifact"), item.get("document_type"), item.get("schema_version"), item.get("detail"))
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def _source_labels(refs: List[Dict[str, Any]]) -> str:
    return ", ".join(_unique_text([str(ref["artifact"]) for ref in refs]))


def _short_title(text: str) -> str:
    stripped = " ".join(text.split())
    if len(stripped) <= 80:
        return stripped
    return stripped[:77].rstrip() + "..."


def _comparison_side(summary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "document_type": summary["document_type"],
        "schema_version": summary["schema_version"],
        "label": summary["label"],
        "metrics": summary["metrics"],
        "warnings_count": len(summary["warnings"]),
    }


def _warning_delta(base: List[str], candidate: List[str]) -> Dict[str, Any]:
    base_set = set(base)
    candidate_set = set(candidate)
    return {
        "added": sorted(candidate_set - base_set),
        "removed": sorted(base_set - candidate_set),
        "unchanged_count": len(base_set.intersection(candidate_set)),
    }


def _numeric_delta(base: Optional[float], candidate: Optional[float]) -> Optional[float]:
    if base is None or candidate is None:
        return None
    return round(candidate - base, 6)


def _optional_number(value: Any) -> Optional[float]:
    if value is None:
        return None
    return round(float(value), 6)


def _flush_claim_paragraph(paragraph: List[str], claims: List[str]) -> None:
    if not paragraph:
        return
    claim = " ".join(paragraph).strip()
    if claim:
        claims.append(claim)
    paragraph.clear()


def _map_claim_to_artifacts(
    claim: Dict[str, str], artifacts: List[Dict[str, Any]], warnings: List[str]
) -> Dict[str, Any]:
    text = claim["text"]
    lower = text.lower()
    metric_names = _claim_metric_names(lower)
    observed = []
    statuses = []
    for artifact in artifacts:
        for metric_name in metric_names:
            value = artifact["metrics"].get(metric_name)
            if value is None:
                continue
            interpretation = _interpret_metric(lower, metric_name, value)
            observed.append(
                {
                    "artifact": artifact["path"],
                    "label": artifact["label"],
                    "metric": metric_name,
                    "value": value,
                    "interpretation": interpretation,
                }
            )
            statuses.append(interpretation)
    related_warnings = _related_warnings(lower, warnings)
    checklist = _claim_checklist(lower)
    status = _claim_status(statuses, related_warnings)
    return {
        "claim_id": claim["id"],
        "claim": text,
        "status": status,
        "observed_metrics": observed,
        "warnings": related_warnings,
        "checklist": checklist,
    }


def _claim_metric_names(lower: str) -> List[str]:
    metrics = []
    if any(word in lower for word in ["recover", "return", "upside", "rally", "flat"]):
        metrics.append("return_pct")
    if any(word in lower for word in ["choppy", "decay", "volatility", "daily-reset", "daily reset", "simple multiple"]):
        metrics.append("path_decay_vs_simple_multiple")
    if any(word in lower for word in ["leverage", "exposure", "portfolio", "concentration"]):
        metrics.append("weighted_exposure")
    if not metrics:
        metrics = ["return_pct", "path_decay_vs_simple_multiple", "weighted_exposure"]
    return metrics


def _interpret_metric(lower: str, metric_name: str, value: float) -> str:
    if metric_name == "return_pct":
        if any(word in lower for word in ["recover", "upside", "rally"]) and value <= 0:
            return "challenges positive-return claim"
        if any(word in lower for word in ["loss", "reject", "stop"]) and value < 0:
            return "confirms downside scenario is present"
        return "observed return metric"
    if metric_name == "path_decay_vs_simple_multiple":
        if value < 0:
            return "shows modeled path decay"
        if value > 0:
            return "does not show modeled decay in this artifact"
        return "no modeled path-decay difference"
    if metric_name == "weighted_exposure":
        if abs(value) >= 2:
            return "shows elevated leveraged exposure"
        return "shows limited aggregate exposure"
    return "observed metric"


def _related_warnings(lower: str, warnings: List[str]) -> List[str]:
    keywords = {
        "return": ["return", "forecast", "path"],
        "recover": ["return", "forecast", "path"],
        "loss": ["loss", "stop", "drawdown"],
        "stop": ["loss", "stop"],
        "decay": ["decay", "reset", "choppy", "volatility", "simple multiple"],
        "choppy": ["decay", "reset", "choppy", "volatility"],
        "leverage": ["leverage", "exposure", "daily reset"],
        "exposure": ["leverage", "exposure", "concentration"],
        "liquidity": ["liquidity", "execution"],
        "event": ["event", "earnings", "macro"],
    }
    selected_terms = []
    for token, terms in keywords.items():
        if token in lower:
            selected_terms.extend(terms)
    if not selected_terms:
        selected_terms = ["risk", "leverage", "path", "loss"]
    matched = []
    for warning in warnings:
        warning_lower = warning.lower()
        if any(term in warning_lower for term in selected_terms):
            matched.append(warning)
    return _unique_text(matched[:5])


def _claim_checklist(lower: str) -> List[str]:
    items = ["Record whether the observed artifact metrics support, challenge, or leave the claim unresolved."]
    if any(word in lower for word in ["recover", "return", "upside", "rally"]):
        items.append("Compare the thesis return expectation with modeled ETP and underlying returns.")
    if any(word in lower for word in ["choppy", "decay", "volatility", "daily-reset", "daily reset"]):
        items.append("Review path decay versus the simple multiple before relying on multi-day leverage.")
    if any(word in lower for word in ["loss", "budget", "stop", "reject"]):
        items.append("Confirm loss budget and stop band are acceptable before entry.")
    if any(word in lower for word in ["liquidity", "execution", "spread"]):
        items.append("Complete a liquidity and execution-quality review outside this model.")
    if any(word in lower for word in ["event", "earnings", "macro", "regulatory"]):
        items.append("Check event risk before treating the scenario as actionable.")
    if any(word in lower for word in ["leverage", "exposure", "portfolio", "concentration"]):
        items.append("Check aggregate exposure and concentration against portfolio limits.")
    return _unique_text(items)


def _claim_status(statuses: List[str], warnings: List[str]) -> str:
    if any(status.startswith("challenges") for status in statuses):
        return "challenged"
    if statuses and not warnings:
        return "observed"
    return "needs_review"


def _display_path(path: str) -> str:
    value = Path(path)
    return value.as_posix() if not value.is_absolute() else value.name


def _display_value(value: Any) -> str:
    if value is None:
        return "n/a"
    return str(value)


def _unique_text(items: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
