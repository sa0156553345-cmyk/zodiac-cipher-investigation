> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 27794674084038088a070ed5c03f6a1fa8f223e6ea6459d5b4c81cb8797fa71f.

# Audit of the first ten disagreements in mismatch_positions_v4.csv (blinded review with visual evidence)

## Review method

- Panel: figures/blind_review2_first10.png. For each cell: the image of the original symbol from the Z340 grid, then five candidates from the key table (the best five by v4 matching score).
- Blinding: the positions of the candidates and their labels (1 to 5) were shuffled at random, and the panel carries no letter name or key identifier.
- Verdicts were recorded (artifacts/verdicts_first10.json) before the blind map was opened (artifacts/blind2_hidden_map.json).
- Neither the automatic matcher nor the reference text was used to select the visual candidate.
- Caveat on independence: I had seen the reference letters for some cells in earlier outputs, so the independence is partial. The verdicts need confirmation from a second reviewer.

## The table

| # | k | cell | v4 margin | automatic match (letter) | visual verdict (confidence) | reference | visual letter | matches reference? |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | r1c1 | 0.052 | O04 (O) | I01 (high) | I | I | yes |
| 2 | 7 | r8c15 | 0.046 | T04 (T) | U03 (high) | U | U | yes |
| 3 | 10 | r2c4 | 0.022 | T03 (T) | E03 (medium-high) | E | E | yes |
| 4 | 12 | r4c8 | 0.008 | U02 (U) | not settled | A | - | - |
| 5 | 14 | r6c12 | 0.033 | T03 (T) | not settled | I | - | - |
| 6 | 17 | r9c1 | 0.046 | Y01 (Y) | L01 (medium-high) | L | L | yes |
| 7 | 23 | r6c13 | 0.015 | V01 (V) | F01 (high) | F | F | yes |
| 8 | 25 | r8c17 | 0.026 | L02 (L) | N05 (medium-high) | N | N | yes |
| 9 | 26 | r9c2 | 0.094 | E01 (E) | not settled | I | - | - |
| 10 | 28 | r2c6 | 0.125 | V01 (V) | T03 (low; tied with E01) | T | (T, low) | not applied |

## Evidence for the verdicts applied (symbol shape only)

- k = 0: the image shows a thin H stroke. The only candidate resembling H is I01 (a wide H). The automatic match O04 does not resemble H.
- k = 7: a square with a dot in the centre. U03 is the only square with a central dot. T04 is a square with a white triangle (no dot).
- k = 10: a B shape with a straight left wall; E03 matches. The other candidate (E06) has a notch on the left side and was excluded.
- k = 17: a hollow D shape with a straight left wall; L01 matches. Y01 is a filled half-circle and does not match.
- k = 23: a clear F; F01 matches. V01 is a filled circle and does not match.
- k = 25: a hollow triangle with no dot; N05 matches. L02 is a triangle with an internal dot and was excluded.

## Unsettled cases

- k = 12: the image is a square with a dark diagonal triangle, and no candidate of this kind is among the best five. The formal possibilities are A03 or T04, but they cannot be distinguished at this resolution.
- k = 14: an unclear, tangled blob. No candidate matches it convincingly.
- k = 26: the image is a clear "<" sign, and no "<" is among the best five. The automatic match E01 (a filled rectangular letter) contradicts the shape completely, despite a margin of 0.094.
- k = 28: a blurred filled square. It matches T03 or E01, and the choice is low-confidence, so it was not applied.

## Conclusions

1. The margin is not a sufficient indicator of correctness: k = 26 with margin 0.094 and k = 28 with margin 0.125 are both visually wrong.
2. The top-five set is not sufficient: some correct symbols (such as "<" and "square with triangle") do not appear among the candidates.
3. The six visual corrections applied represent a documented visual improvement, and move the ratio from 0.609 to 0.626. No other symbol was changed.

## Agreement after the corrections

- Before: 207/340 = 0.609.
- After six documented visual corrections: 213/340 = 0.626.
- Remaining: 127 disagreements, of which 4 in the first ten are unsettled (k = 12, 14, 26, 28).

## What was not done

- The 116 low-margin cells were not reviewed (pending your approval of the method).
- No full matching against the 63 candidates for each cell was carried out.
- The full Z340 solution was not rebuilt, and H4a or any Z32 analysis was not run.
