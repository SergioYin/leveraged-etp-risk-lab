# Product Factsheet Checklist

- Schema version: 0.15
- Product: Generic 3x Nasdaq Daily Reset ETP
- Ticker: NDAQ3X
- Ready for review: yes
- Checks: 9 passed, 1 review, 0 missing

## Checklist

| Field | Status | Source | Value |
| --- | --- | --- | --- |
| Issuer | pass | factsheet_text | Generic Education Issuer. |
| Exchange | pass | factsheet_text | Example Exchange. |
| Underlying | pass | product_json | Nasdaq-100 reference index |
| Leverage factor | pass | product_json | 3 |
| Daily reset wording | pass | product_json | reset_frequency=daily |
| Fee | pass | product_json | 0.0095 |
| Currency | pass | product_json | USD |
| Liquidity/spread placeholder | review | factsheet_text | placeholder: verify current liquidity and bid-ask spread before use |
| iNAV field | pass | factsheet_text | review the public intraday indicative value field or ticker before use. |
| Premium/discount field | pass | factsheet_text | review issuer premium/discount history before use. |

## Missing Fields

- None

## Notes

- This factsheet checklist is for educational product-term review only. It is not investment advice, a recommendation, or a suitability determination.
