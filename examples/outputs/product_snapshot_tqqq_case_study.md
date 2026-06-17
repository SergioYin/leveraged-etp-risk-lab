# TQQQ Daily-Target Product Snapshot

**Not investment advice:** This static product snapshot is for scenario planning and education only. It is not investment advice, a recommendation, or a suitability determination.

## Product Snapshot

- Snapshot id: tqqq-daily-target-source-snapshot
- Snapshot date: 2026-06-17
- Product: ProShares UltraPro QQQ (TQQQ)
- Issuer: ProShares
- Underlying: Nasdaq-100 Index
- Daily target: Three times the daily performance of the Nasdaq-100 Index before fees and expenses.
- Reset frequency: daily
- Expense ratio note: The fixture does not assert a current fee. Review the current prospectus before using real product terms.

## Case Study

- Reviewer question: What should a reviewer check before using a 3x daily Nasdaq-100 product in a multi-day scenario demo?
- Plain answer: Confirm that the product target is daily, then compare the modeled multi-day path with a simple three-times index move so path dependency is visible.
- Demo fixture: examples/fixtures/leveraged_nasdaq_3x.json

### Learning Points

- A daily target is not the same as a guaranteed multi-day multiple.
- Volatile or alternating paths can make compounded returns diverge from a simple multiple.
- A public reviewer can reproduce the local demo without live prices, broker access, or personalized advice.

## Source Attribution

- SEC Investor.gov leveraged and inverse ETF bulletin: Leveraged and inverse ETFs commonly reset daily, and longer-period results can differ significantly from the stated multiple, especially in volatile markets. (https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-alerts/sec)
- FINRA Non-Traditional ETFs FAQ: FINRA explains that daily reset and compounding can make longer-horizon results differ from a leveraged or inverse fund's objective. (https://www.finra.org/rules-guidance/key-topics/etf/non-traditional-etf-faq)
- ProShares UltraPro QQQ product page: The issuer describes TQQQ as seeking daily investment results, before fees and expenses, corresponding to three times the daily performance of the Nasdaq-100 Index. (https://www.proshares.com/our-etfs/leveraged-and-inverse/tqqq)

## Reviewer Demo Path

- Emit the source-attributed product snapshot as Markdown.
  `python -m leveraged_etp_risk_lab product-snapshot --fixture examples/fixtures/product_snapshot_tqqq_case_study.json --format markdown`
- Regenerate the deterministic local demo bundle including the snapshot artifact.
  `python -m leveraged_etp_risk_lab demo-bundle --output-dir examples/outputs`
- Validate the snapshot artifact against local lightweight schemas.
  `python -m leveraged_etp_risk_lab artifact-validate examples/outputs/product_snapshot_tqqq_case_study.json --format markdown`

## Warnings

- This fixture is static and does not fetch live holdings, prices, assets, spreads, or fees.
- The included ticker is used as an educational case study only.
- Real-world use requires current issuer documents, tax review, liquidity review, and suitability review outside this package.

## Provenance

- broker_execution: False
- command: product-snapshot
- fixture: examples/fixtures/product_snapshot_tqqq_case_study.json
- live_market_data: False
- personalized_recommendations: False
- private_context: False
- shell_out: False
- trading_enabled: False
