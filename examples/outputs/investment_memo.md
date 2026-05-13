# Investment Memo: NDAQ3X

**Not investment advice:** This investment memo packet is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## Thesis

# Example Thesis Note

The modeled trade is a short-horizon tactical scenario for a generic daily-reset leveraged ETP. The thesis assumes the reference index can recover after recent volatility, but recognizes that choppy paths can create decay even when the underlying ends near flat.

The plan should be rejected if the loss budget, stop band, liquidity review, or event-risk checklist cannot be accepted before entry.

## Product Terms

- Product: Generic 3x Nasdaq Daily Reset ETP
- Underlying: Nasdaq-100 reference index
- Daily leverage: 3.0x
- Reset frequency: daily
- Annual fee: 0.95%

## Scenario Evidence

- Days: 6
- ETP return: 0.6088%
- Underlying return: 0.4038%
- Path decay vs simple multiple: -0.602755
- Worst grid return: -48.8504%

## Risk Budget

- Maximum loss budget: 750.0 USD
- Recommended notional: 5000.0
- Modeled loss at stop: 750.0
- Stop-loss: 15.0%
- Take-profit: 20.0%

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

## Invalidation Triggers

- critical: return -48.8504%; worst drawdown -52.5497%; path decay 5.694511; band events: day 1 stop_loss at NAV 74.49623
- high: return -19.8516%; worst drawdown -19.8516%; path decay 1.136554; band events: day 8 stop_loss at NAV 84.483822
- medium: The modeled trade is a short-horizon tactical scenario for a generic daily-reset leveraged ETP. The thesis assumes the reference index can recover after recent volatility, but recognizes that choppy paths can create decay even when the underlying ends near flat.
- medium: The plan should be rejected if the loss budget, stop band, liquidity review, or event-risk checklist cannot be accepted before entry.
- medium: return -0.3186%; worst drawdown -6.5029%; path decay -1.429133
- high: Worst grid return is -48.8504% in gap_down.
- medium: Report card is not decision-ready.

## Warnings

- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.
- Large daily moves can compound quickly and may create losses larger than a simple one-day estimate.
- Fee drag is approximated as a constant daily deduction from the leveraged daily return.
- A pretrade plan does not confirm liquidity, execution quality, tax treatment, or suitability.
- Stop-loss and take-profit bands are planning levels, not guaranteed execution prices.
- Recommended notional is a deterministic planning output, not a trade recommendation.
- Share count is a placeholder because no live or execution price is modeled.
- Stop-loss levels are planning inputs and do not guarantee execution at the modeled loss.
- trend_up has 4 modeled warning(s).
- Sensitivity rows summarize deterministic built-in regimes and do not model execution, liquidity, tax, or suitability.

## Provenance

- artifacts: ['examples/outputs/recipe_run.json', 'examples/outputs/thesis_dashboard_data.json', 'examples/outputs/report_card.json', 'examples/outputs/factsheet_check.json']
- command: memo-draft
- live_market_data: False
- shell_out: False
