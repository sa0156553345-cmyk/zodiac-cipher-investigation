import numpy as np, json
from PIL import Image
from scipy import ndimage as ndi
from sklearn.cluster import KMeans
im=np.asarray(Image.open('img/p01-000.png').convert('RGB')).astype(float); R=im[...,0]
ink=R<90; ink[:200,:]=False; ink[1480:,:]=False; ink[:,:95]=False; ink[:,1190:]=False
lab,n=ndi.label(ink); cents=[]
for i,sl in enumerate(ndi.find_objects(lab),1):
    a=int((lab[sl]==i).sum())
    if a<60: continue
    y0,y1=sl[0].start,sl[0].stop; x0,x1=sl[1].start,sl[1].stop
    if (y1-y0)<12 or (x1-x0)<12: continue
    cents.append(((y0+y1)/2,(x0+x1)/2))
cents=np.array(cents)
yr=np.sort(KMeans(20,n_init=10,random_state=0).fit(cents[:,0].reshape(-1,1)).cluster_centers_.ravel())
xc=np.sort(KMeans(17,n_init=10,random_state=0).fit(cents[:,1].reshape(-1,1)).cluster_centers_.ravel())
print("row centre spacing (median):", round(float(np.median(np.diff(yr))),1), " min/max diff:", round(float(np.min(np.diff(yr))),1), round(float(np.max(np.diff(yr))),1))
print("col centre spacing (median):", round(float(np.median(np.diff(xc))),1), " min/max diff:", round(float(np.min(np.diff(xc))),1), round(float(np.max(np.diff(xc))),1))
# cell ink content in window around each grid node
H=28; ink_cell=np.zeros((20,17),int)
for r in range(20):
    for c in range(17):
        y=int(round(yr[r])); x=int(round(xc[c]))
        ink_cell[r,c]=int(ink[y-H:y+H, x-H:x+H].sum())
print("cells with ink<30 (possibly empty):", int((ink_cell<30).sum()), " min/median ink:", int(ink_cell.min()), int(np.median(ink_cell)))
np.save('z340_yr.npy',yr); np.save('z340_xc.npy',xc); np.save('z340_inkcell.npy',ink_cell)
