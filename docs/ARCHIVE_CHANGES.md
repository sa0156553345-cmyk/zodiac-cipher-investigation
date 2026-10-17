# Archive changes

This file lists everything that differs between the workspace and this archive: exclusions, additions from the working folder, path changes, wording changes, and new packaging files. Every change is recorded here, and no research result was changed.

## 1. Exclusions

- 33 item(s): image
- 5 item(s): publication-derived or image
- 4 item(s): archive duplicate
- 4 item(s): publication copy (PDF)
- 2 item(s): text extracted from a publication

Full list with reasons: `manifests/EXCLUSIONS.csv`.

Duplicate copies of publications: the four workspace copies of `2023-982.pdf` (in `z32_*/input/`) and the uploaded `z32_independent_audit.zip` are excluded. Four archives (`z32_*.zip`) that duplicate folders are excluded. Images are excluded in all folders (see the dossier, section 15).

## 2. Additions from the working folder (no identical copy in the workspace outputs)

- `logs/rerun_log.txt`
- `logs/run_all_repro.log`
- `z32_phase5_audit/analysis/reproduce_models.py`
- `z32_phase5_audit/analysis/sensitivity.py`
- `z32_phase5_audit/candidate_sensitivity/docs/PREREG_CANDIDATE_SENSITIVITY.md`
- `z32_phase5_audit/candidate_sensitivity/scripts/candidate_sensitivity.py`
- `z32_phase5_audit/candidate_sensitivity/results/candidate_sensitivity_grid.csv`
- `z32_structure/audit/audit_structure_stat.py`
- `z32_structure/audit/audit_structure_stat.log`
- `z32_structure/audit/results_structure_audit.json`
- `z32_checkpoint/phase1_working/blind_hidden_map.json`
- `z32_checkpoint/phase1_working/blind_review.py`
- `z32_checkpoint/phase1_working/blind_review2.py`
- `z32_checkpoint/phase1_working/decrypt_check.py`
- `z32_checkpoint/phase1_working/key_glyph_boxes.json`
- `z32_checkpoint/phase1_working/key_glyph_boxes2.json`
- `z32_checkpoint/phase1_working/key_templates48.npy`
- `z32_checkpoint/phase1_working/match_v2.py`
- `z32_checkpoint/phase1_working/match_v3.py`
- `z32_checkpoint/phase1_working/seg_key.py`
- `z32_checkpoint/phase1_working/seg_key2.py`
- `z32_checkpoint/phase1_working/seg_z340.py`
- `z32_checkpoint/phase1_working/trans_numbers.json`
- `z32_checkpoint/phase1_working/trans_ocr.txt`
- `z32_checkpoint/phase1_working/trans_ocr_cells.py`
- `z32_checkpoint/phase1_working/trans_order.json`
- `z32_checkpoint/phase1_working/trans_suspect.json`
- `z32_checkpoint/phase1_working/tune_z340.py`
- `z32_checkpoint/phase1_working/z340_best.json`
- `z32_checkpoint/phase1_working/z340_cipher_grid.csv`
- `z32_checkpoint/phase1_working/z340_components.json`
- `z32_checkpoint/phase1_working/z340_comps_final.json`
- `z32_checkpoint/phase1_working/z340_grid.py`
- `z32_checkpoint/phase1_working/z340_grid_ids.npy`
- `z32_checkpoint/phase1_working/z340_grid_margin.npy`
- `z32_checkpoint/phase1_working/z340_inkcell.npy`
- `z32_checkpoint/phase1_working/z340_v2_ids.npy`
- `z32_checkpoint/phase1_working/z340_v2_margin.npy`
- `z32_checkpoint/phase1_working/z340_v3_ids.npy`
- `z32_checkpoint/phase1_working/z340_v3_margin.npy`
- `z32_checkpoint/phase1_working/z340_xc.npy`
- `z32_checkpoint/phase1_working/z340_yr.npy`

## 3. New packaging files

- `README.md`, `docs/REPRODUCTION_GUIDE.md`, `docs/SOURCES.md`, `docs/ARCHIVE_CHANGES.md`, `docs/RECORDS_INDEX.md`
- `manifests/FILE_INVENTORY.csv`, `manifests/SHA256SUMS.txt`, `manifests/EXCLUSIONS.csv`, `manifests/DUPLICATES_WITHIN_ARCHIVE.csv`
- `z32_checkpoint/reproduce_z340_from_pdf.sh` (new script: regenerates the Z340 pipeline from the user's PDF; it was tested, see the reproduction guide)
- Four placeholder files named `PLACE_2023-982.pdf_HERE.md` in the input folders, where the publication copy was removed

## 4. Path changes in archived code (only the absolute workspace paths were replaced; computation unchanged)

### 4.1 `z32_phase5_audit/audit_phase5_independent.py`

Before:
```
PKG = '/home/claude/work/z32_independent_audit'
P5 = '/home/claude/work/phase5'
OUT = '/home/claude/work/phase5_audit'
```
After:
```
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
PKG = _os.path.join(_HERE, '..', 'z32_independent_audit')
P5 = _os.path.join(_HERE, '..', 'z32_phase5')
OUT = _HERE
```

### 4.2 `z32_structure/run_structure.py`

Before:
```
PKG = '/home/claude/work/z32_independent_audit'
```
After:
```
import os as _os
PKG = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'z32_independent_audit')
```

### 4.3 `z32_structure/run_structure.py`

Before:
```
f'{"/home/claude/work/z32_structure"}/results_structure.json'
```
After:
```
_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'results_structure.json')
```

### 4.4 `z32_phase5_audit/analysis/reproduce_models.py`

Before:
```
sys.path.insert(0, '/home/claude/work/z32_independent_audit/scripts')
PKG = '/home/claude/work/z32_independent_audit'
```
After:
```
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
sys.path.insert(0, _os.path.join(_HERE, '..', '..', 'z32_independent_audit', 'scripts'))
PKG = _os.path.join(_HERE, '..', '..', 'z32_independent_audit')
```

### 4.5 `z32_phase5_audit/candidate_sensitivity/scripts/candidate_sensitivity.py`

Before:
```
ARCH = Path('/home/claude/work/z32_independent_audit')
OUT = Path('/home/claude/work/review/results')
```
After:
```
ARCH = Path(__file__).resolve().parents[3] / 'z32_independent_audit'
OUT = Path(__file__).resolve().parents[1] / 'results'
```

### 4.6 `z32_structure/audit/audit_structure_stat.py`

Before:
```
PKG = '/home/claude/work/z32_independent_audit'
```
After:
```
import os as _os
PKG = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', 'z32_independent_audit')
```

### 4.7 `z32_repro/superseded/z32_map_scale_check.py`

Before:
```
'/mnt/user-data/outputs/z32_map_scale_check.csv'
```
After:
```
'z32_map_scale_check.csv'
```

### 4.8 `z32_repro/superseded/z32_transposition_test.py`

Before:
```
'/mnt/user-data/outputs/z32_all_configs.csv'
```
After:
```
'z32_all_configs.csv'
```

### 4.9 `z32_repro/superseded/z32_transposition_test.py`

Before:
```
'/mnt/user-data/outputs/z32_phrase_tests.csv'
```
After:
```
'z32_phrase_tests.csv'
```

## 5. Wording changes in the archived dossier (`ZODIAC_CIPHER_RESEARCH_DOSSIER.md`)

- Section 9.2: the clause that described `reproduce_models.py` as being in the working folder now points to its archive location, `z32_phase5_audit/analysis/reproduce_models.py`.
- Section 11: descriptions of absolute paths were replaced with a note on archive-relative paths.
- A one-paragraph archive note was added below the status line.
- No numbers, findings, or evidence classes were changed.

## 6. Duplicates

Round folders (`z32_repro/`, `z32_next_review/`, `z32_map_calibration_audit/`) and the package folder `z32_independent_audit/` share some identical files. They are all kept, because each round is a self-contained run with its own `run_all.sh` and `CHECKSUMS.txt`. Identical files across folders are listed in `manifests/DUPLICATES_WITHIN_ARCHIVE.csv`. This is a judgement call: if you prefer a single copy of each file, it can be done, but the round folders would then no longer run on their own.


## 7. Remaining historical wording

Section 2 and other statements in the dossier that mention `/home/claude/work/` describe the original workspace. They were left unchanged on purpose, so that the record of where things were is preserved.

## 8. Image-only folders absent from the archive

These folders held only images and are therefore not in the archive: `z32_checkpoint/figures/`, `z32_independent_audit/images/`, `z32_map_calibration_audit/images/`, `z32_next_review/images/`, `z32_repro/images/`. Where the dossier mentions them, it refers to the workspace layout.

## 9. Release preparation: charts and README

- Added: `assets/make_charts.py`, `assets/m0_m5_letter_agreement.png`, `assets/error_rank_distribution.png`, `assets/wilson_confidence_intervals.png`, `assets/chart_data.json`. These are original visualisations generated from the archived result files (see `docs/IMAGE_PROVENANCE.md`, section 5).
- Rewritten: `README.md` (plain-language version with the charts embedded).
- Changed: `.gitignore` (adds `!assets/*.png` so the charts are not ignored); `requirements.txt` (adds matplotlib, seaborn, pandas with observed versions); `docs/IMAGE_PROVENANCE.md`, `docs/PROJECT_MAP.md`, `docs/REPRODUCTION_GUIDE.md` (sections updated to match the new `assets/`).
- Test rule change, recorded here: the earlier rule 2 forbade all PNG images. It now permits PNG files only under `assets/`, and only when each is listed with its SHA-256 in `assets/chart_data.json` (new check I3b). The other rules are unchanged.
- Manifests (`manifests/SHA256SUMS.txt`, `manifests/FILE_INVENTORY.csv`, `manifests/DUPLICATES_WITHIN_ARCHIVE.csv`) were regenerated after these changes.

## 10. Translation of the Arabic working records into English

The repository was prepared for English-only publication. Every Arabic text file in the repository was translated into English. The original Arabic files are kept unchanged in the research workspace (the `z32_*` folders outside this repository); none was deleted. Each translated file starts with a note giving the SHA-256 of its Arabic original, so the original can be checked against it.

- Unique Arabic-language contents translated: 33. One further file, `z32_structure/audit/audit_structure_stat.py`, contained a single Arabic phrase in its docstring, which was translated in place.
- Installed copies: 41. Identical duplicates were translated identically.
- Numbers and identifiers: each translation was checked automatically against its original. Every number token in each original appears in its translation, except the one noted below.
- Code: the only change to code is one docstring phrase (an Arabic phrase meaning "appears twice") replaced by the English phrase "appears twice". No computation was changed.
- The original files were checked to be identical to their recorded hashes before they were overwritten.

Observations found during translation (recorded, not corrected):
- `z32_h4/PREREG_H4.md` cites the solution paper as "Blake, Oranchak and Van Eycke, 2021". The arXiv version (arXiv:2403.17350) is dated 26 March 2024. `z32_checkpoint/REPORT_H4_readiness.md` refers to the announced solution as December 2020. Both dates are kept as written.
- `z32_structure/PREREG_structure.md` gives the simulation count as 100000 (the source wording). The test C25 relies on this wording. The text was briefly rendered as "100,000" and restored to the literal form.

Translated files (path, SHA-256 prefix of the Arabic original):

| File | Original SHA-256 (first 12) |
|---|---|
| `z32_checkpoint/FIRST10_MISMATCH_AUDIT.md` | `277946740840` |
| `z32_checkpoint/FULL63_REPORT.md` | `5fca0ab5acd3` |
| `z32_checkpoint/METHODS_REPORT.md` | `13b75fc9a7b7` |
| `z32_checkpoint/PHASE1_SOURCES_STATUS.md` | `e7d0401dcdcc` |
| `z32_checkpoint/PREREG_H4.md` | `ccc94448d5bd` |
| `z32_checkpoint/README.md` | `5456dc619470` |
| `z32_checkpoint/REPORT_H4_readiness.md` | `045378ccb65d` |
| `z32_checkpoint/STATE.md` | `6c60794b56e5` |
| `z32_checkpoint/full63/FULL63_REPORT.md` | `5fca0ab5acd3` |
| `z32_checkpoint/methods/METHODS_REPORT.md` | `13b75fc9a7b7` |
| `z32_checkpoint/methods/PREREG_METHODS.md` | `77e2c34aa596` |
| `z32_checkpoint/methods/VALIDATION_LOG.md` | `ea8113e2b453` |
| `z32_h4/PREREG_H4.md` | `ccc94448d5bd` |
| `z32_h4/REPORT_H4_readiness.md` | `045378ccb65d` |
| `z32_independent_audit/README.md` | `a3081bc38d57` |
| `z32_independent_audit/docs/AUDIT_REPORT.md` | `ee7902afcdfa` |
| `z32_independent_audit/docs/CORRECTIONS_LOG.md` | `42966cb7cf42` |
| `z32_independent_audit/original_docs/README_previous_package.md` | `9256865e453a` |
| `z32_independent_audit_review/REVIEW_SUMMARY.md` | `576344695857` |
| `z32_map_calibration_audit/README.md` | `49000bc03eec` |
| `z32_map_calibration_audit/docs/ASSUMPTION_REGISTER.md` | `6e3aa970cbdf` |
| `z32_map_calibration_audit/docs/CHANGE_LOG.md` | `8e711332b2e1` |
| `z32_map_calibration_audit/docs/MAP_CALIBRATION_REPORT.md` | `4894cedf258b` |
| `z32_map_calibration_audit/docs/PREREGISTRATION_TRANSFORMS.md` | `3ddde4b6f509` |
| `z32_map_calibration_audit/previous_results/README_PREVIOUS.md` | `b94cd2f497cd` |
| `z32_map_calibration_audit/previous_results/docs_previous_audit/AUDIT_REPORT.md` | `ee7902afcdfa` |
| `z32_map_calibration_audit/previous_results/docs_previous_audit/CORRECTIONS_LOG.md` | `42966cb7cf42` |
| `z32_next_review/README.md` | `9256865e453a` |
| `z32_phase1/PHASE1_SOURCES_STATUS.md` | `e7d0401dcdcc` |
| `z32_phase5/PREREGISTRATION_phase5.md` | `1348330b5ded` |
| `z32_phase5/REPORT_phase5.md` | `3979ee207397` |
| `z32_phase5_audit/AUDIT_PHASE5_REPORT.md` | `0df7153e7068` |
| `z32_phase5_audit/candidate_sensitivity/docs/PREREG_CANDIDATE_SENSITIVITY.md` | `4bd222a13b0d` |
| `z32_repro/README.md` | `923150ceddec` |
| `z32_repro/superseded/README_SUPERSEDED.md` | `700c1c24b9df` |
| `z32_source_search/PHASE2_SOURCE_REPORT.md` | `2a061ae11ffa` |
| `z32_source_search/PHASE3_FBI_PARTS_2_TO_7.md` | `4436678aa1e2` |
| `z32_source_search/PHASE4_STATUS.md` | `9c26bb7631ec` |
| `z32_source_search/SOURCE_SEARCH_REPORT.md` | `16400cdaf5e0` |
| `z32_structure/PREREG_structure.md` | `5dcae9a8ab61` |
| `z32_structure/REPORT_structure_short.md` | `4e6fb08c8fed` |
| `z32_structure/audit/audit_structure_stat.py` | `e19c77079955` |
