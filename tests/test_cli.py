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
        self.assertIn("sensitivity-grid", data["commands"])
        self.assertIn("portfolio-sensitivity", data["commands"])
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
        self.assertIn("asset-hub", data["commands"])
        self.assertIn("scenario-pack", data["commands"])
        self.assertIn("scenario-pack-reviewer-receipt", data["commands"])
        self.assertIn("scenario-pack-visual-receipt", data["commands"])
        self.assertIn("package-audit", data["commands"])
        self.assertIn("product-snapshot", data["commands"])
        self.assertIn("product-family-walkthrough", data["commands"])
        self.assertIn("schema-inventory", data["commands"])
        self.assertIn("artifact-validate", data["commands"])
        self.assertIn("release-manifest", data["commands"])
        self.assertIn("docs-export", data["commands"])
        self.assertIn("explain-term", data["commands"])
        self.assertIn("glossary-list", data["commands"])
        self.assertIn("factsheet-check", data["commands"])
        self.assertIn("risk-profile", data["commands"])
        self.assertIn("recipe-run", data["commands"])
        self.assertIn("report-card", data["commands"])
        self.assertIn("thesis-dashboard-data", data["commands"])
        self.assertIn("audit-trail", data["commands"])
        self.assertIn("memo-draft", data["commands"])
        self.assertIn("memo-review", data["commands"])
        self.assertIn("cycle-init", data["commands"])
        self.assertIn("cycle-update", data["commands"])
        self.assertIn("guardrail-policy", data["commands"])
        self.assertIn("guardrail-check", data["commands"])
        self.assertIn("order-ticket", data["commands"])
        self.assertIn("order-review", data["commands"])

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
            self.assertTrue((Path(tmp) / "sensitivity_grid.json").exists())
            self.assertTrue((Path(tmp) / "sensitivity_grid.md").exists())
            self.assertTrue((Path(tmp) / "portfolio_sensitivity.json").exists())
            self.assertTrue((Path(tmp) / "portfolio_sensitivity.md").exists())
            self.assertTrue((Path(tmp) / "compare_runs.json").exists())
            self.assertTrue((Path(tmp) / "compare_runs.md").exists())
            self.assertTrue((Path(tmp) / "run_ledger.jsonl").exists())
            self.assertTrue((Path(tmp) / "thesis_impact.json").exists())
            self.assertTrue((Path(tmp) / "thesis_impact.md").exists())
            self.assertTrue((Path(tmp) / "watchlist.json").exists())
            self.assertTrue((Path(tmp) / "watchlist.md").exists())
            self.assertTrue((Path(tmp) / "factsheet_check.json").exists())
            self.assertTrue((Path(tmp) / "factsheet_check.md").exists())
            self.assertTrue((Path(tmp) / "risk_profiles.json").exists())
            self.assertTrue((Path(tmp) / "risk_profiles.md").exists())
            self.assertTrue((Path(tmp) / "recipe_run.json").exists())
            self.assertTrue((Path(tmp) / "recipe_run.md").exists())
            self.assertTrue((Path(tmp) / "report_card.json").exists())
            self.assertTrue((Path(tmp) / "report_card.md").exists())
            self.assertTrue((Path(tmp) / "thesis_dashboard_data.json").exists())
            self.assertTrue((Path(tmp) / "thesis_dashboard_data.md").exists())
            self.assertTrue((Path(tmp) / "investment_memo.json").exists())
            self.assertTrue((Path(tmp) / "investment_memo.md").exists())
            self.assertTrue((Path(tmp) / "audit_trail.json").exists())
            self.assertTrue((Path(tmp) / "audit_trail.md").exists())
            self.assertTrue((Path(tmp) / "investment_memo_review.json").exists())
            self.assertTrue((Path(tmp) / "investment_memo_review.md").exists())
            self.assertTrue((Path(tmp) / "cycle_state.json").exists())
            self.assertTrue((Path(tmp) / "cycle_state.md").exists())
            self.assertTrue((Path(tmp) / "cycle_update.json").exists())
            self.assertTrue((Path(tmp) / "cycle_update.md").exists())
            self.assertTrue((Path(tmp) / "guardrail_policy.json").exists())
            self.assertTrue((Path(tmp) / "guardrail_policy.md").exists())
            self.assertTrue((Path(tmp) / "guardrail_check.json").exists())
            self.assertTrue((Path(tmp) / "guardrail_check.md").exists())
            self.assertTrue((Path(tmp) / "order_ticket.json").exists())
            self.assertTrue((Path(tmp) / "order_ticket.md").exists())
            self.assertTrue((Path(tmp) / "order_review.json").exists())
            self.assertTrue((Path(tmp) / "order_review.md").exists())
            self.assertTrue((Path(tmp) / "demo_story.json").exists())
            self.assertTrue((Path(tmp) / "demo_story.md").exists())
            self.assertTrue((Path(tmp) / "gallery_index.json").exists())
            self.assertTrue((Path(tmp) / "gallery_index.md").exists())
            self.assertTrue((Path(tmp) / "asset_hub.json").exists())
            self.assertTrue((Path(tmp) / "asset_hub.md").exists())
            self.assertTrue((Path(tmp) / "scenario_pack.json").exists())
            self.assertTrue((Path(tmp) / "scenario_pack.md").exists())
            self.assertTrue((Path(tmp) / "daily_reset_path_decay.json").exists())
            self.assertTrue((Path(tmp) / "daily_reset_path_decay.md").exists())
            self.assertTrue((Path(tmp) / "drawdown_risk.json").exists())
            self.assertTrue((Path(tmp) / "drawdown_risk.md").exists())
            self.assertTrue((Path(tmp) / "pretrade_guardrails.json").exists())
            self.assertTrue((Path(tmp) / "pretrade_guardrails.md").exists())
            self.assertTrue((Path(tmp) / "scenario_pack_reviewer_receipt.json").exists())
            self.assertTrue((Path(tmp) / "scenario_pack_reviewer_receipt.md").exists())
            self.assertTrue((Path(tmp) / "scenario_pack_visual_receipt.json").exists())
            self.assertTrue((Path(tmp) / "scenario_pack_visual_receipt.md").exists())
            self.assertTrue((Path(tmp) / "scenario_pack_visual_receipt.html").exists())
            self.assertTrue((Path(tmp) / "schema_inventory.json").exists())
            self.assertTrue((Path(tmp) / "schema_inventory.md").exists())
            self.assertTrue((Path(tmp) / "artifact_validation.json").exists())
            self.assertTrue((Path(tmp) / "artifact_validation.md").exists())
            self.assertTrue((Path(tmp) / "release_manifest.json").exists())
            self.assertTrue((Path(tmp) / "release_manifest.md").exists())
            self.assertTrue((Path(tmp) / "docs_export.html").exists())
            self.assertTrue((Path(tmp) / "docs_export.json").exists())
            self.assertTrue((Path(tmp) / "docs_export.md").exists())
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
            self.assertTrue((Path(tmp) / "product_snapshot_tqqq_case_study.json").exists())
            self.assertTrue((Path(tmp) / "product_snapshot_tqqq_case_study.md").exists())
            self.assertTrue((Path(tmp) / "product_family_walkthrough.json").exists())
            self.assertTrue((Path(tmp) / "product_family_walkthrough.md").exists())
            package_audit = json.loads((Path(tmp) / "package_audit.json").read_text(encoding="utf-8"))
            release_manifest = json.loads((Path(tmp) / "release_manifest.json").read_text(encoding="utf-8"))
            docs_export = json.loads((Path(tmp) / "docs_export.json").read_text(encoding="utf-8"))
            self.assertTrue(package_audit["summary"]["ready"])
            self.assertEqual(release_manifest["schema_version"], "0.30")
            self.assertEqual(release_manifest["release_readiness"]["status"], "ready")
            self.assertEqual(docs_export["schema_version"], "0.30")

    def test_product_snapshot_case_study(self):
        result = self.run_cli("product-snapshot", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.31")
        self.assertEqual(data["document_type"], "product_snapshot_case_study")
        self.assertEqual(data["product"]["ticker"], "TQQQ")
        self.assertFalse(data["provenance"]["live_market_data"])
        self.assertFalse(data["provenance"]["broker_execution"])
        self.assertFalse(data["provenance"]["personalized_recommendations"])
        self.assertGreaterEqual(len(data["source_attribution"]), 3)
        commands = [item["command"] for item in data["reviewer_demo_path"]]
        self.assertTrue(any("artifact-validate" in item for item in commands))

    def test_product_family_walkthrough(self):
        result = self.run_cli("product-family-walkthrough", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.31")
        self.assertEqual(data["document_type"], "product_family_walkthrough")
        self.assertEqual(data["summary"]["snapshot_product"], "TQQQ")
        self.assertEqual(data["summary"]["scenario_cases"], 3)
        self.assertEqual(data["summary"]["product_family_examples"], 3)
        self.assertFalse(data["summary"]["live_market_data"])
        self.assertFalse(data["summary"]["broker_execution"])
        self.assertFalse(data["summary"]["trading_enabled"])
        self.assertFalse(data["summary"]["personalized_recommendations"])
        examples = {item["ticker"]: item for item in data["product_family_examples"]}
        self.assertEqual(examples["SECT2X"]["fixture"], "examples/fixtures/sector_index_2x.json")
        self.assertIn("Static educational fixture", examples["SECT2X"]["boundary"])
        self.assertGreaterEqual(len(data["fixture_provenance"]), 6)
        self.assertTrue(all(len(item["sha256"]) == 64 for item in data["source_artifacts"]))
        caveats = " ".join(data["path_dependency_caveats"]).lower()
        self.assertIn("daily-reset leverage", caveats)
        self.assertIn("simple leverage multiple", caveats)
        boundaries = " ".join(data["safety_boundaries"]).lower()
        self.assertIn("no live market data", boundaries)
        self.assertIn("no broker", boundaries)
        self.assertIn("no trading", boundaries)
        self.assertIn("not investment advice", data["not_investment_advice"].lower())
        markdown = self.run_cli("product-family-walkthrough", "--format", "markdown")
        self.assertEqual(markdown.returncode, 0, markdown.stderr)
        self.assertIn("# Product Family Walkthrough", markdown.stdout)
        self.assertIn("## Artifact Comparison", markdown.stdout)
        self.assertIn("## Static Product Family Examples", markdown.stdout)
        self.assertIn("SECT2X", markdown.stdout)
        validation = self.run_cli("artifact-validate", "examples/outputs/product_family_walkthrough.json")
        self.assertEqual(validation.returncode, 0, validation.stderr)
        validation_data = json.loads(validation.stdout)
        self.assertTrue(validation_data["summary"]["ready"])

    def test_scenario_pack_writes_case_studies(self):
        with tempfile.TemporaryDirectory() as demo_tmp, tempfile.TemporaryDirectory() as pack_tmp:
            demo = self.run_cli("demo-bundle", "--output-dir", demo_tmp)
            self.assertEqual(demo.returncode, 0, demo.stderr)
            result = self.run_cli(
                "scenario-pack",
                "--input-dir",
                demo_tmp,
                "--fixtures-dir",
                "examples/fixtures",
                "--output-dir",
                pack_tmp,
                "--format",
                "json",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["schema_version"], "0.30")
            self.assertEqual(data["document_type"], "scenario_pack")
            self.assertEqual(data["summary"]["cases"], 3)
            targets = {item["target_system"] for item in data["integration_notes"]}
            self.assertEqual(targets, {"portfolio-risk-compass", "invest-thesis-ledger"})
            self.assertTrue(all("dependency" in item["dependency_boundary"].lower() for item in data["integration_notes"]))
            self.assertTrue(all("private" in item["public_context"].lower() for item in data["integration_notes"]))
            self.assertFalse(data["provenance"]["live_market_data"])
            self.assertFalse(data["provenance"]["workflow_files_read"])
            evidence = data["cold_user_evidence"]
            commands = [item["command"] for item in evidence["exact_commands"]]
            self.assertIn(
                "python -m leveraged_etp_risk_lab scenario-pack --input-dir examples/outputs --fixtures-dir examples/fixtures --output-dir examples/outputs --format markdown",
                commands,
            )
            self.assertIn(
                "examples/outputs/scenario_pack.md",
                [item["path"] for item in evidence["artifact_links"]],
            )
            pack_markdown = (Path(pack_tmp) / "scenario_pack.md").read_text(encoding="utf-8")
            self.assertIn("## Integration Notes", pack_markdown)
            self.assertIn("portfolio-risk-compass", pack_markdown)
            self.assertIn("invest-thesis-ledger", pack_markdown)
            self.assertTrue(any("Does not place trades" in item for item in evidence["safety_boundaries"]))
            self.assertTrue((Path(pack_tmp) / "scenario_pack.json").exists())
            self.assertTrue((Path(pack_tmp) / "scenario_pack_reviewer_receipt.json").exists())
            self.assertTrue((Path(pack_tmp) / "daily_reset_path_decay.md").exists())
            case = json.loads((Path(pack_tmp) / "pretrade_guardrails.json").read_text(encoding="utf-8"))
            self.assertEqual(case["document_type"], "scenario_case_study")
            self.assertEqual(case["focus_area"], "pretrade_guardrails")
            self.assertIn("guardrail_status", case["metrics"])
            case_evidence = case["cold_user_evidence"]
            self.assertTrue(
                any("order-review" in item["command"] for item in case_evidence["exact_commands"])
            )
            self.assertIn(
                "examples/outputs/pretrade_guardrails.md",
                [item["path"] for item in case_evidence["artifact_links"]],
            )
            case_markdown = (Path(pack_tmp) / "pretrade_guardrails.md").read_text(encoding="utf-8")
            self.assertIn("## New User Evidence", case_markdown)
            self.assertIn("### Exact Commands", case_markdown)

    def test_scenario_pack_reviewer_receipt(self):
        with tempfile.TemporaryDirectory() as demo_tmp, tempfile.TemporaryDirectory() as receipt_tmp:
            demo = self.run_cli("demo-bundle", "--output-dir", demo_tmp)
            self.assertEqual(demo.returncode, 0, demo.stderr)
            result = self.run_cli(
                "scenario-pack-reviewer-receipt",
                "--input-dir",
                demo_tmp,
                "--fixtures-dir",
                "examples/fixtures",
                "--artifact-dir",
                demo_tmp,
                "--output-dir",
                receipt_tmp,
                "--format",
                "json",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["schema_version"], "0.30")
            self.assertEqual(data["document_type"], "scenario_pack_reviewer_receipt")
            self.assertEqual(data["summary"]["hash_algorithm"], "sha256")
            self.assertFalse(data["summary"]["live_market_data"])
            self.assertFalse(data["summary"]["broker_execution"])
            self.assertFalse(data["summary"]["trading_enabled"])
            self.assertFalse(data["summary"]["personalized_recommendations"])
            self.assertEqual(data["summary"]["fixture_inputs"], 6)
            self.assertEqual(data["summary"]["generated_artifacts"], 8)
            self.assertTrue(all(len(item["sha256"]) == 64 for item in data["fixture_inputs"]))
            artifact_paths = [item["path"] for item in data["generated_artifacts"]]
            self.assertIn(f"{demo_tmp}/scenario_pack.json", artifact_paths)
            self.assertIn("scenario-pack-reviewer-receipt", data["regeneration"]["receipt_command"])
            self.assertIn("artifact-validate", data["regeneration"]["validation_command"])
            boundaries = " ".join(data["safety_boundaries"]).lower()
            self.assertIn("no live market data", boundaries)
            self.assertIn("no broker", boundaries)
            self.assertIn("no trading", boundaries)
            self.assertIn("no personalized recommendation", boundaries)
            receipt_markdown = (Path(receipt_tmp) / "scenario_pack_reviewer_receipt.md").read_text(encoding="utf-8")
            self.assertIn("## Generated Artifacts", receipt_markdown)
            self.assertIn("SHA-256", receipt_markdown)
            validation = self.run_cli("artifact-validate", str(Path(receipt_tmp) / "scenario_pack_reviewer_receipt.json"))
            self.assertEqual(validation.returncode, 0, validation.stderr)
            validation_data = json.loads(validation.stdout)
            self.assertTrue(validation_data["summary"]["ready"])
            data["summary"]["trading_enabled"] = True
            bad_receipt = Path(receipt_tmp) / "bad_scenario_pack_reviewer_receipt.json"
            bad_receipt.write_text(json.dumps(data), encoding="utf-8")
            bad_validation = self.run_cli("artifact-validate", str(bad_receipt))
            self.assertEqual(bad_validation.returncode, 0, bad_validation.stderr)
            bad_validation_data = json.loads(bad_validation.stdout)
            self.assertFalse(bad_validation_data["summary"]["ready"])
            self.assertIn("trading_enabled must be false", bad_validation_data["artifacts"][0]["issues"])

    def test_scenario_pack_visual_receipt(self):
        with tempfile.TemporaryDirectory() as demo_tmp, tempfile.TemporaryDirectory() as receipt_tmp:
            demo = self.run_cli("demo-bundle", "--output-dir", demo_tmp)
            self.assertEqual(demo.returncode, 0, demo.stderr)
            result = self.run_cli(
                "scenario-pack-visual-receipt",
                "--input-dir",
                demo_tmp,
                "--fixtures-dir",
                "examples/fixtures",
                "--artifact-dir",
                demo_tmp,
                "--output-dir",
                receipt_tmp,
                "--format",
                "json",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["schema_version"], "0.32")
            self.assertEqual(data["document_type"], "scenario_pack_visual_receipt")
            self.assertEqual(data["summary"]["scenario_cases"], 3)
            self.assertEqual(data["summary"]["hash_algorithm"], "sha256")
            self.assertTrue(data["summary"]["static_html"])
            self.assertFalse(data["summary"]["live_market_data"])
            self.assertFalse(data["summary"]["broker_execution"])
            self.assertFalse(data["summary"]["trading_enabled"])
            self.assertFalse(data["summary"]["personalized_recommendations"])
            self.assertIn("demo-bundle", data["demo_bundle_bridge"]["source_command"])
            self.assertIn("scenario-pack-visual-receipt", data["demo_bundle_bridge"]["visual_receipt_command"])
            self.assertEqual([item["step"] for item in data["evidence_chain"]][-1], "visual_receipt")
            self.assertTrue(all(len(item["sha256"]) == 64 for item in data["generated_artifacts"]))
            self.assertEqual({card["case_id"] for card in data["case_cards"]}, {"daily_reset_path_decay", "drawdown_risk", "pretrade_guardrails"})
            checklist = " ".join(item["item"] for item in data["release_owner_checklist"]).lower()
            self.assertIn("demo bundle", checklist)
            self.assertIn("safety", checklist)
            boundaries = " ".join(data["safety_boundaries"]).lower()
            self.assertIn("no live market data", boundaries)
            self.assertIn("no broker", boundaries)
            self.assertIn("no trading", boundaries)
            html = (Path(receipt_tmp) / "scenario_pack_visual_receipt.html").read_text(encoding="utf-8")
            self.assertIn("<!doctype html>", html)
            self.assertIn("Scenario Evidence Cards", html)
            self.assertNotIn("<script", html.lower())
            self.assertNotIn("http://", html.lower())
            self.assertNotIn("https://", html.lower())
            markdown = (Path(receipt_tmp) / "scenario_pack_visual_receipt.md").read_text(encoding="utf-8")
            self.assertIn("## Demo Bundle Bridge", markdown)
            self.assertIn("## Release Owner Checklist", markdown)
            validation = self.run_cli("artifact-validate", str(Path(receipt_tmp) / "scenario_pack_visual_receipt.json"))
            self.assertEqual(validation.returncode, 0, validation.stderr)
            validation_data = json.loads(validation.stdout)
            self.assertTrue(validation_data["summary"]["ready"])

    def test_release_manifest_json_and_missing_inputs(self):
        result = self.run_cli("release-manifest", "--no-git")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.30")
        self.assertEqual(data["document_type"], "release_manifest")
        self.assertEqual(data["version"], __version__)
        self.assertFalse(data["provenance"]["live_market_data"])
        self.assertFalse(data["provenance"]["private_context"])
        self.assertFalse(data["provenance"]["workflow_files_read"])
        self.assertIn(data["release_readiness"]["status"], {"ready", "review", "blocked"})
        with tempfile.TemporaryDirectory() as tmp:
            missing = self.run_cli("release-manifest", "--input-dir", tmp, "--no-git")
        self.assertEqual(missing.returncode, 0, missing.stderr)
        missing_data = json.loads(missing.stdout)
        self.assertTrue(all(item["status"] == "missing" for item in missing_data["inputs"]))
        self.assertEqual(missing_data["git"]["status"], "disabled")

    def test_docs_export_html_json_and_markdown(self):
        html_result = self.run_cli("docs-export")
        self.assertEqual(html_result.returncode, 0, html_result.stderr)
        self.assertIn("<!doctype html>", html_result.stdout)
        self.assertIn("Safety Caveats", html_result.stdout)
        self.assertIn("Command Map", html_result.stdout)
        self.assertIn("Local Artifact Links", html_result.stdout)
        self.assertNotIn("<script", html_result.stdout.lower())
        self.assertNotIn("http://", html_result.stdout.lower())
        self.assertNotIn("https://", html_result.stdout.lower())

        json_result = self.run_cli("docs-export", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        data = json.loads(json_result.stdout)
        self.assertEqual(data["schema_version"], "0.30")
        self.assertEqual(data["document_type"], "docs_export")
        self.assertFalse(data["provenance"]["live_market_data"])
        self.assertFalse(data["provenance"]["external_assets"])
        self.assertFalse(data["provenance"]["javascript"])
        self.assertFalse(data["provenance"]["private_context"])
        self.assertFalse(data["provenance"]["workflow_files_read"])
        self.assertTrue(data["command_map"])
        self.assertEqual(
            {item["target_system"] for item in data["integration_notes"]},
            {"portfolio-risk-compass", "invest-thesis-ledger"},
        )
        self.assertTrue(data["markdown_artifacts"])

        markdown_result = self.run_cli("docs-export", "--format", "markdown")
        self.assertEqual(markdown_result.returncode, 0, markdown_result.stderr)
        self.assertIn("# Leveraged ETP Risk Lab Documentation", markdown_result.stdout)
        self.assertIn("## Integration Notes", markdown_result.stdout)
        self.assertIn("## Release Notes", markdown_result.stdout)

    def test_schema_inventory_respects_custom_root_paths(self):
        from leveraged_etp_risk_lab.schema_validation import schema_inventory

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            outputs = root / "examples" / "outputs"
            docs.mkdir()
            outputs.mkdir(parents=True)
            (docs / "custom.schema.json").write_text(
                json.dumps(
                    {
                        "$schema": "https://json-schema.org/draft/2020-12/schema",
                        "title": "Custom",
                        "type": "object",
                        "required": ["schema_version", "document_type", "value"],
                        "properties": {
                            "schema_version": {"const": "1.0"},
                            "document_type": {"const": "custom_doc"},
                        },
                    }
                ),
                encoding="utf-8",
            )
            (outputs / "custom.json").write_text(
                json.dumps({"schema_version": "1.0", "document_type": "custom_doc", "value": 1}),
                encoding="utf-8",
            )
            data = schema_inventory(root=root, examples_dir=outputs)
            self.assertEqual(data["schemas"][0]["examples"], ["examples/outputs/custom.json"])

    def test_cycle_init_and_update_json(self):
        init = self.run_cli(
            "cycle-init",
            "--memo",
            "examples/outputs/investment_memo.json",
            "--watchlist",
            "examples/outputs/watchlist.json",
            "--report-card",
            "examples/outputs/report_card.json",
            "--sensitivity-grid",
            "examples/outputs/sensitivity_grid.json",
        )
        self.assertEqual(init.returncode, 0, init.stderr)
        state = json.loads(init.stdout)
        self.assertEqual(state["schema_version"], "0.22")
        self.assertEqual(state["document_type"], "cycle_state")
        self.assertTrue(state["state_id"].startswith("cycle_"))
        self.assertIn("not investment advice", state["not_investment_advice"].lower())
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "cycle_state.json"
            state_path.write_text(init.stdout, encoding="utf-8")
            update = self.run_cli(
                "cycle-update",
                "--cycle-state",
                str(state_path),
                "--report-card",
                "examples/outputs/report_card.json",
                "--watchlist",
                "examples/outputs/watchlist.json",
                "--audit-trail",
                "examples/outputs/audit_trail.json",
            )
        self.assertEqual(update.returncode, 0, update.stderr)
        data = json.loads(update.stdout)
        self.assertEqual(data["schema_version"], "0.22")
        self.assertEqual(data["document_type"], "cycle_update")
        self.assertEqual(data["state_id"], state["state_id"])
        self.assertIn("hash_drift", data)

    def test_guardrail_policy_and_check_json(self):
        policy = self.run_cli("guardrail-policy", "--policy", "default")
        self.assertEqual(policy.returncode, 0, policy.stderr)
        policy_data = json.loads(policy.stdout)
        self.assertEqual(policy_data["schema_version"], "0.23")
        self.assertEqual(policy_data["document_type"], "guardrail_policy")
        self.assertEqual(policy_data["limits"]["max_leverage_exposure"], 3.0)
        with tempfile.TemporaryDirectory() as tmp:
            policy_path = Path(tmp) / "policy.json"
            policy_path.write_text(policy.stdout, encoding="utf-8")
            check = self.run_cli(
                "guardrail-check",
                "--policy",
                str(policy_path),
                "--portfolio-sensitivity",
                "examples/outputs/portfolio_sensitivity.json",
                "--position-size",
                "examples/outputs/position_size.json",
                "--investment-memo",
                "examples/outputs/investment_memo.json",
                "--cycle-update",
                "examples/outputs/cycle_update.json",
            )
        self.assertEqual(check.returncode, 0, check.stderr)
        data = json.loads(check.stdout)
        self.assertEqual(data["schema_version"], "0.23")
        self.assertEqual(data["document_type"], "guardrail_check")
        self.assertIn(data["summary"]["result"], {"pass", "review", "fail"})
        self.assertTrue(data["rules"])
        self.assertIn("next_actions", data)

    def test_order_ticket_and_review_json(self):
        ticket = self.run_cli(
            "order-ticket",
            "--guardrail-check",
            "examples/outputs/guardrail_check.json",
            "--investment-memo",
            "examples/outputs/investment_memo.json",
            "--position-size",
            "examples/outputs/position_size.json",
            "--factsheet-check",
            "examples/outputs/factsheet_check.json",
            "--thesis-dashboard-data",
            "examples/outputs/thesis_dashboard_data.json",
        )
        self.assertEqual(ticket.returncode, 0, ticket.stderr)
        ticket_data = json.loads(ticket.stdout)
        self.assertEqual(ticket_data["schema_version"], "0.24")
        self.assertEqual(ticket_data["document_type"], "order_ticket")
        self.assertIn(ticket_data["summary"]["status"], {"blocked", "review", "ready"})
        self.assertFalse(ticket_data["provenance"]["live_market_data"])
        self.assertFalse(ticket_data["provenance"]["broker_execution"])
        self.assertIn("no_live_price_warning", ticket_data)
        self.assertTrue(ticket_data["required_broker_fields"])
        with tempfile.TemporaryDirectory() as tmp:
            ticket_path = Path(tmp) / "order_ticket.json"
            ticket_path.write_text(ticket.stdout, encoding="utf-8")
            review = self.run_cli(
                "order-review",
                "--order-ticket",
                str(ticket_path),
                "--guardrail-check",
                "examples/outputs/guardrail_check.json",
                "--cycle-update",
                "examples/outputs/cycle_update.json",
                "--audit-trail",
                "examples/outputs/audit_trail.json",
            )
        self.assertEqual(review.returncode, 0, review.stderr)
        review_data = json.loads(review.stdout)
        self.assertEqual(review_data["schema_version"], "0.24")
        self.assertEqual(review_data["document_type"], "order_review")
        self.assertIn(review_data["summary"]["status"], {"blocked", "review", "ready"})
        self.assertFalse(review_data["summary"]["broker_execution"])
        self.assertTrue(review_data["checklist"])

    def test_asset_hub_json_and_markdown(self):
        result = self.run_cli("asset-hub", "--input-dir", "examples/outputs", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.25")
        self.assertEqual(data["document_type"], "asset_hub")
        self.assertEqual(data["product_positioning"]["version"], __version__)
        self.assertIn("asset-hub", [item["name"] for item in data["command_map"]])
        self.assertEqual(data["agent_skill_path"], "skills/agent/leveraged-etp-risk-lab/SKILL.md")
        self.assertFalse(data["provenance"]["live_market_data"])
        self.assertFalse(data["provenance"]["shell_out"])
        self.assertFalse(data["provenance"]["private_context"])
        markdown = self.run_cli("asset-hub", "--input-dir", "examples/outputs", "--format", "markdown")
        self.assertEqual(markdown.returncode, 0, markdown.stderr)
        self.assertIn("# leveraged-etp-risk-lab Public Asset Hub", markdown.stdout)
        self.assertIn("Three-Version Roadmap", markdown.stdout)

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

    def test_sensitivity_grid_json(self):
        result = self.run_cli(
            "sensitivity-grid",
            "--product",
            "examples/fixtures/leveraged_nasdaq_3x.json",
            "--regime",
            "trend_down",
            "--regime",
            "chop",
            "--leverage-multiplier",
            "1,3",
            "--stop-loss",
            "none,0.15",
            "--take-profit",
            "none,0.20",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.19")
        self.assertEqual(data["document_type"], "sensitivity_grid")
        self.assertEqual(data["inputs"]["leverage_multipliers"], [1.0, 3.0])
        self.assertEqual(data["inputs"]["stop_loss_pct_grid"], [None, 15.0])
        self.assertEqual(data["inputs"]["take_profit_pct_grid"], [None, 20.0])
        self.assertEqual(data["summary"]["combinations"], 8)
        self.assertEqual(len(data["cells"]), 16)
        self.assertIn("worst_return_pct", data["rows"][0])
        self.assertIn("path_decay", " ".join(data["rows"][0].keys()))

    def test_sensitivity_grid_markdown(self):
        result = self.run_cli(
            "sensitivity-grid",
            "--product",
            "examples/fixtures/leveraged_nasdaq_3x.json",
            "--regime",
            "volatility_cluster",
            "--stop-loss",
            "none,0.15",
            "--take-profit",
            "none,0.20",
            "--format",
            "markdown",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Sensitivity Grid", result.stdout)
        self.assertIn("worst_return_pct", result.stdout)
        self.assertIn("volatility_cluster", result.stdout)

    def test_portfolio_sensitivity_json(self):
        result = self.run_cli(
            "portfolio-sensitivity",
            "--manifest",
            "examples/fixtures/portfolio_manifest.json",
            "--regime",
            "trend_down",
            "--regime",
            "chop",
            "--stop-loss",
            "none,0.15",
            "--take-profit",
            "none,0.20",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.20")
        self.assertEqual(data["document_type"], "portfolio_sensitivity")
        self.assertEqual(data["summary"]["positions"], 2)
        self.assertIn("aggregate_worst_case_weighted_exposure", data["summary"])
        self.assertEqual([item["id"] for item in data["positions"]], ["nasdaq_tactical", "single_stock_satellite"])
        self.assertFalse(data["provenance"]["live_market_data"])
        self.assertFalse(data["provenance"]["shell_out"])

    def test_portfolio_sensitivity_markdown(self):
        result = self.run_cli(
            "portfolio-sensitivity",
            "--manifest",
            "examples/fixtures/portfolio_manifest.json",
            "--regime",
            "trend_down",
            "--format",
            "markdown",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Portfolio Sensitivity", result.stdout)
        self.assertIn("Aggregate worst-case", result.stdout)

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

    def test_risk_profile_json(self):
        result = self.run_cli("risk-profile")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.16")
        self.assertEqual(data["document_type"], "risk_profile_rules")
        self.assertEqual([profile["id"] for profile in data["profiles"]], ["default", "conservative", "active-trader", "thesis-review"])
        thesis = data["profiles"][3]
        self.assertEqual(thesis["max_holding_days"], 10)
        self.assertIn("max_account_risk_pct_placeholder", thesis)
        self.assertIn("issuer", thesis["required_factsheet_fields"])
        self.assertIn("volatility_cluster", thesis["required_scenario_regimes"])
        self.assertTrue(thesis["mandatory_checklist_questions"])
        self.assertEqual(thesis["stop_take_review_defaults"]["take_profit_pct"], 18.0)
        self.assertIn("not investment advice", data["not_investment_advice"].lower())

    def test_risk_profile_markdown_selected(self):
        result = self.run_cli("risk-profile", "--profile", "conservative", "--format", "markdown")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Risk Rule Profiles", result.stdout)
        self.assertIn("## Conservative (conservative)", result.stdout)
        self.assertIn("Required Factsheet Fields", result.stdout)
        self.assertIn("Stop/Take Review Defaults", result.stdout)
        self.assertNotIn("## Active Trader", result.stdout)

    def test_recipe_run_json(self):
        result = self.run_cli("recipe-run", "--recipe", "examples/fixtures/recipe_thesis_review.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.17")
        self.assertEqual(data["document_type"], "recipe_run")
        self.assertFalse(data["provenance"]["shell_out"])
        self.assertEqual(data["inputs"]["profile"], "thesis-review")
        self.assertEqual(data["summary"]["recommended_notional"], 5000.0)
        self.assertGreater(data["summary"]["watchlist_entries"], 0)
        self.assertEqual(data["artifacts"]["factsheet_check"]["document_type"], "factsheet_check")
        self.assertEqual(data["artifacts"]["risk_profile"]["document_type"], "risk_profile_rules")
        self.assertEqual(data["artifacts"]["stress_matrix"]["document_type"], "stress_matrix")
        self.assertEqual(data["artifacts"]["pretrade_plan"]["document_type"], "pretrade_plan")
        self.assertEqual(data["artifacts"]["thesis_impact"]["document_type"], "thesis_impact")
        self.assertEqual(data["artifacts"]["watchlist"]["document_type"], "watchlist")
        commands = [item["step"] for item in data["workflow"]]
        self.assertIn("factsheet-check", commands)
        self.assertIn("position-size", commands)
        self.assertIn("watchlist-build", commands)

    def test_recipe_run_markdown(self):
        result = self.run_cli(
            "recipe-run",
            "--recipe",
            "examples/fixtures/recipe_thesis_review.json",
            "--format",
            "markdown",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Recipe Run", result.stdout)
        self.assertIn("Conceptual Workflow", result.stdout)
        self.assertIn("watchlist-build", result.stdout)

    def test_report_card_json(self):
        result = self.run_cli(
            "report-card",
            "--artifact",
            "examples/outputs/pretrade_plan.json",
            "--artifact",
            "examples/outputs/position_size.json",
            "--artifact",
            "examples/outputs/stress_matrix.json",
            "--artifact",
            "examples/outputs/factsheet_check.json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.18")
        self.assertEqual(data["document_type"], "report_card")
        self.assertFalse(data["summary"]["decision_ready"])
        self.assertIn("pretrade_plan", data["summary"]["document_types"])
        self.assertIn("factsheet_check", data["summary"]["document_types"])
        self.assertTrue(data["strengths"])
        self.assertTrue(data["unresolved_checks"])
        self.assertTrue(data["warnings"])
        self.assertFalse(data["provenance"]["live_market_data"])
        self.assertFalse(data["provenance"]["shell_out"])
        self.assertTrue(any("package-audit" in command for command in data["next_commands"]))

    def test_report_card_markdown(self):
        result = self.run_cli(
            "report-card",
            "--artifact",
            "examples/outputs/pretrade_plan.json",
            "--artifact",
            "examples/outputs/stress_matrix.json",
            "--format",
            "markdown",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Decision Readiness Report Card", result.stdout)
        self.assertIn("## Unresolved Checks", result.stdout)
        self.assertIn("## Next Commands", result.stdout)

    def test_thesis_dashboard_data_json(self):
        result = self.run_cli(
            "thesis-dashboard-data",
            "--recipe-run",
            "examples/outputs/recipe_run.json",
            "--report-card",
            "examples/outputs/report_card.json",
            "--watchlist",
            "examples/outputs/watchlist.json",
            "--sensitivity-grid",
            "examples/outputs/sensitivity_grid.json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.20")
        self.assertEqual(data["document_type"], "thesis_dashboard_data")
        self.assertIn("readiness", data["cards"])
        self.assertIn("top_entries", data["cards"]["watchlist"])
        self.assertFalse(data["provenance"]["live_market_data"])
        self.assertFalse(data["provenance"]["shell_out"])

    def test_audit_trail_json(self):
        result = self.run_cli(
            "audit-trail",
            "--ledger",
            "examples/outputs/run_ledger.jsonl",
            "--artifact",
            "examples/outputs/pretrade_plan.json",
            "--artifact",
            "examples/outputs/stress_matrix.json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.20")
        self.assertEqual(data["document_type"], "audit_trail")
        self.assertEqual(data["summary"]["artifacts"], 2)
        self.assertTrue(all(item["hash_matches_ledger"] for item in data["checklist"]))

    def test_memo_draft_json(self):
        result = self.run_cli(
            "memo-draft",
            "--recipe-run",
            "examples/outputs/recipe_run.json",
            "--thesis-dashboard-data",
            "examples/outputs/thesis_dashboard_data.json",
            "--report-card",
            "examples/outputs/report_card.json",
            "--factsheet-check",
            "examples/outputs/factsheet_check.json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.21")
        self.assertEqual(data["document_type"], "investment_memo_packet")
        self.assertEqual(data["product_terms"]["ticker"], "NDAQ3X")
        self.assertIn("not investment advice", data["not_investment_advice"].lower())
        self.assertTrue(data["open_checks"])
        self.assertTrue(data["invalidation_triggers"])
        self.assertFalse(data["provenance"]["live_market_data"])
        self.assertFalse(data["provenance"]["shell_out"])

    def test_memo_draft_markdown(self):
        result = self.run_cli(
            "memo-draft",
            "--recipe-run",
            "examples/outputs/recipe_run.json",
            "--thesis-dashboard-data",
            "examples/outputs/thesis_dashboard_data.json",
            "--report-card",
            "examples/outputs/report_card.json",
            "--format",
            "markdown",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Investment Memo", result.stdout)
        self.assertIn("## Invalidation Triggers", result.stdout)

    def test_memo_review_json(self):
        result = self.run_cli(
            "memo-review",
            "--memo",
            "examples/outputs/investment_memo.json",
            "--report-card",
            "examples/outputs/report_card.json",
            "--watchlist",
            "examples/outputs/watchlist.json",
            "--audit-trail",
            "examples/outputs/audit_trail.json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.21")
        self.assertEqual(data["document_type"], "investment_memo_review")
        self.assertTrue(data["checklist"])
        self.assertTrue(data["next_actions"])
        self.assertFalse(data["provenance"]["live_market_data"])
        self.assertFalse(data["provenance"]["shell_out"])

    def test_memo_review_markdown(self):
        result = self.run_cli(
            "memo-review",
            "--memo",
            "examples/outputs/investment_memo.json",
            "--report-card",
            "examples/outputs/report_card.json",
            "--watchlist",
            "examples/outputs/watchlist.json",
            "--audit-trail",
            "examples/outputs/audit_trail.json",
            "--format",
            "markdown",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Investment Memo Review", result.stdout)
        self.assertIn("## Changed Risks", result.stdout)

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
        self.assertIn("report_card.json", sources)
        self.assertIn("investment_memo.json", sources)
        self.assertIn("investment_memo_review.json", sources)
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
            ["fixtures", "plans", "sizing", "stress", "thesis/watchlist", "audit/story", "dashboard", "validation"],
        )
        artifacts = [item for stage in data["stages"] for item in stage["artifacts"]]
        names = {item["name"] for item in artifacts}
        self.assertIn("pretrade_plan.json", names)
        self.assertIn("dashboard.html", names)
        self.assertIn("artifact_validation.json", names)
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
        self.assertIn("docs/risk-profile.schema.json", required_schemas)
        self.assertIn("examples/outputs/risk_profiles.json", required_examples)
        self.assertIn("docs/report-card.schema.json", required_schemas)
        self.assertIn("examples/outputs/report_card.json", required_examples)
        self.assertIn("docs/investment-memo.schema.json", required_schemas)
        self.assertIn("examples/outputs/investment_memo.json", required_examples)
        self.assertIn("docs/schema-inventory.schema.json", required_schemas)
        self.assertIn("examples/outputs/schema_inventory.json", required_examples)
        self.assertIn("docs/artifact-validation.schema.json", required_schemas)
        self.assertIn("examples/outputs/artifact_validation.json", required_examples)
        self.assertIn("docs/scenario-pack.schema.json", required_schemas)
        self.assertIn("docs/scenario-case-study.schema.json", required_schemas)
        self.assertIn("docs/scenario-pack-reviewer-receipt.schema.json", required_schemas)
        self.assertIn("docs/product-family-walkthrough.schema.json", required_schemas)
        self.assertIn("examples/outputs/scenario_pack.json", required_examples)
        self.assertIn("examples/outputs/pretrade_guardrails.json", required_examples)
        self.assertIn("examples/outputs/scenario_pack_reviewer_receipt.json", required_examples)
        self.assertIn("examples/outputs/product_family_walkthrough.json", required_examples)
        self.assertTrue(any("scenario-pack" in " ".join(command["command"]) for command in data["test_commands"]))
        self.assertTrue(any("scenario-pack-reviewer-receipt" in " ".join(command["command"]) for command in data["test_commands"]))
        self.assertTrue(any("product-family-walkthrough" in " ".join(command["command"]) for command in data["test_commands"]))
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

    def test_schema_inventory_json(self):
        result = self.run_cli("schema-inventory")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.26")
        self.assertEqual(data["document_type"], "schema_inventory")
        schema_paths = {item["path"] for item in data["schemas"]}
        self.assertIn("docs/pretrade-plan.schema.json", schema_paths)
        self.assertIn("docs/artifact-validation.schema.json", schema_paths)
        pretrade = next(item for item in data["schemas"] if item["document_type"] == "pretrade_plan")
        self.assertIn("provenance", pretrade["required_top_level_fields"])
        self.assertIn("examples/outputs/pretrade_plan.json", pretrade["examples"])
        self.assertFalse(data["provenance"]["live_market_data"])
        self.assertFalse(data["provenance"]["shell_out"])
        self.assertFalse(data["provenance"]["private_context"])
        self.assertFalse(data["provenance"]["broker_execution"])

    def test_artifact_validate_json(self):
        result = self.run_cli("artifact-validate", "examples/outputs/pretrade_plan.json", "examples/outputs/run_ledger.jsonl")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["schema_version"], "0.26")
        self.assertEqual(data["document_type"], "artifact_validation")
        self.assertEqual(data["summary"]["failed"], 0)
        self.assertEqual(data["summary"]["artifacts"], 2)
        self.assertTrue(data["summary"]["ready"])
        self.assertFalse(data["provenance"]["live_market_data"])
        self.assertFalse(data["provenance"]["shell_out"])
        self.assertFalse(data["provenance"]["private_context"])
        self.assertFalse(data["provenance"]["broker_execution"])

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
