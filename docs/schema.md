# Data Schema

All schemas are versioned as `0.1` and are intentionally small enough to edit by hand.

## Product

Product files are JSON objects with these fields:

- `name`: display name.
- `ticker`: generic or listed ticker label.
- `underlying`: underlying reference asset.
- `leverage`: daily leverage factor, such as `3` or `2`.
- `annual_fee`: decimal annual fee, such as `0.0095` for 0.95%.
- `currency`: optional, defaults to `USD`.
- `reset_frequency`: optional, defaults to `daily`.
- `notes`: optional plain-text notes.

## Path

Path files are CSV files with:

- `day`: integer day number.
- `label`: scenario label.
- `underlying_return`: decimal daily return, such as `-0.025` for -2.5%.

## Simulation Output

Simulation output contains:

- `product`: normalized product terms.
- `inputs`: initial NAV, day count, and risk bands.
- `summary`: ending values, returns, path decay, and estimated fee drag.
- `band_events`: first stop-loss or take-profit events as modeled NAV crosses bands.
- `warnings`: deterministic risk warnings.
- `path`: per-day modeled values.
