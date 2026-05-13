import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


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
        self.assertEqual(data["version"], "0.3.0")
        self.assertIn("simulate", data["commands"])
        self.assertIn("generate-scenario", data["commands"])
        self.assertIn("exposure-report", data["commands"])
        self.assertIn("pretrade-plan", data["commands"])
        self.assertIn("static-dashboard", data["commands"])

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
            self.assertTrue((Path(tmp) / "dashboard.html").exists())

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


if __name__ == "__main__":
    unittest.main()
