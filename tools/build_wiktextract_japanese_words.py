#!/usr/bin/env python3
"""Extract playable hiragana Japanese readings from a Wiktextract JSONL gzip dump."""

from __future__ import annotations

import argparse
import gzip
import json
import re
from pathlib import Path

HIRAGANA_RE = re.compile(r"^[ぁ-ゖ]{2,}$")
KATAKANA_RE = re.compile(r"[\u30a1-\u30f6]")
EXCLUDED_POS = {"romanization", "soft-redirect", "character", "punct", "suffix", "prefix"}
EXCLUDED_MARKERS = {
    "abbreviation",
    "alt-of",
    "alternative",
    "archaic",
    "character",
    "contraction",
    "form-of",
    "historical",
    "inflection",
    "letter",
    "obsolete",
    "romanization",
    "symbol",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create public/words-ja.txt from Wiktextract JSONL.")
    parser.add_argument("--source", default="raw-wiktextract-data.jsonl.gz", help="Input .jsonl.gz path.")
    parser.add_argument("--out", default="public/words-ja.txt", help="Output hiragana words file.")
    parser.add_argument(
        "--blocked-out",
        default="public/words-ja-blocked.txt",
        help="Output rejected hiragana readings, mostly words ending in ん.",
    )
    return parser.parse_args()


def katakana_to_hiragana(text: str) -> str:
    return KATAKANA_RE.sub(lambda m: chr(ord(m.group(0)) - 0x60), text)


def clean_reading(raw: object) -> str:
    if not isinstance(raw, str):
        return ""
    text = katakana_to_hiragana(raw.strip())
    text = re.sub(r"[・\s\-ー〜～、。,.()/\[\]{}]+", "", text)
    return text if HIRAGANA_RE.fullmatch(text) else ""


def marker_texts(value: object) -> set[str]:
    if not value:
        return set()
    if isinstance(value, str):
        return {value.lower()}
    if isinstance(value, list):
        return {str(item).lower() for item in value}
    return {str(value).lower()}


def item_markers(item: dict) -> set[str]:
    markers = set()
    for key in ("tags", "categories", "topics"):
        markers.update(marker_texts(item.get(key)))
    for sense in item.get("senses") or []:
        for key in ("tags", "categories", "topics"):
            markers.update(marker_texts(sense.get(key)))
    return markers


def has_excluded_marker(item: dict) -> bool:
    markers = item_markers(item)
    return any(marker in text for marker in EXCLUDED_MARKERS for text in markers)


def readings_from_ruby(form: dict) -> list[str]:
    chunks = []
    ruby = form.get("ruby")
    if not isinstance(ruby, list):
        return []
    for pair in ruby:
        if isinstance(pair, list) and len(pair) >= 2:
            chunks.append(str(pair[1]))
    reading = clean_reading("".join(chunks))
    return [reading] if reading else []


def readings_from_item(item: dict) -> set[str]:
    readings: set[str] = set()
    readings.add(clean_reading(item.get("word")))
    for sound in item.get("sounds") or []:
        if isinstance(sound, dict):
            readings.add(clean_reading(sound.get("other")))
    for form in item.get("forms") or []:
        if not isinstance(form, dict):
            continue
        tags = set(marker_texts(form.get("tags")))
        if form.get("source") == "inflection":
            continue
        if "romanization" in tags:
            continue
        readings.add(clean_reading(form.get("form")))
        readings.update(readings_from_ruby(form))
    return {reading for reading in readings if reading}


def main() -> int:
    args = parse_args()
    source = Path(args.source)
    words: set[str] = set()
    blocked_words: set[str] = set()
    lines = 0
    matched = 0

    with gzip.open(source, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            lines += 1
            if '"lang_code": "ja"' not in line and '"lang_code":"ja"' not in line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if item.get("lang_code") != "ja":
                continue
            if item.get("pos") in EXCLUDED_POS or has_excluded_marker(item):
                continue

            matched += 1
            for reading in readings_from_item(item):
                if reading.endswith("ん"):
                    blocked_words.add(reading)
                else:
                    words.add(reading)

    blocked_words.difference_update(words)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(sorted(words)) + "\n", encoding="utf-8")
    blocked_out = Path(args.blocked_out)
    blocked_out.parent.mkdir(parents=True, exist_ok=True)
    blocked_out.write_text("\n".join(sorted(blocked_words)) + "\n", encoding="utf-8")
    print(f"read {lines:,} entries; matched {matched:,} Japanese entries")
    print(f"wrote {out} with {len(words):,} words")
    print(f"wrote {blocked_out} with {len(blocked_words):,} blocked words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
