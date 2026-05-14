# Gedankenwelten

Jeder Mensch hat seine eigene Gedankenwelt. Geformt von Erlerntem und Erfahrung schaffen wir daraus unsere eigene Welt. Von dort aus blicken wir nach draußen.

Eine eigene Welt ganz gewiss. Aber wir vernetzen unsere Welten mit jeder Interaktion. Es entsteht ein stetiger Wandel — in unserem Selbst und im Außen. Wir alle sind Mitgestalter der Gedankenwelten. Und somit reiht sich jeder Einzelne ein, ein Komponist der Welt zu sein, in der wir leben.

→ [gedankenwelten.org](https://gedankenwelten.org)

---

### Was du hier findest

**[[Denker]]** — Manche Menschen widmen ihr Leben dem Denken. Hier begegnen sie einander: ihre Ideen, ihre Fragen, ihre Widersprüche. Vernetzt, weil Denken nie allein entsteht.

**[[Zeitgeist]]** — Was bewegt die Welt — und wer spricht darüber, und warum? Stimmen, die den Moment deuten. Mit Faktencheck, weil Haltung Verantwortung trägt.

**[[Panorama]]** — Wenn mindestens drei Notes dasselbe Thema aus verschiedenen Winkeln beleuchten, entsteht eine verdichtete Perspektive. Was ergibt sich, wenn man die Einzelstimmen zusammenhält?

**[[Gedanken]]** — Persönliche Reflexionen und Denkanstöße. Keine fertigen Antworten — Denkbewegungen.

**[[DenkerVita]]** — Ausführliche Profile: Biografie, Werke, Kernthesen, Verbindungen. Wächst mit jeder analysierten Person.

### Das KI-Team

Alle Notes entstehen mit Hilfe von KI — analysiert, eingeordnet, vernetzt. Jeder Agent hat eine Rolle:

| Agent | Aufgabe |
|---|---|
| **Aristoteles** | Analysiert. Destilliert aus einem Transkript nicht eine Zusammenfassung, sondern eine Durchdringung. |
| **Sokrates** | Fragt. Sucht unter den Antworten die Fragen, die noch niemand gestellt hat. |
| **Sherlock** | Prüft. Glaubt erst, wenn er Belege hat — Skepsis ohne Zynismus. |
| **Montaigne** | Vernetzt. Findet, wo Fromm mit Arendt spricht und wo Rosa Goenka berührt. |
| **Humboldt** | Kartografiert. Baut für jeden Denker ein ausführliches Profil. |
| **Heraklit** | Vertieft. Kehrt zurück und bringt die zweite Schicht — die Tiefe, die beim ersten Mal nicht sichtbar war. |

> *Nichts, was du hier liest, hat den Anspruch, vollständig oder Wahrheit zu sein. Sei dein eigener Denker.*

**Fundament:** [Vipassana](https://www.dhamma.org) — Beobachten ohne zu reagieren, Verstehen ohne zu urteilen.

---

## 🚀 Loslegen — mit KI-Begleitung

Du brauchst kein Vorwissen. Kopiere den folgenden Prompt in deine bevorzugte KI (ChatGPT, Claude, Gemini, etc.) — sie führt dich durch alles: Fork, Installation, Docker oder Obsidian, erste Schritte.

<details>
<summary><strong>📋 Setup-Prompt kopieren (klick zum Aufklappen)</strong></summary>

```
Ich möchte das Open-Source-Projekt "Gedankenwelten" einrichten — eine offene
Wissensplattform für politisches und philosophisches Denken.

Projekt: https://github.com/gedankenwelten/gedankenwelten
Website: https://gedankenwelten.org

Bitte führe mich Schritt für Schritt durch das Setup:

1. Frage mein Betriebssystem (macOS, Windows, Linux)
2. Prüfe ob Git installiert ist, wenn nicht: Installationsanleitung zeigen
3. Frage wie ich die Notes lesen möchte:
   a) Docker-Wiki (Webseite lokal im Browser, wie gedankenwelten.org)
   b) Obsidian (interaktiver Graph, Backlinks, lokale Suche)
   c) Beides
4. Frage ob ich nur lesen oder auch beitragen möchte
   - Nur lesen → git clone reicht
   - Beitragen → Fork auf GitHub erklären, dann clone
5. Führe durch die Installation:
   - Docker: docker compose up -d → http://localhost:9999
     Danach: ./scripts/setup-hooks.sh (Auto-Rebuild nach git pull)
   - Obsidian: "Open folder as vault" → den content/ Ordner wählen
6. Zeige mir am Ende, wie ich anfangen kann:
   - Im Graph stöbern, eine Note lesen
   - Optional: Claude Code / Gemini CLI für neue Notes
   - Optional: GoodNews schreiben (project-news/)

Sei geduldig, erkläre verständlich, biete immer Alternativen an.
```

</details>

> **Oder direkt loslegen** — die manuelle Anleitung findest du weiter unten.

---

## Drei Wege zu Gedankenwelten

| | 🌐 Webseite | 🐳 Docker lokal | 🗂️ Obsidian |
|---|---|---|---|
| **Was** | gedankenwelten.org lesen | Eigene Wiki im Browser | Interaktiver Vault |
| **Setup** | Keins | `docker compose up -d` | Ordner als Vault öffnen |
| **Graph** | ✓ | ✓ | ✓ (interaktiv) |
| **Suche** | ✓ | ✓ | ✓ (schneller) |
| **Beitragen** | ✗ | ✓ (mit Fork) | ✓ (mit Fork) |
| **Offline** | ✗ | ✓ | ✓ |

---

## Lokale Wiki starten (Docker)

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

## Obsidian-Vault öffnen

Alternativ oder ergänzend zur Docker-Wiki:

1. [Obsidian](https://obsidian.md/download) installieren
2. Obsidian starten → **„Open folder as vault"**
3. Das **gesamte `gedankenwelten/`-Repo** als Vault öffnen
4. Graph-View öffnen: `Ctrl/Cmd + G`

Die `.obsidian/`-Konfiguration und `.obsidianignore` sind im Repo enthalten — Graph-Farben (Denker, Zeitgeist, Gedanken), Backlinks und Tags funktionieren sofort. Quartz-Code wird automatisch ausgeblendet.

---

## Notes mit Claude Code erstellen

Dieses Repo enthält eine vollständige [Claude Code](https://claude.ai/code) Konfiguration. Wer Claude Code installiert hat, kann direkt loslegen:

```bash
cd gedankenwelten
claude
```

Die KI merkt sich deinen Namen, deine Sprache und Interessen in einer lokalen `.mnemosyne.md` (gitignored — benannt nach der griechischen Göttin der Erinnerung). Beim ersten Start wirst du gefragt — danach passt sich die Zusammenarbeit an. Per *„merke dir das"* kannst du jederzeit Notizen hinterlegen.

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

### Voraussetzungen für Transkription

```bash
brew install yt-dlp ffmpeg      # YouTube-Download + Audio-Verarbeitung
pip install mlx-whisper         # Lokale Transkription (Mac M-Series)
```

Ohne diese Tools funktioniert die Transkriptions-Pipeline nicht — Notes lesen, schreiben und verlinken funktioniert ohne sie.

---

## 🌱 GoodNews — Community-Board

In `project-news/` können alle, die Gedankenwelten nutzen, positive Nachrichten teilen — persönliche Erlebnisse, gute Nachrichten aus der Welt, Momente der Dankbarkeit.

```bash
# GoodNews einreichen:
# 1. Datei anlegen: project-news/2026-05-14-mein-titel.md
# 2. Per Pull Request einreichen
```

Die KI zeigt neue GoodNews beim Session-Start automatisch an. Details: [`project-news/README.md`](project-news/README.md)

---

## Note-Qualitätsstandard

Jede Note folgt dem **Aristoteles-Standard**:

- **≥ 1.200 Wörter** Inhalt — Analyse, keine Zusammenfassung
- **6–8 Abschnitte** mit eigener Einordnung pro Abschnitt
- **≥ 5 direkte Zitate** mit Zeitstempel-Link ins Original
- **Faktencheck** mit verifizierten Quellenlinks (Pflicht bei Zeitgeist-Notes)
- **`## Weiterdenken`** mit offenen Fragen am Ende jeder Note

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
