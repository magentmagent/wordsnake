# word chain snake

`word chain snake`는 끝말잇기, 스네이크 이동, 크로스워드식 글자 교차를 합친 모바일 우선 HTML 퍼즐 프로토타입입니다.

## 실행

브라우저에서 `index.html`을 열면 바로 실행됩니다. 로컬 서버가 필요 없는 단일 파일 프로토타입입니다.

## 규칙

- 첫 화면에서 칸 수를 고르고 `시작`을 누릅니다.
- 보드의 가장자리 빈 칸을 눌러 시작점을 고릅니다.
- 현재 머리 칸 주변에 표시되는 진행 후보 칸을 눌러 방향을 정합니다.
- 단어는 보드가 포커스를 받은 상태에서 바로 입력하며, 입력 중인 글자는 선택한 경로의 칸 위에 미리 표시됩니다.
- 둘째 턴부터는 현재 머리 글자가 자동으로 붙으므로, 사용자는 그 뒤 글자만 입력합니다. 예를 들어 머리가 `자`면 `가용`만 입력해도 `자가용`으로 판정합니다.
- 첫 단어는 시작 칸부터 선택한 진행 방향으로 놓입니다.
- 둘째 턴부터는 현재 머리 글자와 같은 글자로 시작하는 단어만 놓을 수 있습니다. 두음법칙도 허용되어 `라/나`, `녀/여`, `력/역`처럼 읽을 수 있는 첫 글자는 같은 시작으로 봅니다. 두음법칙이 적용된 칸은 대각선으로 나뉘어 원래 글자와 읽은 글자를 함께 표시합니다.
- 직전 턴과 같은 방향은 사용할 수 없습니다. 반대 방향은 허용됩니다.
- 이미 글자가 있는 칸은 새 단어의 해당 글자와 같을 때만 지나갈 수 있습니다.
- 새 칸을 하나도 채우지 않고 기존 글자 위로만 이동하는 것도 허용됩니다.
- 한 번 사용한 단어는 다시 사용할 수 없습니다.
- 점수는 누적 점수입니다. 새로 채운 칸마다 1점을 받고, 기본 단어 점수는 2글자 2점, 3글자 4점, 4글자 6점처럼 `2 * (글자 수 - 1)`로 늘어나며, 기존 글자와 교차하면 교차 보너스를 받습니다.
- 64칸을 모두 채우면 전체 보드 클리어입니다.
- 전체 보드 클리어 또는 항복 시 지금까지 이어온 경로를 거꾸로 따라 시작점 쪽으로 판 밖으로 빠져나갑니다.
- 클리어/항복 뒤에는 결과 화면이 표시되며, 제안 서버가 설정되어 있으면 점수를 등록하고 보드 크기별 랭킹을 볼 수 있습니다.

## 사전 파일

게임은 `public/words-data.js`를 먼저 불러오고, 로컬 서버에서는 `public/words.txt`도 fallback으로 읽습니다. `words-data.js`는 `index.html`을 파일로 직접 열어도 동작하게 하기 위한 사전 payload입니다.

```txt
가게
가격
라디오
버스
카메라
토마토
```

게임은 `#`으로 시작하는 줄을 주석으로 보고 무시합니다. 단어는 순수 한글 음절 2글자 이상만 사용합니다. `words.txt`를 다시 만들었다면 다음 명령으로 `words-data.js`도 갱신하세요.

```bash
python tools/build_words_data_js.py --words public/words.txt --out public/words-data.js
```

## 영어판

영어판은 본판에 합치지 않고 `en/index.html`로 분리되어 있습니다. 루트 페이지의 `English` 버튼은 `/wordsnake/en/?start=1&size=8`처럼 영어판으로 바로 이동합니다.

영어 사전은 Wiktextract JSONL 덤프에서 대문자 A-Z 2글자 이상 단어를 추출해 `public/words-en.txt`와 `public/words-en-data.js`로 둡니다.

```powershell
python .\tools\build_wiktextract_english_words.py --source .\raw-wiktextract-data.jsonl.gz --out .\public\words-en.txt --include-forms
python .\tools\build_words_data_js.py --words .\public\words-en.txt --out .\public\words-en-data.js --global-name window.WORDSNAKE_WORDS_EN
python .\tools\build_english_page.py
```

영어판 제안 단어와 랭킹은 서버에 `lang=en`으로 전송되어 한국어판 데이터와 분리됩니다.

## 표준국어대사전 API 빌드

API 키는 클라이언트 HTML에 넣지 마세요. 브라우저에서 직접 API를 호출하면 키가 노출됩니다. 로컬 Python 스크립트로 `words.txt`를 만든 뒤 게임에서 파일로 불러오거나 `public/words.txt`로 보관하세요.

```bash
python tools/build_official_stdict_words.py --key YOUR_API_KEY --out public/words.txt
```

외래어가 빠지지 않도록 기본값은 `type2=all`입니다. 외래어만 시험하려면 다음처럼 실행합니다.

```bash
python tools/build_official_stdict_words.py --key YOUR_API_KEY --out loanwords.txt --type2 loanword
```

일부 prefix만 테스트할 수도 있습니다.

```bash
python tools/build_official_stdict_words.py --key YOUR_API_KEY --out words-test.txt --prefixes 가 나 다 라 마 --verbose
```

중단 후 재개:

```bash
python tools/build_official_stdict_words.py --key YOUR_API_KEY --out public/words.txt --resume
```

표준국어대사전 데이터 사용 시 국립국어원 표준국어대사전 OpenAPI 이용 조건, 출처 표기, 저작권 안내를 확인하세요.

## 표준국어대사전 전체 내려받기 XLS 빌드

표준국어대사전 전체 내려받기 `.xls` 파일이 있으면 Excel COM으로 더 빠르게 `words.txt`를 만들 수 있습니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\build_words_from_stdict_xls.ps1 `
  -InputDir ".\전체 내려받기_표준국어대사전_xls_20260704" `
  -Out .\public\words.txt
```

이 스크립트는 `구성 단위=단어`, `품사`에 `명사`, `동사`, `형용사`, `부사` 중 하나 포함, 순수 한글 2글자 이상 조건으로 표제어를 정제합니다.

## Wiktionary/Kaikki 데이터 병합

표준국어대사전에 없는 생활 어휘와 복합어를 보강하려면 Kaikki의 Korean JSONL 데이터를 병합합니다.

```bash
python tools/merge_kaikki_korean_words.py --words public/words.txt --include-forms --verbose
```

Kaikki 데이터는 Wiktionary/Wiktextract 기반입니다. 배포 전에 Wiktionary와 Kaikki의 라이선스와 출처 표기 조건을 확인하세요.

## 우리말샘 XML 데이터 병합

우리말샘 전체 XML 내려받기 폴더가 있으면 다음 명령으로 기존 `public/words.txt`에 병합합니다.

```powershell
python .\tools\merge_urimalsaem_words.py --words .\public\words.txt --input-dir ".\전체 내려받기_우리말샘_xml_20260602" --include-conjugations --verbose
python .\tools\build_words_data_js.py --words .\public\words.txt --out .\public\words-data.js
```

추출 기준은 순수 한글 2글자 이상이며, 접사/조사/어미/옛말 항목은 제외합니다.

## 공개 배포와 광고

정적 웹사이트로 배포할 수 있습니다. GitHub Pages, Netlify, Vercel, Cloudflare Pages 같은 정적 호스팅에 `index.html`과 `public/`을 올리면 됩니다.

구체적인 배포 절차와 AdSense 준비 순서는 `DEPLOYMENT.md`를 참고하세요. AdSense publisher ID를 받기 전까지는 `public/ad-config.js`의 `enabled`를 `false`로 두고, `ads.txt.template`도 그대로 둡니다. 실제 ID를 받은 뒤 `public/ad-config.js`를 갱신하고 `ads.txt.template`을 `ads.txt`로 이름을 바꿔 배포합니다.

광고를 붙이기 전에는 다음을 확인하세요.

- `NOTICE.md`의 출처와 라이선스 표기를 유지합니다.
- 첫 화면의 Notice/Privacy 링크를 유지합니다.
- 광고/분석 서비스를 넣는 경우 `privacy.html`을 실제 서비스 정책에 맞게 갱신합니다.
- 사전 데이터는 코드와 별도 산출물로 취급하고, 국립국어원/우리말샘/Kaikki/Wiktionary-derived 데이터의 이용 조건을 검토합니다.

## 사용자 단어 제안

게임에서 사전에 없는 단어를 입력하면 단어 제안 패널이 표시됩니다. 기본 상태에서는 GitHub 이슈 작성 화면으로 연결되고, `public/suggest-config.js`에 제안 서버 URL을 넣으면 서버로 직접 제출됩니다.

승인형 서버 예시는 `server/cloudflare-worker.js`에 있습니다. 같은 단어가 여러 번 제출되면 서버에서 하나의 항목으로 합치고 `count`만 올립니다. 관리자는 `admin.html`에서 대기 단어를 보고 승인하거나 거절할 수 있습니다. 승인된 단어는 게임 시작 시 서버의 `/words`에서 추가로 불러와 사전에 합쳐집니다.

같은 Worker는 점수 랭킹도 처리합니다. 게임은 종료 후 `/scores`에 점수를 제출하고, `/scores?boardSize=8&limit=10`처럼 보드 크기별 랭킹을 읽습니다.

```js
window.WORDSNAKE_SUGGEST_API = "https://YOUR_WORKER.YOUR_SUBDOMAIN.workers.dev";
```
