# CLAUDE.md — Gedankenwelten

@.claude/rules/gedankenwelten.md
@.claude/rules/pipeline.md
@.claude/rules/tags.md
@.claude/rules/setup.md

---

## Session-Start

Beim ersten Message des Users in einer neuen Session:

```bash
test -f .claude/.welcomed && echo "returning" || echo "new"
```

**`new` (Datei fehlt — frischer Clone):**
Den User willkommen heißen. Kurz erklären was Gedankenwelten ist, was hier entsteht und wie man loslegt. Auf `/gedankenwelten-note-pipeline` und `docker compose up` hinweisen. Fragen womit er starten möchte. Danach die Datei anlegen:
```bash
touch .claude/.welcomed
```

**`returning` (Datei existiert):** Direkt in die Arbeit — kein Begrüßungs-Overhead.

---

## Projektstruktur

```
content/
  Denker/       Zeitgeist/    DenkerVita/
  Panorama/     Gedanken/     Vipassana/
  Transkripte/  known-speakers.md   Quellen & Links.md
```

## Lokale Wiki

```bash
docker compose up   # → http://localhost:9999 (Auto-Rebuild bei Dateiänderungen)
```

## Skills & Agenten

| Befehl | Aufgabe |
|---|---|
| `/gedankenwelten-note-pipeline` | Neue Note aus YouTube / Podcast / Artikel |
| `/aristoteles` | Tiefenanalyse ab Transkript (Schritt 5 der Pipeline) |
| `/heraklit` | Bestehende Note vertiefen |
| `/agent humboldt` | Sprecher recherchieren, DenkerVita anlegen |
| `/agent sherlock` | Faktencheck mit Quellenverifikation |
| `/agent montaigne` | Cross-Linking zwischen Notes |

## Commit-Konvention

```bash
git add -A && git commit -m "note-pipeline: Autor — Thema" && git push
```
