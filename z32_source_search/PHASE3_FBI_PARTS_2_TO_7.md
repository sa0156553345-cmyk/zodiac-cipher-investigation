> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 4436678aa1e28040d85e4e335e92831298996cd9086ac02b7bbe84c52de43d31.

# Stage 3: examination of FBI Vault parts 02 to 07 (Zodiac)

## Technical limits first

- The fetch tool returns the **beginning** of the text extracted from each PDF, up to a set token limit. It does not return the number of pages, nor the proportion of the file that was read. Therefore I cannot say that any part was read in full.
- The fetch tool does not return PDF pages as images. Therefore I cannot examine scanned pages visually.
- The container has no network access, so it cannot download the files. The files are not present in `/mnt/user-data/uploads`.
- The local tools exist (`pdftotext`, `pdftoppm` and `tesseract`), but they work only on files uploaded to the conversation.

## Table

| Part | Official file (size) | Text layer | What was actually read | Source |
|---|---|---|---|---|
| 01 | zodiac1.pdf (about 13 MB) | yes, OCR-scanned | beginning of the text only (from stage 2) | https://vault.fbi.gov/The%20Zodiac%20Killer/The%20Zodiac%20Killer%20Part%2001/view |
| 02 | zodiac2.pdf (2.9 MB) | yes, OCR-scanned, noisy | beginning of the text, about 12,000 tokens | https://vault.fbi.gov/The%20Zodiac%20Killer/The%20Zodiac%20Killer%20Part%2002/view |
| 03 | zodiac3.pdf (2.0 MB) | yes, OCR-scanned, noisy | beginning of the text, about 8,000 tokens | https://vault.fbi.gov/The%20Zodiac%20Killer/The%20Zodiac%20Killer%20Part%2003/view |
| 04 | zodiac4.pdf (19.6 MB) | yes, OCR-scanned, noisy | beginning of the text, about 4,000 tokens | https://vault.fbi.gov/The%20Zodiac%20Killer/The%20Zodiac%20Killer%20Part%2004/view |
| 05 | zodiac5 pages 1-249.pdf (28.7 MB) | **no text layer** | nothing. The tool returned: "This PDF is empty or contains no machine-readable text" | https://vault.fbi.gov/The%20Zodiac%20Killer/The%20Zodiac%20Killer%20Part%2005/view |
| 06 | zodiac5 pages 250-372.pdf (6.5 MB) | **no text layer** | nothing (same message) | https://vault.fbi.gov/The%20Zodiac%20Killer/The%20Zodiac%20Killer%20Part%2006/view |
| 07 (Final) | The Zodiac Killer Part 07 (Final).pdf (7.4 MB) | **no text layer** | nothing (same message) | https://vault.fbi.gov/The%20Zodiac%20Killer/the-zodiac-killer-part-07-final/view |

## What was found in the readable text (parts 02, 03 and 04)

Note: the dates and file numbers are taken from the document headers as they appeared in the noisy text. They are not confirmed from the image.

**Part 02** (memoranda and telegrams from October to November 1969, file 9-HQ-49911):
- An internal memorandum dated 23 October 1969 about a contact with the San Francisco police regarding a newspaper report that parts of a cipher had not been solved. This is a piece of information that can be checked against the original.
- Fingerprint files relating to the Vallejo Times-Herald case (extortion), with laboratory reports numbered A-10042.
- Noisy OCR text suggesting a request from the cryptography section of the laboratory to attempt to decrypt a postal message dated 9 November 1969, previously sent from the Sacramento office on 6 August 1969. **Confidence: low**, because the text is noisy.
- In the readable text I found no reference to Mount Diablo, Phillips 66, a map, or magnetic north.

**Part 03** (memoranda and telegrams from November and December 1969):
- Requests to compare fingerprints of specific individuals, and fingerprint reports. No reference to the map.

**Part 04** (correspondence from August to December 1970):
- Correspondence about a suspect in Ohio (Butler County) after a case in Cincinnati, and fingerprint requests.
- A laboratory report dated 5 November 1970 describes specimens Qc59 to Qc61 (a postcard, an envelope with a San Francisco postmark dated 27 October 1970, and a greeting card). It states that the specimens were sent to the cryptanalysis section.
- A memorandum dated 12 November 1970 says: **"Nothing of cryptographic significance was noted in specimens Qc59 through Qc61."** This is a specific piece of information that can be checked against the original. **Confidence: medium**, because the text is noisy.
- In the readable text I found no reference to the map.

## What was not examined

- Parts 05, 06 and 07 were not examined visually or as text, because they have no text layer and the tool does not display images.
- Parts 02, 03 and 04 were not read in full. Only their beginnings were read.
- The page numbers returned by the tool cannot be determined, because the tool does not provide them. I therefore use the file number and the date instead of the page number.

## Conclusion

- **No readable part showed** a description of the map, an image of it, a reference to Mount Diablo, Phillips 66, Z32, or magnetic north.
- This does not mean the information does not exist. Parts 05, 06 and 07 are scanned and not machine-readable, and parts 02, 03 and 04 were only partly read.
- Two new pieces of information can be checked against the original: the laboratory report on Qc59 to Qc61 (1970), and the cryptanalysis request concerning the message of 9 November 1969 (low confidence because the text is noisy).
- No calibration, and no coordinates.

## The alternative step carried out

Upload the six files to the conversation. Then I will run locally:
1. `pdftotext` to extract the full text from each PDF, then search by keywords (Diablo, Phillips, map, Z32, magnetic, north, 340).
2. `tesseract` on the scanned pages (all of parts 05 to 07).
3. `pdftoppm` to convert the candidate pages into images and display them for visual examination.
4. Record each result with its file number, its actual page number, and the type of evidence.
