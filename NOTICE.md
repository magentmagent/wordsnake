# wordsnake Notices

This project combines original game code with dictionary data derived from third-party sources. This file is intended to make attribution and redistribution boundaries clear before public release or ad-supported deployment.

## Game Code

The `wordsnake` game code, UI, and project-specific scripts are original work unless otherwise noted.

Choose and document a project license before publishing the repository. If no license is chosen, keep the code under "all rights reserved" by default.

## Dictionary Data

The generated dictionary files in `public/words.txt` and `public/words-data.js` include data derived from:

- National Institute of Korean Language, Standard Korean Language Dictionary / 표준국어대사전
  - Website: https://stdict.korean.go.kr/
  - Open API information: https://stdict.korean.go.kr/openapi/openApiInfo.do
- Kaikki.org Korean machine-readable dictionary data
  - Website: https://kaikki.org/dictionary/Korean/
  - Raw data page: https://kaikki.org/dictionary/rawdata.html
- Wiktionary / Wiktextract-derived data
  - Wiktionary: https://www.wiktionary.org/
  - Wiktextract: https://github.com/tatuylonen/wiktextract

Kaikki/Wiktionary-derived data is based on Wiktionary content and is generally distributed under Creative Commons Attribution-ShareAlike terms. Review the relevant current license terms before public redistribution:

- CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/
- Wikimedia Terms of Use: https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use

## Changes Made

Dictionary data has been filtered and transformed for gameplay:

- Non-Hangul entries were removed.
- One-character entries were removed.
- Some source markers and separators were normalized.
- Multiple sources were merged and deduplicated.
- A JavaScript payload, `public/words-data.js`, was generated from `public/words.txt` for file-based browser loading.

## Advertising and Monetization

Advertising or commercial use should be reviewed against the dictionary data licenses and attribution requirements. In particular, CC BY-SA content permits commercial use, but requires attribution and may require share-alike treatment for adapted database/data portions.

This notice is not legal advice.
