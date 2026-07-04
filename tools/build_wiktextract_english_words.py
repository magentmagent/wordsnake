#!/usr/bin/env python3
"""Extract playable uppercase English words from a Wiktextract JSONL gzip dump."""

from __future__ import annotations

import argparse
import gzip
import json
import re
from pathlib import Path


WORD_RE = re.compile(r"^[A-Z]{2,}$")
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
    "proper",
    "verb",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create public/words-en.txt from Wiktextract JSONL.")
    parser.add_argument("--source", default="raw-wiktextract-data.jsonl.gz", help="Input .jsonl.gz path.")
    parser.add_argument("--out", default="public/words-en.txt", help="Output words file.")
    parser.add_argument(
        "--pos",
        default=",".join(sorted(DEFAULT_POS)),
        help="Comma-separated part-of-speech values to include.",
    )
    parser.add_argument("--include-forms", action="store_true", help="Include inflected forms.")
    return parser.parse_args()


def normalized_word(value: object) -> str:
    word = str(value or "").strip().upper()
    return word if WORD_RE.fullmatch(word) else ""


def add_word(words: set[str], value: object) -> None:
    word = normalized_word(value)
    if word:
        words.add(word)


def main() -> int:
    args = parse_args()
    source = Path(args.source)
    out = Path(args.out)
    allowed_pos = {item.strip() for item in args.pos.split(",") if item.strip()}
    words: set[str] = set()
    lines = 0
    english_entries = 0

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

            english_entries += 1
            add_word(words, item.get("word"))
            if args.include_forms:
                for form in item.get("forms") or []:
                    add_word(words, form.get("form"))

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(sorted(words)) + "\n", encoding="utf-8")
    print(f"read {lines:,} entries; matched {english_entries:,} English entries")
    print(f"wrote {out} with {len(words):,} words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
