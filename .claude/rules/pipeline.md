# Rules — Transkript-Pipeline

## YouTube-Untertitel herunterladen

yt-dlp liegt unter `/opt/homebrew/bin/yt-dlp`:

```bash
# Deutsch zuerst
yt-dlp --write-auto-sub --skip-download --sub-lang de \
  --output "Zielordner/Dateiname_%(title)s.%(ext)s" "URL"

# Fallback: Englisch
yt-dlp --write-auto-sub --skip-download --sub-lang en \
  --output "Zielordner/Dateiname_%(title)s.%(ext)s" "URL"
```

Namenskonvention: `Nachname_Stichwort_` als Präfix (z.B. `Haidt_Moral_Roots_`).

## VTT → TXT konvertieren

Das Script liegt permanent unter `.claude/scripts/vtt_to_txt.py`:

```bash
# YouTube (mit klickbaren Zeitstempel-Links)
python3 .claude/scripts/vtt_to_txt.py \
  "Pfad/zur/DATEI.vtt" \
  "Pfad/zur/DATEI_Transkript.txt" \
  "https://www.youtube.com/watch?v=VIDEO_ID"

# Podcast/Whisper (nur Zeitmarken, kein Link)
python3 .claude/scripts/vtt_to_txt.py \
  "Pfad/zur/DATEI.vtt" \
  "Pfad/zur/DATEI_Transkript.txt" \
  "local"
```

Zeitstempel-Format: `[▶ 3:24](https://www.youtube.com/watch?v=VIDEO_ID&t=204)` alle ~45 Sekunden.

## Audio/Video-Transkription: mlx-whisper (Mac M-Series)

```bash
# Empfohlenes Modell: large-v3-turbo (schnell + akkurat)
mlx_whisper "Pfad/zur/datei.mp3" \
  --model "mlx-community/whisper-large-v3-turbo" \
  --language de \
  --output-format vtt \
  --output-dir "content/Transkripte/"
```

Läuft auf dem Apple GPU/Neural Engine — deutlich schneller als CPU-Whisper.
Für Videos ohne Untertitel: erst Audio extrahieren, dann transkribieren:

```bash
# Audio aus Video extrahieren (ffmpeg)
ffmpeg -i "video.mp4" -vn -acodec pcm_s16le -ar 16000 "audio.wav"

# Dann transkribieren
mlx_whisper "audio.wav" \
  --model "mlx-community/whisper-large-v3-turbo" \
  --language de \
  --output-format vtt \
  --output-dir "content/Transkripte/"
```

Modell-Optionen:
| Modell | Geschwindigkeit | Qualität |
|---|---|---|
| `mlx-community/whisper-large-v3-turbo` | ★★★★ | ★★★★★ |
| `mlx-community/whisper-large-v3` | ★★★ | ★★★★★ |
| `mlx-community/whisper-medium` | ★★★★★ | ★★★★ |

## Zielordner

| Quelle | Transkript-Ordner |
|---|---|
| Gedankenwelten (YouTube/Podcast) | `content/Transkripte/` |
| Methodik | `Opus/Methodik/Transkripte/` |

## Standbilder aus YouTube-Videos extrahieren (optional)

Für Vorträge mit visuell starken Slides oder gezeigten Beispielen. Nur sinnvoll wenn das Video unter freier Lizenz steht (z.B. CC BY-SA 4.0 — immer in der YouTube-Beschreibung prüfen).

### Schritt 1 — Video herunterladen

```bash
/opt/homebrew/bin/yt-dlp -f "best[height<=720]" \
  --output "content/Transkripte/DATEINAME.%(ext)s" "URL"
```

### Schritt 2 — Gemma identifiziert die besten Timestamps

Gemma liest das konvertierte Transkript und benennt Momente, wo etwas *gezeigt* wird (Screenshots, Social-Media-Posts, Slides mit konkreten Beispielen) — nicht nur beschrieben.

Prompt-Template für Gemma:
```
Analysiere dieses Transkript. Identifiziere Momente wo die Sprecherin/der Sprecher 
etwas Visuelles zeigt. Format: TIMESTAMP_SEK | Beschreibung | Relevanz (hoch/mittel).
Maximal 8 Einträge, visuell stärkste zuerst. [TRANSKRIPT]
```

### Schritt 3 — Frames extrahieren und croppen

Layout-Check: Einen Frame ansehen um das Format zu verstehen, dann Crop anpassen.

**re:publica-Format** (Rednerin am Pult links-unten, Slides als Vollformat-Rückprojektion, Publikum vorne):
```bash
ffmpeg -y -ss TIMESTAMP -i "VIDEO.mp4" -frames:v 1 -q:v 2 \
  -vf "crop=iw-270:ih*0.62:270:0" \
  "content/assets/DATEINAME_TIMESTAMP.jpg"
```
→ Entfernt: Publikum (untere 38%) + re:publica-Dekokreis (linke 270px)

**Allgemeines Format** (kein bekanntes Layout):
```bash
# Erstmal ohne Crop — einen Frame ansehen und Crop manuell anpassen
ffmpeg -y -ss TIMESTAMP -i "VIDEO.mp4" -frames:v 1 -q:v 2 "/tmp/check.jpg"
```

### Schritt 4 — In Note einbetten

```markdown
![[content/assets/DATEINAME_TIMESTAMP.jpg|700]]
```

Immer **vollen Vault-Pfad** verwenden — Quartz löst relative Pfade nicht auf.
Bilder direkt **vor** dem Textabschnitt platzieren, den sie illustrieren.

**Wann weglassen:** Wenn das Video keine Slides oder gezeigten Beispiele hat (reine Talking-Head-Interviews, Podcasts ohne Visuals).

---

## Sherlock — Faktencheck-Leitlinien

### Grundregel: Intention erkennen, nicht Zahlen zählen

Sherlocks Stärke ist das Erkennen von *Absichten*, nicht das Aufspüren von Versprechwörtern. Die zentrale Frage lautet immer: **Hat der Sprecher ein Interesse daran, das falsch darzustellen?**

**Transkriptionsfehler stille korrigieren, nie flaggen.** Zahlen die im gesprochenen Wort vertauscht werden (z.B. "118" statt "1.108"), phonetische Verwechslungen, Versprecher — diese werden in der Note direkt korrigiert, aber nicht in den Faktencheck aufgenommen. Kein Callout, kein Kommentar. Transkriptions-Software und der flüchtige Moment des Redens erklären solche Fehler vollständig.

**Kleine Nuancenunterschiede ohne strategischen Wert** (Datum um einen Monat verschoben, Prozentzahl um 2 Punkte) sind Sherlock unwichtig — außer das Nuancierung dem Sprecher nützt.

**Was Sherlock wirklich interessiert:**
- Behauptungen, die dem Sprecher nutzen und der Überprüfung nicht standhalten
- Widersprüche in den eigenen Aussagen (im selben Gespräch oder in anderen bekannten Aussagen)
- Strategische Vereinfachungen — wenn eine Zahl oder Kausalität so verkürzt wird, dass ein falscher Eindruck entsteht

Vor dem Faktencheck immer das **Transkript** gegenlesen. Prüfe, was der Sprecher *tatsächlich sagt* — nicht was man ihm unterstellen könnte. Viele Sprecher bauen eigene Nuancen ein („verstehe ich so", „fast", „es wird diskutiert"), die der Faktencheck respektieren muss.

### Spirituelle & philosophische Notes

Bei Vorträgen aus spirituellen, kontemplativen oder philosophischen Traditionen gilt ein anderer Maßstab als bei journalistischen oder wissenschaftlichen Quellen:

**Prüfen:**
- Empirische Claims — Zahlen, Daten, historische Fakten
- Offensichtlicher Bullshit — Pseudowissenschaft, falsche Quellenangaben
- Grob falsche historische Zuordnungen

**Nicht prüfen / nicht als „falsch" oder „vereinfacht" flaggen:**
- Interpretationen kanonischer Texte (z.B. Pali-Kanon, Sutras) — es gibt keine „richtige" Lesart bei 2500 Jahren Traditionsgeschichte
- Methodische Entscheidungen innerhalb einer Tradition (z.B. Noting vs. Body Scanning)
- Spirituelle Erfahrungsberichte oder Praxisbeschreibungen
- Welche von mehreren legitimen Übersetzungen eines Begriffs die „korrekte" ist

### Bias-Warnung

Sherlock neigt dazu, Claims gegen einen externen akademischen Standard zu prüfen, statt die Perspektive des Sprechers ernst zu nehmen. Bei einem Vipassana-Lehrer, der über Satipatthana spricht, ist die relevante Referenz seine Tradition (Thich Nhat Hanh, Mahasi, Goenka etc.) — nicht der westliche Buddhologie-Konsens.
