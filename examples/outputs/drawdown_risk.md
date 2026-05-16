# Drawdown Risk Under Regime Stress

**Not investment advice:** This scenario pack is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## New User Question

Which deterministic regime hurts most, and what does that imply for a portfolio-level loss budget?

## Answer

The stress matrix ranks built-in regimes by modeled return and drawdown, while portfolio sensitivity translates the weakest rows into aggregate modeled loss and weighted exposure.

## Key Metrics

| Metric | Value |
| --- | ---: |
| worst_regime | gap_down |
| worst_regime_return_pct | -48.8504 |
| worst_regime_drawdown_pct | -52.5497 |
| aggregate_worst_case_modeled_loss | 4885.18 |
| aggregate_worst_case_loss_pct | 48.8518 |
| aggregate_worst_case_weighted_exposure | 3.0 |
| portfolio_positions | 2 |
| manifest_positions | 2 |

## Takeaways

- Worst return and worst drawdown can point to the same regime, but they are separate checks.
- Portfolio sensitivity converts product-level stress into a budget-sized loss number.
- Weighted exposure helps separate notional size from effective leveraged exposure.

## Guardrails To Check

- Review aggregate modeled loss before adding exposure to an existing portfolio.
- Treat stop events as review triggers because gap risk and execution quality are not modeled.
- Use regime stress alongside, not instead of, thesis invalidation checks.

## New User Evidence

### Exact Commands

- Regenerate the deterministic demo inputs used by the pack.
  `python -m leveraged_etp_risk_lab demo-bundle --output-dir examples/outputs`
- Regenerate the new-user scenario pack and case-study outputs.
  `python -m leveraged_etp_risk_lab scenario-pack --input-dir examples/outputs --fixtures-dir examples/fixtures --output-dir examples/outputs --format markdown`
- Validate the scenario-pack artifacts against local schemas.
  `python -m leveraged_etp_risk_lab artifact-validate examples/outputs/scenario_pack.json examples/outputs/daily_reset_path_decay.json examples/outputs/drawdown_risk.json examples/outputs/pretrade_guardrails.json --format markdown`
- Inspect the source artifact behind this case.
  `python -m leveraged_etp_risk_lab portfolio-sensitivity --manifest examples/fixtures/portfolio_manifest.json --stop-loss none,0.15 --take-profit none,0.20 --format markdown`

### Artifact Links

- [Drawdown risk JSON](drawdown_risk.json) (`examples/outputs/drawdown_risk.json`)
- [Drawdown risk Markdown](drawdown_risk.md) (`examples/outputs/drawdown_risk.md`)
- [Stress matrix source](stress_matrix.json) (`examples/outputs/stress_matrix.json`)
- [Portfolio sensitivity source](portfolio_sensitivity.json) (`examples/outputs/portfolio_sensitivity.json`)

### Safety Boundaries

- Uses checked-in fixtures and generated local examples only.
- Does not read live market data, private context, workflow files, environment variables, or command history.
- Does not place trades, contact brokers, determine suitability, or recommend buying, selling, or holding any product.
- Treats position sizing and guardrail outputs as educational review aids, not instructions.

## Source Artifacts

- examples/outputs/stress_matrix.json (json)
- examples/outputs/portfolio_sensitivity.json (json)
- examples/fixtures/portfolio_manifest.json (json)

## Warnings

- This case study uses deterministic local examples only.
- It does not model live prices, spreads, liquidity, taxes, suitability, or broker execution.
