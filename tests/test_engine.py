import unittest

from leveraged_etp_risk_lab.engine import simulate
from leveraged_etp_risk_lab.io import load_path, load_product
from leveraged_etp_risk_lab.models import RiskBand, SimulationConfig


class EngineTests(unittest.TestCase):
    def test_nasdaq_chop_path_is_deterministic(self):
        product = load_product("examples/fixtures/leveraged_nasdaq_3x.json")
        path = load_path("examples/fixtures/nasdaq_chop_path.csv")
        result = simulate(SimulationConfig(product, path, 100.0, RiskBand(stop_loss=0.15, take_profit=0.2)))

        self.assertEqual(result["schema_version"], "0.1")
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


if __name__ == "__main__":
    unittest.main()
