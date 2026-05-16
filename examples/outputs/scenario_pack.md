# New User Scenario Pack

**Not investment advice:** This scenario pack is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## Summary

- Cases: 3
- Source artifacts: 15
- Live market data: False
- Broker execution: False

## Case Studies

| Case | Focus | Primary metric | Output |
| --- | --- | --- | --- |
| Daily Reset Path Decay | daily_reset_path_decay | nasdaq_underlying_return_pct=0.4038 | daily_reset_path_decay.md |
| Drawdown Risk Under Regime Stress | drawdown_risk | worst_regime=gap_down | drawdown_risk.md |
| Pretrade Guardrails Before An Order | pretrade_guardrails | pretrade_loss_budget=750.0 | pretrade_guardrails.md |

## Integration Notes

### portfolio-risk-compass

- Complement: Scenario-pack outputs provide deterministic stress narratives and case-study metrics that can support a portfolio risk review as evidence for path decay, drawdown, and guardrail checks.
- Handoff artifacts: scenario_pack.json, daily_reset_path_decay.json, drawdown_risk.json, pretrade_guardrails.json
- Dependency boundary: No import, API call, shared storage, live-data feed, broker connection, or runtime dependency is required; another system can read or ignore these static files independently.
- Public context: Uses only checked-in fixtures and generated public examples; no private portfolio context is embedded.

### invest-thesis-ledger

- Complement: Scenario-pack case studies can be attached to thesis records as reproducible evidence for thesis pressure tests, invalidation checks, and pretrade review notes.
- Handoff artifacts: scenario_pack.md, daily_reset_path_decay.md, drawdown_risk.md, pretrade_guardrails.md
- Dependency boundary: No dependency, ledger schema change, plugin, workflow read, command history read, or bidirectional sync is assumed; the notes are portable references, not a required integration.
- Public context: Keeps examples generic and educational, with no account, broker, suitability, or private thesis data.


## New User Evidence

### Exact Commands

- Regenerate the deterministic demo inputs used by the pack.
  `python -m leveraged_etp_risk_lab demo-bundle --output-dir examples/outputs`
- Regenerate the new-user scenario pack and case-study outputs.
  `python -m leveraged_etp_risk_lab scenario-pack --input-dir examples/outputs --fixtures-dir examples/fixtures --output-dir examples/outputs --format markdown`
- Validate the scenario-pack artifacts against local schemas.
  `python -m leveraged_etp_risk_lab artifact-validate examples/outputs/scenario_pack.json examples/outputs/daily_reset_path_decay.json examples/outputs/drawdown_risk.json examples/outputs/pretrade_guardrails.json --format markdown`

### Artifact Links

- [Scenario pack JSON](scenario_pack.json) (`examples/outputs/scenario_pack.json`)
- [Scenario pack Markdown](scenario_pack.md) (`examples/outputs/scenario_pack.md`)

### Safety Boundaries

- Uses checked-in fixtures and generated local examples only.
- Does not read live market data, private context, workflow files, environment variables, or command history.
- Does not place trades, contact brokers, determine suitability, or recommend buying, selling, or holding any product.
- Treats position sizing and guardrail outputs as educational review aids, not instructions.

## Warnings

- Scenario packs are deterministic educational artifacts and do not recommend trades.
- Daily reset, gap risk, liquidity, borrow, tax, and execution effects can differ from these local examples.
- Pretrade guardrails are review gates, not suitability determinations or broker instructions.

## Source Artifacts

- examples/outputs/leveraged_nasdaq_3x.json (json, sha256=fec4c6c6c83d)
- examples/outputs/single_stock_2x.json (json, sha256=8d87b4439e5c)
- examples/outputs/pretrade_plan.json (json, sha256=3632930e9b4f)
- examples/outputs/position_size.json (json, sha256=e858c5ccc946)
- examples/outputs/stress_matrix.json (json, sha256=a53e51a4e83c)
- examples/outputs/portfolio_sensitivity.json (json, sha256=f87f726abab6)
- examples/outputs/guardrail_check.json (json, sha256=f3ffc62fe1af)
- examples/outputs/order_review.json (json, sha256=63130d3e268e)
- examples/outputs/compare_runs.json (json, sha256=245621f9ace0)
- examples/fixtures/leveraged_nasdaq_3x.json (json, sha256=a4f63ef24a12)
- examples/fixtures/single_stock_2x.json (json, sha256=fbcd054ad34a)
- examples/fixtures/nasdaq_chop_path.csv (csv, sha256=9a3ebd3e2fd9)
- examples/fixtures/single_stock_gap_path.csv (csv, sha256=d01514fd8e06)
- examples/fixtures/portfolio_manifest.json (json, sha256=be6ed3d6d32f)
- examples/fixtures/thesis_note.md (md, sha256=0cec7a6990f7)
