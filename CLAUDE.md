# CLAUDE.md — Gedankenwelten

@.claude/rules/gedankenwelten.md
@.claude/rules/pipeline.md
@.claude/rules/tags.md

---

Gedankenwelten ist eine offene Wissensplattform für politisches und philosophisches Denken — faktengeprüft, vernetzt, analytisch.

**Vision:** Ein Gegenmodell zum algorithmischen Outrage-Loop. Nicht neutral, sondern dokumentierte Perspektive mit Faktencheck. Nicht nur Kritik, sondern Einordnung und Denkanstöße.

**Fundament:** Vipassana — Beobachten ohne zu reagieren, Verstehen ohne zu urteilen.

---

## Projektstruktur

```
gedankenwelten/
  content/
    Denker/          ← Tiefenanalysen einzelner Denker/Quellen
    Zeitgeist/       ← Interviews, Vorträge, Podcasts
    DenkerVita/      ← Biografische Profile
    Panorama/        ← Thematische Synthese-Notes
    Transkripte/     ← VTT + TXT Rohmaterial (nicht auf Website)
    known-speakers.md
    Quellen & Links.md
  .claude/
    rules/           ← Projektregeln (Ordner, Tags, Pipeline)
    skills/          ← Claude Code Skills (Pipeline, Aristoteles, Heraklit, Obsidian)
    agents/          ← Sub-Agenten (Humboldt, Sherlock, Montaigne)
    scripts/         ← Python-Hilfsskripte (vtt_to_txt.py, merge_vtt_chunks.py)
    settings.json    ← Erlaubte Bash-Befehle
  quartz/            ← Quartz-Konfiguration für die Website
  CLAUDE.md          ← diese Datei
```

---

## Mit Claude Code arbeiten

### Neue Note aus YouTube/Podcast erstellen

```
/gedankenwelten-note-pipeline
```

Startet die vollständige Pipeline: Download → Transkription → Note-Erstellung → Faktencheck → Cross-Linking.

### Note vertiefen

```
/aristoteles
```
Für neue Notes (Tiefenanalyse ab Transkript).

```
/heraklit
```
Für bestehende Notes die mehr Substanz brauchen.

### Verfügbare Agenten

| Agent | Aufruf | Aufgabe |
|---|---|---|
| **Humboldt** | `/agent humboldt` | Sprecher recherchieren, DenkerVita anlegen |
| **Sherlock** | `/agent sherlock` | Faktencheck mit Quellenverifikation |
| **Montaigne** | `/agent montaigne` | Cross-Linking zwischen Notes |

---

## Note-Qualitätsstandard

Jede Note folgt dem **Aristoteles-Standard**:

- **Inhalt ≥ 1.200 Wörter** — Analyse, keine Zusammenfassung
- **6–8 Abschnitte** à ≥ 120 Wörter mit eigener Einordnung
- **≥ 5 direkte Zitate** mit Zeitstempel-Link
- **Faktencheck** (Pflicht bei Zeitgeist-Notes)
- **Weiterdenken-Abschnitt** mit Aristoteles-Fragen

---

## Geist des Projekts

- Nicht neutral — sondern **dokumentierte Perspektive mit Faktencheck**
- Nicht nur Kritik — Einordnung, Kontext, Denkanstöße
- Analytisch statt reaktiv: Beobachten ohne sofort zu urteilen
- Vernetzt: Jede Note ist Teil eines größeren Gesprächs

---

## Integritätssystem

**Skill-Hash:** Der `gedankenwelten-note-pipeline`-Skill generiert einen `skill_hash` aus dem Note-Content. Das beweist Skill-Nutzung und erkennt unvalidierte manuelle Nachbearbeitung.

**GitHub Action:** Validiert Template-Einhaltung, Faktencheck-Pflicht und Hash-Konsistenz bei PRs.
