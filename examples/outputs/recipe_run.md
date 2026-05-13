# Recipe Run

**Not investment advice:** This recipe bundle is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## Summary

- Product: NDAQ3X
- Scenario days: 6
- Scenario return: 0.6088%
- Path decay vs simple multiple: -0.602755
- Recommended notional: 5000.0
- Watchlist entries: 5

## Conceptual Workflow

- factsheet-check: `factsheet-check --product examples/fixtures/leveraged_nasdaq_3x.json --factsheet-file examples/fixtures/factsheet_note.txt`
- risk-profile: `risk-profile --profile thesis-review`
- simulate: `simulate --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv`
- stress-matrix: `stress-matrix --product examples/fixtures/leveraged_nasdaq_3x.json --regime trend_down --regime chop --regime gap_down`
- position-size: `position-size --pretrade-plan recipe:pretrade_plan`
- pretrade-plan: `pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv`
- thesis-impact: `thesis-impact --thesis-file examples/fixtures/thesis_note.md --artifact recipe:pretrade_plan`
- watchlist-build: `watchlist-build --thesis-impact recipe:thesis_impact --stress-matrix recipe:stress_matrix`

## Components

| Component | Type | Schema | Summary |
| --- | --- | --- | --- |
| factsheet_check | factsheet_check | 0.15 | 9 passed, 1 review, 0 missing |
| risk_profile | risk_profile_rules | 0.16 | 1 profile(s) |
| simulation_output | simulation_output | 0.2 | scenario return 0.6088% |
| stress_matrix | stress_matrix | 0.9 | 3 regimes |
| position_size_plan | position_size_plan | 0.8 | recommended notional 5000.0 |
| pretrade_plan | pretrade_plan | 0.3 | max loss budget 750.0 |
| thesis_impact | thesis_impact | 0.6 | 2 claim(s) |
| watchlist | watchlist | 0.10 | 5 entries |

## Provenance

- command: recipe-run
- recipe: examples/fixtures/recipe_thesis_review.json
- shell_out: False
