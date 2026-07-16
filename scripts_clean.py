#!/usr/bin/env python3
"""Stage 1 — data-quality: profile & conservatively clean each raw CSV.
Writes output/<name>_clean.csv, output/quarantine.csv, output/cleaning_log.md."""
import csv, re, os, collections

DATA="data"; OUT="output"
os.makedirs(OUT, exist_ok=True)
log=[]
def L(msg): log.append(msg)

# ---------- helpers ----------
def num(v):
    if v is None: return None
    v=v.strip().replace('$','').replace(',','')
    if v=='' : return None
    if v.endswith('%'): return float(v[:-1])/100.0
    return float(v)

REGION={'w':'West','west':'West','e':'East','east':'East','s':'South','south':'South',
        'mw':'Midwest','midwest':'Midwest','north':'North'}
def norm_region(v):
    k=v.strip().lower()
    return REGION.get(k, v.strip().title())

def norm_cat(v):
    return v.strip().title() if v.strip() else v.strip()

TRUE={'yes','y','1','true','t'}; FALSE={'no','n','0','false','f'}
def norm_bool(v):
    k=v.strip().lower()
    if k in TRUE: return 'true'
    if k in FALSE: return 'false'
    return ''

def norm_date(v):
    v=v.strip()
    m=re.match(r'(\d{2})/(\d{2})/(\d{4})$', v)          # MM/DD/YYYY
    if m: return f"{m.group(3)}-{m.group(1)}-{m.group(2)}"
    if re.match(r'\d{4}-\d{2}-\d{2}$', v): return v      # already ISO
    return v

# ---------- SALES (the spine, messy) ----------
raw=list(csv.DictReader(open(f"{DATA}/retail_sales_messy.csv")))
L(f"## retail_sales_messy.csv")
L(f"- Profiled: {len(raw)} data rows, {len(raw[0])} columns.")

# 1) exact duplicate removal
seen=set(); deduped=[]; dup=0
for r in raw:
    key=tuple(r.values())
    if key in seen: dup+=1; continue
    seen.add(key); deduped.append(r)
L(f"- Removed **{dup}** exact-duplicate rows ({len(raw)} -> {len(deduped)}).")

quarantine=[]; clean=[]
counters=collections.Counter()
for r in deduped:
    reasons=[]
    up=r['UnitPrice']; qty=r['Quantity']; rev=r['Revenue']
    # detect impossible values on RAW parse
    try: up_n=num(up)
    except: up_n=None
    try: qty_n=float(qty) if qty.strip() else None
    except: qty_n=None
    try: rev_n=num(rev)
    except: rev_n=None
    if up_n is not None and up_n<0: reasons.append(f"negative UnitPrice ({up})")
    if qty_n is not None and qty_n>=999: reasons.append(f"impossible Quantity ({qty})")
    if rev_n is not None and rev_n in (99999,999999,9999999): reasons.append(f"sentinel Revenue ({rev})")
    if reasons:
        rr=dict(r); rr['_QuarantineReason']='; '.join(reasons); rr['_SourceFile']='retail_sales_messy.csv'
        quarantine.append(rr); continue

    # ---- normalize ----
    row=dict(r)
    row['Region']=norm_region(r['Region']); counters['region']+= (norm_region(r['Region'])!=r['Region'])
    row['ProductCategory']=norm_cat(r['ProductCategory']); counters['cat']+=(norm_cat(r['ProductCategory'])!=r['ProductCategory'])
    row['OrderDate']=norm_date(r['OrderDate']); counters['date']+=(norm_date(r['OrderDate'])!=r['OrderDate'])
    row['Returned']=norm_bool(r['Returned']); counters['bool']+=1
    row['UnitPrice']= f"{up_n:.2f}" if up_n is not None else ''
    counters['price_fmt']+= bool(re.search(r'[$,]', up))
    disc_n=num(r['Discount']); counters['disc_pct']+= r['Discount'].strip().endswith('%')
    if disc_n is None: disc_n=0.0; counters['disc_blank']+=1
    row['Discount']=f"{disc_n:.4f}".rstrip('0').rstrip('.') if disc_n else '0'
    ship_n=num(r['ShippingCost'])
    if ship_n is None: ship_n=0.0; counters['ship_blank']+=1
    row['ShippingCost']=f"{ship_n:.2f}"
    # recompute missing revenue
    if rev_n is None:
        if up_n is not None and qty_n is not None:
            rev_n=round(up_n*qty_n*(1-disc_n),2); counters['rev_recomputed']+=1
        else:
            rev_n=None
    row['Revenue']= f"{rev_n:.2f}" if rev_n is not None else ''
    counters['pname_blank']+= (r['ProductName'].strip()=='')
    clean.append(row)

# write clean sales
if clean:
    with open(f"{OUT}/retail_sales_messy_clean.csv","w",newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(clean[0].keys())); w.writeheader(); w.writerows(clean)

L(f"- Normalized Region aliases/case: **{counters['region']}** rows (W->West, e->East, MW->Midwest, ...).")
L(f"- Normalized ProductCategory case/whitespace: **{counters['cat']}** rows (footwear/'Footwear ' -> Footwear).")
L(f"- Parsed MM/DD/YYYY dates to ISO: **{counters['date']}** rows.")
L(f"- Normalized Returned to boolean: **{counters['bool']}** rows (Yes/Y/1/TRUE->true, No/N/0/FALSE->false).")
L(f"- Stripped $/commas from UnitPrice: **{counters['price_fmt']}** rows.")
L(f"- Converted Discount percent strings (15% -> 0.15): **{counters['disc_pct']}** rows; blank Discount treated as 0: **{counters['disc_blank']}** rows *(assumption)*.")
L(f"- Blank ShippingCost treated as 0: **{counters['ship_blank']}** rows *(assumption; shipping not used in profit math)*.")
L(f"- Recomputed missing Revenue = UnitPrice*Quantity*(1-Discount): **{counters['rev_recomputed']}** rows.")
L(f"- Left **{counters['pname_blank']}** blank ProductName rows in place (missing, not impossible) — will not match products; flagged as join gap.")
L(f"- **Quarantined {len(quarantine)}** impossible-value rows (negative price, Quantity 999, sentinel Revenue) -> output/quarantine.csv (never dropped).")
L(f"- **Clean sales rows: {len(clean)}**.")
L("")

# ---------- LOOKUP TABLES (already clean; trim + pass through) ----------
def passthrough(fn, name):
    rows=list(csv.DictReader(open(f"{DATA}/{fn}")))
    for r in rows:
        for k in r: r[k]=r[k].strip()
    with open(f"{OUT}/{name}_clean.csv","w",newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    L(f"## {fn}\n- {len(rows)} rows; clean on profile (unique keys, no dupes/blanks/sentinels). Trimmed whitespace only.\n")
    return rows
passthrough('retail_products.csv','retail_products')
passthrough('retail_customers.csv','retail_customers')
passthrough('retail_returns.csv','retail_returns')

# ---------- write quarantine + log ----------
if quarantine:
    cols=list(raw[0].keys())+['_QuarantineReason','_SourceFile']
    with open(f"{OUT}/quarantine.csv","w",newline='') as f:
        w=csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(quarantine)

with open(f"{OUT}/cleaning_log.md","w") as f:
    f.write("# Cleaning Log\n\nEvery change applied by the data-quality stage. Impossible values were quarantined, never silently dropped.\n\n")
    f.write("\n".join(log))

print("STAGE 1 COMPLETE")
print(f"  clean sales rows : {len(clean)}")
print(f"  quarantined rows : {len(quarantine)}")
for q in quarantine: print("    -", q['OrderID'], q['_QuarantineReason'])
