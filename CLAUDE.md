# CLAUDE.md — Gedankenwelten

@.claude/rules/gedankenwelten.md
@.claude/rules/pipeline.md
@.claude/rules/tags.md

---

Gedankenwelten ist eine offene Wissensplattform für politisches und philosophisches Denken — faktengeprüft, vernetzt, analytisch.

**Vision:** Ein Gegenmodell zum algorithmischen Outrage-Loop. Nicht neutral, sondern dokumentierte Perspektive mit Faktencheck.

**Fundament:** Vipassana — Beobachten ohne zu reagieren, Verstehen ohne zu urteilen.

---

## Quick Start

### 1. Lokale Wiki starten

```bash
docker compose up        # Wiki starten
# → http://localhost:8080
```

Die Wiki lädt alle Notes aus `content/` und baut sich bei Dateiänderungen **automatisch neu**.

### 2. Neue Note aus Video/Podcast erstellen

```
/gedankenwelten-note-pipeline
```

Vollständige Pipeline: Download → Transkription → Note → Faktencheck → Cross-Linking → Push.
Die Wiki zeigt die neue Note nach dem nächsten Auto-Build.

### 3. Bestehende Note vertiefen

```
/heraklit
```

---

## Projektstruktur

```
gedankenwelten/
  content/
    Denker/          ← Tiefenanalysen einzelner Denker/Quellen
    Zeitgeist/       ← Interviews, Vorträge, Podcasts
    DenkerVita/      ← Biografische Profile (angelegt von Humboldt)
    Panorama/        ← Thematische Synthese-Notes
    Gedanken/        ← Persönliche Reflexionen
    Vipassana/       ← Vipassana-Konzepte und Meditationspraxis
    Transkripte/     ← VTT + TXT Rohmaterial (nicht auf Website)
    known-speakers.md
    Quellen & Links.md
  .claude/
    rules/           ← Projektregeln
    skills/          ← Claude Code Skills
    agents/          ← Sub-Agenten (Humboldt, Sherlock, Montaigne)
    scripts/         ← vtt_to_txt.py, merge_vtt_chunks.py
    settings.json
  Dockerfile         ← Quartz-Container
  docker-compose.yml ← Lokale Wiki mit Auto-Rebuild
  quartz.config.ts   ← Website-Konfiguration
  CLAUDE.md          ← diese Datei
```

---

## Wiki-Befehle

```bash
docker compose up -d     # Wiki im Hintergrund starten
docker compose logs -f   # Build-Logs verfolgen
docker compose down      # Wiki stoppen
docker compose build     # Image neu bauen (nach Quartz-Config-Änderungen)
```

**Auto-Rebuild:** Wenn der Container läuft, wird die Wiki bei jeder Dateiänderung in `content/` automatisch neu gebaut (~2–5 Sekunden).

---

## Skills

| Skill | Befehl | Aufgabe |
|---|---|---|
| **Pipeline** | `/gedankenwelten-note-pipeline` | Neue Note aus YouTube/Podcast/Artikel |
| **Aristoteles** | `/aristoteles` | Tiefenanalyse ab Transkript (Schritt 5 der Pipeline) |
| **Heraklit** | `/heraklit` | Bestehende Note vertiefen |
| **Obsidian-Markdown** | `/obsidian-markdown` | Callouts, Wikilinks, Frontmatter-Syntax |

## Agenten

| Agent | Aufruf | Aufgabe |
|---|---|---|
| **Humboldt** | `/agent humboldt` | Sprecher recherchieren, DenkerVita anlegen |
| **Sherlock** | `/agent sherlock` | Faktencheck mit Quellenverifikation |
| **Montaigne** | `/agent montaigne` | Cross-Linking zwischen Notes |

---

## Note-Qualitätsstandard (Aristoteles)

- **≥ 1.200 Wörter** Inhalt — Analyse, keine Zusammenfassung
- **6–8 Abschnitte** à ≥ 120 Wörter mit eigener Einordnung
- **≥ 5 direkte Zitate** mit Zeitstempel-Link
- **Faktencheck** via Sherlock (Pflicht bei Zeitgeist-Notes)
- **`## Weiterdenken`** mit 3–5 Aristoteles-Fragen

---

## Geist des Projekts

- Nicht neutral — sondern dokumentierte Perspektive mit Faktencheck
- Nicht nur Kritik — Einordnung, Kontext, Denkanstöße
- Analytisch statt reaktiv: Beobachten ohne sofort zu urteilen
- Vernetzt: Jede Note ist Teil eines größeren Gesprächs
