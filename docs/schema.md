# Data Schema

Simulation and exposure schemas are versioned as `0.2`. The user-facing pretrade plan packet is versioned as `0.3`. The product template gallery is versioned as `0.4`. Run comparison and run ledger metadata outputs are versioned as `0.5`. Thesis impact outputs are versioned as `0.6`. The market regime gallery is versioned as `0.7`. Position size plans are versioned as `0.8`. Stress matrix outputs are versioned as `0.9`. Thesis watchlist outputs are versioned as `0.10`. Package audit outputs are versioned as `0.11`. Public demo story outputs are versioned as `0.12`. Public gallery index outputs are versioned as `0.13`. Leveraged product glossary outputs are versioned as `0.14`. Product factsheet checklist outputs are versioned as `0.15`. Schemas are intentionally small enough to edit by hand.

## Product

Product files are JSON objects with these fields:

- `name`: display name.
- `ticker`: generic or listed ticker label.
- `underlying`: underlying reference asset.
- `leverage`: daily leverage factor, such as `3` or `2`.
- `annual_fee`: decimal annual fee, such as `0.0095` for 0.95%.
- `currency`: optional, defaults to `USD`.
- `reset_frequency`: optional, defaults to `daily`.
- `notes`: optional plain-text notes.

The `template-export` command writes product JSON in this same shape, without gallery-only fields such as risk notes or use cases.

## Product Template Gallery

The `template-list` command returns a gallery object with:

- `schema_version`: fixed as `0.4`.
- `document_type`: fixed as `template_gallery`.
- `templates`: deterministic list of built-in product templates.

Each template contains the product fields above plus:

- `id`: stable template identifier used by `template-export --template`.
- `risk_notes`: generic risk notes for the template.
- `use_cases`: generic educational planning use cases.

Built-in template identifiers are:

- `generic-2x-long-equity`
- `generic-3x-long-index`
- `generic--2x-inverse-index`
- `generic-2x-single-stock`

## Market Regime Gallery

The `regime-list` command returns a gallery object with:

- `schema_version`: fixed as `0.7`.
- `document_type`: fixed as `regime_gallery`.
- `regimes`: deterministic list of built-in market regimes.

Each regime contains:

- `id`: stable regime identifier used by `regime-export --regime`.
- `name`: display name.
- `description`: short plain-language regime description.
- `default_days`: default number of rows exported by `regime-export`.
- `tags`: generic metadata tags.
- `risk_notes`: generic risk notes for the regime.
- `use_cases`: generic educational planning use cases.
- `sample_path`: one cycle of deterministic `day`, `label`, and `underlying_return` rows.

Built-in regime identifiers are:

- `trend_up`
- `trend_down`
- `chop`
- `gap_down`
- `rebound`
- `volatility_cluster`

The `regime-export` command writes a selected regime as path CSV. Passing `--days` overrides the regime default and repeats the sample path cycle as needed.

## Leveraged Product Glossary

The `glossary-list` command returns an educational glossary object with:

- `schema_version`: fixed as `0.14`.
- `document_type`: fixed as `glossary`.
- `not_investment_advice`: explicit language stating the glossary is education, not advice.
- `summary`: glossary term count.
- `terms`: deterministic list of built-in glossary terms.
- `provenance`: command metadata.

Each term contains:

- `id`: stable identifier used by `explain-term`.
- `term`: display label.
- `plain_language`: short educational definition.
- `why_it_matters`: scenario-planning relevance.
- `example`: generic example with no live prices or recommendations.
- `related_terms`: related built-in term identifiers.

Built-in term identifiers are:

- `daily_reset`
- `path_decay`
- `volatility_decay`
- `leverage_factor`
- `stop_loss_band`
- `take_profit_band`
- `gap_risk`
- `iNAV`
- `premium_discount`
- `max_loss_budget`

The `explain-term` command emits one selected term as JSON or Markdown with the same educational and not-investment-advice framing. Glossary commands do not read live market data, workflow files, private context, environment variables, or command history.

## Product Factsheet Checklist

The `factsheet-check` command reads a product JSON file and an optional plain-text factsheet note. It does not fetch live market data, workflow files, private context, environment variables, or command history.

Factsheet checklist output contains:

- `schema_version`: fixed as `0.15`.
- `document_type`: fixed as `factsheet_check`.
- `not_investment_advice`: explicit language stating the checklist is not advice, a recommendation, or a suitability determination.
- `inputs`: display-safe product and factsheet path labels.
- `product`: product name and ticker from the product JSON where present.
- `summary`: total checks plus pass, review, and missing counts.
- `checks`: deterministic field checks for issuer, exchange, underlying, leverage factor, daily reset wording, fee, currency, liquidity/spread placeholder, iNAV, and premium/discount.
- `missing_fields`: checklist field ids not found in either input.
- `provenance`: command inputs used to build the checklist.

The liquidity/spread item is a review placeholder because the package does not fetch current bid-ask spreads, depth, or average daily volume. Fields can be satisfied by explicit product JSON keys or by matching plain-language factsheet text.

## Path

Path files are CSV files with:

- `day`: integer day number.
- `label`: scenario label.
- `underlying_return`: decimal daily return, such as `-0.025` for -2.5%.

The `generate-scenario` command writes deterministic CSV paths in this shape for `trend`, `chop`, `crash`, and `rebound` scenarios. The `regime-export` command writes the same CSV shape from the built-in market regime library.

## Portfolio Manifest

Portfolio manifest files are JSON objects with:

- `name`: display name.
- `base_currency`: optional, defaults to `USD`.
- `positions`: non-empty list of position objects.

Each position contains:

- `id`: optional position identifier.
- `product_fixture`: product JSON path. Relative paths are resolved from the manifest directory first.
- `path_fixture`: path CSV path. Relative paths are resolved from the manifest directory first.
- `notional`: positive starting notional value.
- `stop_loss`: optional decimal stop-loss band.
- `take_profit`: optional decimal take-profit band.

The aliases `product` and `path` are accepted for `product_fixture` and `path_fixture`.

## Simulation Output

Simulation output contains:

- `product`: normalized product terms.
- `inputs`: initial NAV, day count, and risk bands.
- `summary`: ending values, returns, path decay, and estimated fee drag.
- `band_events`: first stop-loss or take-profit events as modeled NAV crosses bands.
- `warnings`: deterministic risk warnings.
- `path`: per-day modeled values.

## Exposure Report Output

Exposure reports contain:

- `portfolio`: manifest name and base currency.
- `summary`: starting value, aggregate ending value, portfolio return, starting-notional weighted exposure, and worst drawdown approximation.
- `positions`: per-position notional, leverage, weighted exposure, ending value, return, risk bands, and value path.
- `portfolio_path`: aggregate modeled daily portfolio value.
- `stop_events`: stop-loss and take-profit events with position identifiers.
- `warnings`: portfolio-level and deduplicated simulation warnings.

## Pretrade Plan Packet

Pretrade plan packets contain:

- `document_type`: fixed as `pretrade_plan`.
- `not_investment_advice`: explicit language stating the packet is not advice, a recommendation, or a suitability determination.
- `product`: normalized product terms copied from the simulation.
- `scenario`: day count, ending ETP NAV, modeled returns, and path decay.
- `risk_bands`: stop-loss and take-profit percentages plus modeled band events.
- `budget`: user-supplied maximum loss budget and product currency.
- `thesis`: optional thesis text from `--thesis-file` and/or `--thesis-text`.
- `assumptions`: deterministic planning assumptions used by the command.
- `checklist`: selected checklist profile and checklist items.
- `warnings`: deterministic risk warnings.
- `provenance`: command inputs used to build the packet.

## Position Size Plan

The `position-size` command reads either a product/path pair or a generated pretrade-plan JSON file. It requires `--account-value` and exactly one of `--risk-budget-pct` or `--max-loss-budget`. The optional `--stop-loss` overrides any stop-loss in the source input.

Position size output contains:

- `schema_version`: fixed as `0.8`.
- `document_type`: fixed as `position_size_plan`.
- `not_investment_advice`: explicit language stating the planner is not advice, a recommendation, or a suitability determination.
- `product`: normalized product terms copied from the simulation or pretrade plan.
- `inputs`: account value, maximum loss budget, risk budget percentage, stop-loss percentage, loss basis, and currency.
- `recommendation`: recommended notional, max-shares placeholder, modeled loss at stop, modeled loss as an account percentage, and exposure multiple.
- `scenario`: scenario metrics used to contextualize the sizing plan.
- `checklist`: deterministic review items before using the notional figure.
- `warnings`: deterministic risk warnings.
- `provenance`: command inputs used to build the plan.

The `max_shares` field is always `null` because the core package does not fetch live prices or model execution prices. Use `recommended_notional` divided by an intended execution price outside this model.

## Stress Matrix

The `stress-matrix` command reads one product JSON file and runs it against the built-in market regime paths. With no `--regime` flags it uses every built-in regime; repeated `--regime` flags restrict and order the matrix rows. Optional `--stop-loss` and `--take-profit` bands are applied to each regime simulation.

Stress matrix output contains:

- `schema_version`: fixed as `0.9`.
- `document_type`: fixed as `stress_matrix`.
- `not_investment_advice`: explicit language stating the matrix is not advice, a recommendation, or a suitability determination.
- `product`: normalized product terms copied from the product JSON.
- `inputs`: product path label, initial NAV, selected regimes, and risk bands.
- `rows`: per-regime return (`return_pct`, also exposed as `etp_return_pct`), path decay, worst drawdown, stop/take event count, stop/take event labels, and warning count.
- `warnings`: deduplicated warnings observed across the matrix simulations.
- `provenance`: command inputs used to build the matrix.

Worst drawdown is calculated from the modeled ETP NAV path using the starting NAV as the initial peak. Stop events are modeled end-of-day risk band crossings and are not execution guarantees.

## Run Comparison

The `compare-runs` command reads two JSON outputs generated by `simulate`, `pretrade-plan`, or `exposure-report`. It does not modify either input.

Comparison output contains:

- `schema_version`: fixed as `0.5`.
- `document_type`: fixed as `run_comparison`.
- `inputs`: display-safe input path labels as provided on the command line, with absolute paths reduced to filenames.
- `base` and `candidate`: detected document type, source schema version, display label, extracted metrics, and warning count.
- `deltas`: candidate-minus-base deltas for return percentage, path decay versus a simple multiple, and weighted exposure where those metrics exist in both inputs.
- `deltas.warnings`: deterministic sorted warnings added, warnings removed, and unchanged warning count.

Metric extraction is intentionally narrow:

- Simulation outputs use `summary.etp_return_pct` and `summary.path_decay_vs_simple_multiple`.
- Pretrade plans use `scenario.etp_return_pct` and `scenario.path_decay_vs_simple_multiple`.
- Exposure reports use `summary.return_pct` and `summary.weighted_exposure`.

Missing metrics are represented as `null` in JSON and `n/a` in Markdown.

## Run Ledger

The `run-ledger` command appends one JSON object per artifact to a JSONL ledger. It records deterministic metadata only and does not embed artifact contents, timestamps, environment variables, command history, or absolute local paths.

Each ledger row contains:

- `schema_version`: fixed as `0.5`.
- `document_type`: fixed as `run_ledger_entry`.
- `artifact_name`: filename only.
- `artifact_type`: detected output type for JSON reports, or a generic file status.
- `artifact_schema_version`: schema version when detected from a JSON object.
- `bytes`: artifact byte length.
- `sha256`: SHA-256 digest of the artifact bytes.

## Thesis Impact

The `thesis-impact` command reads a Markdown thesis file and one or more generated JSON artifacts from `simulate`, `pretrade-plan`, `exposure-report`, or `compare-runs`. It does not modify the input artifacts and does not write timestamps, environment variables, command history, or absolute local paths.

Thesis impact output contains:

- `schema_version`: fixed as `0.6`.
- `document_type`: fixed as `thesis_impact`.
- `inputs`: display-safe thesis and artifact path labels.
- `thesis`: extracted claim objects from Markdown paragraphs or bullet lines.
- `artifacts`: detected artifact type, source schema version, display label, extracted metrics, and warning count.
- `claim_mappings`: deterministic mapping from each claim to observed metrics, related warnings, status, and follow-up checklist items.
- `warnings`: deduplicated warnings from input artifacts.
- `action_checklist`: deduplicated claim-level action checklist.
- `provenance`: command inputs used to build the mapping.

The claim mapping is intentionally heuristic and narrow. It links return-oriented claims to return metrics, decay or choppy-path claims to path-decay metrics, and exposure or leverage claims to weighted exposure when available. Missing metrics are omitted from the per-claim observed metrics list.

## Thesis Watchlist

The `watchlist-build` command reads one thesis-impact JSON output and one stress-matrix JSON output. It does not modify either input and does not write timestamps, environment variables, command history, or absolute local paths.

Watchlist output contains:

- `schema_version`: fixed as `0.10`.
- `document_type`: fixed as `watchlist`.
- `not_investment_advice`: explicit language stating the watchlist is not advice, a recommendation, or a suitability determination.
- `inputs`: display-safe thesis-impact and stress-matrix path labels.
- `summary`: total entry count and severity counts.
- `entries`: claim and regime-trigger ledger entries with title, severity, status, trigger text, metrics, warnings, next review questions, and source artifact references.
- `provenance`: command inputs used to build the watchlist.

Claim severity is based on thesis-impact mapping status and related warnings. Regime-trigger severity is based on stress-matrix return, worst drawdown, path decay versus a simple multiple, and stop/take event counts. The scoring is deterministic and intended for review prioritization only.

## Package Audit

The `package-audit` command emits a JSON or Markdown package-readiness checklist. By default it lists validation commands without running them. Passing `--run-tests` executes those commands and records pass/fail status.

Package audit output contains:

- `schema_version`: fixed as `0.11`.
- `document_type`: fixed as `package_audit`.
- `package`: package name, version, and dependency list.
- `summary`: ready flag plus passed and failed check counts.
- `checks`: checklist items for README, license, schemas, examples, skill file, no workflow files, public hygiene, zero dependencies, version consistency, and test command readiness.
- `test_commands`: deterministic command arrays plus status and return code.

The public hygiene check looks for private terms, machine-local paths, secret-like key assignments, and repository-hosting asset placeholders. Audit output does not include timestamps, environment variables, command history, or absolute local paths.

## Public Demo Story

The `demo-story` command reads existing demo output JSON files from an input directory. It expects `stress_matrix.json`, `watchlist.json`, `package_audit.json`, and `pretrade_plan.json`. It does not rerun simulations and does not read workflow files, environment variables, command history, live market data, or private context.

## Public Gallery Index

The `gallery-index` command reads public demo artifacts from an input directory, defaulting to `examples/outputs`. It emits JSON or Markdown grouped by workflow stage: `fixtures`, `plans`, `sizing`, `stress`, `thesis/watchlist`, `audit/story`, and `dashboard`. It skips `gallery_index.json` and `gallery_index.md` so the index can be regenerated deterministically.

Gallery index output contains:

- `schema_version`: fixed as `0.13`.
- `document_type`: fixed as `gallery_index`.
- `input_dir`: display-safe input directory label.
- `summary`: stage count, artifact count, and total bytes.
- `stages`: ordered stage groups with artifact metadata and a stage-level suggested next command.
- `stages.artifacts`: filename, display-safe path, stage, format, detected document type, detected schema version, byte count, and artifact-level suggested next command.
- `provenance`: command inputs used to build the index.

The index records metadata only. It does not embed artifact contents, timestamps, environment variables, command history, absolute local paths, workflow files, live prices, or private context.

Demo story output contains:

- `schema_version`: fixed as `0.12`.
- `document_type`: fixed as `demo_story`.
- `not_investment_advice`: explicit language carried from the pretrade-plan artifact.
- `inputs`: display-safe labels for the four source demo artifacts.
- `sections.problem`: concise public framing for the daily-reset leverage issue.
- `sections.workflow`: ordered walkthrough of the demo workflow.
- `sections.commands`: reproducible public CLI commands.
- `sections.key_outputs`: concise summaries and metrics from the source artifacts.
- `sections.safety_caveats`: deterministic safety caveats and selected warning text.
- `sections.next_extension_ideas`: generic public roadmap ideas.
- `provenance`: command and input directory label used to build the story.

The Markdown format renders the same sections for public README-style walkthroughs.

## Static Dashboard

The `static-dashboard` output is a self-contained HTML file, not a JSON schema. It contains inline CSS, no JavaScript, summary cards, a positions table, band events, warnings, and command provenance. It can be rendered from a portfolio manifest or from JSON files generated by `demo-bundle`.
