#!/usr/bin/env python3
"""
injection_scan.py — Prompt Injection Scanner für Markdown-Dateien

Erkennt versteckten Text und Injection-Versuche in .md-Dateien.

Zwei Schweregrade:
  HARD  — strukturelle Tarnung, die in einer echten Note nie legitim vorkommt
          (unsichtbarer Text, Zero-Width, Tag-Chars, Bidi-Override, HTML-Kommentare).
          → Blockiert (Exit-Code 1).
  WARN  — verdächtige Klartext-Muster (Injection-Phrasen, Base64-Blobs).
          Kann in legitimen Notes über KI-Sicherheit auftauchen.
          → Nur Hinweis, blockiert NICHT.

Verwendung:
  python3 injection_scan.py file1.md file2.md ...
  python3 injection_scan.py --staged        # nur git-staged .md-Dateien
  python3 injection_scan.py --all           # alle .md-Dateien im Repo
  python3 injection_scan.py --strict ...    # auch WARN-Funde blockieren

Exit-Code: 0 = keine HARD-Funde, 1 = mindestens ein HARD-Fund (bzw. WARN bei --strict)
"""

import re
import sys
import subprocess
from pathlib import Path

HARD = "HARD"
WARN = "WARN"

# ---------------------------------------------------------------------------
# Muster — (Regex, Label, Schweregrad)
# ---------------------------------------------------------------------------

PATTERNS = [
    # --- HARD: strukturelle Tarnung, nie legitim in einer Note -------------

    # HTML-Kommentare — primäres Versteck für unsichtbare Anweisungen
    (r"<!--[\s\S]*?-->", "HTML-Kommentar", HARD),

    # Unsichtbare Styles — Farbe
    (r'style=["\'][^"\']*color\s*:\s*(white|#fff(?:fff)?|rgb\(255\s*,\s*255\s*,\s*255\))[^"\']*["\']',
     "Unsichtbarer Text (weiße Schriftfarbe)", HARD),

    # Unsichtbare Styles — Schriftgröße
    (r'style=["\'][^"\']*font-size\s*:\s*[01](?:\.\d+)?px[^"\']*["\']',
     "Unsichtbarer Text (Schriftgröße ≤ 1px)", HARD),

    # display:none / visibility:hidden
    (r'style=["\'][^"\']*(?:display\s*:\s*none|visibility\s*:\s*hidden)[^"\']*["\']',
     "Verstecktes Element (display:none / visibility:hidden)", HARD),

    # Zero-width Unicode-Zeichen
    # (U+00AD Soft Hyphen bewusst NICHT enthalten — legitimes Trennzeichen in dt. Text)
    (r"[​‌‍⁠﻿]",
     "Zero-Width / unsichtbares Unicode-Zeichen", HARD),

    # Unicode Tag Characters (U+E0000–U+E007F) — komplett unsichtbar,
    # modernste Form versteckter Anweisungen
    (r"[\U000E0000-\U000E007F]",
     "Unicode Tag Character (unsichtbare Steueranweisung)", HARD),

    # Bidi-Override (Trojan Source) — kehrt Leserichtung um, verbirgt Text
    (r"[‪-‮⁦-⁩]",
     "Bidi-Override (Trojan-Source-Zeichen)", HARD),

    # --- WARN: verdächtiger Klartext, kann legitim sein --------------------

    (r"(?i)ignore\s+(all\s+)?previous\s+instructions?",
     "Injection-Phrase: 'ignore previous instructions'", WARN),
    (r"(?i)\bnew\s+instruction[s:]",
     "Injection-Phrase: 'new instruction'", WARN),
    (r"(?i)\bsystem\s*:\s*(update|override|priority)",
     "Injection-Phrase: 'system: update/override'", WARN),
    (r"(?i)\bpriority\s+override\b",
     "Injection-Phrase: 'priority override'", WARN),
    (r"(?i)you\s+are\s+now\s+(?:a|an)\s+\w+\s+(?:assistant|ai|model)",
     "Injection-Phrase: 'you are now a ... assistant'", WARN),
    (r"(?i)disregard\s+(all\s+)?(?:previous|prior|earlier)\s+(?:instructions?|context|rules?)",
     "Injection-Phrase: 'disregard previous instructions'", WARN),
    (r"(?i)\bDAN\b.*no\s+restrictions?",
     "Injection-Phrase: DAN-Muster", WARN),

    # Base64-Blob — langer zusammenhängender Token, der eine Payload tarnen
    # könnte. Schwelle hoch gehalten, da WARN ohnehin nur informiert.
    (r"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{120,}={0,2}(?![A-Za-z0-9+/])",
     "Möglicher Base64-Blob (encodierte Payload?)", WARN),
]

COMPILED = [(re.compile(p), label, sev) for p, label, sev in PATTERNS]

# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def scan_file(path: Path) -> list[tuple[int, str, str, str]]:
    """Gibt Liste von (Zeilennummer, Treffer, Label, Schweregrad) zurück."""
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  [FEHLER] Kann {path} nicht lesen: {e}", file=sys.stderr)
        return findings

    for pattern, label, sev in COMPILED:
        for match in pattern.finditer(text):
            line_no = text[: match.start()].count("\n") + 1
            snippet = match.group(0)[:80].replace("\n", "↵")
            findings.append((line_no, snippet, label, sev))

    # Deduplizieren (gleiche Zeile + Label)
    seen = set()
    unique = []
    for f in sorted(findings, key=lambda x: (x[0], x[2])):
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
    strict = "--strict" in args

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

    hard_count = 0
    warn_count = 0
    flagged_files = 0

    for path in files:
        if not path.exists():
            continue
        findings = scan_file(path)
        if findings:
            flagged_files += 1
            print(f"\n  {path}")
            for line_no, snippet, label, sev in findings:
                if sev == HARD:
                    hard_count += 1
                    tag = "⛔ BLOCK"
                else:
                    warn_count += 1
                    tag = "⚠️  WARN "
                print(f"   {tag} Zeile {line_no:4d} | {label}")
                print(f"                  → {snippet!r}")

    print()
    if hard_count == 0 and warn_count == 0:
        print(f"[injection_scan] ✓ Sauber — {len(files)} Datei(en) geprüft.")
        sys.exit(0)

    print(f"[injection_scan] {hard_count} BLOCK · {warn_count} WARN "
          f"in {flagged_files} Datei(en).")

    blocking = hard_count > 0 or (strict and warn_count > 0)
    if blocking:
        print("Abgebrochen. BLOCK-Funde (oder --strict) müssen bereinigt werden.")
        sys.exit(1)
    else:
        print("Nur WARN-Funde — Durchlauf nicht blockiert. Bitte trotzdem prüfen.")
        sys.exit(0)


if __name__ == "__main__":
    main()
