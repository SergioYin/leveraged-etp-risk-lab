from __future__ import annotations

import html
import json
from pathlib import Path
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


def exposure_markdown(data: Dict[str, Any]) -> str:
    summary = data["summary"]
    portfolio = data["portfolio"]
    lines: List[str] = [
        f"# Exposure Report: {portfolio['name']}",
        "",
        f"- Base currency: {portfolio['base_currency']}",
        f"- Starting value: {summary['starting_value']}",
        f"- Ending value: {summary['ending_value']}",
        f"- Return: {summary['return_pct']}%",
        f"- Weighted exposure: {summary['weighted_exposure']}x",
        f"- Worst drawdown approximation: {summary['worst_drawdown_pct']}%",
        "",
        "## Positions",
        "",
        _table_with_headers(
            data["positions"],
            ["id", "ticker", "notional", "notional_weight_pct", "leverage", "weighted_exposure", "ending_value", "return_pct"],
        ),
        "",
        "## Stop Events",
        "",
    ]
    if data["stop_events"]:
        for event in data["stop_events"]:
            lines.append(
                f"- {event['position_id']} ({event['ticker']}), day {event['day']} ({event['label']}): "
                f"{event['event']} at NAV {event['nav']}"
            )
    else:
        lines.append("- None")
    lines.extend(["", "## Portfolio Path", "", _table_with_headers(data["portfolio_path"], ["day", "value"]), "", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in data["warnings"])
    return "\n".join(lines) + "\n"


def pretrade_plan_packet(
    simulation: Dict[str, Any],
    thesis: str,
    max_loss_budget: float,
    checklist_profile: str,
    assumptions: List[str],
    provenance: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": "0.3",
        "document_type": "pretrade_plan",
        "not_investment_advice": (
            "This decision packet is for scenario planning and education only. "
            "It is not investment advice, a recommendation, or a suitability determination."
        ),
        "product": simulation["product"],
        "scenario": {
            "days": simulation["inputs"]["days"],
            "ending_etp_nav": simulation["summary"]["ending_etp_nav"],
            "etp_return_pct": simulation["summary"]["etp_return_pct"],
            "underlying_return_pct": simulation["summary"]["underlying_return_pct"],
            "path_decay_vs_simple_multiple": simulation["summary"]["path_decay_vs_simple_multiple"],
        },
        "risk_bands": {
            "stop_loss_pct": simulation["inputs"]["stop_loss_pct"],
            "take_profit_pct": simulation["inputs"]["take_profit_pct"],
            "band_events": simulation["band_events"],
        },
        "budget": {
            "max_loss_budget": round(float(max_loss_budget), 6),
            "currency": simulation["product"]["currency"],
        },
        "thesis": thesis.strip() or "No thesis text provided.",
        "assumptions": assumptions,
        "checklist": {"profile": checklist_profile, "items": checklist_items(checklist_profile)},
        "warnings": _unique_text(
            simulation["warnings"]
            + [
                "A pretrade plan does not confirm liquidity, execution quality, tax treatment, or suitability.",
                "Stop-loss and take-profit bands are planning levels, not guaranteed execution prices.",
            ]
        ),
        "provenance": provenance,
    }


def pretrade_plan_markdown(data: Dict[str, Any]) -> str:
    product = data["product"]
    scenario = data["scenario"]
    budget = data["budget"]
    risk_bands = data["risk_bands"]
    lines: List[str] = [
        f"# Pretrade Plan: {product['ticker']}",
        "",
        f"**Not investment advice:** {data['not_investment_advice']}",
        "",
        "## Product",
        "",
        f"- Product: {product['name']}",
        f"- Underlying: {product['underlying']}",
        f"- Daily leverage: {product['leverage']}x",
        f"- Reset frequency: {product['reset_frequency']}",
        f"- Annual fee: {product['annual_fee_pct']}%",
        "",
        "## Thesis",
        "",
        data["thesis"],
        "",
        "## Scenario Summary",
        "",
        f"- Scenario days: {scenario['days']}",
        f"- Ending ETP NAV: {scenario['ending_etp_nav']}",
        f"- ETP return: {scenario['etp_return_pct']}%",
        f"- Underlying return: {scenario['underlying_return_pct']}%",
        f"- Path decay vs simple multiple: {scenario['path_decay_vs_simple_multiple']}",
        "",
        "## Risk Budget And Bands",
        "",
        f"- Maximum loss budget: {budget['max_loss_budget']} {budget['currency']}",
        f"- Stop-loss band: {_display_pct(risk_bands['stop_loss_pct'])}",
        f"- Take-profit band: {_display_pct(risk_bands['take_profit_pct'])}",
        "",
        "### Band Events",
        "",
    ]
    if risk_bands["band_events"]:
        for event in risk_bands["band_events"]:
            lines.append(f"- Day {event['day']} ({event['label']}): {event['event']} at NAV {event['nav']}")
    else:
        lines.append("- None in modeled path")
    lines.extend(["", "## Assumptions", ""])
    lines.extend(f"- {item}" for item in data["assumptions"])
    lines.extend(["", "## Checklist", ""])
    lines.extend(f"- [ ] {item}" for item in data["checklist"]["items"])
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in data["warnings"])
    lines.extend(["", "## Command Provenance", ""])
    for key in sorted(data["provenance"]):
        lines.append(f"- {key}: {data['provenance'][key]}")
    return "\n".join(lines) + "\n"


def checklist_markdown(profile: str) -> str:
    items = checklist_items(profile)
    lines = [f"# Leveraged ETP Risk Checklist: {profile}", ""]
    lines.extend(f"- [ ] {item}" for item in items)
    return "\n".join(lines) + "\n"


def checklist_json(profile: str) -> str:
    return to_json({"schema_version": "0.2", "profile": profile, "items": checklist_items(profile)})


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
            "commands": [
                "simulate",
                "generate-scenario",
                "exposure-report",
                "pretrade-plan",
                "static-dashboard",
                "checklist",
                "demo-bundle",
                "selfcheck",
                "version-report",
            ],
        }
    )


def dashboard_html(data: Dict[str, Any], title: str, provenance: Dict[str, Any]) -> str:
    summary = data.get("summary", {})
    portfolio = data.get("portfolio", {"name": title, "base_currency": "USD"})
    positions = data.get("positions", [])
    warnings = data.get("warnings", [])
    simulations = data.get("simulations", [])
    cards = [
        ("Starting Value", summary.get("starting_value", "n/a")),
        ("Ending Value", summary.get("ending_value", "n/a")),
        ("Return", _suffix(summary.get("return_pct"), "%")),
        ("Weighted Exposure", _suffix(summary.get("weighted_exposure"), "x")),
        ("Worst Drawdown", _suffix(summary.get("worst_drawdown_pct"), "%")),
    ]
    if not positions:
        for simulation in simulations:
            product = simulation.get("product", {})
            scenario = simulation.get("summary", {})
            positions.append(
                {
                    "id": product.get("ticker", "simulation"),
                    "ticker": product.get("ticker", "n/a"),
                    "product": product.get("name", "Simulation"),
                    "notional": "n/a",
                    "leverage": product.get("leverage", "n/a"),
                    "ending_value": scenario.get("ending_etp_nav", "n/a"),
                    "return_pct": scenario.get("etp_return_pct", "n/a"),
                    "stop_loss_pct": simulation.get("inputs", {}).get("stop_loss_pct"),
                    "take_profit_pct": simulation.get("inputs", {}).get("take_profit_pct"),
                }
            )
            warnings.extend(simulation.get("warnings", []))
    warning_items = _unique_text([str(item) for item in warnings])
    rows = [
        [
            position.get("id", ""),
            position.get("ticker", ""),
            position.get("product", ""),
            position.get("notional", ""),
            _suffix(position.get("leverage"), "x"),
            position.get("ending_value", ""),
            _suffix(position.get("return_pct"), "%"),
            _display_pct(position.get("stop_loss_pct")),
            _display_pct(position.get("take_profit_pct")),
        ]
        for position in positions
    ]
    stop_events = data.get("stop_events", [])
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{_e(title)}</title>",
            "<style>",
            "body{margin:0;font-family:Arial,Helvetica,sans-serif;color:#182026;background:#f6f7f4;line-height:1.45}",
            "header{background:#15332f;color:#fff;padding:28px 32px}",
            "main{max-width:1120px;margin:0 auto;padding:28px 20px 44px}",
            "h1,h2{margin:0 0 12px} h1{font-size:30px} h2{font-size:20px;margin-top:28px}",
            ".meta{color:#d7e7df}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}",
            ".card{background:#fff;border:1px solid #d7ddd6;border-radius:8px;padding:14px}",
            ".label{font-size:12px;color:#5d6a66;text-transform:uppercase}.value{font-size:23px;font-weight:700;margin-top:6px}",
            "table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #d7ddd6;border-radius:8px;overflow:hidden}",
            "th,td{text-align:left;padding:10px;border-bottom:1px solid #e6eae5;font-size:14px}th{background:#e8eee8}",
            ".warn{background:#fff4d6;border-left:4px solid #b57900;padding:10px 12px;margin:8px 0}",
            ".provenance{background:#fff;border:1px solid #d7ddd6;border-radius:8px;padding:14px}",
            "</style>",
            "</head>",
            "<body>",
            "<header>",
            f"<h1>{_e(title)}</h1>",
            f"<div class=\"meta\">{_e(portfolio.get('name', title))} · {_e(portfolio.get('base_currency', 'USD'))} · No JavaScript</div>",
            "</header>",
            "<main>",
            "<section class=\"cards\">",
            "".join(f"<div class=\"card\"><div class=\"label\">{_e(label)}</div><div class=\"value\">{_e(value)}</div></div>" for label, value in cards),
            "</section>",
            "<h2>Positions</h2>",
            _html_table(["ID", "Ticker", "Product", "Notional", "Leverage", "Ending Value", "Return", "Stop", "Take"], rows),
            "<h2>Band Events</h2>",
            _event_list(stop_events),
            "<h2>Warnings</h2>",
            "".join(f"<div class=\"warn\">{_e(item)}</div>" for item in warning_items) or "<p>None.</p>",
            "<h2>Command Provenance</h2>",
            "<div class=\"provenance\">",
            "".join(f"<p><strong>{_e(key)}:</strong> {_e(provenance[key])}</p>" for key in sorted(provenance)),
            "</div>",
            "</main>",
            "</body>",
            "</html>",
            "",
        ]
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


def load_demo_outputs(input_dir: Path) -> Dict[str, Any]:
    simulations: List[Dict[str, Any]] = []
    portfolio = None
    for path in sorted(input_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if "portfolio" in data and "positions" in data:
            portfolio = data
        elif "product" in data and "summary" in data:
            simulations.append(data)
    if portfolio is not None:
        portfolio = dict(portfolio)
        portfolio["simulations"] = simulations
        return portfolio
    return {
        "schema_version": "0.3",
        "portfolio": {"name": "Demo Simulation Outputs", "base_currency": "USD"},
        "summary": {
            "starting_value": "n/a",
            "ending_value": "n/a",
            "return_pct": "n/a",
            "weighted_exposure": "n/a",
            "worst_drawdown_pct": "n/a",
        },
        "positions": [],
        "stop_events": [],
        "warnings": [],
        "simulations": simulations,
    }


def default_pretrade_assumptions() -> List[str]:
    return [
        "Scenario path is deterministic fixture data, not a forecast.",
        "Modeled NAV starts at 100 and applies daily reset leverage once per scenario row.",
        "Fees are approximated as a constant daily deduction from leveraged daily return.",
        "Risk bands are evaluated on modeled end-of-day NAV values.",
        "The maximum loss budget is supplied by the user and is not a sizing recommendation.",
    ]


def _display_pct(value: Any) -> str:
    if value is None:
        return "not set"
    return f"{value}%"


def _suffix(value: Any, suffix: str) -> str:
    if value is None:
        return "n/a"
    if value == "n/a":
        return "n/a"
    return f"{value}{suffix}"


def _e(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _html_table(headers: List[str], rows: List[List[Any]]) -> str:
    head = "".join(f"<th>{_e(header)}</th>" for header in headers)
    if not rows:
        body = f"<tr><td colspan=\"{len(headers)}\">No positions found.</td></tr>"
    else:
        body = "".join("<tr>" + "".join(f"<td>{_e(value)}</td>" for value in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def _event_list(events: List[Dict[str, Any]]) -> str:
    if not events:
        return "<p>None.</p>"
    items = []
    for event in events:
        position = event.get("position_id", event.get("ticker", "position"))
        items.append(
            f"<div class=\"warn\">{_e(position)} day {_e(event.get('day', ''))}: "
            f"{_e(event.get('event', 'band_event'))} at NAV {_e(event.get('nav', ''))}</div>"
        )
    return "".join(items)


def _unique_text(items: List[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _table_with_headers(rows: Iterable[Dict[str, Any]], headers: List[str]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[key]) for key in headers) + " |")
    return "\n".join(lines)
