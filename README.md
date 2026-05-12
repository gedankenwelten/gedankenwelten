# Gedankenwelten

Eine offene Wissensplattform für politisches und philosophisches Denken — faktengeprüft, vernetzt, analytisch.

**Vision:** Gegenmodell zum algorithmischen Outrage-Loop. Nicht neutral, sondern dokumentierte Perspektive mit Faktencheck. Nicht nur Kritik — Einordnung, Kontext, Denkanstöße.

**Fundament:** Vipassana — Beobachten ohne zu reagieren, Verstehen ohne zu urteilen.

→ [gedankenwelten.org](https://gedankenwelten.org)

---

## Lokale Wiki starten

```bash
git clone https://github.com/gedankenwelten/gedankenwelten
cd gedankenwelten
docker compose up
```

Wiki öffnen: **http://localhost:8080**

Die Wiki baut sich bei jeder Dateiänderung in `content/` automatisch neu.

---

## Notes mit Claude Code erstellen

Dieses Repo enthält eine vollständige [Claude Code](https://claude.ai/code) Konfiguration. Wer Claude Code installiert hat, kann direkt loslegen:

```bash
cd gedankenwelten
claude
```

### Pipeline: Neue Note aus YouTube / Podcast / Artikel

```
/gedankenwelten-note-pipeline
```

Die Pipeline führt durch den gesamten Prozess:
1. YouTube-Untertitel herunterladen oder Audio transkribieren
2. Sprecher recherchieren (Humboldt-Agent)
3. Analytische Note schreiben (Aristoteles-Standard: ≥1.200 Wörter, ≥5 Zitate)
4. Faktencheck (Sherlock-Agent)
5. Cross-Linking zu bestehenden Notes (Montaigne-Agent)
6. Commit & Push — Note erscheint sofort in der lokalen Wiki

### Weitere Skills

| Befehl | Aufgabe |
|---|---|
| `/aristoteles` | Note aus Transkript tiefenanalytisch schreiben |
| `/heraklit` | Bestehende Note vertiefen |
| `/obsidian-markdown` | Callouts, Wikilinks, Frontmatter-Referenz |

### Voraussetzungen für Transkription

```bash
brew install yt-dlp ffmpeg      # YouTube-Download + Audio-Verarbeitung
pip install mlx-whisper         # Lokale Transkription (Mac M-Series)
```

Ohne diese Tools funktioniert die Transkriptions-Pipeline nicht — Notes lesen, schreiben und verlinken funktioniert ohne sie.

---

## Note-Qualitätsstandard

Jede Note folgt dem **Aristoteles-Standard**:

- **≥ 1.200 Wörter** Inhalt — Analyse, keine Zusammenfassung
- **6–8 Abschnitte** mit eigener Einordnung pro Abschnitt
- **≥ 5 direkte Zitate** mit Zeitstempel-Link ins Original
- **Faktencheck** mit verifizierten Quellenlinks (Pflicht bei Zeitgeist-Notes)
- **`## Weiterdenken`** mit offenen Fragen am Ende jeder Note

---

## Struktur

```
content/
  Denker/       ← Tiefenanalysen einzelner Denker und Quellen
  Zeitgeist/    ← Interviews, Vorträge, Podcasts
  DenkerVita/   ← Biografische Profile
  Panorama/     ← Thematische Synthese (min. 3 Notes zum Thema)
  Gedanken/     ← Persönliche Reflexionen
  Vipassana/    ← Vipassana-Konzepte und Meditationspraxis
```

---

## Mit KI arbeiten

Dieses Repo enthält fertige Konfigurationen für alle gängigen KI-CLI-Tools — einfach klonen und loslegen:

| Tool | Konfigurationsdatei | Befehl |
|---|---|---|
| [Claude Code](https://claude.ai/code) | `CLAUDE.md` + `.claude/` | `claude` |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `GEMINI.md` + `AGENTS.md` | `gemini` |
| [OpenAI Codex](https://github.com/openai/codex) | `AGENTS.md` | `codex` |
| [Aider](https://aider.chat) | `AGENTS.md` | `aider` |
| [Cursor](https://cursor.com) | `.cursor/rules/gedankenwelten.mdc` | Cursor öffnen |
| [GitHub Copilot](https://github.com/features/copilot) | `.github/copilot-instructions.md` | im Editor |

Die vollständige Pipeline-Dokumentation (8 Schritte, Qualitätsstandard, Tag-Taxonomie) liegt in **`AGENTS.md`** und ist für jedes Tool lesbar — kein spezielles Format, plain Markdown.

---

## Mitmachen

Contributions willkommen — als Pull Request mit neuer Note oder Ergänzung.

Qualitätskriterien: Faktencheck vorhanden, Quellen verlinkt, analytisch statt zusammenfassend.

---

## Lizenz

**Inhalte** (`content/`) — [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — teilen und anpassen, auch kommerziell, solange die gleiche Lizenz weitergegeben wird.

**Code & Tooling** — [MIT](LICENSE)

Die Gedanken sind frei.

---

Gebaut mit [Quartz](https://github.com/jackyzha0/quartz) © Jacky Zhao, MIT License.
