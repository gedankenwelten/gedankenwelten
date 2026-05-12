# CLAUDE.md — Gedankenwelten

@.claude/rules/gedankenwelten.md
@.claude/rules/pipeline.md
@.claude/rules/tags.md
@.claude/rules/setup.md

---

## Session-Start

Beim ersten Message des Users in einer neuen Session folgende Schritte **immer ausführen**:

### 1 — Git Pull
```bash
git pull --ff-only origin main 2>&1 | tail -3
```
Wenn neue Commits: kurz melden welche Notes neu sind (`git log --oneline ORIG_HEAD..HEAD -- content/`).

### 2 — Docker-Status prüfen
```bash
docker ps --filter "name=gedankenwelten" --format "{{.Names}} {{.Status}}" 2>/dev/null
```
- **Läuft:** Wiki ist unter http://localhost:9999 erreichbar — neue Notes erscheinen automatisch.
- **Läuft nicht:** Hinweis geben: `docker compose up -d` startet die Wiki im Hintergrund.

### 3 — Willkommen oder direkt arbeiten
```bash
test -f .claude/.welcomed && echo "returning" || echo "new"
```

**`new` (frischer Clone):**
Kurz willkommen heißen. Erklären was Gedankenwelten ist. Auf `/gedankenwelten-note-pipeline` hinweisen. Den Fork-Workflow erwähnen (PR auf GitHub). Fragen womit gestartet werden soll. Dann:
```bash
touch .claude/.welcomed
```

**`returning`:** Direkt in die Arbeit — kein Begrüßungs-Overhead.

---

## Community & Fork-Workflow

Gedankenwelten ist ein offenes Projekt. Das Modell:
- Nutzer **forken** das Repo, erstellen Notes mit der Pipeline, öffnen einen **Pull Request**
- Der Maintainer reviewed und merged
- Qualitätskriterien: Aristoteles-Standard, Faktencheck, Quellen verlinkt

Wenn ein Nutzer eine neue Note erstellt hat und fragt wie er sie einreichen soll:
→ `git push` in seinen Fork + PR auf `github.com/gedankenwelten/gedankenwelten` öffnen.

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
| `/sokrates` | Frageschicht ergänzen — Gegenfragen, Widersprüche, Kernthesen herausfordern |
| `/heraklit` | Bestehende Note vertiefen |
| `/agent humboldt` | Sprecher recherchieren, DenkerVita anlegen |
| `/agent sherlock` | Faktencheck mit Quellenverifikation |
| `/agent montaigne` | Cross-Linking zwischen Notes |

## Commit-Konvention

```bash
git add -A && git commit -m "note-pipeline: Autor — Thema" && git push
```
