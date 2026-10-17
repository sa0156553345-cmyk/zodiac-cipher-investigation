import numpy as np, subprocess, json
from PIL import Image
from scipy import ndimage as ndi
from sklearn.cluster import KMeans
im=np.asarray(Image.open('img/p31-001.png').convert('RGB')).astype(int)
white=(im[...,0]>195)&(im[...,1]>195)&(im[...,2]>195)
lab,n=ndi.label(white)
comps=[]
for i,sl in enumerate(ndi.find_objects(lab),1):
    a=int((lab[sl]==i).sum())
    if a<15: continue
    comps.append((sl[0].start,sl[0].stop,sl[1].start,sl[1].stop))
# group glyph components into numbers: same row band and horizontal gap <=6 px
comps.sort(key=lambda c:(c[0]+c[1])/2)
ycs=np.array([(c[0]+c[1])/2 for c in comps]).reshape(-1,1)
km=KMeans(20,n_init=10,random_state=0).fit(ycs)
groups=[]
for r in range(20):
    members=[c for c,l in zip(comps,km.labels_) if l==r]
    members.sort(key=lambda c:c[2])
    cur=[]
    for c in members:
        if cur and c[2]-cur[-1][3] <= 12: cur.append(c)
        else:
            if cur: groups.append((r,cur))
            cur=[c]
    if cur: groups.append((r,cur))
cnt=np.bincount([g[0] for g in groups],minlength=20)
print("numbers per row:", cnt.tolist(), " total:", len(groups))
out=[]
for r,mem in groups:
    y0=min(m[0] for m in mem)-6; y1=max(m[1] for m in mem)+6; x0=min(m[2] for m in mem)-6; x1=max(m[3] for m in mem)+6
    crop=(~white[y0:y1,x0:x1]).astype(np.uint8)*255   # black digits on white
    Image.fromarray(crop).save('tmp_num.png')
    txt=subprocess.run(['tesseract','tmp_num.png','-','--psm','8','-c','tessedit_char_whitelist=0123456789'],capture_output=True,text=True).stdout.strip()
    out.append(dict(row=r,x0=int(x0),value=txt))
json.dump(out,open('trans_numbers.json','w'))
vals=[int(o['value']) for o in out if o['value'].isdigit()]
print("parsed:", len(vals), "of", len(out), " unique:", len(set(vals)), " missing:", sorted(set(range(340))-set(vals))[:15], " dup:", sorted({v for v in vals if vals.count(v)>1})[:15])
