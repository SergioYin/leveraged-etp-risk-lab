# Package Audit

- Package: leveraged-etp-risk-lab
- Version: 0.29.0
- Ready: yes
- Checks: 10 passed, 0 failed

## Checklist

| Check | Category | Status | Message |
| --- | --- | --- | --- |
| readme | documentation | pass | all required files present |
| license | metadata | pass | all required files present |
| schemas | schemas | pass | all required files present |
| examples | examples | pass | all required files present |
| skill_file | skills | pass | all required files present |
| no_workflows | hygiene | pass | no workflow files found |
| no_private_terms | hygiene | pass | no private terms, local paths, or secret-like values found |
| zero_dependencies | metadata | pass | runtime dependency list is empty |
| version_consistency | metadata | pass | version fields agree at 0.29.0 |
| test_commands | validation | pass | test commands listed |

## Test Commands

| Command | Status |
| --- | --- |
| `python -m unittest discover -s tests` | not_run |
| `python scripts/selfcheck.py` | not_run |
| `python -m leveraged_etp_risk_lab package-audit --format json` | not_run |
| `python -m leveraged_etp_risk_lab gallery-index --format json` | not_run |
| `python -m leveraged_etp_risk_lab asset-hub --format json` | not_run |
| `python -m leveraged_etp_risk_lab schema-inventory --format json` | not_run |
| `python -m leveraged_etp_risk_lab artifact-validate --format json` | not_run |
| `python -m leveraged_etp_risk_lab release-manifest --format json --no-git` | not_run |
| `python -m leveraged_etp_risk_lab docs-export --format json` | not_run |
| `python -m leveraged_etp_risk_lab glossary-list --format json` | not_run |
| `python -m leveraged_etp_risk_lab explain-term daily_reset --format json` | not_run |
| `python -m leveraged_etp_risk_lab factsheet-check --product examples/fixtures/leveraged_nasdaq_3x.json --factsheet-file examples/fixtures/factsheet_note.txt --format json` | not_run |
| `python -m leveraged_etp_risk_lab risk-profile --format json` | not_run |
| `python -m leveraged_etp_risk_lab recipe-run --recipe examples/fixtures/recipe_thesis_review.json --format json` | not_run |
| `python -m leveraged_etp_risk_lab report-card --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/position_size.json --artifact examples/outputs/stress_matrix.json --format json` | not_run |
| `python -m leveraged_etp_risk_lab sensitivity-grid --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss none,0.15 --take-profit none,0.20 --format json` | not_run |
| `python -m leveraged_etp_risk_lab portfolio-sensitivity --manifest examples/fixtures/portfolio_manifest.json --stop-loss none,0.15 --take-profit none,0.20 --format json` | not_run |
| `python -m leveraged_etp_risk_lab thesis-dashboard-data --recipe-run examples/outputs/recipe_run.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --sensitivity-grid examples/outputs/sensitivity_grid.json --format json` | not_run |
| `python -m leveraged_etp_risk_lab memo-draft --recipe-run examples/outputs/recipe_run.json --thesis-dashboard-data examples/outputs/thesis_dashboard_data.json --report-card examples/outputs/report_card.json --factsheet-check examples/outputs/factsheet_check.json --format json` | not_run |
| `python -m leveraged_etp_risk_lab memo-review --memo examples/outputs/investment_memo.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --audit-trail examples/outputs/audit_trail.json --format json` | not_run |
| `python -m leveraged_etp_risk_lab cycle-init --memo examples/outputs/investment_memo.json --watchlist examples/outputs/watchlist.json --report-card examples/outputs/report_card.json --sensitivity-grid examples/outputs/sensitivity_grid.json --format json` | not_run |
| `python -m leveraged_etp_risk_lab cycle-update --cycle-state examples/outputs/cycle_state.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --audit-trail examples/outputs/audit_trail.json --format json` | not_run |
| `python -m leveraged_etp_risk_lab guardrail-policy --policy default --format json` | not_run |
| `python -m leveraged_etp_risk_lab guardrail-check --policy examples/outputs/guardrail_policy.json --portfolio-sensitivity examples/outputs/portfolio_sensitivity.json --position-size examples/outputs/position_size.json --investment-memo examples/outputs/investment_memo.json --cycle-update examples/outputs/cycle_update.json --format json` | not_run |
| `python -m leveraged_etp_risk_lab order-ticket --guardrail-check examples/outputs/guardrail_check.json --investment-memo examples/outputs/investment_memo.json --position-size examples/outputs/position_size.json --factsheet-check examples/outputs/factsheet_check.json --thesis-dashboard-data examples/outputs/thesis_dashboard_data.json --format json` | not_run |
| `python -m leveraged_etp_risk_lab order-review --order-ticket examples/outputs/order_ticket.json --guardrail-check examples/outputs/guardrail_check.json --cycle-update examples/outputs/cycle_update.json --audit-trail examples/outputs/audit_trail.json --format json` | not_run |
| `python -m leveraged_etp_risk_lab audit-trail --ledger examples/outputs/run_ledger.jsonl --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/stress_matrix.json --format json` | not_run |
