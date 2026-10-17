> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 1348330b5ded7844ad56f181bfba0b9f30e8a963e91dec587085dfbbbd848bb2.

# Pre-registration of the test (before any phase-5 computation)

## Hypothesis under test

H1: point (12, 3) on the original Phillips 66 map lies at the candidate coordinates 37.929792, -122.150318.

H0: no single reasonable, pre-registered reference convention places the point there at an independently determined scale.

## Fixed inputs (do not change after the run)

- Origin point: Mount Diablo, NAD27, 37° 52' 54.387" N, 121° 54' 47.107" W (Foxon 2023, table 2). No free offset for the origin.
- Angular conventions: the four references N, E, S and W, each with the two directions CW and CCW, giving 8 conventions. These are the same 8 points drawn in figure 2 of the paper; their pixel-level match was checked before registration.
- Minute value: round(16.9 / 6) = 3, following the paper's rule (primary procedure). floor = 2 (sensitivity analysis only).
- Distance: r = 12 units × s miles per unit.

## Scale source (pre-specified rule)

- The scale is not measured on the original map. The value 1.162 from the archive is not used as a chosen value; it is used only as a sensitivity value.
- Primary test: Grinell's claim (Foxon 2023, section 2.3) that San Francisco lies "about five inches" from Mount Diablo on the map.
- The bounds of "about five inches" are pre-defined as [4.5, 5.5] inches.
- The San Francisco area is represented by approximate boundary points (corners of the city). These coordinates are approximate, come from general knowledge rather than the archive, and are labelled as such.
- The acceptable scale from the claim: s in [D_min / 5.5, D_max / 4.5], where D_min and D_max are the smallest and largest distances from Mount Diablo to the San Francisco boundary points.

## Separate claim: 6.4 miles per inch

- Its source is Grinell's blog (2020/2021), not an independent measurement. It is tested with the same calculation as a separate case.

## Decision rules (fixed before the run)

- The candidate location is considered "supported" only if (a) one of the 8 conventions with minute value 3 places an endpoint less than 0.5 miles from the candidate location, and (b) the scale used for that endpoint lies within the acceptable San Francisco range.
- It is considered "contradicted" if all procedural endpoints (the 8 with minute value 3) lie in the acceptable scale range but more than 2 miles from the location, and the acceptable scale range excludes 1.162.
- In all other cases: "undecided".
- No scale or convention will be chosen because it lies close to the candidate location.
