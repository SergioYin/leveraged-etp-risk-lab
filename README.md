# leveraged-etp-risk-lab

`leveraged-etp-risk-lab` is a zero-dependency Python CLI for planning daily-reset leveraged ETF/ETP risk scenarios. It models product terms, daily reset leverage, management-fee drag, path decay versus a simple multiple, stop-loss and take-profit bands, and plain-language warnings.

This is not investment advice. The tool is for scenario analysis and education only; it does not forecast prices, recommend trades, or evaluate suitability.

## Install

Run from a checkout:

```bash
python -m leveraged_etp_risk_lab --help
```

Optional editable install:

```bash
python -m pip install -e .
leveraged-etp-risk-lab --help
```

## Commands

```bash
python -m leveraged_etp_risk_lab simulate \
  --product examples/fixtures/leveraged_nasdaq_3x.json \
  --path examples/fixtures/nasdaq_chop_path.csv \
  --format markdown
```

```bash
python -m leveraged_etp_risk_lab checklist --profile active-trader
python -m leveraged_etp_risk_lab demo-bundle --output-dir demo-output
python -m leveraged_etp_risk_lab selfcheck
python -m leveraged_etp_risk_lab version-report
```

## Examples

Fixtures are in `examples/fixtures/`:

- `leveraged_nasdaq_3x.json`: a generic 3x Nasdaq-linked ETP example.
- `single_stock_2x.json`: a generic 2x single-stock ETP example.
- `nasdaq_chop_path.csv`: alternating up/down path that shows volatility decay.
- `single_stock_gap_path.csv`: path with a gap and partial recovery.

Deterministic sample outputs can be regenerated with:

```bash
python -m leveraged_etp_risk_lab demo-bundle --output-dir examples/outputs
```

## Data Schema

Schema notes live in `docs/schema.md`. Machine-readable draft schemas are provided in:

- `docs/product.schema.json`
- `docs/path.schema.json`
- `docs/simulation-output.schema.json`

## Roadmap

- Add richer position sizing helpers.
- Add additional deterministic scenario generators.
- Support portfolio-level aggregation across several leveraged ETPs.
- Add optional plotting through an extra package while keeping the core CLI dependency-free.

## Development

Run tests:

```bash
python -m unittest discover -s tests
```

Run repository validation:

```bash
python scripts/selfcheck.py
```

## License

MIT. See `LICENSE`.
