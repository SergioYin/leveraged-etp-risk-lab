# Public Gallery Index

- Schema version: 0.13
- Input directory: examples/outputs
- Artifacts: 80
- Bytes: 617556

## fixtures

- Artifacts: 21
- Suggested next command: `python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --format markdown`

| Artifact | Format | Document type | Schema version | Bytes | Suggested next command |
| --- | --- | --- | --- | --- | --- |
| examples/outputs/checklist.md | md | n/a | n/a | 718 | `python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --format markdown` |
| examples/outputs/glossary.json | json | glossary | 0.14 | 6496 | `python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --format markdown` |
| examples/outputs/glossary.md | md | glossary | 0.14 | 5341 | `python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --format markdown` |
| examples/outputs/leveraged_nasdaq_3x.json | json | simulation_output | 0.2 | 2782 | `python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --format markdown` |
| examples/outputs/leveraged_nasdaq_3x.md | md | simulation_output | 0.2 | 1426 | `python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --format markdown` |
| examples/outputs/portfolio_exposure.json | json | exposure_report | 0.2 | 3097 | `python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --format markdown` |
| examples/outputs/portfolio_exposure.md | md | exposure_report | 0.2 | 1430 | `python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --format markdown` |
| examples/outputs/regime_chop.csv | csv | n/a | n/a | 317 | `python -m leveraged_etp_risk_lab regime-export --regime volatility_cluster --output volatility_cluster_path.csv` |
| examples/outputs/regime_gallery.json | json | regime_gallery | 0.7 | 7916 | `python -m leveraged_etp_risk_lab regime-export --regime volatility_cluster --output volatility_cluster_path.csv` |
| examples/outputs/regime_gallery.md | md | regime_gallery | 0.7 | 4525 | `python -m leveraged_etp_risk_lab regime-export --regime volatility_cluster --output volatility_cluster_path.csv` |
| examples/outputs/regime_gap_down.csv | csv | n/a | n/a | 258 | `python -m leveraged_etp_risk_lab regime-export --regime volatility_cluster --output volatility_cluster_path.csv` |
| examples/outputs/regime_rebound.csv | csv | n/a | n/a | 302 | `python -m leveraged_etp_risk_lab regime-export --regime volatility_cluster --output volatility_cluster_path.csv` |
| examples/outputs/regime_trend_down.csv | csv | n/a | n/a | 364 | `python -m leveraged_etp_risk_lab regime-export --regime volatility_cluster --output volatility_cluster_path.csv` |
| examples/outputs/regime_trend_up.csv | csv | n/a | n/a | 368 | `python -m leveraged_etp_risk_lab regime-export --regime volatility_cluster --output volatility_cluster_path.csv` |
| examples/outputs/regime_volatility_cluster.csv | csv | n/a | n/a | 366 | `python -m leveraged_etp_risk_lab regime-export --regime volatility_cluster --output volatility_cluster_path.csv` |
| examples/outputs/risk_profiles.json | json | risk_profile_rules | 0.16 | 6498 | `python -m leveraged_etp_risk_lab risk-profile --format markdown` |
| examples/outputs/risk_profiles.md | md | risk_profile_rules | 0.16 | 4978 | `python -m leveraged_etp_risk_lab risk-profile --format markdown` |
| examples/outputs/single_stock_2x.json | json | simulation_output | 0.2 | 2539 | `python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --format markdown` |
| examples/outputs/single_stock_2x.md | md | simulation_output | 0.2 | 1372 | `python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --format markdown` |
| examples/outputs/template_gallery.json | json | template_gallery | 0.4 | 3751 | `python -m leveraged_etp_risk_lab template-export --template generic-3x-long-index --output generic_index_3x.json` |
| examples/outputs/template_gallery.md | md | template_gallery | 0.4 | 2751 | `python -m leveraged_etp_risk_lab template-export --template generic-3x-long-index --output generic_index_3x.json` |

## plans

- Artifacts: 9
- Suggested next command: `python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015 --format markdown`

| Artifact | Format | Document type | Schema version | Bytes | Suggested next command |
| --- | --- | --- | --- | --- | --- |
| examples/outputs/compare_runs.json | json | run_comparison | 0.5 | 961 | `python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015 --format markdown` |
| examples/outputs/compare_runs.md | md | run_comparison | 0.5 | 408 | `python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015 --format markdown` |
| examples/outputs/pretrade_plan.json | json | pretrade_plan | 0.3 | 3460 | `python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015` |
| examples/outputs/pretrade_plan.md | md | pretrade_plan | 0.3 | 3090 | `python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015` |
| examples/outputs/recipe_run.json | json | recipe_run | 0.17 | 40281 | `python -m leveraged_etp_risk_lab recipe-run --recipe examples/fixtures/recipe_thesis_review.json --format markdown` |
| examples/outputs/recipe_run.md | md | recipe_run | 0.17 | 1965 | `python -m leveraged_etp_risk_lab recipe-run --recipe examples/fixtures/recipe_thesis_review.json --format markdown` |
| examples/outputs/report_card.json | json | report_card | 0.18 | 16254 | `python -m leveraged_etp_risk_lab report-card --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/position_size.json --artifact examples/outputs/stress_matrix.json --format markdown` |
| examples/outputs/report_card.md | md | report_card | 0.18 | 4259 | `python -m leveraged_etp_risk_lab report-card --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/position_size.json --artifact examples/outputs/stress_matrix.json --format markdown` |
| examples/outputs/run_ledger.jsonl | jsonl | run_ledger | 0.5 | 4813 | `python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015 --format markdown` |

## sizing

- Artifacts: 2
- Suggested next command: `python -m leveraged_etp_risk_lab stress-matrix --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss 0.15 --take-profit 0.20 --format markdown`

| Artifact | Format | Document type | Schema version | Bytes | Suggested next command |
| --- | --- | --- | --- | --- | --- |
| examples/outputs/position_size.json | json | position_size_plan | 0.8 | 2630 | `python -m leveraged_etp_risk_lab stress-matrix --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss 0.15 --take-profit 0.20` |
| examples/outputs/position_size.md | md | position_size_plan | 0.8 | 2279 | `python -m leveraged_etp_risk_lab stress-matrix --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss 0.15 --take-profit 0.20` |

## stress

- Artifacts: 6
- Suggested next command: `python -m leveraged_etp_risk_lab thesis-impact --thesis-file examples/fixtures/thesis_note.md --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/stress_matrix.json --format markdown`

| Artifact | Format | Document type | Schema version | Bytes | Suggested next command |
| --- | --- | --- | --- | --- | --- |
| examples/outputs/portfolio_sensitivity.json | json | portfolio_sensitivity | 0.20 | 31150 | `python -m leveraged_etp_risk_lab portfolio-sensitivity --manifest examples/fixtures/portfolio_manifest.json --format markdown` |
| examples/outputs/portfolio_sensitivity.md | md | portfolio_sensitivity | 0.20 | 1870 | `python -m leveraged_etp_risk_lab portfolio-sensitivity --manifest examples/fixtures/portfolio_manifest.json --format markdown` |
| examples/outputs/sensitivity_grid.json | json | sensitivity_grid | 0.19 | 75105 | `python -m leveraged_etp_risk_lab report-card --artifact examples/outputs/sensitivity_grid.json --format markdown` |
| examples/outputs/sensitivity_grid.md | md | sensitivity_grid | 0.19 | 3962 | `python -m leveraged_etp_risk_lab report-card --artifact examples/outputs/sensitivity_grid.json --format markdown` |
| examples/outputs/stress_matrix.json | json | stress_matrix | 0.9 | 3894 | `python -m leveraged_etp_risk_lab watchlist-build --thesis-impact examples/outputs/thesis_impact.json --stress-matrix examples/outputs/stress_matrix.json` |
| examples/outputs/stress_matrix.md | md | stress_matrix | 0.9 | 1957 | `python -m leveraged_etp_risk_lab watchlist-build --thesis-impact examples/outputs/thesis_impact.json --stress-matrix examples/outputs/stress_matrix.json` |

## thesis/watchlist

- Artifacts: 4
- Suggested next command: `python -m leveraged_etp_risk_lab demo-story --input-dir examples/outputs --format markdown`

| Artifact | Format | Document type | Schema version | Bytes | Suggested next command |
| --- | --- | --- | --- | --- | --- |
| examples/outputs/thesis_impact.json | json | thesis_impact | 0.6 | 8001 | `python -m leveraged_etp_risk_lab watchlist-build --thesis-impact examples/outputs/thesis_impact.json --stress-matrix examples/outputs/stress_matrix.json` |
| examples/outputs/thesis_impact.md | md | thesis_impact | 0.6 | 4851 | `python -m leveraged_etp_risk_lab watchlist-build --thesis-impact examples/outputs/thesis_impact.json --stress-matrix examples/outputs/stress_matrix.json` |
| examples/outputs/watchlist.json | json | watchlist | 0.10 | 15069 | `python -m leveraged_etp_risk_lab demo-story --input-dir examples/outputs --format markdown` |
| examples/outputs/watchlist.md | md | watchlist | 0.10 | 9699 | `python -m leveraged_etp_risk_lab demo-story --input-dir examples/outputs --format markdown` |

## audit/story

- Artifacts: 10
- Suggested next command: `python -m leveraged_etp_risk_lab static-dashboard --input-dir examples/outputs --output examples/outputs/dashboard.html`

| Artifact | Format | Document type | Schema version | Bytes | Suggested next command |
| --- | --- | --- | --- | --- | --- |
| examples/outputs/asset_hub.json | json | asset_hub | 0.25 | 17425 | `python -m leveraged_etp_risk_lab asset-hub --input-dir examples/outputs --format markdown` |
| examples/outputs/asset_hub.md | md | asset_hub | 0.25 | 11973 | `python -m leveraged_etp_risk_lab asset-hub --input-dir examples/outputs --format markdown` |
| examples/outputs/audit_trail.json | json | audit_trail | 0.20 | 19322 | `python -m leveraged_etp_risk_lab audit-trail --ledger examples/outputs/run_ledger.jsonl --artifact examples/outputs/pretrade_plan.json --format markdown` |
| examples/outputs/audit_trail.md | md | audit_trail | 0.20 | 3442 | `python -m leveraged_etp_risk_lab audit-trail --ledger examples/outputs/run_ledger.jsonl --artifact examples/outputs/pretrade_plan.json --format markdown` |
| examples/outputs/demo_story.json | json | demo_story | 0.12 | 14357 | `python -m leveraged_etp_risk_lab gallery-index --input-dir examples/outputs --format markdown` |
| examples/outputs/demo_story.md | md | demo_story | 0.12 | 9015 | `python -m leveraged_etp_risk_lab gallery-index --input-dir examples/outputs --format markdown` |
| examples/outputs/factsheet_check.json | json | factsheet_check | 0.15 | 3534 | `python -m leveraged_etp_risk_lab factsheet-check --product examples/fixtures/leveraged_nasdaq_3x.json --factsheet-file examples/fixtures/factsheet_note.txt --format markdown` |
| examples/outputs/factsheet_check.md | md | factsheet_check | 0.15 | 1174 | `python -m leveraged_etp_risk_lab factsheet-check --product examples/fixtures/leveraged_nasdaq_3x.json --factsheet-file examples/fixtures/factsheet_note.txt --format markdown` |
| examples/outputs/package_audit.json | json | package_audit | 0.11 | 29200 | `python -m leveraged_etp_risk_lab gallery-index --input-dir examples/outputs --format markdown` |
| examples/outputs/package_audit.md | md | package_audit | 0.11 | 5371 | `python -m leveraged_etp_risk_lab gallery-index --input-dir examples/outputs --format markdown` |

## dashboard

- Artifacts: 19
- Suggested next command: `python -m leveraged_etp_risk_lab package-audit --format markdown`

| Artifact | Format | Document type | Schema version | Bytes | Suggested next command |
| --- | --- | --- | --- | --- | --- |
| examples/outputs/cycle_state.json | json | cycle_state | 0.22 | 9527 | `python -m leveraged_etp_risk_lab cycle-update --cycle-state examples/outputs/cycle_state.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --audit-trail examples/outputs/audit_trail.json --format markdown` |
| examples/outputs/cycle_state.md | md | cycle_state | 0.22 | 3271 | `python -m leveraged_etp_risk_lab cycle-update --cycle-state examples/outputs/cycle_state.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --audit-trail examples/outputs/audit_trail.json --format markdown` |
| examples/outputs/cycle_update.json | json | cycle_update | 0.22 | 2967 | `python -m leveraged_etp_risk_lab cycle-init --memo examples/outputs/investment_memo.json --watchlist examples/outputs/watchlist.json --report-card examples/outputs/report_card.json --sensitivity-grid examples/outputs/sensitivity_grid.json --format markdown` |
| examples/outputs/cycle_update.md | md | cycle_update | 0.22 | 1435 | `python -m leveraged_etp_risk_lab cycle-init --memo examples/outputs/investment_memo.json --watchlist examples/outputs/watchlist.json --report-card examples/outputs/report_card.json --sensitivity-grid examples/outputs/sensitivity_grid.json --format markdown` |
| examples/outputs/dashboard.html | html | n/a | n/a | 3536 | `python -m leveraged_etp_risk_lab gallery-index --input-dir examples/outputs --format markdown` |
| examples/outputs/guardrail_check.json | json | guardrail_check | 0.23 | 5525 | `python -m leveraged_etp_risk_lab order-ticket --guardrail-check examples/outputs/guardrail_check.json --investment-memo examples/outputs/investment_memo.json --position-size examples/outputs/position_size.json --factsheet-check examples/outputs/factsheet_check.json --thesis-dashboard-data examples/outputs/thesis_dashboard_data.json --format markdown` |
| examples/outputs/guardrail_check.md | md | guardrail_check | 0.23 | 2207 | `python -m leveraged_etp_risk_lab order-ticket --guardrail-check examples/outputs/guardrail_check.json --investment-memo examples/outputs/investment_memo.json --position-size examples/outputs/position_size.json --factsheet-check examples/outputs/factsheet_check.json --thesis-dashboard-data examples/outputs/thesis_dashboard_data.json --format markdown` |
| examples/outputs/guardrail_policy.json | json | guardrail_policy | 0.23 | 1191 | `python -m leveraged_etp_risk_lab guardrail-check --policy examples/outputs/guardrail_policy.json --portfolio-sensitivity examples/outputs/portfolio_sensitivity.json --position-size examples/outputs/position_size.json --investment-memo examples/outputs/investment_memo.json --cycle-update examples/outputs/cycle_update.json --format markdown` |
| examples/outputs/guardrail_policy.md | md | guardrail_policy | 0.23 | 961 | `python -m leveraged_etp_risk_lab guardrail-check --policy examples/outputs/guardrail_policy.json --portfolio-sensitivity examples/outputs/portfolio_sensitivity.json --position-size examples/outputs/position_size.json --investment-memo examples/outputs/investment_memo.json --cycle-update examples/outputs/cycle_update.json --format markdown` |
| examples/outputs/investment_memo.json | json | investment_memo_packet | 0.21 | 10963 | `python -m leveraged_etp_risk_lab memo-draft --recipe-run examples/outputs/recipe_run.json --thesis-dashboard-data examples/outputs/thesis_dashboard_data.json --report-card examples/outputs/report_card.json --factsheet-check examples/outputs/factsheet_check.json --format markdown` |
| examples/outputs/investment_memo.md | md | investment_memo_packet | 0.21 | 4262 | `python -m leveraged_etp_risk_lab memo-draft --recipe-run examples/outputs/recipe_run.json --thesis-dashboard-data examples/outputs/thesis_dashboard_data.json --report-card examples/outputs/report_card.json --factsheet-check examples/outputs/factsheet_check.json --format markdown` |
| examples/outputs/investment_memo_review.json | json | investment_memo_review | 0.21 | 3877 | `python -m leveraged_etp_risk_lab memo-review --memo examples/outputs/investment_memo.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --audit-trail examples/outputs/audit_trail.json --format markdown` |
| examples/outputs/investment_memo_review.md | md | investment_memo_review | 0.21 | 2477 | `python -m leveraged_etp_risk_lab memo-review --memo examples/outputs/investment_memo.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --audit-trail examples/outputs/audit_trail.json --format markdown` |
| examples/outputs/order_review.json | json | order_review | 0.24 | 2548 | `python -m leveraged_etp_risk_lab guardrail-policy --policy conservative --format markdown` |
| examples/outputs/order_review.md | md | order_review | 0.24 | 1414 | `python -m leveraged_etp_risk_lab guardrail-policy --policy conservative --format markdown` |
| examples/outputs/order_ticket.json | json | order_ticket | 0.24 | 7380 | `python -m leveraged_etp_risk_lab order-review --order-ticket examples/outputs/order_ticket.json --guardrail-check examples/outputs/guardrail_check.json --cycle-update examples/outputs/cycle_update.json --audit-trail examples/outputs/audit_trail.json --format markdown` |
| examples/outputs/order_ticket.md | md | order_ticket | 0.24 | 3555 | `python -m leveraged_etp_risk_lab order-review --order-ticket examples/outputs/order_ticket.json --guardrail-check examples/outputs/guardrail_check.json --cycle-update examples/outputs/cycle_update.json --audit-trail examples/outputs/audit_trail.json --format markdown` |
| examples/outputs/thesis_dashboard_data.json | json | thesis_dashboard_data | 0.20 | 6625 | `python -m leveraged_etp_risk_lab thesis-dashboard-data --recipe-run examples/outputs/recipe_run.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --sensitivity-grid examples/outputs/sensitivity_grid.json --format markdown` |
| examples/outputs/thesis_dashboard_data.md | md | thesis_dashboard_data | 0.20 | 2658 | `python -m leveraged_etp_risk_lab thesis-dashboard-data --recipe-run examples/outputs/recipe_run.json --report-card examples/outputs/report_card.json --watchlist examples/outputs/watchlist.json --sensitivity-grid examples/outputs/sensitivity_grid.json --format markdown` |

## validation

- Artifacts: 9
- Suggested next command: `python -m leveraged_etp_risk_lab artifact-validate --format markdown`

| Artifact | Format | Document type | Schema version | Bytes | Suggested next command |
| --- | --- | --- | --- | --- | --- |
| examples/outputs/artifact_validation.json | json | artifact_validation | 0.26 | 9802 | `python -m leveraged_etp_risk_lab artifact-validate --format markdown` |
| examples/outputs/artifact_validation.md | md | artifact_validation | 0.26 | 4366 | `python -m leveraged_etp_risk_lab artifact-validate --format markdown` |
| examples/outputs/docs_export.html | html | docs_export | 0.29 | 27577 | `python -m leveraged_etp_risk_lab docs-export --input-dir examples/outputs --output examples/outputs/docs_export.html` |
| examples/outputs/docs_export.json | json | docs_export | 0.29 | 25504 | `python -m leveraged_etp_risk_lab docs-export --input-dir examples/outputs --output examples/outputs/docs_export.html` |
| examples/outputs/docs_export.md | md | docs_export | 0.29 | 16674 | `python -m leveraged_etp_risk_lab docs-export --input-dir examples/outputs --output examples/outputs/docs_export.html` |
| examples/outputs/release_manifest.json | json | release_manifest | 0.29 | 9265 | `python -m leveraged_etp_risk_lab release-manifest --input-dir examples/outputs --format markdown` |
| examples/outputs/release_manifest.md | md | release_manifest | 0.29 | 4148 | `python -m leveraged_etp_risk_lab release-manifest --input-dir examples/outputs --format markdown` |
| examples/outputs/schema_inventory.json | json | schema_inventory | 0.26 | 24375 | `python -m leveraged_etp_risk_lab artifact-validate --format markdown` |
| examples/outputs/schema_inventory.md | md | schema_inventory | 0.26 | 11100 | `python -m leveraged_etp_risk_lab artifact-validate --format markdown` |

## Provenance

- command: gallery-index
- input_dir: examples/outputs
