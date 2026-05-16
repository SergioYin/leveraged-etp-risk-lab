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
- Run sensitivity grids across leverage multipliers, stop-loss values, take-profit values, and built-in regimes.
- Run portfolio sensitivity summaries from a manifest and aggregate worst-case exposure.
- Compare generated simulation, exposure, or pretrade JSON outputs.
- Append metadata-only JSONL ledger rows for generated outputs.
- Map thesis claims to observed metrics, warnings, and action checklists from generated JSON artifacts.
- Build thesis watchlist ledgers from thesis-impact and stress-matrix JSON artifacts.
- Check product JSON and optional factsheet notes for issuer, exchange, underlying, leverage, daily reset wording, fee, currency, liquidity/spread placeholder, iNAV, and premium/discount fields.
- Emit risk-rule profiles for default, conservative, active-trader, and thesis-review workflows.
- Run JSON workflow recipes that compose factsheet, profile, scenario, stress, sizing, pretrade, thesis, and watchlist outputs without shelling out.
- Build decision-readiness report cards from generated JSON artifacts with strengths, unresolved checks, warnings, and next commands.
- Build thesis dashboard data packets from recipe-run, report-card, watchlist, and sensitivity-grid outputs.
- Build audit trails from run-ledger JSONL files and generated artifact hashes.
- Build investment memo packets from recipe-run, thesis-dashboard-data, report-card, and optional factsheet-check JSON artifacts.
- Review investment memo packets against latest report-card, watchlist, and audit-trail JSON artifacts.
- Initialize and update persistent watch cycle state from memo, watchlist, report-card, sensitivity-grid, and audit-trail artifacts.
- Emit allocation guardrail policies and check portfolio-sensitivity, position-size, investment-memo, and cycle-update artifacts against explicit exposure, loss-budget, holding-period, artifact, and review rules.
- Build placeholder-only order tickets and final educational order review checklists without live data or broker execution.
- Build public demo stories from checked-in demo output artifacts.
- Build public gallery indexes from checked-in demo output artifacts.
- Build public asset hubs from checked-in package-audit, gallery-index, demo-story, order-review, guardrail-check, and cycle-update artifacts.
- Build release manifests from checked-in public release artifacts with optional git metadata, release notes drafts, skill sync guidance, and post-release checks.
- Export one self-contained static HTML documentation page from checked-in release, asset-hub, demo-story, gallery-index, package-audit, and Markdown artifacts.
- Build new-user scenario packs with exact reproducibility commands, artifact links, and safety boundaries for path decay, drawdown risk, and pretrade guardrails.
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
python -m leveraged_etp_risk_lab sensitivity-grid --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss none,0.15,0.25 --take-profit none,0.20,0.35 --format markdown
python -m leveraged_etp_risk_lab portfolio-sensitivity --manifest examples/fixtures/portfolio_manifest.json --stop-loss none,0.15,0.25 --take-profit none,0.20,0.35 --format markdown
python -m leveraged_etp_risk_lab compare-runs --base examples/outputs/leveraged_nasdaq_3x.json --candidate examples/outputs/single_stock_2x.json --format markdown
python -m leveraged_etp_risk_lab run-ledger --ledger run_ledger.jsonl --artifact examples/outputs/leveraged_nasdaq_3x.json --artifact examples/outputs/pretrade_plan.json
python -m leveraged_etp_risk_lab thesis-impact --thesis-file examples/fixtures/thesis_note.md --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/portfolio_exposure.json --format markdown
python -m leveraged_etp_risk_lab watchlist-build --thesis-impact examples/outputs/thesis_impact.json --stress-matrix examples/outputs/stress_matrix.json --format markdown
python -m leveraged_etp_risk_lab factsheet-check --product examples/fixtures/leveraged_nasdaq_3x.json --factsheet-file examples/fixtures/factsheet_note.txt --format markdown
python -m leveraged_etp_risk_lab risk-profile --profile thesis-review --format markdown
python -m leveraged_etp_risk_lab recipe-run --recipe examples/fixtures/recipe_thesis_review.json --format markdown
python -m leveraged_etp_risk_lab report-card --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/position_size.json --artifact examples/outputs/stress_matrix.json --artifact examples/outputs/factsheet_check.json --format markdown
python -m leveraged_etp_risk_lab thesis-dashboard-data --recipe-run examples/outputs/recipe_run.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --sensitivity-grid examples/outputs/sensitivity_grid.json --format markdown
python -m leveraged_etp_risk_lab audit-trail --ledger examples/outputs/run_ledger.jsonl --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/stress_matrix.json --format markdown
python -m leveraged_etp_risk_lab memo-draft --recipe-run examples/outputs/recipe_run.json --thesis-dashboard-data examples/outputs/thesis_dashboard_data.json --report-card examples/outputs/report_card.json --factsheet-check examples/outputs/factsheet_check.json --format markdown
python -m leveraged_etp_risk_lab memo-review --memo examples/outputs/investment_memo.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --audit-trail examples/outputs/audit_trail.json --format markdown
python -m leveraged_etp_risk_lab cycle-init --memo examples/outputs/investment_memo.json --watchlist examples/outputs/watchlist.json --report-card examples/outputs/report_card.json --sensitivity-grid examples/outputs/sensitivity_grid.json --format markdown
python -m leveraged_etp_risk_lab cycle-update --cycle-state examples/outputs/cycle_state.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --audit-trail examples/outputs/audit_trail.json --format markdown
python -m leveraged_etp_risk_lab guardrail-policy --policy default --format markdown
python -m leveraged_etp_risk_lab guardrail-check --policy examples/outputs/guardrail_policy.json --portfolio-sensitivity examples/outputs/portfolio_sensitivity.json --position-size examples/outputs/position_size.json --investment-memo examples/outputs/investment_memo.json --cycle-update examples/outputs/cycle_update.json --format markdown
python -m leveraged_etp_risk_lab order-ticket --guardrail-check examples/outputs/guardrail_check.json --investment-memo examples/outputs/investment_memo.json --position-size examples/outputs/position_size.json --factsheet-check examples/outputs/factsheet_check.json --thesis-dashboard-data examples/outputs/thesis_dashboard_data.json --format markdown
python -m leveraged_etp_risk_lab order-review --order-ticket examples/outputs/order_ticket.json --guardrail-check examples/outputs/guardrail_check.json --cycle-update examples/outputs/cycle_update.json --audit-trail examples/outputs/audit_trail.json --format markdown
python -m leveraged_etp_risk_lab demo-story --input-dir examples/outputs --format markdown
python -m leveraged_etp_risk_lab gallery-index --input-dir examples/outputs --format markdown
python -m leveraged_etp_risk_lab asset-hub --input-dir examples/outputs --format markdown
python -m leveraged_etp_risk_lab release-manifest --input-dir examples/outputs --format markdown
python -m leveraged_etp_risk_lab docs-export --input-dir examples/outputs --output examples/outputs/docs_export.html
python -m leveraged_etp_risk_lab scenario-pack --input-dir examples/outputs --fixtures-dir examples/fixtures --output-dir examples/outputs --format markdown
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
- Confirm sensitivity grids include leverage, stop-loss, and take-profit grids; worst return; stop/take event counts; path decay; warnings; `live_market_data: false`; and `shell_out: false`.
- Confirm portfolio sensitivity outputs include per-position sensitivity summaries, aggregate worst-case modeled loss, aggregate worst-case weighted exposure, warnings, and deterministic provenance.
- Confirm comparison reports show return, path decay, weighted exposure, and warning deltas where available.
- Confirm ledger rows contain only deterministic metadata and do not embed artifact contents, timestamps, secrets, or absolute local paths.
- Confirm thesis impact reports map extracted thesis claims to available artifact metrics, related warnings, and actionable checklist items.
- Confirm watchlist ledgers include claim and regime-trigger entries with severity, next review questions, and source artifact refs.
- Confirm factsheet checks include issuer, exchange, underlying, leverage factor, daily reset wording, fee, currency, liquidity/spread placeholder, iNAV, premium/discount, missing fields, provenance, and not-investment-advice language.
- Confirm risk profiles include max holding days, account-risk placeholder text, factsheet fields, scenario regimes, checklist questions, stop/take review defaults, provenance, and not-investment-advice language.
- Confirm recipe-run bundles include component summaries, conceptual command links, embedded artifacts, `shell_out: false`, and no hidden workflow/private context assumptions.
- Confirm report cards read only generated JSON artifacts, include strengths, unresolved checks, warnings, next commands, `live_market_data: false`, and `shell_out: false`.
- Confirm thesis dashboard data reads recipe-run, report-card, watchlist, and sensitivity-grid artifacts and emits summary cards with deterministic provenance.
- Confirm audit trails compare generated artifact byte counts and SHA-256 hashes against run-ledger rows without embedding artifact contents.
- Confirm memo drafts include thesis, product terms, scenario evidence, risk budget, open checks, invalidation triggers, warnings, `not_investment_advice`, `live_market_data: false`, and `shell_out: false`.
- Confirm memo reviews read latest report-card, watchlist, and audit-trail outputs and emit changed risks, deterministic checklist items, next actions, `live_market_data: false`, and `shell_out: false`.
- Confirm watch cycle states include deterministic state ids, baseline risks, baseline artifact hashes, baseline watch items, open checks, review cadence placeholders, and not-investment-advice language.
- Confirm watch cycle updates read latest report-card, watchlist, and audit-trail outputs and emit added, removed, changed watch items, hash drift, status transitions, next review actions, `live_market_data: false`, and `shell_out: false`.
- Confirm guardrail policies include max leverage exposure, max loss budget percent, max holding days, required artifacts, review conditions, `live_market_data: false`, and `shell_out: false`.
- Confirm guardrail checks read policy, portfolio-sensitivity, position-size, investment-memo, and cycle-update artifacts and emit pass/review/fail results, violated rules, next actions, `live_market_data: false`, and `shell_out: false`.
- Confirm order tickets read guardrail-check, investment-memo, position-size, factsheet-check, and optional thesis-dashboard-data artifacts and emit order intent placeholders, max notional, required broker fields, no-live-price warnings, do-not-trade-if conditions, `live_market_data: false`, `shell_out: false`, and `broker_execution: false`.
- Confirm order reviews read order-ticket, guardrail-check, cycle-update, and audit-trail artifacts and emit blocked/review/ready checklist status, final educational notes, `live_market_data: false`, `shell_out: false`, and `broker_execution: false`.
- Confirm schema inventories list every `docs/*.schema.json` file with document type, schema version, required top-level fields, matching examples, public safety notes, and provenance flags showing no live data, shelling out, private context, or broker execution.
- Confirm artifact validation runs against `examples/outputs` or explicit JSON/JSONL paths, checks local lightweight required fields and schema consts, validates provenance safety flags when present, and uses no external `jsonschema` dependency.
- Confirm demo stories read stress-matrix, sensitivity-grid, watchlist, package-audit, pretrade-plan, report-card, investment-memo, investment-memo-review, cycle-state, cycle-update, guardrail-policy, guardrail-check, order-ticket, and order-review outputs and render problem, workflow, commands, key outputs, safety caveats, and next extension ideas.
- Confirm gallery indexes group public demo artifacts by fixtures, plans, sizing, stress, thesis/watchlist, audit/story, dashboard, and validation, with bytes, document type, schema version, and suggested next commands.
- Confirm asset hubs read checked package-audit, gallery-index, demo-story, order-review, guardrail-check, and cycle-update artifacts and render product positioning, command map, demo artifact map, readiness checklist, safety boundaries, agent skill path, release checklist, and three-version roadmap.
- Confirm release manifests read asset-hub, package-audit, artifact-validation, schema-inventory, demo-story, gallery-index, and optional git metadata without failing when artifacts or git metadata are absent, and render public artifact inventory, validation summary, release readiness, agent skill path, local skill sync recommendation, GitHub release notes draft, and post-release verification checklist.
- Confirm docs exports read release-manifest, asset-hub, demo-story, gallery-index, package-audit, and sibling Markdown artifacts and render one self-contained static HTML page with no JavaScript, no external assets, safety caveats, command map, release notes, local artifact links, and deterministic provenance.
- Confirm scenario packs and case studies include `cold_user_evidence` with exact commands, local artifact links, safety boundaries, deterministic source artifacts, `live_market_data: false`, `shell_out: false`, `private_context: false`, and `broker_execution: false`.
- Confirm demo-bundle converges generated release artifacts deterministically instead of relying on hand-duplicated regeneration steps.
- Confirm static dashboards are self-contained HTML with no JavaScript.
- Confirm `template-list` includes the four built-in generic templates and `template-export` writes product-schema JSON only.
- Confirm `regime-list` includes the six built-in regimes and `regime-export` writes `day,label,underlying_return` CSV only.
- Confirm `explain-term` covers the ten built-in glossary ids and `glossary-list` renders deterministic JSON/Markdown with not-investment-advice language.
- Confirm `package-audit` reports README, license, schemas, examples, skill file, workflow absence, public hygiene, zero dependencies, version consistency, schema inventory, artifact validation, and test commands.
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
