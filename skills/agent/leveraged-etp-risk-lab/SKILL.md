# leveraged-etp-risk-lab Agent Skill

Use this skill when a user asks an agent to inspect, extend, validate, or explain the `leveraged-etp-risk-lab` repository or to run leveraged ETF/ETP daily-reset risk scenarios.

## Trigger Scenarios

- Add or review CLI commands for leveraged ETP scenario analysis.
- Validate product-term fixtures, scenario paths, or deterministic outputs.
- Generate deterministic trend, chop, crash, or rebound scenario paths.
- List or export built-in market regime paths for trend, chop, gap, rebound, and volatility-cluster scenarios.
- Explain built-in leveraged product glossary terms and list the glossary as JSON or Markdown.
- Aggregate exposure reports from a portfolio manifest.
- Build pretrade decision packets with explicit not-investment-advice language.
- Build position sizing plans from product/path inputs or pretrade-plan JSON.
- Run multi-regime stress matrices across built-in market regimes.
- Compare generated simulation, exposure, or pretrade JSON outputs.
- Append metadata-only JSONL ledger rows for generated outputs.
- Map thesis claims to observed metrics, warnings, and action checklists from generated JSON artifacts.
- Build thesis watchlist ledgers from thesis-impact and stress-matrix JSON artifacts.
- Check product JSON and optional factsheet notes for issuer, exchange, underlying, leverage, daily reset wording, fee, currency, liquidity/spread placeholder, iNAV, and premium/discount fields.
- Build public demo stories from checked-in demo output artifacts.
- Build public gallery indexes from checked-in demo output artifacts.
- Render static no-JavaScript dashboards from manifests or demo outputs.
- List or export built-in generic product templates.
- Audit package readiness for public sharing.
- Sync the checked-in skill file into a local Codex skills directory.
- Explain daily reset leverage, fee drag, path decay, volatility decay, leverage factors, stop-loss bands, take-profit bands, gap risk, iNAV, premium/discount, or maximum loss budgets.
- Run repository checks before sharing a public package.

## Route

1. Read `README.md`, `docs/schema.md`, and the relevant module in `leveraged_etp_risk_lab/`.
2. Prefer the CLI entry point: `python -m leveraged_etp_risk_lab`.
3. Keep the package dependency-free unless the user explicitly changes the project scope.
4. Keep generated public files generic and free of private names, machine-local paths, and secrets.

## Commands

```bash
python -m leveraged_etp_risk_lab --help
python -m leveraged_etp_risk_lab simulate --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv
python -m leveraged_etp_risk_lab generate-scenario --kind crash --days 10 --output crash_path.csv
python -m leveraged_etp_risk_lab exposure-report --manifest examples/fixtures/portfolio_manifest.json
python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --stop-loss 0.15 --take-profit 0.20
python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015 --format markdown
python -m leveraged_etp_risk_lab stress-matrix --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss 0.15 --take-profit 0.20 --format markdown
python -m leveraged_etp_risk_lab compare-runs --base examples/outputs/leveraged_nasdaq_3x.json --candidate examples/outputs/single_stock_2x.json --format markdown
python -m leveraged_etp_risk_lab run-ledger --ledger run_ledger.jsonl --artifact examples/outputs/leveraged_nasdaq_3x.json --artifact examples/outputs/pretrade_plan.json
python -m leveraged_etp_risk_lab thesis-impact --thesis-file examples/fixtures/thesis_note.md --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/portfolio_exposure.json --format markdown
python -m leveraged_etp_risk_lab watchlist-build --thesis-impact examples/outputs/thesis_impact.json --stress-matrix examples/outputs/stress_matrix.json --format markdown
python -m leveraged_etp_risk_lab factsheet-check --product examples/fixtures/leveraged_nasdaq_3x.json --factsheet-file examples/fixtures/factsheet_note.txt --format markdown
python -m leveraged_etp_risk_lab demo-story --input-dir examples/outputs --format markdown
python -m leveraged_etp_risk_lab gallery-index --input-dir examples/outputs --format markdown
python -m leveraged_etp_risk_lab static-dashboard --manifest examples/fixtures/portfolio_manifest.json --output examples/outputs/dashboard.html
python -m leveraged_etp_risk_lab template-list --format markdown
python -m leveraged_etp_risk_lab template-export --template generic-3x-long-index --output generic_index_3x.json
python -m leveraged_etp_risk_lab regime-list --format markdown
python -m leveraged_etp_risk_lab regime-export --regime volatility_cluster --days 12 --output volatility_cluster_path.csv
python -m leveraged_etp_risk_lab explain-term daily_reset --format markdown
python -m leveraged_etp_risk_lab glossary-list --format markdown
python -m leveraged_etp_risk_lab checklist --profile risk-review
python -m leveraged_etp_risk_lab demo-bundle --output-dir examples/outputs
python -m leveraged_etp_risk_lab package-audit --format markdown
python -m leveraged_etp_risk_lab selfcheck
python scripts/sync_local_skill.py
python scripts/selfcheck.py
python -m unittest discover -s tests
```

## Validation

- Run `python -m unittest discover -s tests`.
- Run `python scripts/selfcheck.py`.
- Confirm no `.github/workflows` files were added.
- Confirm CLI JSON output is deterministic for fixture inputs.
- Confirm generated scenario CSVs and exposure reports are deterministic for fixture inputs.
- Confirm pretrade plans include not-investment-advice language, assumptions, checklist items, and provenance.
- Confirm position size plans include recommended notional, max-shares placeholder, modeled loss at stop, exposure multiple, checklist items, and provenance.
- Confirm stress matrices include return, path decay, worst drawdown, stop/take event counts, warning counts, and provenance.
- Confirm comparison reports show return, path decay, weighted exposure, and warning deltas where available.
- Confirm ledger rows contain only deterministic metadata and do not embed artifact contents, timestamps, secrets, or absolute local paths.
- Confirm thesis impact reports map extracted thesis claims to available artifact metrics, related warnings, and actionable checklist items.
- Confirm watchlist ledgers include claim and regime-trigger entries with severity, next review questions, and source artifact refs.
- Confirm factsheet checks include issuer, exchange, underlying, leverage factor, daily reset wording, fee, currency, liquidity/spread placeholder, iNAV, premium/discount, missing fields, provenance, and not-investment-advice language.
- Confirm demo stories read stress-matrix, watchlist, package-audit, and pretrade-plan outputs and render problem, workflow, commands, key outputs, safety caveats, and next extension ideas.
- Confirm gallery indexes group public demo artifacts by fixtures, plans, sizing, stress, thesis/watchlist, audit/story, and dashboard, with bytes, document type, schema version, and suggested next commands.
- Confirm static dashboards are self-contained HTML with no JavaScript.
- Confirm `template-list` includes the four built-in generic templates and `template-export` writes product-schema JSON only.
- Confirm `regime-list` includes the six built-in regimes and `regime-export` writes `day,label,underlying_return` CSV only.
- Confirm `explain-term` covers the ten built-in glossary ids and `glossary-list` renders deterministic JSON/Markdown with not-investment-advice language.
- Confirm `package-audit` reports README, license, schemas, examples, skill file, workflow absence, public hygiene, zero dependencies, version consistency, and test commands.
- Confirm `scripts/sync_local_skill.py --target-dir <tmp>` copies `SKILL.md` without changing repository files.

## Safety Boundaries

- Do not present output as investment advice.
- Do not recommend buying, selling, or holding a product.
- Do not treat position sizing output as a recommendation.
- Do not treat multi-day leveraged returns as a simple multiple of the underlying.
- Do not add secrets, local paths, private names, or organization-specific messaging references to public files.

## Done Criteria

- CLI commands run through `python -m leveraged_etp_risk_lab`.
- Fixtures and docs match the schema notes.
- Package audit outputs exist in `examples/outputs/`.
- Tests and selfcheck pass.
- Public-facing text remains generic and suitable for an open repository.
