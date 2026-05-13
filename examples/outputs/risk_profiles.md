# Risk Rule Profiles

**Not investment advice:** These profile rules are for scenario planning and education only. They are not investment advice, recommendations, or suitability determinations.

## Default (default)

Baseline review rules for generic daily-reset leveraged ETP scenario planning.

- Max holding days: 5
- Max account risk pct placeholder: Set a user-defined account risk cap before sizing; no default is implied.

### Required Factsheet Fields

- issuer
- exchange
- underlying
- leverage_factor
- daily_reset
- annual_fee
- currency
- liquidity_spread
- inav
- premium_discount

### Required Scenario Regimes

- trend_up
- trend_down
- chop
- gap_down

### Mandatory Checklist Questions

- [ ] Have product objective, leverage factor, reset frequency, fees, and currency been verified?
- [ ] Does the planned holding period fit the product objective and modeled path risk?
- [ ] Has the scenario been tested against both trending and choppy paths?
- [ ] Are stop-loss and take-profit review levels recorded before entry?
- [ ] Is the maximum tolerable loss documented outside the model output?

### Stop/Take Review Defaults

- Stop-loss review: 15.0%
- Take-profit review: 20.0%
- Review frequency: daily close
- Gap review: Review immediately after an overnight gap or modeled stop breach.

## Conservative (conservative)

Tighter holding-period and review rules for lower tolerance planning.

- Max holding days: 2
- Max account risk pct placeholder: Use a smaller user-defined account risk cap; this package does not set suitability limits.

### Required Factsheet Fields

- issuer
- exchange
- underlying
- leverage_factor
- daily_reset
- annual_fee
- currency
- liquidity_spread
- inav
- premium_discount

### Required Scenario Regimes

- trend_down
- chop
- gap_down
- volatility_cluster

### Mandatory Checklist Questions

- [ ] Is there a documented reason to use a leveraged product instead of lower-leverage exposure?
- [ ] Can the position be exited if spreads widen or the product trades at a premium/discount?
- [ ] Does the modeled loss remain tolerable after applying gap-risk judgment outside this tool?
- [ ] Have concentration and correlated portfolio exposure been reviewed?
- [ ] Is there a same-day review trigger for adverse movement?

### Stop/Take Review Defaults

- Stop-loss review: 8.0%
- Take-profit review: 12.0%
- Review frequency: same day and daily close
- Gap review: Review before adding exposure after any gap-down or volatility-cluster regime result.

## Active Trader (active-trader)

Intraday-oriented review rules for short planned holding periods and fast exits.

- Max holding days: 1
- Max account risk pct placeholder: Set per-trade and per-day account risk caps outside this package before using the profile.

### Required Factsheet Fields

- issuer
- exchange
- underlying
- leverage_factor
- daily_reset
- annual_fee
- currency
- liquidity_spread
- inav
- premium_discount

### Required Scenario Regimes

- trend_up
- trend_down
- gap_down
- rebound
- volatility_cluster

### Mandatory Checklist Questions

- [ ] Are entry, exit, stop, and take-profit review levels defined before the trade?
- [ ] Have intraday liquidity, spreads, halt risk, and closing-auction exposure been reviewed?
- [ ] Is there a rule for not averaging down after a stop breach?
- [ ] Does the product have event risk during the intended trading window?
- [ ] Has position size been checked against both stop loss and worst modeled regime loss?

### Stop/Take Review Defaults

- Stop-loss review: 5.0%
- Take-profit review: 10.0%
- Review frequency: intraday and daily close
- Gap review: Review immediately after market open gaps, halts, or fast spread widening.

## Thesis Review (thesis-review)

Rules for linking a written thesis to factsheet checks, stress regimes, and review questions.

- Max holding days: 10
- Max account risk pct placeholder: Document a thesis-specific account risk cap before sizing; leave unset if no cap is approved.

### Required Factsheet Fields

- issuer
- exchange
- underlying
- leverage_factor
- daily_reset
- annual_fee
- currency
- liquidity_spread
- inav
- premium_discount

### Required Scenario Regimes

- trend_up
- trend_down
- chop
- gap_down
- rebound
- volatility_cluster

### Mandatory Checklist Questions

- [ ] What specific thesis claim would invalidate the trade or require size reduction?
- [ ] Which factsheet fields or product terms are critical to the thesis?
- [ ] Which stress-matrix regime most directly challenges the thesis?
- [ ] What metric, warning, or watchlist entry triggers the next review?
- [ ] Has the thesis been updated after modeled path decay, drawdown, and stop/take events?

### Stop/Take Review Defaults

- Stop-loss review: 12.0%
- Take-profit review: 18.0%
- Review frequency: daily close and thesis event
- Gap review: Review thesis language after any gap, rebound failure, or volatility-cluster result.

## Provenance

- command: risk-profile
- profile: all
