#!/usr/bin/env bash
# Re-run every check from this folder.
# Requires: python3 >= 3.9, numpy, Pillow. Optional: pdfimages (poppler-utils) for step 0.
set -euo pipefail
cd "$(dirname "$0")"

echo "== environment =="
date -u +"run at (UTC): %Y-%m-%dT%H:%M:%SZ"
python3 --version
python3 -c "import numpy, PIL; print('numpy', numpy.__version__, '| Pillow', PIL.__version__)"

echo "== 0. re-extract figures from input/2023-982.pdf and compare with bundled PNGs =="
if command -v pdfimages >/dev/null 2>&1; then
  TMP="$(mktemp -d)"
  bash extract_figures.sh input/2023-982.pdf "$TMP"
  for f in fig1_all_panels_p8_native.png fig2_map_p9_native.png; do
    python3 compare_pixels.py "$TMP/$f" "$f" || { echo "DIFFERENT pixels: $f"; exit 1; }
    echo "bytes sha256 fresh extraction: $(sha256sum "$TMP/$f" | cut -d' ' -f1)"
  done
  rm -rf "$TMP"
else
  echo "pdfimages not found: step 0 skipped (bundled PNGs are used as they are)"
fi

echo "== 1. bitmap identity check (fig_glyph_check.py) =="
python3 fig_glyph_check.py

echo "== 2. transposition family and phrase tests (transposition_family.py) =="
python3 transposition_family.py

echo "== 3. map check (map_check.py) =="
python3 map_check.py

echo "== 4. SHA-256 of all bundled and generated files =="
sha256sum -c CHECKSUMS.txt
echo "== done =="
