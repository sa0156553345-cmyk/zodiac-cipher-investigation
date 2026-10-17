#!/usr/bin/env bash
# Re-runs the whole map-calibration audit from this folder and verifies all checksums.
# Requires python3 >= 3.9, numpy, Pillow (see requirements.txt). No network access is used.
set -euo pipefail
cd "$(dirname "$0")"
echo "run at (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
python3 --version
python3 -c "import numpy, PIL; print('numpy', numpy.__version__, '| Pillow', PIL.__version__)"
cd scripts
echo "== 1. geodesy tests =="; python3 tests_geodesy.py
echo "== 2. figure measurements =="; python3 fig_measure.py
echo "== 3. georeferencing G1..G8 =="; python3 georeg.py
echo "== 4. transform tests =="; python3 tests_transforms.py
echo "== 5. pre-registered transform family =="; python3 transforms.py
echo "== 6. rotation test (exploratory) =="; python3 rotation_test.py
echo "== 7. pre-registered pairwise scale criterion =="; python3 pairwise_scale.py
cd ..
find . -name "__pycache__" -prune -exec rm -rf {} \; 2>/dev/null || true
echo "== 8. checksums =="
sha256sum -c CHECKSUMS.txt
echo "== done =="
