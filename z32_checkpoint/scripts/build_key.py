import numpy as np, json, csv
from PIL import Image, ImageDraw
g = np.asarray(Image.open('img/p31-002.png').convert('L')).astype(float)
ink = g < 110
boxes = json.load(open('key_glyph_boxes3.json'))
# split any segment that is abnormally wide by its deepest ink valley
widths = sorted(b['x1']-b['x0'] for b in boxes)
med = widths[len(widths)//2]
final = []
for b in boxes:
    w = b['x1']-b['x0']
    if w > 1.8*med:
        col = ink[b['y0']:b['y1'], b['x0']:b['x1']].sum(0).astype(float)
        cut = int(np.argmin(col[int(w*0.3):int(w*0.7)]) + int(w*0.3))
        final.append(dict(b, x1=b['x0']+cut)); final.append(dict(b, x0=b['x0']+cut))
        print("split", b['letter'], b['row'], "width", w, "at", cut)
    else:
        final.append(b)
order = {}
final.sort(key=lambda d: (d['block'], d['row'], d['x0']))
letters_all = sum([list("ABCDEFG"), list("HILMNOP"), list("RSTUVWY")], [])
counts = {}
for d in final:
    counts[d['letter']] = counts.get(d['letter'],0)+1
    d['id'] = f"{d['letter']}{counts[d['letter']]:02d}"
print("total glyphs:", len(final))
print("per letter:", {k: counts.get(k,0) for k in letters_all})
# templates: 48x48 cleaned binary crops, scaled to fit bounding box
T = []
for d in final:
    crop = (ink[d['y0']:d['y1'], d['x0']:d['x1']]).astype(np.uint8)*255
    im = Image.fromarray(crop).resize((48,48), Image.BILINEAR)
    T.append(np.asarray(im).astype(float))
T = np.stack(T)
np.save('key_templates48.npy', T)
with open('key_table_glyphs.csv','w',newline='',encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['glyph_id','letter','block','row','x0','y0','x1','y1','ink_area'])
    for d in final: w.writerow([d['id'],d['letter'],d['block'],d['row'],d['x0'],d['y0'],d['x1'],d['y1'],d['area']])
# atlas
tiles=[]
cols=11; rows=(len(final)+cols-1)//cols
sheet = Image.new('L',(cols*96, rows*112),255); dr=ImageDraw.Draw(sheet)
for k,d in enumerate(final):
    im = Image.fromarray(g[d['y0']-2:d['y1']+2, d['x0']-2:d['x1']+2].astype('uint8')).resize((86,86))
    x=(k%cols)*96+5; y=(k//cols)*112+3
    sheet.paste(im,(x,y)); dr.text((x,y+90), d['id'], fill=0)
sheet.save('key_atlas_final.png'); print("atlas", sheet.size)
