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

### 3 — Mnemosyne: Persona laden oder einrichten
```bash
test -f .mnemosyne.md && cat .mnemosyne.md || echo "no-profile"
```

**`profile-exists`:** Datei lesen, Nutzer mit Name ansprechen, in bevorzugter Sprache kommunizieren, Präferenzen beachten.

Wenn `notify_new_notes: true` gesetzt ist:
```bash
git log --oneline --since="7 days ago" -- content/ | head -10
```
Neue Notes gegen `interests` abgleichen. Bei Treffern kurz empfehlen:
> *„Hey [Name], letzte Woche ist eine Note reingekommen, die dich interessieren könnte: [[Titel]] — [Einzeiler]. Soll ich kurz zusammenfassen?"*

**`no-profile` (und kein `.claude/.no-profile`):** Onboarding starten — **eine Frage nach der anderen**, nicht alles auf einmal:

**Frage 1 — Vertrauen aufbauen:**
> *„Willkommen bei Gedankenwelten! 👋 Bevor wir loslegen — ich kann mir ein paar Dinge merken, damit ich besser mit dir arbeiten kann. Das bleibt alles lokal bei dir auf dem Rechner, wird nicht geteilt und nicht committed. Darf ich dir drei kurze Fragen stellen?"*

Bei Nein: Respektieren, `.claude/.no-profile` erstellen, nie wieder fragen. Weiter mit Schritt 4.

**Frage 2 — Name & Sprache:**
> *„Wie heißt du? Und in welcher Sprache möchtest du am liebsten arbeiten?"*

Choices anbieten: Deutsch, English, Français, Español, andere.

**Frage 3 — Interessen:**
> *„Was interessiert dich? Einfach ein paar Stichworte oder einen Satz — ich merke mir das und kann dir passende Notes empfehlen. Zum Beispiel: Klimapolitik, Philosophie, KI, Demokratie..."*

Freitext — kompakt als Tags speichern.

**Frage 4 — Benachrichtigungen:**
> *„Soll ich dich am Anfang einer Session darauf hinweisen, wenn neue Notes reingekommen sind, die zu deinen Interessen passen?"*

Choices: Ja, gerne / Nein danke.

Dann `.mnemosyne.md` erstellen:
```markdown
---
name: [Vorname]
language: [de/en/fr/es/...]
interests: [klimapolitik, philosophie, ki]
notify_new_notes: [true/false]
---

# Mnemosyne

> Göttin der Erinnerung, Mutter der Musen.
> Diese Datei speichert dein persönliches Profil — lokal, nicht committed.

## Erinnerungen
<!-- Via "merke dir das bitte" ergänzen -->
```

### „Merke dir das" — Remember-Skill
Wenn der Nutzer sagt *„merke dir das"*, *„remember this"*, *„notier dir"* oder ähnliches:
1. `.mnemosyne.md` öffnen (erstellen falls nicht vorhanden)
2. Unter `## Erinnerungen` als Bullet-Point ergänzen: `- **[DD.MM.YYYY]** Inhalt`
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
