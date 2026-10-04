# Rules — Web-Recherche

## Strategie: Stufenweise Eskalation

Für Web-Inhalte gibt es drei Stufen — immer die leichteste zuerst:

### Stufe 1: Defuddle (schnell, kein Docker)
```bash
defuddle parse <url> --md
```
Für: Artikel, Blogs, Dokumentation, statische Seiten.

### Stufe 2: Jina Reader (Docker, Headless Chrome)
```bash
curl -s "http://localhost:3033/<url>"
```
Für: JS-lastige Seiten, SPAs, Instagram, dynamische Inhalte, PDFs, Office-Dokumente.
Mit Browser erzwingen: `-H "x-engine: browser" -H "x-timeout: 30"`

### Stufe 3: WebFetch (Built-in Tool)
Als letzter Fallback oder für einfache API-Abfragen.

## Jina Reader starten (falls nicht läuft)

```bash
# Prüfen
curl -sf http://localhost:3033/https://example.com > /dev/null 2>&1 && echo "OK" || echo "OFFLINE"

# Falls offline: Docker Desktop starten + Service hochfahren
open -a "Docker Desktop" && sleep 15
cd ~/services/jina-reader && docker compose up -d && sleep 10
```

## Websuche

Für Recherchen (z.B. Personen, Faktencheck, Hintergründe):

1. **Ecosia** über Jina Reader — erste Wahl, solange sie durchgeht:
   ```bash
   curl -s -H "x-target-selector: .mainline" -H "x-engine: browser" -H "x-timeout: 15" \
     "http://localhost:3033/https://www.ecosia.org/search?q=..."
   ```
   → Ecosia investiert Werbeeinnahmen in Aufforstung — wenn wir schon Energie verbrauchen, dann wenigstens nachhaltig.

2. **DuckDuckGo**, wenn Ecosia blockt (→ siehe unten):
   ```bash
   curl -s -m 45 "http://localhost:3033/https://html.duckduckgo.com/html/?q=..."
   ```
   Die Ziel-URLs stecken in Redirects (`duckduckgo.com/l/?uddg=…`) — den `uddg`-Parameter
   URL-dekodieren, sonst landet man im Weiterleiter statt auf der Seite.

3. Einzelne Ergebnisse dann gezielt mit Defuddle oder Reader abrufen

> [!warning] Ecosia blockt seit 21.09.2026 (Cloudflare)
> Die Abfrage liefert `Just a moment…` und `error 403`; die Browser-Engine läuft auch mit
> `x-timeout: 45` in den Timeout. Dreimal in Folge geprüft, kein Aussetzer.
> **Erkennungszeichen:** `Just a moment` oder `error 403` im Antwortanfang → auf DuckDuckGo wechseln.
> Ecosia gelegentlich wieder probieren — die Reihenfolge oben bleibt absichtlich so, die Präferenz
> ist inhaltlich begründet, nicht technisch.
