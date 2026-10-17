"""Projection-based segmentation of Figure-44 key rows (block x-ranges exclude separators)."""
import numpy as np, json
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
g = np.asarray(Image.open('img/p31-002.png').convert('L')).astype(float)
ink = g < 110
blocks = {0:(125,640), 1:(660,1160), 2:(1180,1600)}
letters = [list("ABCDEFG"), list("HILMNOP"), list("RSTUVWY")]
# row bands: horizontal projection over each block
out = []
for b,(xa,xb) in blocks.items():
    sub = ink[:, xa:xb]
    rowsum = sub.sum(1)
    on = rowsum > 0
    bands=[]; y=0
    while y < len(on):
        if on[y]:
            s=y
            while y < len(on) and on[y]: y+=1
            bands.append((s,y))
        y+=1
    # merge tiny gaps between bands, keep bands tall enough
    bands=[bd for bd in bands if bd[1]-bd[0] > 25]
    if len(bands)!=7:
        print("block",b,"bands found:",len(bands), bands)
    for r,(ya,yb) in enumerate(bands[:7]):
        colsum = ink[ya:yb, xa:xb].sum(0) > 0
        segs=[]; x=0
        while x < len(colsum):
            if colsum[x]:
                s=x
                while x < len(colsum) and colsum[x]: x+=1
                segs.append([s,x])
            x+=1
        # merge segments separated by <=2 px (same glyph hairline gaps)
        merged=[]
        for s in segs:
            if merged and s[0]-merged[-1][1] <= 2: merged[-1][1]=s[1]
            else: merged.append(s)
        merged=[m for m in merged if m[1]-m[0] >= 6]
        for m in merged:
            sub2 = ink[ya:yb, xa+m[0]:xa+m[1]]
            yy = np.where(sub2.sum(1)>0)[0]
            out.append(dict(block=b,row=r,letter=letters[b][r],x0=xa+m[0],x1=xa+m[1],y0=ya+int(yy.min()),y1=ya+int(yy.max())+1,area=int(sub2.sum())))
counts={}
for d in out: counts[d['letter']]=counts.get(d['letter'],0)+1
exp=dict(A=5,B=2,C=1,D=3,E=6,F=1,G=1,H=1,I=5,L=3,M=1,N=5,O=4,P=2,R=5,S=4,T=6,U=3,V=1,W=2,Y=2)
print("total:",len(out))
print("counts:",{k:counts.get(k,0) for k in sum(letters,[])})
print("mismatch:",{k:(counts.get(k,0),exp[k]) for k in exp if counts.get(k,0)!=exp[k]})
json.dump(out,open('key_glyph_boxes2.json','w'))
