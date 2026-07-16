# Cleaning Log

Every change applied by the data-quality stage. Impossible values were quarantined, never silently dropped.

## retail_sales_messy.csv
- Profiled: 930 data rows, 14 columns.
- Removed **10** exact-duplicate rows (930 -> 920).
- Normalized Region aliases/case: **202** rows (W->West, e->East, MW->Midwest, ...).
- Normalized ProductCategory case/whitespace: **144** rows (footwear/'Footwear ' -> Footwear).
- Parsed MM/DD/YYYY dates to ISO: **358** rows.
- Normalized Returned to boolean: **916** rows (Yes/Y/1/TRUE->true, No/N/0/FALSE->false).
- Stripped $/commas from UnitPrice: **41** rows.
- Converted Discount percent strings (15% -> 0.15): **64** rows; blank Discount treated as 0: **94** rows *(assumption)*.
- Blank ShippingCost treated as 0: **86** rows *(assumption; shipping not used in profit math)*.
- Recomputed missing Revenue = UnitPrice*Quantity*(1-Discount): **95** rows.
- Left **18** blank ProductName rows in place (missing, not impossible) — will not match products; flagged as join gap.
- **Quarantined 4** impossible-value rows (negative price, Quantity 999, sentinel Revenue) -> output/quarantine.csv (never dropped).
- **Clean sales rows: 916**.

## retail_products.csv
- 25 rows; clean on profile (unique keys, no dupes/blanks/sentinels). Trimmed whitespace only.

## retail_customers.csv
- 179 rows; clean on profile (unique keys, no dupes/blanks/sentinels). Trimmed whitespace only.

## retail_returns.csv
- 99 rows; clean on profile (unique keys, no dupes/blanks/sentinels). Trimmed whitespace only.


## Model join coverage
- Model spine: 916 clean order rows.
- products: 898/916 matched (98.0%).
- customers: 916/916 matched (100.0%).
- returns: 99/916 matched (10.8%).
- Note: returns join < 100% is expected (only 99 orders were ever returned); unmatched orders get RefundAmount=0.
