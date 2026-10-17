> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 2a061ae11ffa226375d41545ab41e316ab51a795c0e81054392ead59450129fc.

# Stage 2: search for the original source of the Phillips 66 map

## 0. Summary

- **The edition of the map sent by the Zodiac has not yet been identified**, nor its date, nor its documented scale.
- I found **institutional records** showing that Phillips 66 published maps of California, San Francisco and its peninsula, Marin and Oakland, but the catalogue entries carry no dates. This identifies **where** to search, not **which** map it is.
- **The search of the FBI files is incomplete:** I could not open parts 2 to 6, and I did not examine the image pages of part 1. I do not describe the search of the files as comprehensive.
- **The code 9-QQ-1219-S and the dimensions 18.75 × 34 inches:** I found no independent confirmation for them, and I could not access the original images on which the secondary sources relied.
- **No geographic calibration and no coordinates** at this stage, as requested.

Detailed tables: `phase2_sources.csv` (16 items with the status of each) and `phase2_claims_table.csv` (classification of the claims).

## 1. What was actually examined

| Source | What was done | Result | Link |
|---|---|---|---|
| FBI Vault, part 1 (zodiac1.pdf) | Read part of the OCR-extracted text (about the first 6000 tokens) | The document header gives the file number **9-HQ-49911**. No description of the map appeared in the readable part | https://vault.fbi.gov/The%20Zodiac%20Killer/The%20Zodiac%20Killer%20Part%2001/view |
| Peterson III collection finding aid, Library of Congress (PDF) | Read the text of the box lists for series I to VI | States that Phillips 66 is a publisher for several boxes linked to California (see section 2). No dates in the finding aid | https://tile.loc.gov/storage-services/service/gdc/gdcfindingaidpdfs/gm023002/gm023002.pdf |
| H.M. Gousha collection, Newberry Library | Read the record | About 25,000 road maps. The oldest (1927 to 1949) are catalogued item by item; the most recent are not catalogued item by item online | https://archives.newberry.org/repositories/2/archival_objects/304257 |
| The Henry Ford library: Phillips 66 map of Illinois (1934) | Read the record excerpt from the search results | The map was "printed and copyrighted by the H.M. Gousha Company and distributed by Phillips 66" (1934). Evidence of a printing relationship, but for 1934 only | https://www.thehenryford.org/collections/explore/artifact/368818 |
| Osher library: Phillips 66 interstate highway guide (1968) | Read the record excerpt | An interstate road guide, LC number G1201.P2 P45 1968. Not a bay map; I did not open its contents | https://oshermaps.org/map/47196.0001 |
| Timetable World: list of oil-company maps | Read the whole California section | No Phillips 66 entry for California in any year. There is a "Road Map San Francisco Bay & River Area 1970" with no publisher named | https://timetableworld.com/oil-company-maps/ |
| RMCA: cover dates (Tom Sveum, 2020) | Read the text excerpt from the search results | Phillips 66 printed a year on the covers of its maps only in 1933 and 1935–36. So the absence of a year on a 1960s map cover means nothing, and any date needs other evidence | https://roadmaps.org/assets/Map-Cover-Dates-8-2020-with-GLS-edits.pdf |
| Zodiac forum, thread t3190, first page | Read the first page | Claims of a 1969 edition, a section of 8 × 6.75 inches, the code 9-QQ-1219-S, and a map of 18.75 × 34 inches. No institutional confirmation | https://www.tapatalk.com/groups/zodiackillerfr/original-phillips-66-map-t3190.html |

## 2. Institutional Phillips 66 records linked to California (Library of Congress finding aid)

The finding aid gives the **publisher** of each box, but not the **date** or the **scale**:
- **Series I, box 12 (California):** Phillips 66 among the publishers.
- **Series I, box 113 (San Francisco–Santa Monica):** "San Francisco (CA): ... Phillips 66 ..." (a map of the city of San Francisco).
- **Series I, box 94 (Oakland–Ottawa):** Phillips 66 among the publishers of Oakland.
- **Series 2 (county maps), box 1:** Marin County (CA): Phillips 66 among the publishers.
- **Series 3 (special regions), box 3:** "San Francisco Peninsula": Phillips 66 among the publishers.
- **Series 3, box 2:** "Pacific Coast States (U.S.)": Phillips 66.

The finding aid says that the collection's strength in published maps is between 1948 and 1973, and that it is stored off-site and requires advance notice. **These are the most important targets for a request**, but I cannot say that any of them is the Zodiac map without seeing the individual record or the image.

## 3. Classification of the claims

| Claim | Classification | Link |
|---|---|---|
| Phillips 66 published maps of San Francisco and its peninsula (publisher only) | institutional cataloguing record, no date | https://tile.loc.gov/storage-services/service/gdc/gdcfindingaidpdfs/gm023002/gm023002.pdf |
| Gousha printing of Phillips 66 maps | institutional cataloguing record, for 1934 only | https://www.thehenryford.org/collections/explore/artifact/368818 |
| FBI file number 9-HQ-49911 | primary source read partly (document header) | https://vault.fbi.gov/The%20Zodiac%20Killer/The%20Zodiac%20Killer%20Part%2001/view |
| Phillips 66 put dates on its covers only in 1933 and 1935–36 | specialist secondary source | https://roadmaps.org/assets/Map-Cover-Dates-8-2020-with-GLS-edits.pdf |
| Clock layout: 0 at the top, 3 to the right, 6 at the bottom, 9 to the left | secondary source | https://www.boxentriq.com/code-breaking/zodiac-ciphers |
| Declination of 16.5 to 17 degrees east in 1970 | secondary source, not checked against a NOAA model | https://zodiackillerfacts.com/The%20Mysteries%20of%20the%20Mt.%20Diablo%20Map.htm |
| Scale "San Francisco and Vicinity" = 1 inch ≈ 6.4 miles | **claim that could not be verified** (no source) | https://ciphermysteries.com/zodiac-killer-z32 |
| The 1969 edition ("68 and '70 different") | **claim that could not be verified** (a forum user; images unavailable) | https://www.tapatalk.com/groups/zodiackillerfr/original-phillips-66-map-t3190.html |
| The code 9-QQ-1219-S | **claim that could not be verified** (no independent search result; images unavailable) | same link as above |
| The map 18.75 × 34 inches, and the Zodiac section 8 × 6.75 inches | **claim that could not be verified** (images unavailable) | same link as above |

## 4. What was not examined (in detail; the search is not considered comprehensive)

1. **FBI Vault, parts 2 to 6:** I could not access them. The fetch tool rejects any link that did not appear in earlier search or fetch results, and none of the links to these parts appeared. (The link I tried: https://vault.fbi.gov/The%20Zodiac%20Killer/The%20Zodiac%20Killer%20Part%2002%20of%2006%20./view)
2. **Image pages in part 1:** the extracted text does not describe the image content, and I could not open the images.
3. **The full cataloguing record of the Peterson III collection:** https://lccn.loc.gov/2019360293 is blocked for automated access (ROBOTS_DISALLOWED). I used only the box list from the finding aid.
4. **The detailed Phillips 66 section in RMCA:** available to members only (https://roadmaps.org/?p=3702). I did not examine it.
5. **Forum pages 2 to 4:** access refused (the links did not appear in search results). I did not read replies 11 to 39, which may contain confirmations or objections.
6. **Images hosted on Photobucket** (the files Phillips66MapSFsection.jpg and Phillips66SFinsertcode.jpg): access refused.
7. **High-resolution zodiackiller.com page (PMHR):** access refused, and it did not appear in the search results.
8. **Other libraries:** I searched with general terms only. I did not systematically search the UC, Stanford, Harvard and David Rumsey collections for Phillips 66 maps of California from 1968 to 1970.
9. **The actual wording of the instruction:** I did not examine an image of the actual text "is to be set to Mag. N." on the map.

## 5. Where to request the original source (in order of priority)

1. **Library of Congress, Geography and Map Division:** the contact link given in the finding aid: https://hdl.loc.gov/loc.gmd/gmd.contact. The request: a list of all Phillips 66 maps of California, San Francisco, its peninsula, Marin and Oakland between 1968 and 1971, with dates and scales, and a request for a copy of the full state map and of the small bay map. Target boxes: 12 and 113 (series I), 94 (series I), 3 (series 3), and 1 (series 2).
2. **Newberry Library, H.M. Gousha collection:** reference@newberry.org, telephone 312-255-3512. The request: a box-level search for Phillips 66 maps of California from 1968 to 1970, since Gousha printed Phillips maps and most items after 1949 are not catalogued item by item.
3. **Federal Bureau of Investigation (FOIA):** https://www.fbi.gov/foia. The request: the complete file 9-HQ-49911, with parts 2 to 6, specifically any copy or image of the map, and any laboratory request relating to it.
4. **The owner of zodiackiller.com:** a request for the high-resolution image file (PMHR), and for the source of the claimed code and dimensions. Contact through the website (I did not verify the contact page).
5. **The owner of the forum post (user Tahoe27):** a request for the original scan files and the source of the map. Note: this is an individual, not an institution, and the information from him needs independent confirmation.
6. **The San Francisco Chronicle archive or the San Francisco Public Library (San Francisco History Center):** coverage of 1970 of the cipher message, and whether either republished the map. I did not verify that either holds it.
7. **The Phillips 66 company:** check whether it has an archive of road maps for 1968 to 1970. I did not verify that such an archive exists.
8. **The FBI, for the complete collection:** as in item 3.

## 6. What could unlock the path now

If you upload FBI files parts 2 to 6 (and all of part 1) to the conversation, I can read them locally, search their text, and convert the image pages into images for visual examination. This is the fastest way to get past the limits described in section 4.

## 7. Explicit conclusion

- The original source has not been identified: the edition, date and scale are still not documented.
- I cannot confirm: the 1969 edition, the scale of 6.4 miles per inch, the code 9-QQ-1219-S, or the dimensions 18.75 × 34 inches.
- There is no geographic calibration, no matching control points, and no coordinates.
- Verdict: **we are still in the exploration stage**, and the search is incomplete for the reasons given in section 4.
