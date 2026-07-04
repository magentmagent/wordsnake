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
    if (request.method === "GET" && path === "/words") return listApprovedWords(env);
    if (request.method === "POST" && path === "/scores") return createScore(request, env);
    if (request.method === "GET" && path === "/scores") return listScores(url, env);
    if (request.method === "GET" && path === "/admin/suggestions") return listSuggestions(request, url, env);

    const match = path.match(/^\/admin\/suggestions\/([^/]+)\/(approve|reject)$/);
    if (request.method === "POST" && match) {
      return decideSuggestion(request, decodeURIComponent(match[1]), match[2], env);
    }

    return json({ error: "not found" }, 404);
  } catch (error) {
    return json({ error: error.message || "server error" }, error.status || 500);
  }
}

async function createSuggestion(request, env) {
  const body = await request.json().catch(() => ({}));
  const word = normalizeWord(body.word);
  if (!isValidWord(word)) return json({ error: "순수 한글 2글자 이상 단어만 제안할 수 있습니다." }, 400);

  const key = wordKey(word);
  const now = new Date().toISOString();
  const existing = await readRecord(env, key);
  if (existing) {
    existing.count = Number(existing.count || 1) + 1;
    existing.updatedAt = now;
    await env.WORDSNAKE_SUGGESTIONS.put(key, JSON.stringify(existing));
    return json({ ok: true, word, status: existing.status, duplicate: true, count: existing.count });
  }

  const record = {
    word,
    status: "pending",
    count: 1,
    createdAt: now,
    updatedAt: now
  };
  await env.WORDSNAKE_SUGGESTIONS.put(key, JSON.stringify(record));
  return json({ ok: true, word, status: "pending", duplicate: false, count: 1 }, 201);
}

async function listApprovedWords(env) {
  const records = await listRecords(env, "approved");
  const words = records.map(item => item.word).sort((a, b) => a.localeCompare(b, "ko"));
  return new Response(words.join("\n"), { headers: TEXT_HEADERS });
}

async function listSuggestions(request, url, env) {
  requireAdmin(request, env);
  const status = url.searchParams.get("status") || "pending";
  const items = await listRecords(env, status);
  items.sort((a, b) => String(b.updatedAt || "").localeCompare(String(a.updatedAt || "")));
  return json({ items });
}

async function decideSuggestion(request, word, action, env) {
  requireAdmin(request, env);
  const normalized = normalizeWord(word);
  if (!isValidWord(normalized)) return json({ error: "invalid word" }, 400);

  const key = wordKey(normalized);
  const record = await readRecord(env, key);
  if (!record) return json({ error: "suggestion not found" }, 404);

  const now = new Date().toISOString();
  record.status = action === "approve" ? "approved" : "rejected";
  record.updatedAt = now;
  record.decidedAt = now;
  await env.WORDSNAKE_SUGGESTIONS.put(key, JSON.stringify(record));
  return json({ ok: true, item: record });
}

async function createScore(request, env) {
  const body = await request.json().catch(() => ({}));
  const score = clampInteger(body.score, 0, 999999999);
  const boardSize = clampInteger(body.boardSize, 6, 12);
  const total = clampInteger(body.total, boardSize * boardSize, boardSize * boardSize);
  const filled = clampInteger(body.filled, 0, total);
  const turns = clampInteger(body.turns, 0, 9999);
  const finishType = body.finishType === "clear" ? "clear" : "surrender";
  const name = sanitizePlayerName(body.name);
  const now = new Date().toISOString();
  const id = crypto.randomUUID();
  const rankScore = String(999999999 - score).padStart(9, "0");
  const key = `score:${boardSize}:${rankScore}:${Date.now()}:${id}`;
  const record = { id, name, score, boardSize, filled, total, turns, finishType, createdAt: now };

  await env.WORDSNAKE_SUGGESTIONS.put(key, JSON.stringify(record));
  return json({ ok: true, item: record }, 201);
}

async function listScores(url, env) {
  const boardSize = clampInteger(url.searchParams.get("boardSize"), 6, 12);
  const limit = clampInteger(url.searchParams.get("limit"), 1, 50);
  const items = await listScoreRecords(env, `score:${boardSize}:`, limit);
  return json({ items });
}

async function listScoreRecords(env, prefix, limit) {
  const out = [];
  let cursor;
  do {
    const page = await env.WORDSNAKE_SUGGESTIONS.list({ prefix, cursor });
    for (const item of page.keys) {
      const record = await readRecord(env, item.name);
      if (record) out.push(record);
      if (out.length >= limit * 2) break;
    }
    if (out.length >= limit * 2) break;
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);

  out.sort((a, b) => {
    const scoreDiff = Number(b.score || 0) - Number(a.score || 0);
    if (scoreDiff) return scoreDiff;
    return String(a.createdAt || "").localeCompare(String(b.createdAt || ""));
  });
  return out.slice(0, limit);
}

async function listRecords(env, status) {
  const out = [];
  let cursor;
  do {
    const page = await env.WORDSNAKE_SUGGESTIONS.list({ prefix: "word:", cursor });
    for (const item of page.keys) {
      const record = await readRecord(env, item.name);
      if (record && (!status || record.status === status)) out.push(record);
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

function normalizeWord(word) {
  return String(word || "").trim();
}

function isValidWord(word) {
  return /^[가-힣]{2,}$/.test(word);
}

function wordKey(word) {
  return `word:${word}`;
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
    .slice(0, 16) || "익명";
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: JSON_HEADERS });
}
