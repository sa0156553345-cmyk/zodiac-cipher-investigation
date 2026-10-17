> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is ea8113e2b4530f8c7f3e5b273e189747316ec7a8ed00c68c909f4bbd131451eb.

# Data validation log (step 1)

| Check | Expected | Observed | Status |
|---|---|---|---|
| grid cells (20x17) | 340 | 340 | verified (count) |
| grid cells with ink < 30 (possibly empty) | 0 | 6 | partially verified: 6 low-ink cells, matched with fallback threshold; visually spot-checked only |
| key glyphs (Figure 44) | 63 | 63 | verified (count) + atlas checked visually |
| key glyph counts per letter = visual count | exact | exact | verified visually; not against an external key table |
| transposition values form permutation of 0..339 | 340 | 340 | verified |
| section 1 (rows 1-9) agrees with (1,2)-decimation | 153 | 153 | verified (independent formula) |
| section 2 (rows 10-18) agrees with pure decimation | 153 | 91 | differs at 62 cells: consistent with the paper stating corrections in Figure 43; corrections NOT independently verifiable |
| OCR errors fixed in transposition figure (visual) | documented | 14 | documented per cell; each verified on enlarged crops |
| reference plaintext length = symbol count | 340 | 340 | consistency only (text from the paper, misspellings kept) |
| reading direction (k -> cell with number k) | k=1 H, k=2 O | k=1 H01 ok, k=2 O04 ok, k=0 I01 expected but matcher O04 | partially verified: visual anchors agree for k=1,2; k=0 fails by matcher |
