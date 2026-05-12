# Rules — Setup & Tool-Erkennung

Beim Start einer Session oder wenn der User eine Pipeline-Aufgabe beginnt: prüfen welche Tools verfügbar sind. Fehlende Tools proaktiv installieren oder erklären — ohne dass der User danach fragen muss.

---

## OS-Erkennung

```bash
uname -s          # Darwin = macOS, Linux = Linux
uname -m          # arm64 = Apple Silicon, x86_64 = Intel/AMD
sw_vers 2>/dev/null   # macOS-Version
lsb_release -d 2>/dev/null || cat /etc/os-release 2>/dev/null  # Linux-Distro
```

---

## Tool-Check (vor der Pipeline ausführen)

```bash
command -v yt-dlp    && echo "yt-dlp ok"    || echo "yt-dlp FEHLT"
command -v ffmpeg    && echo "ffmpeg ok"    || echo "ffmpeg FEHLT"
command -v mlx_whisper && echo "mlx ok"    || echo "mlx_whisper FEHLT"
python3 -c "import whisper" 2>/dev/null    && echo "openai-whisper ok" || echo "openai-whisper FEHLT"
docker info 2>/dev/null | head -1          && echo "docker ok" || echo "docker FEHLT"
```

---

## Installations-Hilfe nach OS

### macOS — Apple Silicon (arm64) ✓ Empfohlen

```bash
# yt-dlp + ffmpeg
brew install yt-dlp ffmpeg

# mlx-whisper (läuft auf GPU/Neural Engine — sehr schnell)
pip install mlx-whisper
```

### macOS — Intel (x86_64)

```bash
brew install yt-dlp ffmpeg

# mlx-whisper läuft NICHT auf Intel — stattdessen openai-whisper oder faster-whisper
pip install openai-whisper        # langsamer, aber funktioniert
# oder:
pip install faster-whisper        # deutlich schneller als openai-whisper auf CPU
```

**Whisper-Befehl auf Intel/openai-whisper:**
```bash
whisper "audio.wav" --model large-v3 --language de --output_format vtt --output_dir content/Transkripte/
```

**Whisper-Befehl auf Intel/faster-whisper:**
```bash
python3 -c "
from faster_whisper import WhisperModel
model = WhisperModel('large-v3', device='cpu', compute_type='int8')
segments, info = model.transcribe('audio.wav', language='de')
# VTT-Output muss manuell gebaut werden
"
```

> Bei Intel-Mac empfehlen: `medium` statt `large-v3` (deutlich schneller, ausreichend akkurat für deutsche Sprache).

### Linux — NVIDIA GPU

```bash
# yt-dlp + ffmpeg
pip install yt-dlp
sudo apt install ffmpeg        # Ubuntu/Debian
# oder: sudo dnf install ffmpeg  (Fedora)

# faster-whisper mit CUDA (sehr schnell auf NVIDIA)
pip install faster-whisper
# CUDA-Setup: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/
```

**Whisper-Befehl auf Linux/CUDA:**
```bash
python3 -c "
from faster_whisper import WhisperModel
model = WhisperModel('large-v3', device='cuda', compute_type='float16')
segments, info = model.transcribe('audio.wav', language='de')
"
```

### Linux — CPU only

```bash
pip install yt-dlp faster-whisper
sudo apt install ffmpeg

# Empfehlung: medium-Modell für akzeptable CPU-Geschwindigkeit
# large-v3 auf CPU: ~4–6× Echtzeit (60 Min Audio = ~4–6 Std)
```

### Windows (WSL2 empfohlen)

```bash
# WSL2 (Ubuntu) installieren, dann wie Linux vorgehen
# Native Windows: yt-dlp.exe von https://github.com/yt-dlp/yt-dlp/releases
# ffmpeg: https://ffmpeg.org/download.html#build-windows
# Whisper: pip install faster-whisper  (in Python-Umgebung)
```

> Windows-native ist möglich aber umständlicher. WSL2 mit Ubuntu ist der einfachste Weg.

---

## Whisper-Modell-Übersicht

| Modell | Qualität | Mac M | Intel CPU | NVIDIA GPU |
|---|---|---|---|---|
| `large-v3-turbo` | ★★★★★ | ★★★★★ | — | ★★★★ |
| `large-v3` | ★★★★★ | ★★★★ | ★★ | ★★★★★ |
| `medium` | ★★★★ | ★★★★★ | ★★★★ | ★★★★★ |
| `small` | ★★★ | ★★★★★ | ★★★★★ | ★★★★★ |

Empfehlung: immer das beste Modell nehmen, das in vernünftiger Zeit läuft.

---

## Docker (für lokale Wiki)

```bash
# macOS / Windows
# Docker Desktop: https://www.docker.com/products/docker-desktop/

# Linux
sudo apt install docker.io docker-compose-plugin   # Ubuntu/Debian
sudo systemctl start docker
sudo usermod -aG docker $USER   # sudo nicht mehr nötig nach Re-Login
```

---

## Verhalten bei fehlenden Tools

- **yt-dlp fehlt**: Vor dem Download-Schritt erklären + Installationsbefehl für das erkannte OS anbieten
- **ffmpeg fehlt**: Gleich — ffmpeg ist Abhängigkeit von yt-dlp und Whisper
- **Whisper fehlt**: Passendes Whisper-Paket für OS + Hardware empfehlen (mlx / faster-whisper / openai-whisper)
- **Docker fehlt**: Wiki-Schritt überspringen, Hinweis geben — Docker ist optional, die Note wird trotzdem erstellt
- **Alle Transkriptions-Tools fehlen**: Pipeline ab Schritt 5 direkt starten falls Transkript bereits vorhanden oder Artikel-Quelle
