const JSON_HEADERS = {
  "Content-Type": "application/json; charset=utf-8",
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization"
};

const TEXT_HEADERS = {
  "Content-Type": "text/plain; charset=utf-8",
  "Access-Control-Allow-Origin": "*"
};

export default {
  fetch(request, env) {
    return handleRequest(request, env);
  }
};

async function handleRequest(request, env) {
  if (request.method === "OPTIONS") return new Response(null, { headers: JSON_HEADERS });

  const url = new URL(request.url);
  const path = url.pathname.replace(/\/+$/, "") || "/";

  try {
    if (request.method === "POST" && path === "/suggestions") return createSuggestion(request, env);
    if (request.method === "GET" && path === "/words") return listApprovedWords(url, env);
    if (request.method === "POST" && path === "/scores") return createScore(request, env);
    if (request.method === "GET" && path === "/scores") return listScores(url, env);
    if (request.method === "POST" && path === "/events") return createEvent(request, env);
    if (request.method === "GET" && path === "/admin/stats") return listStats(request, url, env);
    if (request.method === "GET" && path === "/admin/suggestions") return listSuggestions(request, url, env);

    const match = path.match(/^\/admin\/suggestions\/([^/]+)\/(approve|reject)$/);
    if (request.method === "POST" && match) {
      return decideSuggestion(request, decodeURIComponent(match[1]), match[2], env, url);
    }

    return json({ error: "not found" }, 404);
  } catch (error) {
    return json({ error: error.message || "server error" }, error.status || 500);
  }
}

async function createSuggestion(request, env) {
  const body = await request.json().catch(() => ({}));
  const lang = normalizeLang(body.lang);
  const word = normalizeWord(body.word, lang);
  if (!isValidWord(word, lang)) return json({ error: "invalid word" }, 400);

  const key = wordKey(word, lang);
  const now = new Date().toISOString();
  const existing = await readRecord(env, key);
  if (existing) {
    existing.lang = existing.lang || lang;
    existing.count = Number(existing.count || 1) + 1;
    existing.updatedAt = now;
    await env.WORDSNAKE_SUGGESTIONS.put(key, JSON.stringify(existing));
    return json({ ok: true, word, status: existing.status, duplicate: true, count: existing.count });
  }

  const record = {
    word,
    lang,
    status: "pending",
    count: 1,
    createdAt: now,
    updatedAt: now
  };
  await env.WORDSNAKE_SUGGESTIONS.put(key, JSON.stringify(record));
  return json({ ok: true, word, status: "pending", duplicate: false, count: 1 }, 201);
}

async function listApprovedWords(url, env) {
  const lang = normalizeLang(url.searchParams.get("lang"));
  const records = await listRecords(env, "approved", lang);
  const locale = lang === "en" ? "en" : lang === "ja" ? "ja" : "ko";
  const words = records.map(item => item.word).sort((a, b) => a.localeCompare(b, locale));
  return new Response(words.join("\n"), { headers: TEXT_HEADERS });
}

async function listSuggestions(request, url, env) {
  requireAdmin(request, env);
  const status = url.searchParams.get("status") || "pending";
  const lang = url.searchParams.has("lang") ? normalizeLang(url.searchParams.get("lang")) : "";
  const items = await listRecords(env, status, lang);
  items.sort((a, b) => String(b.updatedAt || "").localeCompare(String(a.updatedAt || "")));
  return json({ items });
}

async function decideSuggestion(request, word, action, env, url) {
  requireAdmin(request, env);
  const lang = normalizeLang(url.searchParams.get("lang"));
  const normalized = normalizeWord(word, lang);
  if (!isValidWord(normalized, lang)) return json({ error: "invalid word" }, 400);

  const key = wordKey(normalized, lang);
  const record = await readRecord(env, key);
  if (!record) return json({ error: "suggestion not found" }, 404);

  const now = new Date().toISOString();
  record.lang = record.lang || lang;
  record.status = action === "approve" ? "approved" : "rejected";
  record.updatedAt = now;
  record.decidedAt = now;
  await env.WORDSNAKE_SUGGESTIONS.put(key, JSON.stringify(record));
  return json({ ok: true, item: record });
}

async function createScore(request, env) {
  const body = await request.json().catch(() => ({}));
  const game = normalizeGame(body.game);
  const lang = normalizeLang(body.lang);
  const score = clampInteger(body.score, 0, 999999999);
  const boardSize = clampInteger(body.boardSize, 6, 12);
  const mode = normalizeMode(body.mode, game);
  const total = clampInteger(body.total, boardSize * boardSize, boardSize * boardSize);
  const filled = clampInteger(body.filled, 0, total);
  const turns = clampInteger(body.turns, 0, 9999);
  const finishType = normalizeFinishType(body.finishType, game);
  const name = sanitizePlayerName(body.name);
  const now = new Date().toISOString();
  const id = crypto.randomUUID();
  const rankScore = String(999999999 - score).padStart(9, "0");
  const key = scoreKey(game, boardSize, rankScore, id, lang, mode);
  const record = { id, game, lang, mode, name, score, boardSize, filled, total, turns, finishType, createdAt: now };

  await env.WORDSNAKE_SUGGESTIONS.put(key, JSON.stringify(record));
  return json({ ok: true, item: record }, 201);
}

async function listScores(url, env) {
  const game = normalizeGame(url.searchParams.get("game"));
  const lang = normalizeLang(url.searchParams.get("lang"));
  const boardSize = clampInteger(url.searchParams.get("boardSize"), 6, 12);
  const mode = normalizeMode(url.searchParams.get("mode"), game);
  const limit = clampInteger(url.searchParams.get("limit"), 1, 50);
  const id = String(url.searchParams.get("id") || "").trim();
  const records = await listScoreRecords(env, scorePrefix(game, boardSize, lang, mode));
  const items = records.slice(0, limit);
  const ownIndex = id ? records.findIndex(item => item.id === id) : -1;
  const ownRank = ownIndex >= 0 ? ownIndex + 1 : null;
  const ownItem = ownIndex >= 0 ? records[ownIndex] : null;
  return json({ items, ownRank, ownItem });
}

async function createEvent(request, env) {
  const body = await request.json().catch(() => ({}));
  const game = normalizeGame(body.game);
  const lang = normalizeLang(body.lang);
  const boardSize = clampInteger(body.boardSize, 6, 12);
  const mode = normalizeMode(body.mode, game);
  const type = normalizeEventType(body.type, body.finishType, game);
  if (!type) return json({ error: "invalid event" }, 400);

  const day = new Date().toISOString().slice(0, 10);
  await incrementStat(env, statKey("day", day, game, lang, boardSize, mode, type), { scope: "day", day, game, lang, boardSize, mode, type });
  await incrementStat(env, statKey("all", "all", game, lang, boardSize, mode, type), { scope: "all", day: "all", game, lang, boardSize, mode, type });
  return json({ ok: true });
}

async function listStats(request, url, env) {
  requireAdmin(request, env);
  const scope = url.searchParams.get("scope") === "all" ? "all" : "day";
  const day = scope === "all" ? "all" : String(url.searchParams.get("date") || new Date().toISOString().slice(0, 10));
  const prefix = `stats:${scope}:${day}:`;
  const itemsByKey = new Map();
  for (const item of defaultStatItems(scope, day)) {
    itemsByKey.set(statIdentity(item), item);
  }
  let cursor;
  do {
    const page = await env.WORDSNAKE_SUGGESTIONS.list({ prefix, cursor });
    for (const item of page.keys) {
      const record = await readRecord(env, item.name);
      if (record) itemsByKey.set(statIdentity(record), normalizeStatRecord(record, scope, day));
    }
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);
  const items = [...itemsByKey.values()];
  items.sort((a, b) => `${a.game || "word-chain-snake"}:${a.lang}:${a.boardSize}:${a.mode || "classic"}:${a.type}`.localeCompare(`${b.game || "word-chain-snake"}:${b.lang}:${b.boardSize}:${b.mode || "classic"}:${b.type}`));
  return json({ scope, day, items });
}

function defaultStatItems(scope, day) {
  const items = [];
  const langs = ["en", "ko", "ja"];
  const push = (game, lang, boardSize, mode, type) => {
    items.push({ scope, day, game, lang, boardSize, mode, type, count: 0 });
  };

  for (const lang of langs) {
    for (let boardSize = 6; boardSize <= 12; boardSize += 1) {
      for (const mode of ["classic", "snake"]) {
        for (const type of ["page_view", "game_start", "game_finish_clear", "game_finish_surrender", "share_result"]) {
          push("word-chain-snake", lang, boardSize, mode, type);
        }
      }
    }

    for (const mode of ["basic", "chaos"]) {
      for (const type of ["page_view", "game_start", "game_finish_gameover", "share_result"]) {
        push("crown-chain", lang, 8, mode, type);
      }
    }

    for (const mode of ["60", "180"]) {
      for (const type of ["page_view", "game_start", "game_finish_manual", "game_finish_timeout", "share_result"]) {
        push("tower-cut", lang, 6, mode, type);
      }
    }
  }
  return items;
}

function statIdentity(item) {
  const game = normalizeGame(item.game);
  const lang = normalizeLang(item.lang);
  const boardSize = clampInteger(item.boardSize, 1, 99);
  const mode = normalizeMode(item.mode, game);
  const type = normalizeEventType(item.type, item.finishType, game) || String(item.type || "");
  return `${game}:${lang}:${boardSize}:${mode}:${type}`;
}

function normalizeStatRecord(record, scope, day) {
  const game = normalizeGame(record.game);
  const lang = normalizeLang(record.lang);
  const boardSize = clampInteger(record.boardSize, 1, 99);
  const mode = normalizeMode(record.mode, game);
  const type = normalizeEventType(record.type, record.finishType, game) || String(record.type || "");
  return {
    ...record,
    scope,
    day,
    game,
    lang,
    boardSize,
    mode,
    type,
    count: clampInteger(record.count, 0, 999999999)
  };
}

async function incrementStat(env, key, base) {
  const now = new Date().toISOString();
  const existing = await readRecord(env, key);
  const record = existing || { ...base, count: 0, createdAt: now };
  record.count = Number(record.count || 0) + 1;
  record.updatedAt = now;
  await env.WORDSNAKE_SUGGESTIONS.put(key, JSON.stringify(record));
}

async function listScoreRecords(env, prefix) {
  const out = [];
  let cursor;
  do {
    const page = await env.WORDSNAKE_SUGGESTIONS.list({ prefix, cursor });
    for (const item of page.keys) {
      const record = await readRecord(env, item.name);
      if (record) out.push(record);
    }
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);

  out.sort((a, b) => {
    const scoreDiff = Number(b.score || 0) - Number(a.score || 0);
    if (scoreDiff) return scoreDiff;
    return String(a.createdAt || "").localeCompare(String(b.createdAt || ""));
  });
  return out;
}

async function listRecords(env, status, lang = "") {
  const out = [];
  let cursor;
  do {
    const page = await env.WORDSNAKE_SUGGESTIONS.list({ prefix: "word:", cursor });
    for (const item of page.keys) {
      const record = await readRecord(env, item.name);
      if (!record) continue;
      const recordLang = normalizeLang(record.lang);
      if ((!status || record.status === status) && (!lang || recordLang === lang)) out.push(record);
    }
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);
  return out;
}

async function readRecord(env, key) {
  const text = await env.WORDSNAKE_SUGGESTIONS.get(key);
  return text ? JSON.parse(text) : null;
}

function requireAdmin(request, env) {
  const expected = String(env.ADMIN_TOKEN || "");
  if (!expected) throw new Error("ADMIN_TOKEN is not configured");
  const actual = request.headers.get("Authorization") || "";
  if (actual !== `Bearer ${expected}`) {
    const error = new Error("unauthorized");
    error.status = 401;
    throw error;
  }
}

function normalizeLang(value) {
  const lang = String(value || "ko").toLowerCase();
  return ["ko", "en", "ja"].includes(lang) ? lang : "ko";
}

function normalizeGame(value) {
  const game = String(value || "word-chain-snake").toLowerCase();
  if (game === "crown-chain") return "crown-chain";
  if (game === "tower-cut") return "tower-cut";
  return "word-chain-snake";
}

function normalizeMode(value, game = "word-chain-snake") {
  const mode = String(value || "").toLowerCase();
  if (game === "crown-chain") return mode === "chaos" ? "chaos" : "basic";
  if (game === "tower-cut") return mode === "180" ? "180" : "60";
  return mode === "snake" ? "snake" : "classic";
}

function normalizeFinishType(value, game = "word-chain-snake") {
  const finishType = String(value || "").toLowerCase();
  if (game === "crown-chain") return finishType === "gameover" ? "gameover" : "gameover";
  if (game === "tower-cut") return finishType === "manual" ? "manual" : "timeout";
  return finishType === "clear" ? "clear" : "surrender";
}

function normalizeWord(word, lang = "ko") {
  const text = String(word || "").trim();
  if (lang === "en") return text.toUpperCase();
  return text;
}

function isValidWord(word, lang = "ko") {
  if (lang === "en") return /^[A-Z]{2,}$/.test(word);
  if (lang === "ja") return /^[ぁ-ゖ]{2,}$/.test(word);
  return /^[가-힣]{2,}$/.test(word);
}

function wordKey(word, lang = "ko") {
  return lang === "ko" ? `word:${word}` : `word:${lang}:${word}`;
}

function scorePrefix(game = "word-chain-snake", boardSize, lang = "ko", mode = "classic") {
  if (game === "crown-chain") return `score:${game}:${lang}:${mode}:${boardSize}:`;
  if (game === "tower-cut") return `score:${game}:${lang}:${mode}:${boardSize}:`;
  if (mode === "snake") return `score:${lang}:${mode}:${boardSize}:`;
  return lang === "ko" ? `score:${boardSize}:` : `score:${lang}:${boardSize}:`;
}

function scoreKey(game = "word-chain-snake", boardSize, rankScore, id, lang = "ko", mode = "classic") {
  const stamp = Date.now();
  if (game === "crown-chain") return `score:${game}:${lang}:${mode}:${boardSize}:${rankScore}:${stamp}:${id}`;
  if (game === "tower-cut") return `score:${game}:${lang}:${mode}:${boardSize}:${rankScore}:${stamp}:${id}`;
  if (mode === "snake") return `score:${lang}:${mode}:${boardSize}:${rankScore}:${stamp}:${id}`;
  return lang === "ko"
    ? `score:${boardSize}:${rankScore}:${stamp}:${id}`
    : `score:${lang}:${boardSize}:${rankScore}:${stamp}:${id}`;
}

function normalizeEventType(type, finishType = "", game = "word-chain-snake") {
  const eventType = String(type || "").trim();
  if (eventType === "page_view") return "page_view";
  if (eventType === "game_start") return "game_start";
  if (eventType === "share_result") return "share_result";
  if (game === "crown-chain" && eventType === "game_finish") return "game_finish_gameover";
  if (game === "tower-cut" && eventType === "game_finish") return finishType === "manual" ? "game_finish_manual" : "game_finish_timeout";
  if (eventType === "game_finish") return finishType === "clear" ? "game_finish_clear" : "game_finish_surrender";
  return "";
}

function statKey(scope, day, game, lang, boardSize, mode, type) {
  return `stats:${scope}:${day}:${game}:${lang}:${boardSize}:${mode}:${type}`;
}

function clampInteger(value, min, max) {
  const number = Number.parseInt(value, 10);
  if (!Number.isFinite(number)) return min;
  return Math.min(max, Math.max(min, number));
}

function sanitizePlayerName(name) {
  return String(name || "")
    .replace(/[\u0000-\u001f\u007f]/g, "")
    .trim()
    .slice(0, 16) || "Player";
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: JSON_HEADERS });
}
