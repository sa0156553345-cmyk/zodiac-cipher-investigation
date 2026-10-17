"""Sensitivity of the v4 scoring to: crop window size (30/36/42 px), in-plane rotation (+/-4 deg),
and cell overlap/cropping flags. Same scoring code as match_v4 (definitions reused)."""
import numpy as np, json
from scipy import ndimage as ndi
from skimage.filters import threshold_otsu
src=open('match_v4.py',encoding='utf-8').read()
exec(src.split('ids_grid=np.empty')[0])
def mask_H(r,c,H):
    y=int(round(yr[r])); x=int(round(xc[c]))
    patch=pg[y-H:y+H, x-H:x+H]; t=threshold_otsu(patch); win=patch<t
    lab,n=ndi.label(win)
    best=None; bd=1e9
    for i in range(1,n+1):
        yy,xx=np.where(lab==i)
        if len(yy)<40: continue
        d=np.min((yy-H)**2+(xx-H)**2)
        if d<bd: bd=d; best=i
    if best is None: return None, None, None
    sel=(lab==best)
    return sel, lab, best
def top1_from_mask(m):
    A=ndi.binary_dilation(normalise(m), iterations=1)
    s=np.array([dice_shift(A,KM[i]) for i in range(63)])
    return int(np.argmax(s)), s
base_ids=np.load('z340_v4_ids.npy',allow_pickle=True)
res={'window30':{}, 'window42':{}, 'rot+4':{}, 'rot-4':{}}
flags={}
for r in range(20):
    for c in range(17):
        p=r*17+c
        sel36, lab36, best36 = mask_H(r,c,36)
        if sel36 is None: continue
        ys,xs=np.where(sel36)
        border = bool(sel36[0].any() or sel36[-1].any() or sel36[:,0].any() or sel36[:,-1].any())
        dist=ndi.distance_transform_edt(~sel36)
        others=(lab36>0)&(~sel36)
        for i in range(1,lab36.max()+1):
            pass
        close=False
        if others.any():
            ids_other=np.unique(lab36[others])
            for j in ids_other:
                if (lab36==j).sum()>=40 and dist[lab36==j].min()<=6: close=True; break
        flags[p]=dict(border=border, close_neighbour=close, area=int(sel36.sum()))
        base=int(np.argmax(dice_shift_vec := None) if False else 0)
        i36,_=top1_from_mask(sel36)
        for key,H in [('window30',30),('window42',42)]:
            sel, _, _ = mask_H(r,c,H)
            if sel is None: res[key][p]=None; continue
            i,_=top1_from_mask(sel); res[key][p]=i
        for key,ang in [('rot+4',4),('rot-4',-4)]:
            rot=ndi.rotate(sel36.astype(float), ang, reshape=False, order=1)>0.5
            i,_=top1_from_mask(rot); res[key][p]=i
        res.setdefault('base36',{})[p]=i36
summary={}
for key in ['window30','window42','rot+4','rot-4']:
    changed=[p for p in res['base36'] if res[key].get(p) is not None and res[key][p]!=res['base36'][p]]
    summary[key]=dict(cells=len(res['base36']), top1_changed=len(changed), changed_cells=changed)
    print(f"{key:>9}: top-1 changed in {len(changed):3d} of {len(res['base36'])} cells")
bd=sum(1 for f in flags.values() if f['border']); cl=sum(1 for f in flags.values() if f['close_neighbour'])
print(f"cells whose selected component touches the 72x72 window border: {bd}")
print(f"cells with another glyph-sized component within 6 px: {cl}")
json.dump(dict(summary=summary, flags={str(k):v for k,v in flags.items()}, base36={str(k):v for k,v in res['base36'].items()}), open('robustness_results.json','w'))
