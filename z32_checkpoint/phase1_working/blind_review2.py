"""Blinded review v2: top-5 candidates per mismatch, tile positions AND labels shuffled independently."""
import numpy as np, json, csv, random
from PIL import Image, ImageDraw
src=open('match_v4.py',encoding='utf-8').read()
exec(src.split('ids_grid=np.empty')[0])
mm=list(csv.DictReader(open('mismatch_positions_v4.csv',encoding='utf-8')))[:10]
vals=json.load(open('trans_values_rowmajor.json'))['values']
pos={v:(p//17,p%17) for p,v in enumerate(vals)}
rowsdict={r['glyph_id']:r for r in csv.DictReader(open('key_table_glyphs.csv',encoding='utf-8'))}
rnd=random.Random(7731)
margin=np.load('z340_v4_margin.npy')
PH=np.asarray(Image.open('img/p01-000.png').convert('RGB')); KG=np.asarray(Image.open('img/p31-002.png').convert('RGB'))
hidden={}; rows_out=[]
for m in mm:
    k=int(m['k']); r,c=pos[k]
    A=ndi.binary_dilation(normalise(cell_mask(r,c,yr,xc)), iterations=1)
    s=np.array([dice_shift(A,KM[i]) for i in range(len(keyids))])
    top=np.argsort(s)[::-1][:5]
    order=list(range(5)); rnd.shuffle(order)            # display position -> rank index
    labels=[1,2,3,4,5]; rnd.shuffle(labels)              # display position -> visible label
    tiles=[]
    y=int(round(yr[r])); x=int(round(xc[c])); H=36
    tiles.append(('PHOTO', Image.fromarray(PH[y-H:y+H, x-H:x+H]).resize((150,150))))
    tile_map={}
    for dpos,ri in enumerate(order):
        kid=keyids[top[ri]]; rr=rowsdict[kid]
        crop=Image.fromarray(KG[max(0,int(rr['y0'])-6):int(rr['y1'])+6, max(0,int(rr['x0'])-6):int(rr['x1'])+6]); crop.thumbnail((150,150))
        canvas=Image.new('RGB',(150,150),(255,255,255)); canvas.paste(crop,((150-crop.size[0])//2,(150-crop.size[1])//2))
        lab=labels[dpos]; tiles.append((f'cand {lab}',canvas)); tile_map[str(lab)]=dict(id=kid, rank=ri+1, score=round(float(s[top[ri]]),3))
    hidden[k]=dict(cell=[r+1,c+1], margin=round(float(margin[r,c]),3), tiles=tile_map)
    rows_out.append((k,tiles))
json.dump(hidden,open('blind2_hidden_map.json','w'),ensure_ascii=False,indent=1)
sheet=Image.new('RGB',(6*160, len(rows_out)*172+10),(255,255,255)); d=ImageDraw.Draw(sheet)
for i,(k,tiles) in enumerate(rows_out):
    y0=i*172+18
    d.text((4,y0-16),f"review row {i+1}  (cell r{hidden[k]['cell'][0]}c{hidden[k]['cell'][1]})",fill=(0,0,0))
    for j,(lab,im) in enumerate(tiles):
        sheet.paste(im,(j*160,y0)); d.text((j*160+4,y0+152),lab,fill=(0,0,0))
sheet.save('blind_review2_first10.png'); print("saved; rows:",len(rows_out))
