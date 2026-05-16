# Pretrade Guardrails Before An Order

**Not investment advice:** This scenario pack is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## New User Question

How does a new user connect a thesis, loss budget, position size, and order review without sending a trade?

## Answer

The pretrade artifacts keep the workflow in review mode. The size plan converts a loss budget into placeholder notional, then guardrail and order-review artifacts report whether required checks are ready.

## Key Metrics

| Metric | Value |
| --- | ---: |
| pretrade_loss_budget | 750.0 |
| scenario_etp_return_pct | 0.6088 |
| stop_loss_pct | 15.0 |
| recommended_notional | 5000.0 |
| modeled_loss_at_stop | 750.0 |
| exposure_multiple | 0.3 |
| guardrail_status | review |
| order_review_status | review |
| thesis_lines | 3 |

## Takeaways

- Sizing is derived from the modeled loss budget and stop assumption, not from a live recommendation.
- Guardrail status is an explicit gate for exposure, loss-budget, holding-period, and review conditions.
- Order review remains placeholder-only and records that no broker execution is modeled.

## Guardrails To Check

- Resolve guardrail review items before treating an order ticket as complete.
- Convert notional to shares outside the model with the intended execution price.
- Keep factsheet, thesis, cycle, and audit artifacts attached to the pretrade record.

## New User Evidence

### Exact Commands

- Regenerate the deterministic demo inputs used by the pack.
  `python -m leveraged_etp_risk_lab demo-bundle --output-dir examples/outputs`
- Regenerate the new-user scenario pack and case-study outputs.
  `python -m leveraged_etp_risk_lab scenario-pack --input-dir examples/outputs --fixtures-dir examples/fixtures --output-dir examples/outputs --format markdown`
- Validate the scenario-pack artifacts against local schemas.
  `python -m leveraged_etp_risk_lab artifact-validate examples/outputs/scenario_pack.json examples/outputs/daily_reset_path_decay.json examples/outputs/drawdown_risk.json examples/outputs/pretrade_guardrails.json --format markdown`
- Inspect the source artifact behind this case.
  `python -m leveraged_etp_risk_lab order-review --order-ticket examples/outputs/order_ticket.json --guardrail-check examples/outputs/guardrail_check.json --cycle-update examples/outputs/cycle_update.json --audit-trail examples/outputs/audit_trail.json --format markdown`

### Artifact Links

- [Pretrade guardrails JSON](pretrade_guardrails.json) (`examples/outputs/pretrade_guardrails.json`)
- [Pretrade guardrails Markdown](pretrade_guardrails.md) (`examples/outputs/pretrade_guardrails.md`)
- [Pretrade plan source](pretrade_plan.json) (`examples/outputs/pretrade_plan.json`)
- [Order review source](order_review.json) (`examples/outputs/order_review.json`)

### Safety Boundaries

- Uses checked-in fixtures and generated local examples only.
- Does not read live market data, private context, workflow files, environment variables, or command history.
- Does not place trades, contact brokers, determine suitability, or recommend buying, selling, or holding any product.
- Treats position sizing and guardrail outputs as educational review aids, not instructions.

## Source Artifacts

- examples/outputs/pretrade_plan.json (json)
- examples/outputs/position_size.json (json)
- examples/outputs/guardrail_check.json (json)
- examples/outputs/order_review.json (json)
- examples/fixtures/thesis_note.md (md)

## Warnings

- This case study uses deterministic local examples only.
- It does not model live prices, spreads, liquidity, taxes, suitability, or broker execution.
