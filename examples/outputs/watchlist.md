# Thesis Watchlist

**Not investment advice:** This watchlist is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

- Thesis impact: examples/outputs/thesis_impact.json
- Stress matrix: examples/outputs/stress_matrix.json
- Entries: 8 (critical 1, high 3, medium 4, low 0)

## Entries

| id | category | severity | status | title | sources |
| --- | --- | --- | --- | --- | --- |
| regime_gap_down | regime_trigger | critical | triggered | Gap Down stress trigger | examples/outputs/stress_matrix.json |
| claim_1 | claim | high | challenged | The modeled trade is a short-horizon tactical scenario for a generic daily-re... | examples/outputs/thesis_impact.json, examples/outputs/pretrade_plan.json, examples/outputs/portfolio_exposure.json |
| regime_trend_down | regime_trigger | high | triggered | Trend Down stress trigger | examples/outputs/stress_matrix.json |
| regime_volatility_cluster | regime_trigger | high | triggered | Volatility Cluster stress trigger | examples/outputs/stress_matrix.json |
| claim_2 | claim | medium | needs_review | The plan should be rejected if the loss budget, stop band, liquidity review,... | examples/outputs/thesis_impact.json, examples/outputs/pretrade_plan.json, examples/outputs/portfolio_exposure.json |
| regime_chop | regime_trigger | medium | triggered | Chop stress trigger | examples/outputs/stress_matrix.json |
| regime_rebound | regime_trigger | medium | triggered | Rebound stress trigger | examples/outputs/stress_matrix.json |
| regime_trend_up | regime_trigger | medium | triggered | Trend Up stress trigger | examples/outputs/stress_matrix.json |

### regime_gap_down: Gap Down stress trigger

- Category: regime_trigger
- Severity: critical
- Status: triggered
- Trigger: return -48.8504%; worst drawdown -52.5497%; path decay 5.694511; band events: day 1 stop_loss at NAV 74.49623

Next review questions:

- [ ] Would the thesis still be acceptable under the gap_down regime?
- [ ] What pre-defined action follows if this regime starts to resemble the current market path?
- [ ] Are modeled stop or take-profit band events acceptable after accounting for execution and gap risk?
- [ ] Is the loss budget still valid under this modeled return?

Source artifact refs:

- examples/outputs/stress_matrix.json (stress_matrix 0.9): stress row gap_down

Warnings:

- 4 stress-matrix warning(s) observed for this regime.

### claim_1: The modeled trade is a short-horizon tactical scenario for a generic daily-re...

- Category: claim
- Severity: high
- Status: challenged
- Trigger: The modeled trade is a short-horizon tactical scenario for a generic daily-reset leveraged ETP. The thesis assumes the reference index can recover after recent volatility, but recognizes that choppy paths can create decay even when the underlying ends near flat.

Next review questions:

- [ ] What evidence would change the status of claim_1 from challenged?
- [ ] Which observed metrics are most relevant to the claim, and are any expected metrics missing?
- [ ] Record whether the observed artifact metrics support, challenge, or leave the claim unresolved.
- [ ] Compare the thesis return expectation with modeled ETP and underlying returns.
- [ ] Review path decay versus the simple multiple before relying on multi-day leverage.
- [ ] Which warning would invalidate the thesis if it appears in live review?

Source artifact refs:

- examples/outputs/thesis_impact.json (thesis_impact 0.6): claim mapping claim_1
- examples/outputs/pretrade_plan.json (observed_metric_source n/a): return_pct for claim_1
- examples/outputs/pretrade_plan.json (observed_metric_source n/a): path_decay_vs_simple_multiple for claim_1
- examples/outputs/portfolio_exposure.json (observed_metric_source n/a): return_pct for claim_1
- examples/outputs/portfolio_exposure.json (observed_metric_source n/a): weighted_exposure for claim_1

Warnings:

- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.
- Fee drag is approximated as a constant daily deduction from the leveraged daily return.
- Weighted exposure uses starting notional weights and product daily leverage factors.

### regime_trend_down: Trend Down stress trigger

- Category: regime_trigger
- Severity: high
- Status: triggered
- Trigger: return -19.8516%; worst drawdown -19.8516%; path decay 1.136554; band events: day 8 stop_loss at NAV 84.483822

Next review questions:

- [ ] Would the thesis still be acceptable under the trend_down regime?
- [ ] What pre-defined action follows if this regime starts to resemble the current market path?
- [ ] Are modeled stop or take-profit band events acceptable after accounting for execution and gap risk?
- [ ] Is the loss budget still valid under this modeled return?

Source artifact refs:

- examples/outputs/stress_matrix.json (stress_matrix 0.9): stress row trend_down

Warnings:

- 4 stress-matrix warning(s) observed for this regime.

### regime_volatility_cluster: Volatility Cluster stress trigger

- Category: regime_trigger
- Severity: high
- Status: triggered
- Trigger: return -9.0937%; worst drawdown -16.3862%; path decay -3.205395; band events: day 7 stop_loss at NAV 83.613785

Next review questions:

- [ ] Would the thesis still be acceptable under the volatility_cluster regime?
- [ ] What pre-defined action follows if this regime starts to resemble the current market path?
- [ ] Are modeled stop or take-profit band events acceptable after accounting for execution and gap risk?
- [ ] Does modeled path decay weaken the expected holding-period thesis?
- [ ] Is the loss budget still valid under this modeled return?

Source artifact refs:

- examples/outputs/stress_matrix.json (stress_matrix 0.9): stress row volatility_cluster

Warnings:

- 4 stress-matrix warning(s) observed for this regime.

### claim_2: The plan should be rejected if the loss budget, stop band, liquidity review,...

- Category: claim
- Severity: medium
- Status: needs_review
- Trigger: The plan should be rejected if the loss budget, stop band, liquidity review, or event-risk checklist cannot be accepted before entry.

Next review questions:

- [ ] What evidence would change the status of claim_2 from needs_review?
- [ ] Which observed metrics are most relevant to the claim, and are any expected metrics missing?
- [ ] Record whether the observed artifact metrics support, challenge, or leave the claim unresolved.
- [ ] Confirm loss budget and stop band are acceptable before entry.
- [ ] Complete a liquidity and execution-quality review outside this model.
- [ ] Which warning would invalidate the thesis if it appears in live review?

Source artifact refs:

- examples/outputs/thesis_impact.json (thesis_impact 0.6): claim mapping claim_2
- examples/outputs/pretrade_plan.json (observed_metric_source n/a): return_pct for claim_2
- examples/outputs/pretrade_plan.json (observed_metric_source n/a): path_decay_vs_simple_multiple for claim_2
- examples/outputs/portfolio_exposure.json (observed_metric_source n/a): return_pct for claim_2
- examples/outputs/portfolio_exposure.json (observed_metric_source n/a): weighted_exposure for claim_2

Warnings:

- Large daily moves can compound quickly and may create losses larger than a simple one-day estimate.
- A pretrade plan does not confirm liquidity, execution quality, tax treatment, or suitability.
- Stop-loss and take-profit bands are planning levels, not guaranteed execution prices.
- Portfolio aggregation is scenario-based and does not model tax, borrow, spread, liquidity, or intraday stop execution.

### regime_chop: Chop stress trigger

- Category: regime_trigger
- Severity: medium
- Status: triggered
- Trigger: return -0.3186%; worst drawdown -6.5029%; path decay -1.429133

Next review questions:

- [ ] Would the thesis still be acceptable under the chop regime?
- [ ] What pre-defined action follows if this regime starts to resemble the current market path?
- [ ] Does modeled path decay weaken the expected holding-period thesis?
- [ ] Is the loss budget still valid under this modeled return?

Source artifact refs:

- examples/outputs/stress_matrix.json (stress_matrix 0.9): stress row chop

Warnings:

- 4 stress-matrix warning(s) observed for this regime.

### regime_rebound: Rebound stress trigger

- Category: regime_trigger
- Severity: medium
- Status: triggered
- Trigger: return 5.1886%; worst drawdown -12.5903%; path decay -1.385944

Next review questions:

- [ ] Would the thesis still be acceptable under the rebound regime?
- [ ] What pre-defined action follows if this regime starts to resemble the current market path?
- [ ] Does modeled path decay weaken the expected holding-period thesis?

Source artifact refs:

- examples/outputs/stress_matrix.json (stress_matrix 0.9): stress row rebound

Warnings:

- 4 stress-matrix warning(s) observed for this regime.

### regime_trend_up: Trend Up stress trigger

- Category: regime_trigger
- Severity: medium
- Status: triggered
- Trigger: return 20.0961%; worst drawdown -0.6038%; path decay 0.994607; band events: day 12 take_profit at NAV 120.096051

Next review questions:

- [ ] Would the thesis still be acceptable under the trend_up regime?
- [ ] What pre-defined action follows if this regime starts to resemble the current market path?
- [ ] Are modeled stop or take-profit band events acceptable after accounting for execution and gap risk?

Source artifact refs:

- examples/outputs/stress_matrix.json (stress_matrix 0.9): stress row trend_up

Warnings:

- 4 stress-matrix warning(s) observed for this regime.
