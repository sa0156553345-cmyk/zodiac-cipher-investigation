> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 6e3aa970cbdf7879f3baea40163bc642ed58731489f273ec1c859606f703b22d.

# Assumptions register (what is computed, what is inferred, and what is assumed)

| ID | Assumption or input | Type | Evidence | Effect on location (miles) | Status |
|---|---|---|---|---|---|
| A1 | Centre of the figure = weighted centre of the rings (490.88, 454.30) | computed | section 2.2 | under 1 pixel, about 0.05 miles | supported by measurement |
| A2 | Figure scale 25.66 pixels per unit | computed | section 2.3 | error about ±0.5 % (±0.13 pixels) | supported by measurement |
| A3 | Angle reference: east, anticlockwise (R0) | documented in the paper and in the figure | sections 3.1 and 2.4 | the main reference | supported by the text |
| A4 | Angle unit: radians | documented (the word "Radians", the figure's labels) | section 2.4 | degrees change the location considerably (shown separately) | supported by the text |
| A5 | Angle value = 3 (from the minute) | **inferred** from the deviation calculation, not stated in the text | section 3.2 | the whole location depends on it | not supported by the text |
| A6 | Minute rounding = round | **inferred** from the symbol ⌊·⌉ | section 3.2 | 13.4 miles versus floor | supported by the symbol, not justified by the text |
| A7 | Declination 16.9 (alternatives 15, 16.3, 17.7) | documented in the paper | section 1 (D2) | 0.5 miles within the range; affects R2 to R4 only | reference value |
| A8 | Angle reference = the east axis of the map (R0) | **convention** from the paper, not an explicit input for reading Zodiac's message | section 3.2 | R2 moves 18.8 miles; R1 moves 4.0 | undecided |
| A9 | Pole = the crosshair centre as it is on the map (PC) | assumption | section 4.1 | 2.7 miles with PS | undecided |
| A10 | Geographic link via label positions (a proxy) | **conditional assumption** | sections 4.2 and 5.2 | residuals 2 to 6 miles; sensitivity 0.5 to 2.9 miles | conditional |
| A11 | City coordinates (Wikipedia) | secondary external, not re-verified | section 1 (E1) | enter the link | verification recommended |
| A12 | Unit = printed inch (1.09 to 1.34 miles per inch) | **undocumented assumption** | section 6 (I3) | defines the scale itself; 3 miles per 0.25 | undecided |
| A13 | Scale 6.4 miles per unit (secondary claim) | secondary external | section 6.3 | 62.8 miles, and outside the frame for the number 12 | excluded by the conditional criterion above |
| A14 | The displayed map contains the event's position (frame condition) | **assumption** | section 6.1 | excludes 1295 configurations | conditional |
| A15 | The main rotation of the figure is close to true north | **inference** from the link residuals and the exploratory test | section 5.3 | 81 pixels RMS versus 144 for +16.9° | conditional on the labels |
| A16 | Reference date NAD27 versus USSD | documented | section 4.1 | 0.03 miles | practically no effect |
| A17 | Route 24 point | coordinate from geocoding a route name | section 1 (E3) | **not used for selection** | outside the analysis |
