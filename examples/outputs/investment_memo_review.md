# Investment Memo Review

**Not investment advice:** This memo review is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## Summary

- Decision ready: no
- Checklist: 2 pass, 4 review
- Changed risks: 6

## Checklist

| id | status | item | action |
| --- | --- | --- | --- |
| memo_not_investment_advice | pass | Memo contains not-investment-advice language. | Keep explicit educational framing in the memo. |
| report_card_decision_ready | review | Latest report-card is decision-ready. | Resolve latest report-card unresolved checks and warnings. |
| watchlist_risks_stable | review | Watchlist has no added or changed memo risks. | Update memo invalidation triggers from latest watchlist. |
| audit_trail_passed | pass | Audit trail hashes pass for reviewed artifacts. | Regenerate ledger or investigate artifacts with audit review status. |
| open_checks_closed | review | Memo open checks are closed or accepted. | Close or explicitly accept each memo open check. |
| critical_watchlist_clear | review | Latest watchlist has no critical entries. | Escalate critical watchlist triggers before any decision review. |

## Changed Risks

- claim_1: worsened - medium/needs_review -> high/challenged
- decision_not_ready: removed - Report card is not decision-ready.
- regime_rebound: added - return 5.1886%; worst drawdown -12.5903%; path decay -1.385944
- regime_trend_up: added - return 20.0961%; worst drawdown -0.6038%; path decay 0.994607; band events: day 12 take_profit at NAV 120.096051
- regime_volatility_cluster: added - return -9.0937%; worst drawdown -16.3862%; path decay -3.205395; band events: day 7 stop_loss at NAV 83.613785
- worst_grid_return: removed - Worst grid return is -48.8504% in gap_down.

## Next Actions

- [ ] Resolve latest report-card unresolved checks and warnings.
- [ ] Update memo invalidation triggers from latest watchlist.
- [ ] Close or explicitly accept each memo open check.
- [ ] Escalate critical watchlist triggers before any decision review.
- [ ] Regenerate memo-draft after reviewing changed watchlist risks.
- [ ] python -m leveraged_etp_risk_lab report-card --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/position_size.json --artifact examples/outputs/stress_matrix.json --artifact examples/outputs/factsheet_check.json --format markdown
- [ ] python -m leveraged_etp_risk_lab package-audit --format markdown --run-tests
