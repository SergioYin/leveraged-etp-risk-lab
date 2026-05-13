# Simulation: STK2X

- Product: Generic 2x Single-Stock Daily Reset ETP
- Underlying: Single-stock reference share
- Leverage: 2.0x daily reset
- Annual fee: 1.15%
- Ending ETP NAV: 85.245314
- ETP return: -14.7547%
- Underlying return: -7.0506%
- Simple multiple return: -14.1012%
- Path decay vs simple multiple: -0.653442

## Band Events

- None

## Path

| day | label | underlying_return_pct | underlying_index | daily_levered_return_pct | etp_nav | simple_multiple_nav | path_decay |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Earnings gap | -8.5 | 91.5 | -17.0046 | 82.995437 | 83.0 | -0.004563 |
| 2 | Follow-through selloff | -3.2 | 88.572 | -6.4046 | 77.679941 | 77.144 | 0.535941 |
| 3 | Short-cover bounce | 4.1 | 92.203452 | 8.1954 | 84.046151 | 84.406904 | -0.360753 |
| 4 | Analyst downgrade | -2.6 | 89.806162 | -5.2046 | 79.671916 | 79.612324 | 0.059592 |
| 5 | Partial recovery | 3.5 | 92.949378 | 6.9954 | 85.245314 | 85.898756 | -0.653442 |

## Warnings

- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.
- Large daily moves can compound quickly and may create losses larger than a simple one-day estimate.
- Fee drag is approximated as a constant daily deduction from the leveraged daily return.
