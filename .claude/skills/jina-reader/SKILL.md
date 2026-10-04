---
name: jina-reader
description: Fetch and convert web pages to clean LLM-friendly markdown using a local Jina Reader Docker service. Handles JavaScript-heavy sites (Instagram, SPAs), PDFs, and Word/Excel. Use as fallback when Defuddle fails or returns empty content, when JS rendering is needed, or when the user explicitly asks to use Jina Reader.
---

# Jina Reader (Local Docker Service)

Self-hosted Jina Reader on `http://localhost:3033`. Converts any URL to clean markdown via Headless Chrome. Handles JS-heavy pages, PDFs, Office documents.

## When to use

- **Defuddle returns empty or broken content** → try Jina Reader
- **JavaScript-heavy sites** (Instagram, SPAs, dynamic content)
- **PDFs, Word, Excel, PowerPoint** → converted to markdown
- **Anti-bot pages** that block simple HTTP requests
- User explicitly asks to use Jina Reader or "den Reader"

## Prerequisites

Jina Reader runs as a Docker container on the Mac. If it's not running:

```bash
# Check if running
docker ps --filter name=jina-reader --format "{{.Status}}" 2>/dev/null

# If Docker Desktop is not running, start it first
open -a "Docker Desktop"
sleep 15  # wait for Docker to initialize

# Start Jina Reader
cd ~/services/jina-reader && docker compose up -d

# Wait for startup (Chrome needs a few seconds)
sleep 10

# Verify
curl -sf http://localhost:3033/https://example.com | head -5
```

## Usage

### Basic URL → Markdown

```bash
curl -s "http://localhost:3033/https://example.com"
```

### JS-heavy pages (Instagram, SPAs)

```bash
curl -s -H "x-engine: browser" -H "x-timeout: 30" \
  "http://localhost:3033/https://www.instagram.com/username/"
```

### Useful headers

| Header | Value | Effect |
|---|---|---|
| `x-engine` | `browser` / `curl` / `auto` | Force rendering engine |
| `x-timeout` | `30` | Max wait time in seconds |
| `x-target-selector` | CSS selector | Extract only matching element |
| `x-wait-for-selector` | CSS selector | Wait until element renders |
| `x-retain-images` | `none` / `alt` / `all` | Image handling |
| `x-retain-links` | `none` / `text` / `all` | Link handling |
| `x-no-cache` | `true` | Bypass cache |
| `x-max-tokens` | `5000` | Limit output tokens |

### Token-saving mode (recommended for LLM input)

```bash
curl -s -H "x-retain-images: none" -H "x-retain-links: text" \
  "http://localhost:3033/https://example.com"
```

## Strategy: Defuddle → Jina Reader

1. **First try Defuddle** — fast, no Docker needed
2. **If Defuddle fails or returns empty** → use Jina Reader with `x-engine: auto`
3. **If still problematic** → force `x-engine: browser` with `x-timeout: 30`

## Service details

- **Image:** `ghcr.io/jina-ai/reader:oss`
- **Ports:** 3033 (HTTP/1.1), 3034 (h2c)
- **Config:** `~/services/jina-reader/docker-compose.yml`
- **Logs:** `docker logs jina-reader`
