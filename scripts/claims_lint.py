#!/usr/bin/env python3
"""Claims-lint: find retired or banned claims before they go out again.

Stdlib only (no installs). Walks the given paths, pulls the visible text out
of .html files (scripts, styles and tags removed) and reads .md / .txt files
as they are, then reports every match of the banned-strings pattern from the
24 Nov 2026 panel (shared facts block F18), with file, line and context.

Skipped on purpose:
  * text inside a <details> block whose <summary> mentions "History" or
    "SUPERSEDED" (kept as history, clearly labelled);
  * lines that start with "Never say:" or "HISTORY" (they quote the banned
    words so people know what not to say);
  * any hit allowed in scripts/claims_allowlist.txt (one `path:regex` per
    line; `path` is a glob matched against the file path, `regex` against the
    matched text plus its context).

Exit code 0 when nothing is found, 1 when at least one hit is not allowed.

Usage:
  python3 scripts/claims_lint.py                 # default paths
  python3 scripts/claims_lint.py --paths docs/ README.md
"""
from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

BANNED = re.compile(
    r"we never buy the stock|clears the stock|end.to.end|destination file|second life|"
    r"\bone file\b|now onboarding|onboarding our first|partnering with our first|founded in|"
    r"\bfounder\b|\bCEO\b|free (first )?pilot|first (pilot )?batch (is )?free|£500.{0,3}1[,.]5|"
    r"10% commission|£25m|£75.100m|£0\.5m|10 Mt|never destroyed|we pay the transport|"
    r"minus our share|no legal route|every item tracked|one by one|partner warehouses|"
    r"named on request|startup hub|profitable since|against nothing|instead of nothing|"
    r"3PLs first|lower fine risk|fines avoided|liquidators typically|"
    r"report of where every item went",  # retired by Cat 24 Nov 2026 (D1)
    re.IGNORECASE,
)

SKIP_LINE = re.compile(r"^\s*(never say:|history)", re.IGNORECASE)
TEXT_SUFFIXES = {".md", ".txt"}
HTML_SUFFIXES = {".html", ".htm"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".omc", ".venv", "venv"}

REPO = Path(__file__).resolve().parent.parent
ALLOWLIST = REPO / "scripts" / "claims_allowlist.txt"


class _VisibleText(HTMLParser):
    """Collect visible text, keeping line breaks so line numbers stay useful."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._hidden = 0          # inside <script> / <style>
        self._details: list[bool] = []  # stack: is this <details> history?
        self._in_summary = False
        self._summary_text = ""

    def _history_depth(self) -> bool:
        return any(self._details)

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._hidden += 1
        elif tag == "details":
            self._details.append(False)
        elif tag == "summary" and self._details:
            self._in_summary = True
            self._summary_text = ""
        if tag in ("br", "p", "li", "tr", "div", "h1", "h2", "h3", "h4", "section", "article"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._hidden:
            self._hidden -= 1
        elif tag == "summary" and self._in_summary:
            self._in_summary = False
            if re.search(r"history|superseded", self._summary_text, re.IGNORECASE):
                self._details[-1] = True
        elif tag == "details" and self._details:
            self._details.pop()

    def handle_data(self, data):
        if self._hidden:
            return
        if self._in_summary:
            self._summary_text += data
        if self._history_depth():
            # keep the line count, drop the words
            self.parts.append("\n" * data.count("\n"))
            return
        self.parts.append(data)


def html_text(raw: str) -> str:
    parser = _VisibleText()
    parser.feed(raw)
    parser.close()
    return "".join(parser.parts)


def load_allowlist(path: Path) -> list[tuple[str, re.Pattern[str]]]:
    rules: list[tuple[str, re.Pattern[str]]] = []
    if not path.exists():
        return rules
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        glob, rx = line.split(":", 1)
        rules.append((glob.strip(), re.compile(rx.strip(), re.IGNORECASE)))
    return rules


def iter_files(paths: list[Path]):
    for p in paths:
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and not (set(f.parts) & SKIP_DIRS) and not f.parent.name.endswith("_files"):
                    if f.suffix.lower() in TEXT_SUFFIXES | HTML_SUFFIXES:
                        yield f


def default_paths() -> list[Path]:
    paths = [REPO / "site", REPO / "README.md", REPO / "docs"]
    parent = REPO.parent
    for extra in ("03_pitch", "06_learn", "00_Thread_Futures_HQ.html", "02_business"):
        if (parent / extra).exists():
            paths.append(parent / extra)
    return [p for p in paths if p.exists()]


def lint(files, allow) -> list[tuple[str, int, str, str]]:
    hits = []
    for f in files:
        try:
            raw = f.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"skip {f}: {exc}", file=sys.stderr)
            continue
        text = html_text(raw) if f.suffix.lower() in HTML_SUFFIXES else raw
        shown = str(f)
        for n, line in enumerate(text.splitlines(), 1):
            if SKIP_LINE.match(line):
                continue
            for m in BANNED.finditer(line):
                start = max(0, m.start() - 35)
                ctx = " ".join(line[start:start + 80].split())
                if any(fnmatch.fnmatch(shown, g) and rx.search(ctx) for g, rx in allow):
                    continue
                hits.append((shown, n, m.group(0), ctx))
    return hits


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--paths", nargs="+", help="files or folders to check (default: site/, README.md, docs/ and sibling folders)")
    ap.add_argument("--allowlist", default=str(ALLOWLIST), help="allowlist file (path:regex per line)")
    args = ap.parse_args(argv)

    paths = [Path(p) for p in args.paths] if args.paths else default_paths()
    files = list(iter_files(paths))
    hits = lint(files, load_allowlist(Path(args.allowlist)))
    for shown, n, word, ctx in hits:
        print(f"{shown}:{n}: [{word}] {ctx}")
    print(f"claims-lint: {len(files)} files checked, {len(hits)} hit(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
