---
name: gedankenwelt
description: Vollständige Pipeline vom Rohmaterial zur fertigen Note. YouTube, Podcast, Artikel → Transkript → Tiefenanalyse → Cross-Linking. Vollständige Note-Pipeline. Trigger — URL einfügen, "verarbeite", "neue note aus", "gedankenwelt".
---

# Gedankenwelten Note Pipeline

Vollständiger Prozess vom Rohmaterial zur fertigen, vernetzten Obsidian-Note.
Nutze immer sämtliche Agenten. Dies sind folgende:

- Humboldt
- Sherlock
- Montaigne

Zusätzlich: RAG ist jetzt produktiv und wird in dieser Pipeline aktiv genutzt.

> [!important] Seit 08.10.2026: Die Hauptinstanz ist Managerin, die Agenten laufen im Fächer
> Humboldt, Sherlock und Montaigne brauchen nur das **Transkript**, nicht die fertige Note. Darum
> starten sie **gleichzeitig im Hintergrund**, sobald das Transkript steht (→ **Schritt 4b — Der
> Fächer**), und die Hauptinstanz schreibt währenddessen die Note. Sie behält alles im Blick: liest
> jeden Agenten-Bericht mit Urteil, baut ein, was trägt, und verwirft, was nicht trägt. Die Note
> schreibt **immer die Hauptinstanz selbst**, im Gespräch mit Andreas — delegiert wird Recherche,
> nie die Hand. Alter, rein sequenzieller Stand: Git-Tag `gedankenwelt-skill-vor-faecher`.

---

## RAG-Integration (Pflicht, Stand: Mai 2026)

Gedankenwelten-Notes werden nicht mehr nur manuell vernetzt, sondern mit RAG unterstützt.
Alle Gedankenwelten-Notes leben in einer **eigenen Qdrant-Collection `gedankenwelten`** — strikt getrennt von privaten Daten (Opus, Paperless).

**Dedizierte Endpoints (n8n):**
- `POST <dein-rag-server>/webhook/query-gedankenwelten` — Hybrid Search + Reranker + Graph-Expansion
- `POST <dein-rag-server>/webhook/ingest-gedankenwelten` — Section-aware Chunking → Qdrant

> [!warning] Nie die alten Endpoints `/webhook/query` oder `/webhook/ingest` verwenden!
> Diese zeigen auf die `knowledge`-Collection (privat). Gedankenwelten hat eigene Endpoints.

**Wofür in dieser Pipeline:**
1. **Vor Montaigne (Step 6a):** RAG liefert thematisch ähnliche Notes + Querbezüge als Input für Cross-Linking.
2. **Nach finaler Note (Step 6b):** Note wird sofort in RAG eingespeist, damit Folgeanfragen sie direkt sehen.
3. **Nach DenkerVita (Step 0c):** DenkerVita wird ebenfalls in RAG eingespeist.
4. **Nach Bidirektional-Linking (Step 6):** Jede modifizierte bestehende Note wird re-ingestiert.

**Minimaler Query-Body:**
```json
{
  "question": "Welche bestehenden Gedankenwelten-Notes passen thematisch zu <Titel/These>?",
  "top_k": 12
}
```

**Minimaler Ingest-Body:**
```json
{
  "path": "content/Zeitgeist/Dateiname.md",
  "content": "<vollstaendiger markdown-inhalt der note>",
  "media_type": "text"
}
```

**Wichtig:** `path` muss der Vault-Pfad sein. Darueber werden `note_type`, `hemisphere` und Dedup korrekt erkannt.

> [!important] Response-Format (Query + Ingest)
> Beide Endpoints liefern ein **JSON-Array**, kein Objekt: `[{answer, sources, ...}]`.
> Beim Parsen immer zuerst `[0]` nehmen: `d = json.load(sys.stdin)[0]`, dann `d.get('sources', [])`.
> **Nie** direkt `d.get(...)` auf die rohe Response anwenden — das schlägt fehl.

---

## Schritt -1 — Quellen-Check (vor dem Start)

Bevor die Pipeline losläuft: kurze ehrliche Einschätzung aus meiner Perspektive.

**Drei Fragen:**

1. **Wer spricht?** — Ist die Person/Quelle erkennbar seriös, oder gibt es ein offensichtliches Agenda-Problem? (Clickbait, reine Empörungsmaschine, bekannte Desinformationsquelle)

2. **Thematische Passung** — Fügt das etwas zum Gedankenwelten-Anspruch hinzu? Aufklärung, Reflexion, Tiefe — oder ist es eher oberflächlich / polemisch / bereits gut abgedeckt?

3. **Vipassana-Filter** — Würde diese Note jemanden aufklären oder eher verwirren? Gibt es eine reflektierte Grundhaltung, oder ist es reine Empörung ohne Erkenntnisgewinn?

**Dann eine ehrliche Empfehlung:**
- ✅ **Grünes Licht** — weiter mit der Rubrik-Wahl (Schritt -0.5)
- ⚠️ **Gelbes Licht** — kurzer Hinweis, was mich zögern lässt. Andreas entscheidet.
- 🛑 **Rotes Licht** — Begründung warum ich die Note nicht empfehle. Andreas entscheidet trotzdem final.

> Diese Einschätzung ist mein ehrlicher Bias — nicht Zensur. Das Ziel ist, Andreas aufmerksam zu machen, nicht zu blockieren. Wenn er trotz gelbem oder rotem Licht weitermachen will: Pipeline läuft.

---

## Schritt -0.5 — Rubrik-Entscheidung (gemeinsam)

Direkt nach dem Quellen-Check, **bevor** Humboldt o.ä. startet: gemeinsam festlegen, in welche der drei Rubriken die Note gehört. Das bestimmt Zielordner, Typ-Tag, Note-Aufbau und welche Schritte greifen (DenkerVita, Sherlock).

**Ich schlage auf Basis der Quellen-Einschätzung eine Rubrik vor — mit einem Satz Begründung — und Andreas bestätigt oder korrigiert.** Erst danach läuft die Pipeline weiter.

| Rubrik | Wann | Kern |
|---|---|---|
| **Denker** | Tiefenanalyse *einer* Person und ihres Werks/Denkens | Das Denken einer Stimme in der Tiefe |
| **Zeitgeist** | Geist der *Zeit* — tagesaktueller Diskurs, Politik, Gesellschaft, Interviews | Was passiert gerade, und was bedeutet es? |
| **Geistesblitz** ⚡ | Grundsätzliches Wissen & Schöpferkraft — Wissenschaft, Philosophie, Psychologie, Technik | Wissen über Welt und Geist, zeitlos & quellenbasiert (z.B. Wissenschafts-Dokus, Erklärformate) |

**Faustregel Zeitgeist vs. Geistesblitz:** Was das Jahr überdauert → **Geistesblitz**; was das Jetzt kommentiert → **Zeitgeist**. Im Zweifel fragen, nicht raten.

**Folgen der Wahl:**
- **Denker** → Zielordner `content/Denker/`, Typ-Tag `denker`, Denker-Tiefenanalyse, DenkerVita-Pflicht (Schritt 0/0c), Faktencheck nur bei empirischen Claims.
- **Zeitgeist** → Zielordner `content/Zeitgeist/`, Typ-Tag `zeitgeist`, Sherlock-Faktencheck (Schritt 5b) Pflicht.
- **Geistesblitz** → Zielordner `content/Geistesblitz/`, Typ-Tag `geistesblitz`, Aufbau wie Zeitgeist *mit* analytischer Denker-Tiefe; Sherlock-Faktencheck bei empirischen Claims (bei Wissenschaftsthemen meist Pflicht). DenkerVita nur, wenn eine *einzelne* Person im Zentrum steht — bei narrierten Dokus mit mehreren Experten i.d.R. nicht.

> Abgrenzung & Migrations-Regeln im Detail: `.claude/rules/gedankenwelten.md` → Abschnitt „Geistesblitz".

---

## Schritt 0 — Humboldt: Sprecher-Recherche + DenkerVita

### 0a — DenkerVita prüfen

Bevor Humboldt recherchiert: prüfen, ob bereits eine DenkerVita existiert.

```bash
ls "content/DenkerVita/<Vorname Nachname>.md" 2>/dev/null
```

**Wenn DenkerVita existiert:**
- DenkerVita lesen → Biographischen Snapshot (`> [!info] Wer spricht?`-Sektion) als Grundlage für den Callout verwenden
- Humboldt-Recherche (0b) **überspringen**
- Note erhält am Ende des Callouts: `→ [[content/DenkerVita/<Name>|DenkerVita]]`
- **⚠️ Pflicht — Vita mit der neuen Note füllen:** Die DenkerVita ist die Sammelstelle *aller* Notes zu einer Person. Darum nach der Note-Erstellung die neue Note in die `## Cortex-Notes`-Sektion der bestehenden Vita eintragen (`- [[<Note-Titel>]]`) **und die Vita re-ingestieren** (RAG, wie Schritt 6c). Das gilt jedes Mal, wenn eine Note zu einer Person mit bestehender Vita bearbeitet wird — nicht nur bei neu angelegten Vitas. So wächst die Vita mit jeder Note mit, statt auf dem Stand ihrer Erstellung einzufrieren.

**Wenn keine DenkerVita existiert:**
- Humboldt-Recherche durchführen (0b)
- Nach der Note-Erstellung (Schritt 5) DenkerVita anlegen (0c)

---

### 0b — Humboldt: Recherche (nur wenn keine DenkerVita)

> Läuft seit 08.10.2026 im **Fächer** (Schritt 4b) im Hintergrund, parallel zum Schreiben.

```
/agent humboldt
Sprecher: [Name aus Videotitel oder URL extrahieren]
Thema: [Videotitel]
```

Humboldts Ausgabe (Stichpunkte zu Person + Kontext) für die Note-Erstellung merken — sie liefert die Fakten für den `> [!info] Wer spricht?`-Callout.

Gilt für: YouTube-Videos, Podcasts, TED-Talks.
Bei Artikeln: nur wenn Autor-Kontext sinnvoll erscheint.

---

### 0c — DenkerVita anlegen (nach Schritt 5, nur wenn neu)

Wenn keine DenkerVita existierte: nach dem Erstellen der Note eine neue DenkerVita anlegen.

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
2. `## Biografie` — lebendig: Wendepunkte, Prägungen, nicht nur Stationen
3. `## Bücher & Publikationen` — **Genialokal Suchlinks (Pflicht-Methode):**
   - Genialokal-Link bauen: `https://www.genialokal.de/Suche/?q=autor+buchtitel+keywords` (Leerzeichen als `+`)
   - Kurz aber spezifisch: Nachname + Schlüsselwörter des Titels reichen aus
   - Beispiel: `https://www.genialokal.de/Suche/?q=clara+mattei+capital+order`
   - **Nicht** `searchhash=isbn%3D` verwenden — das funktioniert unzuverlässig
4. `## Empfehlenswerte Videos & Vorträge` — mit YouTube-Links
5. `## Kernthesen` — 3–5 nummerierte Kernaussagen
6. `## Politische Einordnung` — wenn relevant
7. `## Verbindungen zu anderen Denkern` — Montaigne befüllt das
8. `## Cortex-Notes` — Backlinks zu allen Notes über diese Person

**Anschließend aktualisieren:**
- `content/known-speakers.md` — Eintrag mit `**Status:** ✓ Vollanalyse → [[content/DenkerVita/<Name>]]`
- `content/DenkerVita/Alle Denker.md` — Zeile mit Link + Einzeiler

**RAG-Ingest der DenkerVita (Pflicht):**
```bash
VITA_PATH="content/DenkerVita/<Vorname Nachname>.md"
python3 -c "
import json
with open('$VITA_PATH') as f: content = f.read()
print(json.dumps({'path': '$VITA_PATH', 'content': content, 'media_type': 'text'}))
" | curl -s --max-time 120 -X POST "<dein-rag-server>/webhook/ingest-gedankenwelten" \
  -H "Content-Type: application/json" -d @- | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  RAG: {d[0][\"chunks_ingested\"]} chunks')"
```

Die Note erhält am Ende des Callouts den Link: `→ [[content/DenkerVita/<Name>|DenkerVita]]`

> **⚠️ WIKILINK-PFAD-REGEL:** Alle Wikilinks zu DenkerVita-Notes **MÜSSEN** den vollen Pfad ab Vault-Root verwenden: `[[content/DenkerVita/<Name>]]` — NICHT `[[DenkerVita/<Name>]]`. Quartz (unser Static-Site-Generator) löst relative Pfade nicht korrekt auf. Das gilt überall: in Zeitgeist-Notes, in DenkerVita-Notes untereinander, in known-speakers.md, in Alle Denker.md.

---

## Schritt 1 — Quelle klären

Bevor etwas heruntergeladen wird:

- **YouTube-Video**: URL direkt verfügbar? → weiter zu Schritt 2.
- **PeerTube-Video** (föderiertes Netz, z.B. `video.mondoweiss.net`; gefunden via `/sepia`):
  yt-dlp kann PeerTube-URLs direkt. Meist **keine Untertitel** → Audio ziehen
  (`yt-dlp -x --audio-format wav --postprocessor-args "-ar 16000 -ac 1"`) und weiter zu Schritt 3
  (mlx-whisper — **Sprache beachten**, oft `--language en`). Zeitstempel-Links:
  `[▶ 12:34](URL?start=754s)`. Schritt 11b (Playlist-Umzug) entfällt. Provenienz von Instanz +
  Kanal gehört in die Note (→ `.claude/skills/sepia/SKILL.md`).
- **Podcast (Steady / RSS)**: Siehe Podcast-Workflow unten → MP3 aus RSS-Feed extrahieren → weiter zu Schritt 3 (Whisper).
- **Podcast (MP3/Audio lokal)**: Liegt die Datei bereits lokal? → weiter zu Schritt 3 (Whisper).
- **Apple Podcasts URL**: ⚠️ Apple-Podcasts sind DRM-geschützt (FairPlay). Stattdessen den Steady-RSS-Feed verwenden (siehe unten).
- **TED-Talk**: Zuerst YouTube-ID per yt-dlp suchen (`yt-dlp ytsearch1:"Vorname Nachname Titel"`), dann wie YouTube behandeln.
- **Artikel / Website**: Defuddle-Skill verwenden, dann direkt Note erstellen (kein Transkript nötig).

**Zielordner für Transkripte:** `content/Transkripte/`

### Podcast-Workflow: Steady-RSS → MP3 → Whisper

Für Podcasts hinter Paywalls (Steady, Apple Podcasts Abo) gibt es private RSS-Feeds mit direkten MP3-Links. Die Feed-URLs liegen in `.env` (gitignored).

**Bekannte Feeds (Variablen in `.env`):**

| Podcast | Env-Variable |
|---|---|
| Die Neuen Zwanziger (Salon) | `STEADY_RSS_NEUEZWANZIGER` |

**MP3 aus RSS-Feed extrahieren:**

```bash
# .env laden und Feed abrufen
source .env
curl -s "$STEADY_RSS_NEUEZWANZIGER" | grep -B5 "SUCHWORT_AUS_TITEL" | grep "enclosure" | grep -oP 'url="[^"]*"'

# MP3 herunterladen
curl -L -o "content/Transkripte/Podcast_Titel.mp3" "ENCLOSURE_URL"
```

Dann weiter mit Schritt 3 (Whisper-Transkription). **Achtung:** Podcast-Episoden sind oft 60-120 Min lang — Chunked Transcription ist hier Pflicht.

**Wichtig:** Apple-Podcasts-URLs (`podcasts.apple.com`) können *nicht* direkt verarbeitet werden — immer den Steady-RSS-Feed verwenden. Die Apple-Downloads sind HLS-fragmentiert und FairPlay-DRM-verschlüsselt.

---

## Schritt 2 — YouTube: Untertitel herunterladen

```bash
# Deutsch zuerst probieren
yt-dlp --write-auto-sub --skip-download --sub-lang de \
  --output "content/Transkripte/DATEINAME_%(title)s.%(ext)s" "URL"

# Bei HTTP 429 oder fehlendem Deutsch: Englisch als Fallback
yt-dlp --write-auto-sub --skip-download --sub-lang en \
  --output "content/Transkripte/DATEINAME_%(title)s.%(ext)s" "URL"
```

**Namenskonvention:** `Nachname_Stichwort_` als Präfix (z.B. `Haidt_Moral_Roots_`).

---

## Schritt 2b — YouTube: Video-Beschreibung auf Quellen prüfen

Direkt nach dem Download die Video-Beschreibung abrufen und auf genannte Quellen prüfen:

```bash
yt-dlp --get-description "URL"
```

**Was zu extrahieren ist:**
- Bücher, Artikel, Studien (mit Autor, Titel, ggf. Link)
- Weiterführende YouTube-Videos oder Playlists
- Erwähnte Websites, Institutionen, Projekte
- Alle explizit verlinkten URLs

**Wo einfügen:** In der Note einen Abschnitt `## Weiterführende Quellen` anlegen — direkt vor `## Verbindungen`. Format:

```markdown
## Weiterführende Quellen

*Aus der Video-Beschreibung:*

- [Titel](URL) — Kurzbeschreibung was es ist
- Autor: *Buchtitel* — Kontext (z.B. „im Gespräch erwähnt")
- ...
```

**Wenn die Beschreibung keine Quellen enthält:** Abschnitt weglassen, nicht als leere Section in die Note schreiben.

> Manche Youtuber (Scobel, Jung & Naiv, Monitor u.a.) listen systematisch alle im Video genannten Werke und Links. Diese sind oft wertvoller als Transkript-Fundstellen, weil sie von den Sprechern selbst kuratiert wurden.

---

## Schritt 3 — Audio/Video ohne Untertitel: mlx-whisper (Mac M-Series)

Für lokale Audio-/Video-Dateien ohne Untertitel.

### Chunked Transcription (Pflicht bei Audio > 30 Min)

Whisper verliert bei großen Dateien an Qualität und Performance. **Immer in ~25-30 Min Chunks aufteilen**, einzeln transkribieren, dann zusammenführen.

```bash
# 1. Audio aus Video extrahieren (falls nötig)
ffmpeg -i "video.mp4" -vn -acodec pcm_s16le -ar 16000 "audio.wav"

# 2. Gesamtlänge ermitteln (in Sekunden)
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "audio.wav" | cut -d. -f1)
echo "Gesamtlänge: $((DURATION / 60)) Minuten"

# 3. In 25-Minuten-Chunks aufteilen (1500 Sekunden)
CHUNK_SEC=1500
mkdir -p /tmp/whisper_chunks
i=0; START=0
while [ $START -lt $DURATION ]; do
  ffmpeg -y -i "audio.wav" -ss $START -t $CHUNK_SEC -c copy "/tmp/whisper_chunks/chunk_$(printf '%03d' $i).wav"
  START=$((START + CHUNK_SEC))
  i=$((i + 1))
done
echo "$i Chunks erstellt"

# 4. Jeden Chunk einzeln transkribieren
for chunk in /tmp/whisper_chunks/chunk_*.wav; do
  mlx_whisper "$chunk" \
    --model "mlx-community/whisper-large-v3-turbo" \
    --language de \
    --output-format vtt \
    --output-dir /tmp/whisper_chunks/
done

# 5. VTT-Dateien zusammenführen (Zeitstempel korrigieren)
python3 .claude/scripts/merge_vtt_chunks.py \
  /tmp/whisper_chunks/ \
  "content/Transkripte/DATEINAME.vtt" \
  --chunk-duration $CHUNK_SEC

# 6. Aufräumen
rm -rf /tmp/whisper_chunks
```

**Kurze Dateien (< 30 Min):** Können direkt ohne Chunking transkribiert werden:

```bash
mlx_whisper "Pfad/zur/datei.mp3" \
  --model "mlx-community/whisper-large-v3-turbo" \
  --language de \
  --output-format vtt \
  --output-dir "content/Transkripte/"
```

> Läuft auf Apple GPU/Neural Engine — deutlich schneller als CPU-Whisper. Kein Background-Task nötig.
> **Erfahrungswert:** Im 25-30 Min Fenster arbeitet Whisper schnell und präzise. Bei längeren Dateien sinkt sowohl Geschwindigkeit als auch Qualität erheblich.

---

## Schritt 4 — VTT → TXT konvertieren

**Variante A: YouTube-VTT** (mit klickbaren Zeitstempel-Links):

```bash
python3 .claude/scripts/vtt_to_txt.py \
  "content/Transkripte/DATEI.vtt" \
  "content/Transkripte/DATEI_Transkript.txt" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Variante B: Podcast/Whisper-VTT** (ohne Links, nur Zeitmarken):

```bash
python3 .claude/scripts/vtt_to_txt.py \
  "content/Transkripte/DATEI.vtt" \
  "content/Transkripte/DATEI_Transkript.txt" \
  "local"
```

> Für Podcasts `"local"` als URL übergeben — der Konverter erkennt fehlende YouTube-URL und gibt nur Zeitmarken im Format `[▶ 3:24]` aus.

---

## Schritt 4b — Der Fächer: Agenten parallel starten (seit 08.10.2026)

Sobald `_Transkript.txt` und die Video-Beschreibung da sind **und** Quellen-Check (Schritt -1) und
Rubrik (Schritt -0.5) entschieden sind, startet die Hauptinstanz **in einer einzigen Nachricht** die
Hintergrund-Agenten (`run_in_background: true`, Modell Opus). Danach liest sie selbst das Transkript
und beginnt mit Schritt 5 — sie wartet nicht.

**Erster Fächer — sofort, braucht nur das Transkript:**

| Agent | Auftrag | Liefert | Wird eingebaut in |
|---|---|---|---|
| **Humboldt** | nur wenn keine DenkerVita existiert (Schritt 0a prüfen) | fertige Vita-Datei + Index-Zeilen | Schritt 0c |
| **Sherlock** | Faktencheck **am Transkript**: Pfad, Video-URL, bekannte heikle Claims mitgeben | `## Faktencheck`-Block + „Still korrigieren“-Liste | Schritt 5b |
| **Montaigne** | Verbindungs-Kandidaten aus Transkript + Thema (RAG `"answer": false`) | 8–12 Kandidaten mit Begründung, Rückverweis-Sätze | Schritt 6 |

**Zweiter Fächer — sobald Andreas die Nachbesprechungs-Themen gewählt hat (Schritt 5d.1):**
je Thema ein Recherche-Agent (Forschung mit DOI via `wiss_search.py`, Fälle, Stimmen im Bestand mit
exaktem Abschnitt-Anker) — und, sobald der Kern der Note feststeht, das **Banner** (Schritt 10c) als
eigener Hintergrund-Agent. Die Hauptinstanz schreibt derweil weiter.

**Regeln für den Fächer:**
- **Agenten schreiben nur eigene neue Dateien** (Humboldt die Vita, Banner-Agent die JPEGs) oder
  liefern Text. Gemeinsam genutzte Dateien — die Note selbst, Altnotes, Panoramen, Log, Journal,
  `index.md`, Kataloge, `known-speakers.md`, `Alle Denker.md` — fasst **nur die Hauptinstanz** an.
  Humboldt bekommt darum den Zusatz: *Index-Dateien nicht bearbeiten, Zeilen im Bericht liefern.*
- **Kein Agent ingestiert, committet oder deployt.** Der Embed-Server ist single-threaded; RAG-Ingest
  läuft am Ende nacheinander durch die Hauptinstanz (Schritt 6b/6c).
- **Sherlocks Befunde fließen schon beim Schreiben ein:** Was falsch ist, wird im Text nicht
  wiederholt, sondern eingeordnet; „Still korrigieren“ wird still korrigiert. Der Callout-Block kommt
  in Schritt 5b dazu.
- **Urteil bleibt oben:** Jeder Bericht wird gelesen und gewogen — Montaignes Kandidaten werden gegen
  die fertige Note geprüft (passt die Brücke wirklich?), Sherlocks Verdikte gegen das Transkript
  gegengelesen, Banner angesehen. Was nicht trägt, fällt raus.
- **Ankündigen** im Routing-Format, z. B.:
  `→ [FÄCHER] Humboldt · Sherlock · Montaigne im Hintergrund | ich schreibe die Note`

---

## Copyright-Leitlinien (immer einhalten)

Alle Notes basieren auf fremden Inhalten — das Zitatrecht (§ 51 UrhG) erlaubt Zitate nur unter diesen Bedingungen:

- **Kurz halten:** Direkte Zitate maximal 1–3 Sätze. Kein ganzer Absatz wörtlich aus dem Transkript.
- **Quelle immer angeben:** Zeitstempel-Link direkt beim Zitat — das ist gleichzeitig der urheberrechtliche Nachweis.
- **Zitat dient der Analyse:** Zitate müssen kommentiert, eingeordnet oder bewertet werden — kein reines Wiedergeben.
- **Paraphrase bevorzugen:** Wenn möglich Kernaussage in eigenen Worten, direktes Zitat nur wenn die genaue Formulierung relevant ist.
- **Kein Hosting von Fremdmaterial:** Keine Audio-, Video- oder PDF-Dateien von Dritten in den Vault oder auf die Website.
- **Titelbilder/Thumbnails:** Nicht verwenden — immer nur den Link zum Original.
- **Empfehlung bei Paywall-Content:** Wenn der Inhalt hinter einer Paywall liegt (Steady, Patreon etc.), **immer** einen `> [!tip]`-Callout einfügen, der den Originalkanal empfiehlt. Platzierung: direkt nach der `Quelle:`-Zeile, vor dem `> [!info] Wer spricht?`-Callout. Format:

```markdown
> [!tip] Salon unterstützen
> Diese Zusammenfassung ersetzt nicht das Original — sie macht Lust drauf. Der Lektüre-Salon der Neuen Zwanziger ist einer der besten deutschsprachigen Podcasts. Unterstützenswert: [steady.page/de/neuezwanziger](https://steady.page/de/neuezwanziger)
```

  Text und Link an den jeweiligen Kanal anpassen. Gilt für alle Paywall-Quellen (Steady, Patreon, Substack etc.).

---

## Schritt 5 — Obsidian-Note erstellen (mit Aristoteles-Tiefe)

> [!important] Aristoteles-Standard
> Die Note-Erstellung folgt dem **Aristoteles-Skill** (`.claude/skills/aristoteles/SKILL.md`).
> Keine Zusammenfassung — sondern Analyse. Qualitätsmetriken:
> - Inhalt ≥ 1.200 Wörter
> - 6–8 Kernabschnitte à 150+ Wörter
> - ≥ 5 direkte Zitate mit Timestamp
> - Eigenständige Einordnung in jedem Abschnitt
>
> **Self-Check nach dem Schreiben.** Falls Metriken nicht erreicht: zweiter Durchgang mit gezieltem Transkript-Nachschlagen.

> [!danger] Keine KI-Floskeln — **beim Schreiben**, nicht erst hinterher
> Die Streichliste `.claude/skills/gedankenpoesie/references/ki-tells.md` gilt **schon für den ersten
> Entwurf**. Sie hinterher wegzuputzen ist teuer und gelingt nie ganz. Die drei, die in unseren Notes
> wirklich beißen:
>
> 1. **Negative Parallelismen** (`nicht X, sondern Y`) — der häufigste Verräter. **Höchstens *eine* pro
>    Note**, dort wo sie wirklich kippt. Alle anderen auflösen: den positiven Kern direkt setzen
>    („Das Problem ist gesellschaftlich, nicht technisch.") oder die Spannung erzählen. ⚠️ **Zitate und
>    Faktencheck-Verdikte sind ausgenommen** — wenn der Sprecher selbst so argumentiert, bleibt das stehen.
> 2. **Häufungswörter** — *Geflecht · verwoben · navigieren · unterstreichen · vielschichtig ·
>    Spannungsfeld · Resonanz · zutiefst · im Kern · letztlich · gewissermaßen · nicht zuletzt ·
>    darüber hinaus · Wechselspiel · entfalten · beleuchten*. Drei davon in einem Absatz = Durchschnittsregister.
> 3. **Autoritäts-Floskeln & generische Schlüsse** — „Die eigentliche Frage ist…", „Was wirklich zählt…",
>    „Es bleibt spannend, wohin die Reise geht."
>
> Dazu: Kopula-Vermeidung („fungiert als" → „ist"), Partizip-Anhängsel („…, was die Dringlichkeit
> verdeutlicht"), Dreierfiguren-Reflex. **Maß halten** — es geht um Tendenz, nicht um Nulltoleranz;
> Gedankenstriche, Callouts und Boldface sind Hausstil und bleiben.

> [!tip] Journalistisches Register (still gewählt, angekündigt)
> Für Zeitgeist/Denker/Geistesblitz wählt aristoteles beim Schreiben still eine journalistische Hand
> (Kisch, Tucholsky, Orwell, Roth, Didion, Haffner, Kapuściński …) — nach der **Temperatur der Geschichte**,
> rubrik-übergreifend erlaubt, Anker im Zweifel Orwell-Klarheit. Das verbessert den KI-Speech schon bei der
> Entstehung (das stille Register — abgegrenzt von der benannten *Kür* in Schritt 5c). aristoteles kündigt
> die Wahl **vor dem Schreiben in einer Zeile an** (`→ [STIL: <Hand>] <Rubrik> — <warum>`), damit Andreas
> mitlernt. Details: `.claude/skills/aristoteles/references/journalismus.md`.

**Zielordner** (gemäß Rubrik-Entscheidung aus Schritt -0.5):
- Zeitgeist-Note → `content/Zeitgeist/`
- Denker-Note → `content/Denker/`
- Geistesblitz-Note → `content/Geistesblitz/` (Aufbau wie Zeitgeist mit Denker-Tiefe; Typ-Tag `geistesblitz`)

Den `> [!info] Wer spricht?`-Callout immer auf Basis von Humboldts Briefing (Schritt 0) formulieren — nicht aus dem Gedächtnis erfinden.

### Dateiname-Konvention (URL-kompatibel)

**Format:** `Autor — Kurztitel.md`

**Regeln:**
- **Kein `&`** → `und` verwenden (oder weglassen)
- **Kein `:`** → weglassen oder durch Komma/Gedankenstrich ersetzen — Doppelpunkte machen Probleme in URLs und Dateisystemen
- **Keine runden Klammern `()`** → Datum gehört ins Frontmatter, nicht in den Dateinamen
- **Em-Dash `—` als Trennzeichen** ist ok (wird zu `%E2%80%94`, funktioniert stabil)
- **Keine Umlaute** → `ä→ae`, `ö→oe`, `ü→ue`, `ß→ss` — nur im Dateinamen, nicht im `title:`-Frontmatter oder Fließtext. Quartz würde `ä→a` sluggen, was semantisch falsch sein kann (`Stärke→Starke` vs. `Stärke→Staerke`).
- **Datum im Dateinamen** nur bei **Serien** zur Disambiguierung: z.B. `Staiy — News Machtmissbrauch CDU CSU (25.03.2026)` wenn mehrere Staiy-News-Folgen existieren
- **Länge:** max. ~60 Zeichen inkl. Autor — lieber kürzen als den Videotitel übernehmen

**Gut:**
```
Konstantin Flemig — Ukraine Gebietsgewinne 2026.md
MONITOR — AfD-Erfolg trotz Skandalen.md
Christoph Butterwegge — Armut NEU DENKEN.md
Staiy — News Orbán-Wahl, Katharina Reiche und Iran (12.04.2026).md
Barbara Schmitz und Giovanni Maio — Verletzlichkeit als Staerke.md
Goetz Aly — Wie konnte das geschehen.md
```

**Schlecht:**
```
Konstantin Flemig — Ukraine Gebietsgewinne & Putin unter Druck (12.04.2026).md  ← & und () brechen URLs
MONITOR — AfD-Erfolg trotz Skandalen: Warum wählen so viele Menschen die AfD? – MONITOR.md  ← : und Videotitel 1:1 übernommen
Staiy — News: Orbán-Wahl, Reiche und Iran.md  ← : im Titel macht Probleme
Barbara Schmitz und Giovanni Maio — Verletzlichkeit als Stärke.md  ← Umlaut im Dateinamen → Quartz sluggt zu "Starke"
```

---

### Wenn Zeitgeist-Note

> [!warning] `date:` = **Verarbeitungstag (heute)**, NICHT das Quelldatum des Videos/Podcasts
> Der Karten-Feed (`computeTier` in `DesktopFeed.tsx`) liest `date:` als Eintrittsdatum in die
> Gedankenwelten und sortiert danach in Tier 0 („neu", ≤ 7 Tage). Trägt man hier das
> Veröffentlichungsdatum der Quelle ein (z.B. ein 2 Wochen altes Video), fällt die frische Note sofort
> auf Tier 4 („alt") und **sinkt im Feed nach unten**, obwohl sie gerade erst entstand. Darum: `date:` =
> **heutiges Datum**. Das Quelldatum gehört in die `Quelle:`-Zeile / den Fließtext, nie ins `date:`.
> (Das Startseiten-Journal nimmt ohnehin das Git-Erstellungsdatum — nur der Feed hängt an `date:`.)

```markdown
---
title: "Titel"
date: DD.MM.YYYY   # = HEUTE (Verarbeitungstag), nicht das Video-/Podcast-Datum
tags:
  - zeitgeist
  - thema-tag
  - year-XXXX
aliases:
  - Kurzname
---

# Titel

> [!abstract] Worum es geht
> (2–4 Sätze: Worum geht es? Worauf lässt man sich ein? Erste Zeile entspricht dem `description:`-Frontmatter.)

Quelle: [Titel](https://www.youtube.com/watch?v=VIDEO_ID)

> [!info] Wer spricht?
> **Name** — Kurzbeschreibung (Rolle, Expertise, Kontext)
>
> → [[content/DenkerVita/<Name>|DenkerVita]]

---

## Inhalt
...

---

## Publikumsfragen   ← Pflicht, wenn die Folge eine Fragerunde hat (Jung & Naiv!) — Regeln: aristoteles, „Publikumsfragen“
*[Wer moderiert, wie der Chat war.]*

**[Frage]** [▶ mm:ss](URL&t=…) — [Antwort mit Substanz; Nachfragen des Moderators; eigene Einwände als *(Jessens eigener Einwand)*]

---

## Faktencheck
> [!success] Bestätigt — [Claim-Name]
> [Claim]. Quelle: [Titel](URL)

> [!warning] Vereinfacht — [Claim-Name]
> [Claim]. [Warum vereinfacht]. Quelle: [Titel](URL) *(oder: Keine unabhängige Quelle gefunden)*

> [!danger] Falsch — [Claim-Name]
> [Claim]. [Warum falsch]. Quelle: [Titel](URL)

**Pflicht:** Jeder Faktencheck-Eintrag braucht eine Quellenangabe — entweder einen verlinkten Artikel oder den expliziten Hinweis „Keine unabhängige Quelle gefunden". Kein Eintrag ohne Transparenz über die Grundlage.

---

## Weiterführende Quellen
*Aus der Video-Beschreibung:* ← immer prüfen, auch wenn leer
- [Titel](URL) — was es ist

*Im Video/Artikel zitierte Quellen:* ← alle im Inhalt erwähnten Artikel, Studien, Berichte
- [Titel](URL) — Kurzbeschreibung

Dieser Abschnitt ist **immer Pflicht** — auch wenn nur das Originalvideo als Quelle bleibt. Fehlende Links durch Suche nachrecherchieren (WebSearch).

---

## Verbindungen

### → [[Andere Note]]

Konzeptuelle Beziehung — nicht nur "beide beschäftigen sich mit X", sondern: wie ergänzen/widersprechen sie sich?

### → [[Weitere Note]]

Begründung der Verbindung.
```

---

### Wenn Denker-Note

Denker sind das Fundament des Projekts — sie werden tiefer analysiert als Zeitgeist-Notes.
Maßstab: El-Mafaalani und Matthieu Ricard.

```markdown
---
title: "Titel"
tags:
  - denker
  - thema-tag
  - year-XXXX
aliases:
  - Kurzname
---

# Titel

> [!abstract] Worum es geht
> (2–4 Sätze: Worum geht es? Worauf lässt man sich ein? Erste Zeile entspricht dem `description:`-Frontmatter.)

Quelle: [Titel](https://www.youtube.com/watch?v=VIDEO_ID)

> [!info] Wer spricht?
> **Name** (*Geburtsjahr, Ort*) — Kernbeschreibung in einem Satz.
>
> [2–3 Sätze: Prägender Lebensweg, Wendepunkte, was ihn zur zentralen Frage gebracht hat]
>
> Wichtigste Werke: *Titel* (Jahr), *Titel* (Jahr)
> Kernkonzepte: Begriff1, Begriff2, Begriff3
>
> → [[content/DenkerVita/<Name>|DenkerVita]]

---

## Inhalt

### [Kernkonzept oder These]

[Zeitstempel] — [Erklärung in eigenen Worten + direktes Zitat]

> *„Direktes Zitat"*

[Was folgt daraus?]

> [!note] Eigene Einschätzung
> [Persönliche Reflexion: Wo resoniert das? Wo sehe ich Grenzen?
>  Was bedeutet das für konkrete Situationen oder eigenes Denken?]

### [Nächstes Kernkonzept]
...

---

## Faktencheck     ← nur bei empirischen Claims; bei reiner Philosophie weglassen
> [!success] Bestätigt — [Claim-Name]
> [Claim]. Quelle: [Titel](URL)

> [!warning] Vereinfacht — [Claim-Name]
> [Claim]. [Warum vereinfacht]. Quelle: [Titel](URL) *(oder: Keine unabhängige Quelle gefunden)*

**Pflicht:** Jeder Eintrag braucht eine Quellenangabe oder den expliziten Hinweis „Keine unabhängige Quelle gefunden".

---

## Weiterführende Quellen   ← nur wenn vorhanden
- [Titel](URL) — was es ist

---

## Verbindungen

### → [[Anderer Denker]]

Nicht nur "beide beschäftigen sich mit X", sondern: wie ergänzen/widersprechen sie sich konzeptuell?

### → [[Weitere Verbindung]]

Begründung.
```

**Pflicht für Denker-Notes:**
- Biografie lebendig: Wendepunkte, Prägungen — nicht nur Lebenslauf-Stationen
- Jedes Kernkonzept als eigener `###`-Abschnitt mit Zitat und Herleitung
- Mindestens 2–3 `> [!note] Eigene Einschätzung`-Callouts
- Verbindungen erklären die konzeptuelle Beziehung, nicht nur das Thema
- Faktencheck nur bei empirischen Claims (Neurowissenschaft, Geschichte, Statistik) — bei reiner Philosophie weglassen

### Zeitstempel-Links in der Note (Pflicht bei verfügbarem Transkript)

Jeden inhaltlichen Abschnitt mit einem klickbaren Zeitstempel-Link einleiten — so kann der Leser die Stelle direkt im Video nachverfolgen.

**Format je Plattform:**

| Plattform | Format |
|---|---|
| YouTube | `[▶ 12:34](https://www.youtube.com/watch?v=VIDEO_ID&t=754)` |
| YouTube (kurz) | `[▶ 12:34](https://youtu.be/VIDEO_ID&t=754)` |
| Podcast / lokal | `[▶ 12:34]` — nur Zeitmarke, kein Link |

**Woher kommen die Timestamps?**
- Aus dem konvertierten Transkript (`_Transkript.txt`) — dort sind sie alle ~45 Sekunden eingebettet
- Den nächsten Timestamp *vor* dem relevanten Inhalt nehmen
- Grep nach Schlüsselwörtern im Transkript → Zeilennummer → nächsten `[▶ ...]`-Eintrag davor verwenden

**Wo einfügen:**
- Direkt am Anfang eines jeden `###`-Abschnitts (vor dem ersten Satz oder Zitat)
- Bei langen Abschnitten auch mitten im Text, wenn ein neues Teilthema beginnt

**Wenn kein Transkript mit Timestamps verfügbar ist:** Abschnitt ohne Zeitstempel schreiben — nie erfundene Timestamps einfügen.

## Schritt 5b — Sherlock: Faktencheck (nur Zeitgeist-Notes)

> Sherlock arbeitet seit 08.10.2026 im **Fächer** (Schritt 4b) am Transkript; hier wird sein Block nur noch geprüft und eingesetzt.

Den Sherlock-Agenten aufrufen:

```
/agent sherlock
[vollständiger Note-Text]
```

Sherlocks Ausgabe besteht aus **zwei Blöcken** — beide per Edit in die Note einfügen:

1. `## Faktencheck` — nach dem Inhalt, vor den Verbindungen
2. `## Weiterführende Quellen (Sherlock)` — falls vorhanden: direkt nach einem eventuell bereits vorhandenen `## Weiterführende Quellen`-Abschnitt aus Schritt 2b. Wenn beide Abschnitte existieren, zusammenführen zu einem einzigen `## Weiterführende Quellen`-Block.

---

## Schritt 5c — Gedankenpoesie: Stimme (optionale Kür)

> [!info] Substanz steht — jetzt darf die Stimme dazu
> Nach Inhalt (5) und Faktencheck (5b), **vor** Cross-Linking/Ingest, damit die eingebettete und deployte
> Fassung schon die gestimmte ist. Folgt dem **`gedankenpoesie`-Skill** (`.claude/skills/gedankenpoesie/SKILL.md`).

**Rubrik-Default:**
- **Gedanken → ja** (die Rubrik kehrt bewusst zur Poesie zurück) — Skill anbieten und im Regelfall ausführen.
- **Zeitgeist / Denker / Geistesblitz → angeboten, Default nein** — ihr Register ist analytisch; nur auf
  ausdrücklichen Wunsch und dann behutsam, nie ins Lyrische zwingen.

**Nie Pflicht, nie still.** Dialogisch wie der Skill: Note + Modus lesen → Stimme vorschlagen (Luc =
Haussprache, kein Default) → gemeinsam entscheiden → veredeln (Subtraktion zuerst) → vorher/nachher zeigen,
Andreas finalisiert. Schon gestimmte Notes (Luc-Text, Pascal-Gedanke) **nicht anfassen**. Substanz bleibt
unangetastet — Stimme ändert nur das *Wie*, nie das *Was* (Faktencheck-Verdikte nie verwischen).

---

## Schritt 5d — Nachbesprechung: Themen vertiefen, ins Panorama führen (Angebot)

> [!info] Seit 26.09.2026 — erstes Beispiel: [[Herfried Muenkler — Die Sehnsucht nach Ordnung#Nachbesprechung]]
> Das Video ist das Video. Wer beim Lesen neugierig wird, soll auf der Seite weiterkommen: Die
> Nachbesprechung nimmt **zwei bis drei Themen** des Abends noch einmal auf — was man über das hinaus
> weiß, was gesagt wurde — und führt am Ende jedes Themas in ein **wachsendes Panorama**, wo die
> anderen Stimmen des Bestands zur selben Frage stehen.

**Wann anbieten:** Bei Panels, langen Vorträgen, Gesprächen mit vielen Themen, wenn ein Thema *nebenbei*
fällt, das eine eigene Frage wert ist (Münkler: Bürgerräte, Plebiszit — beides Nebenschauplätze des
Abends). **Nicht** bei Kultur-Reisen, Vipassana-/Kontemplationsvorträgen, kurzen Notes mit einem Thema.
Nach Faktencheck und Stimme, **vor** Cross-Linking — so kann Montaigne die Panorama-Verbindung gleich mitnehmen.

**Ablauf — vorschlagen, nicht still ausführen:**
1. **Themen vorschlagen** (max. 3, meist 2): *„Hier sehe ich zwei Themen für eine Nachbesprechung: …
   Das eine führt nach [Panorama X], das andere wäre eine neue Frage."* Andreas entscheidet. Das
   Auswählen ist das eigentliche Urteil — die Themen, bei denen echte Neugier entsteht oder der Sprecher
   etwas Wichtiges offen lässt, nicht alle.
2. **Recherche** (parallel, Subagenten): Forschung mit DOI über `wiss_search.py` (Solidität markieren:
   Review > Einzelstudie), Fälle und aktueller Stand (Jina/DuckDuckGo), Funfacts nur belegt. Dazu eine
   **Stimmensuche im Bestand** (grep + RAG `"answer": false`): wer bezieht zur Frage echte Position, mit
   exaktem Abschnitt für den Anker. Heiße Fakten (Tagesaktuelles, Zahlen) vor dem Schreiben selbst gegenprüfen.
3. **Schreiben** — `## Nachbesprechung` zwischen `## Publikumsfragen`/Inhalt und `## Faktencheck`:
   - kursiver Einleitungssatz (eine Zeile), dann je Thema ein `###`-Abschnitt
   - **entlang der Aussagen des Sprechers**, nicht als Lexikonartikel: Was sagte er, was weiß man darüber
     hinaus, wo trägt es, wo nicht (Yin-Yang — die Forschung darf ihm auch recht geben)
   - Quellen **inline** im Satz (MCP/RAG findet sie dort), nicht doppelt in `## Weiterführende Quellen`
   - endet je Thema mit `→ Weiter im Panorama: **[[<Panorama>#<Abschnitt>|<Frage>]]**, mit …`
   - Umfang: die Note wächst um höchstens ein Drittel, nicht auf das Doppelte
   - **Abgrenzung Faktencheck:** der prüft, *ob stimmt, was gesagt wurde*; die Nachbesprechung fragt, *was
     man darüber hinaus wissen kann*. Nichts doppelt — auf den Faktencheck verweisen statt ihn zu wiederholen.
4. **Panorama speisen:** Die Stimme der neuen Note (ein Satz, Sprung auf den Abschnitt) in den passenden
   Abschnitt des wachsenden Panoramas eintragen; was die Recherche an Forschung bringt, in dessen Sachstand;
   Zeile in `## Nachbesprechungen, die hierher führen`. Gibt es noch kein passendes Panorama: vorschlagen
   (Schwelle: mind. 3 echte Stimmen im Bestand) — anlegen nur mit Andreas' Ja. Form → `rules/gedankenwelten.md`, „Panorama".
5. **Anker prüfen:** Jeder `[[Note#Überschrift]]`-Link muss eine existierende Überschrift treffen
   (Doppelpunkt in der Überschrift im Link weglassen: `#Bürgerräte Skeptisch` für „Bürgerräte: Skeptisch").
   Die Astro-Fassung setzt daraus automatisch den Sprung in der Randspalte („Nachbesprechung ↓").
6. `aktualisiert:` der Note bumpen (echte Substanz), das Panorama ebenso; Rückverweise nicht.
7. **Ins Register (Pflicht):** `python3 .claude/scripts/nachbesprechungen.py ingest` — liest alle
   `## Nachbesprechung`-Abschnitte neu aus, schreibt `.claude/data/nachbesprechungen.jsonl` und bettet
   jedes Thema in die Collection `gedankenwelten_nachbesprechungen` ein (Hash-Skip, Sekunden). Themen
   ohne Panorama („Waisen") gehen so nicht verloren; die monatliche `analyse` prüft, ob drei davon auf
   dieselbe Frage zulaufen — der Kandidat für ein neues Panorama. Die Note bleibt die einzige Wahrheit.

---

## Schritt 6 — Montaigne: Cross-Linking (RAG-gestützt)

> Montaignes Kandidaten kommen seit 08.10.2026 aus dem **Fächer** (Schritt 4b); hier werden sie gegen die fertige Note geprüft und bidirektional eingebaut.

Montaigne nutzt jetzt RAG direkt — der separate Step 6a entfällt. Montaigne hat einen eingebauten RAG-Query als ersten Schritt und findet relevante Notes semantisch statt über Glob.

**Montaigne aufrufen:**
```
/agent montaigne
[neue Note Volltext]
```

Montaigne wird selbstständig:
1. RAG nach thematisch verwandten Notes fragen (top-15)
2. Die Top-12 Kandidaten lesen (Verbindungen-Abschnitte)
3. Max. 8 Verbindungen mit Begründung ausgeben

> Kein manuelles Glob + Tag-Extraktion mehr nötig — RAG ersetzt das.

**Nach Montaignes Ausgabe:**

1. Links in die neue Note einfügen (Abschnitt `## Verbindungen`)

2. Bestehende Notes bidirektional verlinken:
   - Für jeden Link: bestehende Note mit Edit öffnen, `[[neue Note]]` im Verbindungs-Abschnitt ergänzen
   - Wenn kein Verbindungs-Abschnitt vorhanden: am Ende der Note anlegen
   - Nicht existierende Dateinamen aus Montaignes Liste stillschweigend ignorieren

## Schritt 6b — Neue Note sofort in RAG ingestieren (Pflicht)

Sobald die Note inhaltlich final ist (inkl. Verbindungen), direkt in Qdrant einspeisen:

```bash
NOTE_PATH="content/Zeitgeist/DATEINAME.md"   # oder content/Denker/...

python3 -c "
import json
with open('$NOTE_PATH') as f: content = f.read()
print(json.dumps({'path': '$NOTE_PATH', 'content': content, 'media_type': 'text'}))
" | curl -s --max-time 120 -X POST "<dein-rag-server>/webhook/ingest-gedankenwelten" \
  -H "Content-Type: application/json" -d @-
```

Erwartung: Response mit `status: ok` und `chunks_ingested > 0`.

> [!warning] Embed-Server kann >60s brauchen → `--max-time 120`
> Der single-threaded Mac-Embed-Server braucht bei großen Notes (3000+ Wörter, viele Chunks) auch mal
> 60–70 s. Ein zu knapper `--max-time` lässt curl **stumm mit leerer Antwort** abbrechen (HTTP-Code wird
> nie erreicht) — die Note ist dann *nicht* ingestiert, obwohl kein Fehler erscheint. Darum überall
> `--max-time 120`. Bei leerer Antwort: mit `-w "\nHTTP:%{http_code} %{time_total}s\n"` prüfen und erneut
> feuern (Ingest ist idempotent). Nie zwei Ingests parallel — der Embed-Server ist single-threaded.

## Schritt 6c — Modifizierte Notes re-ingestieren (Pflicht)

Durch bidirektionales Linking (Schritt 6) wurden bestehende Notes verändert. **Jede geänderte Note muss re-ingestiert werden**, damit die neuen Verbindungen im RAG-Graph sichtbar sind.

```bash
# Für JEDE Note, die in Schritt 6 einen neuen Verbindungs-Link bekommen hat:
MODIFIED_PATH="content/Denker/BESTEHENDE_NOTE.md"

python3 -c "
import json
with open('$MODIFIED_PATH') as f: content = f.read()
print(json.dumps({'path': '$MODIFIED_PATH', 'content': content, 'media_type': 'text'}))
" | curl -s --max-time 120 -X POST "<dein-rag-server>/webhook/ingest-gedankenwelten" \
  -H "Content-Type: application/json" -d @- | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  Re-Ingest: {d[0][\"title\"]}: {d[0][\"chunks_ingested\"]} chunks')"
```

> Der Ingest-Workflow ist idempotent (löscht alte Chunks vor Upsert) — Re-Ingest ist sicher.

## Schritt 6d — Verifikation (Pflicht)

Nach allen Ingests einen Quick-Check durchführen:

```bash
# Prüfen ob die neue Note im RAG auffindbar ist
curl -s -X POST "<dein-rag-server>/webhook/query-gedankenwelten" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Was sind die Kernthesen von <TITEL DER NEUEN NOTE>?",
    "top_k": 3,
    "answer": false
  }'
```

Wenn die neue Note **nicht** in den Quellen auftaucht: Ingest-Response prüfen und erneut ingestieren.

## Schritt 6e — Quellen der Note in den Quellen-Layer aufnehmen (Pflicht)

Jede neue Note **und** jede neu angelegte DenkerVita speist automatisch den Quellen-Layer — so wächst der
über MCP (`find_sources`) abfragbare Beleg-Apparat mit jeder Note, und `/gedankenwelt-kurator` muss nur
noch gelegentlich für Vollständigkeit laufen.

```bash
python3 .claude/scripts/extract_sources.py --note "$NOTE_PATH"
# Falls in Schritt 0c eine neue DenkerVita angelegt wurde, auch deren Quellen aufnehmen:
python3 .claude/scripts/extract_sources.py --note "content/DenkerVita/<Vorname Nachname>.md"
```

Das hängt alle Quellen dedupliziert + klassifiziert an `.claude/data/sources.jsonl` an. **Automatisch erfasst** werden damit:

| Quelle | Woher |
|---|---|
| **Sherlock** | `## Faktencheck`-Belege + `## Weiterführende Quellen (Sherlock)` |
| **YouTube-/Podcast-Beschreibung** | die in `## Weiterführende Quellen` übernommenen Links (Schritt 2b) |
| **Humboldt** | Bücher (genialokal) + Vorträge aus der DenkerVita |
| **Primärquelle** | die `Quelle:`-Zeile der Note |

> Je vollständiger die `## Weiterführende Quellen` (Schritt 2b — Video-**und Podcast-Beschreibung/Show-Notes
> komplett** übernehmen!), desto wertvoller der Quellen-Layer. Die vom Creator selbst kuratierten Listen
> sind die wertvollsten Quellen.

Der eigentliche Ingest in die Collection `gedankenwelten_sources` wird in **Schritt 11 nach dem Push**
ausgelöst (inkrementell — dank Hash-Skip werden nur die neuen Quellen embeddet, Sekunden).

---

## Schritt 7 — Quellen & Links.md aktualisieren

Eintrag in `content/Quellen & Links.md` anlegen:

```markdown
## [Autorenname / Thema]

| | |
|---|---|
| **Vortrag / Video** | [Titel](URL) |
| **Notiz** | [[Obsidian Note Name]] |
```

---

## Schritt 8 — Journal-Eintrag

Eintrag oben in `journal/MM.YYYY.md` (aktueller Monat) einfügen:

```markdown
### DD.MM.YYYY — Autor — Thema 📝
> Einzeiler-Teaser der Note.

Kurze Beschreibung (2–3 Sätze): Was wurde verarbeitet, warum ist es relevant?

**Quelle:** [Titel](URL)
**Note:** [[content/Zeitgeist/Dateiname ohne .md]]
```

Bei mehreren Quellen:
```markdown
**Quelle A:** [Titel A](URL-A) · **Quelle B:** [Titel B](URL-B)
**Note:** [[content/Denker/Dateiname ohne .md]]
```

> **Pflicht:** Die `**Note:**`-Zeile mit vollem Vault-Pfad (z.B. `content/Zeitgeist/...` oder `content/Denker/...`) ist immer anzugeben — auch bei Einträgen mit mehreren Quellen. Ohne Note-Link ist der Journal-Eintrag unvollständig.

Falls die Monatsdatei noch nicht existiert: neue Datei anlegen (Frontmatter + Überschrift aus `journal/04.2026.md` übernehmen).

Danach `index.md` aktualisieren: neuesten Journal-Teaser oben in die `## 📰 Journal`-Sektion einfügen. Format:

```markdown
> **DD.MM.YYYY** — Titel 📝
> Einzeiler-Beschreibung.
> → [Weiterlesen](journal/MM.YYYY.md)
> → [[content/Zeitgeist/Dateiname ohne .md|Note öffnen]]
```

> **Pflicht:** Beide Zeilen sind immer anzugeben — `Weiterlesen` für den Journal-Kontext, `Note öffnen` für den Direktsprung zur Note. Einträge ohne eigene Note (Infrastruktur, Ops) bekommen nur `Weiterlesen`.

---

## Schritt 9 — Gedankenwelten.md aktualisieren

Die Note in den zentralen Katalog `Gedankenwelten/Gedankenwelten.md` eintragen:

1. Passende Sektion finden (z.B. `### Deutschland & Europa`, `### USA & Trump`, `### Philosophie & Denken`)
2. Zeile einfügen im Format:
   ```
   - [[Dateiname ohne .md]] | tag1, tag2, tag3 | Ein-Satz-Zusammenfassung der Kernaussage
   ```
3. Zähler in der Fußzeile anpassen:
   - Zeitgeist-Note → `XX Zeitgeist` um 1 erhöhen
   - Denker-Note → `XX Denker` um 1 erhöhen
   - Gesamtzahl `= XXX Notes` entsprechend aktualisieren

---

## Schritt 10 — Cortex-Log aktualisieren

Eintrag in `Cortex-Log.md` **ganz oben** einfügen — direkt nach dem `---`-Trennstrich unter dem Titel-Header, vor dem bisher ersten Eintrag. Neueste Einträge stehen immer oben.

```markdown
## [DD.MM.YYYY] note-created | Autor — Thema

**Note:** [[Autor — Thema]]
**Quelle:** URL
```

---

## Schritt 10b — Frontmatter-YAML-Check (Pflicht, vor dem Commit)

> [!danger] Ein einziger Frontmatter-Fehler bricht den **gesamten** Quartz-Build ab
> Quartz parst die `--- … ---`-Frontmatter als YAML. Ein ungültiger Wert (Klassiker: ein **gerades** `"`
> mitten in einem `"…"`-gequoteten `title:`/`description:`, das den String vorzeitig beendet) lässt nicht
> nur *diese* Note, sondern den **kompletten Build** scheitern (`set -e`). Weil `.last-built` erst nach
> erfolgreichem Build geschrieben wird, hängt dann der minütliche Pi-Cron dauerhaft im selben Fehler —
> nichts wird mehr deployed, bis die Frontmatter gefixt ist. (Real passiert am 17.06.2026.)

Darum vor jedem Commit den Validator laufen lassen — prüft standardmäßig alle in git geänderten/neuen Notes:

```bash
python3 .claude/scripts/check_frontmatter.py
```

Erwartung: `✓ N Note(s) sauber.` (Exit 0). Bei Exit 1 **erst fixen, dann committen** — die Meldung nennt
Datei, YAML-Fehler und bei geraden Quotes den konkreten Verdacht. Faustregel: im `title:`/`description:`
**geschweifte** `„…“` verwenden (nie das gerade `"` im Inneren), oder den Wert mit `'…'` quoten.

---

## Schritt 10c — Banner generieren (Pflicht, seit 03.07.2026)

Jede neue Note bekommt **vor dem Commit** ihr Banner — und **zugleich die DenkerVita, wenn sie
noch keins hat** (bei bestehenden Vitas prüfen: `grep -l "vita-banner" <Vita-Pfad>`; neue Vitas
aus Schritt 0c haben nie eins). Ablauf nach dem **`gedankenart`-Skill** (Kern des Skills lesen,
wenn nicht präsent): Kern der Note finden → Künstlerhand bewusst wählen (jede Note ihre eigene
Kreation, Klee ist Haussprache, kein Default) → Prompt komponieren → generieren:

```bash
python3 .claude/scripts/gen_banner.py \
  --prompt "<Prompt>" \
  --out "<NOTE-SLUG>-banner"          # Vita: "<Vorname-Nachname>-vita-banner"
# optional: --model recraft --style vector_illustration (grafische Linien-Stile)
```

Das Skript (fal.ai, FLUX.2 Pro, `FAL_KEY` in `.env`, ~2–4 ct/Bild) legt das fertige 1200×500-JPEG
direkt in `content/assets/` ab. **Bild ansehen (Read), ehrlich urteilen, bei Schwächen neu
generieren.** Dann einbetten wie in `gedankenart` Schritt 6: Embed mit vollem Vault-Pfad `|1200`
direkt unter der `# Überschrift`, gefolgt vom `<details><summary>🎨</summary>`-Block (Künstler,
Warum, vollständiger Prompt). **Nie** `banner:`-Frontmatter. Note- und Vita-Banner bekommen
bewusst **verschiedene** Künstlerhände — die Note malt das Thema, die Vita den Menschen.

---

## Schritt 10d — Wandspruch für den Gedankenraum (Pflicht, seit 04.10.2026)

Im Gedankenraum (gedankenwelten.org/raum, Osterei: Doppelklick aufs Banner) ist jede Note ein Saal; über
ihrem Bild steht leise ein **geheimnisvoller Satz**. Er entsteht jetzt mit der Note, gleich nach dem
Banner, damit er nicht untergeht — für die **Note** und für **jede neue DenkerVita** dieses Laufs:

```yaml
raetsel: "Hinein führt eine Jacke. Heraus führt manchmal ein Kind."
```

Vorher **`.claude/skills/gedankenpoesie/references/wandspruch.md` lesen** (Regeln, Eichsätze). Kurz: ein
Rätsel, das den Inhalt nicht verrät, höchstens ~80 Zeichen, keine Namen aus dem Titel, aus einem Bild der
Note geschöpft; jeder Satz in **seiner eigenen Hand** (gedankenpoesie-Palette, Luc wo er trägt), Note und
Vita mit verschiedenen Bildern. Ankündigen: `→ [WANDSPRUCH: <Hand>] „<Satz>"`. Im YAML doppelt gequotet,
innen nur typografische „…" (sonst bricht der String — Schritt 10b gilt auch für `raetsel:`).

Ohne Satz ist der Saal stumm — kein Fehler, aber die Note gilt als unvollständig.

---

## Schritt 11 — Commit, Push, Sync & Deploy

Änderungen committen und pushen. Pfad je nach Gerät:

```bash
# Mac
cd <vault>/
git add -A && git commit -m "note-pipeline: <Autor> — <Thema>"
git push
```

**Gedankenwelten GitHub-Repo synchronisieren (Pflicht auf Mac):**

Nach dem Push das öffentliche Gedankenwelten-Repo aktualisieren — das Sync-Script kopiert alle .md- und Bilddateien aus Cortex/Gedankenwelten ins separate GitHub-Repo und committet/pusht automatisch:

```bash
<vault>/.claude/scripts/sync-from-cortex.sh
```

> Das Script synct nur Notes (kein Transkripte/Audio) und committed+pusht nur wenn sich etwas geändert hat. Sicher, idempotent — kann immer aufgerufen werden.

**Quellen-Layer ingestieren (Pflicht, nach dem Push):**

Damit die in Schritt 6e gesammelten Quellen sofort über `find_sources` auffindbar sind, den inkrementellen
Sources-Ingest auf dem Pi auslösen. Das Script pullt `<vault>/` und embeddet nur die neuen Quellen
(Hash-Skip → Sekunden):

```bash
ssh <server> "~/services/gedankenwelten-mcp/rebuild-sources.sh"
```

> So wächst `gedankenwelten_sources` mit **jeder** Note automatisch mit. `/gedankenwelt-kurator` ist dann
> nur noch für Vollständigkeits-Durchläufe (Bestandsanreicherung) nötig, nicht für den laufenden Betrieb.

> Die headless n8n-Auto-Pipeline ist **pausiert** (zu teuer; manuelle Verarbeitung bevorzugt — bewusste
> Kuratierung). Der Quellen-Ingest läuft daher über diesen manuellen Mac-Pfad.

**Nur auf dem Mac:** Note im Browser öffnen.

**Pflicht:** Slug NIE „aus dem Kopf" bauen — immer den deterministischen One-Liner unten verwenden. Der häufigste Fehler ist, dass ` - ` (Space-Dash-Space) im Dateinamen zu `---` wird, weil die Mehrfach-Bindestrich-Kollabierung vergessen wird.

```bash
# SECTION = Zeitgeist oder Denker, FILE = Dateiname ohne .md
SECTION="Zeitgeist"
FILE="Tilo Wesche - Rechte der Natur Eigentum Kolonialismus"

SLUG=$(printf '%s' "$FILE" \
  | sed -e 's/—/-/g' \
        -e 's/&/-and-/g' \
        -e 's/[?#]//g' \
        -e 's/ /-/g' \
        -e 's/-\{2,\}/-/g' \
        -e 's/^-//' -e 's/-$//')

open -a Firefox "<dein-wiki>/Gedankenwelten/${SECTION}/${SLUG}"
```

**URL-Slug-Regeln** (Quartz sluggify mit Pi-Patch `fa173cf`):
- Em-Dash `—` → `-`
- `&` → `-and-`
- `?` und `#` werden entfernt
- Leerzeichen → `-`
- **Mehrfache Bindestriche (`--`, `---`) → `-` (kollabiert)** — der häufigste Stolperstein
- Führende/nachfolgende `-` werden entfernt
- Umlaute: Quartz sluggt `ä→a`, `ö→o`, `ü→u` — deshalb im Dateinamen bereits `ae/oe/ue` verwenden

**Beispiele (genau so prüfen):**

| Dateiname | Korrekter Slug |
|---|---|
| `Tilo Wesche - Rechte der Natur Eigentum Kolonialismus.md` | `Tilo-Wesche-Rechte-der-Natur-Eigentum-Kolonialismus` |
| `Koschi Politik — Amanda Ungaro Melanias Vertraute will auspacken.md` | `Koschi-Politik-Amanda-Ungaro-Melanias-Vertraute-will-auspacken` |

Falsch wäre `Tilo-Wesche---Rechte-...` (drei Bindestriche) — der Pi-Patch kollabiert das zwar, aber der Browser-Open-Befehl muss bereits den finalen Slug enthalten, sonst öffnet Firefox eine 404-Seite.

---

## Schritt 11b — Video in Nachschau **und** Archiv umziehen (wenn es aus einer Playlist kam)

Das verarbeitete Video wandert **raus aus seiner Quell-Playlist** und **rein in beide <konto-2>-Ziele**:
`<konto-2>_gedankenwelten_nachschau` **und** `<konto-2>_gedankenwelten_archiv`.

> [!note] `nachschau` vs. `archiv` — zwei Rollen, beide Pflicht (seit 03.07.26)
> **`*_archiv` = das eigentliche Archiv:** jedes verarbeitete Video landet hier, damit am Ende alles
> sauber archiviert ist. **`*_nachschau` = die „vielleicht noch anschauen"-Liste:** verarbeitet, aber
> evtl. noch nicht selbst gesehen — von dort räumt Andreas selbst weg, wenn er es angeschaut hat.
> Verarbeiten ≠ ansehen (meist läuft nur das Transkript durch die Pipeline), darum immer **beide** Adds.
> Einzige Ausnahme: Sagt Andreas *„hab ich schon gesehen"*, entfällt die Nachschau — das Archiv bleibt.

> [!important] Ziel ist **immer** die <konto-2>-Seite
> Egal aus welchem Konto die Quelle stammt (<konto-1> *oder* <konto-2>): das Video landet immer auf **<konto-2>**,
> weil Andreas meist dort ist. Ist die Quelle eine **<konto-1>**-Playlist, ist der Umzug kontenübergreifend —
> deshalb **nicht** ein einzelnes `move`, sondern `add <konto-2> <ziel>` (<konto-2>-Token) **plus**
> `remove <konto-1> <quelle>` (<konto-1>-Token). Beide Konten sind autorisiert. Diese Add-dann-Remove-Reihenfolge
> ist die uniforme Regel für *beide* Fälle.

> [!tip] Default: beide Ziele — „hab ich schon gesehen" lässt nur die Nachschau weg
> **Ziel-Default:** `<konto-2>_gedankenwelten_nachschau` **+** `<konto-2>_gedankenwelten_archiv` (zwei Adds).
> **Override:** Sagt Andreas beim Verarbeiten sinngemäß *„hab ich schon gesehen"*, entfällt nur das
> Nachschau-Add — das Archiv-Add läuft **immer** (es ist die Archivierung, kein „gesehen"-Signal mehr).

**Gilt nur, wenn das Video aus einer der .env-Playlisten kam** (kurato/kairos oder ein Playlist-Video von Hand). Ein frei eingeworfener URL, der in keiner Liste liegt, wird trotzdem in Nachschau + Archiv gelegt (idempotent), nur ohne Remove — es ist ja nichts zu entfernen.

```bash
PY=~/.config/cortex-youtube/venv/bin/python
YT=<vault>/.claude/scripts/yt_playlist.py
VID="<videoId>"   # aus der Quell-URL (v=… oder youtu.be/…)

# 1) Immer: in beide <konto-2>-Ziele, idempotent
"$PY" "$YT" add <konto-2> <konto-2>_gedankenwelten_archiv "$VID"
"$PY" "$YT" add <konto-2> <konto-2>_gedankenwelten_nachschau "$VID"   # entfällt nur bei „hab ich schon gesehen"

# 2) Aus ALLEN Quell-Playlisten entfernen + verifizieren (idempotent).
#    `cleanup` scannt <konto-1>_gedankenwelten, <konto-1>_gedankenwelten_global,
#    <konto-1>_republica, <konto-2>_gedankenwelten, <konto-2>_gedankenwelten_global,
#    entfernt das Video überall wo es liegt und prüft nach, dass es wirklich weg ist.
#    Exit 0 = Quellen sauber · Exit ≠ 0 = FEHLER LAUT MELDEN, nicht verschlucken!
"$PY" "$YT" cleanup "$VID"
```

> [!warning] Verifikation ist Teil des Schritts — kein stilles Scheitern
> Früher lief hier ein Scan-Loop mit `2>/dev/null`, der Fehler (abgelaufenes Token, API-Fehler)
> verschluckte — Folge: Videos blieben trotz Note in den Quell-Listen hängen. `cleanup` prüft nach
> jedem Remove nach und endet mit Exit ≠ 0, wenn etwas hängen bleibt. Schlägt es fehl: Andreas
> Bescheid geben (meist Token-Refresh nötig: `yt_playlist.py auth <konto>`), **nicht** übergehen.
> Aufgelaufene Altlasten räumt `"$PY" "$YT" sweep` (vergleicht Archiv gegen alle Quell-Listen;
> `--dry-run` zum Anschauen).

> [!note] Dubletten in Playlisten — `dedupe` (seit 07.08.2026)
> YouTube erlaubt **denselben Video-Eintrag mehrfach** in einer Playlist, und beim manuellen Sammeln
> passiert das leicht: `<konto-1>_republica` hatte 100 Einträge für nur 77 Videos, einzelne Talks
> standen 4×. Früher brach `cleanup` daran ab (Exit 1) — es löschte einen Eintrag und fand bei der
> Verifikation die zweite Kopie. **Beides ist gefixt:** `cleanup` entfernt jetzt *alle* Kopien pro
> Liste (und meldet `(N Einträge — Dubletten)`), und für die Bestandspflege gibt es ein eigenes
> Kommando:
>
> ```bash
> "$PY" "$YT" dedupe <konto> <playlist> [--dry-run]
> ```
>
> Behält immer den **ersten** Eintrag (Reihenfolge bleibt stabil), entfernt alle weiteren, verifiziert
> danach. `sweep` sieht Dubletten **nicht** — es vergleicht Quelle gegen Archiv, nicht eine Liste
> gegen sich selbst. Also gelegentlich beides laufen lassen.

> Läuft **nach** dem Deploy — scheitert die Note, bleibt das Video in der Warteliste. Ziel sind
> standardmäßig **Nachschau + Archiv**; bei Andreas' „hab ich schon gesehen" nur das **Archiv**.

---

## Schritt 12 — Floskel-Review (Pflicht, zum Abschluss)

> [!important] Der letzte Blick gehört der Sprache
> Ganz am Ende — nach Deploy und Playlist-Umzug — **jede** in diesem Lauf neu erstellte oder
> substantiell überarbeitete Note noch einmal gegen `.claude/skills/gedankenpoesie/references/ki-tells.md`
> lesen. Nicht die Substanz prüfen (die steht), sondern nur: **„Was verrät hier noch die Maschine?"**
> Eingeführt am 01.08.2026, weil in einem Dreier-Lauf ~18 negative Parallelismen durchrutschten,
> obwohl die Regel in `aristoteles` längst stand — der Vorsatz allein trägt nicht, es braucht den Blick danach.

**Ablauf — mechanisch zählen, dann mit Urteil streichen:**

```bash
# Für jede neue Note: die Tells sichtbar machen
for f in <NOTE_PFADE>; do
  echo "########## $(basename "$f" .md)"
  echo "--- 'sondern' (Zitate/Faktencheck abziehen!) ---"; grep -n "sondern" "$f" | cut -c1-190
  echo "--- Häufungswörter ---"
  grep -oiE "\b(geflecht|verwoben|navigier\w*|unterstreich\w*|facettenreich|vielschichtig|spannungsfeld|resonanz|zutiefst|im kern|letztlich|gewissermaßen|ein stück weit|nicht zuletzt|darüber hinaus|wechselspiel|entfalten|beleuchten)\b" "$f" | sort | uniq -c | sort -rn
  echo "--- Kopula-Vermeidung / Partizip-Anhängsel ---"
  grep -noE "(fungiert als|stellt [^.]{0,30}dar|dient als|bildet den Auftakt|was die [A-Za-zäöü]+ (verdeutlicht|unterstreicht))" "$f"
done
```

**Dann urteilen, nicht blind streichen:**

| Fund | Behandlung |
|---|---|
| `nicht X, sondern Y` in **meinem** Erzähltext | auflösen — bis auf **eine** pro Note |
| `nicht X, sondern Y` im **Zitat**, in einem Faktencheck-Verdikt oder als **These des Sprechers** | **stehen lassen** (Substanz friert ein) |
| Häufungswort einzeln | ok |
| ≥ 3 Häufungswörter in einem Absatz | umschreiben |
| generischer Aufschwung-Schluss | durch konkretes Bild / offene Frage ersetzen |

Zum Schluss die eine ehrliche Frage laut beantworten — **„Was verrät hier noch die Maschine?"** Die erste
Antwort ist fast immer richtig; genau die eine Stelle nachschleifen. Ein zweiter Durchgang fängt, was der
erste überlas; ein dritter ist Übertreibung (Glätten ist der Tod der Stimme).

**Wurde etwas geändert:** Note neu ingestieren (Schritt 6b), `check_frontmatter.py`, committen, `cgsync`.

---

## Checkliste (Zusammenfassung)

- [ ] Quellen-Check (Schritt -1) — Ampel-Empfehlung gegeben
- [ ] **Rubrik gemeinsam entschieden (Schritt -0.5): Denker / Zeitgeist / Geistesblitz** — Vorschlag + Begründung, Andreas bestätigt
- [ ] DenkerVita geprüft: existiert → lesen; existiert nicht → Humboldt-Recherche + DenkerVita anlegen (Schritt 0)
- [ ] DenkerVita in RAG ingestiert (wenn neu angelegt)
- [ ] Download / Transkription abgeschlossen
- [ ] **Fächer gestartet (Schritt 4b):** Humboldt (falls nötig) · Sherlock am Transkript · Montaigne — parallel im Hintergrund, Hauptinstanz schreibt; zweiter Fächer (Nachbesprechungs-Recherche, Banner) nach Themenwahl
- [ ] Video-Beschreibung auf Quellen geprüft (Schritt 2b) — ggf. `## Weiterführende Quellen` in Note ergänzt
- [ ] VTT → TXT konvertiert
- [ ] Obsidian-Note erstellt — Callout aus DenkerVita, Link `→ [[content/DenkerVita/<Name>|DenkerVita]]` am Ende des Callouts
- [ ] **Publikumsfragen:** Fragerunde im Transkript vermessen, alle Fragen gelistet, `## Publikumsfragen` mit Substanz + Moderator-Nachfragen geschrieben (entfällt nur, wenn die Folge keine Runde hat)
- [ ] **Zeitgeist:** Sherlock-Faktencheck eingefügt
- [ ] **Geistesblitz:** Aufbau wie Zeitgeist mit Denker-Tiefe; Sherlock-Faktencheck bei empirischen Claims; DenkerVita nur bei Einzelperson im Zentrum
- [ ] **Denker:** Tiefenanalyse durchgeführt — lebendige Biografie, Kernkonzepte als eigene Abschnitte, 2–3 Eigene Einschätzungen, konzeptuelle Verbindungen
- [ ] **Denker (neu):** DenkerVita angelegt + `known-speakers.md` + `DenkerVita/Alle Denker.md` aktualisiert
- [ ] RAG-gestütztes Montaigne-Cross-Linking durchgeführt (Montaigne nutzt RAG intern)
- [ ] Bidirektionales Linking: neue Note ↔ bestehende Notes; DenkerVita Verbindungen aktualisiert
- [ ] Neue Note in RAG ingestiert (`/webhook/ingest-gedankenwelten`) + alle modifizierten Notes re-ingestiert
- [ ] RAG-Verifikation: Kurztest-Query bestätigt neue Note ist auffindbar
- [ ] Quellen der Note **und** (falls neu) der DenkerVita in `sources.jsonl` aufgenommen (`extract_sources.py --note`, Schritt 6e)
- [ ] Quellen-Layer ingestiert: `rebuild-sources.sh` nach dem Push ausgelöst (Schritt 11)
- [ ] Eintrag in `Quellen & Links.md`
- [ ] Journal-Eintrag in `journal/MM.YYYY.md` + Teaser in `index.md`
- [ ] `Gedankenwelten/Gedankenwelten.md` — Note eingetragen + Zähler aktualisiert
- [ ] **Playlist-Umzug (Schritt 11b):** Video in `<konto-2>_gedankenwelten_nachschau` **und** `<konto-2>_gedankenwelten_archiv` gelegt (bei „schon gesehen" nur Archiv), danach `yt_playlist.py cleanup <videoId>` gelaufen und **mit Exit 0 verifiziert**, dass das Video aus allen Quell-Playlisten raus ist
- [ ] Eintrag in `Cortex-Log.md`
- [ ] **Frontmatter-YAML-Check bestanden** (`python3 .claude/scripts/check_frontmatter.py` → Exit 0, Schritt 10b) — sonst bricht der ganze Quartz-Build ab
- [ ] **Banner generiert & eingebettet (Schritt 10c):** Note immer; DenkerVita zugleich, wenn sie noch keins hat (`gen_banner.py` via fal.ai; verschiedene Künstlerhände für Note und Vita)
- [ ] Commit, Push & Deploy — Note im Browser geöffnet
- [ ] **Floskel-Review (Schritt 12):** jede neue Note gegen `ki-tells.md` gelesen — max. **eine** negative Parallele pro Note (Zitate/Faktencheck ausgenommen), keine Häufungswort-Cluster, kein generischer Schluss; bei Änderungen re-ingestiert + neu deployed
- [ ] Gedankenwelten GitHub-Repo synchronisiert (`cgsync` / `<vault>/.claude/scripts/sync-from-cortex.sh`)
