#!/usr/bin/env python3
"""Build a file:// friendly JavaScript dictionary payload from words.txt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create public/words-data.js from public/words.txt.")
    parser.add_argument("--words", default="public/words.txt", help="Input words.txt path.")
    parser.add_argument("--out", default="public/words-data.js", help="Output JavaScript file.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    words_path = Path(args.words)
    out_path = Path(args.out)
    text = words_path.read_text(encoding="utf-8")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = "window.WORDSNAKE_WORDS = " + json.dumps(text, ensure_ascii=False) + ";\n"
    out_path.write_text(payload, encoding="utf-8")
    print(f"wrote {out_path} from {words_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
