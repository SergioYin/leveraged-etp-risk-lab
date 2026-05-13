# Public Gallery Index

- Schema version: 0.13
- Input directory: examples/outputs
- Artifacts: 39
- Bytes: 131257

## fixtures

- Artifacts: 19
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
| examples/outputs/single_stock_2x.json | json | simulation_output | 0.2 | 2539 | `python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --format markdown` |
| examples/outputs/single_stock_2x.md | md | simulation_output | 0.2 | 1372 | `python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --format markdown` |
| examples/outputs/template_gallery.json | json | template_gallery | 0.4 | 3751 | `python -m leveraged_etp_risk_lab template-export --template generic-3x-long-index --output generic_index_3x.json` |
| examples/outputs/template_gallery.md | md | template_gallery | 0.4 | 2751 | `python -m leveraged_etp_risk_lab template-export --template generic-3x-long-index --output generic_index_3x.json` |

## plans

- Artifacts: 5
- Suggested next command: `python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015 --format markdown`

| Artifact | Format | Document type | Schema version | Bytes | Suggested next command |
| --- | --- | --- | --- | --- | --- |
| examples/outputs/compare_runs.json | json | run_comparison | 0.5 | 961 | `python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015 --format markdown` |
| examples/outputs/compare_runs.md | md | run_comparison | 0.5 | 408 | `python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015 --format markdown` |
| examples/outputs/pretrade_plan.json | json | pretrade_plan | 0.3 | 3460 | `python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015` |
| examples/outputs/pretrade_plan.md | md | pretrade_plan | 0.3 | 3090 | `python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015` |
| examples/outputs/run_ledger.jsonl | jsonl | run_ledger | 0.5 | 1868 | `python -m leveraged_etp_risk_lab position-size --pretrade-plan examples/outputs/pretrade_plan.json --account-value 50000 --risk-budget-pct 0.015 --format markdown` |

## sizing

- Artifacts: 2
- Suggested next command: `python -m leveraged_etp_risk_lab stress-matrix --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss 0.15 --take-profit 0.20 --format markdown`

| Artifact | Format | Document type | Schema version | Bytes | Suggested next command |
| --- | --- | --- | --- | --- | --- |
| examples/outputs/position_size.json | json | position_size_plan | 0.8 | 2630 | `python -m leveraged_etp_risk_lab stress-matrix --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss 0.15 --take-profit 0.20` |
| examples/outputs/position_size.md | md | position_size_plan | 0.8 | 2279 | `python -m leveraged_etp_risk_lab stress-matrix --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss 0.15 --take-profit 0.20` |

## stress

- Artifacts: 2
- Suggested next command: `python -m leveraged_etp_risk_lab thesis-impact --thesis-file examples/fixtures/thesis_note.md --artifact examples/outputs/pretrade_plan.json --artifact examples/outputs/stress_matrix.json --format markdown`

| Artifact | Format | Document type | Schema version | Bytes | Suggested next command |
| --- | --- | --- | --- | --- | --- |
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

- Artifacts: 6
- Suggested next command: `python -m leveraged_etp_risk_lab static-dashboard --input-dir examples/outputs --output examples/outputs/dashboard.html`

| Artifact | Format | Document type | Schema version | Bytes | Suggested next command |
| --- | --- | --- | --- | --- | --- |
| examples/outputs/demo_story.json | json | demo_story | 0.12 | 5178 | `python -m leveraged_etp_risk_lab gallery-index --input-dir examples/outputs --format markdown` |
| examples/outputs/demo_story.md | md | demo_story | 0.12 | 3303 | `python -m leveraged_etp_risk_lab gallery-index --input-dir examples/outputs --format markdown` |
| examples/outputs/factsheet_check.json | json | factsheet_check | 0.15 | 3534 | `python -m leveraged_etp_risk_lab factsheet-check --product examples/fixtures/leveraged_nasdaq_3x.json --factsheet-file examples/fixtures/factsheet_note.txt --format markdown` |
| examples/outputs/factsheet_check.md | md | factsheet_check | 0.15 | 1174 | `python -m leveraged_etp_risk_lab factsheet-check --product examples/fixtures/leveraged_nasdaq_3x.json --factsheet-file examples/fixtures/factsheet_note.txt --format markdown` |
| examples/outputs/package_audit.json | json | package_audit | 0.11 | 8727 | `python -m leveraged_etp_risk_lab gallery-index --input-dir examples/outputs --format markdown` |
| examples/outputs/package_audit.md | md | package_audit | 0.11 | 1519 | `python -m leveraged_etp_risk_lab gallery-index --input-dir examples/outputs --format markdown` |

## dashboard

- Artifacts: 1
- Suggested next command: `python -m leveraged_etp_risk_lab package-audit --format markdown`

| Artifact | Format | Document type | Schema version | Bytes | Suggested next command |
| --- | --- | --- | --- | --- | --- |
| examples/outputs/dashboard.html | html | n/a | n/a | 3536 | `python -m leveraged_etp_risk_lab gallery-index --input-dir examples/outputs --format markdown` |

## Provenance

- command: gallery-index
- input_dir: examples/outputs
