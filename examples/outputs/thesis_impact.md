# Thesis Impact

- Thesis file: examples/fixtures/thesis_note.md
- Artifacts: examples/outputs/pretrade_plan.json, examples/outputs/compare_runs.json, examples/outputs/portfolio_exposure.json
- Claims mapped: 2

## Artifact Metrics

| artifact | type | label | return_pct | path_decay_vs_simple_multiple | weighted_exposure | warnings |
| --- | --- | --- | --- | --- | --- | --- |
| examples/outputs/pretrade_plan.json | pretrade_plan | NDAQ3X | 0.6088 | -0.602755 | n/a | 6 |
| examples/outputs/compare_runs.json | run_comparison | run_comparison | n/a | n/a | n/a | 0 |
| examples/outputs/portfolio_exposure.json | exposure_report | Generic Leveraged ETP Portfolio | -5.5366 | n/a | 2.6 | 6 |

## Claim Mapping

### claim_1: challenged

The modeled trade is a short-horizon tactical scenario for a generic daily-reset leveraged ETP. The thesis assumes the reference index can recover after recent volatility, but recognizes that choppy paths can create decay even when the underlying ends near flat.

Observed metrics:

- examples/outputs/pretrade_plan.json return_pct: 0.6088 (observed return metric)
- examples/outputs/pretrade_plan.json path_decay_vs_simple_multiple: -0.602755 (shows modeled path decay)
- examples/outputs/portfolio_exposure.json return_pct: -5.5366 (challenges positive-return claim)
- examples/outputs/portfolio_exposure.json weighted_exposure: 2.6 (shows elevated leveraged exposure)

Warnings:

- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.
- Fee drag is approximated as a constant daily deduction from the leveraged daily return.
- Weighted exposure uses starting notional weights and product daily leverage factors.

Checklist:

- [ ] Record whether the observed artifact metrics support, challenge, or leave the claim unresolved.
- [ ] Compare the thesis return expectation with modeled ETP and underlying returns.
- [ ] Review path decay versus the simple multiple before relying on multi-day leverage.
- [ ] Check aggregate exposure and concentration against portfolio limits.

### claim_2: needs_review

The plan should be rejected if the loss budget, stop band, liquidity review, or event-risk checklist cannot be accepted before entry.

Observed metrics:

- examples/outputs/pretrade_plan.json return_pct: 0.6088 (observed return metric)
- examples/outputs/pretrade_plan.json path_decay_vs_simple_multiple: -0.602755 (shows modeled path decay)
- examples/outputs/portfolio_exposure.json return_pct: -5.5366 (confirms downside scenario is present)
- examples/outputs/portfolio_exposure.json weighted_exposure: 2.6 (shows elevated leveraged exposure)

Warnings:

- Large daily moves can compound quickly and may create losses larger than a simple one-day estimate.
- A pretrade plan does not confirm liquidity, execution quality, tax treatment, or suitability.
- Stop-loss and take-profit bands are planning levels, not guaranteed execution prices.
- Portfolio aggregation is scenario-based and does not model tax, borrow, spread, liquidity, or intraday stop execution.

Checklist:

- [ ] Record whether the observed artifact metrics support, challenge, or leave the claim unresolved.
- [ ] Confirm loss budget and stop band are acceptable before entry.
- [ ] Complete a liquidity and execution-quality review outside this model.
- [ ] Check event risk before treating the scenario as actionable.

## Action Checklist

- [ ] Record whether the observed artifact metrics support, challenge, or leave the claim unresolved.
- [ ] Compare the thesis return expectation with modeled ETP and underlying returns.
- [ ] Review path decay versus the simple multiple before relying on multi-day leverage.
- [ ] Check aggregate exposure and concentration against portfolio limits.
- [ ] Confirm loss budget and stop band are acceptable before entry.
- [ ] Complete a liquidity and execution-quality review outside this model.
- [ ] Check event risk before treating the scenario as actionable.

## Warnings

- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.
- Large daily moves can compound quickly and may create losses larger than a simple one-day estimate.
- Fee drag is approximated as a constant daily deduction from the leveraged daily return.
- A pretrade plan does not confirm liquidity, execution quality, tax treatment, or suitability.
- Stop-loss and take-profit bands are planning levels, not guaranteed execution prices.
- Portfolio aggregation is scenario-based and does not model tax, borrow, spread, liquidity, or intraday stop execution.
- Weighted exposure uses starting notional weights and product daily leverage factors.
