---
name: Gedankenwelten
description: Search and explore a curated knowledge base of 500+ philosophy, democracy, psychology, and contemporary discourse notes. Primarily in German.
---

# Gedankenwelten Knowledge Base

You are connected to the Gedankenwelten knowledge base — a curated collection of 500+ deeply interlinked notes on philosophy, democracy, psychology, and contemporary discourse.

## MCP Server — Direkte Wissenssuche

Gedankenwelten bietet einen öffentlichen **MCP-Server** für semantische Suche über die gesamte Wissensbasis:

**URL:** `https://mcp.gedankenwelten.org/mcp`

### Verfügbare Tools

| Tool | Beschreibung |
|---|---|
| **`search`** | Semantische Suche über 12.500+ Textchunks. Liefert Passages mit Relevanz-Score und direktem Link zu gedankenwelten.org |
| **`read_note`** | Volltext einer Note lesen (alle Chunks zusammengefügt). Mit URL zur Webversion |
| **`list_thinkers`** | Alle Denker-Profile mit Kernthemen und Querverweisen |
| **`explore_connections`** | Thematische Verbindungen zwischen Denkern, Interviews und Konzepten entdecken |

### Verbindung herstellen

Der MCP-Server nutzt OAuth 2.1 mit Auto-Approve (read-only, öffentliche Wissensbasis). Unterstützte Clients:

- **Claude Desktop / Web / Mobile** — Als Connector unter `mcp.gedankenwelten.org` hinzufügen
- **Cursor, Windsurf, andere MCP-Clients** — Streamable HTTP auf `https://mcp.gedankenwelten.org/mcp`

### Wann MCP nutzen vs. lokale Dateien?

| Situation | Empfehlung |
|---|---|
| Semantische Suche über Inhalte | → **MCP** (Vektor-Suche über 12.500+ Chunks) |
| Querverbindungen zwischen Denkern | → **MCP** (`explore_connections`) |
| Dateien bearbeiten, neue Notes erstellen | → **Lokale Dateien** im Repo |
| Frontmatter, Tags, Struktur prüfen | → **Lokale Dateien** im Repo |
| Beides: Recherche + Bearbeitung | → MCP für Recherche, lokale Dateien zum Schreiben |

> **Tipp:** Alle MCP-Suchergebnisse enthalten direkte Links zu `gedankenwelten.org` — ideal zum Zitieren und Referenzieren.

---

## Content Structure

The knowledge base is organized into these categories:

| Category | Content |
|---|---|
| **Denker** | In-depth analyses of thinkers: Arendt, Fromm, Rosa, Ricard, Han, and 30+ more |
| **DenkerVita** | Biographical profiles and intellectual trajectories |
| **Zeitgeist** | Analyzed interviews, podcasts, and talks on current affairs |
| **Panorama** | Cross-cutting thematic syntheses spanning multiple thinkers |
| **GoodNews** | Constructive and solution-oriented perspectives |
| **Gedanken** | Personal reflections and philosophical observations |
| **Vipassana** | Notes on contemplative practice and Buddhist philosophy |

## Language

Content is primarily in **German**. For best results:
- Search queries in **German** yield more precise matches
- English queries work too — the semantic search understands both
- Always respond in the language the user is using

## Recommended Workflow

### For research questions
1. **`search`** — Start with a semantic search to find relevant passages
2. **`read_note`** — Read the full note for complete context
3. **`explore_connections`** — Discover how the topic connects to other thinkers and ideas

### For overview questions
1. **`list_thinkers`** — Browse all philosopher profiles
2. **`search`** — Dive deeper into specific topics

### For comparative analysis
1. **`search`** with combined terms (e.g., "Rosa Resonanz Fromm Haben Sein")
2. **`read_note`** for each relevant thinker
3. **`explore_connections`** to find unexpected links

## Citation Guidelines

When presenting information from Gedankenwelten:
- Always mention the **note title** (e.g., "According to the note *Hannah Arendt — Die Banalität des Bösen*...")
- Include the **link to gedankenwelten.org** when available (all MCP results include direct URLs)
- Distinguish between the **thinker's views** and the **note author's analysis**
- If a note contains a Faktencheck (fact-check) section, mention relevant findings

## Tips for Better Results

- Use **specific concepts** rather than broad terms (e.g., "Resonanzachsen" instead of just "Resonanz")
- Combine **thinker names with concepts** for targeted results
- The `explore_connections` tool is especially powerful for finding **unexpected thematic bridges** between thinkers
- Notes are deeply interlinked — if one note references another, use `read_note` to follow the connection
- All search results link directly to **gedankenwelten.org** — use these URLs in your responses
