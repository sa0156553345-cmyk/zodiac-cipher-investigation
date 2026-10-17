import json
from collections import Counter
d = json.load(open('trans_numbers.json'))
# visual readings verified on the enlarged crops (trans_suspect_small.png); index -> true value
fixes = {58:97, 65:7, 121:171, 124:198, 150:41, 199:193, 240:1, 250:91, 253:118, 263:4, 264:13, 314:123, 316:141, 323:119}
vals = []
for k,o in enumerate(d):
    v = fixes.get(k, int(o['value']) if o['value'].isdigit() else None)
    vals.append(v)
assert None not in vals, "unresolved cell"
c = Counter(vals)
missing = sorted(set(range(340)) - set(vals)); extra = sorted(v for v in c if c[v] > 1 or v > 339)
print("permutation check -> missing:", missing, " duplicates/out-of-range:", extra)
json.dump(dict(values=vals, corrections=fixes), open('trans_values_fixed.json','w'))
