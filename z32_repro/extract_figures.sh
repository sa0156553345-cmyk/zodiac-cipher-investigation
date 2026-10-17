#!/usr/bin/env bash
# Extract the two raster figures from the paper, unmodified.
# usage: bash extract_figures.sh <path-to-pdf> [output-dir]      (output-dir defaults to .)
# needs: poppler-utils (pdfimages)
set -euo pipefail
PDF="$1"
OUT="${2:-.}"
TMP="$(mktemp -d)"
pdfimages -f 8 -l 8 -png "$PDF" "$TMP/p8"   # page 8: Fig.1 panels A-D (one raster, 987x498)
pdfimages -f 9 -l 9 -png "$PDF" "$TMP/p9"   # page 9: Fig.2 map (one raster, 916x894)
cp "$TMP/p8-000.png" "$OUT/fig1_all_panels_p8_native.png"
cp "$TMP/p9-000.png" "$OUT/fig2_map_p9_native.png"
rm -rf "$TMP"
echo "extracted into $OUT"
