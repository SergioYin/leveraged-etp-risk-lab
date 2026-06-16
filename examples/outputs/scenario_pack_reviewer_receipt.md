# Scenario Pack Reviewer Receipt

**Not investment advice:** This scenario pack is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## Summary

- Fixture inputs: 6
- Source inputs: 9
- Generated artifacts: 8
- Hash algorithm: sha256
- Live market data: False
- Broker execution: False
- Trading enabled: False
- Personalized recommendations: False

## Regeneration

- demo_bundle_command: `python -m leveraged_etp_risk_lab demo-bundle --output-dir examples/outputs`
- scenario_pack_command: `python -m leveraged_etp_risk_lab scenario-pack --input-dir examples/outputs --fixtures-dir examples/fixtures --output-dir examples/outputs --format markdown`
- receipt_command: `python -m leveraged_etp_risk_lab scenario-pack-reviewer-receipt --input-dir examples/outputs --fixtures-dir examples/fixtures --artifact-dir examples/outputs --output-dir examples/outputs --format markdown`
- validation_command: `python -m leveraged_etp_risk_lab artifact-validate examples/outputs/scenario_pack_reviewer_receipt.json examples/outputs/scenario_pack.json examples/outputs/daily_reset_path_decay.json examples/outputs/drawdown_risk.json examples/outputs/pretrade_guardrails.json --format markdown`

## Reviewer Checks

- Confirm every fixture path is under examples/fixtures or the supplied fixtures directory.
- Confirm every generated artifact path is under examples/outputs or the supplied artifact directory.
- Compare SHA-256 hashes after regeneration before reviewing the scenario-pack narrative.
- Verify safety boundaries remain false for live market data, broker execution, trading, and personalized recommendations.

## Fixture Inputs

| Path | Kind | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| examples/fixtures/leveraged_nasdaq_3x.json | json | 275 | `a4f63ef24a1282198e65cda178946b42fdfa0182165607fe86bfd60f92e0cd8f` |
| examples/fixtures/single_stock_2x.json | json | 282 | `fbcd054ad34a4b97b42c8bf9e3b3c4b180f16e49b193c928ae03eeeb07e3bbc2` |
| examples/fixtures/nasdaq_chop_path.csv | csv | 153 | `9a3ebd3e2fd9bbfa7545d16570c36c3a039d530e435aa5939eddd513d156cf79` |
| examples/fixtures/single_stock_gap_path.csv | csv | 161 | `d01514fd8e06f8ce62e23fe0657e33e527a99b3354d5e9eff971d4005d50a838` |
| examples/fixtures/portfolio_manifest.json | json | 536 | `be6ed3d6d32f4b14b713beb1e8b7576dc75ef9f301efbaf4f36ff744128dfbdf` |
| examples/fixtures/thesis_note.md | md | 421 | `0cec7a6990f71726205f8e2ac9c507ce7782f252d4592e5092c1c4fdeb825b85` |

## Source Inputs

| Path | Kind | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| examples/outputs/leveraged_nasdaq_3x.json | json | 2782 | `fec4c6c6c83dc18d76579831a83f024506a2983ffdfb0c9f7a2c305561dda48a` |
| examples/outputs/single_stock_2x.json | json | 2539 | `8d87b4439e5ce51026b9cc5139f4860460f033a32ffcbe7f033a9a8f78f90a9f` |
| examples/outputs/pretrade_plan.json | json | 3460 | `3632930e9b4f6c91c35158bbd19e41f7ea5f98be90fdfda747512cf6702a30f6` |
| examples/outputs/position_size.json | json | 2630 | `e858c5ccc946ab87c7b926859fca2cb863013cda3b48b7af3e8085ab379bf940` |
| examples/outputs/stress_matrix.json | json | 3894 | `a53e51a4e83cd511dd25b4180b099ad4a70ab36742838b5db260520502d31c3f` |
| examples/outputs/portfolio_sensitivity.json | json | 31150 | `f87f726abab68709f90de09c75570888b96604d981882b1ebd06ac0f51454f07` |
| examples/outputs/guardrail_check.json | json | 5525 | `f3ffc62fe1af1941cbd60e5ae38801ad5ecfb8eaa86777f04a75cc301ab744ab` |
| examples/outputs/order_review.json | json | 2548 | `63130d3e268e8171d890e745792848cfe9399fa97479bfee6505401e940eb4c7` |
| examples/outputs/compare_runs.json | json | 961 | `245621f9ace03d0bc48244e2b87348afb99db14185b2541a6b757e7cbe77de32` |

## Generated Artifacts

| Path | Kind | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| examples/outputs/scenario_pack.json | json | 8198 | `c322a9c73a3b24433388dc729644f569ff426e4150557b1bd60bc3836b24fee0` |
| examples/outputs/scenario_pack.md | md | 4679 | `93b47354841d3fa67a97d8216dc29b961fcbd462891cad3a34765428f334b000` |
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

## Provenance

- artifact_dir: examples/outputs
- broker_execution: False
- command: scenario-pack-reviewer-receipt
- fixtures_dir: examples/fixtures
- input_dir: examples/outputs
- live_market_data: False
- personalized_recommendations: False
- private_context: False
- shell_out: False
- trading_enabled: False
- workflow_files_read: False
