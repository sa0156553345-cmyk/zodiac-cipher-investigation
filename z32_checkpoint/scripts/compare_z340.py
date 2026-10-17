"""Decrypt Z340 with (a) reading order from Figure 43 values and (b) matcher v4 IDs; compare with reference plaintext."""
import json, csv, re, difflib, numpy as np
paged=open('paged.txt',encoding='utf-8').read().split('\n')
def clean(s): return re.sub(r'[^A-Z]','',re.sub(r'\[([^:\]]+):[^\]]+\]', r'\1', s).upper())
# block 1: bullet list (already extracted and stored)
ref1=json.load(open('decrypt_result.json'))['raw']
# block 2: lines from 'OF DEATH I AM NOT AFRAID' until 'LIFE IS DEATH'
i0=next(i for i,l in enumerate(paged) if 'OF DEATH I AM NOT AFRAID' in l)
i1=next(i for i in range(i0,len(paged)) if 'LIFE IS DEATH' in paged[i])
block2=' '.join(re.sub(r'^\d+: ','',l) for l in paged[i0:i1+1])
ref2=clean(block2)
ref=ref1+ref2
vals=json.load(open('trans_values_rowmajor.json'))['values']
ids=np.load('z340_v4_ids.npy',allow_pickle=True)
rows=list(csv.DictReader(open('key_table_glyphs.csv',encoding='utf-8')))
letter={r['glyph_id']:r['letter'] for r in rows}
pos={v:(p//17,p%17) for p,v in enumerate(vals)}
ids_stream=[ids[pos[k]] for k in range(340)]
dec=''.join(letter.get(g,'?') for g in ids_stream)
print("reference letters:", len(ref), " (block1", len(ref1), "+ block2", len(ref2), ")")
print("decrypted symbols:", len(dec))
print("first 40 decrypted:", dec[:40])
print("first 40 reference:", ref[:40])
n=min(len(dec),len(ref))
pos_acc=sum(1 for k in range(n) if dec[k]==ref[k])/n
ratio=difflib.SequenceMatcher(None, ref, dec).ratio()
first_bad=next((k for k in range(n) if dec[k]!=ref[k]),None)
print(f"position-wise agreement: {pos_acc:.3f}   SequenceMatcher ratio: {ratio:.3f}")
print("first mismatch at symbol index:", first_bad, " decrypted:", dec[first_bad] if first_bad is not None else None, " reference:", ref[first_bad] if first_bad is not None else None)
amb=[(k,str(ids_stream[k])) for k in range(340) if float(np.load('z340_v4_margin.npy')[pos[k]])<0.03]
print("symbols at low-margin cells (<0.03):", len(amb))
json.dump(dict(ref_len=len(ref), dec_len=len(dec), pos_acc=pos_acc, ratio=ratio, first_bad=first_bad,
               dec=dec, ref=ref, ids_stream=[str(x) for x in ids_stream], low_margin_symbols=amb),
          open('compare_z340_v4.json','w'), ensure_ascii=False)
