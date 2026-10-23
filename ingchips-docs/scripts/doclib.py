"""Read-only catalog helpers. No external dependencies or cache writes."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "references"
CHIPS = ("ING916", "ING918", "ING20")
TOPICS = ("chip", "ble", "peripheral", "power", "rtos")


def positive(value):
    value = int(value)
    if value < 1:
        raise ValueError("must be positive")
    return value


def headings(text):
    fence = None
    result = []
    for line, content in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})", content)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        match = re.match(r"^(#{1,6})\s+(.+?)(?:\s+\{#([^}]+)\})?$", content)
        if match and fence is None:
            result.append(dict(line=line, level=len(match[1]), title=match[2], anchor=match[3]))
    return result


def catalog():
    return json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))


def safe_path(relative):
    path = (REF / relative).resolve()
    if not path.is_relative_to(REF.resolve()) or path.suffix != ".md" or not path.is_file():
        raise ValueError("path must be an existing Markdown file inside references/")
    return path


def section_at(entries, line):
    return next((h["title"] for h in reversed(entries) if h["line"] <= line), "")
