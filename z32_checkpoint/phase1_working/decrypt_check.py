import json, csv, re, numpy as np, difflib
txt = open('paged.txt',encoding='utf-8').read().split('\n')
block=[]; on=False
for line in txt:
    s=line.split(': ',1)[-1] if ': ' in line else line
    if s.strip().startswith('• I HOPE YOU'): on=True
    if on and s.strip().startswith('Figure 44'): break
    if on: block.append(s.strip().lstrip('• ').strip())
raw=' '.join(block)
raw=re.sub(r'\[([^:\]]+):\s*[^\]]+\]', r'\1', raw)          # keep the misspelt (left) form
raw=re.sub(r'\s+',' ',raw).strip()
raw_letters=re.sub(r'[^A-Z]','',raw.upper())
vals=json.load(open('trans_values_fixed.json'))['values']
grid=np.load('z340_grid_ids.npy',allow_pickle=True)
keyrows=list(csv.DictReader(open('key_table_glyphs.csv',encoding='utf-8')))
letter_of={r['glyph_id']:r['letter'] for r in keyrows}
pos={}
for idx,k in enumerate(vals): pos[k]=(idx//17, idx%17)
H=[grid[pos[k]] for k in range(340)]
dec=''.join(letter_of.get(h,'?') for h in H)
print("raw known text (letters):", len(raw_letters), raw_letters[:70])
print("decrypted letters     :", len(dec), dec[:70])
sm=difflib.SequenceMatcher(None, raw_letters, dec.replace('?',''))
print("similarity ratio:", round(sm.ratio(),3))
print("'?' (unidentified cells) in stream:", dec.count('?'))
# letter-level agreement on the aligned blocks
aligned=sum(b.size for b in sm.get_matching_blocks())
print("matched letters (aligned):", aligned, "of raw", len(raw_letters))
json.dump(dict(raw=raw_letters, dec=dec), open('decrypt_result.json','w'))
