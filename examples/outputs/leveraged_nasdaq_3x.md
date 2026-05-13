# Simulation: NDAQ3X

- Product: Generic 3x Nasdaq Daily Reset ETP
- Underlying: Nasdaq-100 reference index
- Leverage: 3.0x daily reset
- Annual fee: 0.95%
- Ending ETP NAV: 100.608795
- ETP return: 0.6088%
- Underlying return: 0.4038%
- Simple multiple return: 1.2115%
- Path decay vs simple multiple: -0.602755

## Band Events

- None

## Path

| day | label | underlying_return_pct | underlying_index | daily_levered_return_pct | etp_nav | simple_multiple_nav | path_decay |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Up impulse | 2.5 | 102.5 | 7.4962 | 107.49623 | 107.5 | -0.00377 |
| 2 | Sharp giveback | -2.2 | 100.245 | -6.6038 | 100.397427 | 100.735 | -0.337573 |
| 3 | Relief bounce | 1.8 | 102.04941 | 5.3962 | 105.815103 | 106.14823 | -0.333127 |
| 4 | Distribution day | -1.7 | 100.31457 | -5.1038 | 100.414543 | 100.94371 | -0.529167 |
| 5 | Small rally | 1.1 | 101.41803 | 3.2962 | 103.724438 | 104.254091 | -0.529653 |
| 6 | Fade | -1.0 | 100.40385 | -3.0038 | 100.608795 | 101.21155 | -0.602755 |

## Warnings

- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.
- Large daily moves can compound quickly and may create losses larger than a simple one-day estimate.
- Fee drag is approximated as a constant daily deduction from the leveraged daily return.
