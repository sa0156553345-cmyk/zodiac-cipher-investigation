> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 9c26bb7631ec0ae68f73d38463a8c93ad05c4582db448f3b68fe8b261042f96c.

# Stage 4: status of the examination of the FBI files and the parallel track (Phillips 66)

## First: status of the examination of the FBI files

- **Download into the container: failed.** The `curl` command to `https://vault.fbi.gov/The%20Zodiac%20Killer/The%20Zodiac%20Killer%20Part%2002/at_download/file` returned `curl: (6) Could not resolve host: vault.fbi.gov` and `HTTP 000`. The network is disabled in the bash environment, and the same error applies to all of parts 02 to 07.
- **Reading through the fetch tool: partial.** The tool returns the beginning of the text inside the conversation only. It does not save the file, and does not give the number of pages.
  - Parts 02, 03 and 04: only their beginnings were read (see PHASE3_FBI_PARTS_2_TO_7.md). They were not examined in full.
  - Parts 05, 06 and 07: return "This PDF is empty or contains no machine-readable text". There is no OCR, and the tool does not display page images.
- **Full OCR of parts 05 to 07: not carried out.** The files are not present in the container. The local tools (`pdftotext`, `pdftoppm` and `tesseract`) exist, but they need the files uploaded to `/mnt/user-data/uploads`.
- **New pages examined in this stage: none.**

## Second: what is needed to complete the examination

Upload the six files downloaded from the official links:
1. `zodiac2.pdf` (2.9 MB)
2. `zodiac3.pdf` (2.0 MB)
3. `zodiac4.pdf` (19.6 MB)
4. `zodiac5 pages 1-249.pdf` (28.7 MB, 249 pages)
5. `zodiac5 pages 250-372.pdf` (6.5 MB, 123 pages)
6. `The Zodiac Killer Part 07 (Final).pdf` (7.4 MB, number of pages unknown)

After uploading: `pdftotext` to extract the full text of parts 02 to 04; then `pdftoppm` and `tesseract` on parts 05 to 07; then a search for the required words, allowing for OCR variations; then visual examination of the candidate pages. Each result is recorded with its file number and its actual page number.

## Third: the parallel track (searching for the original Phillips 66 map)

| Claim | Source | Classification |
|---|---|---|
| Phillips 66 was a publisher of maps for California, San Francisco and its peninsula, Oakland and Marin, without dates | Peterson III collection finding aid, Library of Congress: https://tile.loc.gov/storage-services/service/gdc/gdcfindingaidpdfs/gm023002/gm023002.pdf | institutional cataloguing record (no date and no scale) |
| The map "1969 Edition", with the section 8 × 6¾ inches and the full map 18¾ × 34 inches | forum post, 2009–2010, whose author owns a physical copy: https://www.tapatalk.com/groups/zodiackillerfr/original-phillips-66-map-t3190.html | primary but non-institutional source; not verified |
| A 1968 edition differing from the 1969 edition | forum post (2022) saying its author scanned the back of "his 68 copy": https://www.tapatalk.com/groups/zodiackillerfr/original-phillips-66-map-t3190-s30.html | claim that could not be verified (no image available here) |
| A high-resolution map is available on zodiackillerfacts.com | mentioned in a forum post (2022) | secondary source; I could not see the image |
| "1969 Edition" printed on the map | post on X (August 2026): https://x.com/maddiedreese/status/2083604506592575600/photo/2 | claim that could not be verified |
| Scale of San Francisco and Vicinity = 1 inch ≈ 6.4 miles | the websites ciphermysteries.com and zodiackillerfacts.com | secondary source with no primary source |
| Magnetic north, and the instruction "0 is to be set to Mag. N." on the map | zodiackillerfacts.com, and forum posts | claim not verified from an image of the original map |
| The code 9-QQ-1219-S | forum posts only | claim that could not be verified |

**The parallel track did not produce an institutional primary source identifying the edition, date or scale of the map.** The closest thing found is the Library of Congress finding aid, which identifies only the publisher. Information about the 1968 or 1969 edition comes from people who own private copies, and it cannot be verified here.

## Fourth: assessment of the hypothesis

- The evidence from the readable FBI files (the beginnings of parts 02 to 04) does not mention the map, Mount Diablo or Z32. This neither supports nor weakens the hypothesis, because the parts have not been examined in full.
- The edition, date and scale of the map are unconfirmed. If more than one edition exists (1968 and 1969, as the forum says), any calibration that relies on the wrong edition will be wrong.
- I have not recalculated coordinates, and I have not used them in any conclusion.
