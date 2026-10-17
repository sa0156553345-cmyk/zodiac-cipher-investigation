> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is a3081bc38d57c24050b80dd9c143033ec50e3ba982fc66c516603108f0562088.

# z32_independent_audit: independent audit of the Z32 results

## 0. Summary

**Verdict: confirmed errors or methodological problems.** No computational error was found that changes the main numbers, but:

1. The statistical test at family level cannot support the conclusion "there is no signal". The null model destroys the positional structure of the templates, and the total is balanced only because two large deviations (k7 and k14) offset the deviations of the other orders.
2. The uncertainty of the map calibration is estimated below its real size. The printed labels do not lie on the city centres (San Leandro is about 8 miles off), and the residuals reach 133 pixels.
3. Closeness to Route 24 depends on the minute rounding rule (3 or 2), which is not justified by the text. Changing it moves the location 12–13 miles.
4. Some documentation rules are imprecise: template C is empty, models B and D were added after the fact, E2 was added after the fact, and "34 valid readings" includes 32 that do not match the figure's layout.

Details: `docs/AUDIT_REPORT.md`. Corrections: `docs/CORRECTIONS_LOG.md`.

## 1. Contents

| Path | Function |
|---|---|
| `docs/AUDIT_REPORT.md` | Audit report (review of the scripts, the statistical test, transposition rules, the map, the proposed tests, classification) |
| `docs/CORRECTIONS_LOG.md` | Corrections log, with the reason and evidence for each change |
| `scripts/` | The original processing pipeline as it is (not modified) |
| `scripts/audit/` | Independent audit scripts: `audit_01` to `audit_11` |
| `data/` | The visual transcription, and the documented landmarks with their sources |
| `images/`, `input/` | Images extracted from the PDF, and the original PDF |
| `results/` | New audit results, and the results of the original pipeline |
| `original_results/` | Byte-identical copy of the results of the previous package (for comparison; not modified) |
| `original_docs/` | Previous documents as they are (for comparison; not modified) |
| `run_all.sh` | Runs everything in order, with fingerprint verification |
| `original_run_all.sh` | The original run script of the previous package, kept for comparison only |
| `CHECKSUMS.txt` | SHA-256 fingerprints of all files (except `run_log.txt` and `CHECKSUMS.txt`) |
| `run_log.txt` | The actual run log |

## 2. Requirements

- Python 3.9 or later, with `numpy` and `Pillow` (`pip install -r requirements.txt`).
- Optional: `pdfimages` (poppler-utils) for the re-extraction step from the PDF.
- No internet access is needed.

## 3. How to run

```bash
unzip z32_independent_audit.zip
cd z32_independent_audit
pip install -r requirements.txt
bash run_all.sh | tee my_run_log.txt
sha256sum -c CHECKSUMS.txt
```

`run_all.sh` runs, in order:
1. Verification of the image extraction from the PDF, pixel by pixel (if `pdfimages` is available).
2. The original pipeline: `make_grid_overlay`, then `fig_glyph_check`, then `transposition_family`, then `literal_phrase_test`, then `alternatives_family`, then `map_audit`.
3. The audit scripts in order: `audit_01` to `audit_11`.
4. A byte-by-byte comparison of the results with `original_results/`.
5. Verification of the fingerprints.

**Important order:** `audit_04` and `audit_10` depend on `audit_03`. `audit_06`, `audit_07` and `audit_11` depend on `map_audit`.

## 4. Main results (numbers from the files in `results/`)

| Check | File | Result |
|---|---|---|
| Independent check of the constraints | `audit_01_repeat_recheck.csv` | 34 orders, 0 contradictions |
| Second implementation of the transposition family | `audit_02_second_implementation.csv` | 204/204 agree |
| Primary path of the order | `audit_02_primary_path.csv` | 33 moves, two skips (steps 9 and 17) |
| Structure of the skipping | `audit_02_forced_structure.csv` | All orders: 17 visits in the first row and 15 in the second, and at least one skip |
| Exact null probability | `audit_03_exact_null_summary.csv` | N = 3544 (template C = 0); exact expectation 45.296 versus simulation 45.266 |
| Sensitivity to the choice of orders | `audit_04_alternatives_sensitivity.csv` | All: O = 47, p = 0.417. The two orders matching the figure: O = 1, p = 0.94. The other 32: O = 46, p = 0.33 |
| Power of the statistic | `audit_05_statistic_power.csv` | The statistic does not change when symbols are relabelled. The threshold p < 0.05 requires O ≥ 58 |
| Geographic pairs | `audit_06_pairwise.csv`, `audit_06_summary.csv` | Scale of the pairs from 15.6 to 29.7 pixels per mile; median 1.09 miles per unit; directions from −11° to +72° |
| Sensitivity of the map | `audit_07_leave_one_out.csv`, `audit_07_noise_sweep.csv` | 95% radius from 1.4 to 4.4 miles depending on the noise |
| Identity margin | `audit_08_identity_margin.csv` | 29 categories; gap 0.1316 |
| Family structure | `audit_09_family_construction.csv` | No phrase shared between the two templates; T1 and T2 inside the family; T3 outside it |
| Diagnosis of the null model | `audit_10_pair_match_rates.csv`, `audit_10_summary.csv` | 47 pairs out of 496 with rates above 2, and 125 below 0.5. The excess (+31.3) is cancelled by the deficit (−29.6) |
| Sensitivity to rounding | `audit_11_rounding_sensitivity.csv` | The location moves 11.7–13.4 miles when changing 3 to 2 |

## 5. Limitations

- The test checks only the three constraints. It does not measure meaning or language.
- The symbols are ASCII characters printed in the paper, not the original Zodiac symbols. The pixel categories are determined by pixels, but their names come from visual reading.
- All the positions of the labels on the map were read by eye, not measured automatically.
- The coordinates come from Wikipedia (city centres) and from Foxon's table. The Route 24 point is not a location.
- The null model used does not suit this family (section 3 of the report), and it is advised not to use it to conclude that there is no signal.
- The audit is not blind: the family and the tests were designed after seeing (C) and after earlier results.

## 6. What this audit does not establish

- It does not establish that the solution exists, nor that it is impossible.
- It does not give a probability that any statement is correct.
- It does not establish any geographic location.

## 7. Next step

Fix the scale of the original map (T1 in the report), then obtain an original transcription of the symbols (T7). Then run a test with a null model that preserves the templates (T4), and a power estimate (T5), before any new statistical conclusion.
