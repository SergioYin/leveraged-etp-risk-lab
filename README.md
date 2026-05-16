# leveraged-etp-risk-lab

`leveraged-etp-risk-lab` is a zero-dependency Python CLI for planning daily-reset leveraged ETF/ETP risk scenarios. It models product terms, deterministic scenario paths, daily reset leverage, management-fee drag, path decay versus a simple multiple, stop-loss and take-profit bands, portfolio exposure aggregation, and plain-language warnings.

This is not investment advice. The tool is for scenario analysis and education only; it does not forecast prices, recommend trades, or evaluate suitability.

Public integration notes are included in the generated scenario pack. They explain how `scenario_pack.*` and case-study outputs can sit beside generic tools such as `portfolio-risk-compass` and `invest-thesis-ledger` as static reference artifacts, without imports, APIs, shared storage, workflow reads, live data, broker access, or private context.

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

python -m leveraged_etp_risk_lab sensitivity-grid \
  --product examples/fixtures/leveraged_nasdaq_3x.json \
  --stop-loss none,0.15,0.25 \
  --take-profit none,0.20,0.35 \
  --format markdown

python -m leveraged_etp_risk_lab portfolio-sensitivity \
  --manifest examples/fixtures/portfolio_manifest.json \
  --stop-loss none,0.15,0.25 \
  --take-profit none,0.20,0.35 \
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

python -m leveraged_etp_risk_lab risk-profile \
  --profile thesis-review \
  --format markdown

python -m leveraged_etp_risk_lab recipe-run \
  --recipe examples/fixtures/recipe_thesis_review.json \
  --format markdown

python -m leveraged_etp_risk_lab report-card \
  --artifact examples/outputs/pretrade_plan.json \
  --artifact examples/outputs/position_size.json \
  --artifact examples/outputs/stress_matrix.json \
  --artifact examples/outputs/factsheet_check.json \
  --format markdown

python -m leveraged_etp_risk_lab thesis-dashboard-data \
  --recipe-run examples/outputs/recipe_run.json \
  --report-card examples/outputs/report_card.json \
  --watchlist examples/outputs/watchlist.json \
  --sensitivity-grid examples/outputs/sensitivity_grid.json \
  --format markdown

python -m leveraged_etp_risk_lab audit-trail \
  --ledger examples/outputs/run_ledger.jsonl \
  --artifact examples/outputs/pretrade_plan.json \
  --artifact examples/outputs/stress_matrix.json \
  --format markdown

python -m leveraged_etp_risk_lab schema-inventory \
  --format markdown

python -m leveraged_etp_risk_lab artifact-validate \
  --format markdown

python -m leveraged_etp_risk_lab cycle-init \
  --memo examples/outputs/investment_memo.json \
  --watchlist examples/outputs/watchlist.json \
  --report-card examples/outputs/report_card.json \
  --sensitivity-grid examples/outputs/sensitivity_grid.json \
  --format markdown

python -m leveraged_etp_risk_lab cycle-update \
  --cycle-state examples/outputs/cycle_state.json \
  --report-card examples/outputs/report_card.json \
  --watchlist examples/outputs/watchlist.json \
  --audit-trail examples/outputs/audit_trail.json \
  --format markdown

python -m leveraged_etp_risk_lab guardrail-policy \
  --policy default \
  --format markdown

python -m leveraged_etp_risk_lab guardrail-check \
  --policy examples/outputs/guardrail_policy.json \
  --portfolio-sensitivity examples/outputs/portfolio_sensitivity.json \
  --position-size examples/outputs/position_size.json \
  --investment-memo examples/outputs/investment_memo.json \
  --cycle-update examples/outputs/cycle_update.json \
  --format markdown

python -m leveraged_etp_risk_lab order-ticket \
  --guardrail-check examples/outputs/guardrail_check.json \
  --investment-memo examples/outputs/investment_memo.json \
  --position-size examples/outputs/position_size.json \
  --factsheet-check examples/outputs/factsheet_check.json \
  --thesis-dashboard-data examples/outputs/thesis_dashboard_data.json \
  --format markdown

python -m leveraged_etp_risk_lab order-review \
  --order-ticket examples/outputs/order_ticket.json \
  --guardrail-check examples/outputs/guardrail_check.json \
  --cycle-update examples/outputs/cycle_update.json \
  --audit-trail examples/outputs/audit_trail.json \
  --format markdown

python -m leveraged_etp_risk_lab demo-story \
  --input-dir examples/outputs \
  --format markdown

python -m leveraged_etp_risk_lab gallery-index \
  --input-dir examples/outputs \
  --format markdown

python -m leveraged_etp_risk_lab asset-hub \
  --input-dir examples/outputs \
  --format markdown

python -m leveraged_etp_risk_lab scenario-pack \
  --input-dir examples/outputs \
  --fixtures-dir examples/fixtures \
  --output-dir examples/outputs \
  --format markdown

python -m leveraged_etp_risk_lab release-manifest \
  --input-dir examples/outputs \
  --format markdown

python -m leveraged_etp_risk_lab docs-export \
  --input-dir examples/outputs \
  --output examples/outputs/docs_export.html

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
python -m leveraged_etp_risk_lab asset-hub --input-dir examples/outputs --format markdown
python -m leveraged_etp_risk_lab release-manifest --input-dir examples/outputs --format markdown
python -m leveraged_etp_risk_lab docs-export --input-dir examples/outputs --output examples/outputs/docs_export.html
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
- `recipe_thesis_review.json`: workflow recipe fixture for a factsheet, profile, scenario, sizing, stress, thesis, and watchlist bundle.

Generated path kinds are `trend`, `chop`, `crash`, and `rebound`. They are deterministic and use the same `day,label,underlying_return` CSV shape as checked-in path fixtures.

The `regime-list` command prints the built-in market regime gallery as JSON or Markdown. The gallery includes `trend_up`, `trend_down`, `chop`, `gap_down`, `rebound`, and `volatility_cluster`, with metadata, sample path rows, risk notes, and use cases. The `regime-export` command writes a selected regime to CSV in the same path format used by `simulate`.

The `pretrade-plan` command combines product terms, a scenario path, optional thesis text, stop/take bands, a user-supplied maximum loss budget, assumptions, warnings, and a checklist into a Markdown or JSON decision packet. It always includes explicit not-investment-advice language.

The `position-size` command reads either `--product` plus `--path`, or a generated `--pretrade-plan` JSON file. It sizes recommended notional from `--account-value` and exactly one of `--risk-budget-pct` or `--max-loss-budget`, carries an optional `--stop-loss`, emits a max-shares placeholder instead of fetching prices, and includes explicit not-investment-advice language.

The `stress-matrix` command reads a product JSON file and runs it across every built-in market regime, or only repeated `--regime` selections. It emits JSON or Markdown rows for modeled return, path decay versus a simple multiple, worst drawdown, stop/take event counts, and warning counts.

The `sensitivity-grid` command reads a product JSON file and runs every built-in regime across leverage, stop-loss, and take-profit grids. Default leverage multipliers are `1x`, `2x`, and `3x`; pass repeated or comma-separated `--leverage-multiplier`, `--stop-loss`, and `--take-profit` values to override grids. It emits JSON or Markdown focused on worst return, stop/take event counts, path decay, and warnings.

The `portfolio-sensitivity` command reads a portfolio manifest and runs sensitivity-grid style summaries for every leveraged position. It emits per-position worst return, modeled loss, and weighted exposure plus aggregate worst-case modeled loss and exposure across the manifest.

The `compare-runs` command reads two simulation, pretrade-plan, or exposure-report JSON outputs and emits deterministic JSON or Markdown deltas for return, path decay versus a simple multiple, weighted exposure, and warnings added or removed.

The `run-ledger` command appends JSONL metadata rows for generated artifacts. Rows include only deterministic metadata such as artifact filename, detected output type, schema version, byte count, and SHA-256 digest; artifact contents, secrets, timestamps, and machine-local absolute paths are not written.

The `thesis-impact` command reads a Markdown thesis file plus one or more generated JSON artifacts and maps extracted claims to observed return, path-decay, and exposure metrics where available. It also carries through relevant warnings and emits an action checklist for follow-up review.

The `watchlist-build` command reads a thesis-impact JSON artifact and a stress-matrix JSON artifact, then emits a deterministic watchlist ledger of thesis claims and regime triggers. Each entry includes severity, status, trigger text, next review questions, and source artifact references.

The `factsheet-check` command reads a product JSON file and an optional plain-text factsheet note. It emits JSON or Markdown checks for issuer, exchange, underlying, leverage factor, daily reset wording, fee, currency, liquidity/spread review placeholder, iNAV, premium/discount, and missing fields. It does not fetch live market data and includes explicit not-investment-advice language.

The `risk-profile` command emits deterministic JSON or Markdown risk-rule profiles for `default`, `conservative`, `active-trader`, and `thesis-review`. Each profile includes max holding days, a max-account-risk-percent placeholder, required factsheet fields, required scenario regimes, mandatory checklist questions, and stop/take review defaults.

The `recipe-run` command reads a JSON workflow recipe and composes the same library functions used by factsheet-check, risk-profile, simulate or built-in regime paths, stress-matrix, position-size, pretrade-plan, thesis-impact, and watchlist-build. It does not shell out or write hidden intermediates; it emits one deterministic JSON or Markdown bundle with conceptual command links and embedded component summaries.

The `report-card` command reads one or more generated JSON artifacts from simulation, pretrade-plan, position-size, stress-matrix, sensitivity-grid, factsheet-check, risk-profile, recipe-run, investment-memo, and memo-review outputs. It emits a concise decision-readiness card with strengths, unresolved checks, warnings, artifact metrics, and suggested next commands. It is deterministic and does not fetch live market data, shell out, read workflow files, or load private context.

The `thesis-dashboard-data` command reads recipe-run, report-card, watchlist, and sensitivity-grid JSON outputs and emits one JSON or Markdown packet for dashboard rendering. It keeps the merged data deterministic and records `live_market_data: false` and `shell_out: false`.

The `audit-trail` command reads a run-ledger JSONL file plus generated artifacts and emits a deterministic provenance checklist. It recomputes byte counts and SHA-256 hashes, compares them with ledger rows, and records pass/review status without embedding artifact contents.

The `schema-inventory` command reads local `docs/*.schema.json` files and lists document type, schema version, required top-level fields, matching examples from `examples/outputs`, and public safety notes. It is deterministic and records no live market data, shelling out, private context, or broker execution.

The `artifact-validate` command checks JSON and JSONL artifacts against the local lightweight schema inventory. With no paths it validates `examples/outputs`; with positional paths it validates only those artifacts. It checks required top-level fields, schema version, document type, and safety flags such as `live_market_data`, `shell_out`, `private_context`, and `broker_execution` when present.

The `memo-draft` command reads `recipe_run.json`, `thesis_dashboard_data.json`, `report_card.json`, and optional `factsheet_check.json` to emit a structured JSON or Markdown investment memo packet. The memo includes thesis, product terms, scenario evidence, risk budget, open checks, invalidation triggers, warnings, and explicit not-investment-advice language.

The `memo-review` command reads a memo JSON plus latest report-card, watchlist, and audit-trail JSON outputs. It emits a deterministic review checklist with changed risks and next actions, while recording `live_market_data: false` and `shell_out: false`.

The `cycle-init` command reads investment memo, watchlist, report-card, and sensitivity-grid JSON outputs and emits a persistent cycle state. The state includes a deterministic state id, baseline risks, baseline artifact hashes, compact baseline watch items, open checks, review cadence placeholders, and explicit not-investment-advice language.

The `cycle-update` command reads a cycle state plus latest report-card, watchlist, and audit-trail JSON outputs. It emits added, removed, and changed watch items, artifact hash drift, status transitions, and next review actions without timestamps, shelling out, live data, workflows, or private context.

The `guardrail-policy` command emits deterministic `default`, `conservative`, or `aggressive` allocation policies with max leverage exposure, max loss budget percent, max holding days, required artifact types, and review conditions. The `guardrail-check` command reads a policy JSON plus portfolio-sensitivity, position-size, investment-memo, and cycle-update artifacts, then emits `pass`, `review`, or `fail` results with violated rules and next actions. It does not fetch live market data, shell out, read workflow files, or load private context.

The `order-ticket` command reads guardrail, memo, sizing, factsheet, and optional thesis-dashboard artifacts, then emits a pre-order ticket with intent placeholders, max notional, required broker fields, a no-live-price warning, and do-not-trade-if conditions. The `order-review` command reads the ticket plus guardrail, cycle-update, and audit-trail artifacts, then emits a final educational checklist with `blocked`, `review`, or `ready` status. These commands do not fetch live data, read broker accounts, or place, stage, preview, route, or execute orders.

The `demo-story` command reads existing public demo outputs from an input directory: `stress_matrix.json`, `sensitivity_grid.json`, `watchlist.json`, `package_audit.json`, `pretrade_plan.json`, `report_card.json`, `investment_memo.json`, `investment_memo_review.json`, `cycle_state.json`, `cycle_update.json`, `guardrail_policy.json`, `guardrail_check.json`, `order_ticket.json`, and `order_review.json`. It emits a concise JSON or Markdown walkthrough with problem, workflow, commands, key outputs, safety caveats, and next extension ideas.

The `gallery-index` command reads the public demo output directory and emits a self-contained JSON or Markdown index grouped by workflow stage: fixtures, plans, sizing, stress, thesis/watchlist, audit/story, dashboard, and validation. Each artifact row includes filename, format, detected document type and schema version when available, byte count, and a suggested next command. It records metadata only and skips the generated `gallery_index.*` files for deterministic regeneration.

The `docs-export` command reads `release_manifest.json`, `asset_hub.json`, `demo_story.json`, `gallery_index.json`, `package_audit.json`, `scenario_pack.json`, and sibling Markdown artifacts from the public output directory. It emits one self-contained static HTML documentation page by default, or JSON/Markdown with `--format`. The HTML uses inline CSS only and links to local artifact paths; it has no JavaScript, no external assets, no live data, no workflow reads, and no private context.

The `static-dashboard` command writes a self-contained no-JavaScript HTML dashboard from either a portfolio manifest or demo output JSON files. It includes summary cards, positions, warnings, band events, and command provenance.

The `template-list` command prints the built-in product template gallery as JSON or Markdown. The gallery includes generic templates for 2x long equity, 3x long index, -2x inverse index, and 2x single-stock products, with leverage, risk notes, and use cases. The `template-export` command writes the selected template as product JSON that can be passed to `simulate` or `pretrade-plan`.

The `explain-term` command explains one built-in leveraged product glossary term in JSON or Markdown. Built-in term ids are `daily_reset`, `path_decay`, `volatility_decay`, `leverage_factor`, `stop_loss_band`, `take_profit_band`, `gap_risk`, `iNAV`, `premium_discount`, and `max_loss_budget`. Explanations are educational and include explicit not-investment-advice language.

The `glossary-list` command emits the full built-in glossary as JSON or Markdown. It is deterministic and does not read live market data, workflow files, private context, environment variables, or command history.

The `package-audit` command emits a deterministic JSON or Markdown package-readiness checklist. It checks README and license presence, schema and example outputs, the checked-in agent skill file, absence of workflow files, public hygiene, zero dependencies, version consistency, schema inventory, artifact validation, and listed test commands. Pass `--run-tests` to execute the listed validation commands during the audit.

The `scenario-pack` command writes a new-user evidence section into the pack and each case study. That section lists exact local commands, artifact links, and safety boundaries so a new user can reproduce the path-decay, drawdown, and pretrade-guardrail examples without live market data or broker execution. The pack also includes public integration notes for `portfolio-risk-compass` and `invest-thesis-ledger`, describing static artifact handoffs and explicitly avoiding runtime dependencies, schema coupling, private context, and bidirectional sync.

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
- `docs/sensitivity-grid.schema.json`
- `docs/portfolio-sensitivity.schema.json`
- `docs/template-gallery.schema.json`
- `docs/regime-gallery.schema.json`
- `docs/compare-runs.schema.json`
- `docs/run-ledger.schema.json`
- `docs/thesis-impact.schema.json`
- `docs/watchlist.schema.json`
- `docs/factsheet-check.schema.json`
- `docs/risk-profile.schema.json`
- `docs/recipe-run.schema.json`
- `docs/report-card.schema.json`
- `docs/thesis-dashboard-data.schema.json`
- `docs/audit-trail.schema.json`
- `docs/investment-memo.schema.json`
- `docs/investment-memo-review.schema.json`
- `docs/cycle-state.schema.json`
- `docs/cycle-update.schema.json`
- `docs/guardrail-policy.schema.json`
- `docs/guardrail-check.schema.json`
- `docs/order-ticket.schema.json`
- `docs/order-review.schema.json`
- `docs/package-audit.schema.json`
- `docs/docs-export.schema.json`
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
