"""Independent check of the row-major transposition numbers against the paper's definition (sections + (1,2)-decimation)."""
import json
vals = json.load(open('trans_values_rowmajor.json'))['values']
num = [[vals[r*17+c] for c in range(17)] for r in range(20)]
def k_of(res_row, col, nrows, offset):
    # k in [0,nrows*17): k ≡ res_row (mod nrows), 2k ≡ col (mod 17)
    for k in range(nrows*17):
        if k % nrows == res_row and (2*k) % 17 == col:
            return k + offset
    return None
sections = [(0,9,0), (9,18,153), (18,19,306), (19,20,323)]   # (first row, end row, offset)
total_match = 0; total_cells = 0; mism = []
for (r0,r1,off) in sections:
    nrows = r1-r0
    if nrows == 1:
        # single-row section: value = off + k where 2k ≡ col (mod 17), k in 0..16
        for c in range(17):
            k = next(k for k in range(17) if (2*k)%17==c)
            exp = off + k; total_cells += 1
            if num[r0][c]==exp: total_match += 1
            else: mism.append((r0+1,c+1,num[r0][c],exp))
        continue
    for r in range(r0,r1):
        for c in range(17):
            exp = k_of(r-r0, c, nrows, off); total_cells += 1
            if num[r][c]==exp: total_match += 1
            else: mism.append((r+1,c+1,num[r][c],exp))
print("cells:", total_cells, " agree with the decimation formula:", total_match)
print("disagreements (row,col,figure_value,formula_value):", mism[:30])
print("count of disagreements:", len(mism))
print("row-1 figure values:", num[0])
print("row-2 figure values:", num[1])
