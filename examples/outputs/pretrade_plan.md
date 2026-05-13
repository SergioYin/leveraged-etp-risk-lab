# Pretrade Plan: NDAQ3X

**Not investment advice:** This decision packet is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## Product

- Product: Generic 3x Nasdaq Daily Reset ETP
- Underlying: Nasdaq-100 reference index
- Daily leverage: 3.0x
- Reset frequency: daily
- Annual fee: 0.95%

## Thesis

# Example Thesis Note

The modeled trade is a short-horizon tactical scenario for a generic daily-reset leveraged ETP. The thesis assumes the reference index can recover after recent volatility, but recognizes that choppy paths can create decay even when the underlying ends near flat.

The plan should be rejected if the loss budget, stop band, liquidity review, or event-risk checklist cannot be accepted before entry.

## Scenario Summary

- Scenario days: 6
- Ending ETP NAV: 100.608795
- ETP return: 0.6088%
- Underlying return: 0.4038%
- Path decay vs simple multiple: -0.602755

## Risk Budget And Bands

- Maximum loss budget: 750.0 USD
- Stop-loss band: 15.0%
- Take-profit band: 20.0%

### Band Events

- None in modeled path

## Assumptions

- Scenario path is deterministic fixture data, not a forecast.
- Modeled NAV starts at 100 and applies daily reset leverage once per scenario row.
- Fees are approximated as a constant daily deduction from leveraged daily return.
- Risk bands are evaluated on modeled end-of-day NAV values.
- The maximum loss budget is supplied by the user and is not a sizing recommendation.

## Checklist

- [ ] Confirm the product uses daily reset leverage and identify the stated leverage factor.
- [ ] Compare the planned holding period with the product objective and risk disclosures.
- [ ] Run at least one trending path and one choppy path before sizing the trade.
- [ ] Record stop-loss and take-profit levels before entry.
- [ ] Review borrowing, financing, and management-fee drag assumptions.
- [ ] Check whether the underlying has event risk, earnings, regulatory decisions, or macro releases.
- [ ] Document why the scenario does not rely on a simple leverage multiple over several days.
- [ ] Record maximum tolerable loss, concentration, and portfolio correlation.

## Warnings

- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.
- Large daily moves can compound quickly and may create losses larger than a simple one-day estimate.
- Fee drag is approximated as a constant daily deduction from the leveraged daily return.
- A pretrade plan does not confirm liquidity, execution quality, tax treatment, or suitability.
- Stop-loss and take-profit bands are planning levels, not guaranteed execution prices.

## Command Provenance

- checklist_profile: risk-review
- command: pretrade-plan
- initial_nav: 100.0
- max_loss_budget: 750.0
- path: examples/fixtures/nasdaq_chop_path.csv
- product: examples/fixtures/leveraged_nasdaq_3x.json
- stop_loss: 0.15
- take_profit: 0.2
- thesis_file: examples/fixtures/thesis_note.md
