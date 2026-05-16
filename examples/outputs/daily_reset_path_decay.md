# Daily Reset Path Decay

**Not investment advice:** This scenario pack is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## New User Question

If the underlying ends close to flat after a choppy path, why can a 3x daily-reset product still lag a simple 3x multiple?

## Answer

The example decomposes the modeled ending NAV against the simple multiple. The path-decay field shows the multi-day compounding gap created by alternating daily returns and fee drag.

## Key Metrics

| Metric | Value |
| --- | ---: |
| nasdaq_underlying_return_pct | 0.4038 |
| nasdaq_etp_return_pct | 0.6088 |
| nasdaq_simple_multiple_return_pct | 1.2115 |
| nasdaq_path_decay_nav_points | -0.602755 |
| single_stock_path_decay_nav_points | -0.653442 |
| case_delta_path_decay_nav_points | -0.050687 |
| nasdaq_path_days | 6 |
| nasdaq_fixture_days | 6 |

## Takeaways

- Compare ending ETP return with the simple multiple before treating leverage as a linear multi-day exposure.
- A choppy path can make the daily reset product worse than the simple multiple even when the underlying move looks modest.
- The gap is expressed in NAV points so a new user can inspect it without live prices.

## Guardrails To Check

- Limit holding period assumptions when daily swings dominate the thesis.
- Run compare-runs before replacing one leveraged product or path with another.
- Record path-decay tolerance in the pretrade plan before sizing the position.

## New User Evidence

### Exact Commands

- Regenerate the deterministic demo inputs used by the pack.
  `python -m leveraged_etp_risk_lab demo-bundle --output-dir examples/outputs`
- Regenerate the new-user scenario pack and case-study outputs.
  `python -m leveraged_etp_risk_lab scenario-pack --input-dir examples/outputs --fixtures-dir examples/fixtures --output-dir examples/outputs --format markdown`
- Validate the scenario-pack artifacts against local schemas.
  `python -m leveraged_etp_risk_lab artifact-validate examples/outputs/scenario_pack.json examples/outputs/daily_reset_path_decay.json examples/outputs/drawdown_risk.json examples/outputs/pretrade_guardrails.json --format markdown`
- Inspect the source artifact behind this case.
  `python -m leveraged_etp_risk_lab compare-runs --base examples/outputs/leveraged_nasdaq_3x.json --candidate examples/outputs/single_stock_2x.json --format markdown`

### Artifact Links

- [Daily reset path decay JSON](daily_reset_path_decay.json) (`examples/outputs/daily_reset_path_decay.json`)
- [Daily reset path decay Markdown](daily_reset_path_decay.md) (`examples/outputs/daily_reset_path_decay.md`)
- [NASDAQ simulation source](leveraged_nasdaq_3x.json) (`examples/outputs/leveraged_nasdaq_3x.json`)
- [Comparison source](compare_runs.json) (`examples/outputs/compare_runs.json`)

### Safety Boundaries

- Uses checked-in fixtures and generated local examples only.
- Does not read live market data, private context, workflow files, environment variables, or command history.
- Does not place trades, contact brokers, determine suitability, or recommend buying, selling, or holding any product.
- Treats position sizing and guardrail outputs as educational review aids, not instructions.

## Source Artifacts

- examples/outputs/leveraged_nasdaq_3x.json (json)
- examples/outputs/single_stock_2x.json (json)
- examples/outputs/compare_runs.json (json)
- examples/fixtures/leveraged_nasdaq_3x.json (json)
- examples/fixtures/single_stock_2x.json (json)
- examples/fixtures/nasdaq_chop_path.csv (csv)

## Warnings

- This case study uses deterministic local examples only.
- It does not model live prices, spreads, liquidity, taxes, suitability, or broker execution.
