> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 6c60794b56e58a515907980a9a830be9a781038f827f531a39ee304e3da781d0.

# Resume point for the Z32 investigation (Z340 first)

## General status

- Stage: verification of reproducing the published Z340 solution: **not completed** (position-wise agreement only 0.609).
- H4a test: **not run** (not permitted before the Z340 reproduction succeeds).
- Z32: **halted**, according to the agreed rule.

## Original source (verified)

- File: /mnt/user-data/uploads/2403_17350v1.pdf (62 pages, embedded text).
- Paper: Oranchak, Blake and Van Eycke, arXiv:2403.17350.
- Figure locations: figure 1 (Z340 photograph) on page 1; figure 8 (Z32) on page 5; figures 42, 43 and 44 on page 31; figure 56 (Z32 letter document) on page 50.
- Reference text: extracted from page 31 (two blocks: 260 + 80 = 340 letters), after removing the corrections in brackets, using the raw left-hand reading.

## What was verified (with evidence)

1. **Key table (figure 44):** 63 glyphs, cut out and labelled. The number of glyphs per letter matches the visual count (A5 B2 C1 D3 E6 F1 G1 H1 I5 L3 M1 N5 O4 P2 R5 S4 T6 U3 V1 W2 Y2). Evidence: artifacts/key_table_glyphs.csv and figures/key_atlas_final.png.
2. **Transposition definition (pages 24 and 27):** (1,2)-decimation within four sections: rows 1–9, rows 10–18, row 19, and row 20. The cell numbers in figure 43 are the "reading order".
3. **Independent check of the transposition numbers:** the 340 values form a complete permutation from 0 to 339.
   - Section 1 (rows 1–9): 153 of 153 cells match the mathematical formula.
   - Rows 10–20: 93 cells differ from the pure formula, and agree with the textual mention of "corrections" in figure 43. I could not verify the corrections independently, so the figure's values were kept as they are.
4. **Reading direction:** the cell with number k is the k-th symbol of the sequence. Visual evidence: k = 1 is a "+" sign = H01 = letter H, as expected; k = 2 is an M-shaped sign = O04 = letter O, as expected.
5. **Length of the reference text = number of symbols (340).** This is a consistency check on the reference text.

## What did not verify (failed or incomplete)

- **Position-wise agreement between the decryption and the reference text: 0.609** (133 disagreements out of 340). This is not a reproduction.
- **Symbol matching is unreliable:**
  - 116 cells have a margin below 0.03 (out of 340).
  - 6 key identifiers were not used in the grid (B02, L01, P02, R04, S02, U03), although the paper says all 63 symbols are used. This contradiction indicates matching errors.
- **Smallest failing example:** the first symbol (k = 0, row 1, column 1). The visible shape is a thin-stroked H, and the expected letter is I01 (I), but the matcher (v4) gave O04 (O). The four tested matchers gave N03, then S03, then E03, then O04 for the same cell. This cell therefore reveals the weakness of the matching, not an error of order.
- **Other examples of disagreement (k: extracted/expected):** 7: U/T; 10: T/E; 12: U/A; 14: T/I; 17: Y/L (details in artifacts/mismatch_positions_v4.csv).

## Not yet done

- Full reproduction of the solution (the condition for moving to Z32): no.
- Visual review of the ambiguous symbols and confirmation of their identity, followed by re-decryption.
- Verification of the Z32 symbol identities against the current transcription (figure 8, page 5; file p05-000.png not yet analysed).
- Calibration of H4a with the real key distribution (5, 2, 1, 3, 6, 1, 1, 1, 5, 3, 1, 5, 4, 2, 5, 4, 6, 3, 1, 2, 2 symbols per letter) instead of the uniform assumption (3 per letter). Changing the calibration assumption must be documented before running. It does not change the hypothesis or the threshold.

## Proposed next step

1. Visual review of the ambiguous cells (116 cells and the 6 unused identifiers), showing the top three candidates for each cell, and confirming by looking, not by guessing.
2. Re-decrypt, and measure the position-wise agreement with the reference text. The goal is full reproduction; any difference must be documented against its reference in the paper (the bracketed corrections).
3. Only after success: verify the Z32 identities and run H4a as registered (PREREG_H4.md).

## Resumption rules

- Saved extractions in artifacts/ are not regenerated unless there is a documented reason.
- Transposition values are not changed after seeing the results, and the matching is not adjusted to fit the reference text. Any change is documented as a visual correction for a specific cell, with its image.
- No difference is resolved by guessing.

## Scripts (scripts/), in order

seg_key3.py, then build_key.py, then trans_ocr_cells2.py, then trans_fix.py, then fix_order.py, then verify_transposition.py, then z340_cells.py, then z340_match.py, then match_v4.py, then compare_z340.py.

## Update: review of the first ten disagreements (see FIRST10_MISMATCH_AUDIT.md)

- 6 documented visual corrections (k = 0, 7, 10, 17, 23, 25); agreement 0.609 to 0.626.
- 4 unsettled cases among the first ten (k = 12, 14, 26, 28). k = 26 is an example that a high margin does not guarantee correctness.
- The 116 low-margin cells have still not been reviewed.

## Update: method-improvement experiment (see METHODS_REPORT.md)

- Pre-registration: PREREG_METHODS.md. Tuning set k = 0 to 169; validation set k = 170 to 339.
- The method selected in advance by the tuning rule: M5 (raw mask + size normalisation + rotation search ±6°). Tuning 0.735; validation 0.682 (95 % interval 0.609 to 0.748).
- The exploratory 70 % target was not reached on the validation sample. The method was not changed after seeing the result. H4a and Z32 are not run.
- U03 (visually confirmed at k = 7) is never chosen first at any position under M5. This is evidence of a systematic fault in the matching.
