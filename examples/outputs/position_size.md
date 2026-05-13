# Position Size Plan: NDAQ3X

**Not investment advice:** This position sizing planner is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## Product

- Product: Generic 3x Nasdaq Daily Reset ETP
- Underlying: Nasdaq-100 reference index
- Daily leverage: 3.0x
- Currency: USD

## Budget

- Account value: 50000.0 USD
- Maximum loss budget: 750.0 USD
- Risk budget: 1.5%
- Stop-loss: 15.0%
- Loss basis: stop_loss

## Recommendation

- Recommended notional: 5000.0 USD
- Max shares: n/a
- Max shares placeholder: Divide recommended_notional by the intended execution price; no live price is modeled.
- Modeled loss at stop: 750.0 USD
- Modeled loss as account percent: 1.5%
- Exposure multiple: 0.3x

## Scenario

- Scenario days: 6
- Ending ETP NAV: 100.608795
- ETP return: 0.6088%
- Underlying return: 0.4038%
- Path decay vs simple multiple: -0.602755

## Checklist

- [ ] Confirm account value and loss budget before using the notional figure.
- [ ] Convert notional to shares with the intended execution price outside this model.
- [ ] Check liquidity, spreads, trading halts, and gap risk before relying on a stop.
- [ ] Compare exposure multiple with portfolio concentration and leverage limits.
- [ ] Record that this output is for scenario planning and is not investment advice.

## Warnings

- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.
- Large daily moves can compound quickly and may create losses larger than a simple one-day estimate.
- Fee drag is approximated as a constant daily deduction from the leveraged daily return.
- Recommended notional is a deterministic planning output, not a trade recommendation.
- Share count is a placeholder because no live or execution price is modeled.
- Stop-loss levels are planning inputs and do not guarantee execution at the modeled loss.

## Command Provenance

- account_value: 50000.0
- command: position-size
- max_loss_budget: None
- path: examples/fixtures/nasdaq_chop_path.csv
- product: examples/fixtures/leveraged_nasdaq_3x.json
- risk_budget_pct: 0.015
- source: product_path
- stop_loss: 0.15
