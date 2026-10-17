# Zodiac Ciphers Z340 and Z32: Research Dossier

**Status:** Working record compiled from the project files in this workspace. It does not report a solved Z340 or Z32 cipher, and it does not present any candidate location as confirmed. Items are labelled by evidence class (see Section 1).

**Archive note:** This copy is part of `ZODIAC_CIPHER_INVESTIGATION.zip`. Folder names match the workspace layout. Wording changes made only in this archive copy are listed in `docs/ARCHIVE_CHANGES.md`; no findings were changed.

---

## 1. Status at a glance

| Question | Status | Evidence class |
|---|---|---|
| Is the published Z340 decryption reproduced? | **No.** Algorithmic letter agreement on the held-out half is 68.2% (116 of 170). | C |
| Did the 70% exploratory target succeed? | **No**, on the held-out sample. The Wilson 95% interval is 60.9%–74.8%. | C |
| Full 340-position agreement | 207 of 340 (60.9%) with the algorithm alone; 213 of 340 (62.6%) after six documented visual corrections. | C, VJ |
| Is Z32 decrypted or solved? | **No.** No decryption or location has been reproduced. | — |
| H4a (Z340 key applied to Z32) | Pre-registered and calibrated on synthetic data. **Not run.** | — |
| Candidate coordinates 37.929792, −122.150318 | **Not confirmed.** Not supported under the pre-registered conventions. The source of these coordinates is not recorded in the project files. | C (conditional) |

**Evidence classes used throughout**

- **V** – verified fact, checked against a source document read in this workspace.
- **C** – computed by a project script; scripts and inputs are listed in Section 11.
- **R** – reported by an earlier run or report and not re-run in this session.
- **VJ** – visual judgment, recorded as a decision with a confidence label.
- **H** – hypothesis or assumption.
- **U** – unresolved.

---

## 2. Workspace and repository notes

- The deliverable workspace is `/mnt/user-data/outputs/` (283 files at inspection). Working folders and most intermediate arrays are under `/home/claude/work/`. Several scripts use absolute paths in that folder.
- No Git repository was found for this project. The only `.git` directory located under the searched paths belongs to a package cache. There is therefore no commit history to inspect. The remote GitHub repository was not accessed, and nothing has been committed, pushed, published, or uploaded.
- Several folders contain duplicate copies of the same images and packages, for example the Foxon-derived files under `z32_repro/`, `z32_independent_audit/`, and `z32_next_review/`. Duplicates were identified by file name and location only; they were not compared byte by byte.

---

## 3. Historical context

- **Z408** was published in newspapers on July 31, 1969 (S1, as stated by Foxon).
- **Z340** was published in the San Francisco Chronicle on November 8, 1969 (S1). Its ciphertext has 20 rows of 17 characters (S1; our reconstructed grid is 20 × 17).
- **Z32** is the cipher that accompanied the letter dated June 26, 1970 (S1). The ciphertext has two unequal rows of 17 and 15 symbols and a 29-symbol alphabet (S1).
- The Z32 letter includes a Phillips 66 road map, and the instruction that "0 is to be set to Mag. N." appears on the reproduced map (S1, figure and text).
- Foxon reports that the P.S. of the letter states that the "Mt. Diablo Code" concerns radians and inches along the radians (S1). This is the basis of the radian–inch hypothesis tested in Section 7.
- Foxon's Table 2 gives the Mount Diablo summit in NAD27 as 37° 52′ 54.387″ N, 121° 54′ 47.107″ W, and gives a magnetic declination of 16.9° for June 26, 1970, computed with an IGRF model (S1).
- The Z340 solution by Oranchak, Blake, and Van Eycke (S2) describes homophonic substitution combined with a transposition, a 63-symbol cipher alphabet, and a full plaintext. We verified the paper's header, authors, and text. We have not reproduced its decryption (R).

Publication dates above are as stated by Foxon and were not checked against newspaper archives (Section 14).

---

## 4. Sources

| ID | Source | Access in this workspace | Used for | Status |
|---|---|---|---|---|
| S1 | Floe Foxon, *On the 32-Character Zodiac Cipher* (2023) | `/mnt/user-data/uploads/2023-982.pdf`; a copy is in `z32_independent_audit/input/` | Z32 structure, historical dates, map instruction, Foxon's model and table values | V for the text read. The ePrint identifier 2023/982 comes from a URL seen during search and does not appear in the PDF text we read (C16). |
| S2 | D. Oranchak, S. Blake, J. Van Eycke, arXiv:2403.17350v1 (2024) | `/mnt/user-data/uploads/2403_17350v1.pdf` (62 pages) | Z340 key, transposition, reference plaintext, figures 1, 8, 42–44 | V for header (26 March 2024; category cs.AI), author names, and text. Figures were extracted by us (Section 8). |
| S3 | FBI Vault, *The Zodiac Killer*, parts 02–07 | Web fetch in an earlier session; not stored | Attempted source for map and instruction evidence | Partially read from prefixes only. Parts 05–07 have no machine-readable text (R; `z32_source_search/PHASE3_FBI_PARTS_2_TO_7.md`). |
| S4 | Phillips 66 and Gousha archives and catalogue records | Web search and fetch in an earlier session; not stored | Map publisher and edition | Summarized in `z32_source_search/PHASE2_SOURCE_REPORT.md` (R). |
| S5 | Secondary web material: blog posts, forum threads, a social-media post, a dealer listing, and a PDF summary of a Z340 key | Web search and fetch; not stored | Claims about map scale, edition, and key | Unverified (Section 14). |

---

## 5. Investigation timeline

1. **Foxon reproduction and independent audit** (`z32_repro/`, `z32_next_review/`, `z32_independent_audit/`). The audit package re-derives Foxon's transposition family, phrase tests, and a statistical test (C, R). In this session, `z32_independent_audit/run_all.sh` was re-run in an extracted copy of the uploaded archive. All 10 result files and both figure images compared as identical, which gives 12 identity checks (C; `/home/claude/work/rerun_log.txt`, final `EXIT=0`).
2. **Map calibration audit** (`z32_map_calibration_audit/`). Fits a figure-based scale of 1.162 miles per figure unit to five city labels (C). This scale describes the reproduced figure, not a measured physical scale.
3. **Source search** (`z32_source_search/`). Searched for the original Phillips 66 sheet and for FBI Vault material. No original map image was located (R; `z32_source_search/PHASE2_SOURCE_REPORT.md`, `z32_source_search/PHASE3_FBI_PARTS_2_TO_7.md`, `z32_source_search/PHASE4_STATUS.md`).
4. **Geometric convention audit** (`z32_phase5/`, `z32_phase5_audit/`). Checked the eight registered radials from Foxon's Figure 2 and the candidate coordinates against the Mount Diablo origin. The candidate lies 1.476 miles from the nearest registered radial at any scale (C; `z32_phase5_audit/audit_summary.json`).
5. **Z32 structure analysis** (`z32_structure/`). Repetition statistics and free-key readability tests (C; Section 7).
6. **H4a readiness** (`z32_h4/`). Pre-registered design and calibration on synthetic data (C). The test has not been run.
7. **Z340 source acquisition and reconstruction** (`z32_phase1/`, `z32_checkpoint/`, and the working folder `/home/claude/work/phase1/`). Extracted the key, the grid, the transposition, and the reference text, and iterated the glyph matcher through versions v1 to v4 (C, VJ).
8. **Matching methods M0–M5** (`z32_checkpoint/methods/`). Pre-registered six variants, selected M5 by the tuning rule, and measured held-out agreement (C).

---

## 6. What the evidence supports and does not support

**Supported by the evidence**

- Foxon's description of the Z32 layout (two rows, 29 symbols) and his dates and table values, as read from his text (V).
- The internal consistency of the Z340 extraction: 340 grid cells, 63 key glyphs with the counts described in Section 8, and a valid transposition permutation (C).
- A held-out letter-level agreement of 68.2% for the pre-registered method M5 (C). This is a measurement of the matcher, not of a decryption that has been verified end to end.
- The Z32 structural observation that the printed identities repeat only three times, which rejects small alphabets under the stated assumptions (C).

**Not supported by the evidence**

- Any decryption or readable plaintext of Z32 (C).
- The candidate coordinates as a location of the Z32 target (C).
- The published Z340 plaintext as reproduced by us (R).
- The H4a result, because the test has not been run (Section 10).

---

## 7. Z32: what has been established

**Layout and alphabet (V, S1).** Two rows of 17 and 15 symbols; a 29-symbol alphabet. Foxon also states that two symbols appearing once each are not present in the Z340 key. We did not verify which two symbols these are (C7).

**Repetition structure (C, `z32_structure/results_structure.json`).** In the printed order of the typeset transcription, three identities repeat, at positions 1/26, 2/32, and 6/14. Monte Carlo simulations with 20,000 samples per model were run (see C17 for the difference from the pre-registered 100,000). Consistent with the pre-registered two-sided test at α = 0.05:

- Rejected: uniform alphabets of 29 symbols; English homophonic models with 1, 2, or 3 symbols per letter.
- Borderline and rejected at the threshold: uniform alphabet of 54 symbols (p = 0.0248).
- Consistent: uniform alphabets of 63, 100, 165, 250, and 500 symbols; English homophonic models with 5, 8, 10, 15, and 20 symbols per letter.

These are statements about the distribution of repeats under simple models. They do not identify the cipher.

**Free-key readability (C).** A homophonic substitution search with a free key, scored by English bigram likelihood, does not exceed permutation nulls for any of the four printed-order variants (p = 0.788, 0.490, 0.510, and 0.457 for O1–O4). Calibration on 20 English 32-letter controls detected 2 of 20, giving power of 0.10. The test is therefore uninformative at this length.

**Foxon-model transposition family (C, R).** The audit package enumerates 204 configurations and finds 34 valid readings. Only 2 of the 34 agree with the figure layout (`z32_independent_audit/results/valid_orders.json`; `z32_independent_audit/docs/AUDIT_REPORT.md`). These results describe Foxon's model, not a decryption that has been confirmed.

**Literal phrase test (C).** For the phrase "TWELVEINCHESALONGTHETHREERADIANS", no configuration satisfies all three pairs. The paper's order satisfies one of three (`z32_independent_audit/results/literal_phrase_test.csv`).

**Statistical test (C, R).** The audit reports p = 0.417 over 3,544 phrases. It also concludes that this null model destroys positional structure, so the result does not show absence of signal (`z32_independent_audit/docs/AUDIT_REPORT.md`, sections 1 and 3).

**H4a (pre-registered, not run).** The design is in `z32_h4/PREREG_H4.md`. It tests whether the Z340 key applied to Z32 in printed order gives English-like text above a permutation null. The calibration (Section 10) used a uniform key of three symbols per letter, which differs from the real key distribution (C6). The test must not be run until the Z340 reconstruction is verified.

**Status.** No decryption, reading, or location for Z32 is supported by the evidence.

---

## 8. Z340 reconstruction

### 8.1 Inputs and their origins

| Input | Source | Method | Status |
|---|---|---|---|
| Reference plaintext (340 letters) | S2, page 31: bullet list (260 letters) and the Figure 42 passage (80 letters) | `pdftotext`; bracketed corrections replaced by the left-hand (original) form | Consistent with the symbol count. Not checked against any other transcription (V for text, C for extraction). |
| Transposition numbers (20 × 17) | S2 Figure 43 (page 31 raster image) | Tesseract OCR per cell, followed by visual correction of 14 cells | Permutation of 0–339 verified. Visual corrections documented. |
| Key table (63 glyphs, 21 letters) | S2 Figure 44 (page 31 raster image) | Connected-component and projection segmentation; atlas inspection | Per-letter counts match a visual count (C, VJ). |
| Cipher grid (20 × 17) | S2 Figure 1 (page 1 photograph of the cipher sheet) | Otsu thresholding; grid nodes from k-means on centroids; nearest component per cell | 340 cells; six low-ink cells (C). |
| Z32 figure | S2 Figure 8 (page 5) | Extracted | Not analyzed in this stage. |

### 8.2 Verification of the inputs

- **Grid.** 340 cells in a 20 × 17 lattice. Row spacing median 62.9 px (range 60.9–67.3); column spacing median 63.8 px (range 61.9–66.0). Six cells have low ink (below 30 pixels in the window). These six were matched with a fallback threshold and were spot-checked only (C).
- **Key.** 63 glyphs: A5, B2, C1, D3, E6, F1, G1, H1, I5, L3, M1, N5, O4, P2, R5, S4, T6, U3, V1, W2, Y2. The per-letter counts agree with a visual count of the figure and the atlas. We did not compare the key with any independent glyph table (VJ, C).
- **Transposition.** The 340 values form a permutation of 0–339 (C). Section 1 (rows 1–9) agrees with the (1,2)-decimation formula in all 153 cells. Section 2 (rows 10–18) differs from the same formula in 62 of 153 cells. Rows 19 and 20 differ from a single-row formula in 16 and 15 cells, respectively. That single-row formula assumes section offsets of 306 and 323, which is our assumption (C). The 14 OCR corrections were made by reading enlarged crops and are recorded in `z32_checkpoint/artifacts/trans_values_fixed.json` (VJ, C).
- **Reading direction.** The paper describes the decimation as a procedure (page 27): start at position 1, write the symbol, move down one row and right two columns, wrapping around. For section 1, the figure's numbers equal these reading indices (C). Two visual anchors agree with the reading direction. Reading position k = 1 is a plus-shaped glyph that matches H01, which gives the letter H required by the reference. Reading position k = 2 matches O04, which gives the letter O required by the reference (VJ). Position k = 0 failed under the algorithm (Section 8.8).
- **Reference length.** The reconstructed reference has 340 letters, equal to the symbol count (C). This is a consistency check, not an independent verification of the transcription.

### 8.3 The 62 transposition discrepancies

Section 2 contains 62 cells whose figure values differ from the pure decimation formula. The paper says that Figure 43 shows the transposition "with these corrections." We take the figure values as the authoritative permutation. The text we extracted does not describe the corrections cell by cell, so the 62 section-2 differences, and the 31 differences in rows 19 and 20 against our assumed formula, are **unverified corrections** (see Section 13, item C9). Section 1 has no differences.

### 8.4 Matching methods

Each cell is compared with all 63 key glyphs. The scoring has these components:

1. **Cell mask.** A 72 × 72 window around each grid node is thresholded with a local Otsu threshold. The connected component closest to the window centre, with at least 40 pixels, is kept.
2. **Size.** The glyph is cropped to its ink bounding box and scaled so that its longer side is 44 pixels, preserving aspect ratio. It is centred on a 52 × 52 canvas.
3. **Thickness.** In M0, M2, and M4 the glyph is skeletonized and then dilated with a disk (radius 2 in M0 and M4, radius 1 in M2). M1 and M5 use the mask directly. Skeletonization removes thickness differences but also removes the distinction between filled and outlined shapes.
4. **Orientation.** M0–M3 apply no rotation normalization. M4 and M5 search rotations from −6° to +6° in 2° steps and keep the best score per template.
5. **Translation.** The score is the maximum over integer shifts from −2 to +2 pixels in both directions.
6. **Similarity.** The Dice coefficient 2|A ∩ B| / (|A| + |B|) between a cell mask and a key mask, each dilated by one pixel.

| ID | Definition |
|---|---|
| M0 | Skeleton (radius 2), then dilation; Dice with ±2 px shifts. Baseline. |
| M1 | No skeleton; mask used directly; Dice with ±2 px shifts. |
| M2 | Skeleton (radius 1); Dice with ±2 px shifts. |
| M3 | Average of the M0 and M1 scores. |
| M4 | M0 with a rotation search from −6° to +6°. |
| M5 | M1 with a rotation search from −6° to +6°. |

M0 reproduces the earlier v4 identities exactly: zero differences in the top-1 identity across 340 cells (C).

### 8.5 Pre-registered validation design

- **Tuning set:** reading positions k = 0–169.
- **Validation set:** k = 170–339, fixed by position rather than chosen at random. The ten diagnostic cases and the six visual corrections all fall in the tuning set.
- **Metric:** the fraction of positions whose top-1 glyph has the same letter as the reference. This is a letter-level metric.
- **Selection:** the highest tuning accuracy; ties go to M0. The reference letters were used to compute the metric only, never to choose identities.
- **Target:** 70% is an exploratory target and does not change the selection rule.

Pre-registration: `z32_checkpoint/methods/PREREG_METHODS.md`.

### 8.6 Results (C)

| Method | Tuning (k < 170) | Validation (k ≥ 170) | 95% interval, validation | All 340 |
|---|---|---|---|---|
| M0 (baseline) | 0.624 | 0.594 | 0.519–0.665 | 0.609 |
| M1 | 0.659 | 0.671 | 0.597–0.737 | 0.665 |
| M2 | 0.565 | 0.565 | 0.490–0.637 | 0.565 |
| M3 | 0.688 | 0.688 | 0.615–0.753 | 0.688 |
| M4 | 0.653 | 0.629 | 0.555–0.698 | 0.641 |
| **M5 (selected by the tuning rule)** | **0.735** | **0.682** | **0.609–0.748** | 0.709 |

The intervals are Wilson 95% intervals with n = 170 for the validation column. The M5 interval is 60.9%–74.8%. These intervals were recomputed from `z32_checkpoint/methods/methods_results.json` in this session. An earlier report had typed them from printed output (C13).

**Selection and the M3 comparison.** Under the registered rule, M5 is selected because it has the highest tuning accuracy (0.735, against 0.688 for M3). On validation, M3 scores 0.688 and M5 scores 0.682, a difference of 0.006. That difference is well within the width of either interval. We did not switch to M3 after seeing the validation results, and the selection rule was not changed.

**Target.** M5 reaches 68.2% on the held-out sample, which is below the 70% exploratory target. The interval (60.9%–74.8%) is compatible with a true value near 70% and also with a value below it, so this result does not establish that the method is correct or incorrect at the 70% level.

The 0.709 figure for all 340 positions includes the tuning positions used for selection, so it is not a validation result.

### 8.7 Validation errors for M5 (C)

- 54 of the 170 validation positions are wrong.
- For these 54, the reference letter's best glyph ranks 2–5 in 29 cases, 6–10 in 11, and beyond 10 in 14.
- Median margin (top-1 score minus top-2 score): 0.050 for correct positions and 0.022 for errors. The margin is informative on average but not for individual cells.
- No single confusion dominates. The most frequent confusion pairs occur twice each.
- Four key glyphs are never chosen as top-1 at any of the 340 positions under M5: A04, L02, S02, and U03.

### 8.8 Visual judgments and corrections (VJ)

For the first ten mismatches of the M0 mapping, a blinded review presented each cell with five candidate glyphs. Candidate positions and labels were shuffled, and the sheet carried no letter names or key identifiers. Verdicts were recorded in `z32_checkpoint/artifacts/verdicts_first10.json` before the mapping was revealed (`z32_checkpoint/FIRST10_MISMATCH_AUDIT.md`).

| k | Cell | Visual verdict (confidence) | M0 top-1 (letter) | Reference letter | Applied |
|---|---|---|---|---|---|
| 0 | r1c1 | I01 (high) | O04 (O) | I | Yes |
| 7 | r8c15 | U03 (high) | T04 (T) | U | Yes |
| 10 | r2c4 | E03 (medium-high) | T03 (T) | E | Yes |
| 12 | r4c8 | not decided | U02 (U) | A | No |
| 14 | r6c12 | not decided | T03 (T) | I | No |
| 17 | r9c1 | L01 (medium-high) | Y01 (Y) | L | Yes |
| 23 | r6c13 | F01 (high) | V01 (V) | F | Yes |
| 25 | r8c17 | N05 (medium-high) | L02 (L) | N | Yes |
| 26 | r9c2 | not decided; the shape is "<", and the "<" glyph I04 ranks 15th (not verified visually) | E01 (E), margin 0.094 | I | No |
| 28 | r2c6 | T03 (low; between T03 and E01) | V01 (V), margin 0.125 | T | No |

**Independence.** The reviewers had seen some reference letters in earlier outputs, so the independence of the verdicts is partial. In the six applied cases, the visual verdicts agree with the reference letters. This is part of the record and does not by itself show that the verdicts were free of reference influence. The six corrections need a second, independent reviewer.

### 8.9 Full 340-position result (C, VJ)

- Algorithmic top-1 (M0, identical to v4): 207 of 340 (60.9%).
- With the six visual corrections: 213 of 340 (62.6%).
- Remaining mismatches: 127. For 75 of them, the best glyph of the reference letter ranks 2–5; for 27 it ranks 6–10; for 25 it ranks beyond 10. These ranks are diagnostic only. The most frequent confusions are R→A (7), T→R (6), D→O (5), and Y→E (5).

The 213 figure includes manual visual corrections. It is not an algorithmic accuracy and should not be compared with the 68.2% validation figure, which uses no manual corrections.

### 8.10 Robustness of the top-1 identities (C)

Changes in the M0 top-1 identity across the 340 cells:

| Perturbation | Changed identities |
|---|---|
| Crop window 30 px (instead of 36 px) | 24 (7.1%) |
| Crop window 42 px | 18 (5.3%) |
| Rotation +4° | 58 (17.1%) |
| Rotation −4° | 70 (20.6%) |

Five cells have a selected component that touches the window border. Two cells have another glyph-sized component within 6 pixels. Rotation is the largest source of instability among the factors tested. Size normalization was fixed at 44 pixels and was not varied.

### 8.11 Failure modes

1. **Stroke and fill.** Skeletonization in M0 discards the distinction between filled and outlined shapes. Removing it (M1) raises validation accuracy from 0.594 to 0.671. Filled-versus-outlined confusion remains a plausible cause of errors, but we have not isolated it (H).
2. **Rotation.** Rotations of ±4° change 17–21% of M0 identities. A rotation search improves both M0 and M1 (M4 and M5), which indicates that orientation is part of the problem.
3. **Missing candidates.** For several cells the correct glyph is not among the top five. Examples include the "<" glyph and the square-with-triangle glyphs (VJ).
4. **High-margin errors.** Two cells (k = 26 with margin 0.094, and k = 28 with margin 0.125) are wrong by visual judgment despite large margins (VJ).
5. **Under-selected glyphs.** U03 is visually confirmed at k = 7 with high confidence, yet M5 never selects it (Section 13, item C4).

---

## 9. Geographic and map hypotheses

### 9.1 Foxon's model (S1)

Foxon's model takes the NAD27 summit of Mount Diablo as the origin and uses a declination of 16.9° for June 26, 1970, computed with an IGRF model (not measured). It converts the watch-face reading to hour and minute with hour = floor(d/30) and minute = round(d/6). For d = 16.9 this gives 12:03, which yields r = 12 and θ = 3 radians. Foxon's Figure 2 illustrates the point (12, 3) for all four reference axes and both directions.

Our pixel check located six of the eight marker positions automatically, within 1.1° of the predicted angles. The two right-hand markers could not be located reliably by the automatic method and were checked only by visual coordinates (C, VJ; `z32_phase5_audit/AUDIT_PHASE5_REPORT.md`, section 7).

### 9.2 Results of the geometric audit (C)

- **Candidate:** 37.929792, −122.150318. Distance from Mount Diablo: 13.352 miles. Bearing: 284.461°.
- **Nearest registered radial:** E-CCW, with an angular offset of 6.348°. The distance from the candidate to that radial is 1.476 miles.
- No registered radial passes within 0.5 miles of the candidate at any tested scale. The pre-registered "supported" rule therefore cannot be satisfied under the registered conventions (`z32_phase5_audit/audit_summary.json`).
- **Model A (free pole offset)** reproduces 37.92961, −122.15045, which is 23 meters from the candidate. Model A places the pole about 2.67 miles from the crosshair. This value was computed in our reproduction script and is not stored as a separate file.
- **Model C (pole fixed at Mount Diablo)**, which follows Foxon's assumption, gives 37.90253, −122.15078, which is 1.88 miles from the candidate. This value was computed with `reproduce_models.py` (included in this archive at `z32_phase5_audit/analysis/reproduce_models.py`) in the working folder (`/home/claude/work/analysis/`) and is included in this archive.
- **Scale band.** A scale band derived from the claim that San Francisco lies about five inches from Mount Diablo on the map gives [4.833, 7.486] miles per inch. This band is conditional on the claim (C). Against it, the registered endpoints lie 44.75 to 103.11 miles from the candidate (`z32_phase5/phase5_summary.json`).

**Status.** The candidate is not confirmed. It is not supported under the registered conventions. Its provenance is not recorded in any project file.

### 9.3 Scale

- The figure-based scale is 1.162 miles per figure unit (`z32_independent_audit/results/map_audit_models.csv`). It describes the reproduced figure, not the printed map.
- The printed scale is unknown. Claims of 6.4 miles per inch and of a five-inch distance to San Francisco come from secondary sources (S5) and are not verified (Section 14).

### 9.4 Map source and edition

- The Phillips 66 map has not been found in an original or archival image. A Library of Congress finding aid lists Phillips 66 as the publisher of California and San Francisco regional maps, without dates (S4; `z32_source_search/PHASE2_SOURCE_REPORT.md`).
- Claims of a 1969 edition come from a forum owner's copy, a 2026 social-media post, and a secondary website. A 2022 forum post describes a 1968 copy. These claims conflict, and no imprint image was examined (Section 13, item C11).
- A dealer listing titled as a 1969 Phillips 66 road map of St. Louis, published by H. M. Gousha, is evidence about the publisher of Phillips 66 maps in 1969. It is not evidence about the San Francisco sheet.

---

## 10. Hypotheses register

| ID | Hypothesis | Status | Evidence | Next test |
|---|---|---|---|---|
| H-Z340-1 | The published Z340 decryption (Blake et al.) is correct | Reported, not reproduced | S2 text; our reconstruction reaches 68.2% on held-out positions | Identity-level blinded validation; full reproduction with verified glyphs |
| H-Z340-2 | Glyph identity matching is the main source of error | Partially supported | Failure modes 1–5 in Section 8.11; rotation sensitivity | A new pre-registered matcher, tested on a fresh validation sample |
| H-Z340-3 | Figure 43 is the correct final transposition | Partially supported | Permutation check; section 1 agreement; visual anchors | Locate a text or supplement that describes the corrections |
| H-Z32-1 | Z32 uses the literal radian and inch phrase | Not supported | Literal phrase test (C) | None planned without new data |
| H-Z32-2 | Foxon's transposition family yields readable text | Not supported | 34 valid readings; 2 match the figure layout (C) | Re-examine assumptions with verified Z32 identities |
| H-Z32-3 | Z32 shares its key with Z340 | Pending | Foxon's statement about two symbols; H4a design | Run H4a after the Z340 reconstruction is verified |
| H-Z32-4 | Z32 encodes numbers | Untested | The instruction text mentions radians and inches | Requires a calibrated numeric model |
| H-MAP-1 | The candidate is the Mount Diablo location | Not supported | Section 9.2 | Physical scale and map imprint |
| H-MAP-2 | The printed map scale is about 6.4 miles per inch | Unverified | S5 claims | Measure a physical or high-resolution copy |
| H-MAP-3 | The map is the 1969 edition | Unresolved | Conflicting claims | Imprint image of an original copy |

### 10.1 H4a calibration (C)

From `z32_h4/calibration_h4.json`, read in this session. The calibration was **not re-executed** in this session.

| Correct key fraction | Power at p < 0.01 | Power at p < 0.0025 | Median p |
|---|---|---|---|
| 1.0 | 0.980 | 0.963 | 0.001 |
| 0.9 | 0.923 | 0.797 | 0.001 |
| 0.8 | 0.713 | 0.583 | 0.001 |
| 0.7 | 0.500 | 0.330 | 0.010 |
| Wrong key (H0) | 0.010 (false positive rate) | 0.000 | 0.488 |

The calibration used a uniform key of three symbols per letter. The real Z340 key counts per letter are 5, 2, 1, 3, 6, 1, 1, 1, 5, 3, 1, 5, 4, 2, 5, 4, 6, 3, 1, 2, and 2 (Section 8.2). The calibration therefore does not represent the real key distribution. This must be corrected, and the change documented, before H4a is run (C6).

---

## 11. Reproducibility

### 11.1 Environment observed in this session

Python 3 with numpy 2.4.4 and Pillow 12.1.1 (observed). Versions of scipy, scikit-image, and scikit-learn were not recorded. Poppler utilities (`pdftotext`, `pdfimages`, `pdftoppm`) and the Tesseract command-line tool were used. Network access was disabled in the working container, so no source was downloaded during reproduction.

### 11.2 Experiments

**Foxon audit package** (`z32_independent_audit/`). Run `bash run_all.sh` (`z32_independent_audit/run_all.sh`) from the package directory. The package includes `z32_independent_audit/input/2023-982.pdf`. `z32_independent_audit/requirements.txt` lists numpy ≥ 1.21 and Pillow ≥ 9.0, and the script calls `pdfimages`. *Status:* re-run in this session; 12 identity checks passed (C).

**Z340 reconstruction** (`z32_checkpoint/scripts/`). Requires the arXiv PDF (`/mnt/user-data/uploads/2403_17350v1.pdf`) to regenerate `img/` with `pdfimages` and `pdftoppm`, and the Tesseract command-line tool for `z32_checkpoint/scripts/trans_ocr_cells2.py`. The scripts are meant to run in this order: `z32_checkpoint/scripts/seg_key3.py`, `z32_checkpoint/scripts/build_key.py`, `z32_checkpoint/scripts/z340_cells.py`, `z32_checkpoint/scripts/z340_match.py` (or `z32_checkpoint/scripts/match_v4.py`), `z32_checkpoint/scripts/trans_ocr_cells2.py`, `z32_checkpoint/scripts/trans_fix.py`, `z32_checkpoint/scripts/fix_order.py`, `z32_checkpoint/scripts/verify_transposition.py`, `z32_checkpoint/scripts/compare_z340.py`. They use the working folder `/home/claude/work/phase1/`. Some intermediate inputs (`img/`, `z340_yr.npy`, `z340_xc.npy`) are not stored in the outputs folder. *Status:* reproduced only in the working folder; not reproducible from the outputs folder alone.

**Methods comparison M0–M5** (`z32_checkpoint/methods/methods_experiment.py`). Requires `z32_checkpoint/scripts/match_v4.py` (in `z32_checkpoint/scripts/`), `img/p01-000.png` and `img/p31-002.png` (not in the outputs folder), and `z340_yr.npy` and `z340_xc.npy` (not in the outputs folder). The key and transposition artifacts are present. *Status:* not reproducible from the outputs folder alone. The recorded run took about 193 seconds.

**H4a calibration** (`z32_h4/calibrate_h4.py`). Requires the system files `/usr/share/common-licenses/GPL-2` and `GPL-3`, which may differ across systems. *Status:* not re-executed in this session; the recorded results were read from `z32_h4/calibration_h4.json`.

**Z32 structure analysis** (`z32_structure/run_structure.py`). Requires the audit package transcription (`z32_independent_audit/data/z32_fig1A_transcription.csv`), the package resolved relative to the archive root, and the GPL files. *Status:* results read from `z32_structure/results_structure.json`; not re-executed in this session.

**Geometric audit** (`z32_phase5_audit/audit_phase5_independent.py`). In this archive copy, paths are resolved relative to the archive root (see `docs/ARCHIVE_CHANGES.md`). *Status:* recorded results match `z32_phase5_audit/audit_summary.json` (C); not re-executed in this session.

**Not reproducible here.** The FBI Vault reads and the web-source searches (S3, S4), because the source pages were not stored and the network is disabled.

---

## 12. Unresolved questions and planned next steps

### 12.1 Unresolved questions

1. Why does our reconstruction reach 68.2% on held-out positions, when the published work reports a full decryption? Glyph matching, the transposition corrections, and the reference text are all possible causes, and none has been isolated.
2. Which of the 62 section-2 differences, and the 31 differences in rows 19 and 20, reflect the corrections that the paper describes?
3. What are the true identities of the four glyphs that M5 never selects (A04, L02, S02, U03)? Does the glyph confirmed visually at k = 7 occur elsewhere?
4. Which two Z32 symbols are absent from the Z340 key, and is that statement correct?
5. What is the printed scale of the Phillips 66 sheet, and does the Mount Diablo to San Francisco distance measure about five inches on it?
6. Which edition of the map did Zodiac use: 1968, 1969, or another?
7. Where did the candidate coordinates 37.929792, −122.150318 come from?
8. Did Zodiac apply a rule to convert declination into hour and minute, and if so, which rule?

### 12.2 Planned next steps (none has been started)

1. Obtain a high-resolution facsimile of the Z340 cipher and of the Z32 cipher, and verify the glyph identities.
2. Create a blinded, identity-level validation sample of about 40 random cells, labelled visually before any new matcher is tested. Use it only for validation.
3. Correct the H4a calibration to the real key distribution, record the change before running, and then run H4a as pre-registered.
4. Find a physical or high-resolution copy of the map, and check the printed scale bar and the imprint. Measure the Mount Diablo to San Francisco distance on it.
5. Find a text or supplement that describes the corrections in Figure 43, before accepting the sections 2–4 values.
6. Establish the provenance of the candidate coordinates. If it cannot be established, treat them as an unverified input.

---

## 13. Contradictions and discrepancies (not resolved)

- **C1. Two Z340 accuracy figures.** 207 of 340 (algorithm alone) and 213 of 340 (with six visual corrections). Both are correct for what they measure. Neither is the 68.2% validation figure, which uses 170 positions.
- **C2. Overall M5 figure.** 70.9% over all 340 positions includes the positions used to select M5. The held-out figure is 68.2%.
- **C3. M3 versus M5 on validation.** M3 scores 0.688 and M5 scores 0.682. The registered rule selects M5 on tuning accuracy. The difference lies within the intervals.
- **C4. U03.** Visually confirmed at k = 7 with high confidence, yet never selected by M5. The algorithm and the visual judgment disagree, and this is unresolved.
- **C5. Margin reliability.** Median margins differ between correct and wrong positions (0.050 and 0.022), but two wrong cells have large margins.
- **C6. H4a calibration.** The calibration assumes a uniform key of three symbols per letter. The real key counts differ. The calibration does not represent the real key.
- **C7. Foxon's shared-symbol statement.** Foxon says two Z32 symbols are absent from the Z340 key. We have not verified this.
- **C8. Reported decryption versus our reconstruction.** The paper reports a full decryption. Our reconstruction does not reproduce it, and the cause is not isolated.
- **C9. Transposition corrections.** The paper says Figure 43 includes corrections. The extracted text does not describe them, so the differences in sections 2–4 remain unexplained.
- **C10. Scale claims.** The figure-based scale (1.162 miles per unit) and the claimed printed scale (6.4 miles per inch) disagree. The San Francisco scale band depends on the second.
- **C11. Map edition.** Claims of a 1969 edition and of a 1968 copy conflict. No imprint image was examined.
- **C12. Two model variants.** Model A (free pole, which reproduces the candidate) and model C (pole at Mount Diablo) differ by 1.88 miles.
- **C13. Process record for the M-methods.** The intervals were first typed into the report from printed output, because the diagnostics file was not written after a script error. They were recomputed from the raw results in this session and agree with the report.
- **C14. Re-run count.** An earlier summary described the re-run as "10 files identical". The log contains 12 identity checks: 10 result files and two images.
- **C15. Earlier geometric report.** An early version reported 60–103 miles at 6.4 miles per inch. The correct range for 6.4 alone is 63.55–90.08 miles. The early version also mixed the labels "unsupported" and "contradicted". The corrected figures are used here.
- **C16. ePrint identifier.** The identifier 2023/982 comes from a URL seen in search results and is not printed in the PDF text we read.
- **C17. Simulation count in the structure test.** The pre-registration (`z32_structure/PREREG_structure.md`) specifies 100,000 simulations per model. The executed code (`z32_structure/run_structure.py`) uses 20,000 per model. This is a deviation from the pre-registered design. It affects the precision of the p values but not the decision thresholds, which are unchanged. It is recorded here rather than resolved.

---

## 14. Claims not independently verified

- Grinell's claim that San Francisco lies about five inches from Mount Diablo on the map (S5).
- Grinell's scale of 6.4 miles per inch, and the claim that the printed scale appears on the bottom margin of the map (S5).
- Forum claims of a 1969 imprint, of map dimensions of 18.75 by 34 inches, of a section of 8 by 6.75 inches, and of an identifier 9-QQ-1219-S (S5).
- A 2026 social-media post claiming a "1969 Edition" imprint (S5).
- A 2022 forum post describing a 1968 copy and differences from the 1969 copy (S5).
- The dealer listing for a 1969 Phillips 66 road map of St. Louis (S5).
- The partial key mappings in the Hodel document (S5).
- The publisher statement from the Library of Congress finding aid, as summarized in our report (S4).
- The FBI file number 9-HQ-49911, as read by OCR from part 01 (S3).
- The Z340 solution and its plaintext, as reported in S2 (reported, not reproduced).
- Foxon's statement about two symbols absent from the Z340 key (S1).
- The IGRF declination value of 16.9°, computed by Foxon and not recomputed here (S1).
- The publication dates of Z408, Z340, and Z32, as stated by Foxon (S1). These were not checked against newspaper archives.
- The archival label on the Z340 photograph, which is partly legible and was not used.

---

## 15. Images

**Result: no qualifying original images were found, and this dossier contains no images.**

The workspace holds 45 image files (PNG or JPEG) across the working and output folders, including duplicates. None of them qualifies under the eligibility rules, which require an image to be our own creation and not a copy of a publication or an archival source.

| Group | Count | Origin evidence | Decision |
|---|---|---|---|
| Copies of pages 8 and 9 of the Foxon PDF (`fig1_all_panels_p8_native.png`, `fig2_map_p9_native.png`) | 16 | Named as native extractions of the Foxon PDF; the content is the publication's figure | Excluded: copied from a publication |
| Overlays and crops on the Foxon figure (`fig2_grid_overlay_for_reading.png`, `fig2_center_2x.png`, `p7-07.png`, `p7_formula_crop.png`, and copies) | 8 | Generated by our scripts, but the base image is the publication's figure. The origin of `p7-07.png` is not confirmed beyond its name. | Excluded: annotated images of another researcher's figure |
| Extracted from the arXiv Z340 paper and from the archival photograph (`phase1/img/*`) | 8 | Extracted with `pdfimages` from the uploaded PDF | Excluded: copied from a publication or archival source |
| Composites and crops built from the groups above (`key_atlas*.png`, `check_first_cells.png`, `blind_review*.png`, `trans_suspect*.png`, `trans_bw.png`, `tmp_num.png`) | 9 | Generated by our scripts from the groups above | Excluded: contents derived from others' images |
| Copies of composites in `z32_checkpoint/figures/` | 4 | Duplicates of the composites above | Excluded |

A glyph atlas built from crops of the published key figure could be argued to be our own arrangement. We excluded it, because the glyph content is copied from the publication. We did not generate new images for this dossier.

---

## 16. Supporting files

Paths are relative to the workspace root, `/mnt/user-data/outputs/`. Each file listed below was checked for existence (Section 17).

**Status and reports**

- `z32_checkpoint/STATE.md`: resume point and status history.
- `z32_checkpoint/FIRST10_MISMATCH_AUDIT.md`: blinded review of the first ten mismatches.
- `z32_checkpoint/FULL63_REPORT.md`: full 63-glyph scoring and residuals.
- `z32_checkpoint/METHODS_REPORT.md`: comparison of M0–M5 and validation.
- `z32_checkpoint/methods/PREREG_METHODS.md`: pre-registration of the methods.
- `z32_checkpoint/methods/VALIDATION_LOG.md`: data validation log.
- `z32_phase1/PHASE1_SOURCES_STATUS.md`: source acquisition status.
- `z32_h4/PREREG_H4.md` and `z32_h4/REPORT_H4_readiness.md`: H4a design and readiness.
- `z32_structure/PREREG_structure.md` and `z32_structure/REPORT_structure_short.md`: Z32 structure analysis.
- `z32_phase5_audit/AUDIT_PHASE5_REPORT.md`: geometric audit.
- `z32_source_search/PHASE2_SOURCE_REPORT.md`, `z32_source_search/PHASE3_FBI_PARTS_2_TO_7.md`, and `z32_source_search/PHASE4_STATUS.md`: source searches.

**Data and results**

- `z32_checkpoint/artifacts/key_table_glyphs.csv`: 63 key glyphs with bounding boxes.
- `z32_checkpoint/artifacts/trans_values_rowmajor.json`: transposition values in row-major order.
- `z32_checkpoint/artifacts/compare_z340_v4.json`: reference text and reconstruction.
- `z32_checkpoint/artifacts/mismatch_positions_v4.csv`: mismatched positions with matcher output.
- `z32_checkpoint/methods/methods_results.json`: M0–M5 accuracies.
- `z32_checkpoint/methods/M5_top5_all340.csv`: top-five glyphs for all 340 positions under M5.
- `z32_checkpoint/full63/full63_residuals.csv`: residual mismatches after corrections.
- `z32_checkpoint/full63/robustness_results.json`: sensitivity results.
- `z32_h4/calibration_h4.json`: H4a calibration results.
- `z32_structure/results_structure.json`: Z32 structure results.

**Scripts** are listed in Section 11.

---

## 17. Verification log for this dossier

| Check | Result |
|---|---|
| M0–M5 accuracies (tuning, validation, all) | Match `z32_checkpoint/methods/methods_results.json` |
| M5 validation 0.682 = 116 of 170 | Confirmed from the raw counts (54 mismatches of 170) |
| M5 validation interval, 60.9%–74.8% | Recomputed with the Wilson formula, n = 170: 0.609–0.7476 |
| M3 validation interval | Recomputed: 0.615–0.753 |
| 207 and 213 of 340 | Match `z32_checkpoint/full63/full63_residuals.json` |
| 127 residual mismatches | Match `z32_checkpoint/full63/full63_residuals.json` |
| Robustness counts (24, 18, 58, 70; 5 border cells; 2 neighbour cells) | Match `z32_checkpoint/full63/robustness_results.json` |
| 14 OCR corrections | Match `z32_checkpoint/artifacts/trans_values_fixed.json` |
| Section 1 agreement 153 of 153; section 2 differences 62 | Recomputed from `z32_checkpoint/artifacts/trans_values_rowmajor.json` |
| Rows 19–20 differences 16 and 15 | Recomputed against the assumed offsets 306 and 323 |
| Reference length 340; position agreement 0.6088 | Match `z32_checkpoint/artifacts/compare_z340_v4.json` |
| H4a calibration values | Match `z32_h4/calibration_h4.json` |
| Candidate distance 13.352 mi, bearing 284.461°, offset 6.348°, minimum 1.476 mi | Match `z32_phase5_audit/audit_summary.json` |
| Scale band 4.833–7.486 and San Francisco distances 26.58 and 33.69 mi | Match `z32_phase5/phase5_summary.json` |
| Structure: R = 3, K = 29, readability p values, power 0.10 | Match `z32_structure/results_structure.json` |
| Simulation count, 100,000 pre-registered versus 20,000 executed | Confirmed in `z32_structure/PREREG_structure.md` and `z32_structure/run_structure.py` (C17) |
| Paper facts (63 symbols; 26 March 2024; authors) | Found in the extracted text of the uploaded arXiv PDF |
| Foxon facts (dates, 17 and 15 rows, 29 symbols, 54-symbol Z408 alphabet, Mag. N. instruction, Table 2 values, P.S. wording) | Found in the extracted text of the uploaded Foxon PDF |
| Re-run identity checks (12) | Recorded in `/home/claude/work/rerun_log.txt` (working folder) |
| Literal phrase test | Matches `z32_independent_audit/results/literal_phrase_test.csv` |
| Valid orders (34) | `z32_independent_audit/results/valid_orders.json` contains 34 entries |
| Configuration count (204) and p value (0.417) | Taken from the text of `z32_independent_audit/docs/AUDIT_REPORT.md`; not recomputed |
| Internal links | Checked programmatically after writing this file |
| Images | 45 found; none embedded |

**Items that were not re-verified:** the 204 configuration count and the 0.417 p value (taken from the audit report text); the FBI Vault and web sources, which were not re-accessed; and the intermediate arrays used by the Z340 scripts, which are in the working folder rather than the outputs folder.
