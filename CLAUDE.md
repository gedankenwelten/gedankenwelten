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

**`profile-exists`:** Datei lesen, Nutzer mit Name ansprechen, in bevorzugter Sprache kommunizieren, Präferenzen beachten. Weiter mit Schritt 3b (GoodNews) und 3c (Notes).

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

## Gelesene News
<!-- Automatisch verwaltet — nicht manuell bearbeiten -->
```

### „Merke dir das" — Remember-Skill

→ Wird durch den Skill `.claude/skills/remember/SKILL.md` gesteuert.
Trigger: *„merke dir das"*, *„remember this"*, *„notier dir"*, *„das ist wichtig"*.
Security-Check inkludiert — keine Credentials speichern.

### „Gute Nachricht" — Epikur-Skill

→ Wird durch den Skill `.claude/skills/epikur/SKILL.md` gesteuert.
Trigger: *„gute nachricht"*, *„goodnews"*, *„epikur"*, *„ich hab was positives"*.
Gesprächsweise Begleitung → Verdichtung → Cross-Links zu Notes, Denkern, DenkerVita → Datei in `project-news/`.

### 3b — GoodNews prüfen
```bash
ls project-news/*.md 2>/dev/null | grep -v README
```
Ungelesene News ermitteln: Alle `.md`-Dateien in `project-news/` (außer README.md) abgleichen gegen `## Gelesene News` in `.mnemosyne.md`.

**Ungelesene vorhanden:** Kompakt anzeigen:
```
🌱 [Anzahl] neue GoodNews aus der Community
```

Auf Nachfrage: Titel und Kurzinhalt zeigen, dann in `.mnemosyne.md` unter `## Gelesene News` eintragen:
```markdown
- YYYY-MM-DD-kurztitel.md
```

**Archivierung:** Wenn News älter als 30 Tage:
```bash
# News älter als 30 Tage nach archive/YYYY-MM/ verschieben
find project-news/ -maxdepth 1 -name "*.md" ! -name "README.md" -mtime +30 -exec bash -c '
  f="{}"; d=$(echo "$f" | grep -oE "[0-9]{4}-[0-9]{2}");
  mkdir -p "project-news/archive/$d" && mv "$f" "project-news/archive/$d/"
' \;
```

### 3c — Neue Notes empfehlen (wenn `notify_new_notes: true`)
```bash
git log --oneline --since="7 days ago" -- content/ | head -10
```
Neue Notes gegen `interests` aus `.mnemosyne.md` abgleichen. Kompakt zusammenfassen:
```
📝 [Anzahl] neue Notes diese Woche ([Anzahl] zu deinen Interessen)
```
Auf Nachfrage: Titel + Einzeiler zeigen, bei Wunsch zusammenfassen.

### 4 — Willkommen oder direkt arbeiten
```bash
test -f .claude/.welcomed && echo "returning" || echo "new"
```

**`new` (frischer Clone):**
Kurz willkommen heißen — wenn Profil vorhanden, mit Namen. Erklären was Gedankenwelten ist. Drei Dinge erwähnen:
1. `/gedankenwelten-note-pipeline` für neue Notes
2. Fork-Workflow (PR auf GitHub) für Beiträge
3. `project-news/` — GoodNews-Board für positive Nachrichten aus der Community
Fragen womit gestartet werden soll. Dann:
```bash
touch .claude/.welcomed
```

**`returning`:** Direkt in die Arbeit. Wenn Profil vorhanden: kurz mit Namen grüßen. GoodNews + Note-Updates kompakt anzeigen (wenn vorhanden), dann arbeiten.

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
| *"merke dir das"* | Remember-Skill — speichert Erinnerungen in `.mnemosyne.md` |

## GoodNews — Community-Board

`project-news/` enthält positive Nachrichten aus der Community. Nutzer können GoodNews per Pull Request einreichen.

**KI als erste Schleuse:** Wenn jemand eine GoodNews schreiben möchte:
- ✅ Positive Erlebnisse, gute Nachrichten, Dankbarkeit, Beeindruckendes
- ✅ Im Vipassana-Sinne hilfreich — auch wenn nicht perfekt positiv
- ❌ Klagen, Theorien, Spam, Werbung, Selbstdarstellung
- Immer freundlich umlenken, nie harsch ablehnen
- Im Zweifelsfall: Wenn es jemandem helfen könnte, es zu lesen — darf es stehen

Details: `project-news/README.md`

## Commit-Konvention

```bash
git add -A && git commit -m "note-pipeline: Autor — Thema" && git push
```
