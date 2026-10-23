#!/usr/bin/env python3
"""Read a bounded cited excerpt; paths are relative to references/."""
import argparse
import json
import sys
sys.dont_write_bytecode = True
from doclib import REF, catalog, safe_path, section_at, positive


def excerpt(relative, line=1, start=None, count=80, max_chars=12000):
    path = safe_path(relative)
    key = path.relative_to(REF.resolve()).as_posix()
    entry = next((e for e in catalog()["files"] if e["path"] == key), None)
    if entry is None:
        raise ValueError("file is not in the published catalog")
    lines = path.read_text(encoding="utf-8").splitlines()
    begin = start if start is not None else max(1, line - count // 2)
    if begin > len(lines) or (start is None and line > len(lines)):
        raise ValueError("line is past end of file")
    end = min(len(lines), begin + count - 1)
    selected, used = [], 0
    clipped = False
    for number in range(begin, end + 1):
        content = f"{number}: {lines[number - 1]}"
        remaining = max_chars - used
        if len(content) + 1 > remaining:
            if remaining > 1:
                selected.append(content[:remaining - 1])
            clipped = True
            end = number
            break
        selected.append(content)
        used += len(content) + 1
    return dict(path=key, start=begin, end=end, total_lines=len(lines), section=section_at(entry["headings"], line if start is None else begin),
                source_url=entry["source_url"], version=entry["version"], source_sha256=entry.get("source_sha256"),
                truncated_before=begin > 1, truncated_after=clipped or end < len(lines),
                partial_line=clipped, next_start=end if clipped else end + 1, text="\n".join(selected))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    where = ap.add_mutually_exclusive_group()
    where.add_argument("--line", type=positive, default=1)
    where.add_argument("--start", type=positive)
    ap.add_argument("--lines", type=positive, default=80)
    ap.add_argument("--max-chars", type=positive, default=12000)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        result = excerpt(args.path, args.line, args.start, args.lines, args.max_chars)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"{result['path']} L{result['start']}-L{result['end']} / {result['total_lines']} [{result['section']}]\nsource: {result['source_url']}\nversion: {result['version']}")
            print(result['text'])
            if result['truncated_before'] or result['truncated_after']:
                print(f"[bounded excerpt; before={result['truncated_before']}, after={result['truncated_after']}, partial_line={result['partial_line']}; next --start {result['next_start']}]")
    except (OSError, ValueError) as exc:
        ap.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
