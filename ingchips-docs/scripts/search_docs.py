#!/usr/bin/env python3
"""Bounded, read-only search. Multiple terms mean AND on one line; --any means OR."""
import argparse
import re
import sys
sys.dont_write_bytecode = True
from doclib import CHIPS, TOPICS, catalog, safe_path, section_at, positive
import json


def search(data, queries, book=None, chip=None, topic=None, any_word=False, regex=False):
    patterns = [re.compile(q if regex else re.escape(q), re.I) for q in queries]
    exact = [re.compile(r"(?<!\w)" + re.escape(q) + r"(?!\w)", re.I) for q in queries]
    hits = []
    for entry in data["files"]:
        if book and entry["book"] != book:
            continue
        if chip and entry["chips"] and chip not in entry["chips"]:
            continue
        if topic and topic not in entry["topics"]:
            continue
        for number, line in enumerate(safe_path(entry["path"]).read_text(encoding="utf-8").splitlines(), 1):
            matches = [bool(p.search(line)) for p in patterns]
            if not (any(matches) if any_word else all(matches)):
                continue
            score = sum(matches) * 5 + sum(bool(p.search(line)) for p in exact) * 10
            score += 4 if entry["book"].startswith("pg_") else 0
            score += 2 if line.startswith("#") else 0
            hits.append(dict(path=entry["path"], line=number, section=section_at(entry["headings"], number),
                             text=line.strip()[:240], text_truncated=len(line.strip()) > 240,
                             source_url=entry["source_url"], version=entry["version"], score=score))
    return sorted(hits, key=lambda h: (-h["score"], h["path"], h["line"]))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("query", nargs="+")
    ap.add_argument("--book")
    ap.add_argument("--chip", type=str.upper, choices=CHIPS)
    ap.add_argument("--topic", choices=TOPICS)
    ap.add_argument("--any", action="store_true")
    ap.add_argument("--regex", action="store_true")
    ap.add_argument("--max", type=positive, default=8)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        data = catalog()
        if args.book and args.book not in {b["book"] for b in data["books"]}:
            raise ValueError("unknown book; see INDEX.md")
        hits = search(data, args.query, args.book, args.chip, args.topic, args.any, args.regex)
        selected = hits[:args.max]
        result = dict(total=len(hits), truncated=len(hits) > args.max, hits=selected)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for hit in selected:
                print(f"{hit['path']}:{hit['line']} [{hit['section']}]\n  {hit['text']}" + (" … [line truncated]" if hit['text_truncated'] else ""))
                print(f"  source: {hit['source_url']} | version: {hit['version']}")
            print(f"-- {len(selected)}/{len(hits)} hits" + ("; truncated, narrow scope or increase --max" if result['truncated'] else "") + " --")
    except (OSError, ValueError, re.error) as exc:
        ap.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
