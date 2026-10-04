---
name: geistesblitzumzug
description: "Zieht bestehende Zeitgeist-Notes mit zeitlos-wissenschaftlichem Kern in die Rubrik Geistesblitz um. Schlägt 10 Kandidaten vor, der User wählt aus, dann vollständiger Umzug inkl. Tag, Backlinks, Katalog, RAG, Deploy. Trigger: '/geistesblitzumzug', 'geistesblitz umzug', 'notes nach geistesblitz'."
---

# /geistesblitzumzug — Notes nach Geistesblitz umziehen

Findet Notes, die fälschlich in **Zeitgeist** liegen, aber nach **Geistesblitz**
gehören, schlägt **10 Kandidaten** vor, und zieht die vom User ausgewählten
*vollständig und bruchfrei* um — Datei, Tag, Backlinks, Katalog, RAG, Deploy.

> [!note] Quelle ist nur noch **Zeitgeist**
> Aus **Denker** ist genug umgezogen (Stand 09.06.2026) — die Rubrik bleibt jetzt
> stabil. Kandidaten kommen ausschließlich aus `Zeitgeist/`. Die Umzugs-Mechanik
> (Phase 2) bleibt trotzdem generisch und fixt auch alte `[[Denker/…]]`-Backlinks,
> falls noch welche auftauchen.

> **Geistesblitz** = grundsätzliches Wissen & menschliche Schöpferkraft
> (Wissenschaft, Philosophie, Psychologie, Technik). Notes, deren Kern eine
> **zeitlose Frage über die Welt oder den menschlichen Geist** ist — nicht
> tagesaktuell (→ Zeitgeist). Siehe `.claude/rules/gedankenwelten.md` § Geistesblitz.

> [!important] Geistesblitz *erklärt*, Denker *ergreift*
> Die Grenze zu **Denker** ist **nicht** „Person vs. Wissen". Denker ist der
> *tiefste* Bereich — Worte, die einen ergreifen und etwas in einem erschaffen,
> nicht nur informieren; das kann auch ein Kollektiv oder ein Text sein. Eine
> Note gehört in **Geistesblitz**, wenn sie die Welt *erklärt* (Forschungsstand,
> Wahrnehmung, Gehirn, klares Wissen, das den Funken im Menschen sichtbar macht);
> in **Denker**, wenn sie an der Wurzel *packt* und verwandelt. **Nie reflexhaft
> „Wissenschaftler:in → Geistesblitz" routen** — erst fragen: erklärt sie (auch
> brillant) oder ergreift sie? Es darf verschwimmen, keine pedantische
> Trennschärfe nötig.

## Phase 1 — 10 Kandidaten vorschlagen

1. Notes listen (**nur Zeitgeist** — Denker ist abgeschlossen):
   ```bash
   ls "content/Zeitgeist/"
   ```
2. **10 Kandidaten** auswählen, deren Kern eine zeitlose Welt-/Geist-Frage ist —
   eine Note, die die Welt *erklärt* statt das Jetzt zu kommentieren:
   - **Gute Kandidaten:** Bewusstsein, Wahrnehmung, Gehirn/Neurowissenschaft,
     Kognition, Physik, Biologie, Psychologie als Forschungsstand,
     Wissenschafts-Dokus/Erklärformate.
   - **Im Zweifel raus lassen:** tagesaktueller Diskurs, Politik, Interviews
     zum Geschehen — die bleiben **Zeitgeist**. Faustregel: *Was überdauert das
     Jahr → Geistesblitz; was kommentiert das Jetzt → Zeitgeist.*
   - **Nicht nach Denker schieben wollen:** Denker ist nicht das Ziel dieses
     Skills. Wenn eine Zeitgeist-Note dich an der Wurzel *ergreift* (verwandelnde
     Tiefe, nicht bloß brillante Erklärung), gehört sie eher nach Denker — das
     dann aber **explizit mit dem User klären**, nicht in diesem Lauf miterledigen.
3. Als **Tabelle** präsentieren (Note · Herkunft · *warum* Geistesblitz) + ein
   paar „weitere Kandidaten zum Tauschen". **Der User wählt aus** — nie
   ungefragt umziehen. Echtes Urteil zeigen, keine Pro-forma-Liste.

## Phase 2 — Umzug der ausgewählten Notes

Für **jede** gewählte Note die folgenden Schritte. Mehrere Notes gemeinsam
verarbeiten ist effizienter (ein Commit, ein Deploy).

### 2.1 Datei verschieben (Historie erhalten)
```bash
cd <vault>/Gedankenwelten
git mv "Zeitgeist/<Datei>.md" "Geistesblitz/<Datei>.md"   # bzw. Denker/
```

### 2.2 Typ-Tag umstellen
Im Frontmatter den Typ-Tag ändern: `zeitgeist` **oder** `denker` → `geistesblitz`.
Fehlt ein Typ-Tag ganz (manche alte Denker-Notes fangen direkt mit `philosophie`
an), `  - geistesblitz` als **erste** Tag-Zeile einfügen. Andere Tags bleiben.
Danach kontrollieren:
```bash
for f in Geistesblitz/*.md; do echo -n "$f: "; awk '/^tags:/{p=1;next} p&&/^  - /{print $2; exit}' "$f"; done
```

### 2.2b Alias auf den alten Pfad setzen (SEO-Redirect) ⚠️ Pflicht
Die alte öffentliche URL (`gedankenwelten.org/Zeitgeist/<Slug>` bzw. `/Denker/<Slug>`)
würde nach dem Umzug 404 liefern — Google meldet das als Indexierungsfehler, und extern
gesetzte Links sterben. Quartz' **AliasRedirects-Plugin** (aktiv) baut aus einem Alias
eine Redirect-Seite an der alten URL. Darum bekommt **jede** umgezogene Note im
Frontmatter einen Alias mit dem **alten Pfad** (exakter alter Dateiname ohne `.md`,
relativ zur Rubrik-Ebene):

```yaml
aliases:
  - "Zeitgeist/<alter Dateiname ohne .md>"   # bzw. Denker/…
```

Existiert schon ein `aliases:`-Block (Obsidian-Aliase), den Pfad-Alias **anhängen**,
nicht ersetzen. In Anführungszeichen setzen (Em-Dashes/Sonderzeichen). Gilt sinngemäß
für **jede** Umbenennung öffentlicher Notes, nicht nur Rubrik-Umzüge.

### 2.3 Backlinks nachziehen ⚠️ KRITISCH
**Bare Links** (`[[Titel]]`) brauchen nichts — Quartz löst über den Dateinamen
auf. **Path-qualifizierte Links** (`[[Zeitgeist/Titel]]`, `[[Denker/Titel]]`,
`[[content/Denker/Titel]]`) zeigen nach dem Move ins Leere und **müssen**
auf `Geistesblitz/` umgeschrieben werden — quer durch den ganzen Vault
(Quellen & Links.md, DenkerVitas, Querverweise zwischen Notes, Vipassana …).

> **NIEMALS** mit einem generischen Regex arbeiten, das `[[Denker/` /
> `[[Zeitgeist/` *unabhängig vom Titel* ersetzt — das reißt Prefixe aus
> hunderten unbeteiligter Links (in diesem Umzug einmal passiert, Quellen &
> Links.md mit 326 zerstörten Zeilen). **Nur** die konkreten Titel matchen.

Sicheres Python-Skript (Titelliste = die gerade verschobenen Notes, **ohne**
`.md`, mit echten Umlauten wie im Dateinamen):
```bash
cd <vault>/Gedankenwelten
/opt/homebrew/bin/python3 - <<'PY'
import re, glob
titles = [
    "Albert Moukheiber — Mein Hirn und die anderen",   # längere zuerst,
    "Albert Moukheiber — Mein Hirn und ich",            # falls Titel Präfix voneinander sind
    # … hier die tatsächlich verschobenen Titel eintragen …
]
alt = "|".join(re.escape(t) for t in titles)
pat = re.compile(r'(\[\[(?:Gedankenwelten/)?)(?:Zeitgeist|Denker)/(' + alt + r')')
total = 0
for f in glob.glob("**/*.md", recursive=True):
    s = open(f, encoding="utf-8").read()
    new, n = pat.subn(lambda m: m.group(1) + "Geistesblitz/" + m.group(2), s)
    if n:
        open(f, "w", encoding="utf-8").write(new)
        print(f"{n:2d}  {f}"); total += n
print(f"--- {total} Links gefixt ---")
PY
```
Danach **verifizieren** — jede entfernte Diff-Zeile muss `Zeitgeist/` oder
`Denker/` enthalten, jede hinzugefügte `Geistesblitz/`:
```bash
cd <vault>/
git diff -- Gedankenwelten/ | grep -E '^-' | grep -v '^---' | grep -vE 'Zeitgeist/|Denker/' | grep -c '\[\['  # = 0
git diff -- Gedankenwelten/ | grep -E '^\+' | grep -v '^+++' | grep -vE 'Geistesblitz/' | grep -c '\[\['        # = 0
```
Ist die Zahl ≠ 0 → `git checkout -- Gedankenwelten/` (verwirft nur den
uncommitteten Link-Batch, die Moves waren ggf. schon committet) und sauber neu.

### 2.4 Katalog `Gedankenwelten.md` umhängen
Der Katalog gruppiert **thematisch**, nicht nach Ordner — Zeitgeist-Notes können
im Denker-Block stehen. Pro Note:
- Eintrag aus seinem aktuellen Block **entfernen** (Titel suchen).
- In der `## Geistesblitz`-Sektion **einfügen** (Format: `- [[Titel]] | tags | Teaser` —
  Typ-Tag `zeitgeist`/`denker` aus dem Teaser-Tag-Listing strippen).
- Manche Notes haben **gar keinen** Katalog-Eintrag (dann nur neu anlegen).
- **Zählungen** aktualisieren (Bullet-Counts je Sektion):
  - Quell-Sektion `## Denker (N)` / `## Zeitgeist (N)` → minus entfernte Einträge
  - `## Geistesblitz (N)` → `ls Geistesblitz/*.md | wc -l`
  - Fußzeile `*Zuletzt aktualisiert: <heute> — … = 300 Notes*`: Geistesblitz hoch,
    Zeitgeist/Denker um die je-Ordner verschobene Anzahl runter (Gesamt bleibt gleich).

### 2.5 RAG re-ingest (geänderte Rubrik-Metadaten)
```bash
cd <vault>/Gedankenwelten
bash ../.claude/scripts/ingest_notes.sh "Geistesblitz/<Datei1>.md" "Geistesblitz/<Datei2>.md" …
```
Endpoint ist `…/webhook/ingest-gedankenwelten` (NIE `/ingest` = private Collection).

### 2.6 Cortex-Log
`notes-migrated`-Eintrag oben in `Cortex-Log.md` (neueste oben), mit Liste der
migrierten Zeitgeist-Notes.

### 2.7 Commit, Push, Cortex-Wiki rebuilden
```bash
cd <vault>/
git add -A && git commit -m "geistesblitz: <N> Notes aus Zeitgeist migriert"
git push origin main
ssh <server> "~/services/cortex/scripts/pull-and-rebuild.sh"
```

### 2.8 Public Sync nach gedankenwelten.org
```bash
<vault>/.claude/scripts/sync-from-cortex.sh
```
Das Skript hat `--delete` (+ `protect index.md`) — es **räumt die alten
Public-Kopien in Zeitgeist/Denker selbst auf**. Trotzdem kurz verifizieren:
```bash
cd ~/Gedankenwelten/content
ls Geistesblitz/*.md | wc -l        # = neue Gesamtzahl
ls "Zeitgeist/<verschobener-Titel>"* "Denker/<verschobener-Titel>"* 2>&1 | grep -v "no matches"  # leer
```

### 2.9 Abschluss
- **Cloudflare-Cache purgen** erwähnen (CSS/Pages erscheinen sonst verzögert) —
  **der User macht das selbst**.
- Note im Browser prüfen anbieten:
  ```bash
  open -a Firefox "https://gedankenwelten.org/Geistesblitz/<Datei-ohne-.md>"
  ```

## Fallstricke (aus echten Umzügen)
- **Backlink-Regex:** nur konkrete Titel matchen, nie generisches `[[Denker/`-Strip (s. 2.3).
- **`--delete` & public-only Dateien:** `content/<Rubrik>/index.md` sind
  Quartz-Landingpages, die **nur** im Public-Repo leben. Der `protect index.md`-
  Filter im Sync bewahrt sie — falls doch mal eine verschwindet:
  `cd ~/Gedankenwelten && git checkout <commit~1> -- content/<Rubrik>/index.md`.
- **`aktualisiert:` der Altnotes NICHT anfassen** beim Backlink-Fix — sonst
  spülen sie fälschlich ins Startseiten-Journal hoch.
- **Dateinamen:** beim (seltenen) Umbenennen Konventionen halten — ä/ö/ü →
  ae/oe/ue, kein `:`, einfacher Bindestrich statt Em-Dash. Move ohne Umbenennen
  ist der Normalfall, dann irrelevant.
