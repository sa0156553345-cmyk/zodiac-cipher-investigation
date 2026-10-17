"""Matcher v2: aspect-preserving normalisation, 1-px dilation, Dice with +/-2 px shifts. Frozen before use."""
import numpy as np, csv, json
from PIL import Image
from scipy import ndimage as ndi
kg = np.asarray(Image.open('img/p31-002.png').convert('L')).astype(float)
pg = np.asarray(Image.open('img/p01-000.png').convert('RGB')).astype(float)[...,0]
def normalise(mask, size=44, canvas=52):
    ys,xs=np.where(mask)
    if len(ys)==0: return np.zeros((canvas,canvas),bool)
    crop=mask[ys.min():ys.max()+1, xs.min():xs.max()+1]
    h,w=crop.shape; s=size/max(h,w)
    im=Image.fromarray((crop*255).astype('uint8')).resize((max(1,int(round(w*s))),max(1,int(round(h*s)))),Image.BILINEAR)
    m=np.asarray(im)>127
    out=np.zeros((canvas,canvas),bool); oy=(canvas-m.shape[0])//2; ox=(canvas-m.shape[1])//2
    out[oy:oy+m.shape[0], ox:ox+m.shape[1]]=m
    return out
keyrows=list(csv.DictReader(open('key_table_glyphs.csv',encoding='utf-8')))
keyids=[r['glyph_id'] for r in keyrows]; letter_of={r['glyph_id']:r['letter'] for r in keyrows}
KM=[]
for r in keyrows:
    m=(kg[int(r['y0']):int(r['y1']), int(r['x0']):int(r['x1'])]<110)
    KM.append(ndi.binary_dilation(normalise(m), iterations=1))
KM=np.stack(KM)
def cell_mask(r,c,yr,xc):
    y=int(round(yr[r])); x=int(round(xc[c])); H=36
    win=pg[y-H:y+H, x-H:x+H] < (90 if True else 130)
    lab,n=ndi.label(win)
    if n==0: return None
    best=None; bd=1e9
    for i in range(1,n+1):
        yy,xx=np.where(lab==i)
        if len(yy)<40: continue
        d=np.min((yy-H)**2+(xx-H)**2)
        if d<bd: bd=d; best=i
    if best is None: return None
    return lab==best
yr=np.load('z340_yr.npy'); xc=np.load('z340_xc.npy')
def dice_shift(A, B):
    best=-1
    for dy in (-2,-1,0,1,2):
        for dx in (-2,-1,0,1,2):
            As=np.roll(np.roll(A,dy,0),dx,1)
            inter=(As&B).sum(); s=2*inter/(As.sum()+B.sum()+1e-9)
            best=max(best,s)
    return best
ids_grid=np.empty((20,17),dtype=object); margin=np.zeros((20,17)); score=np.zeros((20,17))
for r in range(20):
    for c in range(17):
        m=cell_mask(r,c,yr,xc)
        if m is None: ids_grid[r,c]='NA'; continue
        A=ndi.binary_dilation(normalise(m), iterations=1)
        s=np.array([dice_shift(A,KM[i]) for i in range(len(keyids))])
        o=np.argsort(s)[::-1]
        ids_grid[r,c]=keyids[o[0]]; score[r,c]=s[o[0]]; margin[r,c]=s[o[0]]-s[o[1]]
np.save('z340_v2_ids.npy', ids_grid); np.save('z340_v2_margin.npy', margin)
used=set(ids_grid.ravel())-{'NA'}
print("cells NA:", int(np.sum(ids_grid=='NA')), " distinct key IDs used:", len(used), "/ 63")
print("unused:", sorted(set(keyids)-used))
print("dice median/min:", round(float(np.median(score)),3), round(float(score.min()),3), " margin<0.03 cells:", int((margin<0.03).sum()))
# visual anchors (frozen before running): cell (1,1)->I01, (2,3)->H01, (3,5)->O04
anch={(0,0):'I01',(1,2):'H01',(2,4):'O04'}
for (r,c),want in anch.items():
    print(f"anchor cell row{r+1} col{c+1}: matched {ids_grid[r,c]}  expected {want}  ->", 'OK' if ids_grid[r,c]==want else 'MISMATCH')
