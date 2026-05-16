# Public Demo Story

**Not investment advice:** This decision packet is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## Problem

Daily-reset leveraged ETPs can diverge from a simple leverage multiple over multi-day paths. The public demo shows a generic product, deterministic paths, explicit risk bands, and review artifacts without using live prices or private context.

## Workflow

- Start from generic product and path fixtures.
- Build a pretrade plan with thesis text, stop/take bands, a loss budget, and checklist items.
- Run the same product across built-in market regimes with stress-matrix.
- Use sensitivity-grid to compare leverage, stop-loss, and take-profit choices across every built-in regime.
- Convert thesis and regime results into a watchlist of review triggers.
- Use recipe-run when one JSON recipe should compose the public workflow into a single bundle.
- Use report-card to condense generated artifacts into strengths, unresolved checks, warnings, and next commands.
- Use memo-draft and memo-review to package the thesis and re-check it against latest public artifacts.
- Use cycle-init and cycle-update to persist a watch cycle, compare watchlist changes, and detect hash drift.
- Use guardrail-policy and guardrail-check to gate allocation artifacts against explicit exposure, loss-budget, holding-period, and review rules.
- Use order-ticket and order-review to create placeholder-only broker checklists without live prices or execution.
- Use schema-inventory and artifact-validate to inspect local schema coverage and validate example JSON artifacts.
- Use release-manifest to assemble artifact inventory, validation status, release notes, skill sync guidance, and post-release checks.
- Use docs-export to render one self-contained static HTML documentation page from local public artifacts.
- Run package-audit to confirm public sharing hygiene, schemas, examples, and zero dependencies.

## Commands

### pretrade-plan

```bash
python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --stop-loss 0.15 --take-profit 0.20 --format markdown
```

### stress-matrix

```bash
python -m leveraged_etp_risk_lab stress-matrix --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss 0.15 --take-profit 0.20 --format markdown
```

### sensitivity-grid

```bash
python -m leveraged_etp_risk_lab sensitivity-grid --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss none,0.15,0.25 --take-profit none,0.20,0.35 --format markdown
```

### watchlist-build

```bash
python -m leveraged_etp_risk_lab watchlist-build --thesis-impact examples/outputs/thesis_impact.json --stress-matrix examples/outputs/stress_matrix.json --format markdown
```

### package-audit

```bash
python -m leveraged_etp_risk_lab package-audit --format markdown
```

### recipe-run

```bash
python -m leveraged_etp_risk_lab recipe-run --recipe examples/fixtures/recipe_thesis_review.json --format markdown
```

### report-card

```bash
python -m leveraged_etp_risk_lab report-card --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/position_size.json --artifact examples/outputs/stress_matrix.json --artifact examples/outputs/factsheet_check.json --format markdown
```

### memo-draft

```bash
python -m leveraged_etp_risk_lab memo-draft --recipe-run examples/outputs/recipe_run.json --thesis-dashboard-data examples/outputs/thesis_dashboard_data.json --report-card examples/outputs/report_card.json --factsheet-check examples/outputs/factsheet_check.json --format markdown
```

### memo-review

```bash
python -m leveraged_etp_risk_lab memo-review --memo examples/outputs/investment_memo.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --audit-trail examples/outputs/audit_trail.json --format markdown
```

### cycle-init

```bash
python -m leveraged_etp_risk_lab cycle-init --memo examples/outputs/investment_memo.json --watchlist examples/outputs/watchlist.json --report-card examples/outputs/report_card.json --sensitivity-grid examples/outputs/sensitivity_grid.json --format markdown
```

### cycle-update

```bash
python -m leveraged_etp_risk_lab cycle-update --cycle-state examples/outputs/cycle_state.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --audit-trail examples/outputs/audit_trail.json --format markdown
```

### guardrail-policy

```bash
python -m leveraged_etp_risk_lab guardrail-policy --policy default --format markdown
```

### guardrail-check

```bash
python -m leveraged_etp_risk_lab guardrail-check --policy examples/outputs/guardrail_policy.json --portfolio-sensitivity examples/outputs/portfolio_sensitivity.json --position-size examples/outputs/position_size.json --investment-memo examples/outputs/investment_memo.json --cycle-update examples/outputs/cycle_update.json --format markdown
```

### order-ticket

```bash
python -m leveraged_etp_risk_lab order-ticket --guardrail-check examples/outputs/guardrail_check.json --investment-memo examples/outputs/investment_memo.json --position-size examples/outputs/position_size.json --factsheet-check examples/outputs/factsheet_check.json --thesis-dashboard-data examples/outputs/thesis_dashboard_data.json --format markdown
```

### order-review

```bash
python -m leveraged_etp_risk_lab order-review --order-ticket examples/outputs/order_ticket.json --guardrail-check examples/outputs/guardrail_check.json --cycle-update examples/outputs/cycle_update.json --audit-trail examples/outputs/audit_trail.json --format markdown
```

### demo-story

```bash
python -m leveraged_etp_risk_lab demo-story --input-dir examples/outputs --format markdown
```

### scenario-pack

```bash
python -m leveraged_etp_risk_lab scenario-pack --input-dir examples/outputs --fixtures-dir examples/fixtures --output-dir examples/outputs --format markdown
```

### schema-inventory

```bash
python -m leveraged_etp_risk_lab schema-inventory --format markdown
```

### artifact-validate

```bash
python -m leveraged_etp_risk_lab artifact-validate --format markdown
```

### release-manifest

```bash
python -m leveraged_etp_risk_lab release-manifest --input-dir examples/outputs --format markdown
```

### docs-export

```bash
python -m leveraged_etp_risk_lab docs-export --input-dir examples/outputs --output examples/outputs/docs_export.html
```

## Key Outputs

- **pretrade_plan.json:** NDAQ3X modeled over 6 days returns 0.6088% with path decay -0.602755.
- **stress_matrix.json:** 6 regimes modeled; weakest return is gap_down at -48.8504%.
- **sensitivity_grid.json:** 27 grid combinations modeled; worst return is -48.8504% in gap_down.
- **watchlist.json:** 8 watchlist entries, 1 critical and 3 high severity.
- **package_audit.json:** Package audit ready=True with 10 passed and 0 failed checks.
- **report_card.json:** Report card decision_ready=False with 8 strengths, 10 unresolved checks, and 10 warnings.
- **investment_memo.json:** Memo packet has 11 open checks and 7 invalidation triggers.
- **investment_memo_review.json:** Memo review found 6 changed risks and 4 review checklist items.
- **cycle_state.json:** Cycle state cycle_c46a3e619fcf75f4 tracks 8 watch items and 11 open checks.
- **cycle_update.json:** Cycle update has 0 hash drift item(s), 0 changed watch item(s), and 1 status transition(s).
- **guardrail_check.json:** Guardrail check result is review with 4 review and 0 fail rule(s).
- **order_ticket.json:** Order ticket status is review with 13 do-not-trade condition(s) and no broker execution.
- **order_review.json:** Order review status is review with 0 blocked and 4 review item(s).

## Safety Caveats

- This decision packet is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.
- The demo uses deterministic fixtures, not forecasts or live market data.
- Stop-loss and take-profit bands are planning levels, not guaranteed execution prices.
- Position sizing and watchlist severity are review aids, not recommendations.
- Order ticket and review outputs are educational checklists, not broker orders.
- The package intentionally avoids workflow files, secrets, live prices, and private context.
- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.

## Next Extension Ideas

- Add more generic regime paths for rate-shock, overnight-gap, and prolonged-chop cases.
- Add optional user-supplied execution-price columns while keeping the core package dependency-free.
- Add a static public gallery page that links the JSON, Markdown, dashboard, and demo-story artifacts.
- Extend package-audit with schema example coverage checks for each public output type.
- Attach release-manifest JSON and Markdown to release notes for reproducible post-release verification.

## Provenance

- command: demo-story
- input_dir: examples/outputs
