import numpy as np, json
from PIL import Image
from scipy import ndimage as ndi
from sklearn.cluster import KMeans
im = np.asarray(Image.open('img/p01-000.png').convert('RGB')).astype(float)
R = im[...,0]
def components(thr, close, amin):
    ink = R < thr
    ink[:200,:]=False; ink[1480:,:]=False; ink[:, :95]=False; ink[:, 1190:]=False
    if close: ink = ndi.binary_closing(ink, structure=np.ones((3,3)), iterations=1)
    lab,n = ndi.label(ink); objs = ndi.find_objects(lab); comps=[]
    for i,sl in enumerate(objs,1):
        y0,y1=sl[0].start,sl[0].stop; x0,x1=sl[1].start,sl[1].stop
        h,w=y1-y0,x1-x0; area=int((lab[sl]==i).sum())
        if area<amin or h<14 or w<14 or h>115 or w>115: continue
        comps.append(dict(x0=x0,y0=y0,x1=x1,y1=y1,area=area,xc=(x0+x1)/2,yc=(y0+y1)/2))
    return comps
best=None
for thr in (110,125,140):
    for close in (False, True):
        for amin in (60,120):
            comps=components(thr,close,amin)
            ys=np.array([c['yc'] for c in comps]).reshape(-1,1)
            if len(comps)<20: continue
            lab_row=KMeans(n_clusters=20,n_init=10,random_state=0).fit(ys).labels_
            cnt=np.bincount(lab_row,minlength=20)
            score=abs(len(comps)-340)+sum(abs(c-17) for c in cnt)
            print(f"thr={thr} close={close} amin={amin}: comps={len(comps)} row-range={cnt.min()}-{cnt.max()} score={score}")
            if best is None or score<best[0]: best=(score,thr,close,amin,comps,lab_row)
score,thr,close,amin,comps,lab_row=best
print("BEST:",thr,close,amin,"comps",len(comps))
json.dump(dict(thr=thr,close=close,amin=amin,comps=comps,lab_row=[int(x) for x in lab_row]),open('z340_best.json','w'))
