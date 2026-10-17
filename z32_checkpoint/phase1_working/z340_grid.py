import numpy as np, json
from PIL import Image
from scipy import ndimage as ndi
from sklearn.cluster import KMeans
im=np.asarray(Image.open('img/p01-000.png').convert('RGB')).astype(float); R=im[...,0]
def comps_at(thr, amin=60):
    ink=R<thr; ink[:200,:]=False; ink[1480:,:]=False; ink[:,:95]=False; ink[:,1190:]=False
    lab,n=ndi.label(ink); out=[]
    for i,sl in enumerate(ndi.find_objects(lab),1):
        a=int((lab[sl]==i).sum()); y0,y1=sl[0].start,sl[0].stop; x0,x1=sl[1].start,sl[1].stop
        if a<amin or (y1-y0)<12 or (x1-x0)<12: continue
        out.append(dict(x0=x0,y0=y0,x1=x1,y1=y1,area=a,xc=(x0+x1)/2,yc=(y0+y1)/2))
    return out
results={}
for thr in (70,80,90,100):
    c=comps_at(thr)
    km=KMeans(n_clusters=20,n_init=10,random_state=0).fit(np.array([x['yc'] for x in c]).reshape(-1,1))
    cnt=np.bincount(km.labels_,minlength=20)
    results[thr]=(len(c),int(cnt.min()),int(cnt.max()),int(np.sum(cnt==17)))
    print(f"thr={thr}: comps={len(c)} rows min/max={cnt.min()}/{cnt.max()} rows==17: {int(np.sum(cnt==17))}")
best=min(results,key=lambda t: abs(results[t][0]-340)+ (20-results[t][3])*5)
print("chosen thr:",best)
c=comps_at(best); json.dump(dict(thr=best,comps=c),open('z340_comps_final.json','w'))
