> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 3979ee207397d082e7a4a0f55638ffa57f475f8de24491e524d383d3f52bb8c4.

# Phase 5: search for the original Phillips 66 map, scale test, and candidate coordinates

## Summary

- **The original map was not found, nor a high-resolution image of its margin.** Only secondary claims and copied images were found.
- **The edition (1968 or 1969) is undetermined.** No documented differences exist between the two copies. The claims exist, but without an image of the printing.
- **The scale was not measured on the map.** The pre-registered test gives a range of [4.83, 7.49] miles per inch, from Grinell's claim. The archive's scale of 1.162 falls outside this range, and the claimed scale of 6.4 falls inside it.
- **The candidate coordinates 37.929792, −122.150318 are not supported.** They come only from a scale of 1.162 and from a free-pole model. With any of the eight conventions at minute 3 and the accepted scale range, the nearest point is at least 44.8 miles away. This is a conflict that is conditional on the correctness of the claim "five inches".

## 1. Sources checked and their classification

| Source | What was actually checked | Classification | Link |
|---|---|---|---|
| Foxon 2023, the uploaded file | the paper text, table 2 (coordinates of Diablo and SF, and declination 16.9°), section 2.3 (Grinell's claim), the figure 2 caption | primary for the paper; secondary for the map | https://eprint.iacr.org/2023/982 |
| Figure 2 in the paper (a redrawn map) | the image: radian labels, rings 4/8/12, the handwritten sentence "0 is to be set to Mag. N.", and eight marks for (12,3) | a redrawing, not the original map | uploaded file |
| Grinell, zodiacciphers blog (2018/2020) | the claims "five inches" and "6.4 miles per inch" (from an archive extract, 02-2021) | secondary; the source of the claim itself; not verified | https://www.zodiacciphers.com/zodiac-news/archives/02-2021 |
| Brooks page on zodiacciphers (2013) | the claim of a "1969 version" | a claim by a theorist; motives are clear | https://www.zodiacciphers.com/zodiac-news/the-phillips-petroleum-map-key |
| X post (Maddie Reese, 2026) | the claim that the map carries "1969 Edition" | social-media claim; no image of the margin | https://x.com/maddiedreese/status/2083604506592575600 |
| Forum thread t3190 (2009–2010) | a physical-copy owner says "1969" and dimensions of 8 × 6¾ and 18¾ × 34 inches | testimony of a copy holder; not verified | https://www.tapatalk.com/groups/zodiackillerfr/original-phillips-66-map-t3190.html |
| Forum thread t3190-s40 (2022) | a claim of a 1968 copy whose back was scanned | claim of a copy holder; not verified | https://www.tapatalk.com/groups/zodiackillerfr/original-phillips-66-map-t3190-s40.html |
| Peterson III finding aid, Library of Congress | Phillips 66 as publisher of California and San Francisco maps; no dates | institutional (publisher only) | https://tile.loc.gov/storage-services/service/gdc/gdcfindingaidpdfs/gm023002/gm023002.pdf |
| Yale/Beinecke indexes of Shell and Gousha maps (1936–1950) and others | no Phillips 66 record for San Francisco, 1968–1970. These records show the scale-statement format used in cataloguing | institutional; negative | https://collections.library.yale.edu/catalog/15818765 |
| eBay seller listing: Phillips 66 map of St Louis, 1969, H.M. Gousha edition | shows that Phillips 66 maps of 1969 were produced by Gousha, not necessarily of SF | seller listing, for a similar product | https://www.ebay.com/itm/402183969106 |

**Not reached:** the original map; an image of its margin or scale bar; the Gousha record at the Newberry Library for this map; the full page of Grinell's blog (2020), where the claims are presumably detailed; zodiackiller.com, which allegedly has a high-resolution scan.

## 2. What can be said about the figure and the instruction

- Figure 2 shows (12,3) with eight marks. I verified by calculation that these marks are the four references N, E, S and W, each with the two directions CW and CCW. Each mark matches its computed direction.
- The open circle near Orinda represents reference E with CCW, the same convention the archive uses.
- The sentence "0 is to be set to Mag. N." appears in the redrawn figure. I did not verify that it appears in the same form on the original map.

## 3. Scale calculation

**Equations:**
- Scale s = D / d, where D is the great-circle distance from Mount Diablo to a point in San Francisco (R = 3958.8 miles), and d is the number of inches.
- Pre-registered rule: "about five inches" means d in [4.5, 5.5].
- Accepted range: s in [D_min / 5.5, D_max / 4.5].

**Data:**
- D_min = 26.58 miles (approximate eastern boundary of San Francisco on the bay).
- D_max = 33.69 miles (approximate western boundary at Ocean Beach).
- The point in Foxon's table 2: 26.65 miles.
- The San Francisco boundaries are approximate, taken from general knowledge rather than from the archive. The expected error is about ±0.5 miles.

**Result:** the accepted range is [4.83, 7.49] miles per inch.
- Archive scale 1.162: outside the range. At this scale San Francisco is about 23 inches away, not five.
- Claimed scale 6.4: inside the range.

**Internal consistency check of Grinell's claim at 6.4:** 4 inches = 25.6 miles, 5 inches = 32.0 miles, 6 inches = 38.4 miles. Five inches falls within San Francisco's boundaries, four inches falls in the bay, and six inches falls in the ocean. This matches what Grinell says, but it is internal consistency only, not a measurement.

**Sensitivity:** if "about five inches" is read more broadly, as [4, 6], the range becomes [4.43, 8.42] miles per inch. The archive scale of 1.162 remains outside the range in every case.

## 4. The eight conventions (minute 3, the primary procedure)

### Scale from the range (lower bound)

| Convention | True direction | Distance (miles) | Latitude | Longitude | Distance to the candidate location (miles) |
|---|---|---|---|---|---|
| N-CW | 171.89° | 58.0 | 37.050652 | −121.764663 | 64.32 |
| N-CCW | 188.11° | 58.0 | 37.050652 | −122.061507 | 60.94 |
| E-CW | 261.89° | 58.0 | 37.758637 | −122.964246 | 45.96 |
| E-CCW | 278.11° | 58.0 | 37.995534 | −122.967633 | 44.75 |
| S-CW | 351.89° | 58.0 | 38.712705 | −122.064895 | 54.29 |
| S-CCW | 8.11° | 58.0 | 38.712705 | −121.761275 | 58.06 |
| W-CW | 81.89° | 58.0 | 37.995534 | −120.858538 | 70.52 |
| W-CCW | 98.11° | 58.0 | 37.758637 | −120.861924 | 71.28 |

### Scale from the range (midpoint)

| Convention | True direction | Distance (miles) | Latitude | Longitude | Distance to the candidate location (miles) |
|---|---|---|---|---|---|
| N-CW | 171.89° | 73.91 | 36.822578 | −121.724509 | 79.99 |
| N-CCW | 188.11° | 73.91 | 36.822578 | −122.101662 | 76.55 |
| E-CW | 261.89° | 73.91 | 37.723221 | −123.252039 | 61.8 |
| E-CCW | 278.11° | 73.91 | 38.025099 | −123.257538 | 60.66 |
| S-CW | 351.89° | 73.91 | 38.940661 | −122.107165 | 69.88 |
| S-CCW | 8.11° | 73.91 | 38.940661 | −121.719006 | 73.64 |
| W-CW | 81.89° | 73.91 | 38.025099 | −120.568633 | 86.39 |
| W-CCW | 98.11° | 73.91 | 37.723221 | −120.574132 | 87.2 |

### Scale from the range (upper bound)

| Convention | True direction | Distance (miles) | Latitude | Longitude | Distance to the candidate location (miles) |
|---|---|---|---|---|---|
| N-CW | 171.89° | 89.83 | 36.59449 | −121.684593 | 95.75 |
| N-CCW | 188.11° | 89.83 | 36.59449 | −122.141578 | 92.26 |
| E-CW | 261.89° | 89.83 | 37.687106 | −123.539553 | 77.67 |
| E-CCW | 278.11° | 89.83 | 38.053952 | −123.547674 | 76.57 |
| S-CW | 351.89° | 89.83 | 39.168601 | −122.149707 | 85.59 |
| S-CCW | 8.11° | 89.83 | 39.168601 | −121.676463 | 89.34 |
| W-CW | 81.89° | 89.83 | 38.053952 | −120.278496 | 102.28 |
| W-CCW | 98.11° | 89.83 | 37.687106 | −120.286617 | 103.11 |

### Archive scale 1.162 (sensitivity only; not accepted by prior decision)

| Convention | True direction | Distance (miles) | Latitude | Longitude | Distance to the candidate location (miles) |
|---|---|---|---|---|---|
| N-CW | 171.89° | 13.94 | 37.681977 | −121.8771 | 22.71 |
| N-CCW | 188.11° | 13.94 | 37.681977 | −121.949071 | 20.34 |
| E-CW | 261.89° | 13.94 | 37.853024 | −122.166119 | 5.37 |
| E-CCW | 278.11° | 13.94 | 37.909983 | −122.166315 | 1.62 |
| S-CW | 351.89° | 13.94 | 38.081561 | −121.949267 | 15.16 |
| S-CCW | 8.11° | 13.94 | 38.081561 | −121.876904 | 18.21 |
| W-CW | 81.89° | 13.94 | 37.909983 | −121.659856 | 26.77 |
| W-CCW | 98.11° | 13.94 | 37.853024 | −121.660051 | 27.25 |

### Claim 6.4 (sensitivity only)

| Convention | True direction | Distance (miles) | Latitude | Longitude | Distance to the candidate location (miles) |
|---|---|---|---|---|---|
| N-CW | 171.89° | 76.8 | 36.781207 | −121.717251 | 82.85 |
| N-CCW | 188.11° | 76.8 | 36.781207 | −122.10892 | 79.39 |
| E-CW | 261.89° | 76.8 | 37.716722 | −123.304211 | 64.67 |
| E-CCW | 278.11° | 76.8 | 38.030386 | −123.310148 | 63.55 |
| S-CW | 351.89° | 76.8 | 38.982007 | −122.114861 | 72.73 |
| S-CCW | 8.11° | 76.8 | 38.982007 | −121.711309 | 76.48 |
| W-CW | 81.89° | 76.8 | 38.030386 | −120.516023 | 89.28 |
| W-CCW | 98.11° | 76.8 | 37.716722 | −120.521959 | 90.08 |

**Sensitivity to minute 2 (floor), at the archive scale:** the nearest result is S-CW, at 2.48 miles from the candidate location. This does not support the location, because minute 2 is not the registered rule, and the convention was selected after looking at the result. It is recorded as an example of the risk of choosing the setting that produces the desired closeness.

## 5. Verdict

- **The candidate coordinates are not supported.** They come from a scale of 1.162, which conflicts with the claim of "five inches", and from a free-pole model that displaced Diablo by about 2.7 miles. The fixed-pole model places them 1.9 miles from its point.
- **The edition is undetermined.** There is no image of the printing and no documented differences.
- **The scale is not measured.** The claim of 6.4 is internally consistent with Grinell's claim, but it comes from a secondary source.
- **What prevents a decision:** we have not seen the original map or its scale bar.

## 6. The next most valuable test

1. **A high-resolution image of the entire map,** including edges, margin, scale bar and printing number. If possible, an image of a physical copy with a ruler beside it. If it is uploaded to the conversation, distances can be measured in pixels, the scale computed from the scale bar or from San Francisco's location, and the pre-registered test repeated.
2. **A cataloguing record** from the Newberry Library (H.M. Gousha collection) or the Library of Congress map division. If the publisher was Gousha, as the 1969 St Louis listing suggests, the record may contain the date and the scale.
3. **Verifying Grinell's claim** by reading his full page, to find the exact point from which "five inches" was measured.

## 7. Files of this phase

- `PREREGISTRATION_phase5.md`: the test rules, registered before computation.
- `phase5_endpoints.csv`: all computed points (80 rows).
- `phase5_summary.json`: the range and the bounds.
- `run_phase5.py`: the full computation script.
