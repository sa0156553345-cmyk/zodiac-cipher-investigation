"""Full matching: every Z340 cell scored against ALL 63 key glyphs (no top-k pruning before scoring).
Scoring is exactly the v4 pipeline (definitions reused from match_v4.py): local Otsu cell mask,
skeleton+dilate(r=2) normalisation, aspect-preserving resize to 44 px in 52x52, 1-px dilation, Dice max over +/-2 px shifts."""
import numpy as np, json, csv
from scipy import ndimage as ndi
src=open('match_v4.py',encoding='utf-8').read()
exec(src.split('ids_grid=np.empty')[0])          # KM (63x52x52), keyids, cell_mask, normalise, dice_shift, yr, xc, pg
S=np.full((340,63), np.nan)
for r in range(20):
    for c in range(17):
        p=r*17+c
        m=cell_mask(r,c,yr,xc)
        if m is None: continue
        A=ndi.binary_dilation(normalise(m), iterations=1)
        S[p]=np.array([dice_shift(A,KM[i]) for i in range(63)])
np.save('z340_full63_scores.npy', S)
json.dump(keyids, open('full63_keyids.json','w'))
ids_v4=np.load('z340_v4_ids.npy',allow_pickle=True)
top1=[keyids[int(np.argmax(S[p]))] for p in range(340)]
diff=sum(1 for p in range(340) if top1[p]!=str(ids_v4[p//17,p%17]))
print("cells scored:", int(np.sum(~np.isnan(S[:,0]))), "of 340 | top-1 differs from v4 in", diff, "cells")
vals=json.load(open('trans_values_rowmajor.json'))['values']; pos={v:p for p,v in enumerate(vals)}
rev=json.load(open('review_reveal_first10.json'))
mm=list(csv.DictReader(open('mismatch_positions_v4.csv',encoding='utf-8')))[:10]
out=[]
for row in mm:
    k=int(row['k']); p=pos[k]; order=np.argsort(S[p])[::-1]
    rank={keyids[i]:j+1 for j,i in enumerate(order)}
    vis=rev[str(k)]['visual_id']; ref=row['reference']
    best_ref_rank=min(rank[x] for x in keyids if x[0]==ref)
    top5=[(keyids[i], round(float(S[p][i]),3)) for i in order[:5]]
    rec=dict(k=k, cell=f"r{p//17+1}c{p%17+1}", top5=top5, visual=vis, visual_rank=(rank[vis] if vis else None),
             matcher=row['matched_id'], ref_letter=ref, best_rank_ref_letter=best_ref_rank)
    out.append(rec)
    print(f"k={k:>2} {rec['cell']:>6} | visual={str(vis):>4} rank={str(rec['visual_rank']):>3} | ref={ref} best-ref-letter rank={best_ref_rank:>2} | top5={top5}")
json.dump(out, open('full63_ten_cases.json','w'), ensure_ascii=False, indent=1)
