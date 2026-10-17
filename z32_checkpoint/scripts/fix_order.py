import numpy as np, json
from PIL import Image
from scipy import ndimage as ndi
from sklearn.cluster import KMeans
rgb=np.asarray(Image.open('img/p31-001.png').convert('RGB')); im=rgb.astype(int)
white=(im[...,0]>195)&(im[...,1]>195)&(im[...,2]>195)
lab,n=ndi.label(white); comps=[]
for i,sl in enumerate(ndi.find_objects(lab),1):
    a=int((lab[sl]==i).sum()); h=sl[0].stop-sl[0].start; w=sl[1].stop-sl[1].start
    if a<15 or a>600 or h>60 or w>80: continue
    comps.append((sl[0].start,sl[0].stop,sl[1].start,sl[1].stop))
comps.sort(key=lambda c:(c[0]+c[1])/2)
km=KMeans(20,n_init=10,random_state=0).fit(np.array([(c[0]+c[1])/2 for c in comps]).reshape(-1,1))
groups=[]  # same order as trans_numbers.json was built (cluster label, then x)
for r in range(20):
    mem=sorted([c for c,l in zip(comps,km.labels_) if l==r],key=lambda c:c[2]); cur=[]
    for c in mem:
        if cur and c[2]-cur[-1][3]<=12: cur.append(c)
        else:
            if cur: groups.append((r,cur))
            cur=[c]
    if cur: groups.append((r,cur))
assert len(groups)==340
cy=[np.mean([ (m[0]+m[1])/2 for m in g[1]]) for g in groups]
label=[g[0] for g in groups]; x0=[min(m[2] for m in g[1]) for g in groups]
rank_of_label={}
centres={r: np.mean([cy[i] for i in range(340) if label[i]==r]) for r in range(20)}
for rank,r in enumerate(sorted(range(20), key=lambda r: centres[r])): rank_of_label[r]=rank
new_order=sorted(range(340), key=lambda i:(rank_of_label[label[i]], x0[i]))
# check geometry: rows should now be monotone in y
ys_new=[cy[i] for i in new_order]
print("row-major y monotone across rows:", all(ys_new[k] <= ys_new[k+1]+1e-6 or (k+1)%17==0 for k in range(339)))
json.dump(dict(new_order=new_order), open('trans_order.json','w'))
old=json.load(open('trans_values_fixed.json'))
fixes_old=old['corrections']  # keyed by old index (string)
vals_old=old['values']
vals_new=[None]*340
for pos,i in enumerate(new_order): vals_new[pos]=vals_old[i]
print("first row values now:", vals_new[:17])
print("permutation ok:", sorted(vals_new)==list(range(340)))
json.dump(dict(values=vals_new), open('trans_values_rowmajor.json','w'))
