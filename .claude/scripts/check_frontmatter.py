#!/usr/bin/env python3
"""check_frontmatter.py — Frontmatter-YAML-Validator für Gedankenwelten-Notes.

Fängt die Fehlerklasse ab, die einen ganzen Quartz-Build abbrechen lässt:
ungültiges YAML in der Frontmatter (z.B. ein gerades " inmitten eines
"…"-gequoteten title:, das den String vorzeitig beendet).

Aufruf:
    # gezielt eine oder mehrere Dateien
    python3 .claude/scripts/check_frontmatter.py "content/Zeitgeist/Foo.md"

    # alle in git geänderten/neuen .md-Notes (Standard, ideal vor dem Commit)
    python3 .claude/scripts/check_frontmatter.py

Exit-Code 0 = sauber, 1 = mindestens ein Fehler (Commit stoppen).
"""
import datetime
import re
import subprocess
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML fehlt — `pip3 install pyyaml`")

TODAY = datetime.date.today()
# Wie alt darf `date:` einer brandneuen Note höchstens sein, bevor gewarnt wird?
# (Fängt den Klassiker ab: Quelldatum des Videos/Podcasts statt Verarbeitungstag.)
DATE_STALE_DAYS = 10


def _parse_date(s):
    s = (s or "").strip().strip('"').strip("'")
    for fmt in ("%d.%m.%Y", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None

FM_RE = re.compile(r"(?s)\A---\n(.*?)\n---")
# Gerades ASCII-Quote, das NICHT am Wert-Anfang/-Ende steht (also mitten im String)
# Wir prüfen das pragmatisch über den YAML-Parser; diese Heuristik liefert nur den Hinweis.


def changed_notes():
    """Alle in git geänderten/gestageten/neuen .md-Dateien unter Gedankenwelten/.

    Nutzt `-z` (NUL-getrennt) — sonst quotet git Pfade mit Sonderzeichen
    (Em-Dash, Umlaute, Komma) in "…" mit Oktal-Escapes, was bei praktisch
    JEDER Gedankenwelten-Note zugeschlagen und den Filter unterlaufen hätte.
    """
    out = set()
    for args in (["diff", "-z", "--name-only", "HEAD"],
                 ["ls-files", "-z", "--others", "--exclude-standard"]):
        try:
            res = subprocess.run(["git", *args], capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError:
            continue
        for path in res.stdout.split("\0"):
            if path.startswith("Gedankenwelten/") and path.endswith(".md"):
                out.add(path)
    return sorted(out)


def untracked_notes():
    """Nur die im Repo noch NICHT getrackten (= brandneuen) Gedankenwelten-Notes."""
    out = set()
    try:
        res = subprocess.run(["git", "ls-files", "-z", "--others", "--exclude-standard"],
                             capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError:
        return out
    for path in res.stdout.split("\0"):
        if path.startswith("Gedankenwelten/") and path.endswith(".md"):
            out.add(path)
    return out


def date_warning(path):
    """Soft-Hinweis (nicht fatal): brandneue Note mit `date:` weit in der Vergangenheit.

    `date:` ist die autoritative Sortier-Quelle für Journal UND Karten-Feed und soll
    der VERARBEITUNGSTAG sein (nicht das Quelldatum des Videos/Podcasts). Sitzt hier
    versehentlich das alte Quelldatum, sinkt die frische Note im Feed nach unten.
    """
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return None
    m = re.search(r"^date:\s*(.+)$", text, re.M)
    if not m:
        return None
    d = _parse_date(m.group(1))
    if d and (TODAY - d).days > DATE_STALE_DAYS:
        return (f"`date: {m.group(1).strip()}` liegt {(TODAY - d).days} Tage zurück — "
                f"ist das versehentlich das Quelldatum statt des Verarbeitungstags ({TODAY:%d.%m.%Y})? "
                f"Der Feed sortiert nach `date:`; eine frische Note sinkt sonst nach unten.")
    return None


def check(path):
    """Gibt eine Fehlermeldung zurück oder None, wenn alles ok ist."""
    try:
        text = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        return f"Datei nicht gefunden: {path}"
    m = FM_RE.match(text)
    if not m:
        return f"Keine Frontmatter (--- … ---) am Dateianfang gefunden."
    fm = m.group(1)
    try:
        data = yaml.safe_load(fm)
    except yaml.YAMLError as e:
        hint = ""
        # Häufigste Ursache: gerades " in einem "…"-gequoteten Wert
        for ln in fm.splitlines():
            if ln.lstrip().startswith(("title:", "description:")) and ln.count('"') > 2:
                hint = (f"\n  → Verdacht: gerades \" mitten im Wert — "
                        f"geschweifte „…“ verwenden oder Wert in '…' setzen:\n    {ln.strip()}")
                break
        return f"YAML-Fehler in der Frontmatter:\n  {str(e).splitlines()[0]}{hint}"
    if not isinstance(data, dict):
        return "Frontmatter parst nicht zu einem Mapping (key: value)."
    if not data.get("title"):
        return "Pflichtfeld `title:` fehlt oder ist leer."
    return None


def main():
    paths = sys.argv[1:] or changed_notes()
    if not paths:
        print("check_frontmatter: keine geänderten Notes — nichts zu prüfen.")
        return 0
    errors = 0
    for p in paths:
        err = check(p)
        if err:
            errors += 1
            print(f"✗ {p}\n  {err}\n")
    if errors:
        print(f"check_frontmatter: {errors} Datei(en) mit Frontmatter-Fehlern — Commit stoppen, erst fixen.")
        return 1
    # Soft-Hinweis (blockt nicht): brandneue Notes mit verdächtig altem date:
    fresh = untracked_notes()
    for p in paths:
        if p in fresh:
            w = date_warning(p)
            if w:
                print(f"⚠ {p}\n  {w}\n")
    print(f"check_frontmatter: ✓ {len(paths)} Note(s) sauber.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
