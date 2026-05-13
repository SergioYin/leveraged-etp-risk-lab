# Decision Readiness Report Card

**Not investment advice:** This report card is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## Summary

- Artifacts: 8
- Document types: factsheet_check, portfolio_sensitivity, position_size_plan, pretrade_plan, recipe_run, risk_profile_rules, sensitivity_grid, stress_matrix
- Decision ready: no

## Strengths

- NDAQ3X pretrade plan records thesis, risk bands, and a 750.0 USD loss budget.
- Checklist profile is risk-review.
- Position sizing converts the loss budget into 5000.0 notional.
- Max-share count is intentionally left as a placeholder because no live price is fetched.
- Stress matrix covers 6 deterministic regime rows.
- Sensitivity grid covers 27 leverage and risk-band combinations.
- Portfolio sensitivity covers 2 position(s).
- Aggregate worst-case modeled loss is 4885.18.

## Unresolved Checks

- Checklist item: Confirm the product uses daily reset leverage and identify the stated leverage factor.
- Checklist item: Compare the planned holding period with the product objective and risk disclosures.
- Checklist item: Run at least one trending path and one choppy path before sizing the trade.
- Checklist item: Record stop-loss and take-profit levels before entry.
- Checklist item: Review borrowing, financing, and management-fee drag assumptions.
- Confirm liquidity, execution quality, tax treatment, and suitability outside this model.
- Checklist item: Confirm account value and loss budget before using the notional figure.
- Checklist item: Convert notional to shares with the intended execution price outside this model.
- Checklist item: Check liquidity, spreads, trading halts, and gap risk before relying on a stop.
- Checklist item: Compare exposure multiple with portfolio concentration and leverage limits.

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

## Artifact Cards

| Artifact | Type | Schema | Strengths | Checks | Warnings |
| --- | --- | --- | --- | --- | --- |
| examples/outputs/pretrade_plan.json | pretrade_plan | 0.3 | 2 | 6 | 6 |
| examples/outputs/position_size.json | position_size_plan | 0.8 | 2 | 6 | 7 |
| examples/outputs/stress_matrix.json | stress_matrix | 0.9 | 1 | 2 | 14 |
| examples/outputs/sensitivity_grid.json | sensitivity_grid | 0.19 | 1 | 3 | 10 |
| examples/outputs/portfolio_sensitivity.json | portfolio_sensitivity | 0.20 | 2 | 2 | 8 |
| examples/outputs/factsheet_check.json | factsheet_check | 0.15 | 1 | 1 | 1 |
| examples/outputs/risk_profiles.json | risk_profile_rules | 0.16 | 1 | 1 | 0 |
| examples/outputs/recipe_run.json | recipe_run | 0.17 | 2 | 6 | 9 |

## Next Commands

- `python -m leveraged_etp_risk_lab report-card --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/position_size.json --artifact examples/outputs/stress_matrix.json --artifact examples/outputs/factsheet_check.json --format markdown`
- `python -m leveraged_etp_risk_lab package-audit --format markdown --run-tests`

## Provenance

- artifacts: ['examples/outputs/pretrade_plan.json', 'examples/outputs/position_size.json', 'examples/outputs/stress_matrix.json', 'examples/outputs/sensitivity_grid.json', 'examples/outputs/portfolio_sensitivity.json', 'examples/outputs/factsheet_check.json', 'examples/outputs/risk_profiles.json', 'examples/outputs/recipe_run.json']
- command: report-card
- live_market_data: False
- shell_out: False
