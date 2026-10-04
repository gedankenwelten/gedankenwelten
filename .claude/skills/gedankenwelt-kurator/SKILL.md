---
name: gedankenwelt-kurator
description: Pflegt den Quellen-Layer der Gedankenwelten. Geht durch alle Notes, extrahiert vorhandene Quellen, vervollständigt vom Creator kuratierte Quellenlisten (YouTube-Beschreibungen) und reichert quellenlose Notes nach Review an. Aktualisiert den Quellen-Index und die RAG-Collection gedankenwelten_sources. Trigger — "/gedankenwelt-kurator", "quellen kuratieren", "quellen aktualisieren", "quellen-layer".
---

# Gedankenwelt-Kurator

Pflegt den **Quellen-Layer**: die strukturierte, über MCP abfragbare Sammlung aller Quellen und Links
der Gedankenwelten. Während der `gedankenwelt`-Skill *neue* Notes verarbeitet, geht der Kurator
*periodisch durch den Bestand* — extrahiert, vervollständigt, reichert an und hält die RAG-Collection
`gedankenwelten_sources` aktuell.

> [!info] Warum dieser Skill?
> Quellen werden in Diskussionen immer wichtiger. Aufbereitete, abfragbare Quellen ersparen die
> Live-Recherche: Über das MCP-Tool `find_sources` kann jede KI zu einem Thema oder einer Note die
> passenden Belege liefern. Dieser Skill sorgt dafür, dass der Quellen-Bestand vollständig und gepflegt ist.

---

## Architektur (Kontext)

```
Notes (.md)  ──extract_sources.py──>  .claude/data/sources.jsonl  ──ingest_sources.py──>  Qdrant: gedankenwelten_sources  ──>  MCP find_sources
```

- **Extraktor:** `.claude/scripts/extract_sources.py` (Mac) — parst Quellen aus Notes/DenkerVitas.
- **Index:** `.claude/data/sources.jsonl` — git-versioniert, eine JSON-Zeile pro eindeutiger Quelle.
- **Ingest:** `.claude/scripts/ingest_sources.py` (läuft auf dem Pi im MCP-Image) — bge-m3 → Qdrant.
- **Tool:** `find_sources(query, type?, note?)` auf `mcp.gedankenwelten.org`.

---

## Ablauf

### Schritt 1 — Extrahieren (Bestandsaufnahme)

```bash
cd <vault>/
python3 .claude/scripts/extract_sources.py --stats   # erst nur Stats, nichts schreiben
```

Report lesen: Wie viele Notes haben keine Quellen? Welche Typen sind unterrepräsentiert?
Dann den Index neu schreiben:

```bash
python3 .claude/scripts/extract_sources.py
```

### Schritt 2 — Creator-Quellen vervollständigen (Vollständigkeits-Pass)

YouTuber wie **Scobel, Jung & Naiv, MONITOR** u.a. listen in der Videobeschreibung systematisch *alle*
genannten Werke, Studien und Links. Diese vom Sprecher selbst kuratierten Listen sind die **wertvollste**
Quelle und werden **komplett** übernommen — kein Kürzen.

Für YouTube-Notes (erkennbar an `Quelle: [..](youtube.com/...)`), bei denen die `## Weiterführende
Quellen` dünn wirken oder fehlen:

```bash
yt-dlp --get-description "VIDEO_URL"
```

- **Alle** dort gelisteten Quellen, die noch nicht in der Note stehen, in `## Weiterführende Quellen`
  ergänzen (Format wie bestehende Notes, Gruppe `*Aus der Video-Beschreibung:*`).
- Diese gelten als belegt (vom Creator kuratiert) → kein Einzel-Review nötig, nur ein **Sammel-Hinweis**
  im Report („Note X: 7 Quellen aus Beschreibung übernommen").

### Schritt 3 — Lücken anreichern (mit Review)

Für Notes *ohne* belastbare Quellen bzw. mit unbelegten zentralen Claims:

1. Pro Note 1–3 Kandidaten recherchieren — **Stufen-Eskalation** aus `.claude/rules/web-recherche.md`:
   - Bücher → **genialokal.de** Suchlink (`feedback_buchlinks_genialokal`), nie Amazon
   - Artikel/Studien/Daten → **Jina Reader / Ecosia** (nie Firecrawl)
2. Kandidaten **vorschlagen** — Tabelle:

   | Note | Vorgeschlagene Quelle | Typ | Warum passend |
   |---|---|---|---|

3. **Nach Andreas' Freigabe**: Quelle in die Note schreiben (`## Weiterführende Quellen` anlegen/ergänzen),
   passend zum Inhaltsabschnitt platzieren (`feedback_quellen_inline`).
4. Geänderte Notes in die **bestehende** `gedankenwelten`-Collection re-ingestieren:
   ```bash
   bash .claude/scripts/ingest_notes.sh "content/Zeitgeist/Geänderte Note.md"
   ```

> [!warning] Ehrlichkeit vor Vollständigkeit
> Lieber keine Quelle als eine schwache. Belege müssen den Claim wirklich stützen — Yin-Yang: jede Quelle
> hat eine Perspektive, das im Zweifel benennen. Keine Quelle erfinden, keine toten Links.

### Schritt 4 — Index neu bauen + ingestieren

```bash
# Index aus den (ggf. angereicherten) Notes neu schreiben
python3 .claude/scripts/extract_sources.py

# committen + pushen
git add .claude/data/sources.jsonl Gedankenwelten/
git commit -m "quellen-kurator: Quellen extrahiert + angereichert"
git push

# Quellen-Collection auf dem Pi neu ingestieren (inkrementell, nur Geändertes wird embeddet)
ssh <server> "~/services/gedankenwelten-mcp/rebuild-sources.sh"
```

### Schritt 5 — Verifikation

```bash
# Direkt gegen das MCP-Tool prüfen (über den claude.ai Gedankenwelten-Connector):
#   find_sources("<eben angereichertes Thema>")
# Erwartung: die neuen Quellen tauchen mit echten URLs auf.
```

Oder direkt gegen Qdrant (Punktzahl sollte ~ eindeutige URLs sein):
```bash
ssh <server> "curl -s http://127.0.0.1:6333/collections/gedankenwelten_sources | python3 -c 'import sys,json;print(json.load(sys.stdin)[\"result\"][\"points_count\"],\"Punkte\")'"
```

### Schritt 6 — Logging

Eintrag in `Cortex-Log.md` (oben):

```markdown
## [DD.MM.YYYY] sources-curated | <N> Quellen, <M> Notes angereichert

**Index:** `.claude/data/sources.jsonl` (<gesamt> eindeutige Quellen)
```

---

## Leitlinien

- **Vom Creator kuratierte Quellen immer vollständig übernehmen** — sie ersparen eigene Recherche.
- **genialokal statt Amazon** für Bücher · **Jina statt Firecrawl** für Web.
- Quellen **inline beim passenden Inhaltsabschnitt** platzieren, nicht nur am Ende.
- Anreicherung **immer mit Review** (außer Creator-Listen) — Andreas entscheidet.
- Der Index ist reproduzierbar: `extract_sources.py` kann jederzeit neu laufen, ohne Daten zu verlieren.

---

## Wann ausführen?

Manuell on-demand — z.B. nach einer Reihe neuer Notes, oder wenn der Quellen-Bestand gepflegt werden soll.
Neue Einzel-Notes werden bereits vom `gedankenwelt`-Skill (Schritt 6e) automatisch in den Index aufgenommen;
der Kurator ist für den **Bestand** und die **Anreicherung** zuständig.
