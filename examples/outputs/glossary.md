# Leveraged Product Glossary

**Not investment advice:** This glossary is for leveraged product education and scenario planning only. It is not investment advice, a recommendation, or a suitability determination.

- Schema version: 0.14
- Terms: 10

## daily_reset

- Term: Daily reset
- Plain language: A daily-reset product targets its stated leverage for one trading day at a time, then resets exposure for the next day.
- Why it matters: Multi-day returns compound from the sequence of daily moves, so they can differ from a simple multiple of the underlying's total return.
- Example: A 3x product that gains 3% on day one does not keep the same dollar exposure on day two; the next day's target is reset from the new NAV.
- Related terms: leverage_factor, path_decay, volatility_decay

## path_decay

- Term: Path decay
- Plain language: Path decay is the difference between a leveraged product's compounded path return and a simple leverage multiple of the underlying's start-to-end return.
- Why it matters: It highlights that order, reversals, and compounding can dominate the headline leverage factor over more than one day.
- Example: A choppy underlying path can finish close to flat while a daily-reset leveraged product loses value because gains and losses compound from changing bases.
- Related terms: daily_reset, volatility_decay, leverage_factor

## volatility_decay

- Term: Volatility decay
- Plain language: Volatility decay is the drag that can appear when alternating up and down moves compound in a daily-reset leveraged product.
- Why it matters: Higher leverage and larger daily swings can make the drag more visible, especially in sideways or mean-reverting markets.
- Example: After a -5% underlying day followed by a +5% day, the underlying is not fully back to even; a leveraged product magnifies that compounding effect.
- Related terms: path_decay, daily_reset, leverage_factor

## leverage_factor

- Term: Leverage factor
- Plain language: The leverage factor is the stated daily exposure target, such as 2x, 3x, or -2x for inverse exposure.
- Why it matters: It scales daily underlying moves before fees and compounding, but it is not a guarantee of the same multiple over longer holding periods.
- Example: If the underlying rises 1% in one day, a 3x daily product targets roughly +3% before fees and tracking differences.
- Related terms: daily_reset, path_decay, gap_risk

## stop_loss_band

- Term: Stop-loss band
- Plain language: A stop-loss band is a planning threshold for reviewing or exiting a position after modeled losses.
- Why it matters: It helps translate risk tolerance into a preplanned level, but actual execution can differ in fast or gapping markets.
- Example: A 15% stop-loss band on a 100 NAV scenario flags review if modeled NAV reaches 85 or lower.
- Related terms: take_profit_band, gap_risk, max_loss_budget

## take_profit_band

- Term: Take-profit band
- Plain language: A take-profit band is a planning threshold for reviewing gains or reducing exposure after a modeled favorable move.
- Why it matters: It supports disciplined scenario planning, but it does not predict where liquidity or execution will be available.
- Example: A 20% take-profit band on a 100 NAV scenario flags review if modeled NAV reaches 120 or higher.
- Related terms: stop_loss_band, premium_discount, iNAV

## gap_risk

- Term: Gap risk
- Plain language: Gap risk is the risk that a product or its underlying opens sharply away from the prior price, skipping over planned review levels.
- Why it matters: Stop-loss bands and sizing assumptions may not cap losses if prices move discontinuously or liquidity is thin.
- Example: A product may move from above a stop-loss band to well below it between sessions after an earnings, macro, or regulatory event.
- Related terms: stop_loss_band, max_loss_budget, leverage_factor

## iNAV

- Term: Indicative NAV (iNAV)
- Plain language: Indicative NAV is an intraday estimate of a fund's net asset value based on available underlying market data.
- Why it matters: It can help compare market price with estimated portfolio value, while still being an estimate that may lag or be less reliable in stressed markets.
- Example: If market price is above iNAV, the product may be trading at a premium to the estimated value of its holdings.
- Related terms: premium_discount, take_profit_band, gap_risk

## premium_discount

- Term: Premium/discount
- Plain language: Premium or discount compares a product's market price with its NAV or indicative NAV.
- Why it matters: Large differences can signal trading friction, stale estimates, stressed liquidity, or creation and redemption constraints.
- Example: A product trading at 101 when estimated NAV is 100 is trading at about a 1% premium.
- Related terms: iNAV, gap_risk, take_profit_band

## max_loss_budget

- Term: Maximum loss budget
- Plain language: A maximum loss budget is the amount of account value a user decides to put at risk in a scenario plan.
- Why it matters: It connects position size, stop-loss assumptions, and portfolio concentration in one explicit planning constraint.
- Example: With a 750 currency-unit loss budget and a 15% modeled stop, the corresponding notional basis is 5,000 before considering execution and gap risk.
- Related terms: stop_loss_band, gap_risk, leverage_factor

