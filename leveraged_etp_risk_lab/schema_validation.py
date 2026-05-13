from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


SCHEMA_INVENTORY_VERSION = "0.26"
ARTIFACT_VALIDATION_VERSION = "0.26"
ROOT = Path(__file__).resolve().parents[1]
SAFETY_FLAGS = ["live_market_data", "shell_out", "private_context", "broker_execution"]


def schema_inventory(root: Path = ROOT, examples_dir: Optional[Path] = None) -> Dict[str, Any]:
    docs_dir = root / "docs"
    examples_root = examples_dir or root / "examples" / "outputs"
    examples = _example_claims(examples_root, root)
    schemas = []
    for path in sorted(docs_dir.glob("*.schema.json")):
        schema = _load_json(path)
        document_type = _const_value(schema, "document_type")
        schema_version = _const_value(schema, "schema_version")
        required = [str(item) for item in schema.get("required", [])]
        matched = [item["path"] for item in examples if _claim_matches_schema(item, schema, document_type, schema_version)]
        schemas.append(
            {
                "path": path.relative_to(root).as_posix(),
                "title": str(schema.get("title", path.stem)),
                "document_type": document_type,
                "schema_version": schema_version,
                "required_top_level_fields": required,
                "examples": matched,
                "public_safety_notes": _public_safety_notes(schema),
            }
        )
    return {
        "schema_version": SCHEMA_INVENTORY_VERSION,
        "document_type": "schema_inventory",
        "summary": {
            "schemas": len(schemas),
            "examples": sum(len(item["examples"]) for item in schemas),
            "safety_flags": SAFETY_FLAGS,
        },
        "schemas": schemas,
        "provenance": {
            "command": "schema-inventory",
            "schema_dir": "docs",
            "examples_dir": _display_path(examples_root, root),
            "live_market_data": False,
            "shell_out": False,
            "private_context": False,
            "broker_execution": False,
        },
    }


def schema_inventory_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Schema Inventory",
        "",
        f"- Schema version: {data['schema_version']}",
        f"- Schemas: {summary['schemas']}",
        f"- Matching examples: {summary['examples']}",
        "",
        "| Schema | Document type | Version | Required fields | Matching examples | Safety notes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in data["schemas"]:
        lines.append(
            f"| {item['path']} | {_display_value(item['document_type'])} | "
            f"{_display_value(item['schema_version'])} | {', '.join(item['required_top_level_fields']) or 'None'} | "
            f"{', '.join(item['examples']) or 'None'} | {'; '.join(item['public_safety_notes']) or 'None'} |"
        )
    lines.extend(["", "## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def artifact_validate(paths: Optional[Iterable[str]] = None, root: Path = ROOT) -> Dict[str, Any]:
    schema_map = _schema_map(root / "docs")
    artifact_paths = _artifact_paths(paths, root)
    results = [_validate_path(path, root, schema_map) for path in artifact_paths]
    failed = [item for item in results if item["status"] != "pass"]
    return {
        "schema_version": ARTIFACT_VALIDATION_VERSION,
        "document_type": "artifact_validation",
        "summary": {
            "artifacts": len(results),
            "passed": len(results) - len(failed),
            "failed": len(failed),
            "ready": not failed,
        },
        "artifacts": results,
        "provenance": {
            "command": "artifact-validate",
            "source": "path_list" if paths else "examples/outputs",
            "live_market_data": False,
            "shell_out": False,
            "private_context": False,
            "broker_execution": False,
        },
    }


def artifact_validation_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Artifact Validation",
        "",
        f"- Schema version: {data['schema_version']}",
        f"- Ready: {'yes' if summary['ready'] else 'no'}",
        f"- Artifacts: {summary['passed']} passed, {summary['failed']} failed",
        "",
        "| Artifact | Document type | Version | Status | Issues | Safety flags |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in data["artifacts"]:
        flags = ", ".join(f"{key}={value}" for key, value in item["provenance_flags"].items()) or "None"
        lines.append(
            f"| {item['path']} | {_display_value(item['document_type'])} | "
            f"{_display_value(item['schema_version'])} | {item['status']} | "
            f"{'; '.join(item['issues']) or 'None'} | {flags} |"
        )
    lines.extend(["", "## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def _validate_path(path: Path, root: Path, schema_map: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    rel = _display_path(path, root)
    issues: List[str] = []
    rows: List[Dict[str, Any]] = []
    if path.suffix == ".jsonl":
        try:
            for index, row in enumerate(_load_jsonl(path), start=1):
                rows.append(row)
                issues.extend(f"line {index}: {item}" for item in _validate_object(row, schema_map))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            issues.append(f"parse error: {exc}")
    else:
        try:
            data = _load_json(path)
            if not isinstance(data, dict):
                issues.append("artifact is not a JSON object")
                data = {}
            rows.append(data)
            issues.extend(_validate_object(data, schema_map))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            issues.append(f"parse error: {exc}")
    first = rows[0] if rows else {}
    matched_schema = _schema_for_object(first, schema_map) if first else None
    flags = _collect_flags(rows)
    return {
        "path": rel,
        "document_type": first.get("document_type") or (matched_schema or {}).get("document_type"),
        "schema_version": first.get("schema_version"),
        "status": "pass" if not issues else "fail",
        "issues": issues,
        "provenance_flags": flags,
    }


def _validate_object(data: Dict[str, Any], schema_map: Dict[str, Dict[str, Any]]) -> List[str]:
    issues = []
    document_type = data.get("document_type")
    schema_version = data.get("schema_version")
    if not isinstance(schema_version, str):
        issues.append("missing or non-string schema_version")
        return issues
    schema = _schema_for_object(data, schema_map)
    if schema is None:
        if isinstance(document_type, str):
            issues.append(f"no local schema for document_type {document_type}")
        else:
            issues.append("no local schema matches artifact required fields")
        return issues
    expected_version = schema.get("schema_version")
    if expected_version is not None and schema_version != expected_version:
        issues.append(f"schema_version {schema_version} != {expected_version}")
    for field in schema.get("required", []):
        if field not in data:
            issues.append(f"missing required field {field}")
    issues.extend(_flag_issues(data, schema))
    return issues


def _flag_issues(data: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    issues = []
    expected = _schema_flag_expectations(schema)
    containers = [data]
    provenance = data.get("provenance")
    if isinstance(provenance, dict):
        containers.append(provenance)
    summary = data.get("summary")
    if isinstance(summary, dict):
        containers.append(summary)
    for container in containers:
        for flag in SAFETY_FLAGS:
            if flag not in container:
                continue
            if not isinstance(container[flag], bool):
                issues.append(f"{flag} must be boolean when present")
            elif flag in expected and container[flag] != expected[flag]:
                issues.append(f"{flag} must be {str(expected[flag]).lower()}")
    return issues


def _schema_map(schema_dir: Path) -> Dict[str, Dict[str, Any]]:
    schemas: Dict[str, Dict[str, Any]] = {}
    schema_list = []
    for path in sorted(schema_dir.glob("*.schema.json")):
        schema = _load_json(path)
        document_type = _const_value(schema, "document_type")
        entry = {
            "path": path,
            "document_type": document_type or path.stem.replace(".schema", "").replace("-", "_"),
            "schema_version": _const_value(schema, "schema_version"),
            "required": [str(item) for item in schema.get("required", [])],
            "raw": schema,
        }
        schema_list.append(entry)
        if document_type:
            schemas[document_type] = entry
    schemas["__schemas__"] = {"items": schema_list}
    return schemas


def _schema_for_object(data: Dict[str, Any], schema_map: Dict[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    document_type = data.get("document_type")
    if isinstance(document_type, str) and document_type in schema_map:
        return schema_map[document_type]
    schema_version = data.get("schema_version")
    candidates = []
    for schema in schema_map.get("__schemas__", {}).get("items", []):
        expected_version = schema.get("schema_version")
        if isinstance(schema_version, str) and expected_version != schema_version:
            continue
        required = [field for field in schema.get("required", []) if field != "document_type"]
        if required and all(field in data for field in required):
            candidates.append(schema)
    if len(candidates) == 1:
        return candidates[0]
    return None


def _schema_flag_expectations(schema: Dict[str, Any]) -> Dict[str, bool]:
    raw = schema.get("raw", schema)
    expected: Dict[str, bool] = {}

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in SAFETY_FLAGS and isinstance(child, dict) and child.get("const") in {True, False}:
                    expected[key] = bool(child["const"])
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(raw)
    return expected


def _collect_flags(rows: List[Dict[str, Any]]) -> Dict[str, bool]:
    found: Dict[str, bool] = {}
    for row in rows:
        for container in [row, row.get("provenance"), row.get("summary")]:
            if not isinstance(container, dict):
                continue
            for flag in SAFETY_FLAGS:
                if flag in container and isinstance(container[flag], bool):
                    found[flag] = container[flag]
    return {key: found[key] for key in SAFETY_FLAGS if key in found}


def _artifact_paths(paths: Optional[Iterable[str]], root: Path) -> List[Path]:
    if paths:
        candidates = [Path(path) for path in paths]
    else:
        candidates = sorted((root / "examples" / "outputs").glob("*.json"))
        candidates.extend(sorted((root / "examples" / "outputs").glob("*.jsonl")))
    return [path if path.is_absolute() else root / path for path in candidates]


def _example_claims(examples_root: Path, root: Path) -> List[Dict[str, Any]]:
    claims = []
    if not examples_root.exists() or not examples_root.is_dir():
        return claims
    for path in sorted(examples_root.iterdir()):
        if not path.is_file() or path.suffix not in {".json", ".jsonl"}:
            continue
        try:
            if path.suffix == ".jsonl":
                for row in _load_jsonl(path):
                    claims.append(
                        {
                            "path": _display_path(path, root),
                            "document_type": row.get("document_type"),
                            "schema_version": row.get("schema_version"),
                            "fields": sorted(row.keys()),
                        }
                    )
                    break
            else:
                data = _load_json(path)
                if isinstance(data, dict):
                    claims.append(
                        {
                            "path": _display_path(path, root),
                            "document_type": data.get("document_type"),
                            "schema_version": data.get("schema_version"),
                            "fields": sorted(data.keys()),
                        }
                    )
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
    return claims


def _public_safety_notes(schema: Dict[str, Any]) -> List[str]:
    notes = []
    required = set(str(item) for item in schema.get("required", []))
    if "not_investment_advice" in required:
        notes.append("requires not_investment_advice")
    expectations = _schema_flag_expectations(schema)
    for flag in SAFETY_FLAGS:
        if flag in expectations:
            notes.append(f"requires {flag}: {str(expectations[flag]).lower()}")
    if "provenance" in required:
        notes.append("requires provenance")
    return notes


def _claim_matches_schema(
    claim: Dict[str, Any],
    schema: Dict[str, Any],
    document_type: Optional[str],
    schema_version: Optional[str],
) -> bool:
    if schema_version is not None and claim.get("schema_version") != schema_version:
        return False
    if document_type is not None:
        return claim.get("document_type") == document_type
    required = [str(item) for item in schema.get("required", []) if item != "document_type"]
    fields = set(str(item) for item in claim.get("fields", []))
    return bool(required) and all(field in fields for field in required)


def _const_value(schema: Dict[str, Any], name: str) -> Optional[str]:
    value = schema.get("properties", {}).get(name, {}).get("const")
    return str(value) if value is not None else None


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            text = line.strip()
            if not text:
                continue
            data = json.loads(text)
            if not isinstance(data, dict):
                raise ValueError(f"{path} contains a non-object row")
            rows.append(data)
    return rows


def _display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _display_value(value: Any) -> str:
    return "n/a" if value is None else str(value)
