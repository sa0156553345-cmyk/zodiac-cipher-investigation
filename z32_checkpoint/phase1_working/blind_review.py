"""Blinded visual review of the first 10 mismatches. Candidates are shown with random numeric labels only.
Matcher v4 functions are reused by exec of its definition block (no plaintext used)."""
import numpy as np, json, csv, random
from PIL import Image, ImageDraw
src=open('match_v4.py',encoding='utf-8').read()
exec(src.split('ids_grid=np.empty')[0])             # loads KM, keyids, cell_mask, normalise, dice_shift, yr, xc
mm=list(csv.DictReader(open('mismatch_positions_v4.csv',encoding='utf-8')))[:10]
vals=json.load(open('trans_values_rowmajor.json'))['values']
pos={v:(p//17,p%17) for p,v in enumerate(vals)}
margin=np.load('z340_v4_margin.npy')
rowsdict={r['glyph_id']:r for r in csv.DictReader(open('key_table_glyphs.csv',encoding='utf-8'))}
rnd=random.Random(20261015)
hidden={}; tiles=[]
for m in mm:
    k=int(m['k']); r,c=pos[k]
    mask=cell_mask(r,c,yr,xc)
    A=ndi.binary_dilation(normalise(mask), iterations=1)
    s=np.array([dice_shift(A,KM[i]) for i in range(len(keyids))])
    top=np.argsort(s)[::-1][:3]
    cands=[keyids[i] for i in top]
    labels=[1,2,3]; rnd.shuffle(labels)
    hidden[k]=dict(cell=[r+1,c+1], margin=round(float(margin[r,c]),3),
                   label_to_id={str(labels[j]):cands[j] for j in range(3)},
                   scores={cands[j]:round(float(s[top[j]]),3) for j in range(3)})
    # photo cell (RGB, enlarged)
    y=int(round(yr[r])); x=int(round(xc[c])); H=36
    cell_img=Image.fromarray(np.asarray(Image.open('img/p01-000.png').convert('RGB'))[y-H:y+H, x-H:x+H]).resize((150,150))
    row_tiles=[('cell',cell_img)]
    for j in range(3):
        rr=rowsdict[cands[j]]
        crop=Image.fromarray(np.asarray(Image.open('img/p31-002.png').convert('RGB'))[max(0,int(rr['y0'])-6):int(rr['y1'])+6, max(0,int(rr['x0'])-6):int(rr['x1'])+6])
        crop.thumbnail((150,150))
        canvas=Image.new('RGB',(150,150),(255,255,255)); canvas.paste(crop,((150-crop.size[0])//2,(150-crop.size[1])//2))
        row_tiles.append((str(labels[j]),canvas))
    tiles.append((k,row_tiles))
json.dump(hidden,open('blind_hidden_map.json','w'),ensure_ascii=False,indent=1)
W=4*160; Hh=len(tiles)*170+10
sheet=Image.new('RGB',(W,Hh),(255,255,255)); d=ImageDraw.Draw(sheet)
for i,(k,rt) in enumerate(tiles):
    y0=i*170+20
    d.text((4,y0-16),f"k={k}  (cell r{hidden[k]['cell'][0]}c{hidden[k]['cell'][1]})",fill=(0,0,0))
    for j,(lab,im) in enumerate(rt):
        sheet.paste(im,(j*160,y0))
        d.text((j*160+4,y0+152), 'PHOTO' if lab=='cell' else f'cand {lab}', fill=(0,0,0))
sheet.save('blind_review_first10.png')
print("rows:",len(tiles)); print("margins (first 10):",[hidden[k]['margin'] for k in hidden])
