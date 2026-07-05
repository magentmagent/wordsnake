#!/usr/bin/env python3
"""Extract playable uppercase English words from a Wiktextract JSONL gzip dump."""

from __future__ import annotations

import argparse
import gzip
import json
import re
from pathlib import Path


WORD_RE = re.compile(r"^[A-Z]{2,}$")
SOURCE_WORD_RE = re.compile(r"^[A-Za-z]{2,}$")
BLOCKED_SOURCE_RE = re.compile(r"^[A-Za-z]{2,}$")
MARKER_TOKEN_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)?")
TWO_LETTER_ALLOWLIST = {
    "AM",
    "AN",
    "AS",
    "AT",
    "BE",
    "BY",
    "DO",
    "GO",
    "HE",
    "IF",
    "IN",
    "IS",
    "IT",
    "ME",
    "MY",
    "NO",
    "OF",
    "ON",
    "OR",
    "OX",
    "SO",
    "TO",
    "UP",
    "US",
    "WE",
}
ABBREVIATION_MARKERS = {
    "abbreviation",
    "acronym",
    "initialism",
    "short-form",
}
INFLECTION_MARKERS = {
    "form-of",
}
EXCLUDED_MARKERS = {
    *ABBREVIATION_MARKERS,
    "alt-of",
    "alternative",
    "clipping",
    "contraction",
    "ellipsis",
    "form-of",
    "letter",
    "letter-name",
    "misspelling",
    "nonstandard",
    "romanization",
    "symbol",
}
DEFAULT_POS = {
    "adj",
    "adv",
    "conj",
    "det",
    "intj",
    "name",
    "noun",
    "num",
    "prep",
    "pron",
    "verb",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create public/words-en.txt from Wiktextract JSONL.")
    parser.add_argument("--source", default="raw-wiktextract-data.jsonl.gz", help="Input .jsonl.gz path.")
    parser.add_argument("--out", default="public/words-en.txt", help="Output words file.")
    parser.add_argument(
        "--blocked-out",
        default="public/words-en-blocked.txt",
        help="Output words that should be rejected with a reason.",
    )
    parser.add_argument(
        "--pos",
        default=",".join(sorted(DEFAULT_POS)),
        help="Comma-separated part-of-speech values to include.",
    )
    parser.add_argument("--include-forms", action="store_true", help="Include inflected forms.")
    return parser.parse_args()


def marker_texts(value: object) -> set[str]:
    if not value:
        return set()
    if isinstance(value, str):
        return {value.lower()}
    if isinstance(value, list):
        return {str(item).lower() for item in value}
    return {str(value).lower()}


def marker_set_from_keys(item: dict, keys: tuple[str, ...]) -> set[str]:
    texts = set()
    for key in keys:
        texts.update(marker_texts(item.get(key)))
    return texts


def marker_set(item: dict) -> set[str]:
    texts = marker_set_from_keys(item, ("tags", "topics"))
    for sense in item.get("senses") or []:
        texts.update(marker_set_from_keys(sense, ("tags", "categories", "topics")))
    return texts


def has_marker(texts: set[str], markers: set[str]) -> bool:
    marker_forms = markers | {f"{marker}s" for marker in markers}
    for text in texts:
        for token in MARKER_TOKEN_RE.findall(text):
            if token in marker_forms:
                return True
    return False


def has_excluded_marker(item: dict) -> bool:
    return has_marker(marker_set(item), EXCLUDED_MARKERS)


def has_abbreviation_marker(item: dict) -> bool:
    return has_marker(marker_set(item), ABBREVIATION_MARKERS)


def has_inflection_marker(item: dict) -> bool:
    return has_marker(marker_set(item), INFLECTION_MARKERS)


def has_playable_sense(item: dict) -> bool:
    page_markers = marker_set_from_keys(item, ("tags", "topics"))
    if has_marker(page_markers, EXCLUDED_MARKERS):
        return False

    senses = item.get("senses") or []
    if not senses:
        return True
    for sense in senses:
        sense_markers = marker_set_from_keys(sense, ("tags", "categories", "topics"))
        if not has_marker(sense_markers, EXCLUDED_MARKERS):
            return True
    return False


def normalized_word(value: object) -> str:
    source = str(value or "").strip()
    if not SOURCE_WORD_RE.fullmatch(source):
        return ""
    word = source.upper()
    if len(word) == 2 and word not in TWO_LETTER_ALLOWLIST:
        return ""
    return word if WORD_RE.fullmatch(word) else ""


def normalized_blocked_word(value: object) -> str:
    source = str(value or "").strip()
    if not BLOCKED_SOURCE_RE.fullmatch(source):
        return ""
    word = source.upper()
    if len(word) == 2 and word in TWO_LETTER_ALLOWLIST:
        return ""
    return word if WORD_RE.fullmatch(word) else ""


def add_word(words: set[str], value: object) -> None:
    word = normalized_word(value)
    if word:
        words.add(word)


def add_blocked_word(words: set[str], value: object) -> None:
    word = normalized_blocked_word(value)
    if word:
        words.add(word)


def likely_lemma_for_inflection(word: str, words: set[str]) -> str:
    candidates: list[str] = []
    if word.endswith("ING") and len(word) > 5:
        stem = word[:-3]
        candidates.extend([stem, stem + "E"])
        if len(stem) >= 2 and stem[-1] == stem[-2]:
            candidates.append(stem[:-1])
    if word.endswith("ED") and len(word) > 4:
        stem = word[:-2]
        candidates.extend([stem, stem + "E"])
        if len(stem) >= 2 and stem[-1] == stem[-2]:
            candidates.append(stem[:-1])
    if word.endswith("ES") and len(word) > 4:
        stem = word[:-2]
        candidates.extend([stem, stem + "E"])
    if word.endswith("S") and len(word) > 3 and not word.endswith("SS"):
        candidates.append(word[:-1])
    return next((candidate for candidate in candidates if candidate in words), "")


def main() -> int:
    args = parse_args()
    source = Path(args.source)
    out = Path(args.out)
    blocked_out = Path(args.blocked_out)
    allowed_pos = {item.strip() for item in args.pos.split(",") if item.strip()}
    words: set[str] = set()
    blocked_words: set[str] = set()
    inflected_words: set[str] = set()
    lines = 0
    english_entries = 0
    blocked_entries = 0

    with gzip.open(source, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            lines += 1
            if '"lang_code": "en"' not in line and '"lang_code":"en"' not in line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if item.get("lang_code") != "en":
                continue
            pos = item.get("pos")
            if allowed_pos and pos not in allowed_pos:
                continue
            is_abbreviation = has_abbreviation_marker(item)
            is_inflection = has_inflection_marker(item)
            is_playable = has_playable_sense(item)
            if is_abbreviation or not is_playable:
                blocked_entries += 1
                add_blocked_word(blocked_words, item.get("word"))
            if is_inflection:
                word = normalized_blocked_word(item.get("word"))
                if word:
                    inflected_words.add(word)
            if not is_playable:
                continue

            english_entries += 1
            add_word(words, item.get("word"))
            if args.include_forms:
                for form in item.get("forms") or []:
                    add_word(words, form.get("form"))

    out.parent.mkdir(parents=True, exist_ok=True)
    for word in sorted(inflected_words & words):
        if likely_lemma_for_inflection(word, words):
            words.remove(word)
            blocked_words.add(word)
    blocked_words.difference_update(words)
    out.write_text("\n".join(sorted(words)) + "\n", encoding="utf-8")
    blocked_out.parent.mkdir(parents=True, exist_ok=True)
    blocked_out.write_text("\n".join(sorted(blocked_words)) + "\n", encoding="utf-8")
    print(f"read {lines:,} entries; matched {english_entries:,} English entries")
    print(f"found {blocked_entries:,} blocked-marker entries")
    print(f"wrote {out} with {len(words):,} words")
    print(f"wrote {blocked_out} with {len(blocked_words):,} blocked words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
