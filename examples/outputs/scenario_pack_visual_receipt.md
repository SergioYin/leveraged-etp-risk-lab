# Scenario Pack Visual Receipt

**Not investment advice:** This scenario pack is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## Summary

- Scenario cases: 3
- Demo source artifacts: 9
- Fixture inputs: 6
- Generated artifacts: 10
- Hash algorithm: sha256
- Static HTML: True
- Live market data: False
- Broker execution: False
- Trading enabled: False
- Personalized recommendations: False

## Demo Bundle Bridge

- source_command: `python -m leveraged_etp_risk_lab demo-bundle --output-dir examples/outputs`
- scenario_pack_command: `python -m leveraged_etp_risk_lab scenario-pack --input-dir examples/outputs --fixtures-dir examples/fixtures --output-dir examples/outputs --format markdown`
- visual_receipt_command: `python -m leveraged_etp_risk_lab scenario-pack-visual-receipt --input-dir examples/outputs --fixtures-dir examples/fixtures --artifact-dir examples/outputs --output-dir examples/outputs --format html`
- validation_command: `python -m leveraged_etp_risk_lab artifact-validate examples/outputs/scenario_pack_visual_receipt.json examples/outputs/scenario_pack.json examples/outputs/scenario_pack_reviewer_receipt.json --format markdown`

## Evidence Chain

| Step | Purpose | Artifacts |
| --- | --- | --- |
| demo_bundle_outputs | Deterministic local scenario outputs generated from checked fixtures. | examples/outputs/leveraged_nasdaq_3x.json<br>examples/outputs/single_stock_2x.json<br>examples/outputs/compare_runs.json<br>examples/outputs/stress_matrix.json<br>examples/outputs/portfolio_sensitivity.json<br>examples/outputs/pretrade_plan.json<br>examples/outputs/position_size.json<br>examples/outputs/guardrail_check.json<br>examples/outputs/order_review.json |
| scenario_pack_cases | New-user path-decay, drawdown, and guardrail case studies derived from demo outputs. | examples/outputs/daily_reset_path_decay.json<br>examples/outputs/drawdown_risk.json<br>examples/outputs/pretrade_guardrails.json |
| reviewer_receipt | Hash receipt for fixture inputs, source inputs, generated pack artifacts, and safety boundaries. | examples/outputs/scenario_pack_reviewer_receipt.json |
| visual_receipt | Static visual release-owner checklist tying the pack to demo-bundle regeneration and boundaries. | examples/outputs/scenario_pack_visual_receipt.html |

## Case Cards

| Case | Focus | Primary Metric | JSON | Markdown |
| --- | --- | --- | --- | --- |
| Daily Reset Path Decay | daily_reset_path_decay | case_delta_path_decay_nav_points=-0.050687 | examples/outputs/daily_reset_path_decay.json | examples/outputs/daily_reset_path_decay.md |
| Drawdown Risk Under Regime Stress | drawdown_risk | aggregate_worst_case_loss_pct=48.8518 | examples/outputs/drawdown_risk.json | examples/outputs/drawdown_risk.md |
| Pretrade Guardrails Before An Order | pretrade_guardrails | exposure_multiple=0.3 | examples/outputs/pretrade_guardrails.json | examples/outputs/pretrade_guardrails.md |

## Release Owner Checklist

- [ ] Regenerate the demo bundle before comparing scenario-pack hashes. (demo_bundle_bridge.source_command)
- [ ] Compare scenario-pack and reviewer-receipt SHA-256 hashes before release notes are drafted. (generated_artifacts)
- [ ] Confirm each visual case card points to one scenario JSON artifact and one Markdown artifact. (case_cards)
- [ ] Confirm safety boundaries: live data, broker execution, trading, and personalized recommendations remain disabled. (summary)

## Generated Artifacts

| Path | Kind | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| examples/outputs/scenario_pack.json | json | 8198 | `c322a9c73a3b24433388dc729644f569ff426e4150557b1bd60bc3836b24fee0` |
| examples/outputs/scenario_pack.md | md | 4679 | `93b47354841d3fa67a97d8216dc29b961fcbd462891cad3a34765428f334b000` |
| examples/outputs/scenario_pack_reviewer_receipt.json | json | 7288 | `c180b6e6e8fbfe27245fd93b39a7b389bf77d5ff1f31b855c69fad075dc6ac0b` |
| examples/outputs/scenario_pack_reviewer_receipt.md | md | 5517 | `bb98ee690cdd01750dd84efa5e41c406e19f9fa0c6adcad2b9784867bfbe7637` |
| examples/outputs/daily_reset_path_decay.json | json | 5445 | `1884b8f128f179e3e512453dd90b55309b52c7b86fb6889b9d00a89f299150d4` |
| examples/outputs/daily_reset_path_decay.md | md | 3728 | `23f376279f7bfa797878e965efa8581f390bc08c631343f2549283c87f0fc338` |
| examples/outputs/drawdown_risk.json | json | 4754 | `adf1aeff43c9972e7bddf6c368886038d28092abba01d181f147bd6d9e99f28b` |
| examples/outputs/drawdown_risk.md | md | 3484 | `d07ce063c4d608fc75312f9a1f3e488b8771d44ee668eb14cb949c361b7846bf` |
| examples/outputs/pretrade_guardrails.json | json | 5275 | `f51702702722e6a95f1f43f7225e92c488a68d7bc07d8b7ab1f4be5c56f6f346` |
| examples/outputs/pretrade_guardrails.md | md | 3693 | `e98d4551088e878803cedacccd5aee0c656ef9f72bf7b615d88700a77ba5d285` |

## Safety Boundaries

- No live market data is fetched or required.
- No broker, API, account, order, routing, staging, preview, or execution capability is used.
- No trading instruction, no personalized recommendation, no suitability determination, and no investment advice is produced.
- Receipt hashes cover deterministic local fixtures and generated artifacts only.
- Uses checked-in fixtures and generated local examples only.
- Does not read live market data, private context, workflow files, environment variables, or command history.
- Does not place trades, contact brokers, determine suitability, or recommend buying, selling, or holding any product.
- Treats position sizing and guardrail outputs as educational review aids, not instructions.
- The HTML receipt is static: inline CSS only, no JavaScript, no external assets, and no network calls.
- Release-owner checklist items are review prompts, not trading instructions or approval to place orders.

## Provenance

- artifact_dir: examples/outputs
- broker_execution: False
- command: scenario-pack-visual-receipt
- fixtures_dir: examples/fixtures
- input_dir: examples/outputs
- live_market_data: False
- personalized_recommendations: False
- private_context: False
- shell_out: False
- trading_enabled: False
- workflow_files_read: False
