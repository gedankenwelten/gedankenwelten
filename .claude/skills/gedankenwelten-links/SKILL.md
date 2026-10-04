---
name: gedankenwelten-links
description: "Wikilink-Audit für Gedankenwelten — prüft alle [[...]] Links, fixt automatisch was fixbar ist (fehlende Gedankenwelten/-Prefixes, bekannte Umbenennungen) und liefert einen klaren Report über was offen bleibt. Trigger: 'links prüfen', 'broken links', 'verlinkungen prüfen', 'link-audit', '/gedankenwelten-links'."
---

# gedankenwelten-links — Wikilink-Audit

Prüft alle `[[...]]`-Links in `Gedankenwelten/`, fixt was automatisch sicher fixbar ist, und liefert einen präzisen Report über den Rest.

---

## Was der Skill macht

| Schritt | Was passiert |
|---|---|
| **1. Scan** | `check_links.py` läuft über alle `.md` in `Gedankenwelten/` |
| **2. Auto-Fix: Prefixes** | `[[Zeitgeist/X]]` → `[[content/Zeitgeist/X]]` wenn Datei existiert |
| **3. Auto-Fix: Umbenennungen** | Bekannte Titelwechsel aus dem Reparatur-Log |
| **4. Report** | Was bleibt: fehlende DenkerVitas, fehlende Notes, absichtliche Vorwärts-Links |
| **5. Commit** | Nur wenn tatsächlich Fixes gemacht wurden |

---

## Schritt 1 — Validator ausführen

```bash
cd <vault>/
python3 .claude/scripts/check_links.py --dir Gedankenwelten --json 2>/dev/null > /tmp/gw_links.json
python3 .claude/scripts/check_links.py --dir Gedankenwelten 2>&1 | grep "❌\|✅\|📊"
```

Zahlen merken: wie viele broken links, wie viele Dateien.

---

## Schritt 2 — Auto-Fix: fehlende `Gedankenwelten/`-Prefixes

Links wie `[[Zeitgeist/X]]`, `[[Denker/X]]` etc. die tatsächlich auf eine existierende Datei unter `Gedankenwelten/` zeigen — Prefix ergänzen.

```python
# Inline-Fix (direkt ausführen):
python3 - << 'EOF'
import json, re, os, unicodedata
from pathlib import Path

def nfc(s): return unicodedata.normalize('NFC', s)

with open('/tmp/gw_links.json') as fp:
    data = json.load(fp)

fixed_count = 0
files_fixed = 0
for fe in data:
    fpath = Path(fe['file'])
    fixes = []
    for link in fe['links']:
        lc = link['link_clean']
        m = re.match(r'^(Denker|Zeitgeist|Panorama|Gedanken|DenkerVita|Vipassana)/', lc)
        if not m: continue
        gw_path = f'Gedankenwelten/{lc}.md'
        if os.path.exists(gw_path):
            old_str = f'[[{link["link"]}]]'
            lc_no_anchor = lc.split('#')[0]
            new_str = old_str.replace(f'[[{lc_no_anchor}', f'[[Gedankenwelten/{lc_no_anchor}', 1)
            if old_str != new_str:
                fixes.append((old_str, new_str))
    if fixes:
        content = fpath.read_text('utf-8')
        for old_str, new_str in fixes:
            if old_str in content:
                content = content.replace(old_str, new_str)
                fixed_count += 1
        fpath.write_text(content, 'utf-8')
        files_fixed += 1
        print(f"✅ {fpath.name} — {len(fixes)} links")
print(f"\nGesamt: {fixed_count} Links in {files_fixed} Dateien gefixt")
EOF
```

---

## Schritt 3 — Report: Was bleibt

Nach dem Auto-Fix nochmal scannen und kategorisieren:

```bash
python3 .claude/scripts/check_links.py --dir Gedankenwelten --json 2>/dev/null | python3 - << 'EOF'
import json, sys, re
from collections import Counter
data = json.load(sys.stdin)

missing_vitas, missing_notes, fwd_links, prefix_left, audio = [], [], [], [], []

for fe in data:
    for link in fe['links']:
        lc = link['link_clean']
        if '...' in lc or lc.endswith('.mp3') or lc.endswith('.vtt'):
            audio.append(lc)
            continue
        if lc.startswith('content/DenkerVita/'):
            missing_vitas.append(lc.split('/')[-1])
        elif lc.startswith('Gedankenwelten/'):
            missing_notes.append((fe['file'].split('/')[-1], lc.split('/')[-1]))
        elif re.match(r'^(Denker|Zeitgeist|Panorama|Gedanken|DenkerVita)/', lc):
            prefix_left.append((fe['file'].split('/')[-1], lc))
        elif '/' not in lc:
            fwd_links.append(lc)

print(f"=== FEHLENDE DENKERVITAS ({len(set(missing_vitas))}) ===")
for v in sorted(set(missing_vitas)):
    print(f"  → {v}")

print(f"\n=== FEHLENDE NOTES ({len(missing_notes)}) ===")
for f, n in sorted(set(missing_notes)):
    print(f"  [{f[:40]}] → {n}")

if prefix_left:
    print(f"\n=== NOCH OFFENE PREFIXES ({len(prefix_left)}) ===")
    for f, l in prefix_left[:10]:
        print(f"  [{f[:40]}] [[{l}]]")

print(f"\n=== VORWÄRTS-LINKS (absichtlich, {len(set(fwd_links))}) ===")
for l in sorted(set(fwd_links))[:15]:
    print(f"  [[{l}]]")
if len(set(fwd_links)) > 15:
    print(f"  ... und {len(set(fwd_links)) - 15} weitere")

print(f"\n=== AUDIO-LINKS ({len(set(audio))}) ===")
print("  (mp3/vtt — nicht prüfbar, ignoriert)")
EOF
```

---

## Schritt 4 — Commit (nur wenn Fixes gemacht)

Wenn Schritt 2 oder 3 Fixes produziert haben:

```bash
cd <vault>/
git add -A && git commit -m "fix: Wikilink-Audit — [N] broken links gefixt"
git push
```

---

## Ergebnis-Format

Abschlussmeldung immer in dieser Struktur:

```
✅ Auto-Fix: [N] Links in [M] Dateien korrigiert
   — fehlende Prefixes: X
   — Umbenennungen: Y

📋 Offen (kein Auto-Fix möglich):
   — [N] fehlende DenkerVitas: [Liste]
   — [N] fehlende Notes: [Titel]
   — [N] Vorwärts-Links (absichtlich, kein Handlungsbedarf)

🔗 Validator: python3 .claude/scripts/check_links.py --dir Gedankenwelten
```

---

## Wann zusätzlich den gesamten Vault prüfen

Für Opus, Journal, index.md etc.:

```bash
python3 .claude/scripts/check_links.py 2>&1 | grep "❌\|📊"
```

Ohne `--dir`-Flag läuft der Validator über alle 3.400+ Dateien — dauert ~10 Sekunden.

---

## Bekannte Falsch-Positives (nicht als broken werten)

| Link-Typ | Warum kein Fehler |
|---|---|
| `[[Marc Aurel]]`, `[[Viktor Frankl]]` ohne Pfad | Absichtliche Vorwärts-Links — zukünftige Notes |
| `[[Vipassana/Day01_...mp3]]` | Audio-Dateien — Obsidian rendert sie, Script nicht |
| `[[content/DenkerVita/...]]` Vita fehlt | Humboldt-Job — wird erstellt wenn Zeit |
| `[[...]]` mit `...` als Platzhalter | Template-Reste — absichtlich vage |
