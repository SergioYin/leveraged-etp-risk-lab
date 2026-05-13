# Thesis Dashboard Data

**Not investment advice:** This dashboard packet is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## Summary

- Product: NDAQ3X
- Scenario return: 0.6088%
- Path decay vs simple multiple: -0.602755
- Recommended notional: 5000.0
- Decision ready: no
- Watchlist entries: 8
- Worst grid return: -48.8504% in gap_down

## Readiness

- Strengths: 8
- Unresolved checks: 10
- Warnings: 10

## Watchlist

| id | severity | status | title |
| --- | --- | --- | --- |
| regime_gap_down | critical | triggered | Gap Down stress trigger |
| claim_1 | high | challenged | The modeled trade is a short-horizon tactical scenario for a generic daily-re... |
| regime_trend_down | high | triggered | Trend Down stress trigger |
| regime_volatility_cluster | high | triggered | Volatility Cluster stress trigger |
| claim_2 | medium | needs_review | The plan should be rejected if the loss budget, stop band, liquidity review,... |
| regime_chop | medium | triggered | Chop stress trigger |
| regime_rebound | medium | triggered | Rebound stress trigger |
| regime_trend_up | medium | triggered | Trend Up stress trigger |

## Sensitivity

- combinations: 27
- max_stop_events: 4
- worst_path_decay_vs_simple_multiple: -3.205395
- worst_return_leverage: 3.0
- worst_return_pct: -48.8504
- worst_return_regime: gap_down

## Warnings

- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.
- Large daily moves can compound quickly and may create losses larger than a simple one-day estimate.
- Fee drag is approximated as a constant daily deduction from the leveraged daily return.
- A pretrade plan does not confirm liquidity, execution quality, tax treatment, or suitability.
- Stop-loss and take-profit bands are planning levels, not guaranteed execution prices.
- Recommended notional is a deterministic planning output, not a trade recommendation.
- Share count is a placeholder because no live or execution price is modeled.
- Stop-loss levels are planning inputs and do not guarantee execution at the modeled loss.
- trend_up has 4 modeled warning(s).
- Sensitivity rows summarize deterministic built-in regimes and do not model execution, liquidity, tax, or suitability.

## Provenance

- artifacts: ['examples/outputs/recipe_run.json', 'examples/outputs/report_card.json', 'examples/outputs/watchlist.json', 'examples/outputs/sensitivity_grid.json']
- command: thesis-dashboard-data
- live_market_data: False
- shell_out: False
