from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def replace_between(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[:start] + replacement + text[end:]


def main() -> None:
    text = (ROOT / "index.html").read_text(encoding="utf-8")

    text = text.replace('<html lang="ko">', '<html lang="ja">')
    text = text.replace(
        'content="끝말잇기, 스네이크 이동, 글자 교차를 합친 모바일 한글 단어 퍼즐 게임입니다."',
        'content="しりとり、スネーク移動、文字交差を組み合わせたモバイル単語パズルです。"'
    )
    text = text.replace(
        'content="모바일에서 바로 즐기는 한글 단어 스네이크 퍼즐."',
        'content="ひらがなで遊ぶ日本語 word chain snake。"',
    )
    text = text.replace(
        'content="https://magentmagent.github.io/wordsnake/"',
        'content="https://magentmagent.github.io/wordsnake/ja/"',
    )
    text = text.replace(
        'content="끝말잇기와 스네이크를 결합한 모바일 단어 퍼즐."',
        'content="しりとりとスネークを組み合わせたモバイル単語パズル。"',
    )
    text = text.replace(
        '<script src="public/words-data.js"></script>\n  <script src="public/words-blocked-data.js"></script>',
        '<script src="../public/words-ja-data.js"></script>\n  <script src="../public/words-ja-blocked-data.js"></script>',
    )
    text = text.replace('<script src="public/suggest-config.js"></script>', '<script src="../public/suggest-config.js"></script>')
    text = text.replace('<script src="public/ad-config.js"></script>', '<script src="../public/ad-config.js"></script>')
    text = text.replace('<script src="public/analytics-config.js"></script>', '<script src="../public/analytics-config.js"></script>')

    rule_block = """        <p class="intro-copy">ひらがなでしりとりをしながら、スネークのように盤面を進みます。</p>

        <ul class="rule-list panel">
          <li>
            <div class="mini-board" aria-hidden="true">
              <i class="mini-cell start fill">り</i><i class="mini-cell fill">ん</i><i class="mini-cell head fill">ご</i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell next">り</i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell next">ら</i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i>
            </div>
            <p><b>基本ルール</b><span>りんごの最後は「ご」。続けて「ごりら」を置けます。</span></p>
          </li>
          <li>
            <div class="mini-board" aria-hidden="true">
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell next">し</i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell next">お</i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell fill">す</i><i class="mini-cell fill">し</i><i class="mini-cell fill pass">お</i><i class="mini-cell fill">に</i><i class="mini-cell fill">ぎ</i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell next">に</i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell next">ぎ</i><i class="mini-cell"></i><i class="mini-cell"></i>
            </div>
            <p><b>通過</b><span>同じ文字なら、すでにあるマスを通過できます。</span></p>
          </li>
          <li>
            <div class="mini-board" aria-hidden="true">
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell back">ね</i><i class="mini-cell head fill">こ</i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i>
            </div>
            <p><b>戻る</b><span>ねこで右へ進んだ後、こねを左へ置いて同じ道を戻れます。</span></p>
          </li>
          <li>
            <div class="mini-board" aria-hidden="true">
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell fill">お</i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell fill">に</i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell fill">ぎ</i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell fill pass">り</i><i class="mini-cell fill">ん</i><i class="mini-cell fill">ご</i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i>
            </div>
            <p><b>得点</b><span>おにぎりのような長い単語や、りで交差する配置は追加点になります。</span></p>
          </li>
          <li>
            <div class="mini-board" aria-hidden="true">
              <i class="mini-cell fill">し</i><i class="mini-cell fill">ん</i><i class="mini-cell fill">ぶ</i><i class="mini-cell fill">ん</i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell fill">り</i><i class="mini-cell fill">ん</i><i class="mini-cell fill">ご</i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i>
              <i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i><i class="mini-cell"></i>
            </div>
            <p><b>禁止</b><span>「ん」で終わる単語と、一度使った単語は使えません。</span></p>
          </li>
        </ul>

"""
    text = replace_between(text, '        <p class="intro-copy">', '      <div class="panel controls">', rule_block)

    replacements = {
        "<h1>word chain snake</h1>": "<h1>word chain snake<br>日本語</h1>",
        "칸 수": "盤面",
        ">시작<": ">開始<",
        ">랭킹<": ">ランキング<",
        "사전을 불러오는 중입니다.": "辞書を読み込んでいます。",
        "<span>점수</span>": "<span>得点</span>",
        'placeholder="단어 입력"': 'placeholder="ひらがな入力"',
        "가장자리 빈 칸을 터치해 시작점을 고르세요.": "端の空きマスをタップして開始位置を選んでください。",
        "사전에 없는 단어라면 등록을 제안할 수 있습니다. 관리자가 승인한 뒤에만 게임 사전에 추가됩니다.": "辞書にない単語は提案できます。承認後に追加されます。",
        ">제안<": ">提案<",
        ">결과<": ">結果<",
        "<span>칸</span>": "<span>マス</span>",
        "<span>단어</span>": "<span>単語</span>",
        'placeholder="이름"': 'placeholder="名前"',
        ">등록<": ">登録<",
        ">공유<": ">共有<",
        ">복사<": ">コピー<",
        ">놓기<": ">置く<",
        ">되돌리기<": ">戻す<",
        ">항복<": ">降参<",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace('const GAME_LANG = "ko";', 'const GAME_LANG = "ja";')

    fallback = """    const FALLBACK_WORDS = [
      "りんご", "ごりら", "らっぱ", "すし", "しお", "おにぎり", "ねこ", "こま", "まくら", "らくだ",
      "だるま", "なつ", "つばめ", "めがね", "はな", "しゅうまつ"
    ];

"""
    text = replace_between(text, "    const FALLBACK_WORDS = [", "    function makeEmptyBoard", fallback)

    shape = """    function normalizeWord(word) {
      return String(word || "").trim();
    }

    function isJapaneseWord(word) {
      return /^[ぁ-ゖ]+$/.test(word);
    }

    function isValidWordShape(word) {
      return isJapaneseWord(word) && word.length >= 2;
    }

    const SMALL_KANA_MAP = {
      "ぁ": "あ", "ぃ": "い", "ぅ": "う", "ぇ": "え", "ぉ": "お",
      "ゃ": "や", "ゅ": "ゆ", "ょ": "よ", "ゎ": "わ", "っ": "つ",
      "ゕ": "か", "ゖ": "け"
    };

    function kanaReading(letter) {
      return SMALL_KANA_MAP[letter] || letter;
    }

    function kanaMatches(a, b) {
      return a === b || kanaReading(a) === kanaReading(b);
    }

    function initialLawReadings(letter) {
      return letter ? [...new Set([letter, kanaReading(letter)])] : [];
    }

    function headStartLetters(head) {
      return initialLawReadings(head);
    }

"""
    text = replace_between(text, "    function normalizeWord(word) {", "    function wordCandidatesForInput(rawInput, board, gameState) {", shape)

    js_replacements = {
        'if (!isKoreanWord(input)) return { ok: false, message: "순수 한글 음절 단어만 사용할 수 있습니다." };': 'if (!isJapaneseWord(input)) return { ok: false, message: "ひらがなだけ入力できます。" };',
        'if (!delta) return { ok: false, message: "방향을 선택하세요." };': 'if (!delta) return { ok: false, message: "次のマスを選んでください。" };',
        'if (!gameState.start) return { ok: false, message: "먼저 가장자리 시작 칸을 선택하세요." };': 'if (!gameState.start) return { ok: false, message: "先に端の開始マスを選んでください。" };',
        'if (gameState.lastDir && gameState.lastDir === dir) return { ok: false, message: "직전 방향과 같은 방향으로는 이동할 수 없습니다." };': 'if (gameState.lastDir && gameState.lastDir === dir) return { ok: false, message: "直前と同じ方向には進めません。" };',
        'if (!anchor) return { ok: false, message: "현재 머리 칸이 없습니다." };': 'if (!anchor) return { ok: false, message: "現在の先頭マスがありません。" };',
        'if (firstTurn && !isEdge(board, anchor.x, anchor.y)) return { ok: false, message: "시작점은 보드 가장자리여야 합니다." };': 'if (firstTurn && !isEdge(board, anchor.x, anchor.y)) return { ok: false, message: "開始位置は盤面の端でなければなりません。" };',
        'if (word.length < 2) return { ok: false, message: "한 글자 표제어는 사용할 수 없습니다." };': 'if (word.length < 2) return { ok: false, message: "一文字の単語は使えません。" };',
        'return { ok: false, code: "blocked-word", word, message: "명사로 등재된 단어만 사용할 수 있습니다." };': 'return { ok: false, code: "blocked-word", word, message: "「ん」で終わる単語は使えません。" };',
        'return { ok: false, code: "missing-word", word, message: "현재 사전에 없는 단어입니다." };': 'return { ok: false, code: "missing-word", word, message: "現在の辞書にない単語です。" };',
        'return { ok: false, message: "이미 사용한 단어는 다시 사용할 수 없습니다." };': 'return { ok: false, message: "一度使った単語は使えません。" };',
        'return { ok: false, message: `현재 머리 글자 \'${allowedStarts.join("/")}\'로 시작하는 단어를 입력하세요.` };': 'return { ok: false, message: `${allowedStarts.join("/")} で始まる単語を入力してください。` };',
        'if (!inBounds(board, x, y)) return { ok: false, message: "단어가 보드 밖으로 나갑니다." };': 'if (!inBounds(board, x, y)) return { ok: false, message: "単語が盤面の外に出ます。" };',
        'return { ok: false, message: `(${x + 1}, ${y + 1}) 칸의 \'${existing}\'와 \'${letter}\'가 다릅니다.` };': 'return { ok: false, message: `(${x + 1}, ${y + 1}) の「${existing}」と「${letter}」が合いません。` };',
        'setMessage("시작점은 가장자리 칸만 가능합니다.", "error");': 'setMessage("開始位置は端のマスだけです。", "error");',
        'setMessage("빈 가장자리 칸만 시작점으로 선택할 수 있습니다.", "error");': 'setMessage("空いている端のマスだけ選べます。", "error");',
        'setMessage("진행 중에는 새 판을 눌러 시작점을 다시 고르세요.", "error");': 'setMessage("進行中は新しく始めてください。", "error");',
        'setMessage(`시작점 (${x + 1}, ${y + 1}) 선택됨. 나아갈 칸을 고르세요.`, "ok");': 'setMessage(`開始位置 (${x + 1}, ${y + 1})。次のマスを選んでください。`, "ok");',
        '"전체 보드 클리어! 스네이크가 빠져나갑니다."': '"盤面クリア！スネークが外へ進みます。"',
        '"항복했습니다. 스네이크가 길을 따라 빠져나갑니다."': '"降参しました。スネークが道に沿って外へ進みます。"',
        'const scoreParts = [`+${result.score.gained}점`, `새 칸 +${result.newCells.length}`, `단어 +${result.score.wordBonus}`];': 'const scoreParts = [`+${result.score.gained}点`, `新しいマス +${result.newCells.length}`, `単語 +${result.score.wordBonus}`];',
        'if (result.score.crossBonus) scoreParts.push(`교차 +${result.score.crossBonus}`);': 'if (result.score.crossBonus) scoreParts.push(`交差 +${result.score.crossBonus}`);',
        '`${ruleText}${result.word} 배치 완료. ${scoreParts.join(" · ")}`': '`${ruleText}${result.word} を置きました。${scoreParts.join(" · ")}`',
        'setMessage("되돌릴 턴이 없습니다.", "error");': 'setMessage("戻せる手がありません。", "error");',
        'setMessage("한 턴 되돌렸습니다.", "ok");': 'setMessage("一手戻しました。", "ok");',
        'setMessage("가장자리 칸을 눌러 시작점을 고르세요.", "ok");': 'setMessage("端のマスを押して開始位置を選んでください。", "ok");',
        'setMessage(state.turn === 0 ? "단어를 입력하고 놓기를 누르세요." : "뒷 글자를 입력하고 놓기를 누르세요.", "ok");': 'setMessage(state.turn === 0 ? "単語を入力して置いてください。" : "続きの文字を入力して置いてください。", "ok");',
        'setMessage(state.turn === 0 ? "단어를 입력하고 놓기를 누르세요." : "뒤 글자를 입력하고 놓기를 누르세요.", "ok");': 'setMessage(state.turn === 0 ? "単語を入力して置いてください。" : "続きの文字を入力して置いてください。", "ok");',
        'els.boardInput.placeholder = state.turn === 0 ? "단어 입력" : `${startLabel} 뒷 글자 입력`;': 'els.boardInput.placeholder = state.turn === 0 ? "ひらがな入力" : `${startLabel} に続ける`;',
        'els.boardInput.placeholder = state.turn === 0 ? "단어 입력" : `${startLabel} 뒤 글자 입력`;': 'els.boardInput.placeholder = state.turn === 0 ? "ひらがな入力" : `${startLabel} に続ける`;',
        '"빈 칸"': '"空きマス"',
        'els.scoreText.textContent = `${state.score}점 · ${filled} / ${total}`;': 'els.scoreText.textContent = `${state.score}点 · ${filled} / ${total}`;',
        '.slice(0, 16) || "익명";': '.slice(0, 16) || "匿名";',
        'els.resultTitle.textContent = type === "clear" ? "클리어 결과" : "항복 결과";': 'els.resultTitle.textContent = type === "clear" ? "クリア結果" : "降参結果";',
        'setScoreSubmitStatus(SUGGEST_API ? "점수를 등록할 수 있습니다." : "랭킹 서버 주소가 아직 설정되지 않았습니다.", !SUGGEST_API);': 'setScoreSubmitStatus(SUGGEST_API ? "得点を登録できます。" : "ランキングサーバーが未設定です。", !SUGGEST_API);',
        'els.newBtn.textContent = "항복";': 'els.newBtn.textContent = "降参";',
        'els.resultTitle.textContent = result.finishType === "clear" ? "클리어 결과" : "항복 결과";': 'els.resultTitle.textContent = result.finishType === "clear" ? "クリア結果" : "降参結果";',
        'els.resultScore.textContent = `${result.score.toLocaleString("ko-KR")}점`;': 'els.resultScore.textContent = `${result.score.toLocaleString("ja-JP")}点`;',
        'els.resultTurns.textContent = `${result.turns}개`;': 'els.resultTurns.textContent = `${result.turns}`;',
        'els.newBtn.textContent = "처음으로";': 'els.newBtn.textContent = "ホーム";',
        'const finish = item.finishType === "clear" ? "클리어" : "항복";': 'const finish = item.finishType === "clear" ? "クリア" : "降参";',
        'Number(item.score || 0).toLocaleString("ko-KR")': 'Number(item.score || 0).toLocaleString("ja-JP")',
        'ownItem.name || "익명"': 'ownItem.name || "匿名"',
        'item.name || "익명"': 'item.name || "匿名"',
        'const finish = ownItem.finishType === "clear" ? "클리어" : "항복";': 'const finish = ownItem.finishType === "clear" ? "クリア" : "降参";',
        '나의 순위': '自分の順位',
        '아직 기록이 없습니다': 'まだ記録がありません',
        'if (setStatus) setStatus("랭킹 서버 주소가 아직 설정되지 않았습니다.", true);': 'if (setStatus) setStatus("ランキングサーバーが未設定です。", true);',
        'setScoreSubmitStatus("랭킹 서버 주소가 아직 설정되지 않았습니다.", true);': 'setScoreSubmitStatus("ランキングサーバーが未設定です。", true);',
        'setScoreSubmitStatus("점수 등록 중...");': 'setScoreSubmitStatus("得点を登録中...");',
        'if (!response.ok) throw new Error(data.error || "점수 등록에 실패했습니다.");': 'if (!response.ok) throw new Error(data.error || "得点の登録に失敗しました。");',
        'setScoreSubmitStatus("점수가 등록되었습니다.");': 'setScoreSubmitStatus("得点を登録しました。");',
        'setScoreSubmitStatus(error.message || "점수 등록에 실패했습니다.", true);': 'setScoreSubmitStatus(error.message || "得点の登録に失敗しました。", true);',
        'const finish = result.finishType === "clear" ? "클리어" : "항복";': 'const finish = result.finishType === "clear" ? "クリア" : "降参";',
        'return `${result.boardSize}x${result.boardSize} 한국어 ${finish} ${result.score.toLocaleString("ko-KR")}점`;': 'return `${result.boardSize}x${result.boardSize} 日本語 ${finish} ${result.score.toLocaleString("ja-JP")}点`;',
        '`${result.filled} / ${result.total}칸, ${result.turns}개 단어`,': '`${result.filled} / ${result.total}マス, ${result.turns}単語`,',
        '"긴 단어와 교차로 점수를 올려보세요."': '"長い単語と交差で得点を伸ばしましょう。"',
        'return `${shareSummary()}\\n끝말잇기와 스네이크를 합친 단어 퍼즐`;': 'return `${shareSummary()}\\nしりとりとスネークを組み合わせた単語パズル`;',
        'setShareStatus("X 공유 창을 열었습니다.");': 'setShareStatus("Xの共有画面を開きました。");',
        'setShareStatus("공유했습니다.");': 'setShareStatus("共有しました。");',
        'setShareStatus("결과를 클립보드에 복사했습니다.");': 'setShareStatus("結果をクリップボードにコピーしました。");',
        'setShareStatus("공유하지 못했습니다.", true);': 'setShareStatus("共有できませんでした。", true);',
        'setShareStatus("클립보드에 복사하지 못했습니다.", true);': 'setShareStatus("クリップボードにコピーできませんでした。", true);',
        'title: `단어 제안: ${word}`': 'title: `単語の提案: ${word}`',
        'body: `제안 단어: ${word}\\n\\n게임에서 사전에 없는 단어로 확인되어 등록을 제안합니다.`': 'body: `提案単語: ${word}\\n\\nゲーム辞書にない単語として確認されたため、登録を提案します。`',
        'setIntroRankingStatus("랭킹을 불러오는 중...");': 'setIntroRankingStatus("ランキングを読み込み中...");',
        '// 금지 단어 사전은 실패해도 게임 자체는 계속 진행할 수 있습니다.': '// 禁止語辞書の読み込みに失敗しても、ゲーム自体は続行できます。',
        'setSuggestStatus("순수 한글 2글자 이상 단어만 제안할 수 있습니다.", true);': 'setSuggestStatus("ひらがな2文字以上の単語だけ提案できます。", true);',
        'setSuggestStatus("이미 현재 사전에 있는 단어입니다.");': 'setSuggestStatus("すでに辞書にある単語です。");',
        'setSuggestStatus("제안 전송 중...");': 'setSuggestStatus("提案を送信中...");',
        'setSuggestStatus("서버 주소가 아직 설정되지 않아 GitHub 제안 화면을 열었습니다.");': 'setSuggestStatus("サーバーが未設定のため、GitHubの提案画面を開きました。");',
        'if (!response.ok) throw new Error(data.error || "제안 전송에 실패했습니다.");': 'if (!response.ok) throw new Error(data.error || "提案の送信に失敗しました。");',
        'setMessage(`${word}은 이미 승인된 단어입니다.`, "ok");': 'setMessage(`${word} はすでに承認済みの単語です。`, "ok");',
        'setSuggestStatus("제안이 등록되었습니다. 승인 후 사전에 추가됩니다.");': 'setSuggestStatus("提案を登録しました。承認後に追加されます。");',
        'setSuggestStatus(data.duplicate ? "이미 대기 중인 단어입니다. 중복 제안은 하나로 합칩니다." : "제안이 등록되었습니다. 승인 후 사전에 추가됩니다.");': 'setSuggestStatus(data.duplicate ? "すでに承認待ちです。重複提案はまとめられます。" : "提案を登録しました。承認後に追加されます。");',
        'setSuggestStatus(data.duplicate ? "이미 대기 중인 단어입니다. 중복 제안은 하나로 합쳤습니다." : "제안이 등록되었습니다. 승인 후 사전에 추가됩니다.");': 'setSuggestStatus(data.duplicate ? "すでに承認待ちです。重複提案はまとめられました。" : "提案を登録しました。承認後に追加されます。");',
        'setSuggestStatus(error.message || "제안 전송에 실패했습니다.", true);': 'setSuggestStatus(error.message || "提案の送信に失敗しました。", true);',
        '점': '点',
        'els.dictStatus.textContent = `사전 ${dictionary.wordSet.size.toLocaleString("ko-KR")}개 준비됨`;': 'els.dictStatus.textContent = `辞書 ${dictionary.wordSet.size.toLocaleString("ja-JP")}語 読み込み済み`;',
        'els.dictStatus.textContent = "사전을 불러오지 못했습니다.";': 'els.dictStatus.textContent = "辞書を読み込めませんでした。";',
    }
    for old, new in js_replacements.items():
        text = text.replace(old, new)

    text = text.replace(
        'localStorage.getItem("wordsnakePlayerName")',
        'localStorage.getItem("wordChainSnakeJaPlayerName")',
    )
    text = text.replace(
        'localStorage.setItem("wordsnakePlayerName", payload.name);',
        'localStorage.setItem("wordChainSnakeJaPlayerName", payload.name);',
    )
    text = text.replace(
        'if (typeof window.WORDSNAKE_WORDS === "string" && window.WORDSNAKE_WORDS.trim()) {\n        loadDictionaryFromText(window.WORDSNAKE_WORDS);',
        'if (typeof window.WORDSNAKE_WORDS_JA === "string" && window.WORDSNAKE_WORDS_JA.trim()) {\n        loadDictionaryFromText(window.WORDSNAKE_WORDS_JA);',
    )
    text = text.replace(
        'const response = await fetch("public/words.txt", { cache: "no-store" });',
        'const response = await fetch("../public/words-ja.txt", { cache: "no-store" });',
    )
    text = text.replace("window.WORDSNAKE_BLOCKED_WORDS", "window.WORDSNAKE_BLOCKED_WORDS_JA")
    text = text.replace(
        'fetch("public/words-blocked.txt", { cache: "no-store" })',
        'fetch("../public/words-ja-blocked.txt", { cache: "no-store" })',
    )
    text = text.replace(
        'if (head && word[0] && head !== word[0] && headStartLetters(head).includes(word[0])) {',
        'if (false) {',
    )
    text = text.replace(
        'if (head && head !== word[0] && !initialLaw) {',
        'if (head && !kanaMatches(head, word[0]) && !initialLaw) {',
    )
    text = text.replace(
        'if (state.board[y][x] && state.board[y][x] !== word[i]) conflicts.add(key);',
        'if (state.board[y][x] && !kanaMatches(state.board[y][x], word[i])) conflicts.add(key);',
    )
    text = text.replace(
        'if (!firstTurn && !allowedStarts.includes(word[0])) {',
        'if (!firstTurn && !allowedStarts.some(start => kanaMatches(start, word[0]))) {',
    )
    text = text.replace(
        'if (existing && existing !== letter) {',
        'if (existing && !kanaMatches(existing, letter)) {',
    )
    text = text.replace(
        'if (isBlockedWord(word)) {\n        return { ok: false, code: "blocked-word", word, message: "「ん」で終わる単語は使えません。" };\n      }',
        'if (word.endsWith("ん") || isBlockedWord(word)) {\n        return { ok: false, code: "blocked-word", word, message: "「ん」で終わる単語は使えません。" };\n      }',
    )
    text = text.replace(
        "      initialLawReadings,\n      wordCandidatesForInput,",
        "      initialLawReadings,\n      isJapaneseWord,\n      kanaMatches,\n      wordCandidatesForInput,",
    )

    out = ROOT / "ja" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
