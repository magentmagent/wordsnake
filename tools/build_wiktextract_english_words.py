#!/usr/bin/env python3
"""Extract playable uppercase English words from a Wiktextract JSONL gzip dump."""

from __future__ import annotations

import argparse
import gzip
import json
import re
from pathlib import Path


WORD_RE = re.compile(r"^[A-Z]{2,}$")
SOURCE_WORD_RE = re.compile(r"^[a-z]{2,}$")
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


def marker_set(item: dict) -> set[str]:
    texts = set()
    for key in ("tags", "categories", "topics"):
        texts.update(marker_texts(item.get(key)))
    for sense in item.get("senses") or []:
        for key in ("tags", "categories", "topics"):
            texts.update(marker_texts(sense.get(key)))
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


def main() -> int:
    args = parse_args()
    source = Path(args.source)
    out = Path(args.out)
    blocked_out = Path(args.blocked_out)
    allowed_pos = {item.strip() for item in args.pos.split(",") if item.strip()}
    words: set[str] = set()
    blocked_words: set[str] = set()
    lines = 0
    english_entries = 0
    blocked_entries = 0

    with gzip.open(source, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            lines += 1
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if item.get("lang_code") != "en":
                continue
            if allowed_pos and item.get("pos") not in allowed_pos:
                continue
            is_excluded = has_excluded_marker(item)
            is_abbreviation = has_abbreviation_marker(item)
            if is_abbreviation or is_excluded:
                blocked_entries += 1
                add_blocked_word(blocked_words, item.get("word"))
            if is_excluded:
                continue

            english_entries += 1
            add_word(words, item.get("word"))
            if args.include_forms:
                for form in item.get("forms") or []:
                    add_word(words, form.get("form"))

    out.parent.mkdir(parents=True, exist_ok=True)
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
