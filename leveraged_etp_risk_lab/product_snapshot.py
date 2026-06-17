from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


PRODUCT_SNAPSHOT_SCHEMA_VERSION = "0.31"


def product_snapshot_case_study(fixture_path: str) -> Dict[str, Any]:
    fixture = _load_fixture(fixture_path)
    required = [
        "snapshot_id",
        "title",
        "snapshot_date",
        "not_investment_advice",
        "product",
        "case_study",
        "source_attribution",
        "reviewer_demo_path",
        "warnings",
    ]
    missing = [key for key in required if key not in fixture]
    if missing:
        raise ValueError(f"product snapshot fixture is missing required field(s): {', '.join(missing)}")
    return {
        "schema_version": PRODUCT_SNAPSHOT_SCHEMA_VERSION,
        "document_type": "product_snapshot_case_study",
        "snapshot_id": str(fixture["snapshot_id"]),
        "title": str(fixture["title"]),
        "snapshot_date": str(fixture["snapshot_date"]),
        "not_investment_advice": str(fixture["not_investment_advice"]),
        "product": dict(fixture["product"]),
        "case_study": dict(fixture["case_study"]),
        "source_attribution": [dict(item) for item in fixture["source_attribution"]],
        "reviewer_demo_path": [dict(item) for item in fixture["reviewer_demo_path"]],
        "warnings": [str(item) for item in fixture["warnings"]],
        "provenance": {
            "command": "product-snapshot",
            "fixture": _display_path(fixture_path),
            "live_market_data": False,
            "shell_out": False,
            "private_context": False,
            "broker_execution": False,
            "trading_enabled": False,
            "personalized_recommendations": False,
        },
    }


def product_snapshot_markdown(data: Dict[str, Any]) -> str:
    product = data["product"]
    case = data["case_study"]
    lines: List[str] = [
        f"# {data['title']}",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Product Snapshot",
        "",
        f"- Snapshot id: {data['snapshot_id']}",
        f"- Snapshot date: {data['snapshot_date']}",
        f"- Product: {product.get('name')} ({product.get('ticker')})",
        f"- Issuer: {product.get('issuer')}",
        f"- Underlying: {product.get('underlying')}",
        f"- Daily target: {product.get('daily_target')}",
        f"- Reset frequency: {product.get('reset_frequency')}",
        f"- Expense ratio note: {product.get('expense_ratio_note')}",
        "",
        "## Case Study",
        "",
        f"- Reviewer question: {case.get('reviewer_question')}",
        f"- Plain answer: {case.get('plain_english_answer')}",
        f"- Demo fixture: {case.get('demo_fixture')}",
        "",
        "### Learning Points",
        "",
    ]
    lines.extend(f"- {item}" for item in case.get("learning_points", []))
    lines.extend(["", "## Source Attribution", ""])
    for source in data["source_attribution"]:
        lines.append(f"- {source.get('name')}: {source.get('claim_summary')} ({source.get('url')})")
    lines.extend(["", "## Reviewer Demo Path", ""])
    for item in data["reviewer_demo_path"]:
        lines.append(f"- {item.get('purpose')}")
        lines.append(f"  `{item.get('command')}`")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in data["warnings"])
    lines.extend(["", "## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def _load_fixture(path: str) -> Dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a JSON object")
    return data


def _display_path(path: str) -> str:
    return Path(path).as_posix()
