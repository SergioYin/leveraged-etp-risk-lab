# Pre-Order Ticket: NDAQ3X

**Not investment advice:** This pre-order ticket is for scenario planning and education only. It is not investment advice, a recommendation, a suitability determination, or a broker order.

## Summary

- Status: review
- Max notional: 5000.0 USD
- Max shares: n/a
- Guardrail result: review

## Order Intent Placeholders

- limit_price: set-by-user-no-live-price
- notes: placeholder-only; this package does not place, stage, route, or execute orders
- order_type: set-by-user
- planned_entry_window: set-by-user
- side: set-by-user
- stop_or_exit_plan: set-by-user
- time_in_force: set-by-user

## Required Broker Fields

- [ ] account: Broker account must be selected outside this package.
- [ ] symbol: Confirm ticker and listing venue in broker UI.
- [ ] side: User must choose buy/sell or other permitted side.
- [ ] quantity: Convert notional to shares with an execution price outside this package.
- [ ] order_type: User must choose market, limit, stop, or other broker-supported type.
- [ ] limit_or_stop_price: Required when selected order type needs a price; no live price is provided here.
- [ ] time_in_force: User must choose day, GTC, or other broker-supported duration.
- [ ] estimated_commission_and_fees: Confirm broker preview costs outside this package.
- [ ] liquidity_spread_halt_review: Confirm spread, depth, halts, and trading status outside this package.

## No Live Price Warning

No live or delayed market data is read; confirm quote, spread, liquidity, and broker order preview outside this package.

## Do Not Trade If

- [ ] No current broker quote, spread, liquidity, halt, and order preview has been reviewed.
- [ ] Any required broker field remains unset or inconsistent with the user's intent.
- [ ] Guardrail check has review items that have not been explicitly resolved.
- [ ] Review aggregate modeled portfolio loss against the stated budget before proceeding.
- [ ] Close or explicitly accept memo open checks before relying on the allocation.
- [ ] Review memo invalidation triggers and regenerate memo artifacts if the thesis changed.
- [ ] Resolve cycle-update next review actions before proceeding.
- [ ] Investment memo has open checks.
- [ ] return -48.8504%; worst drawdown -52.5497%; path decay 5.694511; band events: day 1 stop_loss at NAV 74.49623
- [ ] return -19.8516%; worst drawdown -19.8516%; path decay 1.136554; band events: day 8 stop_loss at NAV 84.483822
- [ ] The modeled trade is a short-horizon tactical scenario for a generic daily-reset leveraged ETP. The thesis assumes the reference index can recover after recent volatility, but recognizes that choppy paths can create decay even when the underlying ends near flat.
- [ ] The plan should be rejected if the loss budget, stop band, liquidity review, or event-risk checklist cannot be accepted before entry.
- [ ] Thesis dashboard data is not decision-ready.

## Warnings

- No live price, bid-ask spread, depth, halt, or broker availability check is performed.
- This order ticket is a pre-order educational checklist, not an instruction to trade.
- Broker fields remain placeholders and must be completed outside this package.
- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.
- Large daily moves can compound quickly and may create losses larger than a simple one-day estimate.
- Fee drag is approximated as a constant daily deduction from the leveraged daily return.
