> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 49000bc03eecb20e4b3a7844d640c5d775f11ab4a98a28dd26bc2bfce038c606.

# z32_map_calibration_audit: geographic calibration audit of the Mount Diablo map

## Purpose

To determine whether the method that converts the cipher numbers (r, θ) into a direction and a distance on the Mount Diablo map is supported by evidence. This work does not search for a solution to the cipher, and it does not confirm any earlier hypothesis.

## Verdict in brief

- The measurement inside the image is accurate: the figure's scale of 25.66 pixels per unit, with an error of about 0.5 %.
- The geographic linking is not reliable to better than a few miles. The residuals are 2 to 6 miles, and the variation of the scale between pairs is 71 %.
- The location computed from the paper is not determined to a precision of one mile: it spans 6 miles within the text-supported core, and 43 miles over the full accepted family.
- The most influential factor, the reference angle, is not settled by the paper.
- The details and the answers are in `docs/MAP_CALIBRATION_REPORT.md` (section 10).

## Contents

| Path | Content |
|---|---|
| `docs/MAP_CALIBRATION_REPORT.md` | the full report and the final answers |
| `docs/PREREGISTRATION_TRANSFORMS.md` | the pre-registered test rules, with a correction appendix |
| `docs/ASSUMPTION_REGISTER.md` | the assumptions register: what is computed, inferred and assumed, and the effect of each |
| `docs/CHANGE_LOG.md` | every change and correction, with its reason |
| `scripts/geodesy.py` | Vincenty's direct and inverse formulas on WGS84, and haversine for comparison |
| `scripts/fig_measure.py` | measures the centre of the figure, the rings, the squares, the mark, the angle labels and the scale |
| `scripts/georeg.py` | geographic linking G1 to G8 (similarity, affine, deletion of one city) |
| `scripts/transforms.py` | the registered transformation family (4800 configurations), its sensitivity, the scale curve, and the family without controls |
| `scripts/rotation_test.py` | the map-rotation test (exploratory) |
| `scripts/pairwise_scale.py` | the pre-registered criterion of scale spread between city pairs |
| `scripts/tests_geodesy.py` | 13 independent geodesy tests |
| `scripts/tests_transforms.py` | 27 independent tests of the transformation equations, directions and frame |
| `data/controls.csv` | the link cities: external coordinates, label positions (as proxies), and the source of each |
| `data/reference_points.csv` | Mount Diablo (NAD27 and USSD) and the Route 24 point (not used for selection) |
| `images/`, `input/` | the original figure image (page 9) and the PDF |
| `results/` | all computed outputs (CSV) |
| `previous_results/` | copies matching earlier results, unchanged |
| `run_all.sh` | full re-run and fingerprint check |
| `CHECKSUMS.txt` | SHA-256 for every file |
| `run_log.txt` | the actual run log |

## Requirements

Python 3.9 or later, with numpy and Pillow (see `requirements.txt`). No internet access is needed.

## Running

```bash
unzip z32_map_calibration_audit.zip
cd z32_map_calibration_audit
pip install -r requirements.txt
bash run_all.sh | tee my_run_log.txt
sha256sum -c CHECKSUMS.txt
```

The order inside `run_all.sh`:
1. `tests_geodesy.py` (the 13 tests must pass).
2. `fig_measure.py` (the figure's centre, the rings and the scale).
3. `georeg.py` (the link models G1 to G8).
4. `tests_transforms.py` (the 27 tests must pass).
5. `transforms.py` (the registered family, the sensitivity, the scale curve, and the family without controls).
6. `rotation_test.py` (exploratory).
7. `pairwise_scale.py` (the scale-spread criterion).
8. A fingerprint check of all files.

## Limits

- The geographic linking uses label positions as proxies for the positions of the cities, not the actual positions. Its residuals reach 5.8 miles.
- The external city coordinates were recorded in the previous package and were not read again in this session.
- The magnetic declination is documented in the paper, and was not computed here with an IGRF model.
- The scale of the figure is in Foxon's units. The link between these units and the original printed inch is an assumption, which cannot be verified from the image alone.
- The rounding rule, the numbers (12, 3), and the relation between the pole and the summit of Mount Diablo are all conventions that need further sources.
- The Route 24 point is a coordinate obtained by geocoding a route name, not a location. It is recorded only, and is not used in the selection.

## What this work does not establish

- It does not establish that the computed location is the location of the event.
- It does not establish or refute any meaning of the cipher.
- It does not give a probability that any location is correct.

## Data needed to resolve the open points

A high-resolution image of the original map with its scale bar; reliable positions of unambiguous features (airports, bridges, junctions, the shoreline), with independent modern coordinates; the exact wording of the instruction on the original map, with the position of the clock numbers; and confirmation that the pole is Mount Diablo.
