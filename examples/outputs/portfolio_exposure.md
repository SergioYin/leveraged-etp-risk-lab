# Exposure Report: Generic Leveraged ETP Portfolio

- Base currency: USD
- Starting value: 10000.0
- Ending value: 9446.34026
- Return: -5.5366%
- Weighted exposure: 2.6x
- Worst drawdown approximation: -8.6896%

## Positions

| id | ticker | notional | notional_weight_pct | leverage | weighted_exposure | ending_value | return_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nasdaq_tactical | NDAQ3X | 6000.0 | 60.0 | 3.0 | 1.8 | 6036.5277 | 0.6088 |
| single_stock_satellite | STK2X | 4000.0 | 40.0 | 2.0 | 0.8 | 3409.81256 | -14.7547 |

## Stop Events

- single_stock_satellite (STK2X), day 2 (Follow-through selloff): stop_loss at NAV 77.679941

## Portfolio Path

| day | value |
| --- | --- |
| 1 | 9769.59128 |
| 2 | 9131.04326 |
| 3 | 9710.75222 |
| 4 | 9211.74922 |
| 5 | 9633.27884 |
| 6 | 9446.34026 |

## Warnings

- Portfolio aggregation is scenario-based and does not model tax, borrow, spread, liquidity, or intraday stop execution.
- Weighted exposure uses starting notional weights and product daily leverage factors.
- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.
- Large daily moves can compound quickly and may create losses larger than a simple one-day estimate.
- Fee drag is approximated as a constant daily deduction from the leveraged daily return.
