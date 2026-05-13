# Allocation Guardrail Policy: default

**Not investment advice:** This allocation guardrail policy is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

Balanced public default for short-horizon leveraged ETP scenario review.

## Limits

- Max leverage exposure: 3.0x
- Max loss budget: 1.5%
- Max holding days: 10

## Required Artifacts

- portfolio_sensitivity
- position_size_plan
- investment_memo_packet
- cycle_update

## Review Conditions

- Review if investment memo open checks remain unresolved.
- Review if cycle-update is not decision-ready.
- Review if latest cycle-update reports added, changed, or removed watch items.
- Review if critical or high memo invalidation triggers are present.
- Review if aggregate modeled portfolio loss exceeds the loss-budget percent.

## Provenance

- command: guardrail-policy
- live_market_data: False
- profile: default
- shell_out: False
