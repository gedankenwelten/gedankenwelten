[🇩🇪 Deutsch](README.md) | 🇬🇧 **English** | [🌐 28 languages on gedankenwelten.org](https://gedankenwelten.org/?lang=en)

---

# Gedankenwelten

*Gedankenwelten* — literally "thought-worlds" — is an open knowledge platform for political and philosophical thinking. Built as a networked wiki where ideas meet, connect, and challenge each other.

Every person carries their own thought-world — shaped by experience, learning, and reflection. From that inner world, we look outward. These worlds aren't isolated: they connect with every interaction. We are all co-composers of the world we inhabit.

→ [gedankenwelten.org](https://gedankenwelten.org/?lang=en)

---

### What you'll find here

**[[Denker]]** (Thinkers) — Some people dedicate their lives to thinking. Here their ideas meet: questions, contradictions, connections. Networked, because thinking never happens in isolation.

**[[Zeitgeist]]** (Spirit of the Times) — What moves the world — and who speaks about it, and why? Voices interpreting the current moment. With fact-checks, because conviction carries responsibility.

**[[Geistesblitz]]** (Flash of Insight) — Fundamental knowledge and human creative power: science, philosophy, psychology, technology. Notes that explain the world and make visible what is extraordinary about being human — the spark that joins knowing and creating. Timeless rather than topical.

**[[Panorama]]** — When three or more notes illuminate the same topic from different angles, a condensed perspective emerges. What becomes visible when you hold the individual voices together?

**[[Gedanken]]** (Thoughts) — Personal reflections and provocations. No finished answers — movements of thought.

**[[DenkerVita]]** (Thinker Profiles) — Detailed profiles: biography, works, core theses, connections. Grows with every analyzed person.

**[[GoodNews]]** — Good news from the community. Personal experiences, positive developments, moments of gratitude. In the spirit of Epicurus: joy through simplicity and friendship.

### The AI Team

All notes are created with AI assistance — analyzed, contextualized, cross-linked. Each agent has a role:

| Agent | Role |
|---|---|
| **Gedankenwelt** | Translates raw material — YouTube, podcast, article — into networked notes. |
| **Aristoteles** | Analyzes. Distills not a summary but a penetration of the subject. |
| **Sokrates** | Questions. Finds beneath the answers the questions nobody has asked yet. |
| **Sherlock** | Verifies. Believes only with evidence — skepticism without cynicism. |
| **Montaigne** | Connects. Finds where Fromm speaks with Arendt and where Rosa meets Goenka. |
| **Humboldt** | Maps. Builds detailed profiles for every thinker. |
| **Heraklit** | Deepens. Returns to bring the second layer — the depth invisible on first pass. |
| **Epikur** | Gathers. Accompanies the sharing of good news — joy through simplicity. |
| **Pascal** | Reflects. Holds personal thoughts — from these, notes in [[Gedanken]] emerge. |
| **Vergil** | Guides. Explains the Gedankenwelten — philosophically and technically, patiently. |

> *Nothing you read here claims to be complete or to be truth. Be your own thinker.*

**Foundation:** [Vipassana](https://www.dhamma.org) — Observing without reacting. Understanding without judging.

---

## 🌐 Multi-language Support

The live website at [gedankenwelten.org](https://gedankenwelten.org) supports **28 languages** via automatic translation (DeepL + Cloudflare Workers). Simply add `?lang=en` to any URL, or use the language switcher widget on the site.

Supported: Arabic, Bulgarian, Czech, Danish, Greek, English, Spanish, Estonian, Finnish, French, Hungarian, Indonesian, Italian, Japanese, Korean, Lithuanian, Latvian, Norwegian, Dutch, Polish, Portuguese, Romanian, Russian, Slovak, Slovenian, Swedish, Turkish, Ukrainian, Chinese.

The original notes are written in German — translations are AI-generated and cached for performance.

---

## 🚀 Getting Started — with AI Guidance

No prior knowledge needed. Copy this prompt into your preferred AI (ChatGPT, Claude, Gemini, etc.) — it will guide you through everything: fork, installation, Docker or Obsidian, first steps.

<details>
<summary><strong>📋 Copy setup prompt (click to expand)</strong></summary>

```
I want to set up the open-source project "Gedankenwelten" — an open knowledge
platform for political and philosophical thinking.

Project: https://github.com/gedankenwelten/gedankenwelten
Website: https://gedankenwelten.org

Please guide me step by step through setup:

1. Ask my operating system (macOS, Windows, Linux)
2. Check if Git is installed, if not: show installation guide
3. Ask how I want to read the notes:
   a) Docker Wiki (website locally in browser, like gedankenwelten.org)
   b) Obsidian (interactive graph, backlinks, local search)
   c) Both
4. Ask if I just want to read or also contribute
   - Read only → git clone is enough
   - Contribute → explain GitHub Fork, then clone
5. Guide through installation:
   - Docker: docker compose up -d → http://localhost:9999
     Then: ./scripts/setup-hooks.sh (auto-rebuild after git pull)
   - Obsidian: "Open folder as vault" → choose the content/ folder
6. Show me how to get started:
   - Browse the graph, read a note
   - Optional: Claude Code / Gemini CLI for new notes
   - Optional: Write GoodNews (content/GoodNews/)

Be patient, explain clearly, always offer alternatives.
```

</details>

> **Or jump right in** — manual instructions below.

---

## Three Ways to Gedankenwelten

| | 🌐 Website | 🐳 Docker Local | 🗂️ Obsidian |
|---|---|---|---|
| **What** | Read gedankenwelten.org | Own wiki in browser | Interactive vault |
| **Setup** | None | `docker compose up -d` | Open folder as vault |
| **Graph** | ✓ | ✓ | ✓ (interactive) |
| **Search** | ✓ | ✓ | ✓ (faster) |
| **Contribute** | ✗ | ✓ (with fork) | ✓ (with fork) |
| **Offline** | ✗ | ✓ | ✓ |

---

## Run Local Wiki (Docker)

```bash
git clone https://github.com/gedankenwelten/gedankenwelten
cd gedankenwelten
docker compose up -d
./scripts/setup-hooks.sh   # Install Git hook (once)
```

Open wiki: **http://localhost:9999**

### Auto-rebuild

After `git pull`, the wiki rebuilds automatically (via Git `post-merge` hook).
Manual rebuild: `./scripts/rebuild.sh`

---

## Open as Obsidian Vault

Alternative or complement to Docker:

1. Install [Obsidian](https://obsidian.md/download)
2. Launch Obsidian → **"Open folder as vault"**
3. Open the **entire `gedankenwelten/` repo** as vault
4. Open Graph View: `Ctrl/Cmd + G`

The `.obsidian/` configuration and `.obsidianignore` are included — graph colors (Denker, Zeitgeist, Gedanken), backlinks, and tags work immediately. Quartz code is automatically hidden.

---

## Create Notes with Claude Code

This repo includes a complete [Claude Code](https://claude.ai/code) configuration. Anyone with Claude Code can start immediately:

```bash
cd gedankenwelten
claude
```

The AI remembers your name, language, and interests in a local `.mnemosyne.md` (gitignored — named after the Greek goddess of memory). You'll be asked on first launch — collaboration adapts from there. Use *"remember this"* to store notes anytime.

### Pipeline: New Note from YouTube / Podcast / Article

```
/gedankenwelt-note-pipeline
```

The pipeline guides through the entire process:
1. Download YouTube subtitles or transcribe audio
2. Research the speaker (Humboldt agent)
3. Write analytical note (Aristoteles standard: ≥1,200 words, ≥5 quotes)
4. Fact-check (Sherlock agent)
5. Cross-link to existing notes (Montaigne agent)
6. Commit & push + wiki rebuild — note appears in local wiki

### Prerequisites for Transcription

```bash
brew install yt-dlp ffmpeg      # YouTube download + audio processing
pip install mlx-whisper         # Local transcription (Mac M-Series)
```

Without these tools, the transcription pipeline won't work — reading, writing, and linking notes works without them.

---

## 🌱 GoodNews — Community Board

In `content/GoodNews/`, everyone using Gedankenwelten can share positive news — personal experiences, good news from the world, moments of gratitude.

```bash
# Submit GoodNews:
# 1. Create file: content/GoodNews/2026-05-14-my-title.md
# 2. Submit via Pull Request
```

The AI shows new GoodNews at session start automatically. Details: [`content/GoodNews/README.md`](content/GoodNews/README.md)

---

## Note Quality Standard

Every note follows the **Aristoteles Standard**:

- **≥ 1,200 words** of content — analysis, not summary
- **6–8 sections** with individual commentary per section
- **≥ 5 direct quotes** with timestamp links to the original
- **Fact-check** with verified source links (mandatory for Zeitgeist notes)
- **`## Weiterdenken`** (Further Thinking) with open questions at the end

---

## AI as Conversation Partner

Open this repo with an AI tool and you don't just get a note-creation pipeline — you get a conversation partner who knows the entire content.

**What's possible:**

- *"What does Hannah Arendt say about the origins of totalitarianism — and how does that relate to what Staiy said about the AfD last week?"*
- *"Which notes contradict each other? Where are genuine tensions in the thinking?"*
- *"I just read Frankl's sentence about the space between stimulus and response — can you connect that to the Vipassana foundation?"*
- *"Write me a counter-question to this thesis that Aristotle would have asked."*

This isn't a chatbot about abstract topics — the AI speaks about *these* notes, *these* thinkers, *this* body of knowledge. Every new note expands the conversation space.

**The foundation remains:** Observe without reacting. Understand without judging. The AI offers perspectives and contradictions — judgment stays with the human.

---

## Work with AI

This repo contains ready-made configurations for all major AI CLI tools — just clone and start:

| Tool | Config file | Command |
|---|---|---|
| [Claude Code](https://claude.ai/code) | `CLAUDE.md` + `.claude/` | `claude` |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `GEMINI.md` + `AGENTS.md` | `gemini` |
| [OpenAI Codex](https://github.com/openai/codex) | `AGENTS.md` | `codex` |
| [Aider](https://aider.chat) | `AGENTS.md` | `aider` |
| [Cursor](https://cursor.com) | `.cursor/rules/gedankenwelten.mdc` | Open Cursor |
| [GitHub Copilot](https://github.com/features/copilot) | `.github/copilot-instructions.md` | In editor |

Full pipeline documentation (8 steps, quality standard, tag taxonomy) lives in **`AGENTS.md`** — readable by any tool, plain Markdown.

---

## Contributing — Fork & Pull Request

Gedankenwelten thrives on contributions. The model is simple: **Fork → write your own note → Pull Request**.

> **Clone vs. Fork — what's the difference?**
>
> A **Clone** is enough for reading, philosophizing, and local experimentation — but `git push` will fail because you don't have write access to the original.
>
> A **Fork** creates your own copy of the repo on GitHub. There you have full write access, can push, and submit a Pull Request to the original.
>
> → Just reading and exploring: `git clone` is enough.
> → Submit a contribution: Fork required.

```
1. Fork: github.com/gedankenwelten/gedankenwelten → "Fork" top right
2. Clone your fork:
   git clone https://github.com/YOUR-USERNAME/gedankenwelten
   cd gedankenwelten

3. Start wiki (optional, for local preview):
   docker compose up   →   http://localhost:9999

4. Start AI tool and create note:
   claude              →   /gedankenwelt-note-pipeline
   gemini / codex / aider — work the same way

5. Commit & Push to your fork:
   git add -A && git commit -m "note-pipeline: Author — Topic"
   git push origin main

6. Open Pull Request on GitHub
   github.com/gedankenwelten/gedankenwelten → "New Pull Request"
```

**What gets reviewed:**
- Is it analysis, not summary?
- Fact-check present for Zeitgeist notes?
- Sources linked, quotes with timestamps?
- `## Weiterdenken` with genuine open questions?

The AI pipeline (Gedankenwelt, Aristoteles, Sokrates, Sherlock, Montaigne) helps meet the standard — that's exactly what it's for.

**Tip:** If you fork and plan regular contributions, keep it synced with the original:

```bash
git remote add upstream https://github.com/gedankenwelten/gedankenwelten.git
git pull upstream main
```

---

## License

**Content** (`content/`) — [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — share and adapt, including commercially, as long as the same license is passed on.

**Code & Tooling** — [MIT](LICENSE)

Thoughts are free.

---

Built with [Quartz](https://github.com/jackyzha0/quartz) © Jacky Zhao, MIT License.
