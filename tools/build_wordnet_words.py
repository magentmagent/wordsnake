#!/usr/bin/env python3
"""Extract playable uppercase English words from an Open English Wordnet XML gzip."""

from __future__ import annotations

import argparse
import gzip
import re
import xml.etree.ElementTree as ET
from pathlib import Path


WORD_RE = re.compile(r"^[A-Z]{2,}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create public/words-en.txt from english-wordnet XML.")
    parser.add_argument("--source", default="english-wordnet-2025.xml.gz", help="Input .xml.gz path.")
    parser.add_argument("--out", default="public/words-en.txt", help="Output words file.")
    return parser.parse_args()


def normalized_word(value: str) -> str:
    word = value.strip().upper()
    return word if WORD_RE.fullmatch(word) else ""


def main() -> int:
    args = parse_args()
    source = Path(args.source)
    out = Path(args.out)
    words: set[str] = set()

    with gzip.open(source, "rb") as handle:
        for event, elem in ET.iterparse(handle, events=("end",)):
            if elem.tag == "Lemma":
                word = normalized_word(elem.attrib.get("writtenForm", ""))
                if word:
                    words.add(word)
            elem.clear()

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(sorted(words)) + "\n", encoding="utf-8")
    print(f"wrote {out} with {len(words):,} words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
