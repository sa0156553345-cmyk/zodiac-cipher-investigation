import numpy as np, csv
from PIL import Image
from scipy import ndimage as ndi
from scipy.ndimage import gaussian_filter
im=np.asarray(Image.open('img/p01-000.png').convert('RGB')).astype(float); R=im[...,0]
yr=np.load('z340_yr.npy'); xc=np.load('z340_xc.npy'); inkc=np.load('z340_inkcell.npy')
T=np.load('key_templates48.npy')                      # 63 x 48 x 48 (0/255 cleaned glyphs)
ids=[r['glyph_id'] for r in csv.DictReader(open('key_table_glyphs.csv',encoding='utf-8'))]
def glyph_from_cell(r,c,thr):
    y=int(round(yr[r])); x=int(round(xc[c])); H=36
    win=R[y-H:y+H, x-H:x+H] < thr
    lab,n=ndi.label(win)
    if n==0: return None
    # component nearest to the window centre
    cy,cx=H,H; best=None; bd=1e9
    for i,sl in enumerate(ndi.find_objects(lab),1):
        a=int((lab[sl]==i).sum())
        if a<40: continue
        yy,xx=np.where(lab==i); d=np.min((yy-cy)**2+(xx-cx)**2)
        if d<bd: bd=d; best=(i,sl)
    if best is None: return None
    i,sl=best; mask=(lab[sl]==i)
    pad=max(mask.shape)
    canvas=np.zeros((pad,pad)); oy=(pad-mask.shape[0])//2; ox=(pad-mask.shape[1])//2
    canvas[oy:oy+mask.shape[0], ox:ox+mask.shape[1]]=mask
    return np.asarray(Image.fromarray((canvas*255).astype('uint8')).resize((48,48),Image.BILINEAR)).astype(float)
def prep(a):
    a=gaussian_filter(a,2.0); a=a-a.mean(); n=np.linalg.norm(a); return a/(n+1e-9)
TP=np.stack([prep(t).ravel() for t in T])
rows=[]; grid=np.empty((20,17),dtype=object); margins=np.zeros((20,17)); scores=np.zeros((20,17))
for r in range(20):
    for c in range(17):
        thr=90 if inkc[r,c]>=30 else 130
        g=glyph_from_cell(r,c,thr)
        if g is None:
            grid[r,c]='NA'; scores[r,c]=-1; margins[r,c]=0; continue
        p=prep(g).ravel(); s=TP@p
        o=np.argsort(s)[::-1]
        grid[r,c]=ids[o[0]]; scores[r,c]=s[o[0]]; margins[r,c]=s[o[0]]-s[o[1]]
        rows.append(dict(row=r+1,col=c+1,best=ids[o[0]],score=round(float(s[o[0]]),3),second=ids[o[1]],second_score=round(float(s[o[1]]),3),margin=round(float(s[o[0]]-s[o[1]]),3),ink=int(inkc[r,c])))
with open('z340_cipher_grid.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
na=int(sum(1 for r in range(20) for c in range(17) if grid[r,c]=='NA'))
used=set(grid.ravel())-{'NA'}
print("cells NA:",na," distinct key IDs used:",len(used),"of 63")
print("score median/min:", round(float(np.median(scores)),3), round(float(scores.min()),3))
print("margin median/min:", round(float(np.median(margins)),3), round(float(margins.min()),3), " low-margin(<0.05) cells:", int((margins<0.05).sum()))
print("unused key IDs:", sorted(set(ids)-used))
np.save('z340_grid_ids.npy',grid); np.save('z340_grid_margin.npy',margins)
for r in range(0,20,5): print("row",r+1,":", " ".join(str(grid[r,c]) for c in range(17)))
