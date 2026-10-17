#!/usr/bin/env bash
# Re-run the whole audit package from this folder.
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

echo "== 1. original pipeline (unchanged scripts) =="
python3 scripts/make_grid_overlay.py
python3 scripts/fig_glyph_check.py
python3 scripts/transposition_family.py
python3 scripts/literal_phrase_test.py
python3 scripts/alternatives_family.py
python3 scripts/map_audit.py > /tmp/_map_audit_stdout.txt
echo "-- byte comparison of pipeline outputs with original_results/ --"
for f in fig_glyph_check.csv literal_phrase_test.csv transposition_all_configs.csv transposition_assumption_effects.csv valid_orders.json alternatives_summary.csv alternatives_candidates.csv map_audit_models.csv map_audit_landmarks.csv map_crosshair_and_rings.csv; do
  if cmp -s "results/$f" "original_results/$f"; then echo "identical: $f"; else echo "DIFFERENT: $f"; exit 1; fi
done

echo "== 2. independent audit scripts =="
for s in audit_01_repeat_recheck audit_02_transposition_forced_structure audit_03_exact_null audit_04_alternatives_sensitivity audit_05_statistic_power audit_06_map_pairwise_scale audit_07_map_leave_one_out_and_noise audit_08_identity_margin audit_09_family_construction audit_10_null_diagnostic audit_11_rounding_sensitivity; do
  echo "-- $s --"
  python3 "scripts/audit/$s.py"
done
rm -rf scripts/__pycache__ scripts/audit/__pycache__

echo "== 3. SHA-256 of all bundled and generated files =="
sha256sum -c CHECKSUMS.txt
echo "== done =="
