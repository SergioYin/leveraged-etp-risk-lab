# Public Demo Story

**Not investment advice:** This decision packet is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## Problem

Daily-reset leveraged ETPs can diverge from a simple leverage multiple over multi-day paths. The public demo shows a generic product, deterministic paths, explicit risk bands, and review artifacts without using live prices or private context.

## Workflow

- Start from generic product and path fixtures.
- Build a pretrade plan with thesis text, stop/take bands, a loss budget, and checklist items.
- Run the same product across built-in market regimes with stress-matrix.
- Convert thesis and regime results into a watchlist of review triggers.
- Run package-audit to confirm public sharing hygiene, schemas, examples, and zero dependencies.

## Commands

### pretrade-plan

```bash
python -m leveraged_etp_risk_lab pretrade-plan --product examples/fixtures/leveraged_nasdaq_3x.json --path examples/fixtures/nasdaq_chop_path.csv --thesis-file examples/fixtures/thesis_note.md --max-loss-budget 750 --stop-loss 0.15 --take-profit 0.20 --format markdown
```

### stress-matrix

```bash
python -m leveraged_etp_risk_lab stress-matrix --product examples/fixtures/leveraged_nasdaq_3x.json --stop-loss 0.15 --take-profit 0.20 --format markdown
```

### watchlist-build

```bash
python -m leveraged_etp_risk_lab watchlist-build --thesis-impact examples/outputs/thesis_impact.json --stress-matrix examples/outputs/stress_matrix.json --format markdown
```

### package-audit

```bash
python -m leveraged_etp_risk_lab package-audit --format markdown
```

### demo-story

```bash
python -m leveraged_etp_risk_lab demo-story --input-dir examples/outputs --format markdown
```

## Key Outputs

- **pretrade_plan.json:** NDAQ3X modeled over 6 days returns 0.6088% with path decay -0.602755.
- **stress_matrix.json:** 6 regimes modeled; weakest return is gap_down at -48.8504%.
- **watchlist.json:** 8 watchlist entries, 1 critical and 3 high severity.
- **package_audit.json:** Package audit ready=True with 10 passed and 0 failed checks.

## Safety Caveats

- This decision packet is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.
- The demo uses deterministic fixtures, not forecasts or live market data.
- Stop-loss and take-profit bands are planning levels, not guaranteed execution prices.
- Position sizing and watchlist severity are review aids, not recommendations.
- The package intentionally avoids workflow files, secrets, live prices, and private context.
- Daily reset leverage means multi-day returns can differ materially from the underlying return times leverage.
- Scenario output is not investment advice and does not predict future returns.

## Next Extension Ideas

- Add more generic regime paths for rate-shock, overnight-gap, and prolonged-chop cases.
- Add optional user-supplied execution-price columns while keeping the core package dependency-free.
- Add a static public gallery page that links the JSON, Markdown, dashboard, and demo-story artifacts.
- Extend package-audit with schema example coverage checks for each public output type.

## Provenance

- command: demo-story
- input_dir: examples/outputs
