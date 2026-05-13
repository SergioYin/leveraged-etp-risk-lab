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

python -m leveraged_etp_risk_lab position-size \
  --pretrade-plan examples/outputs/pretrade_plan.json \
  --account-value 50000 \
  --risk-budget-pct 0.015 \
  --format markdown

python -m leveraged_etp_risk_lab stress-matrix \
  --product examples/fixtures/leveraged_nasdaq_3x.json \
  --stop-loss 0.15 \
  --take-profit 0.20 \
  --format markdown

python -m leveraged_etp_risk_lab compare-runs \
  --base examples/outputs/leveraged_nasdaq_3x.json \
  --candidate examples/outputs/single_stock_2x.json \
  --format markdown

python -m leveraged_etp_risk_lab run-ledger \
  --ledger run_ledger.jsonl \
  --artifact examples/outputs/leveraged_nasdaq_3x.json \
  --artifact examples/outputs/pretrade_plan.json

python -m leveraged_etp_risk_lab thesis-impact \
  --thesis-file examples/fixtures/thesis_note.md \
  --artifact examples/outputs/pretrade_plan.json \
  --artifact examples/outputs/portfolio_exposure.json \
  --format markdown

python -m leveraged_etp_risk_lab watchlist-build \
  --thesis-impact examples/outputs/thesis_impact.json \
  --stress-matrix examples/outputs/stress_matrix.json \
  --format markdown

python -m leveraged_etp_risk_lab factsheet-check \
  --product examples/fixtures/leveraged_nasdaq_3x.json \
  --factsheet-file examples/fixtures/factsheet_note.txt \
  --format markdown

python -m leveraged_etp_risk_lab demo-story \
  --input-dir examples/outputs \
  --format markdown

python -m leveraged_etp_risk_lab gallery-index \
  --input-dir examples/outputs \
  --format markdown

python -m leveraged_etp_risk_lab static-dashboard \
  --manifest examples/fixtures/portfolio_manifest.json \
  --output examples/outputs/dashboard.html

python -m leveraged_etp_risk_lab template-list --format markdown
python -m leveraged_etp_risk_lab template-export \
  --template generic-3x-long-index \
  --output generic_index_3x.json

python -m leveraged_etp_risk_lab regime-list --format markdown
python -m leveraged_etp_risk_lab regime-export \
  --regime volatility_cluster \
  --days 12 \
  --output volatility_cluster_path.csv

python -m leveraged_etp_risk_lab explain-term daily_reset --format markdown
python -m leveraged_etp_risk_lab glossary-list --format markdown

python -m leveraged_etp_risk_lab checklist --profile active-trader
python -m leveraged_etp_risk_lab demo-bundle --output-dir demo-output
python -m leveraged_etp_risk_lab package-audit --format markdown
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
- `factsheet_note.txt`: generic plain-text factsheet note for product checklist examples.

Generated path kinds are `trend`, `chop`, `crash`, and `rebound`. They are deterministic and use the same `day,label,underlying_return` CSV shape as checked-in path fixtures.

The `regime-list` command prints the built-in market regime gallery as JSON or Markdown. The gallery includes `trend_up`, `trend_down`, `chop`, `gap_down`, `rebound`, and `volatility_cluster`, with metadata, sample path rows, risk notes, and use cases. The `regime-export` command writes a selected regime to CSV in the same path format used by `simulate`.

The `pretrade-plan` command combines product terms, a scenario path, optional thesis text, stop/take bands, a user-supplied maximum loss budget, assumptions, warnings, and a checklist into a Markdown or JSON decision packet. It always includes explicit not-investment-advice language.

The `position-size` command reads either `--product` plus `--path`, or a generated `--pretrade-plan` JSON file. It sizes recommended notional from `--account-value` and exactly one of `--risk-budget-pct` or `--max-loss-budget`, carries an optional `--stop-loss`, emits a max-shares placeholder instead of fetching prices, and includes explicit not-investment-advice language.

The `stress-matrix` command reads a product JSON file and runs it across every built-in market regime, or only repeated `--regime` selections. It emits JSON or Markdown rows for modeled return, path decay versus a simple multiple, worst drawdown, stop/take event counts, and warning counts.

The `compare-runs` command reads two simulation, pretrade-plan, or exposure-report JSON outputs and emits deterministic JSON or Markdown deltas for return, path decay versus a simple multiple, weighted exposure, and warnings added or removed.

The `run-ledger` command appends JSONL metadata rows for generated artifacts. Rows include only deterministic metadata such as artifact filename, detected output type, schema version, byte count, and SHA-256 digest; artifact contents, secrets, timestamps, and machine-local absolute paths are not written.

The `thesis-impact` command reads a Markdown thesis file plus one or more generated JSON artifacts and maps extracted claims to observed return, path-decay, and exposure metrics where available. It also carries through relevant warnings and emits an action checklist for follow-up review.

The `watchlist-build` command reads a thesis-impact JSON artifact and a stress-matrix JSON artifact, then emits a deterministic watchlist ledger of thesis claims and regime triggers. Each entry includes severity, status, trigger text, next review questions, and source artifact references.

The `factsheet-check` command reads a product JSON file and an optional plain-text factsheet note. It emits JSON or Markdown checks for issuer, exchange, underlying, leverage factor, daily reset wording, fee, currency, liquidity/spread review placeholder, iNAV, premium/discount, and missing fields. It does not fetch live market data and includes explicit not-investment-advice language.

The `demo-story` command reads existing public demo outputs from an input directory: `stress_matrix.json`, `watchlist.json`, `package_audit.json`, and `pretrade_plan.json`. It emits a concise JSON or Markdown walkthrough with problem, workflow, commands, key outputs, safety caveats, and next extension ideas.

The `gallery-index` command reads the public demo output directory and emits a self-contained JSON or Markdown index grouped by workflow stage: fixtures, plans, sizing, stress, thesis/watchlist, audit/story, and dashboard. Each artifact row includes filename, format, detected document type and schema version when available, byte count, and a suggested next command. It records metadata only and skips the generated `gallery_index.*` files for deterministic regeneration.

The `static-dashboard` command writes a self-contained no-JavaScript HTML dashboard from either a portfolio manifest or demo output JSON files. It includes summary cards, positions, warnings, band events, and command provenance.

The `template-list` command prints the built-in product template gallery as JSON or Markdown. The gallery includes generic templates for 2x long equity, 3x long index, -2x inverse index, and 2x single-stock products, with leverage, risk notes, and use cases. The `template-export` command writes the selected template as product JSON that can be passed to `simulate` or `pretrade-plan`.

The `explain-term` command explains one built-in leveraged product glossary term in JSON or Markdown. Built-in term ids are `daily_reset`, `path_decay`, `volatility_decay`, `leverage_factor`, `stop_loss_band`, `take_profit_band`, `gap_risk`, `iNAV`, `premium_discount`, and `max_loss_budget`. Explanations are educational and include explicit not-investment-advice language.

The `glossary-list` command emits the full built-in glossary as JSON or Markdown. It is deterministic and does not read live market data, workflow files, private context, environment variables, or command history.

The `package-audit` command emits a deterministic JSON or Markdown package-readiness checklist. It checks README and license presence, schema and example outputs, the checked-in agent skill file, absence of workflow files, public hygiene, zero dependencies, version consistency, and listed test commands. Pass `--run-tests` to execute the listed validation commands during the audit.

The local skill sync helper copies the checked-in skill file into a local Codex skills directory:

```bash
python scripts/sync_local_skill.py
```

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
- `docs/position-size.schema.json`
- `docs/stress-matrix.schema.json`
- `docs/template-gallery.schema.json`
- `docs/regime-gallery.schema.json`
- `docs/compare-runs.schema.json`
- `docs/run-ledger.schema.json`
- `docs/thesis-impact.schema.json`
- `docs/watchlist.schema.json`
- `docs/factsheet-check.schema.json`
- `docs/package-audit.schema.json`
- `docs/glossary.schema.json`
- `docs/demo-story.schema.json`
- `docs/gallery-index.schema.json`

## Roadmap

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

Run the package readiness audit:

```bash
python -m leveraged_etp_risk_lab package-audit --format markdown
```

## License

MIT. See `LICENSE`.
