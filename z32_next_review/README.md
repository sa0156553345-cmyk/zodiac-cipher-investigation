> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 9256865e453abf51d39481357113aa97a6f0c06644994e988554d7ff38226ff4.

# z32_next_review: the next review stage of the Z32 investigation

## 0. Summary before reading

- **The arrangement of figure (C) is reproduced from the paper**, but with a setting that contains a rule not stated in the paper (skipping the empty cell E2), and a direction first inferred from the figure itself. Therefore this is a conditional reproduction, not an independent discovery.
- **The proposed statement T1, "TWELVE INCHES ALONG THE THREE RADIANS", does not appear literally** under the constraints of repeated symbols in any of the 34 valid orders. On the paper's order it satisfies one constraint out of three.
- **The test of the pre-registered alternatives** (3544 phrases × 34 orders) shows no excess over chance at family level (p = 0.417).
- **The map scale from the figure itself** is about 1.0–1.2 miles per unit, and does not support 6.4 miles per unit. The location (12,3) is not determined precisely enough: the models differ by about 2.8 miles.
- **No current evidence determines the solution of Z32.** This result is documented well enough to be re-tested.

## 1. Contents

| File or folder | Function |
|---|---|
| `input/2023-982.pdf` | The original Foxon paper (1.1 MB) |
| `images/fig1_all_panels_p8_native.png` | Figure 1 (A–D), extracted from page 8 without modification |
| `images/fig2_map_p9_native.png` | Figure 2 (the map), extracted from page 9 without modification |
| `images/fig2_grid_overlay_for_reading.png` | The same map with a pixel grid for reading the positions of the names |
| `data/z32_fig1A_transcription.csv` | The visual transcription of row (A), used only to label the identity categories |
| `data/landmarks.csv` | The five landmarks with their source coordinates, and the positions of their names on the image |
| `scripts/` | All scripts (see section 4) |
| `results/` | All CSV and JSON results |
| `docs/PREREGISTRATION.md` | Pre-registration: families, lists, test, decision rules and disclosures |
| `docs/SOLUTION_CRITERIA.md` | Criteria for any proposed solution (C1–C11), with the status of the current candidate |
| `docs/CLASSIFICATION.md` | Classification of each result: directly supported / inferred from assumptions / undetermined |
| `previous_results/` | Results of the previous package, with a note that they are not results of this review |
| `run_all.sh`, `requirements.txt`, `CHECKSUMS.txt`, `run_log.txt` | Running, dependencies, fingerprints, and the actual log |

## 2. Requirements

- Python 3.9 or later, with `numpy` and `Pillow` (`pip install -r requirements.txt`).
- `pdfimages` (from poppler-utils) for the extraction step from the PDF. It is optional.
- No internet access is needed.

## 3. Step-by-step run

1. Unzip: `unzip z32_next_review.zip`, then `cd z32_next_review`.
2. Dependencies: `pip install -r requirements.txt`.
3. Full run: `bash run_all.sh | tee my_run_log.txt`.
   The script runs in order: the extraction check (if `pdfimages` is available), then `fig_glyph_check.py`, then `transposition_family.py`, then `literal_phrase_test.py`, then `alternatives_family.py`, then `map_audit.py`, then the fingerprint verification.
4. Compare your outputs with `run_log.txt`. Only the timestamp and the temporary folder path differ.

Note: the order of running matters. `transposition_family.py` needs `fig_glyph_check.csv`, and `literal_phrase_test.py` and `alternatives_family.py` need `valid_orders.json`.

## 4. Scripts

- `common.py`: paths, reading the transcription, the repeated-pairs function `repeat_pairs`, and the function `satisfied`.
- `fig_glyph_check.py`: pixel comparison of the symbols. It determines the identity categories in (A), checks (B), and reads (C).
- `transposition_family.py`: the family of 204 settings. It checks that every valid order visits the 32 symbols once, and records the effect of each assumption.
- `literal_phrase_test.py`: literal testing of phrases, without modification, on all valid orders.
- `alternatives_family.py`: the family of pre-registered alternatives (3544 phrases), with a within-phrase permutation test (2000 permutations) and multiplicity correction.
- `map_audit.py`: measurements on the image (the crosshair centre and the rings), a similarity transformation for five cities, an uncertainty simulation, and four models.
- `make_grid_overlay.py`: creates the coordinate grid for manual reading.
- `compare_pixels.py`: pixel comparison of images (not byte comparison).

## 5. Test types and their results

### 5.1 Transposition: what the paper supports, and what I added

- **Stated in the paper:** the shift by 2 (k = 2), the knight pattern, the start (1,1), and the wrap-around "loop back on the same row" (interpreted as W1).
- **Inferred from the figure (C):** the first move (2,3), which means δ = +2.
- **Added to complete the path:** E2 (skipping the empty cell). **The paper does not mention what happens when the path lands on an empty cell.**

**Effect of each assumption (from `results/transposition_assumption_effects.csv`):**

| Setting | Result |
|---|---|
| E1 (fails at the empty cell) | no complete order, for any δ |
| E2 + δ = +2 | complete order, matching (C) 32/32 |
| E2 + δ = −2 | complete order, but matching (C) only 2/32 |
| W2 or W3 | no complete order |

Result: the reproduction of (C) depends on rule E2 and the direction δ = +2, and neither is stated in the paper. The reproduction is therefore not an independent discovery.

### 5.2 The proposed phrase, literally (`results/literal_phrase_test.csv`)

| Phrase | Orders satisfying the three constraints (out of 34) | Note |
|---|---|---|
| T1 "TWELVEINCHESALONGTHETHREERADIANS" | 0 | on the paper's order: 1 out of 3 pairs |
| T2 "THREERADIANSANDTWELVEINCHESALONG" | 0 | |
| T3 "THREEANDTHREEEIGHTHSRADIANSSIXIN" | 0 | a phrase proposed by others, not modified |
| T4 the Foxon text | 1 | after changing two letters (positions 6 and 31), which are the two positions that disagree with T1 |

Result: T1 does not appear without modification. T4 satisfies the constraints only after two letters are changed, so it is not considered a literal match.

### 5.3 Controlled alternatives (`results/alternatives_summary.csv`)

- **The family (pre-registered):** 3 templates (A, B, C), 17 number words, and 8 unit words. Result: N = 3544 phrases of 32 letters.
- **The test:** each phrase × each valid order (M = 34). The number of orders satisfying the three constraints is counted.
- **The null model:** randomly permuting the letters of each phrase (2000 times). It preserves letter frequencies and breaks the word order.
- **Result:** O = 47 successes, against an expected 45.27 by chance (standard deviation 6.81). **p (family level) = 0.417**, i.e. no excess.
- **Highest phrase:** succeeds in one order only. Its adjusted p-value (Bonferroni) = 1.0.
- **Interpretation:** 47 phrases out of 3544 succeed in one order, which is expected by chance. Success here does not mean meaning.

### 5.4 The map (`results/map_audit_models.csv`)

**Landmarks used:** Mount Diablo (from Foxon's table, NAD27), and 5 cities (Oakland, San Leandro, Hayward, Livermore, Vallejo) with Wikipedia coordinates, documented in `data/landmarks.csv`. The positions of their names on the image were read by hand (±6 pixels) with the help of the grid.

**Measurements on the image:** crosshair centre (490, 454), and ring radii of 102, 205 and 307 pixels for units 4, 8 and 12, that is 25.59 pixels per unit.

**The four models (pre-registered):**

| Model | Pixels per mile | Miles per unit (estimate) | Miles per unit (MC 95%) | Rotation (degrees) | Distance of the location (12,3) from the Route 24 point |
|---|---|---|---|---|---|
| A: 5 cities, free offset | 22.0 | 1.16 | 1.10–1.24 | −4.8 | 2.8 miles |
| B: 4 cities (without Oakland), free offset | 23.5 | 1.09 | 1.03–1.16 | −4.9 | 2.2 miles |
| C: 5 cities, crosshair at Diablo | 23.5 | 1.09 | 1.04–1.15 | −1.8 | 1.2 miles |
| D: 4 cities, crosshair at Diablo | 25.1 | 1.02 | 0.97–1.08 | −4.2 | 0.25 miles |

**Conclusions:**

- The scale extracted from the image is about 1.0–1.2 miles per unit. This is inconsistent with 6.4 miles per unit, which would need 4.0 pixels per mile, while the models give 22–25.
- The map is close to true north (declination −2° to −5°), and is not oriented to magnetic north.
- The predicted location (12,3) is 0.25–2.8 miles from the Route 24 point, depending on the model. The 95% radius within each model is 0.8–1.4 miles.
- **The difference between the models is larger than the uncertainty within a single model.** The residuals reach 130 pixels (about 5 miles) in the models that allow a free offset. The MC interval therefore understates the real error.

## 6. What do the results mean?

- **What is supported by the data:** the identity categories in the figure, the pixel reading of (C), the results of the literal test, the result of the alternatives test (no excess), and the measurements on the image.
- **What is inferred from assumptions:** the reproduction of (C), which requires E2 and δ = +2; the map scale; the angle; and the rejection of 6.4 miles.
- **What is undetermined:** the location (12,3) precisely; the meaning of any phrase; the encryption key; the meaning of "#"; and Grinell's SF measurement, since no documented SF coordinates are in this package.

Full details are in `docs/CLASSIFICATION.md`, and the solution criteria are in `docs/SOLUTION_CRITERIA.md`.

## 7. What is needed to establish a solution (summary)

Any proposed solution must succeed on every criterion in `docs/SOLUTION_CRITERIA.md` that applies to it, most importantly:

1. Reproduction under stated rules, or under rules declared in advance with the effect of each one.
2. The phrase appearing literally, without modification, under those rules.
3. Consistency with the three repeated pairs.
4. Exceeding chance after correcting for multiple testing.
5. A single location identified with uncertainty below 0.5 miles, and a map scale measured with small uncertainty.
6. Support from an independent external source (an archival document or a field survey).

## 8. Limitations

- The symbols are ASCII characters printed in the paper, not the original Zodiac symbols. The identity of the original symbols is not known.
- Rule E2 is not stated in the paper. Other rules for skipping the empty cell were not tried, because the paper does not describe them.
- The test is not blind: figure (C) was seen before the family was designed. The pre-registration documents this.
- The coordinates come from Wikipedia (city centres) and from Foxon's table (Mount Diablo). The Route 24 coordinate comes from a commercial website, and it was not verified against an official source.
- Vallejo: two sources differ by about one mile. The Wikipedia source was used, and the difference enters the uncertainty.
- The positions of the names on the image were read by hand, and their error may reach ±6 pixels, about 0.3 miles.
- The English frequency table was written from memory, so the chance probability (Σp² ≈ 0.065) is approximate.
- No percentage is given for the probability that any solution is correct, because the data do not support a model for that.

## 9. Previous results

The folder `previous_results/` contains the results of the previous package (z32_repro). The numbers related to transposition and phrases agree. The file `map_check.csv` relied on a single point and is considered superseded by the results of `map_audit`.
