from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List


PRODUCT_FAMILY_WALKTHROUGH_SCHEMA_VERSION = "0.31"
PRODUCT_FAMILY_FIXTURES = [
    "leveraged_nasdaq_3x.json",
    "single_stock_2x.json",
    "sector_index_2x.json",
]


def product_family_walkthrough(input_dir: str, fixtures_dir: str) -> Dict[str, Any]:
    input_root = Path(input_dir)
    fixture_root = Path(fixtures_dir)
    snapshot = _load_json(input_root / "product_snapshot_tqqq_case_study.json")
    pack = _load_json(input_root / "scenario_pack.json")
    receipt = _load_json(input_root / "scenario_pack_reviewer_receipt.json")
    product_family_examples = _product_family_examples(fixture_root, PRODUCT_FAMILY_FIXTURES)
    source_artifacts = _source_artifacts(
        [
            input_root / "product_snapshot_tqqq_case_study.json",
            input_root / "product_snapshot_tqqq_case_study.md",
            input_root / "scenario_pack.json",
            input_root / "scenario_pack.md",
            input_root / "scenario_pack_reviewer_receipt.json",
            input_root / "scenario_pack_reviewer_receipt.md",
            fixture_root / "product_snapshot_tqqq_case_study.json",
            *[fixture_root / filename for filename in PRODUCT_FAMILY_FIXTURES],
            fixture_root / "nasdaq_chop_path.csv",
            fixture_root / "single_stock_gap_path.csv",
        ]
    )
    return {
        "schema_version": PRODUCT_FAMILY_WALKTHROUGH_SCHEMA_VERSION,
        "document_type": "product_family_walkthrough",
        "not_investment_advice": _not_advice(),
        "walkthrough_id": "v0.31.3-product-family-walkthrough",
        "title": "Product Family Walkthrough",
        "summary": {
            "snapshot_product": snapshot.get("product", {}).get("ticker"),
            "scenario_cases": pack.get("summary", {}).get("cases"),
            "fixture_inputs": receipt.get("summary", {}).get("fixture_inputs"),
            "source_artifacts": len(source_artifacts),
            "product_family_examples": len(product_family_examples),
            "live_market_data": False,
            "broker_execution": False,
            "trading_enabled": False,
            "personalized_recommendations": False,
        },
        "comparison": _comparison(snapshot, pack, receipt),
        "product_family_examples": product_family_examples,
        "fixture_provenance": _fixture_provenance(source_artifacts),
        "path_dependency_caveats": [
            "Daily-reset leverage is modeled one day at a time, so multi-day results can diverge from a simple leverage multiple.",
            "Choppy paths can create path decay even when the underlying starts and ends near the same level.",
            "Gap, liquidity, borrow, financing, tax, spread, and execution effects are outside these deterministic fixtures.",
            "Scenario outputs are local education examples; reviewers should compare hashes and commands before relying on narrative consistency.",
        ],
        "reviewer_steps": [
            {
                "step": "Regenerate product snapshot",
                "command": "python -m leveraged_etp_risk_lab product-snapshot --format markdown --output examples/outputs/product_snapshot_tqqq_case_study.md",
            },
            {
                "step": "Regenerate scenario pack",
                "command": "python -m leveraged_etp_risk_lab scenario-pack --input-dir examples/outputs --fixtures-dir examples/fixtures --output-dir examples/outputs --format markdown",
            },
            {
                "step": "Regenerate this walkthrough",
                "command": "python -m leveraged_etp_risk_lab product-family-walkthrough --input-dir examples/outputs --fixtures-dir examples/fixtures --format markdown",
            },
            {
                "step": "Validate reviewer artifacts",
                "command": "python -m leveraged_etp_risk_lab artifact-validate examples/outputs/product_family_walkthrough.json examples/outputs/product_snapshot_tqqq_case_study.json examples/outputs/scenario_pack.json examples/outputs/scenario_pack_reviewer_receipt.json --format markdown",
            },
        ],
        "source_artifacts": source_artifacts,
        "safety_boundaries": [
            "No live market data is fetched or required.",
            "No broker, API, account, order, routing, staging, preview, or execution capability is used.",
            "No trading instruction, personalized recommendation, suitability determination, or investment advice is produced.",
            "The walkthrough compares static local artifacts and checked-in fixtures only.",
        ],
        "provenance": {
            "command": "product-family-walkthrough",
            "input_dir": str(input_root),
            "fixtures_dir": str(fixture_root),
            "live_market_data": False,
            "shell_out": False,
            "private_context": False,
            "broker_execution": False,
            "workflow_files_read": False,
            "trading_enabled": False,
            "personalized_recommendations": False,
        },
    }


def product_family_walkthrough_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines: List[str] = [
        f"# {data['title']}",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Summary",
        "",
        f"- Snapshot product: {summary['snapshot_product']}",
        f"- Scenario cases: {summary['scenario_cases']}",
        f"- Fixture inputs in receipt: {summary['fixture_inputs']}",
        f"- Source artifacts: {summary['source_artifacts']}",
        f"- Product family examples: {summary['product_family_examples']}",
        f"- Live market data: {summary['live_market_data']}",
        f"- Broker execution: {summary['broker_execution']}",
        f"- Trading enabled: {summary['trading_enabled']}",
        f"- Personalized recommendations: {summary['personalized_recommendations']}",
        "",
        "## Artifact Comparison",
        "",
        "| Artifact | Reviewer use | Boundary |",
        "| --- | --- | --- |",
    ]
    for item in data["comparison"]:
        lines.append(f"| {item['artifact']} | {item['reviewer_use']} | {item['boundary']} |")
    lines.extend(["", "## Static Product Family Examples", "", "| Fixture | Ticker | Underlying | Leverage | Boundary |", "| --- | --- | --- | ---: | --- |"])
    for item in data["product_family_examples"]:
        lines.append(
            f"| {item['fixture']} | {item['ticker']} | {item['underlying']} | {item['leverage']} | {item['boundary']} |"
        )
    lines.extend(["", "## Fixture Provenance", "", "| Path | Kind | Bytes | SHA-256 |", "| --- | --- | ---: | --- |"])
    for item in data["fixture_provenance"]:
        lines.append(f"| {item['path']} | {item['kind']} | {item['bytes']} | `{item['sha256']}` |")
    lines.extend(["", "## Path-Dependency Caveats", ""])
    lines.extend(f"- {item}" for item in data["path_dependency_caveats"])
    lines.extend(["", "## Reviewer Steps", ""])
    for item in data["reviewer_steps"]:
        lines.append(f"- {item['step']}")
        lines.append(f"  `{item['command']}`")
    lines.extend(["", "## Safety Boundaries", ""])
    lines.extend(f"- {item}" for item in data["safety_boundaries"])
    lines.extend(["", "## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def _comparison(snapshot: Dict[str, Any], pack: Dict[str, Any], receipt: Dict[str, Any]) -> List[Dict[str, str]]:
    product = snapshot.get("product", {})
    case_names = ", ".join(str(item.get("focus_area")) for item in pack.get("cases", []))
    return [
        {
            "artifact": "product_snapshot_tqqq_case_study",
            "reviewer_use": f"Source-attributed static snapshot for {product.get('ticker')} product terms and educational warnings.",
            "boundary": "Static fixture only; it does not make a live product recommendation.",
        },
        {
            "artifact": "scenario_pack",
            "reviewer_use": f"Deterministic family scenarios covering {case_names}.",
            "boundary": "Modeled examples only; path outcomes are not forecasts or execution instructions.",
        },
        {
            "artifact": "scenario_pack_reviewer_receipt",
            "reviewer_use": f"Hash receipt covering {receipt.get('summary', {}).get('fixture_inputs')} fixtures and generated scenario artifacts.",
            "boundary": "Reproducibility evidence only; hashes do not certify suitability or live-market accuracy.",
        },
    ]


def _fixture_provenance(source_artifacts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [item for item in source_artifacts if "/fixtures/" in item["path"] or item["path"].startswith("examples/fixtures/")]


def _product_family_examples(fixture_root: Path, filenames: List[str]) -> List[Dict[str, Any]]:
    examples = []
    for filename in filenames:
        product = _load_json(fixture_root / filename)
        examples.append(
            {
                "fixture": (fixture_root / filename).as_posix(),
                "name": str(product.get("name", "")),
                "ticker": str(product.get("ticker", "")),
                "underlying": str(product.get("underlying", "")),
                "leverage": product.get("leverage"),
                "reset_frequency": str(product.get("reset_frequency", "daily")),
                "annual_fee": product.get("annual_fee"),
                "boundary": "Static educational fixture only; not a listed-product recommendation or trading instruction.",
            }
        )
    return examples


def _source_artifacts(paths: List[Path]) -> List[Dict[str, Any]]:
    artifacts = []
    for path in paths:
        data = path.read_bytes()
        artifacts.append(
            {
                "path": path.as_posix(),
                "kind": path.suffix.lstrip(".") or "file",
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    return artifacts


def _load_json(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a JSON object")
    return data


def _not_advice() -> str:
    return (
        "This walkthrough is for deterministic artifact review and education only. "
        "It is not investment advice, a recommendation, or a suitability determination."
    )
