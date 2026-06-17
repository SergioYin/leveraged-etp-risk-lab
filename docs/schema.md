# Data Schema

Simulation and exposure schemas are versioned as `0.2`. The user-facing pretrade plan packet is versioned as `0.3`. The product template gallery is versioned as `0.4`. Run comparison and run ledger metadata outputs are versioned as `0.5`. Thesis impact outputs are versioned as `0.6`. The market regime gallery is versioned as `0.7`. Position size plans are versioned as `0.8`. Stress matrix outputs are versioned as `0.9`. Thesis watchlist outputs are versioned as `0.10`. Package audit outputs are versioned as `0.11`. Public demo story outputs are versioned as `0.12`. Public gallery index outputs are versioned as `0.13`. Leveraged product glossary outputs are versioned as `0.14`. Product factsheet checklist outputs are versioned as `0.15`. Risk rule profile outputs are versioned as `0.16`. Recipe-run bundles are versioned as `0.17`. Decision-readiness report cards are versioned as `0.18`. Scenario sensitivity grids are versioned as `0.19`. Portfolio sensitivity, thesis dashboard data, and audit trail outputs are versioned as `0.20`. Investment memo and memo review outputs are versioned as `0.21`. Watch cycle state and update outputs are versioned as `0.22`. Allocation guardrail policy and check outputs are versioned as `0.23`. Order ticket and order review outputs are versioned as `0.24`. Public asset hub outputs are versioned as `0.25`. Schema inventory and artifact validation outputs are versioned as `0.26`. Scenario packs, scenario case studies, release manifests, and static docs export packets are versioned as `0.30`. Product snapshot case studies are versioned as `0.31`. Schemas are intentionally small enough to edit by hand.

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

## Product Snapshot Case Study

The `product-snapshot` command reads a static local fixture and emits a source-attributed public reviewer packet. It does not fetch live market data, call issuer APIs, shell out, read private context, or enable broker execution.

Product snapshot case-study output contains:

- `schema_version`: fixed as `0.31`.
- `document_type`: fixed as `product_snapshot_case_study`.
- `not_investment_advice`: explicit language stating the snapshot is not advice, a recommendation, or a suitability determination.
- `product`: static display fields for the case-study product.
- `case_study`: reviewer question, plain-English answer, demo fixture, and learning points.
- `source_attribution`: source names, URLs, access date, and paraphrased claim summaries.
- `reviewer_demo_path`: exact local commands a public reviewer can run.
- `warnings`: static limitations, including no live fees, spreads, prices, holdings, or suitability review.
- `provenance`: command metadata, including `live_market_data: false`, `shell_out: false`, `private_context: false`, `broker_execution: false`, `trading_enabled: false`, and `personalized_recommendations: false`.

## Schema Inventory

The `schema-inventory` command reads local `docs/*.schema.json` files and scans `examples/outputs` for JSON or JSONL artifacts that claim matching `document_type` and `schema_version` values. It does not use external schema libraries, live market data, shell commands, workflow files, private context, or broker execution.

Schema inventory output contains:

- `schema_version`: fixed as `0.26`.
- `document_type`: fixed as `schema_inventory`.
- `summary`: schema count, matched example count, and tracked safety flags.
- `schemas`: sorted schema entries with path, title, document type, schema version, required top-level fields, matching examples, and public safety notes.
- `provenance`: command metadata, including `live_market_data: false`, `shell_out: false`, `private_context: false`, and `broker_execution: false`.

## Artifact Validation

The `artifact-validate` command validates JSON artifacts against the local lightweight schema inventory. With no paths, it checks `examples/outputs/*.json` and `examples/outputs/*.jsonl`; with positional paths, it checks only those files. Validation is deliberately limited to deterministic checks: object shape, local `document_type`, local `schema_version`, required top-level fields, and provenance flags `live_market_data`, `shell_out`, `private_context`, and `broker_execution` when present.

Artifact validation output contains:

- `schema_version`: fixed as `0.26`.
- `document_type`: fixed as `artifact_validation`.
- `summary`: artifact count, pass/fail counts, and readiness boolean.
- `artifacts`: per-artifact document type, schema version, status, issues, and detected provenance safety flags.
- `provenance`: command metadata, including `live_market_data: false`, `shell_out: false`, `private_context: false`, and `broker_execution: false`.

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

## Risk Rule Profiles

The `risk-profile` command emits deterministic profile rules as JSON or Markdown. It does not read live market data, workflow files, private context, environment variables, or command history.

Risk profile output contains:

- `schema_version`: fixed as `0.16`.
- `document_type`: fixed as `risk_profile_rules`.
- `not_investment_advice`: explicit language stating the profiles are not advice, recommendations, or suitability determinations.
- `summary`: emitted profile count and available profile identifiers.
- `profiles`: deterministic risk-rule profile objects.
- `provenance`: command inputs used to build the profile output.

Built-in profile identifiers are:

- `default`
- `conservative`
- `active-trader`
- `thesis-review`

Each profile contains max holding days, a max-account-risk-percent placeholder string, required factsheet fields, required scenario regimes, mandatory checklist questions, and stop/take review defaults. The account-risk field is deliberately a placeholder because the package does not determine suitability or user-specific risk limits.

## Recipe Run

The `recipe-run` command reads a JSON recipe and composes existing library functions without shelling out, writing hidden intermediate files, reading workflow files, using live market data, or loading private context.

Recipe input contains:

- `product`: product JSON path.
- exactly one of `path` or `regime`: primary scenario path CSV or built-in regime id.
- `factsheet_note`: optional plain-text factsheet note.
- `profile`: optional risk profile id, defaulting to `thesis-review`.
- `account_value`: positive account value for sizing context.
- exactly one of `risk_budget_pct` or `max_loss_budget`: loss budget input.
- `stop_loss` and `take_profit`: optional decimal planning bands.
- `stress_regimes`: optional list of built-in regime ids for the stress matrix; omitted means all regimes.
- `thesis_file`: optional Markdown/plain-text thesis note. When present, recipe-run also builds thesis-impact and, when stress output exists, watchlist components.

Recipe-run output contains:

- `schema_version`: fixed as `0.17`.
- `document_type`: fixed as `recipe_run`.
- `not_investment_advice`: explicit language stating the bundle is not advice, a recommendation, or a suitability determination.
- `inputs`: display-safe recipe, product, scenario, factsheet, profile, account value, risk budget, thesis, and stress regime labels.
- `summary`: product ticker, scenario days, scenario return, path decay, recommended notional, component count, and watchlist entry count.
- `workflow`: conceptual command links for the composed commands. These are provenance-style strings; the runner does not shell out.
- `components`: compact summaries of included component artifacts.
- `artifacts`: embedded JSON outputs for factsheet-check, risk-profile, simulation, stress-matrix, position-size, pretrade-plan, thesis-impact, and watchlist where applicable.
- `provenance`: command metadata, including `shell_out: false`.

## Report Card

The `report-card` command reads one or more generated JSON artifacts from simulation, pretrade-plan, position-size, stress-matrix, sensitivity-grid, portfolio-sensitivity, factsheet-check, risk-profile, recipe-run, investment-memo, and investment-memo-review outputs. It does not fetch live market data, shell out, read workflow files, or load private context.

Report-card output contains:

- `schema_version`: fixed as `0.18`.
- `document_type`: fixed as `report_card`.
- `not_investment_advice`: explicit language stating the card is not advice, a recommendation, or a suitability determination.
- `inputs`: display-safe artifact labels.
- `summary`: artifact count, document types, count of strengths, unresolved checks, warnings, and a deterministic decision-ready boolean.
- `artifact_cards`: compact per-artifact metrics, strengths, unresolved checks, and warnings.
- `strengths`: deduplicated cross-artifact positive readiness signals.
- `unresolved_checks`: deduplicated checks still requiring review.
- `warnings`: deduplicated warnings collected from supported artifacts.
- `next_commands`: deterministic CLI commands for follow-up generation or validation.
- `provenance`: command metadata, including `live_market_data: false` and `shell_out: false`.

## Thesis Dashboard Data

The `thesis-dashboard-data` command reads one recipe-run JSON output, one report-card JSON output, one watchlist JSON output, and one sensitivity-grid JSON output. It emits a compact data packet for dashboard renderers without rerunning analysis.

Dashboard packet output contains:

- `schema_version`: fixed as `0.20`.
- `document_type`: fixed as `thesis_dashboard_data`.
- `not_investment_advice`: explicit language stating the packet is not advice, a recommendation, or a suitability determination.
- `inputs`: display-safe labels for the four source artifacts.
- `summary`: product, scenario return, path decay, recommended notional, decision-ready flag, watchlist counts, and worst grid metrics.
- `cards`: compact recipe, readiness, watchlist, and sensitivity cards.
- `warnings`: deduplicated readiness and sensitivity warnings.
- `provenance`: command metadata, including `live_market_data: false` and `shell_out: false`.

## Audit Trail

The `audit-trail` command reads a run-ledger JSONL file and one or more generated artifact files. It recomputes deterministic metadata and compares each artifact with matching ledger rows by filename.

Audit trail output contains:

- `schema_version`: fixed as `0.20`.
- `document_type`: fixed as `audit_trail`.
- `inputs`: display-safe ledger and artifact labels.
- `summary`: ledger row count, artifact count, pass/review counts, and deterministic flag.
- `artifacts`: recomputed artifact filename, display path, detected document type, schema version, byte count, and SHA-256 hash.
- `checklist`: pass/review rows for ledger presence, byte match, and hash match.
- `ledger_rows`: parsed ledger metadata rows.
- `provenance`: command metadata, including `live_market_data: false` and `shell_out: false`.

## Investment Memo

The `memo-draft` command reads `recipe_run`, `thesis_dashboard_data`, `report_card`, and optional `factsheet_check` JSON outputs. It emits a structured Markdown or JSON investment memo packet without fetching live market data, shelling out, reading workflow files, or loading private context.

Memo packet output contains:

- `schema_version`: fixed as `0.21`.
- `document_type`: fixed as `investment_memo_packet`.
- `not_investment_advice`: explicit language stating the memo is not advice, a recommendation, or a suitability determination.
- `inputs`: display-safe labels for the source artifacts.
- `thesis`: thesis text, extracted claims, and decision-ready status.
- `product_terms`: product ticker, terms, currency, and factsheet summary.
- `scenario_evidence`: base-case scenario, stress summary, dashboard metrics, and top watchlist entries.
- `risk_budget`: max loss budget, recommended notional, modeled stop loss, stop/take bands, and exposure multiple.
- `open_checks`: deterministic unresolved report-card and factsheet checks.
- `invalidation_triggers`: deterministic watchlist and readiness triggers that require re-review.
- `warnings`: deduplicated warning text from source artifacts.
- `provenance`: command metadata, including `live_market_data: false` and `shell_out: false`.

The `memo-review` command reads a memo JSON plus latest `report_card`, `watchlist`, and `audit_trail` JSON outputs. It emits a deterministic review checklist with changed risks and next actions.

Memo review output contains:

- `schema_version`: fixed as `0.21`.
- `document_type`: fixed as `investment_memo_review`.
- `not_investment_advice`: explicit language stating the review is not advice, a recommendation, or a suitability determination.
- `inputs`: display-safe labels for the reviewed artifacts.
- `summary`: checklist pass/review counts, changed-risk count, and decision-ready flag.
- `changed_risks`: added, removed, or changed watchlist risks relative to memo invalidation triggers.
- `checklist`: deterministic review items and next actions.
- `next_actions`: deduplicated follow-up actions.
- `provenance`: command metadata, including `live_market_data: false` and `shell_out: false`.

## Watch Cycle

The `cycle-init` command reads an `investment_memo_packet`, `watchlist`, `report_card`, and `sensitivity_grid` JSON output. It emits a persistent watch-cycle state with a deterministic state id derived from baseline artifact hashes. It does not fetch live market data, shell out, read workflow files, or load private context.

Cycle state output contains:

- `schema_version`: fixed as `0.22`.
- `document_type`: fixed as `cycle_state`.
- `not_investment_advice`: explicit language stating the state is not advice, a recommendation, or a suitability determination.
- `state_id`: deterministic id derived from baseline artifact filenames and SHA-256 hashes.
- `inputs`: display-safe labels for the four source artifacts.
- `summary`: watch item, open check, baseline risk, and decision-ready counts.
- `baseline_artifact_hashes`: filename, display path, detected document type, schema version, byte count, and SHA-256 hash for memo, watchlist, report-card, and sensitivity-grid artifacts.
- `baseline_watch_items`: compact watchlist items with id, category, severity, status, title, and trigger text.
- `baseline_risks`: memo invalidation triggers plus high-priority watchlist, sensitivity, and readiness risks.
- `open_checks`: memo and report-card checks with open status.
- `review_cadence`: placeholders for user-set cadence, owner, next review, and expected review inputs.
- `provenance`: command metadata, including `live_market_data: false` and `shell_out: false`.

The `cycle-update` command reads a `cycle_state` JSON plus latest `report_card`, `watchlist`, and `audit_trail` JSON outputs. It compares latest watch items and artifact hashes with the persisted baseline.

Cycle update output contains:

- `schema_version`: fixed as `0.22`.
- `document_type`: fixed as `cycle_update`.
- `not_investment_advice`: explicit language stating the update is not advice, a recommendation, or a suitability determination.
- `state_id`: copied from the cycle state.
- `inputs`: display-safe labels for state and latest artifacts.
- `summary`: added, removed, changed watch items, hash drift, status transition count, and decision-ready flag.
- `watch_items`: added, removed, and changed watch item details.
- `hash_drift`: baseline versus latest/audited byte and SHA-256 comparisons.
- `status_transitions`: watch item, report-card, audit-trail, and hash-drift transition rows.
- `next_review_actions`: deterministic follow-up checklist.
- `provenance`: command metadata, including `live_market_data: false` and `shell_out: false`.

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

## Sensitivity Grid

The `sensitivity-grid` command reads one product JSON file and runs built-in market regimes across grids of leverage multipliers, stop-loss values, and take-profit values. With no leverage grid it defaults to `1x`, `2x`, and `3x`, preserving the sign of an inverse product. Stop-loss and take-profit grids accept repeated flags or comma-separated values; `none` includes an unset planning band.

Sensitivity grid output contains:

- `schema_version`: fixed as `0.19`.
- `document_type`: fixed as `sensitivity_grid`.
- `not_investment_advice`: explicit language stating the grid is not advice, a recommendation, or a suitability determination.
- `product`: normalized product terms copied from the product JSON, including the base leverage.
- `inputs`: product path label, initial NAV, selected regimes, leverage grid, stop-loss grid, and take-profit grid.
- `summary`: worst return, worst path decay, and maximum stop/take event count across all grid combinations.
- `rows`: one row per leverage/stop/take combination with worst return regime, largest drawdown, worst path decay, total stop/take events, and warning count.
- `cells`: per-regime detail rows for every combination.
- `warnings`: deduplicated warnings observed across the grid.
- `provenance`: command inputs plus `live_market_data: false` and `shell_out: false`.

The command is deterministic, uses only built-in regime paths, does not fetch live market data, and does not read workflow files, private context, environment variables, or command history.

## Portfolio Sensitivity

The `portfolio-sensitivity` command reads a portfolio manifest and runs sensitivity-grid style summaries for each position. It uses the same built-in market regimes, leverage grid, stop-loss grid, and take-profit grid semantics as `sensitivity-grid`.

Portfolio sensitivity output contains:

- `schema_version`: fixed as `0.20`.
- `document_type`: fixed as `portfolio_sensitivity`.
- `not_investment_advice`: explicit language stating the packet is not advice, a recommendation, or a suitability determination.
- `portfolio`: manifest name and base currency.
- `inputs`: manifest label, initial NAV, selected regimes, and grid inputs.
- `summary`: position count, starting value, base weighted exposure, aggregate worst-case modeled loss, aggregate worst-case loss percent, aggregate worst-case weighted exposure, and weakest position details.
- `positions`: one object per manifest position with notional, weight, base leverage, weighted exposure, sensitivity summary, worst-case row, and compact grid rows.
- `warnings`: deduplicated warnings from portfolio aggregation and sensitivity grids.
- `provenance`: command metadata, including `live_market_data: false` and `shell_out: false`.

Aggregate worst-case modeled loss sums each position's weakest deterministic grid return against its starting notional. It is a planning metric only and does not model fills, margin, tax, liquidity, or suitability.

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

## Allocation Guardrails

The `guardrail-policy` command emits deterministic `default`, `conservative`, or `aggressive` allocation policies. Policies do not read live market data, workflow files, private context, environment variables, or command history.

Guardrail policy output contains:

- `schema_version`: fixed as `0.23`.
- `document_type`: fixed as `guardrail_policy`.
- `policy_id`: `default`, `conservative`, or `aggressive`.
- `limits`: max leverage exposure, max loss budget percent, and max holding days.
- `required_artifacts`: required report types for the check workflow.
- `review_conditions`: deterministic plain-language review conditions.
- `provenance`: command metadata, including `live_market_data: false` and `shell_out: false`.

The `guardrail-check` command reads one policy JSON plus `portfolio_sensitivity`, `position_size_plan`, `investment_memo_packet`, and `cycle_update` JSON artifacts. It emits hard `fail` results for breached exposure, loss-budget, holding-period, or required-artifact rules. It emits `review` results for open memo checks, memo invalidation triggers, cycle changes, cycle not-ready states, and aggregate modeled portfolio loss over the policy budget.

Guardrail check output contains:

- `schema_version`: fixed as `0.23`.
- `document_type`: fixed as `guardrail_check`.
- `summary`: overall `pass`, `review`, or `fail` plus rule counts.
- `observed`: deterministic metrics extracted from the input artifacts.
- `rules`: all evaluated rules with status, observed value, limit, and action.
- `violated_rules`: only review/fail rules.
- `next_actions`: deduplicated next actions.
- `provenance`: command metadata, including `live_market_data: false` and `shell_out: false`.

## Order Checklist Workflow

The `order-ticket` command reads `guardrail_check`, `investment_memo_packet`, `position_size_plan`, `factsheet_check`, and optional `thesis_dashboard_data` JSON artifacts. It emits a placeholder-only pre-order ticket. It never reads live prices, broker accounts, private context, workflow files, environment variables, or command history, and it never places, stages, routes, previews, or executes broker orders.

Order ticket output contains:

- `schema_version`: fixed as `0.24`.
- `document_type`: fixed as `order_ticket`.
- `summary`: blocked/review/ready status, ticker, max notional, currency, guardrail result, and do-not-trade condition count.
- `product`: compact product terms from memo and sizing artifacts.
- `order_intent`: placeholders for side, order type, time in force, limit price, stop/exit plan, entry window, and notes.
- `sizing`: max notional, max-share placeholder, modeled loss, risk budget percent, and exposure multiple.
- `required_broker_fields`: placeholder broker fields that must be completed outside this package.
- `no_live_price_warning`: explicit warning that no live or delayed market data is read.
- `do_not_trade_if`: deterministic conditions from guardrails, memo checks, factsheet gaps, dashboard readiness, and broker/live-price placeholders.
- `provenance`: command metadata, including `live_market_data: false`, `shell_out: false`, and `broker_execution: false`.

The `order-review` command reads an `order_ticket`, `guardrail_check`, `cycle_update`, and `audit_trail` JSON artifact. It emits a final educational review checklist with `blocked`, `review`, or `ready` status. The review is still not a broker order and does not authorize execution.

Order review output contains:

- `schema_version`: fixed as `0.24`.
- `document_type`: fixed as `order_review`.
- `summary`: blocked/review/ready status, checklist counts, and `broker_execution: false`.
- `checklist`: deterministic rows for ticket status, guardrail status, cycle currency, audit trail, no-live-price warning, and broker-execution disabled provenance.
- `final_notes`: safety reminders that all live broker, price, liquidity, and suitability checks happen outside this package.
- `provenance`: command metadata, including `live_market_data: false`, `shell_out: false`, and `broker_execution: false`.

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

The `demo-story` command reads existing demo output JSON files from an input directory. It expects `stress_matrix.json`, `sensitivity_grid.json`, `watchlist.json`, `package_audit.json`, `pretrade_plan.json`, `report_card.json`, `investment_memo.json`, and `investment_memo_review.json`. It does not rerun simulations and does not read workflow files, environment variables, command history, live market data, or private context.

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

## Public Asset Hub

The `asset-hub` command reads checked public artifacts from an input directory, defaulting to `examples/outputs`. It expects `package_audit.json`, `gallery_index.json`, `demo_story.json`, `order_review.json`, `guardrail_check.json`, and `cycle_update.json`. It also reads the local README title and first description line when available. It does not run tests, rerun simulations, fetch live data, read private context, or shell out.

Asset hub output contains:

- `schema_version`: fixed as `0.25`.
- `document_type`: fixed as `asset_hub`.
- `product_positioning`: GitHub-facing name, version, tagline, audience, and public proof points.
- `command_map`: command names, purposes, and reproducible example commands.
- `demo_artifact_map`: gallery stages, artifact counts, key artifacts, and next commands.
- `readiness_checklist`: readiness rows synthesized from package-audit, guardrail-check, order-review, and cycle-update artifacts.
- `safety_boundaries`: deduplicated public safety boundaries from demo, guardrail, and order-review artifacts.
- `agent_skill_path`: checked-in agent skill path.
- `release_checklist`: public release checks sourced from package-audit.
- `roadmap`: three-version public roadmap.
- `provenance`: command metadata, including `live_market_data: false`, `shell_out: false`, and `private_context: false`.

The Markdown format renders the same sections for a GitHub-facing public asset hub page.

## Scenario Pack

The `scenario-pack` command reads existing local example fixtures and generated reports, then writes Markdown and JSON case-study artifacts. It is designed for new users who need a deterministic walkthrough of daily-reset path decay, drawdown risk, and pretrade guardrails without live market data or broker execution.

Scenario pack output contains:

- `schema_version`: fixed as `0.30`.
- `document_type`: fixed as `scenario_pack`.
- `pack_id`: stable identifier for the new-user pack.
- `summary`: case count, source artifact count, focus areas, and safety booleans.
- `cases`: index rows for the generated case-study JSON and Markdown files.
- `integration_notes`: generic public notes explaining how scenario-pack outputs can complement `portfolio-risk-compass` and `invest-thesis-ledger` as static handoff artifacts without runtime dependencies, private context, workflow reads, or bidirectional sync.
- `cold_user_evidence`: exact reproducibility commands, local artifact links, and explicit safety boundaries.
- `source_artifacts`: local paths, file kinds, sizes, and SHA-256 hashes.
- `warnings`: public safety caveats.
- `provenance`: command metadata, including `live_market_data: false`, `shell_out: false`, `private_context: false`, `broker_execution: false`, and `workflow_files_read: false`.

Scenario case-study output contains:

- `schema_version`: fixed as `0.30`.
- `document_type`: fixed as `scenario_case_study`.
- `case_id`: one of `daily_reset_path_decay`, `drawdown_risk`, or `pretrade_guardrails`.
- `focus_area`: the new-user comparison theme.
- `cold_user_question`: the user-facing question answered by the case.
- `plain_english_answer`: concise explanation sourced from local artifacts.
- `metrics`: deterministic metrics pulled from existing fixture/report outputs.
- `takeaways`: short reading notes for the case.
- `guardrails`: checks to perform before relying on the modeled output.
- `cold_user_evidence`: exact commands, case-specific artifact links, and safety boundaries for new users.
- `source_artifacts`, `warnings`, and `provenance`: local reproducibility and safety metadata.

## Scenario Pack Reviewer Receipt

The `scenario-pack-reviewer-receipt` command writes deterministic JSON and Markdown receipts for cold reviewers. It reads local fixture inputs, generated source inputs, and scenario-pack artifacts, then records paths, byte sizes, SHA-256 hashes, exact regeneration commands, validation commands, and explicit no-live-data/no-trading/no-advice boundaries.

Scenario pack reviewer receipt output contains:

- `schema_version`: fixed as `0.30`.
- `document_type`: fixed as `scenario_pack_reviewer_receipt`.
- `receipt_id`: stable receipt identifier.
- `summary`: fixture input count, source input count, generated artifact count, hash algorithm, and false safety booleans.
- `fixture_inputs`: checked fixture paths, file kinds, byte sizes, and SHA-256 hashes.
- `source_inputs`: generated report inputs used by the scenario pack, with paths and hashes.
- `generated_artifacts`: scenario-pack JSON and Markdown artifact paths and hashes.
- `reviewer_checks`: concise cold-review steps for comparing paths, hashes, and boundaries.
- `regeneration`: exact local demo-bundle, scenario-pack, receipt, and artifact-validation commands.
- `safety_boundaries`: explicit no live market data, no broker/API/account/order access, no trading, no suitability, and no personalized recommendation notes.
- `provenance`: command metadata, including `live_market_data: false`, `shell_out: false`, `private_context: false`, `broker_execution: false`, and `workflow_files_read: false`.

## Release Manifest

The `release-manifest` command reads public local release artifacts from an input directory, defaulting to `examples/outputs`. It looks for `asset_hub.json`, `package_audit.json`, `artifact_validation.json`, `schema_inventory.json`, `demo_story.json`, and `gallery_index.json`. Missing or invalid inputs are recorded in the manifest instead of failing the command. Optional git metadata is included when available; use `--no-git` for deterministic output without repository metadata.

Release manifest output contains:

- `schema_version`: fixed as `0.30`.
- `document_type`: fixed as `release_manifest`.
- `version`: package version intended for release.
- `inputs`: status rows for each optional source artifact.
- `git`: optional commit, short commit, branch, and dirty-state metadata, or an unavailable status.
- `public_artifact_inventory`: stage-level artifact counts and key artifacts sourced from gallery-index or asset-hub data.
- `validation_summary`: package-audit, artifact-validation, and schema-inventory readiness counts.
- `release_readiness`: deterministic pass/review checks for source artifacts, validation, inventory, and safety boundaries.
- `agent_skill_path`: checked-in agent skill path.
- `local_skill_sync_recommendation`: command and recommendation for refreshing a local Codex skill copy.
- `github_release_notes_draft`: Markdown draft for GitHub release notes.
- `post_release_verification_checklist`: release follow-up checks.
- `provenance`: command metadata, including `live_market_data: false`, `private_context: false`, and `workflow_files_read: false`.

The command does not read workflow files, environment variables, command history, live market data, broker accounts, or private context.

## Static Docs Export

The `docs-export` command reads public release and demo artifacts from an input directory, defaulting to `examples/outputs`. It expects `release_manifest.json`, `asset_hub.json`, `demo_story.json`, `gallery_index.json`, `package_audit.json`, and `scenario_pack.json`, then scans sibling Markdown artifacts. It emits a single self-contained static HTML page by default, or JSON/Markdown with `--format`. The HTML contains inline CSS only: no JavaScript, no external assets, no live data, no workflow files, and no private context.

Docs export JSON output contains:

- `schema_version`: fixed as `0.30`.
- `document_type`: fixed as `docs_export`.
- `title`: export page title.
- `summary`: source-artifact count, Markdown artifact count, command count, local-link count, release status, and package-readiness flag.
- `sources`: status rows for the six JSON source artifacts.
- `safety_caveats`: deduplicated safety language from asset-hub and demo-story plus export-level caveats.
- `command_map`: command names, purposes, and examples sourced from asset-hub or demo-story.
- `integration_notes`: optional static handoff notes sourced from scenario-pack for companion-tool documentation.
- `release_notes`: release notes draft sourced from release-manifest.
- `local_artifact_links`: local artifact paths and stage/type metadata for generated examples.
- `markdown_artifacts`: Markdown path, title, and byte metadata.
- `provenance`: command metadata, including `live_market_data: false`, `external_assets: false`, `javascript: false`, `private_context: false`, and `workflow_files_read: false`.

The generated HTML links only to local artifact paths. It deliberately does not embed remote fonts, images, scripts, analytics, workflow metadata, environment variables, timestamps, command history, broker data, live prices, or private context.

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
