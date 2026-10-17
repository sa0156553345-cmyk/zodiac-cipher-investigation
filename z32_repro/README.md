> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 923150ceddecbdab9b98120c97c9791c5ed6977271524933ab49f6aceec230a3.

# z32_repro: Z32 re-test bundle (Foxon 2023: figures 1 and 2)

## 0. What this bundle proves, and what it does not

- **It proves:** the reading of row (C) in figure 1, from its pixel data; the reproduction of its arrangement by one rule from a family of 204 settings; the testing of given phrases against the repetition constraint; and the measurement of the circle scale in figure 2.
- **It does not prove:** that any phrase is a solution to the Z32 cipher. The test did not produce a phrase that appears unmodified under any valid order.
- The figure used is ASCII printed by the authors, not the original Zodiac symbols.

## 1. Contents

| File or folder | Function |
|---|---|
| `input/2023-982.pdf` | the original Foxon paper (1.1 MB; included because it is small) |
| `fig1_all_panels_p8_native.png` | figure 1 (A–D) from page 8, extracted unmodified (987 × 498) |
| `fig2_map_p9_native.png` | figure 2 (the map) from page 9, unmodified (916 × 894) |
| `z32_fig1A_transcription.csv` | visual transcription of row (A), used only to label identity categories |
| `fig_glyph_check.py` → `fig_glyph_check.csv` | pixel comparison of the symbols, with no visual reading, to determine identity and the reading of (C) |
| `transposition_family.py` → `z32_all_configs.csv` | the 204 settings and their results, and the checking of orders |
| `transposition_family.py` → `z32_phrase_tests.csv` | phrase tests, compared with a random model |
| `map_check.py` → `map_check.csv` | measurement of the circles in figure 2, compared with source coordinates only |
| `extract_figures.sh` | extraction of the two images from the PDF |
| `run_all.sh` | runs all of the above in order, with extraction and fingerprint checks |
| `requirements.txt` | dependencies (numpy and Pillow) |
| `CHECKSUMS.txt` | SHA-256 fingerprints of all files |
| `run_log.txt` | output of an actual run of `run_all.sh` in this bundle |
| `superseded/` | earlier results and withdrawn files, with `README_SUPERSEDED.md` explaining each |

## 2. Requirements

- Python 3.9 or later, with numpy and Pillow.
- `pdfimages` (from poppler-utils) for the PDF extraction step; optional.
- `sha256sum` and `cmp` (usually present on Linux and macOS).
- No internet access is needed.
- On Windows: use WSL, or run the scripts in order by hand and skip the extraction step.

## 3. Step-by-step run

1. Unzip the bundle, then enter the folder:
   ```bash
   unzip z32_repro_bundle.zip
   cd z32_repro
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run all tests:
   ```bash
   bash run_all.sh | tee run_log_mine.txt
   ```
   The script runs in order: the extraction check from the PDF (if `pdfimages` is available), then `fig_glyph_check.py`, then `transposition_family.py`, then `map_check.py`, then the fingerprint check.
4. Check the fingerprints. Note that `CHECKSUMS.txt` and `run_log.txt` are excluded from the list itself: the first records the fingerprints, and the second records the run.
   ```bash
   sha256sum -c CHECKSUMS.txt
   ```
   Expected: OK for each file.
5. Compare your output with `run_log.txt`. The main numbers in section 4 should match.

## 4. Expected results (main numbers)

- Identity categories matched by pixel in figure (A): 29 categories, with repetition at the positions {1, 26}, {2, 32} and {6, 14}.
- Row (B) is pixel-identical to row (A): difference 0.
- Pixel reading of (C): `CX2VAC7PGID4H6?TJF3!5LR118O9MEOW`.
- Number of settings: 204, of which 34 are valid readings, all with wrap W1 and skip E2.
- One setting reproduces (C) completely: k = 2, δ = +2, W1, E2.
- The phrase T1 ("TWELVE INCHES ALONG THE THREE RADIANS"): 0 of 34 orders satisfy the three constraints.
- The phrase T4 (Foxon's text, modified by two letters): 1 of 34, after the modification.
- Circle measurement: radii of 102, 205 and 307 pixels, about 25.6 pixels per unit.
- The Route 24 point (a source): 12.18 miles away, with an estimate of 1.015 miles per unit, from a single point rather than a fit.
- The claimed 6.4 miles per unit: places (12,3) 76.8 miles away, and the figure does not support it.

## 5. How the 204 settings are defined

The settings are the product: k ∈ {0 … 16} × δ ∈ {+2, −2} × W ∈ {W1, W2, W3} × E ∈ {E1, E2}, that is 17 × 2 × 3 × 2 = 204.

- **k:** forward shift of the lower row. The text states k = 2; the rest are sensitivity tests.
- **δ:** the column step of the knight move, with the row alternating at each move. The path starts at (1,1).
- **W1:** periodic wrap on 17 columns. **W2:** periodic wrap the length of each row. **W3:** no wrap; overshooting invalidates the setting.
- **E1:** landing on an empty cell invalidates the setting. **E2:** the cell is skipped and the same move is completed.

**Checking that a valid order visits the 32 symbols once:**
1. The path is recorded in full.
2. The order is checked to have length 32 and distinct indices; the result is coded in `is_permutation`.
3. Each move is checked to alternate the row; the result is coded in `moves_alternate_rows`.
4. **Warning:** checks 2 and 3 are internal checks that follow the definition of the move itself. They do not prove that the knight rule is the correct rule in the paper.

## 6. What is stated, what is inferred, and what I chose

**Stated in Foxon (section 4.3 and before):**
- The shift of the lower row by two (k = 2).
- The knight pattern, starting from the top-left corner.
- "characters shifted out of the grid loop back on the opposite side of the same row" (the interpretation W1).
- The angles of the figure: 0 east, 1.571 north, 3.142 west; that is, the pole to the east and anticlockwise positive.

**Inferred from the figure:**
- The direction of the first move, δ = +2, is evident from (C): the second letter X is at (2,3). It is inferred from the output itself, not from the text of the paper.
- The identity categories (from the pixels of figure 1 (A)).

**Chosen to complete the rules:**
- E2 (skipping the empty cell). The paper does not say what happens when a path lands on an empty cell. E2 is one of two options, and it gives a complete order that matches (C).
- E1, W2 and W3 are alternatives tested for sensitivity. None gives a complete order.
- The text of the four phrases tested.
- The family of 204 settings itself.

## 7. Limits of the test

- **Not blind:** I saw figure (C) before designing the family of settings. No rule was changed after running, but the family was not designed independently of (C).
- **Weak repetition constraint:** the test checks only three pairs. It does not determine meaning.
- **Probabilities are approximate:** the English frequency table was written from memory (Σp² ≈ 0.0654). The chance per order is about 2.8 × 10⁻⁴, and the expected count over 34 orders is about 0.0095.
- **Chance does not mean that a solution is correct.** If many phrases are tested, coincidental matches appear and must be corrected for.
- **The map:** the only sourced coordinates are Mount Diablo (Foxon's table) and one point on Route 24 from a commercial website. No reliable source for city centres was found, so Grinell's SF measurement was excluded. The pixel reading of the circles is accurate to about 0.5 %.
- **The value 6.4 miles per unit** is a claim from a secondary source. It was not measured from the original map.

## 7b. Note on the figure images

The images of the two figures are extracted directly from the PDF with `pdfimages`, without modification, and their bytes match their fingerprints in `CHECKSUMS.txt`. The check in `run_all.sh` compares pixels (`compare_pixels.py`), because PNG encoding can differ between tools while the pixels remain the same.

## 8. The PDF

The original paper is included as `input/2023-982.pdf` (1.1 MB). Its fingerprint is in `CHECKSUMS.txt`.

## 9. The `superseded/` folder

It contains earlier results and old copies. The approved results are the files in the main folder. Details are in `superseded/README_SUPERSEDED.md`. The old map-measurement file is withdrawn, because it used coordinates from memory.
