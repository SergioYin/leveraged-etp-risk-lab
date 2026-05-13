import unittest

from leveraged_etp_risk_lab.engine import exposure_report, generate_scenario, portfolio_sensitivity, simulate, stress_matrix
from leveraged_etp_risk_lab.io import load_path, load_portfolio_manifest, load_product
from leveraged_etp_risk_lab.models import RiskBand, SimulationConfig


class EngineTests(unittest.TestCase):
    def test_nasdaq_chop_path_is_deterministic(self):
        product = load_product("examples/fixtures/leveraged_nasdaq_3x.json")
        path = load_path("examples/fixtures/nasdaq_chop_path.csv")
        result = simulate(SimulationConfig(product, path, 100.0, RiskBand(stop_loss=0.15, take_profit=0.2)))

        self.assertEqual(result["schema_version"], "0.2")
        self.assertEqual(result["product"]["ticker"], "NDAQ3X")
        self.assertEqual(result["inputs"]["days"], 6)
        self.assertEqual(result["summary"]["ending_etp_nav"], 100.608795)
        self.assertEqual(result["summary"]["path_decay_vs_simple_multiple"], -0.602755)

    def test_single_stock_path_records_stop_event(self):
        product = load_product("examples/fixtures/single_stock_2x.json")
        path = load_path("examples/fixtures/single_stock_gap_path.csv")
        result = simulate(SimulationConfig(product, path, 100.0, RiskBand(stop_loss=0.2)))

        self.assertTrue(result["band_events"])
        self.assertEqual(result["band_events"][0]["event"], "stop_loss")

    def test_scenario_generation_is_deterministic(self):
        path = generate_scenario("crash", 6)

        self.assertEqual(path[0].label, "De-risking")
        self.assertEqual(path[0].underlying_return, -0.018)
        self.assertEqual(path[5].label, "De-risking")

    def test_exposure_report_aggregates_positions(self):
        manifest_path = "examples/fixtures/portfolio_manifest.json"
        result = exposure_report(load_portfolio_manifest(manifest_path), manifest_path)

        self.assertEqual(result["schema_version"], "0.2")
        self.assertEqual(result["summary"]["starting_value"], 10000.0)
        self.assertEqual(result["summary"]["weighted_exposure"], 2.6)
        self.assertTrue(result["stop_events"])
        self.assertEqual(result["stop_events"][0]["position_id"], "single_stock_satellite")

    def test_stress_matrix_runs_selected_regimes(self):
        product = load_product("examples/fixtures/leveraged_nasdaq_3x.json")
        result = stress_matrix(product, ["trend_down", "chop"], 100.0, RiskBand(stop_loss=0.15), "product.json")

        self.assertEqual(result["schema_version"], "0.9")
        self.assertEqual(result["document_type"], "stress_matrix")
        self.assertEqual([row["regime"] for row in result["rows"]], ["trend_down", "chop"])
        self.assertIn("worst_drawdown_pct", result["rows"][0])
        self.assertIn("warnings_count", result["rows"][0])

    def test_portfolio_sensitivity_aggregates_worst_case(self):
        manifest_path = "examples/fixtures/portfolio_manifest.json"
        result = portfolio_sensitivity(
            load_portfolio_manifest(manifest_path),
            manifest_path,
            [1.0, 2.0],
            [None, 0.15],
            [None],
            ["trend_down"],
            100.0,
        )

        self.assertEqual(result["schema_version"], "0.20")
        self.assertEqual(result["document_type"], "portfolio_sensitivity")
        self.assertEqual(result["summary"]["positions"], 2)
        self.assertIn("aggregate_worst_case_modeled_loss", result["summary"])
        self.assertEqual(len(result["positions"]), 2)


if __name__ == "__main__":
    unittest.main()
