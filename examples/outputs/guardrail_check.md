# Allocation Guardrail Check

**Not investment advice:** This allocation guardrail check is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## Summary

- Result: review
- Rules: 5 pass, 4 review, 0 fail

## Observed Metrics

- aggregate_worst_case_loss_pct: 48.8518
- cycle_added_watch_items: 0
- cycle_changed_watch_items: 0
- cycle_decision_ready: False
- cycle_hash_drift: 0
- cycle_removed_watch_items: 0
- cycle_status_transitions: 1.0
- holding_days: 6.0
- leverage_exposure: 3.0
- loss_budget_pct: 1.5
- memo_critical_triggers: 1
- memo_high_triggers: 2
- memo_invalidation_triggers: 7
- memo_open_checks: 11
- position_exposure_multiple: 0.3

## Rules

| Rule | Status | Observed | Limit | Action |
| --- | --- | --- | --- | --- |
| max_leverage_exposure | pass | 3.0 | 3.0 | No action required. |
| max_loss_budget_pct | pass | 1.5 | 1.5 | No action required. |
| max_holding_days | pass | 6.0 | 10.0 | No action required. |
| required_artifacts | pass | cycle_update,investment_memo_packet,portfolio_sensitivity,position_size_plan | portfolio_sensitivity,position_size_plan,investment_memo_packet,cycle_update | No action required. |
| aggregate_modeled_loss_review | review | 48.8518 | 1.5 | Review aggregate modeled portfolio loss against the stated budget before proceeding. |
| memo_open_checks | review | 11 | 0 | Close or explicitly accept memo open checks before relying on the allocation. |
| memo_invalidation_triggers | review | 3 | 0 | Review memo invalidation triggers and regenerate memo artifacts if the thesis changed. |
| cycle_decision_ready | review | False | True | Resolve cycle-update next review actions before proceeding. |
| cycle_changes | pass | 0 | 0 | No action required. |

## Next Actions

- [ ] Complete review items before relying on the allocation packet.
- [ ] Review aggregate modeled portfolio loss against the stated budget before proceeding.
- [ ] Close or explicitly accept memo open checks before relying on the allocation.
- [ ] Review memo invalidation triggers and regenerate memo artifacts if the thesis changed.
- [ ] Resolve cycle-update next review actions before proceeding.
