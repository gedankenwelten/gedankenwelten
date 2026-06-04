---
title: MCP Server
date: 2026-05-31
tags: []
aliases:
  - MCP Documentation
  - Gedankenwelten MCP
---

# Gedankenwelten MCP Server

> [!abstract] Talk to the knowledge base
> Search across 500+ curated notes on philosophy, democracy, psychology, and contemporary discourse — using your own AI assistant.

**URL:** `https://mcp.gedankenwelten.org/mcp`

---

## What is this?

The Gedankenwelten MCP Server lets you connect your AI assistant (Claude, Cursor, Windsurf, or any MCP-compatible client) directly to the [Gedankenwelten](https://gedankenwelten.org) knowledge base.

You ask questions in natural language — the server searches semantically across 12,500+ text chunks from 500+ notes and returns the most relevant passages. Your AI assistant then synthesizes the answer.

> [!tip] Cost model
> **You** use your own AI subscription (e.g. Claude Pro). **We** provide the knowledge — at no cost.

---

## Setup

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gedankenwelten": {
      "type": "streamable-http",
      "url": "https://mcp.gedankenwelten.org/mcp"
    }
  }
}
```

Config file location:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Restart Claude Desktop after saving.

### Claude.ai (Web & Mobile)

1. Go to [claude.ai](https://claude.ai) → Settings → Connectors
2. Click "Add Connector"
3. Enter URL: `https://mcp.gedankenwelten.org/mcp`
4. Follow the OAuth authorization flow (auto-approved)

### Other MCP Clients

Any client supporting the **Streamable HTTP** transport can connect:

```
URL: https://mcp.gedankenwelten.org/mcp
Auth: OAuth 2.1 (auto-approved, no account needed)
```

---

## Available Tools

### 🔍 Semantic Search

Search across all notes with natural language queries. Returns relevant passages with relevance scores.

**Example:** *"What does Hartmut Rosa say about resonance compared to Fromm's concept of having vs being?"*

### 📖 Read Note

Read the full content of any note by title. Use after searching to get complete context.

**Example:** *"Read the full note on Hannah Arendt — The Banality of Evil"*

### 👤 List Thinkers

Browse all philosopher and thinker profiles with their key topics and cross-references.

**Example:** *"Show me all thinkers in the knowledge base"*

### 🔗 Explore Connections

Discover thematic connections between thinkers, interviews, and concepts.

**Example:** *"How do Rosa's resonance theory and Buddhist mindfulness connect?"*

### 📎 Find Sources

Get the primary sources, links, books, studies and videos behind a topic — or behind a specific note.
The references you can actually share in a discussion. Filter by type (book, study, video, article, …)
or ask for the sources of one particular note.

**Example:** *"Find me sources on the rise of authoritarianism in Hungary"* · *"What sources back the BissenBlaBla note?"*

---

## Example Queries

> *"Welche Interviews behandeln den Aufstieg des Autoritarismus in Europa?"*

> *"Compare Byung-Chul Han's burnout society with Hartmut Rosa's acceleration thesis."*

> *"Was sagt Matthieu Ricard über Altruismus und wie unterscheidet sich das von Fromms Konzept der produktiven Liebe?"*

> *"Which thinkers discuss the relationship between capitalism and democracy?"*

> [!info] Language
> The content is primarily in **German**. Queries work in both German and English — the semantic search understands both.

---

## Technical Details

| Component | Details |
|---|---|
| **Transport** | Streamable HTTP |
| **Auth** | OAuth 2.1 with PKCE (auto-approved) |
| **Embeddings** | BAAI/bge-m3 (1024-dim) |
| **Vector DB** | Qdrant (12,500+ chunks) |
| **Content** | ~500 notes, updated regularly |
| **Access** | Read-only, no user data stored |

---

## Privacy

The MCP server does not store queries, track users, or collect personal data. OAuth tokens are held in memory only. See [[Datenschutz|Privacy Policy]] for details.

---

## About Gedankenwelten

[Gedankenwelten](https://gedankenwelten.org) ("thought worlds") is a curated knowledge base covering:

- **Denker** — In-depth analyses of thinkers: Arendt, Fromm, Rosa, Ricard, Han, and 30+ more
- **Zeitgeist** — Analyzed interviews, podcasts, and talks on democracy, capitalism, and media
- **Panorama** — Cross-cutting thematic syntheses
- **Vipassana** — Notes on contemplative practice

All content is publicly available at [gedankenwelten.org](https://gedankenwelten.org).

---

[[Impressum|Impressum]] · [[Datenschutz|Datenschutzerklärung]]
