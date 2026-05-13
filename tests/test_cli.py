import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from leveraged_etp_risk_lab import __version__


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "leveraged_etp_risk_lab", *args],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_version_report(self):
        result = self.run_cli("version-report")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["version"], __version__)
        self.assertIn("simulate", data["commands"])
        self.assertIn("generate-scenario", data["commands"])
        self.assertIn("exposure-report", data["commands"])
        self.assertIn("pretrade-plan", data["commands"])
        self.assertIn("position-size", data["commands"])
        self.assertIn("stress-matrix", data["commands"])
        self.assertIn("compare-runs", data["commands"])
        self.assertIn("run-ledger", data["commands"])
        self.assertIn("thesis-impact", data["commands"])
        self.assertIn("watchlist-build", data["commands"])
        self.assertIn("static-dashboard", data["commands"])
        self.assertIn("template-list", data["commands"])
        self.assertIn("template-export", data["commands"])
        self.assertIn("regime-list", data["commands"])
        self.assertIn("regime-export", data["commands"])
        self.assertIn("demo-story", data["commands"])
        self.assertIn("gallery-index", data["commands"])
        self.assertIn("package-audit", data["commands"])
        self.assertIn("explain-term", data["commands"])
        self.assertIn("glossary-list", data["commands"])
        self.assertIn("factsheet-check", data["commands"])

    def test_simulate_json(self):
        result = self.run_cli(
            "simulate",
            "--product",
            "examples/fixtures/leveraged_nasdaq_3x.json",
            "--path",
            "examples/fixtures/nasdaq_chop_path.csv",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["product"]["ticker"], "NDAQ3X")

    def test_demo_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli("demo-bundle", "--output-dir", tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((Path(tmp) / "leveraged_nasdaq_3x.json").exists())
            self.assertTrue((Path(tmp) / "portfolio_exposure.json").exists())
            self.assertTrue((Path(tmp) / "checklist.md").exists())
            self.assertTrue((Path(tmp) / "pretrade_plan.json").exists())
            self.assertTrue((Path(tmp) / "position_size.json").exists())
            self.assertTrue((Path(tmp) / "position_size.md").exists())
            self.assertTrue((Path(tmp) / "stress_matrix.json").exists())
            self.assertTrue((Path(tmp) / "stress_matrix.md").exists())
            self.assertTrue((Path(tmp) / "compare_runs.json").exists())
            self.assertTrue((Path(tmp) / "compare_runs.md").exists())
            self.assertTrue((Path(tmp) / "run_ledger.jsonl").exists())
            self.assertTrue((Path(tmp) / "thesis_impact.json").exists())
            self.assertTrue((Path(tmp) / "thesis_impact.md").exists())
            self.assertTrue((Path(tmp) / "watchlist.json").exists())
            self.assertTrue((Path(tmp) / "watchlist.md").exists())
            self.assertTrue((Path(tmp) / "factsheet_check.json").exists())
            self.assertTrue((Path(tmp) / "factsheet_check.md").exists())
            self.assertTrue((Path(tmp) / "demo_story.json").exists())
            self.assertTrue((Path(tmp) / "demo_story.md").exists())
            self.assertTrue((Path(tmp) / "gallery_index.json").exists())
            self.assertTrue((Path(tmp) / "gallery_index.md").exists())
            self.assertTrue((Path(tmp) / "dashboard.html").exists())
            self.assertTrue((Path(tmp) / "template_gallery.json").exists())
            self.assertTrue((Path(tmp) / "template_gallery.md").exists())
            self.assertTrue((Path(tmp) / "regime_gallery.json").exists())
            self.assertTrue((Path(tmp) / "regime_gallery.md").exists())
            self.assertTrue((Path(tmp) / "regime_trend_up.csv").exists())
            self.assertTrue((Path(tmp) / "package_audit.json").exists())
            self.assertTrue((Path(tmp) / "package_audit.md").exists())
            self.assertTrue((Path(tmp) / "glossary.json").exists())
            self.assertTrue((Path(tmp) / "glossary.md").exists())

    def test_generate_scenario_writes_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "trend.csv"
            result = self.run_cli("generate-scenario", "--kind", "trend", "--days", "3", "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("wrote trend scenario", result.stdout)
            self.assertEqual(output.read_text(encoding="utf-8").splitlines()[0], "day,label,underlying_return")

    def test_exposure_report_json(self):
        result = self.run_cli("exposure-report", "--manifest", "examples/fixtures/portfolio_manifest.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["portfolio"]["name"], "Generic Leveraged ETP Portfolio")
        self.assertEqual(data["summary"]["weighted_exposure"], 2.6)

    def test_pretrade_plan_json(self):
        result = self.run_cli(
            "pretrade-plan",
            "--product",
            "examples/fixtures/leveraged_nasdaq_3x.json",
            "--path",
            "examples/fixtures/nasdaq_chop_path.csv",
            "--thesis-file",
            "examples/fixtures/thesis_note.md",
            "--max-loss-budget",
            "750",
            "--stop-loss",
            "0.15",
            "--take-profit",
            "0.2",
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.3")
        self.assertEqual(data["document_type"], "pretrade_plan")
        self.assertIn("not investment advice", data["not_investment_advice"].lower())
        self.assertEqual(data["budget"]["max_loss_budget"], 750.0)
        self.assertEqual(data["risk_bands"]["stop_loss_pct"], 15.0)

    def test_position_size_json_from_product_path(self):
        result = self.run_cli(
            "position-size",
            "--product",
            "examples/fixtures/leveraged_nasdaq_3x.json",
            "--path",
            "examples/fixtures/nasdaq_chop_path.csv",
            "--account-value",
            "50000",
            "--risk-budget-pct",
            "0.015",
            "--stop-loss",
            "0.15",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.8")
        self.assertEqual(data["document_type"], "position_size_plan")
        self.assertEqual(data["inputs"]["max_loss_budget"], 750.0)
        self.assertEqual(data["inputs"]["stop_loss_pct"], 15.0)
        self.assertEqual(data["recommendation"]["recommended_notional"], 5000.0)
        self.assertIsNone(data["recommendation"]["max_shares"])
        self.assertEqual(data["recommendation"]["modeled_loss_at_stop"], 750.0)
        self.assertEqual(data["recommendation"]["exposure_multiple"], 0.3)
        self.assertIn("not investment advice", data["not_investment_advice"].lower())

    def test_position_size_json_from_pretrade_plan(self):
        result = self.run_cli(
            "position-size",
            "--pretrade-plan",
            "examples/outputs/pretrade_plan.json",
            "--account-value",
            "50000",
            "--max-loss-budget",
            "750",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["document_type"], "position_size_plan")
        self.assertEqual(data["provenance"]["source"], "pretrade_plan")
        self.assertEqual(data["inputs"]["loss_basis"], "stop_loss")
        self.assertEqual(data["recommendation"]["recommended_notional"], 5000.0)

    def test_position_size_markdown(self):
        result = self.run_cli(
            "position-size",
            "--product",
            "examples/fixtures/leveraged_nasdaq_3x.json",
            "--path",
            "examples/fixtures/nasdaq_chop_path.csv",
            "--account-value",
            "50000",
            "--max-loss-budget",
            "750",
            "--stop-loss",
            "0.15",
            "--format",
            "markdown",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Position Size Plan", result.stdout)
        self.assertIn("Recommended notional", result.stdout)
        self.assertIn("Max shares placeholder", result.stdout)

    def test_stress_matrix_json(self):
        result = self.run_cli(
            "stress-matrix",
            "--product",
            "examples/fixtures/leveraged_nasdaq_3x.json",
            "--regime",
            "trend_down",
            "--regime",
            "chop",
            "--stop-loss",
            "0.15",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.9")
        self.assertEqual(data["document_type"], "stress_matrix")
        self.assertEqual([row["regime"] for row in data["rows"]], ["trend_down", "chop"])
        self.assertIn("path_decay_vs_simple_multiple", data["rows"][0])
        self.assertIn("worst_drawdown_pct", data["rows"][0])
        self.assertGreaterEqual(data["rows"][0]["stop_events"], 1)

    def test_stress_matrix_markdown(self):
        result = self.run_cli(
            "stress-matrix",
            "--product",
            "examples/fixtures/leveraged_nasdaq_3x.json",
            "--regime",
            "volatility_cluster",
            "--format",
            "markdown",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Stress Matrix", result.stdout)
        self.assertIn("worst_drawdown_pct", result.stdout)
        self.assertIn("volatility_cluster", result.stdout)

    def test_compare_runs_json(self):
        result = self.run_cli(
            "compare-runs",
            "--base",
            "examples/outputs/leveraged_nasdaq_3x.json",
            "--candidate",
            "examples/outputs/single_stock_2x.json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.5")
        self.assertEqual(data["document_type"], "run_comparison")
        self.assertEqual(data["base"]["document_type"], "simulation_output")
        self.assertEqual(data["candidate"]["document_type"], "simulation_output")
        self.assertEqual(data["deltas"]["return_pct"], -15.3635)
        self.assertEqual(data["deltas"]["warnings"]["added"], [])
        self.assertEqual(data["deltas"]["warnings"]["removed"], [])

    def test_compare_runs_markdown(self):
        result = self.run_cli(
            "compare-runs",
            "--base",
            "examples/outputs/pretrade_plan.json",
            "--candidate",
            "examples/outputs/portfolio_exposure.json",
            "--format",
            "markdown",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Run Comparison", result.stdout)
        self.assertIn("weighted_exposure", result.stdout)
        self.assertIn("Warnings Removed", result.stdout)

    def test_run_ledger_appends_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "ledger.jsonl"
            result = self.run_cli(
                "run-ledger",
                "--ledger",
                str(ledger),
                "--artifact",
                "examples/outputs/leveraged_nasdaq_3x.json",
                "--artifact",
                "examples/outputs/pretrade_plan.json",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads(result.stdout)
            self.assertEqual(summary["rows_appended"], 2)
            rows = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(rows[0]["schema_version"], "0.5")
            self.assertEqual(rows[0]["document_type"], "run_ledger_entry")
            self.assertEqual(rows[0]["artifact_name"], "leveraged_nasdaq_3x.json")
            self.assertEqual(rows[0]["artifact_type"], "simulation_output")
            self.assertIn("sha256", rows[0])
            self.assertNotIn("product", rows[0])

    def test_thesis_impact_json(self):
        result = self.run_cli(
            "thesis-impact",
            "--thesis-file",
            "examples/fixtures/thesis_note.md",
            "--artifact",
            "examples/outputs/pretrade_plan.json",
            "--artifact",
            "examples/outputs/portfolio_exposure.json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.6")
        self.assertEqual(data["document_type"], "thesis_impact")
        self.assertEqual(data["inputs"]["thesis_file"], "examples/fixtures/thesis_note.md")
        self.assertGreaterEqual(data["thesis"]["claim_count"], 2)
        self.assertTrue(data["claim_mappings"])
        self.assertTrue(data["action_checklist"])
        self.assertNotIn("product", data["provenance"])

    def test_thesis_impact_markdown(self):
        result = self.run_cli(
            "thesis-impact",
            "--thesis-file",
            "examples/fixtures/thesis_note.md",
            "--artifact",
            "examples/outputs/pretrade_plan.json",
            "--format",
            "markdown",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Thesis Impact", result.stdout)
        self.assertIn("## Claim Mapping", result.stdout)
        self.assertIn("## Action Checklist", result.stdout)

    def test_watchlist_build_json(self):
        result = self.run_cli(
            "watchlist-build",
            "--thesis-impact",
            "examples/outputs/thesis_impact.json",
            "--stress-matrix",
            "examples/outputs/stress_matrix.json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.10")
        self.assertEqual(data["document_type"], "watchlist")
        self.assertGreaterEqual(data["summary"]["entries"], 8)
        self.assertTrue(any(entry["category"] == "claim" for entry in data["entries"]))
        self.assertTrue(any(entry["category"] == "regime_trigger" for entry in data["entries"]))
        self.assertTrue(all(entry["next_review_questions"] for entry in data["entries"]))
        self.assertTrue(all(entry["source_artifacts"] for entry in data["entries"]))

    def test_factsheet_check_json(self):
        result = self.run_cli(
            "factsheet-check",
            "--product",
            "examples/fixtures/leveraged_nasdaq_3x.json",
            "--factsheet-file",
            "examples/fixtures/factsheet_note.txt",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.15")
        self.assertEqual(data["document_type"], "factsheet_check")
        self.assertEqual(data["inputs"]["factsheet_file"], "examples/fixtures/factsheet_note.txt")
        self.assertEqual(data["summary"]["checks"], 10)
        self.assertEqual(data["summary"]["missing"], 0)
        self.assertIn("not investment advice", data["not_investment_advice"].lower())
        checks = {item["field"]: item for item in data["checks"]}
        self.assertEqual(checks["issuer"]["status"], "pass")
        self.assertEqual(checks["exchange"]["status"], "pass")
        self.assertEqual(checks["underlying"]["evidence"]["source"], "product_json")
        self.assertEqual(checks["liquidity_spread"]["status"], "review")
        self.assertEqual(data["missing_fields"], [])

    def test_factsheet_check_markdown(self):
        result = self.run_cli(
            "factsheet-check",
            "--product",
            "examples/fixtures/leveraged_nasdaq_3x.json",
            "--factsheet-file",
            "examples/fixtures/factsheet_note.txt",
            "--format",
            "markdown",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Product Factsheet Checklist", result.stdout)
        self.assertIn("Liquidity/spread placeholder", result.stdout)
        self.assertIn("## Missing Fields", result.stdout)

    def test_factsheet_check_reports_missing_without_note(self):
        result = self.run_cli(
            "factsheet-check",
            "--product",
            "examples/fixtures/leveraged_nasdaq_3x.json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertIn("issuer", data["missing_fields"])
        self.assertIn("exchange", data["missing_fields"])
        self.assertIn("inav", data["missing_fields"])
        self.assertEqual(data["inputs"]["factsheet_file"], None)

    def test_watchlist_build_markdown(self):
        result = self.run_cli(
            "watchlist-build",
            "--thesis-impact",
            "examples/outputs/thesis_impact.json",
            "--stress-matrix",
            "examples/outputs/stress_matrix.json",
            "--format",
            "markdown",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Thesis Watchlist", result.stdout)
        self.assertIn("Source artifact refs", result.stdout)
        self.assertIn("regime_trigger", result.stdout)

    def test_demo_story_json(self):
        result = self.run_cli("demo-story", "--input-dir", "examples/outputs", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.12")
        self.assertEqual(data["document_type"], "demo_story")
        self.assertEqual(data["provenance"]["command"], "demo-story")
        self.assertIn("problem", data["sections"])
        self.assertIn("workflow", data["sections"])
        self.assertIn("commands", data["sections"])
        self.assertIn("key_outputs", data["sections"])
        self.assertIn("safety_caveats", data["sections"])
        self.assertIn("next_extension_ideas", data["sections"])
        sources = [item["source"] for item in data["sections"]["key_outputs"]]
        self.assertIn("stress_matrix.json", sources)
        self.assertIn("watchlist.json", sources)
        self.assertIn("package_audit.json", sources)
        self.assertIn("pretrade_plan.json", sources)
        self.assertIn("not investment advice", data["not_investment_advice"].lower())

    def test_demo_story_markdown(self):
        result = self.run_cli("demo-story", "--input-dir", "examples/outputs", "--format", "markdown")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Public Demo Story", result.stdout)
        self.assertIn("## Problem", result.stdout)
        self.assertIn("## Workflow", result.stdout)
        self.assertIn("## Commands", result.stdout)
        self.assertIn("## Key Outputs", result.stdout)
        self.assertIn("## Safety Caveats", result.stdout)
        self.assertIn("## Next Extension Ideas", result.stdout)

    def test_gallery_index_json(self):
        result = self.run_cli("gallery-index", "--input-dir", "examples/outputs", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.13")
        self.assertEqual(data["document_type"], "gallery_index")
        self.assertEqual(data["provenance"]["command"], "gallery-index")
        self.assertEqual(
            [stage["stage"] for stage in data["stages"]],
            ["fixtures", "plans", "sizing", "stress", "thesis/watchlist", "audit/story", "dashboard"],
        )
        artifacts = [item for stage in data["stages"] for item in stage["artifacts"]]
        names = {item["name"] for item in artifacts}
        self.assertIn("pretrade_plan.json", names)
        self.assertIn("dashboard.html", names)
        self.assertNotIn("gallery_index.json", names)
        pretrade = next(item for item in artifacts if item["name"] == "pretrade_plan.json")
        self.assertEqual(pretrade["document_type"], "pretrade_plan")
        self.assertEqual(pretrade["schema_version"], "0.3")
        self.assertGreater(pretrade["bytes"], 0)
        self.assertIn("position-size", pretrade["suggested_next_command"])

    def test_gallery_index_markdown(self):
        result = self.run_cli("gallery-index", "--input-dir", "examples/outputs", "--format", "markdown")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Public Gallery Index", result.stdout)
        self.assertIn("## thesis/watchlist", result.stdout)
        self.assertIn("pretrade_plan.json", result.stdout)
        self.assertIn("Suggested next command", result.stdout)

    def test_static_dashboard_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "dashboard.html"
            result = self.run_cli(
                "static-dashboard",
                "--manifest",
                "examples/fixtures/portfolio_manifest.json",
                "--output",
                str(output),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            text = output.read_text(encoding="utf-8")
            self.assertIn("<!doctype html>", text)
            self.assertIn("No JavaScript", text)
            self.assertIn("Command Provenance", text)

    def test_template_list_json(self):
        result = self.run_cli("template-list")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.4")
        self.assertEqual(data["document_type"], "template_gallery")
        self.assertEqual(len(data["templates"]), 4)
        ids = [item["id"] for item in data["templates"]]
        self.assertIn("generic-2x-long-equity", ids)
        self.assertIn("generic-3x-long-index", ids)
        self.assertIn("generic--2x-inverse-index", ids)
        self.assertIn("generic-2x-single-stock", ids)
        self.assertIn("risk_notes", data["templates"][0])
        self.assertIn("use_cases", data["templates"][0])

    def test_template_list_markdown(self):
        result = self.run_cli("template-list", "--format", "markdown")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Product Template Gallery", result.stdout)
        self.assertIn("## generic-3x-long-index", result.stdout)
        self.assertIn("### Risk Notes", result.stdout)
        self.assertIn("### Use Cases", result.stdout)

    def test_template_export_writes_product_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "inverse.json"
            result = self.run_cli(
                "template-export",
                "--template",
                "generic--2x-inverse-index",
                "--output",
                str(output),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(data["ticker"], "INV2X")
            self.assertEqual(data["leverage"], -2)
            self.assertNotIn("risk_notes", data)
            self.assertNotIn("use_cases", data)

    def test_regime_list_json(self):
        result = self.run_cli("regime-list")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.7")
        self.assertEqual(data["document_type"], "regime_gallery")
        self.assertEqual(len(data["regimes"]), 6)
        ids = [item["id"] for item in data["regimes"]]
        self.assertEqual(ids, ["trend_up", "trend_down", "chop", "gap_down", "rebound", "volatility_cluster"])
        self.assertIn("sample_path", data["regimes"][0])
        self.assertIn("risk_notes", data["regimes"][0])
        self.assertIn("use_cases", data["regimes"][0])

    def test_regime_list_markdown(self):
        result = self.run_cli("regime-list", "--format", "markdown")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Market Regime Gallery", result.stdout)
        self.assertIn("## volatility_cluster", result.stdout)
        self.assertIn("### Sample Path", result.stdout)
        self.assertIn("### Risk Notes", result.stdout)

    def test_regime_export_writes_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "gap_down.csv"
            result = self.run_cli("regime-export", "--regime", "gap_down", "--days", "3", "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("wrote gap_down regime with 3 days", result.stdout)
            lines = output.read_text(encoding="utf-8").splitlines()
            self.assertEqual(lines[0], "day,label,underlying_return")
            self.assertEqual(len(lines), 4)
            self.assertIn("Event gap lower", lines[1])

    def test_package_audit_json(self):
        result = self.run_cli("package-audit")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.11")
        self.assertEqual(data["document_type"], "package_audit")
        self.assertEqual(data["package"]["version"], __version__)
        self.assertEqual(data["package"]["dependencies"], [])
        checks = {item["id"]: item for item in data["checks"]}
        self.assertEqual(checks["readme"]["status"], "pass")
        self.assertEqual(checks["license"]["status"], "pass")
        self.assertEqual(checks["schemas"]["status"], "pass")
        self.assertEqual(checks["skill_file"]["status"], "pass")
        self.assertEqual(checks["no_workflows"]["status"], "pass")
        self.assertEqual(checks["zero_dependencies"]["status"], "pass")
        self.assertEqual(checks["version_consistency"]["status"], "pass")
        required_schemas = checks["schemas"]["evidence"]["required"]
        required_examples = checks["examples"]["evidence"]["required"]
        self.assertIn("docs/gallery-index.schema.json", required_schemas)
        self.assertIn("docs/glossary.schema.json", required_schemas)
        self.assertIn("examples/outputs/gallery_index.json", required_examples)
        self.assertIn("examples/outputs/glossary.json", required_examples)
        self.assertIn("docs/factsheet-check.schema.json", required_schemas)
        self.assertIn("examples/outputs/factsheet_check.json", required_examples)
        self.assertTrue(any(command["status"] == "not_run" for command in data["test_commands"]))

    def test_explain_term_json(self):
        result = self.run_cli("explain-term", "daily_reset", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.14")
        self.assertEqual(data["document_type"], "glossary_term")
        self.assertEqual(data["term"]["id"], "daily_reset")
        self.assertIn("daily", data["term"]["plain_language"].lower())
        self.assertIn("not investment advice", data["not_investment_advice"].lower())

    def test_explain_term_markdown(self):
        result = self.run_cli("explain-term", "gap_risk")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Gap risk", result.stdout)
        self.assertIn("Not investment advice", result.stdout)
        self.assertIn("Related terms", result.stdout)

    def test_glossary_list_json(self):
        result = self.run_cli("glossary-list")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.14")
        self.assertEqual(data["document_type"], "glossary")
        ids = [term["id"] for term in data["terms"]]
        self.assertEqual(
            ids,
            [
                "daily_reset",
                "path_decay",
                "volatility_decay",
                "leverage_factor",
                "stop_loss_band",
                "take_profit_band",
                "gap_risk",
                "iNAV",
                "premium_discount",
                "max_loss_budget",
            ],
        )
        self.assertEqual(data["summary"]["terms"], 10)

    def test_glossary_list_markdown(self):
        result = self.run_cli("glossary-list", "--format", "markdown")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Leveraged Product Glossary", result.stdout)
        self.assertIn("## volatility_decay", result.stdout)
        self.assertIn("not investment advice", result.stdout.lower())

    def test_package_audit_markdown(self):
        result = self.run_cli("package-audit", "--format", "markdown")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Package Audit", result.stdout)
        self.assertIn("version_consistency", result.stdout)
        self.assertIn("python -m unittest discover -s tests", result.stdout)

    def test_sync_local_skill_script(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/sync_local_skill.py",
                    "--target-dir",
                    str(Path(tmp) / "skill"),
                ],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            copied = Path(tmp) / "skill" / "SKILL.md"
            self.assertTrue(copied.exists())
            self.assertIn("leveraged-etp-risk-lab Agent Skill", copied.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
