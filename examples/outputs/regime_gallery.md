# Market Regime Gallery

- Schema version: 0.7
- Regimes: 6

## trend_up

- Name: Trend Up
- Description: Orderly rising market with shallow pauses and positive drift.
- Default days: 12
- Tags: trend, bullish, low_chop

### Sample Path

| day | label | underlying_return |
| --- | --- | --- |
| 1 | Opening bid | 0.006 |
| 2 | Orderly advance | 0.008 |
| 3 | Shallow pause | -0.002 |
| 4 | Breakout follow-through | 0.011 |
| 5 | Consolidation | 0.001 |
| 6 | Momentum close | 0.007 |

### Risk Notes

- Leveraged long products may compound favorably, but late pullbacks can erase gains quickly.
- Inverse products can lose value steadily even without a single large up day.

### Use Cases

- Testing positive compounding in a persistent advance.
- Comparing stop and take-profit bands after a favorable start.

## trend_down

- Name: Trend Down
- Description: Persistent selloff with brief relief rallies that fail.
- Default days: 12
- Tags: trend, bearish, drawdown

### Sample Path

| day | label | underlying_return |
| --- | --- | --- |
| 1 | Risk-off open | -0.007 |
| 2 | Follow-through selling | -0.012 |
| 3 | Weak relief | 0.004 |
| 4 | Lower low | -0.015 |
| 5 | Failed bounce | 0.003 |
| 6 | De-risking close | -0.009 |

### Risk Notes

- Long leveraged products can compound losses faster than a simple multiple suggests.
- Brief relief rallies can materially hurt inverse daily reset exposure sizing.

### Use Cases

- Stress testing long leveraged drawdown paths.
- Reviewing inverse product behavior during failed bounces.

## chop

- Name: Chop
- Description: Alternating up and down sessions with limited net direction.
- Default days: 12
- Tags: sideways, volatility_decay, mean_reversion

### Sample Path

| day | label | underlying_return |
| --- | --- | --- |
| 1 | Risk-on swing | 0.022 |
| 2 | Risk-off swing | -0.021 |
| 3 | Relief bid | 0.018 |
| 4 | Fade | -0.017 |

### Risk Notes

- Alternating returns can create path decay even when the underlying ends near flat.
- Stop and take-profit bands may trigger repeatedly in both directions.

### Use Cases

- Demonstrating volatility decay from daily reset leverage.
- Comparing trend assumptions against sideways whipsaw conditions.

## gap_down

- Name: Gap Down
- Description: Large downside gap followed by unstable trading and a partial attempt to stabilize.
- Default days: 8
- Tags: gap, event_risk, single_stock

### Sample Path

| day | label | underlying_return |
| --- | --- | --- |
| 1 | Event gap lower | -0.085 |
| 2 | Forced selling | -0.032 |
| 3 | Volatile bounce | 0.026 |
| 4 | Second wave | -0.021 |
| 5 | Stabilization attempt | 0.012 |

### Risk Notes

- Gap moves can bypass planning bands and create modeled losses before any exit is possible.
- Single-name event risk can dominate management-fee or ordinary volatility assumptions.

### Use Cases

- Single-stock earnings or regulatory event stress tests.
- Checking whether a loss budget survives a discontinuous first move.

## rebound

- Name: Rebound
- Description: Initial drawdown followed by stabilization and a sharp recovery attempt.
- Default days: 10
- Tags: reversal, recovery, short_covering

### Sample Path

| day | label | underlying_return |
| --- | --- | --- |
| 1 | Capitulation | -0.032 |
| 2 | Base building | -0.011 |
| 3 | Stabilization | 0.009 |
| 4 | Short-cover rally | 0.027 |
| 5 | Follow-through | 0.019 |

### Risk Notes

- Losses early in the path reduce the NAV base that participates in a later rebound.
- Inverse products can give back gains quickly if the recovery accelerates.

### Use Cases

- Testing whether a leveraged position can recover after an early stop zone.
- Reviewing inverse hedge exit rules after an initial selloff.

## volatility_cluster

- Name: Volatility Cluster
- Description: Sequence of large moves in both directions, modeling clustered high volatility.
- Default days: 12
- Tags: high_volatility, cluster, stress

### Sample Path

| day | label | underlying_return |
| --- | --- | --- |
| 1 | Volatility shock | -0.041 |
| 2 | Sharp relief | 0.036 |
| 3 | Renewed pressure | -0.029 |
| 4 | Fast squeeze | 0.033 |
| 5 | Liquidity fade | -0.024 |
| 6 | Wide-range close | 0.018 |

### Risk Notes

- Large alternating moves can produce material decay even if the final underlying move is modest.
- Modeled NAV can become highly sensitive to the order of daily returns.

### Use Cases

- Stress testing path dependence during high-volatility regimes.
- Comparing risk bands under clustered large-move conditions.

