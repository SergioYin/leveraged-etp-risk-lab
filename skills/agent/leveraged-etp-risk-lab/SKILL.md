# leveraged-etp-risk-lab Agent Skill

Use this skill when a user asks an agent to inspect, extend, validate, or explain the `leveraged-etp-risk-lab` repository or to run leveraged ETF/ETP daily-reset risk scenarios.

## Trigger Scenarios

- Add or review CLI commands for leveraged ETP scenario analysis.
- Validate product-term fixtures, scenario paths, or deterministic outputs.
- Generate deterministic trend, chop, crash, or rebound scenario paths.
- Aggregate exposure reports from a portfolio manifest.
- Build pretrade decision packets with explicit not-investment-advice language.
- Render static no-JavaScript dashboards from manifests or demo outputs.
- Explain daily reset leverage, fee drag, path decay, stop-loss bands, or take-profit bands.
- Run repository checks before sharing a public package.

## Route

1. Read `README.md`, `docs/schema.md`, and the relevant module in `leveraged_etp_risk_lab/`.
2. Prefer the CLI entry point: `python -m leveraged_etp_risk_lab`.
3. Keep the package dependency-free unless the user explicitly changes the project scope.
4. Keep generated public files generic and free of private names, machine-local paths, and secrets.

## Commands

```bash
python -m leveraged_etp_risk_lab --help
python -m leveraged_etp_risk_lab simulate --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv
python -m leveraged_etp_risk_lab generate-scenario --kind crash --days 10 --output crash_path.csv
python -m leveraged_etp_risk_lab exposure-report --manifest examples/fixtures/portfolio_manifest.json
python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --stop-loss 0.15 --take-profit 0.20
python -m leveraged_etp_risk_lab static-dashboard --manifest examples/fixtures/portfolio_manifest.json --output examples/outputs/dashboard.html
python -m leveraged_etp_risk_lab checklist --profile risk-review
python -m leveraged_etp_risk_lab demo-bundle --output-dir examples/outputs
python -m leveraged_etp_risk_lab selfcheck
python scripts/selfcheck.py
python -m unittest discover -s tests
```

## Validation

- Run `python -m unittest discover -s tests`.
- Run `python scripts/selfcheck.py`.
- Confirm no `.github/workflows` files were added.
- Confirm CLI JSON output is deterministic for fixture inputs.
- Confirm generated scenario CSVs and exposure reports are deterministic for fixture inputs.
- Confirm pretrade plans include not-investment-advice language, assumptions, checklist items, and provenance.
- Confirm static dashboards are self-contained HTML with no JavaScript.

## Safety Boundaries

- Do not present output as investment advice.
- Do not recommend buying, selling, or holding a product.
- Do not treat multi-day leveraged returns as a simple multiple of the underlying.
- Do not add secrets, local paths, private names, or organization-specific messaging references to public files.

## Done Criteria

- CLI commands run through `python -m leveraged_etp_risk_lab`.
- Fixtures and docs match the schema notes.
- Tests and selfcheck pass.
- Public-facing text remains generic and suitable for an open repository.
