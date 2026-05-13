from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


SCHEMA_VERSION = "0.15"


FIELD_LABELS = {
    "issuer": "Issuer",
    "exchange": "Exchange",
    "underlying": "Underlying",
    "leverage_factor": "Leverage factor",
    "daily_reset": "Daily reset wording",
    "fee": "Fee",
    "currency": "Currency",
    "liquidity_spread": "Liquidity/spread placeholder",
    "inav": "iNAV field",
    "premium_discount": "Premium/discount field",
}

FIELD_ALIASES = {
    "issuer": ["issuer", "sponsor", "provider"],
    "exchange": ["exchange", "listing_exchange", "primary_exchange"],
    "underlying": ["underlying"],
    "leverage_factor": ["leverage", "leverage_factor"],
    "fee": ["annual_fee", "fee", "expense_ratio", "management_fee"],
    "currency": ["currency"],
    "liquidity_spread": ["liquidity", "spread", "bid_ask_spread", "average_daily_volume", "adv"],
    "inav": ["inav", "indicative_nav", "intraday_indicative_value"],
    "premium_discount": ["premium_discount", "premium_discount_url", "premium_discount_history"],
}

TEXT_MARKERS = {
    "issuer": ["issuer", "sponsor", "provider"],
    "exchange": ["exchange", "listed on", "listing"],
    "underlying": ["underlying", "reference index", "reference share"],
    "leverage_factor": ["leverage", "leveraged", "2x", "3x", "-2x"],
    "daily_reset": ["daily reset", "daily-reset", "resets daily", "reset daily", "daily objective"],
    "fee": ["fee", "expense ratio", "management fee"],
    "currency": ["currency", "usd", "eur", "gbp", "jpy", "cad", "aud"],
    "liquidity_spread": ["liquidity", "spread", "bid-ask", "bid ask", "average daily volume", "adv"],
    "inav": ["inav", "indicative nav", "intraday indicative"],
    "premium_discount": ["premium/discount", "premium discount", "premium-discount", "discount history"],
}


def factsheet_check(product_path: str, factsheet_path: Optional[str] = None) -> Dict[str, Any]:
    product = _load_json_object(product_path)
    factsheet_text = Path(factsheet_path).read_text(encoding="utf-8") if factsheet_path else ""
    checks = [_field_check(field, product, factsheet_text) for field in FIELD_LABELS]
    missing_fields = [check["field"] for check in checks if check["status"] == "missing"]
    review_fields = [check["field"] for check in checks if check["status"] == "review"]
    return {
        "schema_version": SCHEMA_VERSION,
        "document_type": "factsheet_check",
        "not_investment_advice": (
            "This factsheet checklist is for educational product-term review only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "inputs": {
            "product": _display_path(product_path),
            "factsheet_file": _display_path(factsheet_path) if factsheet_path else None,
        },
        "product": {
            "name": product.get("name"),
            "ticker": product.get("ticker"),
        },
        "summary": {
            "checks": len(checks),
            "passed": len([check for check in checks if check["status"] == "pass"]),
            "review": len(review_fields),
            "missing": len(missing_fields),
            "ready_for_review": not missing_fields,
        },
        "checks": checks,
        "missing_fields": missing_fields,
        "provenance": {
            "command": "factsheet-check",
            "product": _display_path(product_path),
            "factsheet_file": _display_path(factsheet_path) if factsheet_path else None,
        },
    }


def factsheet_check_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Product Factsheet Checklist",
        "",
        f"- Schema version: {data['schema_version']}",
        f"- Product: {_display_value(data['product'].get('name'))}",
        f"- Ticker: {_display_value(data['product'].get('ticker'))}",
        f"- Ready for review: {'yes' if summary['ready_for_review'] else 'no'}",
        f"- Checks: {summary['passed']} passed, {summary['review']} review, {summary['missing']} missing",
        "",
        "## Checklist",
        "",
        "| Field | Status | Source | Value |",
        "| --- | --- | --- | --- |",
    ]
    for check in data["checks"]:
        evidence = check["evidence"]
        lines.append(
            f"| {check['label']} | {check['status']} | {_display_value(evidence['source'])} | "
            f"{_md_cell(_display_value(evidence['value']))} |"
        )
    lines.extend(["", "## Missing Fields", ""])
    if data["missing_fields"]:
        lines.extend(f"- {field}" for field in data["missing_fields"])
    else:
        lines.append("- None")
    lines.extend(["", "## Notes", "", f"- {data['not_investment_advice']}"])
    return "\n".join(lines) + "\n"


def _field_check(field: str, product: Dict[str, Any], factsheet_text: str) -> Dict[str, Any]:
    if field == "daily_reset":
        return _daily_reset_check(product, factsheet_text)
    value = _first_product_value(product, FIELD_ALIASES[field])
    if value not in (None, ""):
        return _check(field, "pass", "product_json", value, f"{FIELD_LABELS[field]} found in product JSON.")
    if _has_marker(factsheet_text, TEXT_MARKERS[field]):
        if field == "liquidity_spread":
            return _check(
                field,
                "review",
                "factsheet_text",
                "placeholder: verify current liquidity and bid-ask spread before use",
                "Factsheet text includes liquidity or spread language, but no live market data is fetched.",
            )
        value = _factsheet_value(field, factsheet_text) or "mentioned"
        return _check(field, "pass", "factsheet_text", value, f"{FIELD_LABELS[field]} mentioned in factsheet text.")
    if field == "liquidity_spread":
        return _check(
            field,
            "review",
            "placeholder",
            "placeholder: verify current liquidity and bid-ask spread before use",
            "Core package does not fetch live liquidity or spread data.",
        )
    return _check(field, "missing", None, None, f"{FIELD_LABELS[field]} not found in product JSON or factsheet text.")


def _daily_reset_check(product: Dict[str, Any], factsheet_text: str) -> Dict[str, Any]:
    reset_frequency = str(product.get("reset_frequency", "")).strip().lower()
    if reset_frequency == "daily":
        return _check("daily_reset", "pass", "product_json", "reset_frequency=daily", "Product reset frequency is daily.")
    if _has_marker(factsheet_text, TEXT_MARKERS["daily_reset"]):
        return _check("daily_reset", "pass", "factsheet_text", "mentioned", "Factsheet includes daily reset wording.")
    return _check(
        "daily_reset",
        "missing",
        None,
        None,
        "Daily reset wording not found in product JSON or factsheet text.",
    )


def _check(field: str, status: str, source: Optional[str], value: Any, message: str) -> Dict[str, Any]:
    return {
        "field": field,
        "label": FIELD_LABELS[field],
        "status": status,
        "message": message,
        "evidence": {
            "source": source,
            "value": _normalize_value(value),
        },
    }


def _load_json_object(path: str) -> Dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a JSON object")
    return data


def _first_product_value(product: Dict[str, Any], aliases: List[str]) -> Any:
    lower_aliases = {alias.lower() for alias in aliases}
    for key, value in product.items():
        if key.lower() in lower_aliases:
            return value
    return None


def _has_marker(text: str, markers: List[str]) -> bool:
    lower = text.lower()
    return any(marker in lower for marker in markers)


def _factsheet_value(field: str, text: str) -> Optional[str]:
    prefixes = [FIELD_LABELS[field].lower(), *TEXT_MARKERS[field], *FIELD_ALIASES.get(field, [])]
    for line in text.splitlines():
        stripped = line.strip()
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        normalized_key = key.strip().lower()
        if normalized_key in {prefix.lower() for prefix in prefixes}:
            return value.strip() or None
    return None


def _normalize_value(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 6)
    return value


def _display_value(value: Any) -> str:
    if value is None or value == "":
        return "n/a"
    return str(value)


def _display_path(path: Optional[str]) -> Optional[str]:
    if path is None:
        return None
    parsed = Path(path)
    if parsed.is_absolute():
        return parsed.name
    return parsed.as_posix()


def _md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")
