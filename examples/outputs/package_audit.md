# Package Audit

- Package: leveraged-etp-risk-lab
- Version: 0.15.0
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
| version_consistency | metadata | pass | version fields agree at 0.15.0 |
| test_commands | validation | pass | test commands listed |

## Test Commands

| Command | Status |
| --- | --- |
| `python -m unittest discover -s tests` | not_run |
| `python scripts/selfcheck.py` | not_run |
| `python -m leveraged_etp_risk_lab package-audit --format json` | not_run |
| `python -m leveraged_etp_risk_lab gallery-index --format json` | not_run |
| `python -m leveraged_etp_risk_lab glossary-list --format json` | not_run |
| `python -m leveraged_etp_risk_lab explain-term daily_reset --format json` | not_run |
| `python -m leveraged_etp_risk_lab factsheet-check --product examples/fixtures/leveraged_nasdaq_3x.json --factsheet-file examples/fixtures/factsheet_note.txt --format json` | not_run |
