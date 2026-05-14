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
docker compose up -d
./scripts/setup-hooks.sh   # Git-Hook installieren (einmalig)
```

Wiki öffnen: **http://localhost:9999**

### Automatischer Rebuild

Nach `git pull` wird die Wiki automatisch rebuilt (via Git `post-merge` Hook).
Manuell rebuilden: `./scripts/rebuild.sh`

---

## Notes mit Claude Code erstellen

Dieses Repo enthält eine vollständige [Claude Code](https://claude.ai/code) Konfiguration. Wer Claude Code installiert hat, kann direkt loslegen:

```bash
cd gedankenwelten
claude
```

Die KI merkt sich deinen Namen, deine Sprache und Interessen in einer lokalen `.copilot-user.md` (gitignored). Beim ersten Start wirst du gefragt — danach passt sich die Zusammenarbeit an. Per *„merke dir das"* kannst du jederzeit Notizen hinterlegen.

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
6. Commit & Push + Wiki-Rebuild — Note erscheint in der lokalen Wiki

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

## Die KI als Gesprächspartner

Wer dieses Repo mit einem KI-Tool öffnet, bekommt nicht nur eine Pipeline zur Note-Erstellung — sondern einen Gesprächspartner, der den gesamten Inhalt kennt.

**Was möglich ist:**

- *„Was sagt Hannah Arendt über den Ursprung des Totalitarismus — und wie verhält sich das zu dem, was Staiy letzte Woche über die AfD gesagt hat?"*
- *„Welche Notes widersprechen einander? Wo gibt es echte Spannungen im Denken?"*
- *„Ich habe gerade Frankls Satz über den Raum zwischen Reiz und Reaktion gelesen — kannst du das mit dem Vipassana-Fundament verknüpfen?"*
- *„Schreib mir eine Gegenfrage zu dieser These, die Aristoteles gestellt hätte."*

Das ist kein Chatbot über abstrakte Themen — die KI spricht über *diese* Notes, *diese* Denker, *diesen* Wissensstand. Jede neue Note, die hinzukommt, erweitert den Gesprächsraum.

**Das Fundament bleibt:** Beobachten ohne zu reagieren. Verstehen ohne zu urteilen. Die KI liefert Perspektiven und Widersprüche — das Urteilen bleibt beim Menschen.

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

## Mitmachen — Fork & Pull Request

Gedankenwelten lebt von Beiträgen. Das Modell ist einfach: **Fork → eigene Note schreiben → Pull Request**.

> **Clone vs. Fork — was ist der Unterschied?**
>
> Ein **Clone** reicht zum Lesen, Philosophieren und lokalen Ausprobieren — aber `git push` schlägt fehl, weil du keine Schreibrechte auf das Original hast.
>
> Ein **Fork** erstellt deine eigene Kopie des Repos auf GitHub. Dort hast du vollen Schreibzugriff, kannst pushen und einen Pull Request ans Original stellen.
>
> → Nur zum Lesen und Erkunden: `git clone` genügt.
> → Beitrag einreichen: Fork nötig.

```
1. Fork: github.com/gedankenwelten/gedankenwelten → "Fork" oben rechts
2. Clone deinen Fork:
   git clone https://github.com/DEIN-USERNAME/gedankenwelten
   cd gedankenwelten

3. Wiki starten (optional, zum lokalen Vorschauen):
   docker compose up   →   http://localhost:9999

4. KI-Tool starten und Note erstellen:
   claude              →   /gedankenwelten-note-pipeline
   gemini / codex / aider — funktionieren genauso

5. Commit & Push in deinen Fork:
   git add -A && git commit -m "note-pipeline: Autor — Thema"
   git push origin main

6. Pull Request auf GitHub öffnen
   github.com/gedankenwelten/gedankenwelten → "New Pull Request"
```

**Was reviewed wird:**
- Ist es eine Analyse, keine Zusammenfassung?
- Faktencheck vorhanden bei Zeitgeist-Notes?
- Quellen verlinkt, Zitate mit Timestamps?
- `## Weiterdenken` mit echten offenen Fragen?

Die KI-Pipeline (Aristoteles, Sokrates, Sherlock, Montaigne) hilft beim Einhalten des Standards — sie ist genau dafür da.

**Tipp:** Wer das Repo forkt und regelmäßig Beiträge plant, sollte es mit dem Original synchron halten:

```bash
git remote add upstream https://github.com/gedankenwelten/gedankenwelten.git
git pull upstream main
```

---

## Lizenz

**Inhalte** (`content/`) — [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — teilen und anpassen, auch kommerziell, solange die gleiche Lizenz weitergegeben wird.

**Code & Tooling** — [MIT](LICENSE)

Die Gedanken sind frei.

---

Gebaut mit [Quartz](https://github.com/jackyzha0/quartz) © Jacky Zhao, MIT License.
