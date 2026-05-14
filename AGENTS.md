# AGENTS.md — Gedankenwelten

Universal AI instructions for this repository. Works with any AI CLI tool:
Claude Code · Gemini CLI · OpenAI Codex · Aider · Cline · Cursor

---

## Session Start (always)

At the start of every session:
1. `git pull --ff-only origin main` — get latest notes
2. Check Docker: `docker ps --filter "name=gedankenwelten" --format "{{.Names}} {{.Status}}"`
   - Running → wiki at http://localhost:9999
   - Not running → suggest `docker compose up -d`
3. Check rebuild hook: `test -f .git/hooks/post-merge && echo "ok" || ./scripts/rebuild.sh`
4. Check persona: `test -f .mnemosyne.md && cat .mnemosyne.md || echo "no-profile"`
   - **Profile exists:** Greet by name, use preferred language, check for new notes matching interests
   - **No profile (and no `.claude/.no-profile`):** Offer onboarding — ask one question at a time:
     1. "May I ask a few questions? Everything stays local, nothing is shared."
     2. Name & preferred language
     3. Interests (freeform → store as tags)
     4. "Should I notify you about new notes matching your interests?"
     → Create `.mnemosyne.md` with: `name`, `language`, `interests`, `notify_new_notes`
     → If declined: create `.claude/.no-profile`, never ask again
5. Check GoodNews: `ls project-news/*.md 2>/dev/null | grep -v README`
   - Show unread community GoodNews (compare against `## Gelesene News` in `.mnemosyne.md`)

### Remember Skill
When user says "remember this", "merke dir das", "notier dir" or similar:
1. Security check — reject credentials (passwords, tokens, API keys)
2. Open `.mnemosyne.md` (create if needed)
3. Add under `## Erinnerungen`: `- **[DD.MM.YYYY]** content`
4. Confirm: "Noted ✓"

### GoodNews — Community Board
`project-news/` contains positive news from the community. When a user wants to write a GoodNews:
- ✅ Positive experiences, good news, gratitude, impressive moments
- ❌ No complaints, theories, spam, self-promotion
- Always redirect gently, never reject harshly
- File format: `project-news/YYYY-MM-DD-short-title.md` with frontmatter (author, date, tags)

---

## Project Overview

Gedankenwelten is an open knowledge platform for political and philosophical thinking — fact-checked, interconnected, analytical.
Vision: counter-model to the algorithmic outrage loop. Not neutral, but documented perspective with fact-checks.

**Local wiki:** `docker compose up -d` → http://localhost:9999. Rebuild after changes: `./scripts/rebuild.sh`

---

## Directory Structure

```
content/
  Denker/          ← Deep analyses of individual thinkers/sources
  Zeitgeist/       ← Interviews, talks, podcasts — spirit of the time
  DenkerVita/      ← Biographical profiles (public, linked from notes)
  Panorama/        ← Thematic synthesis (min. 3 notes on the same topic)
  Gedanken/        ← Personal reflections and essays
  Vipassana/       ← Vipassana concepts and meditation practice
  Transkripte/     ← Raw transcripts and VTT files (not published)
  known-speakers.md   ← DenkerVita index with status
  Quellen & Links.md  ← Index of all external sources
```

- New Denker notes → `content/Denker/`
- New Zeitgeist notes → `content/Zeitgeist/`
- New DenkerVitas → `content/DenkerVita/`
- New Panoramas → `content/Panorama/` (manual, when ≥3 notes on same topic)

---

## Skills & Agents

| Task | Description |
|---|---|
| New note from YouTube/Podcast/Article | Follow the 8-step pipeline below |
| Deep analysis from transcript | Aristoteles standard (≥1,200 words, ≥5 quotes, 6–8 sections) |
| Add question layer to a note | Sokrates: inline challenges, contradictions, open questions |
| Deepen an existing note | Heraklit: find what's hidden, add substance and quotes |
| Research speaker → DenkerVita | Web research, create biographical profile |
| Fact-check | Verify claims with sources (Zeitgeist notes only) |
| Cross-link notes | Find thematic connections between existing notes |
| Sync content from private vault | `./scripts/sync.sh` — syncs all sections from Cortex |

---

## Note Pipeline — 8 Steps

### Step 0 — Speaker Research + DenkerVita

Check if DenkerVita exists: `ls "content/DenkerVita/<Name>.md"`

**If exists:** Read it → use as basis for `> [!info] Wer spricht?` callout, add `→ [[DenkerVita/<Name>|DenkerVita]]` at end of callout.

**If not:** Research speaker online, create DenkerVita after note is done.

DenkerVita path: `content/DenkerVita/<Vorname Nachname>.md`
DenkerVita frontmatter:
```yaml
---
title: <Name> — DenkerVita
tags: [denker-vita, <thema>]
---
```

DenkerVita structure:
1. `## Biographischer Snapshot` — same `> [!info]` callout as in note
2. `## Biografie` — lively: turning points, influences
3. `## Bücher & Publikationen` — links to genialokal.de
4. `## Empfehlenswerte Videos & Vorträge`
5. `## Kernthesen` — 3–5 numbered statements
6. `## Politische Einordnung` — if relevant
7. `## Verbindungen zu anderen Denkern`
8. `## Notes` — backlinks to all notes about this person

After creating: update `content/known-speakers.md` with `**Status:** ✓ Vollanalyse → [[DenkerVita/<Name>]]`

**IMPORTANT:** Always use full path for DenkerVita wikilinks: `[[DenkerVita/<Name>]]` NOT `[[<Name>]]`

---

### Step 1 — Clarify Source

- **YouTube video**: URL available? → continue to Step 2
- **Local audio**: file exists locally? → continue to Step 3 (Whisper)
- **Article/Website**: scrape content, create note directly (no transcript needed)
- **TED talk**: find YouTube ID via `yt-dlp ytsearch1:"Firstname Lastname Title"`, then like YouTube

Target folder for transcripts: `content/Transkripte/`

---

### Step 2 — YouTube: Download Subtitles

```bash
# German first
yt-dlp --write-auto-sub --skip-download --sub-lang de \
  --output "content/Transkripte/FILENAME_%(title)s.%(ext)s" "URL"

# Fallback: English
yt-dlp --write-auto-sub --skip-download --sub-lang en \
  --output "content/Transkripte/FILENAME_%(title)s.%(ext)s" "URL"
```

Naming convention: `Lastname_Keyword_` as prefix (e.g. `Haidt_Moral_Roots_`).

Also check video description for sources:
```bash
yt-dlp --get-description "URL"
```

Extract all mentioned books, articles, studies → add as `## Weiterführende Quellen` before `## Verbindungen`.

---

### Step 3 — Audio without Subtitles: Whisper

**Mac Apple Silicon (recommended):**
```bash
pip install mlx-whisper
mlx_whisper "path/to/file.mp3" \
  --model "mlx-community/whisper-large-v3-turbo" \
  --language de \
  --output-format vtt \
  --output-dir "content/Transkripte/"
```

**Mac Intel / Linux CPU:**
```bash
pip install openai-whisper
whisper "audio.wav" --model large-v3 --language de --output_format vtt --output_dir content/Transkripte/
```

**Linux NVIDIA GPU:**
```bash
pip install faster-whisper
python3 -c "
from faster_whisper import WhisperModel
model = WhisperModel('large-v3', device='cuda', compute_type='float16')
segments, info = model.transcribe('audio.wav', language='de')
"
```

For videos without subtitles — extract audio first:
```bash
ffmpeg -i "video.mp4" -vn -acodec pcm_s16le -ar 16000 "audio.wav"
```

---

### Step 4 — VTT → TXT Convert

```bash
# YouTube (with clickable timestamp links)
python3 .claude/scripts/vtt_to_txt.py \
  "content/Transkripte/FILE.vtt" \
  "content/Transkripte/FILE_Transkript.txt" \
  "https://www.youtube.com/watch?v=VIDEO_ID"

# Podcast/local (timestamps only)
python3 .claude/scripts/vtt_to_txt.py \
  "content/Transkripte/FILE.vtt" \
  "content/Transkripte/FILE_Transkript.txt" \
  "local"
```

---

### Step 5 — Create Obsidian Note (Aristoteles Quality Standard)

**Quality requirements (mandatory):**
- ≥ 1,200 words content — analysis, not summary
- 6–8 sections with own assessment per section
- ≥ 5 direct quotes with timestamp links
- Fact-check section (Zeitgeist notes)
- `## Weiterdenken` with open questions at the end

**Filename convention (URL-compatible):**
- Format: `Autor - Kurztitel.md` (simple hyphen `-`, NOT em-dash `—`)
- No `&` → use `und`
- No `:` in filename
- No parentheses `()` for dates
- No umlauts → ä→ae, ö→oe, ü→ue, ß→ss
- Date in filename only for series disambiguation

Good: `Konstantin Flemig - Ukraine Gebietsgewinne 2026.md`
Bad: `Konstantin Flemig — Ukraine & Putin: Gebietsgewinne (12.04.2026).md`

**Zeitgeist note template:**
```markdown
---
title: "Titel"
date: DD.MM.YYYY
tags:
  - zeitgeist
  - thema-tag
  - year-XXXX
aliases:
  - Kurzname
---

# Titel

Quelle: [Titel](https://www.youtube.com/watch?v=VIDEO_ID)

> [!info] Wer spricht?
> **Name** — Kurzbeschreibung
> → [[DenkerVita/<Name>|DenkerVita]]

---

## Inhalt
...

---

## Faktencheck
> [!success] Bestätigt — [Claim]
> [Claim]. Quelle: [Titel](URL)

> [!warning] Vereinfacht — [Claim]
> [Claim]. Quelle: [Titel](URL)

---

## Weiterführende Quellen
- [Titel](URL) — was es ist

---

## Verbindungen

### → [[Andere Note]]
Konzeptuelle Beziehung.

---

## Weiterdenken

> [!question] Was Aristoteles vielleicht gefragt hätte
> - Wenn [Kernthese] stimmt — *was folgt daraus?*
> - [Sprecher] sagt [X] — aber widerspricht das nicht [Y]?
> - Wem nützt es, wenn wir [Annahme] für selbstverständlich halten?
> - Was wäre das stärkste Gegenargument?
```

**Aristoteles inline questions (2–4 per note):**
```markdown
> [!question] Weitergedacht
> Wenn [These] — *was bedeutet das für [konkreten Aspekt]?*
```

Place after sections where a claim is counterintuitive, contradictory, or incomplete.

---

### Step 5b — Fact-Check (Zeitgeist notes only)

For each verifiable claim, search for sources and add to `## Faktencheck`:

| Callout | Meaning |
|---|---|
| `> [!success] Bestätigt` | Claim verified by sources |
| `> [!warning] Vereinfacht` | Roughly correct but distorted or incomplete |
| `> [!danger] Falsch` | Factually unsupported |

**Guidelines:**
- Always read the transcript first. Check what the speaker *actually says*.
- For spiritual/philosophical talks: only check empirical claims (numbers, dates, historical facts).
- Do NOT flag interpretations of canonical texts or spiritual experience reports.

---

### Step 6 — Cross-Linking (Montaigne)

Scan all existing notes in `content/Zeitgeist/` and `content/Denker/` for thematic overlaps.
Add found connections **bidirectionally**: update both the new note and the referenced note.

```markdown
## Verbindungen

### → [[Other Note]]
Conceptual relationship — not just "both deal with X".
```

---

### Step 7 — Update Quellen & Links.md

```markdown
## [Author / Topic]

| | |
|---|---|
| **Vortrag / Video** | [Titel](URL) |
| **Notiz** | [[Note-Filename]] |
| **Transkript** | `content/Transkripte/filename.txt` |
```

---

### Step 8 — Commit, Push & Rebuild

```bash
git add -A && git commit -m "note-pipeline: <Author> — <Topic>"
git push origin main
./scripts/rebuild.sh   # rebuilds local wiki with new note
```

The local wiki auto-rebuilds when Docker is running — no extra step needed.

---

## Tag Taxonomy

### Type (required)
| Tag | Meaning |
|---|---|
| `zeitgeist` | Interview, talk, podcast — spirit of the time |
| `denker` | Deep analysis of a thinker |
| `panorama` | Thematic synthesis note |

### Format (optional)
| Tag | Meaning |
|---|---|
| `gespräch` | Dialogue between two equal voices |

### Year (required for Zeitgeist): `year-2024`, `year-2025`, `year-2026`

### Theme (min. 1–3)
Politics: `demokratie` · `autoritarismus` · `faschismus` · `kapitalismus` · `populismus` · `rechtsextremismus`
USA/International: `usa` · `trump` · `oligarchie` · `geopolitik` · `migration`
Germany: `deutschland` · `afd` · `bundesregierung` · `wahlen`
AI/Tech: `ki` · `technologie` · `überwachung` · `datenschutz`
Philosophy: `philosophie` · `psychologie` · `ethik` · `buddhismus` · `vipassana`
Economy: `wirtschaft` · `soziale-ungleichheit`
Media: `medien` · `propaganda` · `desinformation`

**Rules:** Lowercase with hyphen · No personal name tags · Only relevant tags, no spam

---

## Copyright Guidelines

- Direct quotes: maximum 1–3 sentences
- Always cite source with timestamp link
- Quotes serve analysis — must be commented on
- Prefer paraphrase when possible
- No hosting of third-party audio/video files
- Paywall content: add `> [!tip]` callout recommending the original

---

## Tool Requirements

| Tool | Purpose | Install |
|---|---|---|
| `yt-dlp` | YouTube download | `brew install yt-dlp` (Mac) / `pip install yt-dlp` (Linux) |
| `ffmpeg` | Audio extraction | `brew install ffmpeg` (Mac) / `apt install ffmpeg` (Linux) |
| `mlx-whisper` | Transcription (Apple Silicon) | `pip install mlx-whisper` |
| `openai-whisper` | Transcription (Intel/CPU fallback) | `pip install openai-whisper` |
| Docker | Local wiki | Docker Desktop (Mac/Win) / `apt install docker.io` (Linux) |

Missing tools: explain which step requires them and offer install instructions for the detected OS.
Transcription tools are optional — if a transcript already exists, start from Step 4.
Docker is optional — notes work without the local wiki.
