#!/usr/bin/env python3
"""
injection_scan.py — Prompt Injection Scanner für Markdown-Dateien

Erkennt versteckten Text und Injection-Versuche in .md-Dateien.
Verwendung:
  python3 injection_scan.py file1.md file2.md ...
  python3 injection_scan.py --staged        # nur git-staged .md-Dateien
  python3 injection_scan.py --all           # alle .md-Dateien im Repo

Exit-Code: 0 = sauber, 1 = Fund(e) gefunden
"""

import re
import sys
import subprocess
from pathlib import Path

# ---------------------------------------------------------------------------
# Muster
# ---------------------------------------------------------------------------

PATTERNS = [
    # HTML-Kommentare
    (r"<!--[\s\S]*?-->", "HTML-Kommentar"),

    # Unsichtbare Styles — Farbe
    (r'style=["\'][^"\']*color\s*:\s*(white|#fff(?:fff)?|rgb\(255\s*,\s*255\s*,\s*255\))[^"\']*["\']',
     "Unsichtbarer Text (weiße Schriftfarbe)"),

    # Unsichtbare Styles — Schriftgröße
    (r'style=["\'][^"\']*font-size\s*:\s*[01](?:\.\d+)?px[^"\']*["\']',
     "Unsichtbarer Text (Schriftgröße ≤ 1px)"),

    # display:none / visibility:hidden
    (r'style=["\'][^"\']*(?:display\s*:\s*none|visibility\s*:\s*hidden)[^"\']*["\']',
     "Verstecktes Element (display:none / visibility:hidden)"),

    # Zero-width Unicode-Zeichen
    (r"[​‌‍⁠﻿­]",
     "Zero-Width / unsichtbares Unicode-Zeichen"),

    # Typische Injection-Phrasen (case-insensitive)
    (r"(?i)ignore\s+(all\s+)?previous\s+instructions?",
     "Injection-Phrase: 'ignore previous instructions'"),
    (r"(?i)\bnew\s+instruction[s:]",
     "Injection-Phrase: 'new instruction'"),
    (r"(?i)\bsystem\s*:\s*(update|override|priority)",
     "Injection-Phrase: 'system: update/override'"),
    (r"(?i)\bpriority\s+override\b",
     "Injection-Phrase: 'priority override'"),
    (r"(?i)you\s+are\s+now\s+(?:a|an)\s+\w+\s+(?:assistant|ai|model)",
     "Injection-Phrase: 'you are now a ... assistant'"),
    (r"(?i)disregard\s+(all\s+)?(?:previous|prior|earlier)\s+(?:instructions?|context|rules?)",
     "Injection-Phrase: 'disregard previous instructions'"),
    (r"(?i)\bDAN\b.*no\s+restrictions?",
     "Injection-Phrase: DAN-Muster"),
]

COMPILED = [(re.compile(p), label) for p, label in PATTERNS]

# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def scan_file(path: Path) -> list[tuple[int, str, str]]:
    """Gibt Liste von (Zeilennummer, Treffer, Label) zurück."""
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  [FEHLER] Kann {path} nicht lesen: {e}", file=sys.stderr)
        return findings

    lines = text.splitlines()
    for pattern, label in COMPILED:
        for match in pattern.finditer(text):
            # Zeilennummer ermitteln
            line_no = text[: match.start()].count("\n") + 1
            snippet = match.group(0)[:80].replace("\n", "↵")
            findings.append((line_no, snippet, label))

    # Deduplizieren (gleiche Zeile + Label)
    seen = set()
    unique = []
    for f in sorted(findings):
        key = (f[0], f[2])
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique


def get_staged_md_files() -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True
    )
    return [Path(p) for p in result.stdout.splitlines() if p.endswith(".md")]


def get_all_md_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "*.md"],
        capture_output=True, text=True
    )
    return [Path(p) for p in result.stdout.splitlines()]

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]

    if "--staged" in args:
        files = get_staged_md_files()
        mode = "staged"
    elif "--all" in args:
        files = get_all_md_files()
        mode = "alle"
    else:
        files = [Path(a) for a in args if a.endswith(".md")]
        mode = "explizit"

    if not files:
        print(f"[injection_scan] Keine .md-Dateien zu prüfen ({mode}).")
        sys.exit(0)

    total_findings = 0
    flagged_files = 0

    for path in files:
        if not path.exists():
            continue
        findings = scan_file(path)
        if findings:
            flagged_files += 1
            total_findings += len(findings)
            print(f"\n⚠️  {path}")
            for line_no, snippet, label in findings:
                print(f"   Zeile {line_no:4d} | {label}")
                print(f"             → {snippet!r}")

    if total_findings == 0:
        print(f"[injection_scan] ✓ Sauber — {len(files)} Datei(en) geprüft.")
        sys.exit(0)
    else:
        print(f"\n[injection_scan] ✗ {total_findings} Fund(e) in {flagged_files} Datei(en).")
        print("Commit abgebrochen. Bitte Dateien prüfen und bereinigen.")
        sys.exit(1)


if __name__ == "__main__":
    main()
