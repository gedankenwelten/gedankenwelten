# Rules — Transkript-Pipeline

## YouTube-Untertitel herunterladen

yt-dlp unter `/opt/homebrew/bin/yt-dlp` (Mac) oder `yt-dlp` (Linux/Pi):

```bash
# Deutsch zuerst
yt-dlp --write-auto-sub --skip-download --sub-lang de \
  --output "content/Transkripte/Dateiname_%(title)s.%(ext)s" "URL"

# Fallback: Englisch
yt-dlp --write-auto-sub --skip-download --sub-lang en \
  --output "content/Transkripte/Dateiname_%(title)s.%(ext)s" "URL"
```

Namenskonvention: `Nachname_Stichwort_` als Präfix (z.B. `Haidt_Moral_Roots_`).

## VTT → TXT konvertieren

Das Script liegt permanent unter `.claude/scripts/vtt_to_txt.py`:

```bash
# YouTube (mit klickbaren Zeitstempel-Links)
python3 .claude/scripts/vtt_to_txt.py \
  "content/Transkripte/DATEI.vtt" \
  "content/Transkripte/DATEI_Transkript.txt" \
  "https://www.youtube.com/watch?v=VIDEO_ID"

# Podcast/Whisper (nur Zeitmarken, kein Link)
python3 .claude/scripts/vtt_to_txt.py \
  "content/Transkripte/DATEI.vtt" \
  "content/Transkripte/DATEI_Transkript.txt" \
  "local"
```

## Audio/Video-Transkription: mlx-whisper (Mac M-Series)

```bash
# Empfohlenes Modell: large-v3-turbo (schnell + akkurat)
mlx_whisper "Pfad/zur/datei.mp3" \
  --model "mlx-community/whisper-large-v3-turbo" \
  --language de \
  --output-format vtt \
  --output-dir "content/Transkripte/"
```

Für Videos ohne Untertitel: erst Audio extrahieren, dann transkribieren:

```bash
ffmpeg -i "video.mp4" -vn -acodec pcm_s16le -ar 16000 "audio.wav"
mlx_whisper "audio.wav" \
  --model "mlx-community/whisper-large-v3-turbo" \
  --language de \
  --output-format vtt \
  --output-dir "content/Transkripte/"
```

## Zielordner

| Quelle | Transkript-Ordner |
|---|---|
| Gedankenwelten (YouTube/Podcast) | `content/Transkripte/` |

## Sherlock — Faktencheck-Leitlinien

Vor dem Faktencheck immer das Transkript gegenlesen. Prüfe was der Sprecher *tatsächlich sagt*.

Bei Vorträgen aus spirituellen, kontemplativen oder philosophischen Traditionen gilt ein anderer Maßstab:

**Prüfen:** Empirische Claims — Zahlen, Daten, historische Fakten.

**Nicht flaggen:** Interpretationen kanonischer Texte, methodische Entscheidungen innerhalb einer Tradition, spirituelle Erfahrungsberichte.
