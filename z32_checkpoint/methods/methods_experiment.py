"""Pre-registered experiment (PREREG_METHODS.md). Selection on tuning set k<170 only; validation k>=170 measured once."""
import numpy as np, json, csv, time
from scipy import ndimage as ndi
from skimage.morphology import skeletonize, disk
from PIL import Image
t0=time.time()
src=open('match_v4.py',encoding='utf-8').read()
exec(src.split('ids_grid=np.empty')[0])        # yr, xc, pg, kg, keyids, KM (M0 templates), cell_mask, normalise (M0), dice_shift
keyrows=list(csv.DictReader(open('key_table_glyphs.csv',encoding='utf-8')))
def norm_plain(mask, size=44, canvas=52):
    ys,xs=np.where(mask)
    if len(ys)==0: return np.zeros((canvas,canvas),bool)
    crop=mask[ys.min():ys.max()+1, xs.min():xs.max()+1]
    h,w=crop.shape; s=size/max(h,w)
    im=Image.fromarray((crop*255).astype('uint8')).resize((max(1,int(round(w*s))),max(1,int(round(h*s)))),Image.BILINEAR)
    m=np.asarray(im)>127
    out=np.zeros((canvas,canvas),bool); oy=(canvas-m.shape[0])//2; ox=(canvas-m.shape[1])//2
    out[oy:oy+m.shape[0], ox:ox+m.shape[1]]=m
    return out
def norm_skel(mask, rad):
    return norm_plain(ndi.binary_dilation(skeletonize(mask), structure=disk(rad)))
KR=[(kg[int(r['y0']):int(r['y1']), int(r['x0']):int(r['x1'])]<110) for r in keyrows]
KF1=np.stack([ndi.binary_dilation(norm_plain(m),iterations=1) for m in KR])
KF2=np.stack([ndi.binary_dilation(norm_skel(m,1),iterations=1) for m in KR])
KF0=KM                                           # M0 templates (identical pipeline to v4)
CM={}
for r in range(20):
    for c in range(17):
        CM[r*17+c]=cell_mask(r,c,yr,xc)
def scores(A_list, T):
    S=np.zeros((340,63))
    for p in range(340):
        for i in range(63): S[p,i]=dice_shift(A_list[p], T[i])
    return S
def feat(fn, rad=None, rot=0.0):
    out=[]
    for p in range(340):
        m=CM[p]
        if rot: m=ndi.rotate(m.astype(float), rot, reshape=False, order=1)>0.5
        mm = fn(m) if rad is None else fn(m, rad)
        out.append(ndi.binary_dilation(mm, iterations=1))
    return out
vals=json.load(open('trans_values_rowmajor.json'))['values']
pos={v:p for p,v in enumerate(vals)}
ref=json.load(open('compare_z340_v4.json'))['ref']
def letter_of(i): return keyids[i][0]
def evaluate(S):
    top=[int(np.argmax(S[pos[k]])) for k in range(340)]
    hit=np.array([letter_of(top[k])==ref[k] for k in range(340)])
    return top, dict(tune=float(hit[:170].mean()), val=float(hit[170:].mean()), all=float(hit.mean()))
results={}; S_store={}
print("feature build + scoring:", flush=True)
A0=feat(normalise); S0=scores(A0, KF0); S_store['M0']=S0
A1=feat(norm_plain); S1=scores(A1, KF1); S_store['M1']=S1
A2=feat(norm_skel, rad=1); S2=scores(A2, KF2); S_store['M2']=S2
S_store['M3']=0.5*S0+0.5*S1
print("M0-M3 done", round(time.time()-t0,1), "s", flush=True)
rotS0=[]; rotS1=[]
for a in [-6,-4,-2,0,2,4,6]:
    rotS0.append(scores(feat(normalise, rot=a), KF0) if False else scores(feat(lambda m: norm_skel(m,2), rot=a), KF0))
    rotS1.append(scores(feat(norm_plain, rot=a), KF1))
    print(" rot", a, round(time.time()-t0,1), "s", flush=True)
S_store['M4']=np.max(np.stack(rotS0),axis=0); S_store['M5']=np.max(np.stack(rotS1),axis=0)
ids_v4=[str(x) for x in np.load('z340_v4_ids.npy',allow_pickle=True).ravel()]
for name,S in S_store.items():
    top,m=evaluate(S); results[name]=m
    results[name]['top1_ids']=[keyids[i] for i in top]
    print(f"{name}: tune={m['tune']:.3f} val={m['val']:.3f} all={m['all']:.3f}", flush=True)
sanity=sum(1 for p in range(340) if keyids[int(np.argmax(S_store['M0'][p]))]!=ids_v4[p])
print("sanity: M0 top-1 differs from v4 in", sanity, "cells", flush=True)
best=max(results, key=lambda n:(round(results[n]['tune'],6), n=='M0'))
print("selected by tuning set:", best, flush=True)
json.dump(dict(results={k:{kk:vv for kk,vv in v.items() if kk!='top1_ids'} for k,v in results.items()}, selected=best, sanity_diff_vs_v4=sanity), open('methods_results.json','w'), indent=1)
json.dump({k:v['top1_ids'] for k,v in results.items()}, open('methods_top1_ids.json','w'))
np.savez_compressed('methods_scores.npz', **{k:v for k,v in S_store.items()})
print("DONE", round(time.time()-t0,1), "s", flush=True)
