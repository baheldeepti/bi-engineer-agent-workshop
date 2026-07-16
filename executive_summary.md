# Retail Performance — Executive Summary

*Source: all figures trace to `output/model.csv` (916 clean orders). Prepared by the BI pipeline; independently reviewed and **APPROVED** by the data-quality reviewer.*

## Headline
**We are leaving roughly $10,700 of profit on the table in one category: Footwear brings in a third of revenue but is the only category that loses money — fixing it alone would lift total net contribution ~48%.**

Total net contribution across 916 orders is **$22,162** on **$114,784** revenue (19.3% blended margin). Ranking by revenue would point management at exactly the wrong places — so every finding below is ranked by **net contribution**, not revenue.

## Insights (largest dollar impact first)

**1. Footwear sells the most and earns the least — it loses money.**
- **Number:** Footwear = **$40,692 revenue (35% of $114,784, rank #1)** but **–$2,892 net contribution (rank #5 of 5)**. Its **$6,924 of refunds exceed its $4,032 of gross profit**, driven by thin ~9.9% product margins and a 17.5% return rate (189 orders).
- **Why it matters:** A "grow our biggest category" instinct would pour spend into the one line that destroys value. Bringing Footwear to the company-average 19.3% margin is a **~$10,745 swing** (+48% on total net contribution).
- **Action:** Renegotiate Footwear supplier costs (or raise prices), cut discounting, and tackle the return driver — the worst offenders are Canvas Sneakers ($1,770 refunds) and Sandals ($1,872 refunds).

**2. VIPs are the profit engine — and they come from referrals.**
- **Number:** VIP segment = **$9,066 net contribution (41% of total)** from just **99 orders (10.8%)**, at **$295.59 AOV** — 2.5× Returning ($117.44) and 3.3× New ($88.23). **52.5% of VIP orders trace to the Referral channel.**
- **Why it matters:** A tenth of orders produces four-tenths of profit, and the cheapest-to-acquire channel (Referral) is where they concentrate.
- **Action:** Fund a referral program aggressively; it is the highest-yield path to more VIPs.

**3. Mobile App returns are 3.3× the store rate and eat contribution.**
- **Number:** Mobile App return rate = **23.1% (40 of 173 orders)** vs In-Store 6.9% (22/317) and Online 8.7% (37/426). Top reason across every channel: **"Wrong size / poor fit."**
- **Why it matters:** Each mobile return carries a refund that erases the order's margin; the channel with the worst rate is also the fastest-growing surface.
- **Action:** Add size guidance / fit tools at mobile checkout; pilot on Footwear first, where returns hurt most.

**4. Beauty is an under-invested star.**
- **Number:** Beauty = revenue rank **#5 ($13,692)** but net-contribution rank **#2 ($6,289)** at a **45.9% margin** — the healthiest in the portfolio.
- **Why it matters:** It is small precisely where it should be big. **Action:** Expand Beauty assortment and marketing; it converts revenue to profit better than anything else we sell.

## Data caveats (what was cleaned, quarantined, and how well tables joined)
- **Cleaning:** 930 → 916 sales rows. Removed **10 exact-duplicate rows**; **quarantined 4 impossible-value rows** to `output/quarantine.csv` (Revenue sentinel 999999 ×1, negative UnitPrice ×1, Quantity 999 ×2) — **never silently dropped**. Normalized Region aliases (W→West), category case/whitespace, MM/DD/YYYY→ISO dates, Returned→boolean, stripped `$`/commas from prices, and converted `15%`→`0.15`. Full log: `output/cleaning_log.md`.
- **Join coverage:** products **98.0%** (18 unmatched rows are blank-ProductName orders), customers **100%**, returns **10.8%** (expected — only returned orders have a return row; all 99 return records matched).
- **Known limitation:** the `Discount` column is unreliable on 62 rows (blank was coerced to 0). **Profit math is unaffected** — GrossProfit/COGS/NetContribution reconcile to file Revenue with zero mismatches — but do not use `Discount` for discount-depth analysis.
- Quarantined rows are excluded from every figure and chart above.
