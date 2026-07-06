# Leveraged ETP Risk Lab Documentation

- Schema version: 0.30
- Source artifacts: 6/6 present
- Markdown artifacts: 44
- Release status: ready
- Package ready: yes

## Safety Caveats

- This decision packet is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.
- Do not present generated artifacts as investment advice, recommendations, suitability determinations, or broker orders.
- Do not fetch live or delayed market prices, quotes, spreads, depth, halts, or broker availability.
- Do not use private context, organization-specific messaging, secrets, environment variables, or workflow files.
- Treat position-size, guardrail, order-ticket, and order-review outputs as educational review aids only.
- The demo uses deterministic fixtures, not forecasts or live market data.
- Stop-loss and take-profit bands are planning levels, not guaranteed execution prices.
- Position sizing and watchlist severity are review aids, not recommendations.
- Order ticket and review outputs are educational checklists, not broker orders.
- The package intentionally avoids workflow files, secrets, live prices, and private context.
- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.
- Review aggregate modeled portfolio loss against the stated budget before proceeding.
- Close or explicitly accept memo open checks before relying on the allocation.
- Review memo invalidation triggers and regenerate memo artifacts if the thesis changed.
- Resolve cycle-update next review actions before proceeding.
- Do not use this output as a broker order or trade recommendation.
- Confirm all live broker, price, liquidity, and suitability requirements outside this package.
- No order has been placed, staged, routed, previewed, or transmitted.
- This documentation is for deterministic scenario planning and education only.
- It is not investment advice, a recommendation, broker instruction, or suitability determination.
- The export is static HTML with no JavaScript, no external assets, no live market data, no workflow reads, and no private context.

## Command Map

| Command | Purpose | Example |
| --- | --- | --- |
| `pretrade-plan` | Build the base thesis, budget, and risk-band packet. | `python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --stop-loss 0.15 --take-profit 0.20 --format markdown` |
| `stress-matrix` | Run the product across built-in deterministic regimes. | `python -m leveraged_etp_risk_lab stress-matrix --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss 0.15 --take-profit 0.20 --format markdown` |
| `sensitivity-grid` | Compare leverage, stop-loss, and take-profit grids. | `python -m leveraged_etp_risk_lab sensitivity-grid --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss none,0.15,0.25 --take-profit none,0.20,0.35 --format markdown` |
| `watchlist-build` | Turn thesis and stress results into review triggers. | `python -m leveraged_etp_risk_lab watchlist-build --thesis-impact examples/outputs/thesis_impact.json --stress-matrix examples/outputs/stress_matrix.json --format markdown` |
| `package-audit` | Check public sharing readiness and validation commands. | `python -m leveraged_etp_risk_lab package-audit --format markdown` |
| `recipe-run` | Compose the public workflow from one JSON recipe. | `python -m leveraged_etp_risk_lab recipe-run --recipe examples/fixtures/recipe_thesis_review.json --format markdown` |
| `report-card` | Summarize artifact strengths, warnings, and unresolved checks. | `python -m leveraged_etp_risk_lab report-card --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/position_size.json --artifact examples/outputs/stress_matrix.json --artifact examples/outputs/factsheet_check.json --format markdown` |
| `memo-draft` | Package thesis, scenario evidence, and risk budget into a memo. | `python -m leveraged_etp_risk_lab memo-draft --recipe-run examples/outputs/recipe_run.json --thesis-dashboard-data examples/outputs/thesis_dashboard_data.json --report-card examples/outputs/report_card.json --factsheet-check examples/outputs/factsheet_check.json --format markdown` |
| `memo-review` | Compare the memo against latest review artifacts. | `python -m leveraged_etp_risk_lab memo-review --memo examples/outputs/investment_memo.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --audit-trail examples/outputs/audit_trail.json --format markdown` |
| `cycle-init` | Create a persistent public watch-cycle state. | `python -m leveraged_etp_risk_lab cycle-init --memo examples/outputs/investment_memo.json --watchlist examples/outputs/watchlist.json --report-card examples/outputs/report_card.json --sensitivity-grid examples/outputs/sensitivity_grid.json --format markdown` |
| `cycle-update` | Detect watch-cycle hash drift and watchlist changes. | `python -m leveraged_etp_risk_lab cycle-update --cycle-state examples/outputs/cycle_state.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --audit-trail examples/outputs/audit_trail.json --format markdown` |
| `guardrail-policy` | Emit explicit allocation review limits. | `python -m leveraged_etp_risk_lab guardrail-policy --policy default --format markdown` |
| `guardrail-check` | Gate artifacts against exposure, budget, horizon, and review rules. | `python -m leveraged_etp_risk_lab guardrail-check --policy examples/outputs/guardrail_policy.json --portfolio-sensitivity examples/outputs/portfolio_sensitivity.json --position-size examples/outputs/position_size.json --investment-memo examples/outputs/investment_memo.json --cycle-update examples/outputs/cycle_update.json --format markdown` |
| `order-ticket` | Create placeholder-only broker field and do-not-trade checklists. | `python -m leveraged_etp_risk_lab order-ticket --guardrail-check examples/outputs/guardrail_check.json --investment-memo examples/outputs/investment_memo.json --position-size examples/outputs/position_size.json --factsheet-check examples/outputs/factsheet_check.json --thesis-dashboard-data examples/outputs/thesis_dashboard_data.json --format markdown` |
| `order-review` | Run a final educational order review without execution. | `python -m leveraged_etp_risk_lab order-review --order-ticket examples/outputs/order_ticket.json --guardrail-check examples/outputs/guardrail_check.json --cycle-update examples/outputs/cycle_update.json --audit-trail examples/outputs/audit_trail.json --format markdown` |
| `demo-story` | Render the public walkthrough from checked demo artifacts. | `python -m leveraged_etp_risk_lab demo-story --input-dir examples/outputs --format markdown` |
| `scenario-pack` | Write new-user case-study packs for path decay, drawdowns, and guardrails. | `python -m leveraged_etp_risk_lab scenario-pack --input-dir examples/outputs --fixtures-dir examples/fixtures --output-dir examples/outputs --format markdown` |
| `schema-inventory` | List local schemas, required fields, matching examples, and public safety notes. | `python -m leveraged_etp_risk_lab schema-inventory --format markdown` |
| `artifact-validate` | Validate example JSON artifacts against the local lightweight schema inventory. | `python -m leveraged_etp_risk_lab artifact-validate --format markdown` |
| `release-manifest` | Emit release readiness, public artifact inventory, and release notes. | `python -m leveraged_etp_risk_lab release-manifest --input-dir examples/outputs --format markdown` |
| `docs-export` | Render one self-contained static HTML documentation page from public artifacts. | `python -m leveraged_etp_risk_lab docs-export --input-dir examples/outputs --output examples/outputs/docs_export.html` |
| `asset-hub` | Emit the GitHub-facing public asset hub. | `python -m leveraged_etp_risk_lab asset-hub --input-dir examples/outputs --format markdown` |

## Integration Notes

| System | Complement | Dependency Boundary |
| --- | --- | --- |
| `portfolio-risk-compass` | Scenario-pack outputs provide deterministic stress narratives and case-study metrics that can support a portfolio risk review as evidence for path decay, drawdown, and guardrail checks. | No import, API call, shared storage, live-data feed, broker connection, or runtime dependency is required; another system can read or ignore these static files independently. |
| `invest-thesis-ledger` | Scenario-pack case studies can be attached to thesis records as reproducible evidence for thesis pressure tests, invalidation checks, and pretrade review notes. | No dependency, ledger schema change, plugin, workflow read, command history read, or bidirectional sync is assumed; the notes are portable references, not a required integration. |

## Release Notes

## v0.31.3

### Highlights

- Adds deterministic scenario-pack visual receipts with JSON, Markdown, and static HTML release-owner views.
- Connects demo-bundle outputs, scenario-pack case studies, reviewer hashes, checklist prompts, and safety boundaries.
- Carries safety caveats, command map, release notes, and local artifact links from checked public artifacts.
- Publishes 97 public demo artifacts across 8 gallery stages.
- Tracks 45 local schemas and 45 validated artifacts.

### Readiness

- Release status: ready
- Package audit ready: yes
- Artifact validation ready: yes

### Verification

- `python -m unittest discover -s tests`
- `python scripts/selfcheck.py`
- `python -m leveraged_etp_risk_lab docs-export --input-dir examples/outputs --output examples/outputs/docs_export.html`
- `python -m leveraged_etp_risk_lab package-audit --run-tests --format json`

## Local Artifact Links

| Artifact | Type | Stage |
| --- | --- | --- |
| `examples/outputs/checklist.md` | md | fixtures |
| `examples/outputs/glossary.json` | json | fixtures |
| `examples/outputs/glossary.md` | md | fixtures |
| `examples/outputs/leveraged_nasdaq_3x.json` | json | fixtures |
| `examples/outputs/leveraged_nasdaq_3x.md` | md | fixtures |
| `examples/outputs/portfolio_exposure.json` | json | fixtures |
| `examples/outputs/portfolio_exposure.md` | md | fixtures |
| `examples/outputs/product_family_walkthrough.json` | json | fixtures |
| `examples/outputs/product_family_walkthrough.md` | md | fixtures |
| `examples/outputs/product_snapshot_tqqq_case_study.json` | json | fixtures |
| `examples/outputs/product_snapshot_tqqq_case_study.md` | md | fixtures |
| `examples/outputs/regime_chop.csv` | csv | fixtures |
| `examples/outputs/regime_gallery.json` | json | fixtures |
| `examples/outputs/regime_gallery.md` | md | fixtures |
| `examples/outputs/regime_gap_down.csv` | csv | fixtures |
| `examples/outputs/regime_rebound.csv` | csv | fixtures |
| `examples/outputs/regime_trend_down.csv` | csv | fixtures |
| `examples/outputs/regime_trend_up.csv` | csv | fixtures |
| `examples/outputs/regime_volatility_cluster.csv` | csv | fixtures |
| `examples/outputs/risk_profiles.json` | json | fixtures |
| `examples/outputs/risk_profiles.md` | md | fixtures |
| `examples/outputs/single_stock_2x.json` | json | fixtures |
| `examples/outputs/single_stock_2x.md` | md | fixtures |
| `examples/outputs/template_gallery.json` | json | fixtures |
| `examples/outputs/template_gallery.md` | md | fixtures |
| `examples/outputs/compare_runs.json` | json | plans |
| `examples/outputs/compare_runs.md` | md | plans |
| `examples/outputs/pretrade_plan.json` | json | plans |
| `examples/outputs/pretrade_plan.md` | md | plans |
| `examples/outputs/recipe_run.json` | json | plans |
| `examples/outputs/recipe_run.md` | md | plans |
| `examples/outputs/report_card.json` | json | plans |
| `examples/outputs/report_card.md` | md | plans |
| `examples/outputs/run_ledger.jsonl` | jsonl | plans |
| `examples/outputs/position_size.json` | json | sizing |
| `examples/outputs/position_size.md` | md | sizing |
| `examples/outputs/portfolio_sensitivity.json` | json | stress |
| `examples/outputs/portfolio_sensitivity.md` | md | stress |
| `examples/outputs/sensitivity_grid.json` | json | stress |
| `examples/outputs/sensitivity_grid.md` | md | stress |
| `examples/outputs/stress_matrix.json` | json | stress |
| `examples/outputs/stress_matrix.md` | md | stress |
| `examples/outputs/thesis_impact.json` | json | thesis/watchlist |
| `examples/outputs/thesis_impact.md` | md | thesis/watchlist |
| `examples/outputs/watchlist.json` | json | thesis/watchlist |
| `examples/outputs/watchlist.md` | md | thesis/watchlist |
| `examples/outputs/asset_hub.json` | json | audit/story |
| `examples/outputs/asset_hub.md` | md | audit/story |
| `examples/outputs/audit_trail.json` | json | audit/story |
| `examples/outputs/audit_trail.md` | md | audit/story |
| `examples/outputs/daily_reset_path_decay.json` | json | audit/story |
| `examples/outputs/daily_reset_path_decay.md` | md | audit/story |
| `examples/outputs/demo_story.json` | json | audit/story |
| `examples/outputs/demo_story.md` | md | audit/story |
| `examples/outputs/drawdown_risk.json` | json | audit/story |
| `examples/outputs/drawdown_risk.md` | md | audit/story |
| `examples/outputs/factsheet_check.json` | json | audit/story |
| `examples/outputs/factsheet_check.md` | md | audit/story |
| `examples/outputs/package_audit.json` | json | audit/story |
| `examples/outputs/package_audit.md` | md | audit/story |
| `examples/outputs/pretrade_guardrails.json` | json | audit/story |
| `examples/outputs/pretrade_guardrails.md` | md | audit/story |
| `examples/outputs/scenario_pack.json` | json | audit/story |
| `examples/outputs/scenario_pack.md` | md | audit/story |
| `examples/outputs/scenario_pack_reviewer_receipt.json` | json | audit/story |
| `examples/outputs/scenario_pack_reviewer_receipt.md` | md | audit/story |
| `examples/outputs/scenario_pack_visual_receipt.html` | html | audit/story |
| `examples/outputs/scenario_pack_visual_receipt.json` | json | audit/story |
| `examples/outputs/scenario_pack_visual_receipt.md` | md | audit/story |
| `examples/outputs/cycle_state.json` | json | dashboard |
| `examples/outputs/cycle_state.md` | md | dashboard |
| `examples/outputs/cycle_update.json` | json | dashboard |
| `examples/outputs/cycle_update.md` | md | dashboard |
| `examples/outputs/dashboard.html` | html | dashboard |
| `examples/outputs/guardrail_check.json` | json | dashboard |
| `examples/outputs/guardrail_check.md` | md | dashboard |
| `examples/outputs/guardrail_policy.json` | json | dashboard |
| `examples/outputs/guardrail_policy.md` | md | dashboard |
| `examples/outputs/investment_memo.json` | json | dashboard |
| `examples/outputs/investment_memo.md` | md | dashboard |
| `examples/outputs/investment_memo_review.json` | json | dashboard |
| `examples/outputs/investment_memo_review.md` | md | dashboard |
| `examples/outputs/order_review.json` | json | dashboard |
| `examples/outputs/order_review.md` | md | dashboard |
| `examples/outputs/order_ticket.json` | json | dashboard |
| `examples/outputs/order_ticket.md` | md | dashboard |
| `examples/outputs/thesis_dashboard_data.json` | json | dashboard |
| `examples/outputs/thesis_dashboard_data.md` | md | dashboard |
| `examples/outputs/artifact_validation.json` | json | validation |
| `examples/outputs/artifact_validation.md` | md | validation |
| `examples/outputs/docs_export.html` | html | validation |
| `examples/outputs/docs_export.json` | json | validation |
| `examples/outputs/docs_export.md` | md | validation |
| `examples/outputs/release_manifest.json` | json | validation |
| `examples/outputs/release_manifest.md` | md | validation |
| `examples/outputs/schema_inventory.json` | json | validation |
| `examples/outputs/schema_inventory.md` | md | validation |
| `examples/outputs/gallery_index.md` | markdown | markdown |

## Markdown Artifacts

| Artifact | Title | Bytes |
| --- | --- | ---: |
| `examples/outputs/artifact_validation.md` | Artifact Validation | 6086 |
| `examples/outputs/asset_hub.md` | leveraged-etp-risk-lab Public Asset Hub | 12270 |
| `examples/outputs/audit_trail.md` | Audit Trail | 3660 |
| `examples/outputs/checklist.md` | Leveraged ETP Risk Checklist: risk-review | 718 |
| `examples/outputs/compare_runs.md` | Run Comparison | 408 |
| `examples/outputs/cycle_state.md` | Watch Cycle State | 3271 |
| `examples/outputs/cycle_update.md` | Watch Cycle Update | 1435 |
| `examples/outputs/daily_reset_path_decay.md` | Daily Reset Path Decay | 3728 |
| `examples/outputs/demo_story.md` | Public Demo Story | 9204 |
| `examples/outputs/drawdown_risk.md` | Drawdown Risk Under Regime Stress | 3484 |
| `examples/outputs/factsheet_check.md` | Product Factsheet Checklist | 1174 |
| `examples/outputs/gallery_index.md` | Public Gallery Index | 26733 |
| `examples/outputs/glossary.md` | Leveraged Product Glossary | 5341 |
| `examples/outputs/guardrail_check.md` | Allocation Guardrail Check | 2207 |
| `examples/outputs/guardrail_policy.md` | Allocation Guardrail Policy: default | 961 |
| `examples/outputs/investment_memo.md` | Investment Memo: NDAQ3X | 4262 |
| `examples/outputs/investment_memo_review.md` | Investment Memo Review | 2477 |
| `examples/outputs/leveraged_nasdaq_3x.md` | Simulation: NDAQ3X | 1426 |
| `examples/outputs/order_review.md` | Final Educational Order Review | 1414 |
| `examples/outputs/order_ticket.md` | Pre-Order Ticket: NDAQ3X | 3555 |
| `examples/outputs/package_audit.md` | Package Audit | 6144 |
| `examples/outputs/portfolio_exposure.md` | Exposure Report: Generic Leveraged ETP Portfolio | 1430 |
| `examples/outputs/portfolio_sensitivity.md` | Portfolio Sensitivity: Generic Leveraged ETP Portfolio | 1870 |
| `examples/outputs/position_size.md` | Position Size Plan: NDAQ3X | 2279 |
| `examples/outputs/pretrade_guardrails.md` | Pretrade Guardrails Before An Order | 3693 |
| `examples/outputs/pretrade_plan.md` | Pretrade Plan: NDAQ3X | 3090 |
| `examples/outputs/product_family_walkthrough.md` | Product Family Walkthrough | 4679 |
| `examples/outputs/product_snapshot_tqqq_case_study.md` | TQQQ Daily-Target Product Snapshot | 3332 |
| `examples/outputs/recipe_run.md` | Recipe Run | 1965 |
| `examples/outputs/regime_gallery.md` | Market Regime Gallery | 4525 |
| `examples/outputs/release_manifest.md` | Release Manifest | 4142 |
| `examples/outputs/report_card.md` | Decision Readiness Report Card | 4259 |
| `examples/outputs/risk_profiles.md` | Risk Rule Profiles | 4978 |
| `examples/outputs/scenario_pack.md` | New User Scenario Pack | 4679 |
| `examples/outputs/scenario_pack_reviewer_receipt.md` | Scenario Pack Reviewer Receipt | 5517 |
| `examples/outputs/scenario_pack_visual_receipt.md` | Scenario Pack Visual Receipt | 6149 |
| `examples/outputs/schema_inventory.md` | Schema Inventory | 14620 |
| `examples/outputs/sensitivity_grid.md` | Sensitivity Grid: NDAQ3X | 3962 |
| `examples/outputs/single_stock_2x.md` | Simulation: STK2X | 1372 |
| `examples/outputs/stress_matrix.md` | Stress Matrix: NDAQ3X | 1957 |
| `examples/outputs/template_gallery.md` | Product Template Gallery | 2751 |
| `examples/outputs/thesis_dashboard_data.md` | Thesis Dashboard Data | 2658 |
| `examples/outputs/thesis_impact.md` | Thesis Impact | 4851 |
| `examples/outputs/watchlist.md` | Thesis Watchlist | 9699 |

## Provenance

- command: docs-export
- external_assets: False
- input_dir: examples/outputs
- javascript: False
- live_market_data: False
- private_context: False
- workflow_files_read: False
