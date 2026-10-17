import numpy as np, json, csv
from PIL import Image
from scipy import ndimage as ndi
from sklearn.cluster import KMeans
im = np.asarray(Image.open('img/p01-000.png').convert('RGB')).astype(float)
R,G,B = im[...,0], im[...,1], im[...,2]
# sample background vs ink to choose threshold on red channel (blue ink has low red)
print("R percentiles:", [int(np.percentile(R,p)) for p in (2,5,10,50,90)])
ink = R < 110
ink[:200,:]=False; ink[1480:,:]=False; ink[:, :95]=False; ink[:, 1190:]=False
lab,n = ndi.label(ink)
objs = ndi.find_objects(lab)
comps=[]
for i,sl in enumerate(objs,1):
    y0,y1=sl[0].start,sl[0].stop; x0,x1=sl[1].start,sl[1].stop
    h,w=y1-y0,x1-x0; area=int((lab[sl]==i).sum())
    if area<120 or h<12 or w<12 or h>110 or w>110: continue
    comps.append(dict(x0=x0,y0=y0,x1=x1,y1=y1,area=area,xc=(x0+x1)/2,yc=(y0+y1)/2))
print("glyph-like components:", len(comps))
ys=np.array([c['yc'] for c in comps]).reshape(-1,1)
km=KMeans(n_clusters=20,n_init=10,random_state=0).fit(ys)
lab_row=km.labels_
rows=[]
for r in range(20):
    members=[c for c,l in zip(comps,lab_row) if l==r]
    rows.append(sorted(members,key=lambda c:c['xc']))
# order rows top->bottom
order=np.argsort([np.mean([c['yc'] for c in rw]) for rw in rows])
rows=[rows[i] for i in order]
print("per-row counts:", [len(r) for r in rows])
json.dump([[dict(c) for c in r] for r in rows], open('z340_components.json','w'))
