# Sensitivity Grid: NDAQ3X

**Not investment advice:** This sensitivity grid is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

- Product: Generic 3x Nasdaq Daily Reset ETP
- Underlying: Nasdaq-100 reference index
- Base leverage: 3.0x
- Initial NAV: 100.0
- Regimes: trend_up, trend_down, chop, gap_down, rebound, volatility_cluster
- Leverage grid: 1.0x, 2.0x, 3.0x
- Stop-loss grid: not set, 15.0%, 25.0%
- Take-profit grid: not set, 20.0%, 35.0%

## Summary

- Combinations: 27
- Worst return: -48.8504% in gap_down at 3.0x
- Worst path decay: -3.205395 in volatility_cluster
- Maximum stop/take events: 4 at 3.0x

## Matrix Summary

| leverage | stop_loss_pct | take_profit_pct | worst_return_regime | worst_return_pct | largest_drawdown_pct | worst_path_decay_vs_simple_multiple | stop_events | warnings_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0 | None | None | gap_down | -18.207 | -20.2768 | -0.047862 | 0 | 18 |
| 1.0 | None | 20.0 | gap_down | -18.207 | -20.2768 | -0.047862 | 0 | 18 |
| 1.0 | None | 35.0 | gap_down | -18.207 | -20.2768 | -0.047862 | 0 | 18 |
| 1.0 | 15.0 | None | gap_down | -18.207 | -20.2768 | -0.047862 | 1 | 18 |
| 1.0 | 15.0 | 20.0 | gap_down | -18.207 | -20.2768 | -0.047862 | 1 | 18 |
| 1.0 | 15.0 | 35.0 | gap_down | -18.207 | -20.2768 | -0.047862 | 1 | 18 |
| 1.0 | 25.0 | None | gap_down | -18.207 | -20.2768 | -0.047862 | 0 | 18 |
| 1.0 | 25.0 | 20.0 | gap_down | -18.207 | -20.2768 | -0.047862 | 0 | 18 |
| 1.0 | 25.0 | 35.0 | gap_down | -18.207 | -20.2768 | -0.047862 | 0 | 18 |
| 2.0 | None | None | gap_down | -34.4962 | -37.7318 | -1.126228 | 0 | 24 |
| 2.0 | None | 20.0 | gap_down | -34.4962 | -37.7318 | -1.126228 | 0 | 24 |
| 2.0 | None | 35.0 | gap_down | -34.4962 | -37.7318 | -1.126228 | 0 | 24 |
| 2.0 | 15.0 | None | gap_down | -34.4962 | -37.7318 | -1.126228 | 1 | 24 |
| 2.0 | 15.0 | 20.0 | gap_down | -34.4962 | -37.7318 | -1.126228 | 1 | 24 |
| 2.0 | 15.0 | 35.0 | gap_down | -34.4962 | -37.7318 | -1.126228 | 1 | 24 |
| 2.0 | 25.0 | None | gap_down | -34.4962 | -37.7318 | -1.126228 | 1 | 24 |
| 2.0 | 25.0 | 20.0 | gap_down | -34.4962 | -37.7318 | -1.126228 | 1 | 24 |
| 2.0 | 25.0 | 35.0 | gap_down | -34.4962 | -37.7318 | -1.126228 | 1 | 24 |
| 3.0 | None | None | gap_down | -48.8504 | -52.5497 | -3.205395 | 0 | 24 |
| 3.0 | None | 20.0 | gap_down | -48.8504 | -52.5497 | -3.205395 | 1 | 24 |
| 3.0 | None | 35.0 | gap_down | -48.8504 | -52.5497 | -3.205395 | 0 | 24 |
| 3.0 | 15.0 | None | gap_down | -48.8504 | -52.5497 | -3.205395 | 3 | 24 |
| 3.0 | 15.0 | 20.0 | gap_down | -48.8504 | -52.5497 | -3.205395 | 4 | 24 |
| 3.0 | 15.0 | 35.0 | gap_down | -48.8504 | -52.5497 | -3.205395 | 3 | 24 |
| 3.0 | 25.0 | None | gap_down | -48.8504 | -52.5497 | -3.205395 | 1 | 24 |
| 3.0 | 25.0 | 20.0 | gap_down | -48.8504 | -52.5497 | -3.205395 | 2 | 24 |
| 3.0 | 25.0 | 35.0 | gap_down | -48.8504 | -52.5497 | -3.205395 | 1 | 24 |

## Warnings

- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.
- Fee drag is approximated as a constant daily deduction from the leveraged daily return.
- Large daily moves can compound quickly and may create losses larger than a simple one-day estimate.
- Sensitivity rows summarize deterministic built-in regimes and do not model execution, liquidity, tax, or suitability.
- Stop-loss and take-profit values are planning bands and do not guarantee fills.

## Command Provenance

- command: sensitivity-grid
- initial_nav: 100.0
- leverage_multipliers: [1.0, 2.0, 3.0]
- live_market_data: False
- product: examples/fixtures/leveraged_nasdaq_3x.json
- regimes: ['trend_up', 'trend_down', 'chop', 'gap_down', 'rebound', 'volatility_cluster']
- shell_out: False
- stop_losses: [None, 0.15, 0.25]
- take_profits: [None, 0.2, 0.35]
