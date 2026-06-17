# Release Manifest

- Version: 0.30.0
- Status: ready
- Agent skill: `skills/agent/leveraged-etp-risk-lab/SKILL.md`
- Local skill sync: sync after release if you use the local Codex skill copy

## Inputs

| Input | Status | Path | Document type |
| --- | --- | --- | --- |
| artifact_validation | present | examples/outputs/artifact_validation.json | artifact_validation |
| asset_hub | present | examples/outputs/asset_hub.json | asset_hub |
| demo_story | present | examples/outputs/demo_story.json | demo_story |
| gallery_index | present | examples/outputs/gallery_index.json | gallery_index |
| package_audit | present | examples/outputs/package_audit.json | package_audit |
| schema_inventory | present | examples/outputs/schema_inventory.json | schema_inventory |

## Public Artifact Inventory

- Total artifacts: 92
- Total bytes: 704134

| Stage | Artifacts | Key artifacts |
| --- | ---: | --- |
| fixtures | 23 | examples/outputs/checklist.md, examples/outputs/glossary.json, examples/outputs/glossary.md, examples/outputs/leveraged_nasdaq_3x.json, examples/outputs/leveraged_nasdaq_3x.md |
| plans | 9 | examples/outputs/compare_runs.json, examples/outputs/compare_runs.md, examples/outputs/pretrade_plan.json, examples/outputs/pretrade_plan.md, examples/outputs/recipe_run.json |
| sizing | 2 | examples/outputs/position_size.json, examples/outputs/position_size.md |
| stress | 6 | examples/outputs/portfolio_sensitivity.json, examples/outputs/portfolio_sensitivity.md, examples/outputs/sensitivity_grid.json, examples/outputs/sensitivity_grid.md, examples/outputs/stress_matrix.json |
| thesis/watchlist | 4 | examples/outputs/thesis_impact.json, examples/outputs/thesis_impact.md, examples/outputs/watchlist.json, examples/outputs/watchlist.md |
| audit/story | 20 | examples/outputs/asset_hub.json, examples/outputs/asset_hub.md, examples/outputs/audit_trail.json, examples/outputs/audit_trail.md, examples/outputs/daily_reset_path_decay.json |
| dashboard | 19 | examples/outputs/cycle_state.json, examples/outputs/cycle_state.md, examples/outputs/cycle_update.json, examples/outputs/cycle_update.md, examples/outputs/dashboard.html |
| validation | 9 | examples/outputs/artifact_validation.json, examples/outputs/artifact_validation.md, examples/outputs/docs_export.html, examples/outputs/docs_export.json, examples/outputs/docs_export.md |

## Validation Summary

- Package ready: yes
- Artifact validation ready: yes
- Schemas indexed: 43
- Validation issues: 0

## Release Readiness

- pass: All release source artifacts are present
- pass: Package audit is ready
- pass: Artifact validation is ready
- pass: Public artifact inventory is populated
- pass: No live data, workflow, or private context is required

## GitHub Release Notes Draft

## v0.30.0

### Highlights

- Hardens deterministic release artifact generation for package audit, schema inventory, artifact validation, release manifest, and docs export.
- Adds deterministic v0.30 scenario-pack case studies for new users comparing path decay, drawdown risk, and guardrails.
- Carries safety caveats, command map, release notes, and local artifact links from checked public artifacts.
- Publishes 92 public demo artifacts across 8 gallery stages.
- Tracks 43 local schemas and 43 validated artifacts.

### Readiness

- Release status: ready
- Package audit ready: yes
- Artifact validation ready: yes

### Verification

- `python -m unittest discover -s tests`
- `python scripts/selfcheck.py`
- `python -m leveraged_etp_risk_lab docs-export --input-dir examples/outputs --output examples/outputs/docs_export.html`
- `python -m leveraged_etp_risk_lab package-audit --run-tests --format json`

## Post-Release Verification
- [todo] Confirm release tag v0.30.0 points at the intended commit.
- [todo] Confirm JSON and Markdown release_manifest artifacts are attached or linked.
- [todo] Confirm docs/release-manifest.schema.json and docs/docs-export.schema.json are visible in the published package.
- [todo] Run scripts/sync_local_skill.py when a local Codex skill copy should be refreshed.
- [todo] Run version-report, release-manifest, artifact-validate, and package-audit from a clean checkout.
