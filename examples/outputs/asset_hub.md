# leveraged-etp-risk-lab Public Asset Hub

**Version:** 0.29.0

**Not investment advice:** This decision packet is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

leveraged-etp-risk-lab is a zero-dependency Python CLI for planning daily-reset leveraged ETF/ETP risk scenarios. It models product terms, deterministic scenario paths, daily reset leverage, management-fee drag, path decay versus a simple multiple, stop-loss and take-profit bands, portfolio exposure aggregation, and plain-language warnings.

## Product Positioning

- Developers and agents validating deterministic leveraged ETP examples.
- Risk reviewers who need public, reproducible scenario artifacts.
- Educators explaining daily-reset leverage, path decay, and review checklists.

### Proof Points

- 80 checked demo artifacts indexed from examples/outputs.
- Package audit ready=True with 10 passed checks.
- No runtime dependencies, workflow files, private context, broker execution, or live market data.

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
| `schema-inventory` | List local schemas, required fields, matching examples, and public safety notes. | `python -m leveraged_etp_risk_lab schema-inventory --format markdown` |
| `artifact-validate` | Validate example JSON artifacts against the local lightweight schema inventory. | `python -m leveraged_etp_risk_lab artifact-validate --format markdown` |
| `release-manifest` | Emit release readiness, public artifact inventory, and release notes. | `python -m leveraged_etp_risk_lab release-manifest --input-dir examples/outputs --format markdown` |
| `docs-export` | Render one self-contained static HTML documentation page from public artifacts. | `python -m leveraged_etp_risk_lab docs-export --input-dir examples/outputs --output examples/outputs/docs_export.html` |
| `asset-hub` | Emit the GitHub-facing public asset hub. | `python -m leveraged_etp_risk_lab asset-hub --input-dir examples/outputs --format markdown` |

## Demo Artifact Map

| Stage | Artifacts | Key artifacts |
| --- | --- | --- |
| fixtures | 21 | examples/outputs/glossary.json, examples/outputs/glossary.md, examples/outputs/leveraged_nasdaq_3x.json, examples/outputs/leveraged_nasdaq_3x.md, examples/outputs/portfolio_exposure.json, examples/outputs/portfolio_exposure.md |
| plans | 9 | examples/outputs/compare_runs.json, examples/outputs/compare_runs.md, examples/outputs/pretrade_plan.json, examples/outputs/pretrade_plan.md, examples/outputs/recipe_run.json, examples/outputs/recipe_run.md |
| sizing | 2 | examples/outputs/position_size.json, examples/outputs/position_size.md |
| stress | 6 | examples/outputs/portfolio_sensitivity.json, examples/outputs/portfolio_sensitivity.md, examples/outputs/sensitivity_grid.json, examples/outputs/sensitivity_grid.md, examples/outputs/stress_matrix.json, examples/outputs/stress_matrix.md |
| thesis/watchlist | 4 | examples/outputs/thesis_impact.json, examples/outputs/thesis_impact.md, examples/outputs/watchlist.json, examples/outputs/watchlist.md |
| audit/story | 10 | examples/outputs/asset_hub.json, examples/outputs/asset_hub.md, examples/outputs/audit_trail.json, examples/outputs/audit_trail.md, examples/outputs/demo_story.json, examples/outputs/demo_story.md |
| dashboard | 19 | examples/outputs/cycle_state.json, examples/outputs/cycle_state.md, examples/outputs/cycle_update.json, examples/outputs/cycle_update.md, examples/outputs/guardrail_check.json, examples/outputs/guardrail_check.md |
| validation | 9 | examples/outputs/artifact_validation.json, examples/outputs/artifact_validation.md, examples/outputs/docs_export.html, examples/outputs/docs_export.json, examples/outputs/docs_export.md, examples/outputs/release_manifest.json |

## Readiness Checklist

- [x] Package audit reports public readiness. (pass)
- [x] Runtime dependency list is empty. (pass)
- [x] No workflow files are present. (pass)
- [x] No private names, local paths, or secret-like values were found. (pass)
- [x] Guardrail check completed without a fail result. (pass)
- [x] Order review confirms no broker execution. (pass)
- [x] Cycle update artifact is present and deterministic. (pass)

## Safety Boundaries

- Do not present generated artifacts as investment advice, recommendations, suitability determinations, or broker orders.
- Do not fetch live or delayed market prices, quotes, spreads, depth, halts, or broker availability.
- Do not use private context, organization-specific messaging, secrets, environment variables, or workflow files.
- Treat position-size, guardrail, order-ticket, and order-review outputs as educational review aids only.
- This decision packet is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.
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

## Agent Skill Path

- `skills/agent/leveraged-etp-risk-lab/SKILL.md`

## Release Checklist

- [x] README documents the public workflow. (pass)
- [x] License is present. (pass)
- [x] Schema files are present. (pass)
- [x] Checked example outputs are present. (pass)
- [x] Agent skill file is present. (pass)
- [x] Version fields agree. (pass)
- [x] Validation commands are listed or passing. (pass)

## Three-Version Roadmap

### 0.27.x: Release manifest hardening

- Keep release-manifest, package-audit, schema-inventory, and artifact-validation aligned.
- Use release notes drafts and post-release checks for deterministic public release preparation.

### 0.28.x: Static documentation export

- Publish docs-export HTML alongside JSON and Markdown artifacts without JavaScript or external assets.
- Keep command maps, release notes, safety caveats, and local artifact links sourced from checked outputs.

### 0.29.x: Final release hardening

- Converge generated release artifacts deterministically before publishing examples.
- Keep schema validation, docs export, package audit, selfcheck, README, and agent skill guidance aligned.

## Provenance

- command: asset-hub
- input_dir: examples/outputs
- live_market_data: False
- private_context: False
- readme: README.md
- shell_out: False
