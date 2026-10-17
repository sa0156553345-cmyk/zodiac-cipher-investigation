#!/usr/bin/env bash
# Re-run every check of the review package from this folder.
# Requires: python3 >= 3.9, numpy, Pillow. Optional: pdfimages (poppler-utils) for step 0.
set -euo pipefail
cd "$(dirname "$0")"
echo "== environment =="
date -u +"run at (UTC): %Y-%m-%dT%H:%M:%SZ"
python3 --version
python3 -c "import numpy, PIL; print('numpy', numpy.__version__, '| Pillow', PIL.__version__)"

echo "== 0. re-extract figures from input/2023-982.pdf and compare pixels with bundled PNGs =="
if command -v pdfimages >/dev/null 2>&1; then
  TMP="$(mktemp -d)"
  pdfimages -f 8 -l 8 -png input/2023-982.pdf "$TMP/p8"
  pdfimages -f 9 -l 9 -png input/2023-982.pdf "$TMP/p9"
  python3 scripts/compare_pixels.py "$TMP/p8-000.png" images/fig1_all_panels_p8_native.png
  python3 scripts/compare_pixels.py "$TMP/p9-000.png" images/fig2_map_p9_native.png
  rm -rf "$TMP"
else
  echo "pdfimages not found: step 0 skipped (bundled PNGs used as they are)"
fi

echo "== 0b. grid overlay for reading label positions (scripts/make_grid_overlay.py) =="
python3 scripts/make_grid_overlay.py
echo "== 1. bitmap identity check (scripts/fig_glyph_check.py) =="
python3 scripts/fig_glyph_check.py
echo "== 2. transposition family, 204 configurations (scripts/transposition_family.py) =="
python3 scripts/transposition_family.py
echo "== 3. literal phrase test, no edits (scripts/literal_phrase_test.py) =="
python3 scripts/literal_phrase_test.py
echo "== 4. pre-registered alternative family + permutation null (scripts/alternatives_family.py) =="
python3 scripts/alternatives_family.py
echo "== 5. map audit with sourced landmarks (scripts/map_audit.py) =="
python3 scripts/map_audit.py
echo "== 6. SHA-256 of all bundled and generated files =="
sha256sum -c CHECKSUMS.txt
echo "== done =="
