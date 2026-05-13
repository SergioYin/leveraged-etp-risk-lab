from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List


def to_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def simulation_markdown(data: Dict[str, Any]) -> str:
    product = data["product"]
    summary = data["summary"]
    lines: List[str] = [
        f"# Simulation: {product['ticker']}",
        "",
        f"- Product: {product['name']}",
        f"- Underlying: {product['underlying']}",
        f"- Leverage: {product['leverage']}x daily reset",
        f"- Annual fee: {product['annual_fee_pct']}%",
        f"- Ending ETP NAV: {summary['ending_etp_nav']}",
        f"- ETP return: {summary['etp_return_pct']}%",
        f"- Underlying return: {summary['underlying_return_pct']}%",
        f"- Simple multiple return: {summary['simple_multiple_return_pct']}%",
        f"- Path decay vs simple multiple: {summary['path_decay_vs_simple_multiple']}",
        "",
        "## Band Events",
        "",
    ]
    if data["band_events"]:
        for event in data["band_events"]:
            lines.append(f"- Day {event['day']} ({event['label']}): {event['event']} at NAV {event['nav']}")
    else:
        lines.append("- None")
    lines.extend(["", "## Path", "", _table(data["path"]), "", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in data["warnings"])
    return "\n".join(lines) + "\n"


def checklist_markdown(profile: str) -> str:
    items = checklist_items(profile)
    lines = [f"# Leveraged ETP Risk Checklist: {profile}", ""]
    lines.extend(f"- [ ] {item}" for item in items)
    return "\n".join(lines) + "\n"


def checklist_json(profile: str) -> str:
    return to_json({"schema_version": "0.1", "profile": profile, "items": checklist_items(profile)})


def checklist_items(profile: str) -> List[str]:
    base = [
        "Confirm the product uses daily reset leverage and identify the stated leverage factor.",
        "Compare the planned holding period with the product objective and risk disclosures.",
        "Run at least one trending path and one choppy path before sizing the trade.",
        "Record stop-loss and take-profit levels before entry.",
        "Review borrowing, financing, and management-fee drag assumptions.",
        "Check whether the underlying has event risk, earnings, regulatory decisions, or macro releases.",
        "Document why the scenario does not rely on a simple leverage multiple over several days.",
    ]
    if profile == "active-trader":
        base.append("Confirm intraday liquidity, spreads, and exit rules for fast markets.")
    elif profile == "risk-review":
        base.append("Record maximum tolerable loss, concentration, and portfolio correlation.")
    return base


def version_report(version: str) -> str:
    return to_json(
        {
            "name": "leveraged-etp-risk-lab",
            "version": version,
            "python": ">=3.9",
            "dependencies": [],
            "commands": ["simulate", "checklist", "demo-bundle", "selfcheck", "version-report"],
        }
    )


def _table(rows: Iterable[Dict[str, Any]]) -> str:
    headers = [
        "day",
        "label",
        "underlying_return_pct",
        "underlying_index",
        "daily_levered_return_pct",
        "etp_nav",
        "simple_multiple_nav",
        "path_decay",
    ]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[key]) for key in headers) + " |")
    return "\n".join(lines)
