from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def replace_between(text, start_marker, end_marker, replacement):
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[:start] + replacement + text[end:]


def main():
    text = (ROOT / "index.html").read_text(encoding="utf-8")

    text = text.replace('<html lang="ko">', '<html lang="en">')
    text = text.replace(
        'content="끝말잇기, 스네이크 이동, 글자 교차를 합친 모바일 한글 단어 퍼즐 게임입니다."',
        'content="A mobile word-chain snake puzzle with path planning and letter crossings."',
    )
    text = text.replace(
        'content="모바일에서 바로 즐기는 한글 단어 스네이크 퍼즐."',
        'content="A mobile English word-chain snake puzzle."',
    )
    text = text.replace(
        '<script src="public/words-data.js"></script>\n  <script src="public/words-blocked-data.js"></script>',
        '<script src="../public/words-en-data.js"></script>\n  <script src="../public/words-en-blocked-data.js"></script>',
    )
    text = text.replace(
        '<script src="public/suggest-config.js"></script>',
        '<script src="../public/suggest-config.js"></script>',
    )
    text = text.replace(
        '<script src="public/ad-config.js"></script>',
        '<script src="../public/ad-config.js"></script>',
    )
    text = text.replace(
        '<script src="public/analytics-config.js"></script>',
        '<script src="../public/analytics-config.js"></script>',
    )

    rule_start = '        <p class="intro-copy">'
    rule_end = '      <div class="panel controls">'
    rule_block = """        <p class="intro-copy">Chain words by their last and first letters while moving like a snake.</p>

        <ul class="rule-list panel">
          <li>
            <div class="mini-board" aria-hidden="true">
              <i class="mini-cell start fill">S</i><i class="mini-cell fill">T</i><i class="mini-cell fill">O</i><i class="mini-cell fill">N</i><i class="mini-cell head fill">E</i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell next">A</i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell next">G</i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell next">L</i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell next">E</i>
            </div>
            <p><b>Basic Rule</b><span>STONE ends with E. Type AGLE and EAGLE is placed from the head tile.</span></p>
          </li>
          <li>
            <div class="mini-board" aria-hidden="true">
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell next">B</i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell next">L</i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell fill">S</i><i class="mini-cell fill">T</i><i class="mini-cell fill pass">O</i><i class="mini-cell fill">N</i><i class="mini-cell head fill">E</i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell next">O</i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell next">M</i><i class="mini-cell"></i><i class="mini-cell"></i>
            </div>
            <p><b>Crossing</b><span>BLOOM can pass through the existing O because the letters match.</span></p>
          </li>
          <li>
            <div class="mini-board" aria-hidden="true">
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell fill">T</i><i class="mini-cell fill">I</i><i class="mini-cell fill">M</i><i class="mini-cell head fill">E</i><i class="mini-cell"></i>
              <i class="mini-cell back">T</i><i class="mini-cell back">I</i><i class="mini-cell back">M</i><i class="mini-cell back">E</i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i>
            </div>
            <p><b>Turning Back</b><span>After moving right with TIME, place EMIT to travel back along the same tiles.</span></p>
          </li>
          <li>
            <div class="mini-board" aria-hidden="true">
              <i class="mini-cell"></i><i class="mini-cell fill">E</i><i class="mini-cell"></i><i class="mini-cell fill">E</i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell fill">E</i><i class="mini-cell"></i><i class="mini-cell fill">A</i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell fill">L</i><i class="mini-cell"></i><i class="mini-cell fill">G</i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell fill">L</i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell fill">E</i><i class="mini-cell"></i>
            </div>
            <p><b>Scoring</b><span>EAGLE scores more than EEL, and crossings add extra points.</span></p>
          </li>
          <li>
            <div class="mini-board" aria-hidden="true">
              <i class="mini-cell fill">S</i><i class="mini-cell fill">T</i><i class="mini-cell fill">O</i><i class="mini-cell fill">N</i><i class="mini-cell fill">E</i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell fill">S</i><i class="mini-cell fill">T</i><i class="mini-cell fill">O</i><i class="mini-cell fill">N</i><i class="mini-cell fill">E</i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i>
            </div>
            <p><b>Forbidden</b><span>Once STONE has been used, STONE cannot be placed again.</span></p>
          </li>
        </ul>

"""
    text = replace_between(text, rule_start, rule_end, rule_block)

    replacements = {
        "<h1>word chain snake</h1>": "<h1>word chain snake<br>English</h1>",
        "칸 수": "Board size",
        ">시작<": ">Start<",
        ">랭킹<": ">Ranking<",
        "사전을 불러오는 중입니다.": "Loading dictionary.",
        "<span>점수</span>": "<span>Score</span>",
        'placeholder="단어 입력"': 'placeholder="Enter word"',
        "가장자리 빈 칸을 터치해 시작점을 고르세요.": "Tap an empty edge tile to choose a start.",
        "사전에 없는 단어라면 등록을 제안할 수 있습니다. 관리자가 승인한 뒤에만 게임 사전에 추가됩니다.": "If a word is missing, you can suggest it. It is added only after admin approval.",
        ">제안<": ">Suggest<",
        ">결과<": ">Result<",
        "<span>칸</span>": "<span>Tiles</span>",
        "<span>단어</span>": "<span>Words</span>",
        'placeholder="이름"': 'placeholder="Name"',
        ">등록<": ">Upload<",
        ">공유<": ">Share<",
        ">놓기<": ">Place<",
        ">되돌리기<": ">Undo<",
        ">항복<": ">Surrender<",
        '      up: { x: 0, y: -1, label: "위" },\n      down: { x: 0, y: 1, label: "아래" },\n      left: { x: -1, y: 0, label: "왼쪽" },\n      right: { x: 1, y: 0, label: "오른쪽" }': '      up: { x: 0, y: -1, label: "up" },\n      down: { x: 0, y: 1, label: "down" },\n      left: { x: -1, y: 0, label: "left" },\n      right: { x: 1, y: 0, label: "right" }',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace('const GAME_LANG = "ko";', 'const GAME_LANG = "en";')

    fallback_start = "    const FALLBACK_WORDS = ["
    fallback_end = "    function makeEmptyBoard"
    fallback = """    const FALLBACK_WORDS = [
      "APPLE", "EAGLE", "EARTH", "HOUSE", "EMBER", "RIVER", "ROBOT", "TABLE", "ENERGY", "YELLOW",
      "WATER", "RHYTHM", "MARKET", "TRAVEL", "LETTER", "ROAD", "DREAM", "MUSIC", "CANDLE", "ENGINE"
    ];

"""
    text = replace_between(text, fallback_start, fallback_end, fallback)

    shape_start = "    function normalizeWord(word) {"
    shape_end = "    function wordCandidatesForInput(rawInput, board, gameState) {"
    shape = """    function normalizeWord(word) {
      return String(word || "").trim().toUpperCase();
    }

    function isEnglishWord(word) {
      return /^[A-Z]+$/.test(word);
    }

    function isValidWordShape(word) {
      return isEnglishWord(word) && word.length >= 2;
    }

    function initialLawReadings(letter) {
      return letter ? [letter] : [];
    }

    function headStartLetters(head) {
      return initialLawReadings(head);
    }

"""
    text = replace_between(text, shape_start, shape_end, shape)

    js_replacements = {
        'if (!isKoreanWord(input)) return { ok: false, message: "순수 한글 음절 단어만 사용할 수 있습니다." };': 'if (!isEnglishWord(input)) return { ok: false, message: "Use A-Z letters only." };',
        'if (!delta) return { ok: false, message: "방향을 선택하세요." };': 'if (!delta) return { ok: false, message: "Choose a next tile." };',
        'if (!gameState.start) return { ok: false, message: "먼저 가장자리 시작 칸을 선택하세요." };': 'if (!gameState.start) return { ok: false, message: "Choose an edge start tile first." };',
        'if (gameState.lastDir && gameState.lastDir === dir) return { ok: false, message: "직전 방향과 같은 방향으로는 이동할 수 없습니다." };': 'if (gameState.lastDir && gameState.lastDir === dir) return { ok: false, message: "You cannot move in the same direction twice in a row." };',
        'if (!anchor) return { ok: false, message: "현재 머리 칸이 없습니다." };': 'if (!anchor) return { ok: false, message: "There is no current head tile." };',
        'if (firstTurn && !isEdge(board, anchor.x, anchor.y)) return { ok: false, message: "시작점은 보드 가장자리여야 합니다." };': 'if (firstTurn && !isEdge(board, anchor.x, anchor.y)) return { ok: false, message: "The start tile must be on the board edge." };',
        'if (word.length < 2) return { ok: false, message: "한 글자 표제어는 사용할 수 없습니다." };': 'if (word.length < 2) return { ok: false, message: "One-letter words cannot be used." };',
        'return { ok: false, code: "blocked-word", word, message: "명사로 등재된 단어만 사용할 수 있습니다." };': 'return { ok: false, code: "blocked-word", word, message: "Inflected forms and abbreviations cannot be used." };',
        'return { ok: false, code: "missing-word", word, message: "현재 사전에 없는 단어입니다." };': 'return { ok: false, code: "missing-word", word, message: "This word is not in the dictionary yet." };',
        'return { ok: false, message: "이미 사용한 단어는 다시 사용할 수 없습니다." };': 'return { ok: false, message: "You cannot reuse a word." };',
        'return { ok: false, message: `현재 머리 글자 \'${allowedStarts.join("/")}\'로 시작하는 단어를 입력하세요.` };': 'return { ok: false, message: `Use a word that starts with ${allowedStarts.join("/")}.` };',
        'if (!inBounds(board, x, y)) return { ok: false, message: "단어가 보드 밖으로 나갑니다." };': 'if (!inBounds(board, x, y)) return { ok: false, message: "The word goes off the board." };',
        'return { ok: false, message: `(${x + 1}, ${y + 1}) 칸의 \'${existing}\'와 \'${letter}\'가 다릅니다.` };': 'return { ok: false, message: `Tile (${x + 1}, ${y + 1}) has ${existing}, not ${letter}.` };',
        'setMessage("시작점은 가장자리 칸만 가능합니다.", "error");': 'setMessage("Start points must be edge tiles.", "error");',
        'setMessage("빈 가장자리 칸만 시작점으로 선택할 수 있습니다.", "error");': 'setMessage("Choose an empty edge tile as the start.", "error");',
        'setMessage("진행 중에는 새 판을 눌러 시작점을 다시 고르세요.", "error");': 'setMessage("Start a new game to choose another start tile.", "error");',
        'setMessage(`시작점 (${x + 1}, ${y + 1}) 선택됨. 나아갈 칸을 고르세요.`, "ok");': 'setMessage(`Start (${x + 1}, ${y + 1}) selected. Choose the next tile.`, "ok");',
        '"전체 보드 클리어! 스네이크가 빠져나갑니다."': '"Board cleared! The snake is leaving the board."',
        '"항복했습니다. 스네이크가 길을 따라 빠져나갑니다."': '"Surrendered. The snake is leaving along its path."',
        'const ruleText = result.initialLaw ? `${result.initialLaw.from}/${result.initialLaw.to} 두음법칙 적용. ` : "";': 'const ruleText = "";',
        'const scoreParts = [`+${result.score.gained}점`, `새 칸 +${result.newCells.length}`, `단어 +${result.score.wordBonus}`];': 'const scoreParts = [`+${result.score.gained} pts`, `new tiles +${result.newCells.length}`, `word +${result.score.wordBonus}`];',
        'if (result.score.crossBonus) scoreParts.push(`교차 +${result.score.crossBonus}`);': 'if (result.score.crossBonus) scoreParts.push(`cross +${result.score.crossBonus}`);',
        '`${ruleText}${result.word} 배치 완료. ${scoreParts.join(" · ")}`': '`${ruleText}${result.word} placed. ${scoreParts.join(" · ")}`',
        'setMessage("되돌릴 턴이 없습니다.", "error");': 'setMessage("There is no turn to undo.", "error");',
        'setMessage("한 턴 되돌렸습니다.", "ok");': 'setMessage("Undid one turn.", "ok");',
        'setMessage("가장자리 칸을 눌러 시작점을 고르세요.", "ok");': 'setMessage("Tap an edge tile to choose a start.", "ok");',
        'setMessage(state.turn === 0 ? "단어를 입력하고 놓기를 누르세요." : "뒤 글자를 입력하고 놓기를 누르세요.", "ok");': 'setMessage(state.turn === 0 ? "Enter a word, then place it." : "Enter the remaining letters, then place it.", "ok");',
        'const label = initialLawMark\n            ? `${initialLawMark.from}/${initialLawMark.to} 두음법칙 표시`\n            : cellLetter || previewLetter || "빈 칸";': 'const label = cellLetter || previewLetter || "empty tile";',
        'button.setAttribute("aria-label", `${x + 1}열 ${y + 1}행 ${label}`);': 'button.setAttribute("aria-label", `column ${x + 1}, row ${y + 1}, ${label}`);',
        'els.boardInput.placeholder = state.turn === 0 ? "단어 입력" : `${startLabel} 뒤 글자 입력`;': 'els.boardInput.placeholder = state.turn === 0 ? "Enter word" : `${startLabel} remaining letters`;',
        'els.scoreText.textContent = `${state.score}점 · ${filled} / ${total}`;': 'els.scoreText.textContent = `${state.score} pts · ${filled} / ${total}`;',
        '.slice(0, 16) || "익명";': '.slice(0, 16) || "Player";',
        'els.resultTitle.textContent = type === "clear" ? "클리어 결과" : "항복 결과";': 'els.resultTitle.textContent = type === "clear" ? "Clear Result" : "Surrender Result";',
        'setScoreSubmitStatus(SUGGEST_API ? "점수를 등록할 수 있습니다." : "랭킹 서버 주소가 아직 설정되지 않았습니다.", !SUGGEST_API);': 'setScoreSubmitStatus(SUGGEST_API ? "You can upload your score." : "Ranking server is not configured yet.", !SUGGEST_API);',
        'els.newBtn.textContent = "항복";': 'els.newBtn.textContent = "Surrender";',
        'els.resultTitle.textContent = result.finishType === "clear" ? "클리어 결과" : "항복 결과";': 'els.resultTitle.textContent = result.finishType === "clear" ? "Clear Result" : "Surrender Result";',
        'els.resultScore.textContent = `${result.score.toLocaleString("ko-KR")}점`;': 'els.resultScore.textContent = `${result.score.toLocaleString("en-US")} pts`;',
        'els.resultTurns.textContent = `${result.turns}개`;': 'els.resultTurns.textContent = `${result.turns}`;',
        'els.newBtn.textContent = "처음으로";': 'els.newBtn.textContent = "Home";',
        '<span class="rank">-</span><span class="name">아직 기록이 없습니다</span><span class="score-value">0점</span>': '<span class="rank">-</span><span class="name">No scores yet</span><span class="score-value">0 pts</span>',
        'const finish = item.finishType === "clear" ? "클리어" : "항복";': 'const finish = item.finishType === "clear" ? "Clear" : "Surrender";',
        '<span class="score-value">${Number(item.score || 0).toLocaleString("ko-KR")}점</span>': '<span class="score-value">${Number(item.score || 0).toLocaleString("en-US")} pts</span>',
        'row.querySelector(".name").textContent = `${item.name || "익명"} · ${finish}${isOwn ? " · 내 순위" : ""}`;': 'row.querySelector(".name").textContent = `${item.name || "Player"} · ${finish}${isOwn ? " · My rank" : ""}`;',
        'const finish = ownItem.finishType === "clear" ? "클리어" : "항복";': 'const finish = ownItem.finishType === "clear" ? "Clear" : "Surrender";',
        '<span class="score-value">${Number(ownItem.score || 0).toLocaleString("ko-KR")}점</span>': '<span class="score-value">${Number(ownItem.score || 0).toLocaleString("en-US")} pts</span>',
        'row.querySelector(".name").textContent = `${ownItem.name || "익명"} · ${finish} · 내 순위`;': 'row.querySelector(".name").textContent = `${ownItem.name || "Player"} · ${finish} · My rank`;',
        'if (setStatus) setStatus("랭킹 서버 주소가 아직 설정되지 않았습니다.", true);': 'if (setStatus) setStatus("Ranking server is not configured yet.", true);',
        'if (!response.ok) throw new Error(data.error || "랭킹을 불러오지 못했습니다.");': 'if (!response.ok) throw new Error(data.error || "Could not load rankings.");',
        'if (setStatus) setStatus(error.message || "랭킹을 불러오지 못했습니다.", true);': 'if (setStatus) setStatus(error.message || "Could not load rankings.", true);',
        'setIntroRankingStatus("랭킹을 불러오는 중...");': 'setIntroRankingStatus("Loading rankings...");',
        '// 금지 단어 사전은 실패해도 게임 자체는 계속 진행할 수 있습니다.': '// The blocked-word dictionary is optional; the game can keep running if it fails.',
        'setScoreSubmitStatus("랭킹 서버 주소가 아직 설정되지 않았습니다.", true);': 'setScoreSubmitStatus("Ranking server is not configured yet.", true);',
        'setScoreSubmitStatus("점수 등록 중...");': 'setScoreSubmitStatus("Uploading score...");',
        'if (!response.ok) throw new Error(data.error || "점수 등록에 실패했습니다.");': 'if (!response.ok) throw new Error(data.error || "Could not upload score.");',
        'setScoreSubmitStatus("점수가 등록되었습니다.");': 'setScoreSubmitStatus("Score uploaded.");',
        'setScoreSubmitStatus(error.message || "점수 등록에 실패했습니다.", true);': 'setScoreSubmitStatus(error.message || "Could not upload score.", true);',
        'const finish = result.finishType === "clear" ? "클리어" : "항복";': 'const finish = result.finishType === "clear" ? "Clear" : "Surrender";',
        '`${result.boardSize}x${result.boardSize} / 한국어 / ${finish} / ${result.score.toLocaleString("ko-KR")}점 / ${result.filled}칸`,': '`${result.boardSize}x${result.boardSize} / English / ${finish} / ${result.score.toLocaleString("en-US")} pts / ${result.filled} tiles`,',
        '"긴 단어와 교차로 점수를 올려보세요."': '"Score higher with longer words and crossings."',
        'setShareStatus("공유했습니다.");': 'setShareStatus("Shared.");',
        'setShareStatus("결과를 클립보드에 복사했습니다.");': 'setShareStatus("Result copied to clipboard.");',
        'setShareStatus("브라우저에서 공유를 지원하지 않습니다.", true);': 'setShareStatus("This browser does not support sharing.", true);',
        'setShareStatus("공유하지 못했습니다.", true);': 'setShareStatus("Could not share.", true);',
        'title: `단어 제안: ${word}`': 'title: `Word suggestion: ${word}`',
        'body: `제안 단어: ${word}\\n\\n게임에서 사전에 없는 단어로 확인되어 등록을 제안합니다.`': 'body: `Suggested word: ${word}\\n\\nThis word was not found in the game dictionary and is being suggested for review.`',
        'setSuggestStatus("순수 한글 2글자 이상 단어만 제안할 수 있습니다.", true);': 'setSuggestStatus("Only A-Z words with at least 2 letters can be suggested.", true);',
        'setSuggestStatus("이미 현재 사전에 있는 단어입니다.");': 'setSuggestStatus("This word is already in the dictionary.");',
        'setSuggestStatus("제안 전송 중...");': 'setSuggestStatus("Sending suggestion...");',
        'setSuggestStatus("서버 주소가 아직 설정되지 않아 GitHub 제안 화면을 열었습니다.");': 'setSuggestStatus("Server is not configured, so GitHub issue creation was opened.");',
        'if (!response.ok) throw new Error(data.error || "제안 전송에 실패했습니다.");': 'if (!response.ok) throw new Error(data.error || "Could not send suggestion.");',
        'setMessage(`${word}은 이미 승인된 단어입니다.`, "ok");': 'setMessage(`${word} is already approved.`, "ok");',
        'setSuggestStatus(data.duplicate ? "이미 대기 중인 단어입니다. 중복 제안은 하나로 합쳤습니다." : "제안이 등록되었습니다. 승인 후 사전에 추가됩니다.");': 'setSuggestStatus(data.duplicate ? "This word is already pending. Duplicate suggestions were merged." : "Suggestion saved. It will be added after approval.");',
        'setSuggestStatus(error.message || "제안 전송에 실패했습니다.", true);': 'setSuggestStatus(error.message || "Could not send suggestion.", true);',
        'els.dictStatus.textContent = `사전 ${dictionary.wordSet.size.toLocaleString("ko-KR")}개 준비됨`;': 'els.dictStatus.textContent = `Dictionary ${dictionary.wordSet.size.toLocaleString("en-US")} words ready`;',
        'els.dictStatus.textContent = "사전을 불러오지 못했습니다.";': 'els.dictStatus.textContent = "Could not load the dictionary.";',
    }
    for old, new in js_replacements.items():
        text = text.replace(old, new)

    text = text.replace(
        'localStorage.getItem("wordsnakePlayerName")',
        'localStorage.getItem("wordChainSnakeEnPlayerName")',
    )
    text = text.replace(
        'localStorage.setItem("wordsnakePlayerName", payload.name);',
        'localStorage.setItem("wordChainSnakeEnPlayerName", payload.name);',
    )
    text = text.replace(
        'if (typeof window.WORDSNAKE_WORDS === "string" && window.WORDSNAKE_WORDS.trim()) {\n        loadDictionaryFromText(window.WORDSNAKE_WORDS);',
        'if (typeof window.WORDSNAKE_WORDS_EN === "string" && window.WORDSNAKE_WORDS_EN.trim()) {\n        loadDictionaryFromText(window.WORDSNAKE_WORDS_EN);',
    )
    text = text.replace(
        'const response = await fetch("public/words.txt", { cache: "no-store" });',
        'const response = await fetch("../public/words-en.txt", { cache: "no-store" });',
    )
    text = text.replace(
        "window.WORDSNAKE_BLOCKED_WORDS",
        "window.WORDSNAKE_BLOCKED_WORDS_EN",
    )
    text = text.replace(
        'fetch("public/words-blocked.txt", { cache: "no-store" })',
        'fetch("../public/words-en-blocked.txt", { cache: "no-store" })',
    )
    text = text.replace(
        "      initialLawReadings,\n      wordCandidatesForInput,",
        "      initialLawReadings,\n      isEnglishWord,\n      wordCandidatesForInput,",
    )

    # English has no split initial-law display, but keeping the rendering helper is harmless.
    text = text.replace(
        "Dictionary data includes NIKL Standard Korean Dictionary, Urimalsaem, and Kaikki/Wiktionary-derived data.",
        "English dictionary data is derived from Wiktionary/Wiktextract and WordNet preparation data.",
    )

    out = ROOT / "en" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
