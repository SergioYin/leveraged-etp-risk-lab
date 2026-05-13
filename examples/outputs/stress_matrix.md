# Stress Matrix: NDAQ3X

**Not investment advice:** This stress matrix is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

- Product: Generic 3x Nasdaq Daily Reset ETP
- Underlying: Nasdaq-100 reference index
- Daily leverage: 3.0x
- Initial NAV: 100.0
- Stop-loss: 15.0%
- Take-profit: 20.0%

## Matrix

| regime | name | days | underlying_return_pct | return_pct | path_decay_vs_simple_multiple | worst_drawdown_pct | stop_events | warnings_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trend_up | Trend Up | 12 | 6.3671 | 20.0961 | 0.994607 | -0.6038 | 1 | 4 |
| trend_down | Trend Down | 12 | -6.996 | -19.8516 | 1.136554 | -19.8516 | 1 | 4 |
| chop | Chop | 12 | 0.3702 | -0.3186 | -1.429133 | -6.5029 | 0 | 4 |
| gap_down | Gap Down | 8 | -18.1816 | -48.8504 | 5.694511 | -52.5497 | 1 | 4 |
| rebound | Rebound | 10 | 2.1915 | 5.1886 | -1.385944 | -12.5903 | 0 | 4 |
| volatility_cluster | Volatility Cluster | 12 | -1.9628 | -9.0937 | -3.205395 | -16.3862 | 1 | 4 |

## Stop Events

- trend_up: day 12 take_profit at NAV 120.096051
- trend_down: day 8 stop_loss at NAV 84.483822
- chop: None
- gap_down: day 1 stop_loss at NAV 74.49623
- rebound: None
- volatility_cluster: day 7 stop_loss at NAV 83.613785

## Warnings

- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.
- Large daily moves can compound quickly and may create losses larger than a simple one-day estimate.
- Fee drag is approximated as a constant daily deduction from the leveraged daily return.

## Command Provenance

- command: stress-matrix
- initial_nav: 100.0
- product: examples/fixtures/leveraged_nasdaq_3x.json
- regimes: ['trend_up', 'trend_down', 'chop', 'gap_down', 'rebound', 'volatility_cluster']
- stop_loss: 0.15
- take_profit: 0.2
