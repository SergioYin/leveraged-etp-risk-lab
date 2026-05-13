# Portfolio Sensitivity: Generic Leveraged ETP Portfolio

**Not investment advice:** This portfolio sensitivity packet is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## Summary

- Base currency: USD
- Positions: 2
- Starting value: 10000.0
- Base weighted exposure: 2.6x
- Aggregate worst-case modeled loss: 4885.18
- Aggregate worst-case loss: 48.8518%
- Aggregate worst-case weighted exposure: 3.0x
- Weakest position: single_stock_satellite in gap_down

## Positions

| id | ticker | notional | weight_pct | base_leverage | worst_return_pct | worst_regime | modeled_loss | weighted_exposure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nasdaq_tactical | NDAQ3X | 6000.0 | 60.0 | 3.0 | -48.8504 | gap_down | 2931.024 | 1.8 |
| single_stock_satellite | STK2X | 4000.0 | 40.0 | 2.0 | -48.8539 | gap_down | 1954.156 | 1.2 |

## Warnings

- Portfolio sensitivity uses starting notional weights and deterministic built-in regimes.
- Aggregate worst-case exposure is a scenario-planning metric, not a margin, liquidity, tax, or suitability model.
- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.
- Fee drag is approximated as a constant daily deduction from the leveraged daily return.
- Large daily moves can compound quickly and may create losses larger than a simple one-day estimate.
- Sensitivity rows summarize deterministic built-in regimes and do not model execution, liquidity, tax, or suitability.
- Stop-loss and take-profit values are planning bands and do not guarantee fills.

## Provenance

- command: portfolio-sensitivity
- live_market_data: False
- manifest: examples/fixtures/portfolio_manifest.json
- shell_out: False
