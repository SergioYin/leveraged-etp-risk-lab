# Watch Cycle State

**Not investment advice:** This watch cycle state is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## Summary

- State id: cycle_c46a3e619fcf75f4
- Watch items: 8
- Open checks: 11
- Baseline risks: 9
- Decision ready: no

## Baseline Artifact Hashes

| Artifact | Type | Schema | SHA-256 |
| --- | --- | --- | --- |
| investment_memo.json | investment_memo_packet | 0.21 | e65fdac470f187a1b38ecc8c67b034364fcbb86f98193f09f35e01767be0dbf7 |
| watchlist.json | watchlist | 0.10 | 31eb2d3ed67f894ef362ed078845d4db489e3270eebf312aa39951a5d9134aa4 |
| report_card.json | report_card | 0.18 | 77e2de589d7bcc779073c6e99affc7d5cee32c524ab2374a02dd1a2b76ce7a76 |
| sensitivity_grid.json | sensitivity_grid | 0.19 | 37c2e08ee361260a79c744df8f5d373ab6cee9ec07cf3f97e2cb081270757f0d |

## Baseline Risks

- regime_gap_down (critical): return -48.8504%; worst drawdown -52.5497%; path decay 5.694511; band events: day 1 stop_loss at NAV 74.49623
- regime_trend_down (high): return -19.8516%; worst drawdown -19.8516%; path decay 1.136554; band events: day 8 stop_loss at NAV 84.483822
- regime_volatility_cluster (high): return -9.0937%; worst drawdown -16.3862%; path decay -3.205395; band events: day 7 stop_loss at NAV 83.613785
- sensitivity_worst_return (high): Worst grid return is -48.8504% in gap_down.
- worst_grid_return (high): Worst grid return is -48.8504% in gap_down.
- claim_1 (medium): The modeled trade is a short-horizon tactical scenario for a generic daily-reset leveraged ETP. The thesis assumes the reference index can recover after recent volatility, but recognizes that choppy paths can create decay even when the underlying ends near flat.
- claim_2 (medium): The plan should be rejected if the loss budget, stop band, liquidity review, or event-risk checklist cannot be accepted before entry.
- decision_not_ready (medium): Report card is not decision-ready.
- regime_chop (medium): return -0.3186%; worst drawdown -6.5029%; path decay -1.429133

## Open Checks

- [ ] Checklist item: Confirm the product uses daily reset leverage and identify the stated leverage factor.
- [ ] Checklist item: Compare the planned holding period with the product objective and risk disclosures.
- [ ] Checklist item: Run at least one trending path and one choppy path before sizing the trade.
- [ ] Checklist item: Record stop-loss and take-profit levels before entry.
- [ ] Checklist item: Review borrowing, financing, and management-fee drag assumptions.
- [ ] Confirm liquidity, execution quality, tax treatment, and suitability outside this model.
- [ ] Checklist item: Confirm account value and loss budget before using the notional figure.
- [ ] Checklist item: Convert notional to shares with the intended execution price outside this model.
- [ ] Checklist item: Check liquidity, spreads, trading halts, and gap risk before relying on a stop.
- [ ] Checklist item: Compare exposure multiple with portfolio concentration and leverage limits.
- [ ] Review factsheet field: liquidity_spread

## Review Cadence

- cadence: placeholder
- next_review: set-by-user
- review_inputs: ['latest report_card', 'latest watchlist', 'latest audit_trail']
- review_owner: set-by-user
