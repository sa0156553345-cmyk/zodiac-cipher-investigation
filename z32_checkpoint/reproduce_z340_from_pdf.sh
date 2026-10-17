#!/usr/bin/env bash
# Reproduce the Z340 reconstruction pipeline from the arXiv PDF (arXiv:2403.17350v1).
# Usage:  bash reproduce_z340_from_pdf.sh <archive_root> <path/to/2403_17350v1.pdf> <new_run_dir>
# The run directory must not exist. Requires: poppler-utils (pdfimages, pdftotext), tesseract, python3 with
# numpy, scipy, scikit-learn, scikit-image, Pillow.  Runtime: several minutes (methods_experiment.py is the longest step).
set -euo pipefail
ARCH="$(cd "$1" && pwd)"
PDF="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"
RUN="$3"
if [ -e "$RUN" ]; then echo "ERROR: run directory already exists: $RUN"; exit 1; fi
S="$ARCH/z32_checkpoint"
mkdir -p "$RUN/img"
cp "$S"/scripts/*.py "$RUN"/
cp "$S"/methods/methods_experiment.py "$RUN"/
cp "$S"/phase1_working/*.py "$RUN"/
cp "$S"/phase1_working/*.npy "$S"/phase1_working/*.json "$S"/phase1_working/*.csv "$RUN"/
cp "$S"/artifacts/* "$RUN"/
cd "$RUN"
# Figures and text are regenerated from the user's own copy of the PDF (not redistributed in the archive).
pdfimages -png -f 1 -l 1 "$PDF" img/p01
pdfimages -png -f 31 -l 31 "$PDF" img/p31
pdftotext -enc UTF-8 "$PDF" paper.txt
awk 'BEGIN{page=1} { if (index($0,"\f")>0) { c=gsub(/\f/,"&"); } print page ": " $0; page+=gsub(/\f/,"&") }' paper.txt > paged.txt
# Pipeline (order matters)
python3 seg_key3.py
python3 build_key.py
python3 z340_cells.py
python3 match_v4.py
python3 trans_ocr_cells2.py
python3 trans_fix.py
python3 fix_order.py
python3 verify_transposition.py
python3 decrypt_check.py
python3 compare_z340.py
python3 methods_experiment.py
# Compare regenerated outputs with the archived ones
python3 - "$RUN" "$S" << 'PYCMP'
import sys, json, os, numpy as np
run, s = sys.argv[1], sys.argv[2]
def same_json(a,b):
    return json.load(open(a)) == json.load(open(b))
def same_csv(a,b):
    return open(a,'rb').read() == open(b,'rb').read()
def same_npy(a,b):
    x=np.load(a,allow_pickle=True); y=np.load(b,allow_pickle=True)
    return x.shape==y.shape and bool(np.all(x==y))
checks=[('artifacts/key_table_glyphs.csv', same_csv), ('artifacts/trans_values_fixed.json', same_json),
        ('artifacts/trans_values_rowmajor.json', same_json), ('artifacts/compare_z340_v4.json', same_json),
        ('artifacts/z340_v4_ids.npy', same_npy), ('artifacts/z340_v4_margin.npy', same_npy),
        ('methods/methods_results.json', same_json), ('methods/methods_top1_ids.json', same_json)]
ok=0
for rel,fn in checks:
    src=os.path.join(s,rel); gen=os.path.join(run, os.path.basename(rel))
    try:
        r=fn(gen,src)
    except Exception as e:
        r=False; print("  error:", rel, e)
    ok+=bool(r); print(("MATCH " if r else "DIFF  ")+rel)
print(f"{ok}/{len(checks)} archived outputs reproduced exactly")
PYCMP
