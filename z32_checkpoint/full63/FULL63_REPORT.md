> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 5fca0ab5acd34c58b58102972b63560f957de3158e869ca682079d4818c23cf5.

# Full matching of every Z340 cell against the 63 key glyphs (no pruning before scoring)

## Verification status

- Positions matched: 340 of 340 (every position was compared with all 63 glyphs).
- Reproduction: **not yet successful**. Position-wise agreement: 207/340 (0.609) with the first choices, and 213/340 (0.626) after the six registered visual corrections only.
- Remaining disagreements: 127 positions, detailed in full63_residuals.csv. Only the ten diagnostic cases have been reviewed visually.

## How the scores were computed

1. **Mask:** a 72 × 72 window around the cell position estimated from the grid; local Otsu threshold; then the connected component closest to the centre with an area of at least 40 pixels.
2. **Size normalisation:** the symbol is cropped to its ink rectangle and enlarged or reduced so that its longer side is 44 pixels, keeping the aspect ratio; it is then placed on a 52 × 52 panel.
3. **Stroke-width normalisation:** the symbol is skeletonised and then dilated with a disk of radius 2 pixels. This removes differences in stroke width, but **loses information about filling**: a filled shape and a hollow shape become similar. This is a hypothesis that needs testing, not a confirmed judgement.
4. **Orientation:** **there is no orientation normalisation.** The only tolerance is a shift of up to ±2 pixels.
5. **Score:** Dice coefficient = 2|A ∩ B| / (|A| + |B|) on the masks after dilating them by half a pixel, taking the maximum over all integer shifts from −2 to +2 in both directions.
6. **Choice:** the best glyph is the highest score among the 63; the margin is the difference between the first and second scores.

## Testing the ten cases against the registered visual corrections

| k | cell | visual verdict | its rank among 63 | its score | automatic first choice | its score |
|---|---|---|---|---|---|---|
| 0 | r1c1 | I01 | 3 | 0.556 | O04 | 0.726 |
| 7 | r8c15 | U03 | 4 | 0.673 | T04 | 0.771 |
| 10 | r2c4 | E03 | 4 | 0.675 | T03 | 0.755 |
| 12 | r4c8 | not settled | - | - | U02 | 0.745 |
| 14 | r6c12 | not settled | - | - | T03 | 0.627 |
| 17 | r9c1 | L01 | 2 | 0.803 | Y01 | 0.849 |
| 23 | r6c13 | F01 | 3 | 0.535 | V01 | 0.557 |
| 25 | r8c17 | N05 | 2 | 0.677 | L02 | 0.703 |
| 26 | r9c2 | not settled | - | - | E01 | 0.588 |
| 28 | r2c6 | T03 | 2 | 0.499 | V01 | 0.624 |

Notes: the visual verdict in the six corrected cases was at ranks 2 to 4. The correct glyph was among the top five, but the first automatic choice was wrong. For k = 26, the rank of I04 (which matches the "<" shape) is 15, and it has not yet been judged visually. k = 12 and k = 14 remain unsettled visually.

## Score sensitivity (340 cells)

| Variant | First choice changed in |
|---|---|
| window of 30 pixels instead of 36 | 24 cells (7 %) |
| window of 42 pixels instead of 36 | 18 cells (5 %) |
| rotation of +4 degrees | 58 cells (17 %) |
| rotation of −4 degrees | 70 cells (21 %) |

- Crop boundary: in 5 cells the selected component touches the boundary of the window.
- Neighbour overlap: in 2 cells there is another component of symbol size at 6 pixels or less.
- Conclusion: the automatic choice is far more sensitive to rotation than to the window size or to overlap.

## Remaining disagreements (127)

- Position of the correct letter's best glyph in ranks 2 to 5: 75 positions. In other words, the correct glyph is among the top five in most cases, and the weakness lies in distinguishing the leading candidates.
- Ranks 6 to 10: 27. Above 10: 25.
- Most frequent confusion pairs (chosen letter → reference): R→A (7), T→R (6), D→O (5), Y→E (5), V→T (4), T→S (4).
- Glyphs that were never chosen as a first choice at any position: B02, P02, R04, S02. The paper says all 63 glyphs are used, so this indicates matching errors.

## Not yet done

- Visual verification of the remaining 127 positions.
- Compensating for rotation: the automatic choice is sensitive to it, and this has not yet been addressed.
- Any improvement to the method must be registered in advance and tested on a new visual sample that was not used for diagnosis. No improvement has been carried out yet.
- The solution is not considered complete before an acceptable reproduction of all positions.
