from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .engine import position_size_plan, simulate, stress_matrix
from .factsheet import factsheet_check
from .io import load_path, load_product
from .models import RiskBand, SimulationConfig
from .regimes import regime_ids, regime_path
from .render import default_pretrade_assumptions, pretrade_plan_packet
from .reports import thesis_impact_from_reports, watchlist_build_from_reports
from .risk_profile import risk_profile_packet


SCHEMA_VERSION = "0.17"


def load_recipe(path: str) -> Dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a JSON object")
    return data


def recipe_run(recipe_path: str) -> Dict[str, Any]:
    recipe = load_recipe(recipe_path)
    recipe_dir = Path(recipe_path).parent
    product_label = _required_text(recipe, "product")
    product_path = _resolve_input(recipe_dir, product_label)
    product = load_product(str(product_path))
    profile_id = str(recipe.get("profile", "thesis-review"))
    initial_nav = float(recipe.get("initial_nav", 100.0))
    stop_loss = _optional_float(recipe.get("stop_loss"))
    take_profit = _optional_float(recipe.get("take_profit"))
    account_value = float(recipe["account_value"])
    max_loss_budget, risk_budget_source = _loss_budget(recipe, account_value)
    risk_band = RiskBand(stop_loss=stop_loss, take_profit=take_profit)

    primary_path_label, path_rows = _primary_path(recipe, recipe_dir)
    scenario = simulate(SimulationConfig(product, path_rows, initial_nav, risk_band))
    factsheet = None
    factsheet_label = _optional_text(recipe.get("factsheet_note") or recipe.get("factsheet_file"))
    if factsheet_label:
        factsheet = factsheet_check(str(product_path), str(_resolve_input(recipe_dir, factsheet_label)))
    profile = risk_profile_packet(profile_id)
    pretrade = pretrade_plan_packet(
        simulation=scenario,
        thesis=_load_optional_text(recipe, recipe_dir, "thesis_file") or str(recipe.get("thesis_text", "")),
        max_loss_budget=max_loss_budget,
        checklist_profile=str(recipe.get("checklist_profile", "risk-review")),
        assumptions=default_pretrade_assumptions(),
        provenance={
            "command": "recipe-run:pretrade-plan",
            "product": product_label,
            "path": primary_path_label,
            "thesis_file": recipe.get("thesis_file", ""),
            "max_loss_budget": max_loss_budget,
            "initial_nav": initial_nav,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "checklist_profile": str(recipe.get("checklist_profile", "risk-review")),
        },
    )
    sizing = position_size_plan(
        simulation=pretrade,
        account_value=account_value,
        max_loss_budget=max_loss_budget,
        stop_loss=stop_loss,
        source={
            "command": "recipe-run:position-size",
            "source": "recipe_pretrade_plan",
            "recipe": _display_path(recipe_path),
            "account_value": account_value,
            "risk_budget_pct": recipe.get("risk_budget_pct"),
            "max_loss_budget": recipe.get("max_loss_budget"),
            "stop_loss": stop_loss,
        },
    )
    stress = _stress_component(recipe, product, product_label, initial_nav, risk_band)
    thesis = None
    watchlist = None
    thesis_label = _optional_text(recipe.get("thesis_file"))
    thesis_text = _load_optional_text(recipe, recipe_dir, "thesis_file")
    if thesis_text:
        thesis_artifacts = [
            ("recipe:pretrade_plan", pretrade),
            ("recipe:position_size", sizing),
        ]
        if stress:
            thesis_artifacts.append(("recipe:stress_matrix", stress))
        thesis = thesis_impact_from_reports(thesis_text, thesis_label or "recipe thesis", thesis_artifacts, "recipe-run:thesis-impact")
        if stress:
            watchlist = watchlist_build_from_reports(
                thesis,
                stress,
                "recipe:thesis_impact",
                "recipe:stress_matrix",
                "recipe-run:watchlist-build",
            )

    components = _components(factsheet, profile, scenario, stress, sizing, pretrade, thesis, watchlist)
    return {
        "schema_version": SCHEMA_VERSION,
        "document_type": "recipe_run",
        "not_investment_advice": (
            "This recipe bundle is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "inputs": {
            "recipe": _display_path(recipe_path),
            "product": product_label,
            "path": primary_path_label,
            "factsheet_note": factsheet_label,
            "profile": profile_id,
            "account_value": round(account_value, 6),
            "max_loss_budget": round(max_loss_budget, 6),
            "risk_budget_source": risk_budget_source,
            "thesis_file": thesis_label,
            "stress_regimes": stress["inputs"]["regimes"] if stress else [],
        },
        "summary": {
            "product": scenario["product"]["ticker"],
            "scenario_days": scenario["inputs"]["days"],
            "scenario_return_pct": scenario["summary"]["etp_return_pct"],
            "path_decay_vs_simple_multiple": scenario["summary"]["path_decay_vs_simple_multiple"],
            "recommended_notional": sizing["recommendation"]["recommended_notional"],
            "components": len(components),
            "watchlist_entries": watchlist["summary"]["entries"] if watchlist else 0,
        },
        "workflow": _workflow(recipe, product_label, primary_path_label, factsheet_label, thesis_label, stress),
        "components": components,
        "artifacts": {
            "factsheet_check": factsheet,
            "risk_profile": profile,
            "simulation": scenario,
            "stress_matrix": stress,
            "position_size": sizing,
            "pretrade_plan": pretrade,
            "thesis_impact": thesis,
            "watchlist": watchlist,
        },
        "provenance": {
            "command": "recipe-run",
            "recipe": _display_path(recipe_path),
            "shell_out": False,
        },
    }


def recipe_run_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    lines = [
        "# Recipe Run",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Summary",
        "",
        f"- Product: {summary['product']}",
        f"- Scenario days: {summary['scenario_days']}",
        f"- Scenario return: {summary['scenario_return_pct']}%",
        f"- Path decay vs simple multiple: {summary['path_decay_vs_simple_multiple']}",
        f"- Recommended notional: {summary['recommended_notional']}",
        f"- Watchlist entries: {summary['watchlist_entries']}",
        "",
        "## Conceptual Workflow",
        "",
    ]
    for step in data["workflow"]:
        lines.append(f"- {step['step']}: `{step['command']}`")
    lines.extend(["", "## Components", "", "| Component | Type | Schema | Summary |", "| --- | --- | --- | --- |"])
    for item in data["components"]:
        lines.append(f"| {item['id']} | {item['document_type']} | {item['schema_version']} | {_md_cell(item['summary'])} |")
    lines.extend(["", "## Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def _primary_path(recipe: Dict[str, Any], recipe_dir: Path) -> tuple[str, List[Any]]:
    path_label = _optional_text(recipe.get("path"))
    regime = _optional_text(recipe.get("regime"))
    if path_label and regime:
        raise ValueError("recipe must provide only one of path or regime")
    if path_label:
        return path_label, load_path(str(_resolve_input(recipe_dir, path_label)))
    if regime:
        if regime not in regime_ids():
            raise ValueError(f"unknown regime: {regime}")
        return f"regime:{regime}", regime_path(regime)
    raise ValueError("recipe must provide path or regime")


def _stress_component(
    recipe: Dict[str, Any],
    product: Any,
    product_label: str,
    initial_nav: float,
    risk_band: RiskBand,
) -> Optional[Dict[str, Any]]:
    selected = recipe.get("stress_regimes")
    if selected is None:
        selected = recipe.get("regimes")
    if selected is False:
        return None
    regimes = None
    if selected is not None:
        if not isinstance(selected, list):
            raise ValueError("stress_regimes must be a list when provided")
        regimes = [str(item) for item in selected]
    return stress_matrix(product, regimes, initial_nav, risk_band, product_label)


def _components(*items: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result = []
    for item in items:
        if not item:
            continue
        document_type = str(item.get("document_type", "simulation_output" if "summary" in item else "unknown"))
        result.append(
            {
                "id": _component_id(document_type),
                "document_type": document_type,
                "schema_version": item.get("schema_version"),
                "summary": _component_summary(item),
            }
        )
    return result


def _workflow(
    recipe: Dict[str, Any],
    product: str,
    path: str,
    factsheet: Optional[str],
    thesis: Optional[str],
    stress: Optional[Dict[str, Any]],
) -> List[Dict[str, str]]:
    steps = []
    if factsheet:
        steps.append({"step": "factsheet-check", "command": f"factsheet-check --product {product} --factsheet-file {factsheet}"})
    steps.append({"step": "risk-profile", "command": f"risk-profile --profile {recipe.get('profile', 'thesis-review')}"})
    steps.append({"step": "simulate", "command": f"simulate --product {product} --path {path}"})
    if stress:
        regime_flags = " ".join(f"--regime {item}" for item in stress["inputs"]["regimes"])
        steps.append({"step": "stress-matrix", "command": f"stress-matrix --product {product} {regime_flags}".strip()})
    steps.append({"step": "position-size", "command": "position-size --pretrade-plan recipe:pretrade_plan"})
    steps.append({"step": "pretrade-plan", "command": f"pretrade-plan --product {product} --path {path}"})
    if thesis:
        steps.append({"step": "thesis-impact", "command": f"thesis-impact --thesis-file {thesis} --artifact recipe:pretrade_plan"})
        if stress:
            steps.append({"step": "watchlist-build", "command": "watchlist-build --thesis-impact recipe:thesis_impact --stress-matrix recipe:stress_matrix"})
    return steps


def _component_id(document_type: str) -> str:
    if document_type == "risk_profile_rules":
        return "risk_profile"
    if document_type == "recipe_run":
        return "recipe"
    return document_type


def _component_summary(item: Dict[str, Any]) -> str:
    kind = item.get("document_type")
    if kind == "factsheet_check":
        summary = item["summary"]
        return f"{summary['passed']} passed, {summary['review']} review, {summary['missing']} missing"
    if kind == "risk_profile_rules":
        return f"{item['summary']['profiles']} profile(s)"
    if kind == "stress_matrix":
        return f"{len(item['rows'])} regimes"
    if kind == "position_size_plan":
        return f"recommended notional {item['recommendation']['recommended_notional']}"
    if kind == "pretrade_plan":
        return f"max loss budget {item['budget']['max_loss_budget']}"
    if kind == "thesis_impact":
        return f"{item['thesis']['claim_count']} claim(s)"
    if kind == "watchlist":
        return f"{item['summary']['entries']} entries"
    if "summary" in item and "product" in item:
        return f"scenario return {item['summary']['etp_return_pct']}%"
    return "included"


def _loss_budget(recipe: Dict[str, Any], account_value: float) -> tuple[float, str]:
    if account_value <= 0:
        raise ValueError("account_value must be positive")
    has_pct = recipe.get("risk_budget_pct") is not None
    has_max = recipe.get("max_loss_budget") is not None
    if has_pct == has_max:
        raise ValueError("recipe must provide exactly one of risk_budget_pct or max_loss_budget")
    if has_pct:
        pct_value = float(recipe["risk_budget_pct"])
        if not 0 < pct_value <= 1:
            raise ValueError("risk_budget_pct must be a decimal between 0 and 1")
        return account_value * pct_value, "risk_budget_pct"
    max_loss = float(recipe["max_loss_budget"])
    if max_loss <= 0 or max_loss > account_value:
        raise ValueError("max_loss_budget must be positive and not exceed account_value")
    return max_loss, "max_loss_budget"


def _required_text(data: Dict[str, Any], key: str) -> str:
    value = _optional_text(data.get(key))
    if not value:
        raise ValueError(f"recipe is missing {key}")
    return value


def _optional_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _optional_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    return float(value)


def _resolve_input(recipe_dir: Path, value: str) -> Path:
    path = Path(value)
    if path.exists() or path.is_absolute():
        return path
    return recipe_dir / path


def _load_optional_text(recipe: Dict[str, Any], recipe_dir: Path, key: str) -> str:
    value = _optional_text(recipe.get(key))
    if not value:
        return ""
    return _resolve_input(recipe_dir, value).read_text(encoding="utf-8").strip()


def _display_path(path: str) -> str:
    text = str(path)
    return Path(text).name if Path(text).is_absolute() else text


def _md_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")
