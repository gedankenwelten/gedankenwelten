# CLAUDE.md — Gedankenwelten

@.claude/rules/gedankenwelten.md
@.claude/rules/pipeline.md
@.claude/rules/tags.md

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
docker compose up   # → http://localhost:8080 (Auto-Rebuild bei Dateiänderungen)
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
