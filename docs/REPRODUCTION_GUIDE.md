# Reproduction guide

This guide lists what was run, with what inputs, and what was checked. Commands are run from the archive root unless stated otherwise.

## 1. Environment used for the packaging tests

- Linux container, no network access during the tests.
- Python 3.12.3; numpy 2.4.4; Pillow 12.1.1; scipy 1.17.1; scikit-image 0.26.0; scikit-learn 1.8.0.
- Tesseract OCR 5.3.4 (command-line tool).
- Poppler utilities (pdfimages 24.02.0, pdftotext).
- awk, sha256sum, and the GPL license files at `/usr/share/common-licenses/GPL-2` and `GPL-3` (needed by two calibration and structure scripts).

Other systems may differ. Re-running with other versions is not guaranteed to give identical numbers, and this has not been tested.

## 2. Inputs that are not in the archive

| Input | Needed by | How to obtain and place it |
|---|---|---|
| `2403_17350v1.pdf` (arXiv:2403.17350v1) | Z340 pipeline: figures and text | Download it yourself. Pass its path to the reproduction script. |
| `2023-982.pdf` (Foxon 2023) | Foxon audit package, `run_all.sh` | Download it yourself. Place it at `z32_independent_audit/input/2023-982.pdf`. |
| Figures written by `run_all.sh` into `images/` | `audit_phase5_independent.py` | Not produced by `run_all.sh`. No script creates the folder `images/`; the figures must be supplied (see experiment 9 in section 3). |

## 3. Experiments

| # | Experiment | Command | Status in the packaging tests |
|---|---|---|---|
| 1 | Z340 pipeline from the arXiv PDF | `bash z32_checkpoint/reproduce_z340_from_pdf.sh . /path/to/2403_17350v1.pdf ./run_z340` | Ran all steps up to `methods_experiment.py`; see section 6. |
| 2 | Methods comparison M0 to M5 | `python3 methods_experiment.py` inside a run directory made by experiment 1 | Completed (209 s). All 8 archived outputs matched exactly. |
| 3 | Transposition check | `cd z32_checkpoint/artifacts && python3 ../scripts/verify_transposition.py` | Ran in the pipeline; reports 93 disagreements with the decimation formula, as recorded. |
| 4 | H4a calibration (synthetic data) | `cd z32_h4 && python3 calibrate_h4.py` | Re-run in a copy: output identical to `calibration_h4.json`. |
| 5 | Z32 structure analysis | `cd z32_structure && python3 run_structure.py` | Re-run in a copy: identical except the elapsed-time field. |
| 6 | Structure audit | `cd z32_structure/audit && python3 audit_structure_stat.py` | Re-run in a copy: identical except the elapsed-time field. |
| 7 | Map models | `cd z32_phase5_audit/analysis && python3 reproduce_models.py` | Re-run: model A gives 37.92961, -122.15045; model C gives 37.90253, -122.15078; distance from the candidate to model C 1.88 miles; model A pole offset 2.67 miles. |
| 8 | Candidate sensitivity grid | `cd z32_phase5_audit/candidate_sensitivity/scripts && python3 candidate_sensitivity.py` | Re-run in a copy: grid CSV byte-identical. |
| 9 | Foxon audit package | `cd z32_independent_audit && bash run_all.sh` | Not runnable from the archive as delivered. Its comparison step needs the bundled figure images (`images/fig1_all_panels_p8_native.png`, `images/fig2_map_p9_native.png`), which are third-party and excluded, and no script creates `images/`. Twelve identity checks were run earlier, in the working folder before exclusion (see `logs/rerun_log.txt`). |
| 10 | Independent geometric audit | `cd z32_phase5_audit && python3 audit_phase5_independent.py` | Not run. It needs the figure images from experiment 9. It writes into its own folder, so run it in a copy. |
| 11 | Robustness, full 63-glyph scoring, blinded review of the first ten mismatches | scripts in `z32_checkpoint/full63/` and `z32_checkpoint/scripts/` | Not run in the packaging tests. They need the images, which are not in the archive. |
| 12 | H4a test itself | not run | Pre-registered and blocked. It must not be run until the Z340 reconstruction is validated. |

Several scripts write their outputs into the folder they are in. Running them there overwrites the archived copies. Run them in a copy.

## 4. What the Z340 pipeline does

`z32_checkpoint/reproduce_z340_from_pdf.sh` does the following:

1. Creates a new run directory and copies in the scripts, artifacts, and intermediate files.
2. Extracts the page-1 and page-31 images with `pdfimages`, and the text with `pdftotext`. It builds `paged.txt` with awk.
3. Runs, in order: `seg_key3.py`, `build_key.py`, `z340_cells.py`, `match_v4.py`, `trans_ocr_cells2.py`, `trans_fix.py`, `fix_order.py`, `verify_transposition.py`, `decrypt_check.py`, `compare_z340.py`, `methods_experiment.py`.
4. Compares eight regenerated outputs with the archived ones and prints MATCH or DIFF.

Run it with `bash` in the foreground, or start it with `setsid` so it is not tied to a shell session. In the packaging tests, two background runs stopped without an error message (see section 5).

## 5. Known limitations

- Background runs. Two background runs were stopped without an error message: one after the OCR step, and one during `methods_experiment.py`. The steps were re-run individually and completed. The full run stopped during the methods step, so that step was re-run manually in the same run directory, with the same comparison code. Run the script in the foreground or with `setsid` when you reproduce it.
- `fix_order.py` prints `row-major y monotone across rows: False`. That check is wrong. The permutation check and the row values are correct, and the output of the transposition check matches the record.
- `decrypt_check.py` uses the earlier v1 matcher. Its printed similarity of 0.02 is a legacy diagnostic and should be ignored. The meaningful agreement is the position-wise value printed by `compare_z340.py` (0.609).
- `methods_diagnostics.json` was never written, because a diagnostic script stopped on an error. The confidence intervals in `METHODS_REPORT.md` were typed from printed output. They were recomputed in packaging with the Wilson formula (n = 170), giving 0.609 to 0.748 for M5 and 0.615 to 0.753 for M3.
- The six visual corrections (Z340 glyphs) are not part of the algorithmic result. The 213 of 340 figure includes them.
- Several scripts write into their own folder, as noted in section 3.
- Some round folders contain duplicate files. They are kept so that each round runs on its own (see `docs/ARCHIVE_CHANGES.md`, section 6).
- The withdrawn scripts in `z32_repro/superseded/` are kept for the record. Their results must not be used.

## 6. Test results (packaging session)

| Test | Result | Log (under `logs/packaging_tests/`) |
|---|---|---|
| Z340 pipeline from the arXiv PDF, steps up to `compare_z340.py` | Completed. Position-wise agreement 0.609; 340 symbols; first mismatch at index 0 (as recorded). | `full_pipeline_run.log` |
| `methods_experiment.py` (M0 to M5), run manually | Completed in 209 s. Sanity check: 0 top-1 differences from v4. Selected by tuning rule: M5. | `methods_manual_rerun.log` |
| Eight archived Z340 outputs regenerated from the PDF | 8 of 8 identical (key table CSV; transposition values, fixed and row-major; reference comparison; v4 identities and margins; M0 to M5 results and top-1 identities). | comparison printed in `methods_manual_rerun.log` and the pipeline log |
| H4a calibration | Identical to `calibration_h4.json`. | `calibrate_h4_test.log` |
| Z32 structure analysis | Identical except `elapsed_s`. | `run_structure_test.log` |
| Structure audit | Identical except `elapsed_s`. | `audit_structure_stat_test.log` |
| Candidate sensitivity grid | Byte-identical. | `candidate_sensitivity_test.log` |
| Map models | Values as recorded (see experiment 7). | `reproduce_models_test.log` |
| Interrupted runs | Recorded for transparency. The first background pipeline run stopped after OCR; the OCR step was re-run alone and completed. | `z340_pipeline_background_first_attempt_interrupted.log`, `z340_trans_ocr_standalone.log`, `methods_run_interrupted.log` |

Not tested in the packaging session: experiments 9, 10, 11, and the FBI Vault and web-source searches. Experiment 12 was not run, by design.

## 7. Archive integrity

See `docs/ARCHIVE_CHANGES.md` and `manifests/`. The integrity test on the final ZIP is reported in the final message accompanying this archive.

## 8. Final checks added in the audit

Run from the repository root:

    python3 -m pip install -r requirements.txt
    python3 tests/check_archive.py

The second command prints one line per check (PASS, FAIL, DOCUMENTED-DISCREPANCY or UNCHECKED) and a summary. It exits with status 1 if any check fails. Its results and the corrections made to it are recorded in `docs/DISCREPANCY_AUDIT.md`.

## 9. Regenerate the charts

From the repository root:

    python3 -m pip install -r requirements.txt
    python3 assets/make_charts.py

The script reads only the archived result files, recomputes every plotted number, and stops with an error if any number differs from the stored results. It writes three PNG files and `assets/chart_data.json` into `assets/`. The checks it prints confirm the stored accuracies, the M5 validation count (116 of 170), and the M5 validation error bins (29, 11, 14).

