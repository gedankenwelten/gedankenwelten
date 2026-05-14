---
name: hermes
description: Vollständige Pipeline vom Rohmaterial zur fertigen Note. YouTube, Podcast, Artikel → Transkript → Tiefenanalyse → Cross-Linking. Benannt nach Hermes — Bote zwischen den Welten, Namensgeber der Hermeneutik. Trigger — URL einfügen, "verarbeite", "neue note aus", "hermes".
---

# Hermes — Note-Pipeline

> *Hermes übersetzt zwischen den Welten — vom gesprochenen Wort zur geschriebenen Erkenntnis. Die Kunst der Interpretation, Hermeneutik, trägt seinen Namen.*

Vollständiger Prozess vom Rohmaterial zur fertigen, vernetzten Note.
Genutzte Agenten: **Humboldt · Sherlock · Montaigne**

---

## Schritt 0 — Humboldt: Sprecher-Recherche + DenkerVita

### 0a — DenkerVita prüfen

```bash
ls "content/DenkerVita/<Vorname Nachname>.md" 2>/dev/null
```

**Wenn DenkerVita existiert:**
- DenkerVita lesen → als Grundlage für den `> [!info] Wer spricht?`-Callout verwenden
- Humboldt-Recherche überspringen
- Note erhält am Ende des Callouts: `→ [[DenkerVita/<Name>|DenkerVita]]`

**Wenn keine DenkerVita existiert:**
- Humboldt-Recherche durchführen (0b)
- Nach der Note-Erstellung (Schritt 5) DenkerVita anlegen (0c)

---

### 0b — Humboldt: Recherche (nur wenn keine DenkerVita)

```
/agent humboldt
Sprecher: [Name]
Thema: [Videotitel]
```

---

### 0c — DenkerVita anlegen (nach Schritt 5, nur wenn neu)

**Pfad:** `content/DenkerVita/<Vorname Nachname>.md`

**Frontmatter:**
```yaml
---
title: <Name> — DenkerVita
tags: [denker-vita, <thema>, <herkunft>]
---
```

**Pflicht-Struktur:**
1. `## Biographischer Snapshot` — denselben `> [!info] Wer spricht?`-Callout wie in der Note
2. `## Biografie` — lebendig: Wendepunkte, Prägungen
3. `## Bücher & Publikationen` — Genialokal-Links: `https://www.genialokal.de/Suche/?q=nachname+titel`
4. `## Empfehlenswerte Videos & Vorträge`
5. `## Kernthesen` — 3–5 nummerierte Aussagen
6. `## Politische Einordnung` — wenn relevant
7. `## Verbindungen zu anderen Denkern` — Montaigne befüllt das
8. `## Notes` — Backlinks zu allen Notes über diese Person

**Anschließend aktualisieren:**
- `content/known-speakers.md` — Eintrag mit `**Status:** ✓ Vollanalyse → [[DenkerVita/<Name>]]`

Die Note erhält am Ende des Callouts: `→ [[DenkerVita/<Name>|DenkerVita]]`

> **⚠️ WIKILINK-PFAD-REGEL:** Alle Links zu DenkerVita-Notes den vollen Pfad verwenden: `[[DenkerVita/<Name>]]` — NICHT `[[<Name>]]`. Quartz löst kurze Pfade in Unterordnern nicht korrekt auf.

---

## Schritt 1 — Quelle klären

- **YouTube-Video**: URL verfügbar? → weiter zu Schritt 2.
- **Audio lokal**: Datei liegt lokal? → weiter zu Schritt 3 (Whisper).
- **Artikel / Website**: Defuddle-Skill verwenden, dann direkt Note erstellen (kein Transkript nötig).
- **TED-Talk**: Zuerst YouTube-ID per yt-dlp suchen: `yt-dlp ytsearch1:"Vorname Nachname Titel"`, dann wie YouTube.

**Zielordner für Transkripte:** `content/Transkripte/`

---

## Schritt 2 — YouTube: Untertitel herunterladen

```bash
# Deutsch zuerst
yt-dlp --write-auto-sub --skip-download --sub-lang de \
  --output "content/Transkripte/DATEINAME_%(title)s.%(ext)s" "URL"

# Fallback: Englisch
yt-dlp --write-auto-sub --skip-download --sub-lang en \
  --output "content/Transkripte/DATEINAME_%(title)s.%(ext)s" "URL"
```

**Namenskonvention:** `Nachname_Stichwort_` als Präfix.

---

## Schritt 2b — Video-Beschreibung auf Quellen prüfen

```bash
yt-dlp --get-description "URL"
```

Alle genannten Bücher, Artikel, Studien und Links extrahieren. In der Note als `## Weiterführende Quellen` einfügen — direkt vor `## Verbindungen`.

---

## Schritt 3 — Audio ohne Untertitel: mlx-whisper

### Chunked Transcription (Pflicht bei Audio > 30 Min)

```bash
# 1. Audio aus Video extrahieren (falls nötig)
ffmpeg -i "video.mp4" -vn -acodec pcm_s16le -ar 16000 "audio.wav"

# 2. Gesamtlänge ermitteln
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "audio.wav" | cut -d. -f1)

# 3. In 25-Minuten-Chunks aufteilen
CHUNK_SEC=1500
mkdir -p /tmp/whisper_chunks
i=0; START=0
while [ $START -lt $DURATION ]; do
  ffmpeg -y -i "audio.wav" -ss $START -t $CHUNK_SEC -c copy "/tmp/whisper_chunks/chunk_$(printf '%03d' $i).wav"
  START=$((START + CHUNK_SEC))
  i=$((i + 1))
done

# 4. Jeden Chunk transkribieren
for chunk in /tmp/whisper_chunks/chunk_*.wav; do
  mlx_whisper "$chunk" \
    --model "mlx-community/whisper-large-v3-turbo" \
    --language de \
    --output-format vtt \
    --output-dir /tmp/whisper_chunks/
done

# 5. VTT-Dateien zusammenführen
python3 .claude/scripts/merge_vtt_chunks.py \
  /tmp/whisper_chunks/ \
  "content/Transkripte/DATEINAME.vtt" \
  --chunk-duration $CHUNK_SEC

# 6. Aufräumen
rm -rf /tmp/whisper_chunks
```

**Kurze Dateien (< 30 Min):**
```bash
mlx_whisper "Pfad/zur/datei.mp3" \
  --model "mlx-community/whisper-large-v3-turbo" \
  --language de \
  --output-format vtt \
  --output-dir "content/Transkripte/"
```

---

## Schritt 4 — VTT → TXT konvertieren

```bash
# YouTube (klickbare Zeitstempel-Links)
python3 .claude/scripts/vtt_to_txt.py \
  "content/Transkripte/DATEI.vtt" \
  "content/Transkripte/DATEI_Transkript.txt" \
  "https://www.youtube.com/watch?v=VIDEO_ID"

# Podcast/lokal (nur Zeitmarken)
python3 .claude/scripts/vtt_to_txt.py \
  "content/Transkripte/DATEI.vtt" \
  "content/Transkripte/DATEI_Transkript.txt" \
  "local"
```

---

## Copyright-Leitlinien (immer einhalten)

- **Kurz halten:** Direkte Zitate maximal 1–3 Sätze.
- **Quelle immer angeben:** Zeitstempel-Link direkt beim Zitat.
- **Zitat dient der Analyse:** Zitate müssen kommentiert werden — kein reines Wiedergeben.
- **Paraphrase bevorzugen:** Wenn möglich Kernaussage in eigenen Worten.
- **Kein Hosting von Fremdmaterial:** Keine Audio- oder Video-Dateien von Dritten.
- **Paywall-Content:** Immer `> [!tip]`-Callout mit Empfehlung zum Original direkt nach der `Quelle:`-Zeile:

```markdown
> [!tip] [Kanal] unterstützen
> Diese Zusammenfassung ersetzt nicht das Original — sie macht Lust drauf. [Beschreibung + Link]
```

---

## Schritt 5 — Obsidian-Note erstellen (mit Aristoteles-Tiefe)

> [!important] Aristoteles-Standard
> Die Note-Erstellung folgt dem **Aristoteles-Skill** (`.claude/skills/aristoteles/SKILL.md`).
> Keine Zusammenfassung — sondern Analyse. Mindestens 1.200 Wörter Inhalt, 6–8 Abschnitte, ≥5 Zitate.

**Zielordner:**
- Zeitgeist-Note → `content/Zeitgeist/`
- Denker-Note → `content/Denker/`

### Dateiname-Konvention (URL-kompatibel)

**Format:** `Autor — Kurztitel.md`

**Regeln:**
- **Kein `&`** → `und` verwenden
- **Kein `:`** → weglassen oder durch Komma/Gedankenstrich ersetzen
- **Keine runden Klammern `()`** im Standardfall (Datum ins Frontmatter)
- **Em-Dash `—`** als Trennzeichen ist ok
- **Keine Umlaute** im Dateinamen → `ä→ae`, `ö→oe`, `ü→ue`, `ß→ss`
- **Datum im Dateinamen** nur bei Serien zur Disambiguierung

**Gut:** `Konstantin Flemig — Ukraine Gebietsgewinne 2026.md`
**Schlecht:** `Konstantin Flemig — Ukraine & Putin: Gebietsgewinne (12.04.2026).md`

---

### Wenn Zeitgeist-Note

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

---

## Inhalt
...

---

## Faktencheck
> [!success] Bestätigt — [Claim-Name]
> [Claim]. Quelle: [Titel](URL)

> [!warning] Vereinfacht — [Claim-Name]
> [Claim]. Quelle: [Titel](URL)

---

## Weiterführende Quellen
- [Titel](URL) — was es ist

---

## Verbindungen

### → [[Andere Note]]
Konzeptuelle Beziehung — nicht nur "beide beschäftigen sich mit X".

---

## Weiterdenken

> [!question] Was Aristoteles vielleicht gefragt hätte
> - [3–5 übergreifende Fragen]
```

---

### Wenn Denker-Note

```markdown
---
title: "Titel"
tags:
  - denker
  - thema-tag
aliases:
  - Kurzname
---

# Titel

Quelle: [Titel](URL)

> [!info] Wer spricht?
> **Name** (*Geburtsjahr, Ort*) — Kernbeschreibung.
>
> [2–3 Sätze: Lebensweg, Wendepunkte]
>
> Wichtigste Werke: *Titel* (Jahr)

---

## Inhalt

### [Kernkonzept]

[Zeitstempel] — Herleitung

> *„Direktes Zitat"*

> [!note] Eigene Einschätzung
> [Persönliche Reflexion]

---

## Verbindungen

### → [[Anderer Denker]]
Begründung der konzeptuellen Beziehung.

---

## Weiterdenken

> [!question] Was Aristoteles vielleicht gefragt hätte
> - [3–5 Fragen]
```

---

## Schritt 5b — Sokrates: Frageschicht

Nach Aristoteles die Note durch Sokrates' Augen lesen — nicht zum Umschreiben, sondern zum Herausfordern.

Sokrates fügt hinzu:
- **2–4 inline `> [!question]`-Callouts** nach substanziellen Abschnitten, wo eine These besonders stark oder kontraintuitiv ist
- **`## Weiterdenken`** am Ende mit 3–5 echten, nicht-rhetorischen Fragen

**Drei Fragetypen (mind. je 1):**
- *Adversarial* — greift die Kernthese direkt an
- *Konsequenz* — denkt zu Ende, was der Sprecher ausspart
- *Meta* — fragt nach Rahmen, Interesse, Voraussetzungen

Sokrates schreibt keine Antworten. Er öffnet.

---

## Schritt 5c — Sherlock: Faktencheck (nur Zeitgeist-Notes)

```
/agent sherlock
[vollständiger Note-Text]
```

Sherlocks Ausgabe einfügen:
1. `## Faktencheck` — nach dem Inhalt
2. `## Weiterführende Quellen (Sherlock)` — mit dem bestehenden Quellen-Abschnitt zusammenführen

---

## Schritt 6 — Montaigne: Cross-Linking

```
/agent montaigne
[neue Note Volltext]
```

Montaigne findet thematisch verwandte Notes per Glob und gibt Links mit Begründung aus.

**Nach Montaignes Ausgabe:**

1. Links in neue Note einfügen (`## Verbindungen`)
2. Bestehende Notes bidirektional verlinken: jede genannte Note öffnen, `[[neue Note]]` im Verbindungs-Abschnitt ergänzen

---

## Schritt 7 — Quellen & Links.md aktualisieren

```markdown
## [Autorenname / Thema]

| | |
|---|---|
| **Vortrag / Video** | [Titel](URL) |
| **Notiz** | [[Note-Dateiname]] |
| **Transkript** | `content/Transkripte/Dateiname.txt` |
```

---

## Schritt 8 — Commit & Push

```bash
git add -A && git commit -m "note-pipeline: <Autor> — <Thema>"
git push origin main
```

> **Lokale Wiki:** Wenn `docker compose up` läuft, wird die Wiki **automatisch neu gebaut** sobald die Note-Datei gespeichert wird — kein Extra-Schritt nötig. Wiki öffnen: http://localhost:9999

---

## Checkliste

- [ ] DenkerVita geprüft: existiert → lesen; existiert nicht → Humboldt + DenkerVita anlegen
- [ ] Download / Transkription abgeschlossen
- [ ] Video-Beschreibung auf Quellen geprüft (Schritt 2b)
- [ ] VTT → TXT konvertiert
- [ ] Note erstellt (Aristoteles-Standard: ≥1200 Wörter, ≥5 Zitate)
- [ ] Callout aus DenkerVita + Link `→ [[DenkerVita/<Name>|DenkerVita]]`
- [ ] Sokrates: 2–4 inline `> [!question]`-Callouts + `## Weiterdenken` mit 3–5 Fragen
- [ ] **Zeitgeist:** Sherlock-Faktencheck eingefügt
- [ ] **Denker:** Tiefenanalyse — lebendige Biografie, Kernkonzepte, 2–3 Eigene Einschätzungen
- [ ] **Denker (neu):** DenkerVita angelegt + `known-speakers.md` aktualisiert
- [ ] Montaigne Cross-Linking + bidirektionale Links
- [ ] `## Weiterdenken` mit Aristoteles-Fragen
- [ ] Eintrag in `content/Quellen & Links.md`
- [ ] Commit & Push
