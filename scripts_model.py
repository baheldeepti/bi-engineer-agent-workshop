#!/usr/bin/env python3
"""Stage 2 — data-modeling: join the four cleaned tables into output/model.csv."""
import csv, os, collections

OUT="output"
def load(fn): return list(csv.DictReader(open(f"{OUT}/{fn}")))

sales=load("retail_sales_messy_clean.csv")
products={p['ProductName']: p for p in load("retail_products_clean.csv")}
customers={c['CustomerID']: c for c in load("retail_customers_clean.csv")}
# returns: one row per OrderID (keep first if duplicated)
returns={}
for r in load("retail_returns_clean.csv"):
    returns.setdefault(r['OrderID'], r)

def fnum(v):
    try: return float(v)
    except: return None

model=[]
cov=collections.Counter()
for s in sales:
    row=dict(s)
    qty=fnum(s['Quantity']); rev=fnum(s['Revenue'])

    # products on ProductName
    p=products.get(s['ProductName'].strip())
    if p:
        cov['products']+=1
        row['UnitCost']=p['UnitCost']; row['ListPrice']=p['ListPrice']
        row['GrossMarginPct']=p['GrossMarginPct']; row['Supplier']=p['Supplier']
    else:
        row['UnitCost']=row['ListPrice']=row['GrossMarginPct']=row['Supplier']=''

    # customers on CustomerID
    c=customers.get(s['CustomerID'].strip())
    if c:
        cov['customers']+=1
        row['Segment']=c['CustomerSegment']; row['AcquisitionChannel']=c['AcquisitionChannel']
        row['SignupYear']=c['SignupYear']; row['LoyaltyTier']=c['LoyaltyTier']
    else:
        row['Segment']=row['AcquisitionChannel']=row['SignupYear']=row['LoyaltyTier']=''

    # returns on OrderID
    rt=returns.get(s['OrderID'].strip())
    if rt:
        cov['returns']+=1
        row['ReturnReason']=rt['ReturnReason']; row['RefundAmount']=rt['RefundAmount']
        row['RestockedFlag']=rt['RestockedFlag']
    else:
        row['ReturnReason']=''; row['RefundAmount']='0'; row['RestockedFlag']=''

    # derived
    unitcost=fnum(row['UnitCost']); refund=fnum(row['RefundAmount']) or 0.0
    if unitcost is not None and qty is not None:
        cogs=round(unitcost*qty,2); row['COGS']=f"{cogs:.2f}"
        if rev is not None:
            row['GrossProfit']=f"{rev-cogs:.2f}"
            row['NetContribution']=f"{rev-cogs-refund:.2f}"
        else:
            row['GrossProfit']=row['NetContribution']=''
    else:
        row['COGS']=row['GrossProfit']=row['NetContribution']=''
    model.append(row)

cols=['OrderID','OrderDate','CustomerID','Region','ProductCategory','ProductName','Channel',
      'UnitPrice','Quantity','Discount','ShippingCost','Revenue','Returned',
      'UnitCost','ListPrice','GrossMarginPct','Supplier',
      'Segment','AcquisitionChannel','SignupYear','LoyaltyTier',
      'ReturnReason','RefundAmount','RestockedFlag',
      'COGS','GrossProfit','NetContribution']
with open(f"{OUT}/model.csv","w",newline='') as f:
    w=csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader(); w.writerows(model)

n=len(model)
print("STAGE 2 COMPLETE")
print(f"  model rows: {n}")
print(f"  join coverage:")
for t in ['products','customers','returns']:
    print(f"    {t:10s}: {cov[t]:4d}/{n}  ({100*cov[t]/n:.1f}%)")

# append coverage to cleaning log
with open(f"{OUT}/cleaning_log.md","a") as f:
    f.write("\n\n## Model join coverage\n")
    f.write(f"- Model spine: {n} clean order rows.\n")
    for t in ['products','customers','returns']:
        f.write(f"- {t}: {cov[t]}/{n} matched ({100*cov[t]/n:.1f}%).\n")
    f.write(f"- Note: returns join < 100% is expected (only {len(returns)} orders were ever returned); "
            f"unmatched orders get RefundAmount=0.\n")
