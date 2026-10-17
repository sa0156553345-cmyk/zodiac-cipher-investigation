"""Decrypt all 340 positions using full-63 top-1 IDs (no edits), then with the 6 documented visual corrections only.
Reference text is used ONLY to measure agreement and to label residuals (diagnostics), never to choose identities."""
import numpy as np, json, csv, collections
S=np.load('z340_full63_scores.npy'); keyids=json.load(open('full63_keyids.json'))
keyrows={r['glyph_id']:r['letter'] for r in csv.DictReader(open('key_table_glyphs.csv',encoding='utf-8'))}
vals=json.load(open('trans_values_rowmajor.json'))['values']; pos={v:p for p,v in enumerate(vals)}
C=json.load(open('compare_z340_v4.json')); ref=C['ref']
rev=json.load(open('review_reveal_first10.json'))
top1=[keyids[int(np.argmax(S[pos[k]]))] for k in range(340)]          # indexed by reading order k
dec0=''.join(keyrows[top1[k]] for k in range(340))
agree0=sum(dec0[k]==ref[k] for k in range(340))
print(f"[A] full-63 top-1, no edits: agreement {agree0}/340 = {agree0/340:.3f}")
corr={}
for k,info in rev.items():
    v=info['verdict']
    if v['confidence'] in ('high','medium-high') and info['visual_id']:
        corr[int(k)]=info['visual_id']
top1c=list(top1)
for k,idv in corr.items(): top1c[k]=idv
dec1=''.join(keyrows[top1c[k]] for k in range(340))
agree1=sum(dec1[k]==ref[k] for k in range(340))
print(f"[B] + 6 documented visual corrections: agreement {agree1}/340 = {agree1/340:.3f}  (corrections: {sorted(corr)})")
resid=[]
for k in range(340):
    if dec1[k]!=ref[k]:
        p=pos[k]; order=np.argsort(S[p])[::-1]
        rank={keyids[i]:j+1 for j,i in enumerate(order)}
        best_ref=min(rank[x] for x in keyids if x[0]==ref[k])
        resid.append(dict(k=k, cell=f"r{p//17+1}c{p%17+1}", chosen=top1c[k], chosen_letter=dec1[k], reference=ref[k],
                          top1_score=round(float(S[p][np.argmax(S[p])]),3), rank_of_best_reference_glyph=best_ref))
bins=collections.Counter('2-5' if r['rank_of_best_reference_glyph']<=5 else ('6-10' if r['rank_of_best_reference_glyph']<=10 else '>10') for r in resid)
print(f"[C] residual mismatches: {len(resid)}")
print("    best reference-letter glyph rank among residuals:", dict(bins))
conf=collections.Counter((r['chosen_letter'],r['reference']) for r in resid).most_common(8)
print("    most frequent (chosen letter -> reference letter):", conf)
used=collections.Counter(top1c)
unused=sorted(set(keyids)-set(used))
print("    key glyphs never chosen as top-1 after corrections:", unused)
json.dump(dict(agree_full=agree0, agree_corrected=agree1, corrections=corr, residuals=resid, unused=unused),
          open('full63_residuals.json','w'), ensure_ascii=False, indent=1)
with open('full63_residuals.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=list(resid[0].keys())); w.writeheader(); w.writerows(resid)
