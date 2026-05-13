# leveraged-etp-risk-lab

`leveraged-etp-risk-lab` is a zero-dependency Python CLI for planning daily-reset leveraged ETF/ETP risk scenarios. It models product terms, deterministic scenario paths, daily reset leverage, management-fee drag, path decay versus a simple multiple, stop-loss and take-profit bands, portfolio exposure aggregation, and plain-language warnings.

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
python -m leveraged_etp_risk_lab generate-scenario \
  --kind crash \
  --days 10 \
  --output crash_path.csv

python -m leveraged_etp_risk_lab exposure-report \
  --manifest examples/fixtures/portfolio_manifest.json \
  --format markdown

python -m leveraged_etp_risk_lab pretrade-plan \
  --product examples/fixtures/leveraged_nasdaq_3x.json \
  --path examples/fixtures/nasdaq_chop_path.csv \
  --thesis-file examples/fixtures/thesis_note.md \
  --max-loss-budget 750 \
  --stop-loss 0.15 \
  --take-profit 0.20 \
  --format markdown

python -m leveraged_etp_risk_lab static-dashboard \
  --manifest examples/fixtures/portfolio_manifest.json \
  --output examples/outputs/dashboard.html

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
- `portfolio_manifest.json`: two-position portfolio fixture for exposure aggregation.
- `thesis_note.md`: generic thesis note fixture for pretrade plan examples.

Generated path kinds are `trend`, `chop`, `crash`, and `rebound`. They are deterministic and use the same `day,label,underlying_return` CSV shape as checked-in path fixtures.

The `pretrade-plan` command combines product terms, a scenario path, optional thesis text, stop/take bands, a user-supplied maximum loss budget, assumptions, warnings, and a checklist into a Markdown or JSON decision packet. It always includes explicit not-investment-advice language.

The `static-dashboard` command writes a self-contained no-JavaScript HTML dashboard from either a portfolio manifest or demo output JSON files. It includes summary cards, positions, warnings, band events, and command provenance.

Deterministic sample outputs can be regenerated with:

```bash
python -m leveraged_etp_risk_lab demo-bundle --output-dir examples/outputs
```

## Data Schema

Schema notes live in `docs/schema.md`. Machine-readable draft schemas are provided in:

- `docs/product.schema.json`
- `docs/path.schema.json`
- `docs/portfolio-manifest.schema.json`
- `docs/simulation-output.schema.json`
- `docs/exposure-report.schema.json`
- `docs/pretrade-plan.schema.json`

## Roadmap

- Add richer position sizing helpers.
- Add more manifest-level concentration and correlation approximations.
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
