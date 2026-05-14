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

### 2 — Docker-Status & Hook prüfen
```bash
docker ps --filter "name=gedankenwelten" --format "{{.Names}} {{.Status}}" 2>/dev/null
```
- **Läuft:** Wiki ist unter http://localhost:9999 erreichbar.
- **Läuft nicht:** Hinweis geben: `docker compose up -d` startet die Wiki im Hintergrund.

```bash
test -f .git/hooks/post-merge && echo "hook-ok" || echo "hook-missing"
```
- **hook-ok:** Nichts tun.
- **hook-missing:** `./scripts/rebuild.sh` ausführen — installiert den Hook automatisch und rebuildet die Wiki. Kurz erklären: *„Hab den Auto-Rebuild-Hook installiert — ab jetzt rebuildet die Wiki nach jedem git pull automatisch."*

### 2b — Rebuild nach neuen Notes
Nach jeder Note-Erstellung oder Sync: Wiki rebuilden.
```bash
./scripts/rebuild.sh
```

### 3 — Persona laden oder einrichten
```bash
test -f .mnemosyne.md && echo "profile-exists" || echo "no-profile"
```

**`profile-exists`:** Datei lesen, Nutzer mit Name ansprechen, Präferenzen beachten.

**`no-profile`:** Freundlich fragen:
> *„Hey! Ich kann mir merken, wie du heißt, welche Sprache du bevorzugst und was dich interessiert — das macht die Zusammenarbeit persönlicher. Soll ich ein kurzes Profil anlegen?"*

Bei Ja: Name, Sprache und Interessen abfragen, `.mnemosyne.md` erstellen. Template:
```markdown
---
name: [Vorname]
language: [de/en]
style: direkt
---

# Persönliches Profil

## Interessen
[Was beschäftigt den Nutzer? Welche Themen, Denker, Perspektiven?]

## Erinnerungen
<!-- Via "merke dir das bitte" ergänzen -->
```

Bei Nein: Respektieren, nicht nochmal fragen. `.claude/.no-profile` erstellen.

### „Merke dir das" — Remember-Skill
Wenn der Nutzer sagt *„merke dir das"*, *„remember this"* oder ähnliches:
1. `.mnemosyne.md` öffnen (erstellen falls nicht vorhanden)
2. Unter `## Erinnerungen` als Bullet-Point ergänzen mit Datum
3. Kurz bestätigen: *„Notiert ✓"*

### 4 — Willkommen oder direkt arbeiten
```bash
test -f .claude/.welcomed && echo "returning" || echo "new"
```

**`new` (frischer Clone):**
Kurz willkommen heißen — wenn Profil vorhanden, mit Namen. Erklären was Gedankenwelten ist. Auf `/gedankenwelten-note-pipeline` hinweisen. Den Fork-Workflow erwähnen (PR auf GitHub). Fragen womit gestartet werden soll. Dann:
```bash
touch .claude/.welcomed
```

**`returning`:** Direkt in die Arbeit. Wenn Profil vorhanden: kurz mit Namen grüßen, dann arbeiten.

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
docker compose up -d     # → http://localhost:9999
./scripts/rebuild.sh     # Wiki neu bauen (nach git pull oder neuer Note)
```

Nach `git pull` wird automatisch rebuilt, wenn der Hook installiert ist:
```bash
./scripts/setup-hooks.sh   # einmalig nach Clone/Fork
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
