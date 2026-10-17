"""Segment Figure-44 key image (img/p31-002.png) into individual glyphs; assign to letters by layout."""
import numpy as np, csv, json
from PIL import Image
from scipy import ndimage as ndi
g = np.asarray(Image.open('img/p31-002.png').convert('L')).astype(float)
H, W = g.shape
ink = g < 110
lab, n = ndi.label(ink)
objs = ndi.find_objects(lab)
comps = []
for i, sl in enumerate(objs, start=1):
    y0, y1 = sl[0].start, sl[0].stop; x0, x1 = sl[1].start, sl[1].stop
    h, w = y1-y0, x1-x0; area = int((lab[sl]==i).sum())
    if h > 300 or w > 1400 or h > 600: continue          # separators / border
    if area < 25: continue                                 # specks
    comps.append(dict(x0=x0,y0=y0,x1=x1,y1=y1,area=area))
# merge components that are close (same glyph) using expanded boxes
n_c = len(comps); parent = list(range(n_c))
def find(a):
    while parent[a]!=a: parent[a]=parent[parent[a]]; a=parent[a]
    return a
for a in range(n_c):
    for b in range(a+1, n_c):
        A, B = comps[a], comps[b]
        gap_x = max(B['x0']-A['x1'], A['x0']-B['x1'], 0)
        gap_y = max(B['y0']-A['y1'], A['y0']-B['y1'], 0)
        if gap_x <= 7 and gap_y <= 7:
            parent[find(a)] = find(b)
groups = {}
for a in range(n_c): groups.setdefault(find(a), []).append(comps[a])
glyphs = []
for members in groups.values():
    x0=min(m['x0'] for m in members); x1=max(m['x1'] for m in members)
    y0=min(m['y0'] for m in members); y1=max(m['y1'] for m in members)
    glyphs.append(dict(x0=x0,y0=y0,x1=x1,y1=y1,xc=(x0+x1)/2,yc=(y0+y1)/2,area=sum(m['area'] for m in members)))
# block assignment by x (separators at ~115, ~650, ~1172)
def block(xc):
    return 0 if xc < 650 else (1 if xc < 1172 else 2)
letters = [list("ABCDEFG"), list("HILMNOP"), list("RSTUVWY")]
out = []
for b in range(3):
    gb = [gl for gl in glyphs if block(gl['xc'])==b and gl['area']>=60]
    ys = np.array([gl['yc'] for gl in gb])
    # 1-D k-means with k=7 on y-centres
    cent = np.linspace(ys.min(), ys.max(), 7)
    for _ in range(50):
        d = np.abs(ys[:,None]-cent[None,:]); a = d.argmin(1)
        cent = np.array([ys[a==k].mean() if (a==k).any() else cent[k] for k in range(7)])
    order = np.argsort(cent)           # top-to-bottom rows
    row_of = {int(order[k]):k for k in range(7)}
    for gi, gl in enumerate(gb):
        r = row_of[int(a[gi])]
        out.append(dict(block=b, row=r, letter=letters[b][r], x0=gl['x0'],y0=gl['y0'],x1=gl['x1'],y1=gl['y1'],area=gl['area']))
for letter in sum(letters, []):
    pass
# order glyphs within each letter by x
out.sort(key=lambda d: (d['block'], d['row'], d['x0']))
counts = {}
for d in out: counts[d['letter']] = counts.get(d['letter'],0)+1
for d in out: d['idx'] = sum(1 for e in out[:out.index(d)] if e['letter']==d['letter'])+1
exp = dict(A=5,B=2,C=1,D=3,E=6,F=1,G=1,H=1,I=5,L=3,M=1,N=5,O=4,P=2,R=5,S=4,T=6,U=3,V=1,W=2,Y=2)
print("total glyphs:", len(out))
print("counts  :", {k:counts.get(k,0) for k in sum(letters,[])})
print("visual  :", exp)
print("mismatch:", {k:(counts.get(k,0),exp[k]) for k in exp if counts.get(k,0)!=exp[k]})
json.dump(out, open('key_glyph_boxes.json','w'), ensure_ascii=False, indent=0)
# contact sheet for visual verification
tiles=[]
for d in out:
    crop = Image.fromarray(g[d['y0']-3:d['y1']+3, d['x0']-3:d['x1']+3].astype('uint8')).resize((90,90))
    tiles.append((d, crop))
cols=12; rows=(len(tiles)+cols-1)//cols
sheet = Image.new('L', (cols*100, rows*115), 255)
from PIL import ImageDraw
dr = ImageDraw.Draw(sheet)
for k,(d,t) in enumerate(tiles):
    x=(k%cols)*100+5; y=(k//cols)*115+5
    sheet.paste(t,(x,y)); dr.text((x,y+92), f"{d['letter']}{d['idx']}", fill=0)
sheet.save('key_atlas.png'); print("atlas saved", sheet.size)
