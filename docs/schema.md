# Data Schema

Schemas are versioned as `0.2` and are intentionally small enough to edit by hand.

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

The `generate-scenario` command writes deterministic CSV paths in this shape for `trend`, `chop`, `crash`, and `rebound` scenarios.

## Portfolio Manifest

Portfolio manifest files are JSON objects with:

- `name`: display name.
- `base_currency`: optional, defaults to `USD`.
- `positions`: non-empty list of position objects.

Each position contains:

- `id`: optional position identifier.
- `product_fixture`: product JSON path. Relative paths are resolved from the manifest directory first.
- `path_fixture`: path CSV path. Relative paths are resolved from the manifest directory first.
- `notional`: positive starting notional value.
- `stop_loss`: optional decimal stop-loss band.
- `take_profit`: optional decimal take-profit band.

The aliases `product` and `path` are accepted for `product_fixture` and `path_fixture`.

## Simulation Output

Simulation output contains:

- `product`: normalized product terms.
- `inputs`: initial NAV, day count, and risk bands.
- `summary`: ending values, returns, path decay, and estimated fee drag.
- `band_events`: first stop-loss or take-profit events as modeled NAV crosses bands.
- `warnings`: deterministic risk warnings.
- `path`: per-day modeled values.

## Exposure Report Output

Exposure reports contain:

- `portfolio`: manifest name and base currency.
- `summary`: starting value, aggregate ending value, portfolio return, starting-notional weighted exposure, and worst drawdown approximation.
- `positions`: per-position notional, leverage, weighted exposure, ending value, return, risk bands, and value path.
- `portfolio_path`: aggregate modeled daily portfolio value.
- `stop_events`: stop-loss and take-profit events with position identifiers.
- `warnings`: portfolio-level and deduplicated simulation warnings.
