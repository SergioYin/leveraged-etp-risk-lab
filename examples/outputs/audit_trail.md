# Audit Trail

- Ledger: examples/outputs/run_ledger.jsonl
- Artifacts: 19
- Ledger rows: 19
- Passed: 19
- Review: 0

## Checklist

| Artifact | Status | Type | Schema | Bytes | SHA-256 |
| --- | --- | --- | --- | --- | --- |
| leveraged_nasdaq_3x.json | pass | simulation_output | 0.2 | 2782 | fec4c6c6c83dc18d76579831a83f024506a2983ffdfb0c9f7a2c305561dda48a |
| single_stock_2x.json | pass | simulation_output | 0.2 | 2539 | 8d87b4439e5ce51026b9cc5139f4860460f033a32ffcbe7f033a9a8f78f90a9f |
| portfolio_exposure.json | pass | exposure_report | 0.2 | 3097 | 150da78ee800a99d6373059d1d99a2883499c3d8ad50f621c0c2e6d676dbc9d7 |
| pretrade_plan.json | pass | pretrade_plan | 0.3 | 3460 | 3632930e9b4f6c91c35158bbd19e41f7ea5f98be90fdfda747512cf6702a30f6 |
| position_size.json | pass | position_size_plan | 0.8 | 2630 | e858c5ccc946ab87c7b926859fca2cb863013cda3b48b7af3e8085ab379bf940 |
| stress_matrix.json | pass | stress_matrix | 0.9 | 3894 | a53e51a4e83cd511dd25b4180b099ad4a70ab36742838b5db260520502d31c3f |
| sensitivity_grid.json | pass | sensitivity_grid | 0.19 | 75105 | 37c2e08ee361260a79c744df8f5d373ab6cee9ec07cf3f97e2cb081270757f0d |
| portfolio_sensitivity.json | pass | portfolio_sensitivity | 0.20 | 31150 | f87f726abab68709f90de09c75570888b96604d981882b1ebd06ac0f51454f07 |
| compare_runs.json | pass | run_comparison | 0.5 | 961 | 245621f9ace03d0bc48244e2b87348afb99db14185b2541a6b757e7cbe77de32 |
| thesis_impact.json | pass | thesis_impact | 0.6 | 8001 | e613582700fe07fd67f4b7f4ea8da670f8df14d5ade8f8cf91371e5f0d9c196e |
| watchlist.json | pass | watchlist | 0.10 | 15069 | 31eb2d3ed67f894ef362ed078845d4db489e3270eebf312aa39951a5d9134aa4 |
| factsheet_check.json | pass | factsheet_check | 0.15 | 3534 | c976a948cbf84ebb77b52da2c386004c58d0b3b6a4e41c0744c2da39cd41561b |
| risk_profiles.json | pass | risk_profile_rules | 0.16 | 6498 | 37cde78aac231af73dfb2c99ebca4bb9f081b41d2cba0bc0e58b8a112a2cb159 |
| recipe_run.json | pass | recipe_run | 0.17 | 40281 | 2d5289be5544204534798993011bfc21c3b719d6decba21f318928bf917590a4 |
| report_card.json | pass | report_card | 0.18 | 16254 | 77e2de589d7bcc779073c6e99affc7d5cee32c524ab2374a02dd1a2b76ce7a76 |
| thesis_dashboard_data.json | pass | thesis_dashboard_data | 0.20 | 6625 | a411d032e5d4e8fcf7a71902d403526d40e6c81783c387577574179424c3e196 |
| investment_memo.json | pass | investment_memo_packet | 0.21 | 10963 | e65fdac470f187a1b38ecc8c67b034364fcbb86f98193f09f35e01767be0dbf7 |
| cycle_state.json | pass | cycle_state | 0.22 | 9527 | eb3a5bc6220f183a2275438a9150630221e3fe1a85deacd5ac358d89f57d625f |
| product_snapshot_tqqq_case_study.json | pass | product_snapshot_case_study | 0.31 | 4205 | 3c4c1635cd73116630f93f2962f3d25c9ad62579160e233e71251bb9a59d14ef |

## Provenance

- artifacts: ['examples/outputs/leveraged_nasdaq_3x.json', 'examples/outputs/single_stock_2x.json', 'examples/outputs/portfolio_exposure.json', 'examples/outputs/pretrade_plan.json', 'examples/outputs/position_size.json', 'examples/outputs/stress_matrix.json', 'examples/outputs/sensitivity_grid.json', 'examples/outputs/portfolio_sensitivity.json', 'examples/outputs/compare_runs.json', 'examples/outputs/thesis_impact.json', 'examples/outputs/watchlist.json', 'examples/outputs/factsheet_check.json', 'examples/outputs/risk_profiles.json', 'examples/outputs/recipe_run.json', 'examples/outputs/report_card.json', 'examples/outputs/thesis_dashboard_data.json', 'examples/outputs/investment_memo.json', 'examples/outputs/cycle_state.json', 'examples/outputs/product_snapshot_tqqq_case_study.json']
- command: audit-trail
- ledger: examples/outputs/run_ledger.jsonl
- live_market_data: False
- shell_out: False
