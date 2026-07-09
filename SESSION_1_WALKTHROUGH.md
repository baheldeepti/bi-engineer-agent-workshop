# Session 1 — Live Delivery Script (CORRECTED for today's enriched session)

## "Become the Analyst" · today · 60 min · no code · built for \~50

**Facilitator:** Deepti Bahel · **Co-host:** Lakshmi / Retail Women in Technology (chat \+ stragglers) **Dataset:** your messy orders file (`retail_orders_messy.csv`) is the Session-1 spine. The three companion files (`retail_products.csv`, `retail_customers.csv`, `retail_returns.csv`) \+ `DATA_DICTIONARY.md` are the **level-up unlock** for fast finishers.

**What changed from my first draft (all now fixed to your verified answer key):** real numbers ($104K / 25% mobile / VIP 3.6× / etc.), the four-table level-up added, your five named mechanics, a dashboard deliverable, and the Session-2 bridge pointed at **web-based Claude Code (claude.ai/code), not a local terminal.**

**The one rule:** participants make every call; Claude does the typing. "Should I drop this?" → "What do you think, and why?" — then let Claude execute.

---

## Your five interactive mechanics (weave these throughout)

1. **Predict-then-reveal ×3.** Room commits a guess before each reveal; every guess gets subverted.  
2. **The Anomaly Race.** First to find the $999,999 row types **FOUND IT** in chat. 30 sec of energy.  
3. **Pair-and-share.** Cleaning debates: "keep the sentinel row or kill it? Defend it."  
4. **Headline wall.** Everyone posts their one-line headline in chat.  
5. **Level-up unlock.** Fast finishers join the four files and find the buried margin story.

---

## −10:00 to 0:00 · Doors-open (before the clock)

- [ ] Livestream \+ recording live. Slides on the dry-run's finished memo \+ dashboard as a north star.  
- [ ] Pin in chat: link to `retail_orders_messy.csv`, and "open claude.ai in a browser tab."  
- [ ] Also pin (for fast finishers): the 3 companion CSVs \+ data dictionary, labeled **"Level-up files — don't open yet."**  
- [ ] Co-host: "Reply ✅ when you have the orders CSV downloaded and claude.ai open."

**SAY (rolling):** "Download the orders file from the pin, open claude.ai. That's the whole setup — no code today. There's a bonus pack pinned too; ignore it for now, it's your reward for finishing early."

---

## 0:00–0:05 · Frame the mission

**SAY:** "Today *you* are the analyst — not Claude. Claude profiles, cleans, and calculates at your direction, but every judgment call is yours. One messy retail file, one job: find the real story under the mess and write it so a manager could act on it Monday. By the end you'll have a cleaned dataset, a one-page memo, and a dashboard — and you'll have caught something that fools most professionals."

**⚡ Opening poll (30 sec):** "Hands or chat — who's ever renamed 'West / west / W' by hand in a spreadsheet?" *(Let the groans land.)* "Watch how fast this goes."

**Transition:** "Fresh Claude chat, upload the orders CSV. Co-host's dropping prompt 1 now."

---

## 0:05–0:12 · Meet the data (profile — no fixing)

**PASTE — Prompt 1:**

I've uploaded a retail orders dataset. Before changing anything, give me a plain-English

profile: how many rows and columns, what each column means, and the top data-quality

problems you notice. Don't fix anything yet — just tell me what's wrong, worst first.

**WATCH:** \~930 rows × 14 cols; a column glossary; issues named — mixed date formats, 12 region spellings for 4 regions, \~10 encodings of Returned, `$` in prices, blanks, duplicate rows.

**⚡ Trust-builder (30 sec):** "Hands up — Claude flagged a problem you'd have missed?" (Name one: the invisible trailing spaces in Category that'd silently break a group-by.)

**IF IT WOBBLES:** Upload fails → co-host 1:1; room keeps moving.

---

## 0:12–0:20 · Interrogate, then the trap (Predict-then-reveal \#1)

**PASTE — Prompt 2:**

Show me every distinct value with its count for the Region, ProductCategory, and

Returned columns. I want to see the inconsistencies myself.

**WATCH:** 12 spellings → 4 regions; case/space Category variants; \~10 Returned encodings.

**⚡ PREDICT \#1 (before running Prompt 3):** "Commit in chat: which region made the most revenue? Guess now." *(15 sec — commitment makes the reveal land.)*

**PASTE — Prompt 3 (the trap, on RAW data):**

On this data as-is, which region generated the most revenue, and by how much?

Give me a quick ranked table.

**WATCH:** **West looks wildly dominant.** DO NOT CORRECT IT. Let it sit.

**SAY:** "West isn't just winning, it's *crushing* everyone. Hold that too-dramatic feeling — we'll come back to it."

---

## 0:20–0:30 · The catch (the peak — slow down) · Anomaly Race

**PASTE — Prompt 4:**

That West total looks suspiciously large versus the others. Find the specific rows

driving it and show them to me — I want to see the actual records.

**WATCH:** **`ORD50357`** — a **$12.88 ceramic mug** with **Revenue \= $999,999**, sitting in **West / Home / September**. One row invents the whole "West / Home / September" story.

**⚡ ANOMALY RACE:** "First to find it types **FOUND IT** in chat — order ID and what's wrong."

**When it lands — STOP. This is the emotional peak.** **SAY:** "A twelve-dollar-and-eighty-eight-cent mug… with revenue keyed as nine hundred ninety-nine thousand dollars. That's not a sale — that's a finger slip. And that ONE row invented a business conclusion a VP could've put in a board deck. The real question isn't technical: is it a real sale or a typo — and *who decides what we do with it?* You do. That's the job."

**⚡ PAIR-AND-SHARE (90 sec):** "Neighbor or chat: keep this row 'just in case,' or kill it? Defend your call." *(Someone will argue keep — perfect. The point is a human chose, on the record.)*

**IF IT WOBBLES:** Sentinel won't surface → "sort by Revenue descending, show the top 5 rows."

---

## 0:30–0:40 · Clean it — participant makes every call (Predict-then-reveal \#2)

**PASTE — Prompt 5:**

Let's clean this together. Walk through these one at a time and ask me to confirm

before applying each:

1\. Standardize Region to West / East / South / Midwest.

2\. Fix ProductCategory (case \+ trailing spaces) to clean categories.

3\. Convert Returned to a clean Yes/No.

4\. Convert Discount to decimals (15% \-\> 0.15); leave blanks as unknown.

5\. Strip $ from prices; fix the one negative price.

6\. Parse all dates into one ISO format (YYYY-MM-DD).

7\. Remove exact duplicate rows.

8\. Quarantine impossible values (the $999,999 revenue row and the quantity-999 row)

   instead of analyzing them.

For blank Revenue, recompute it as UnitPrice x Quantity x (1 \- Discount).

Keep a short log of every change you make.

**WATCH:** Confirms each fix; quarantines (not deletes) the sentinel; recomputes blank Revenue; keeps a change log. Lands at **\~821 clean rows.**

**SAY at each step:** "Agree, or handle it differently?" And on the log: "That change log is your credibility — when a manager asks 'what did you do to my data?', you show receipts, not 'trust me.'"

**⚡ PREDICT \#2 (before re-analyzing):** "We're about to re-run the region question on the *clean* data. Commit: does West still dominate — yes or no?"

**IF IT WOBBLES:** Claude does it all at once → "tell it 'stop after each step and wait for my confirm.'" Blanks dropped instead of recomputed → "recompute blank Revenue, don't drop those rows."

---

## 0:40–0:50 · Re-analyze — find the REAL headline · Headline wall

**PASTE — Prompt 6:**

Now, on the CLEANED data, give me short tables for:

\- revenue by region

\- revenue by product category

\- return rate by channel

\- return rate by product category

\- average order value by customer segment

\- return rate for orders discounted over 30% vs everything else

**WATCH / ANSWER-KEY CHECKPOINT (your verified numbers):**

- **Regions balanced now:** West **$34K** · East **$28K** · South **$24K** · Midwest **$18K.** *West's dominance vanished the instant the mug left.* (Predict \#2 payoff.)  
- **Return rate by channel:** **Mobile App \~25%** · Online \~10% · In-Store \~8%.  
- **Footwear:** **\#1 in revenue AND \~20% return rate** — a margin leak.  
- **AOV by segment:** **VIP \~$312** vs Returning \~$116 vs **New \~$87 (\~3.6×).**  
- **Deep discounts:** orders discounted **\>30% return \~37%** vs \~10% otherwise.  
- **Totals:** ≈ **$104K** revenue · AOV ≈ **$126** · overall return ≈ **12%** · **no real seasonality** (flat \~$7–11K/mo once the sentinel's gone).

**PASTE — Prompt 7:**

What's the single most surprising, actionable finding here that a retail operations

manager would want on Monday morning? Explain why it matters and show the numbers behind it.

**⚡ HEADLINE WALL:** "Everyone posts ONE headline sentence in chat, with the number behind it. This is the skill — turning a table into a decision."

**SAY (validate live):** "The strongest operational headline is Mobile App returns — one in four orders comes back, \~3× In-Store. Real money leaking through the app, and it's fixable. Footwear's revenue-vs- returns tension and VIP value are legit leads too — pick yours, defend it, show the group-by."

---

## 0:50–0:58 · Ship it — memo \+ dashboard

**PASTE — Prompt 8 (memo):**

Write a one-page insight memo for a retail operations lead: a headline finding, 3 supporting

insights with numbers, one data-quality caveat (what we cleaned and quarantined), and 2

recommended actions. Plain business language, one page. Then give me the cleaned dataset as a

downloadable CSV and the memo as a downloadable file.

**PASTE — Prompt 9 (dashboard):**

Build a simple self-contained HTML dashboard for these findings: KPI cards (total revenue, AOV,

overall return rate, Mobile App return rate) and bar charts for return rate by channel and by

category. Accent only the Mobile App / Footwear bars; keep the rest neutral. One file, no server.

**SAY:** "Notice the caveat line in the memo — telling the reader what you cleaned and set aside is what separates an analyst from a chart generator. Honesty is a feature."

**IF IT WOBBLES (free tier):** Download won't generate → copy the memo text \+ table; "next week's agents write real files." Don't burn clock.

**⚡ Deliverable check:** "Thumbs up in chat if you have three things: cleaned CSV, one-page memo, dashboard."

---

## ⭐ LEVEL-UP UNLOCK (fast finishers, runs in parallel; surface the reveal to the room if time allows)

**SAY (to whoever's done early):** "Unlock the bonus pack — upload `retail_products.csv`, `retail_customers.csv`, and `retail_returns.csv` into your chat."

**⚡ PREDICT \#3:** "Before you join anything — which category do you think is your most *profitable*?" *(Everyone says Footwear, the revenue leader. Let them.)*

**PASTE — Level-up prompt:**

I've uploaded three more files: products (with unit cost \+ margin), customers (with acquisition

channel), and returns (with reasons \+ refund amounts). Join them to my orders and tell me:

1\. True net contribution by product category after netting margin against refunds — which category

   actually MAKES money and which LOSES money?

2\. The \#1 refund reason and which channel it concentrates in.

3\. Which acquisition channels VIP customers came from.

Show the numbers behind each.

**WATCH / THE REVEAL:**

- **Footwear leads revenue ($36K) but is the ONLY money-LOSING category (–$850 net)** after its thin 17% margin and $6.9K in refunds. **Apparel is the real profit leader (\~$9.3K);** Beauty & Accessories are quiet high-margin winners.  
- **"Wrong size / poor fit"** is the \#1 refund driver (\~$5K), concentrated in **Mobile App** → *explains* the 25% mobile return rate. Action: add a size guide to the app.  
- **\~81% of VIPs came from Referral \+ Email;** New customers skew to Paid Social (high returns, low value). Action: shift spend to referral.

**SAY (the reframe — the line that justifies four tables):** "Revenue is vanity. Contribution margin is sanity. The category that looks like your best performer is quietly losing money — and you can *only* see it when you join the files. That's what a data team does that a spreadsheet can't."

---

## 0:58–1:00 · Bridge to Session 2 (CORRECTED — web-based Claude Code)

**SAY:** "In under an hour, no code, you took a broken file, caught an anomaly that fools professionals, made every cleaning call yourself, found the real story, and shipped a memo *and* a dashboard. That's not 'using Claude' — that's being an AI data analyst."

**SAY (the hook, accurate to your plan):** "Next week we don't do this by hand. We build a Claude Code project **in your browser at claude.ai/code — no terminal, no installs** — that connects to a GitHub repo and does all of this from a single `/analyze` command: four reusable Skills (data-quality, data-modeling, insight-generation, reporting-style), a data-quality-reviewer that double-checks the work, and a `CLAUDE.md` that holds your judgment. Same thinking you used today, captured once, running on any file."

**SAY (pre-work — say it clearly, it's different from what people expect):** "To join next week you need a **Claude Pro or Max plan** and a **free GitHub account** — that's it. No Node, no terminal. The pre-work email has the two links. See you next week."

---

## Facilitator quick-reference card (keep visible)

**Must-hit checkpoints:** ① wrong "West wins" on raw data · ② the $999,999 mug reveal · ③ West going normal after cleaning · ④ Mobile App returns headline · ⑤ (level-up) Footwear \= the money loser.

**Answer key at a glance (your verified file):** | Metric | Value | |---|---| | Total revenue (clean) | ≈ $104K | | AOV | ≈ $126 | | Overall return rate | ≈ 12% | | Mobile / Online / In-Store returns | \~25% / \~10% / \~8% | | Footwear | \#1 revenue, \~20% return | | VIP / Returning / New AOV | \~$312 / \~$116 / \~$87 (VIP \~3.6× New) | | Discount \>30% → return | \~37% vs \~10% | | Regions (clean) | West $34K · East $28K · South $24K · Midwest $18K | | Clean row count | \~821 | | Seasonality | none — flat ~~$7–11K/mo | | Sentinel | `ORD50357` — $12.88 mug, $999,999, West/Home/Sept | | **Level-up: true contribution** | **Footwear –$850 (only loser); Apparel \~+$9.3K (real leader)** | | Level-up: \#1 refund reason | "wrong size/fit", concentrated in Mobile App (~~$5K) | | Level-up: VIP acquisition | \~81% from Referral \+ Email |

**Recovery one-liners:** upload fails → co-host 1:1 · sentinel hiding → "sort by Revenue desc, top 5" · Claude fixes all at once → "stop after each step, wait for my confirm" · download won't generate → copy text out, "Session 2 writes real files" · someone spoils the anomaly early → "you might be right — let's *prove* it, not guess it."

**Session-2 pre-work (repeat at the close):** Claude **Pro/Max** plan \+ a free **GitHub** account. No Node, no terminal.

*Protect the clock, keep every decision in the room, and let them catch the mug themselves.*  
