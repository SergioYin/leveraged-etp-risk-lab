# Product Template Gallery

- Schema version: 0.4
- Templates: 4

## generic-2x-long-equity

- Name: Generic 2x Long Equity Daily Reset ETP
- Ticker: EQTY2X
- Underlying: Broad equity reference basket
- Leverage: 2x daily reset
- Annual fee: 0.95%
- Currency: USD

### Risk Notes

- Daily 2x compounding can diverge from twice the multi-day underlying return.
- Equity drawdowns can compound quickly when exposure is reset each day.
- Fee drag, spreads, liquidity, taxes, and tracking error are not modeled in the product file.

### Use Cases

- Broad-market bullish scenario planning.
- Comparing trend and chop paths before sizing a short holding-period trade.
- Educational examples where a moderate long leverage factor is needed.

## generic-3x-long-index

- Name: Generic 3x Long Index Daily Reset ETP
- Ticker: IDX3X
- Underlying: Large-cap equity index reference
- Leverage: 3x daily reset
- Annual fee: 0.95%
- Currency: USD

### Risk Notes

- 3x exposure magnifies daily gains and losses and can produce large path-dependent decay.
- A one-day index loss near one third can drive modeled NAV toward zero before safeguards.
- Best modeled with explicit stop-loss and take-profit bands because losses accelerate.

### Use Cases

- High-conviction index trend stress tests.
- Volatility decay demonstrations in alternating up/down paths.
- Portfolio exposure aggregation with a high-beta long position.

## generic--2x-inverse-index

- Name: Generic -2x Inverse Index Daily Reset ETP
- Ticker: INV2X
- Underlying: Large-cap equity index reference
- Leverage: -2x daily reset
- Annual fee: 1.05%
- Currency: USD

### Risk Notes

- Inverse daily reset products can lose value in rising markets and in volatile sideways markets.
- Multi-day inverse returns are path dependent and should not be treated as a simple hedge ratio.
- Short-lived hedging assumptions can fail if the underlying rebounds sharply.

### Use Cases

- Generic bearish index scenario planning.
- Hedge-ratio education for daily reset inverse exposure.
- Stress testing rebound risk after a market selloff.

## generic-2x-single-stock

- Name: Generic 2x Single-Stock Daily Reset ETP
- Ticker: STK2X
- Underlying: Single-stock reference share
- Leverage: 2x daily reset
- Annual fee: 1.15%
- Currency: USD

### Risk Notes

- Single-stock gaps, earnings, halts, and idiosyncratic news can dominate modeled daily paths.
- 2x daily reset exposure can compound losses rapidly when the reference share gaps lower.
- Scenario output does not model issuer call features, liquidity, spreads, taxes, or suitability.

### Use Cases

- Single-name event-risk stress testing.
- Gap-down and partial-recovery path examples.
- Educational comparison against broad-index leveraged products.

