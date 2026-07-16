#!/usr/bin/env python3
"""Stage 4 — insight-generation: ranked, decision-oriented cuts from output/model.csv.
Emits output/insights.json for the reporting stage."""
import csv, json, collections

rows=list(csv.DictReader(open("output/model.csv")))
def f(v):
    try: return float(v)
    except: return None

N=len(rows)

# ---- net contribution & revenue by category ----
cat=collections.defaultdict(lambda: {'rev':0.0,'nc':0.0,'cogs':0.0,'n':0,'refund':0.0})
for r in rows:
    c=r['ProductCategory'] or 'Unknown'
    rev=f(r['Revenue']); nc=f(r['NetContribution']); cogs=f(r['COGS']); rf=f(r['RefundAmount']) or 0
    d=cat[c]; d['n']+=1
    if rev is not None: d['rev']+=rev
    if nc  is not None: d['nc'] +=nc
    if cogs is not None: d['cogs']+=cogs
    d['refund']+=rf
cats=[]
for c,d in cat.items():
    cats.append({'category':c,'revenue':round(d['rev'],2),'net_contribution':round(d['nc'],2),
                 'cogs':round(d['cogs'],2),'refunds':round(d['refund'],2),'orders':d['n'],
                 'margin_pct': round(100*d['nc']/d['rev'],1) if d['rev'] else None})
rev_rank={c['category']:i+1 for i,c in enumerate(sorted(cats,key=lambda x:-x['revenue']))}
nc_rank ={c['category']:i+1 for i,c in enumerate(sorted(cats,key=lambda x:-x['net_contribution']))}
for c in cats:
    c['revenue_rank']=rev_rank[c['category']]; c['contribution_rank']=nc_rank[c['category']]
    c['rank_disagrees']=c['revenue_rank']!=c['contribution_rank']
cats.sort(key=lambda x:-x['net_contribution'])

# ---- return rate & top reasons by channel ----
chan=collections.defaultdict(lambda: {'n':0,'ret':0,'reasons':collections.Counter()})
for r in rows:
    ch=r['Channel'] or 'Unknown'; chan[ch]['n']+=1
    if r['ReturnReason'].strip():
        chan[ch]['ret']+=1; chan[ch]['reasons'][r['ReturnReason']]+=1
channels=[]
for ch,d in chan.items():
    channels.append({'channel':ch,'orders':d['n'],'returns':d['ret'],
                     'return_rate':round(100*d['ret']/d['n'],1),
                     'top_reasons':d['reasons'].most_common(3)})
channels.sort(key=lambda x:-x['return_rate'])

# ---- AOV & count by segment ----
seg=collections.defaultdict(lambda: {'rev':0.0,'n':0,'nc':0.0})
for r in rows:
    s=r['Segment'] or 'Unknown'; rev=f(r['Revenue']) or 0; nc=f(r['NetContribution']) or 0
    seg[s]['rev']+=rev; seg[s]['n']+=1; seg[s]['nc']+=nc
segments=[]
for s,d in seg.items():
    segments.append({'segment':s,'orders':d['n'],'revenue':round(d['rev'],2),
                     'net_contribution':round(d['nc'],2),'aov':round(d['rev']/d['n'],2)})
segments.sort(key=lambda x:-x['net_contribution'])

# ---- acquisition mix of the top segment (by net contribution) ----
top_seg=segments[0]['segment']
acq=collections.Counter()
for r in rows:
    if (r['Segment'] or 'Unknown')==top_seg:
        acq[r['AcquisitionChannel'] or 'Unknown']+=1
acq_mix=[{'channel':k,'orders':v,'pct':round(100*v/segments[0]['orders'],1)} for k,v in acq.most_common()]

# ---- monthly trend ----
mon=collections.defaultdict(lambda: {'rev':0.0,'nc':0.0,'n':0})
for r in rows:
    d=r['OrderDate'][:7]
    if len(d)==7:
        mon[d]['rev']+=f(r['Revenue']) or 0; mon[d]['nc']+=f(r['NetContribution']) or 0; mon[d]['n']+=1
monthly=[{'month':m,'revenue':round(v['rev'],2),'net_contribution':round(v['nc'],2),'orders':v['n']}
         for m,v in sorted(mon.items())]

totals={'orders':N,'revenue':round(sum(f(r['Revenue']) or 0 for r in rows),2),
        'net_contribution':round(sum(f(r['NetContribution']) or 0 for r in rows),2),
        'refunds':round(sum(f(r['RefundAmount']) or 0 for r in rows),2),
        'returns':sum(1 for r in rows if r['ReturnReason'].strip()),
        'return_rate':round(100*sum(1 for r in rows if r['ReturnReason'].strip())/N,1)}

out={'totals':totals,'categories':cats,'channels':channels,'segments':segments,
     'top_segment':top_seg,'acq_mix':acq_mix,'monthly':monthly}
json.dump(out, open("output/insights.json","w"), indent=2)

# ---- print ranked findings ----
print("STAGE 4 COMPLETE — key cuts")
print(f"\nTotals: {N} orders | Revenue ${totals['revenue']:,.0f} | NetContribution ${totals['net_contribution']:,.0f} | Return rate {totals['return_rate']}%")
print("\nNet contribution by category (rank inversions flagged):")
for c in cats:
    flag=' <-- REV#%d vs NC#%d DISAGREE'%(c['revenue_rank'],c['contribution_rank']) if c['rank_disagrees'] else ''
    print(f"  {c['category']:12s} rev ${c['revenue']:>9,.0f}  NC ${c['net_contribution']:>9,.0f}  ({c['margin_pct']}%){flag}")
print("\nReturn rate by channel:")
for ch in channels:
    print(f"  {ch['channel']:12s} {ch['return_rate']:>5}%  ({ch['returns']}/{ch['orders']})  top: {ch['top_reasons'][0] if ch['top_reasons'] else '-'}")
print("\nSegment by net contribution (AOV):")
for s in segments:
    print(f"  {s['segment']:12s} NC ${s['net_contribution']:>9,.0f}  AOV ${s['aov']:.2f}  ({s['orders']} orders)")
print(f"\nTop segment '{top_seg}' acquisition mix: "+", ".join(f"{a['channel']} {a['pct']}%" for a in acq_mix))
