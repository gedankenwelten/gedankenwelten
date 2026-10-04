---
name: gedankenarchiv
description: Gemeinsame Schatzsuche in offenen Archiven (archive.org, media.ccc.de, PeerTube) nach Content für die Gedankenwelten — Originalaufnahmen großer Denker, Vorträge, Interviews. Präsentiert einen Fund nach dem anderen; was nicht anspricht, wird übersprungen. Trigger — "/gedankenarchiv", "gedankenarchiv", "archiv durchsuchen", "lass uns was entdecken".
---

# Gedankenarchiv — Schatzsuche in offenen Archiven

> *Die Gedankenwelten bauen auf Denkern auf. Viele ihrer Originalstimmen liegen nicht auf YouTube, sondern in offenen Archiven — Radiointerviews aus den 50ern, Vorlesungen aus den 70ern, Konferenzvorträge von gestern. Dieser Skill gräbt sie aus.*

Interaktive Entdecker-Session: Claude sucht, prüft Provenienz, präsentiert **einen Fund nach dem anderen**. Spricht der Fund nicht an → nächster. Spricht er an → Übergabe an die `/gedankenwelt`-Pipeline.

## Trigger

- `/gedankenarchiv` (optional mit Richtung: `/gedankenarchiv Erich Fromm`, `/gedankenarchiv Demokratie`)
- "lass uns was entdecken", "archiv durchsuchen"

---

## Routing

```
→ [CLAUDE] Kuration + Provenienz-Urteil | Urteilsvermögen erforderlich
→ [LOCAL: curl] Archiv-APIs (archive.org, media.ccc.de, SepiaSearch)
```

---

## Schritt 1 — Richtung bestimmen

**Mit Argument:** direkt zu Schritt 2.

**Ohne Argument:** Nicht raten — kurz gemeinsam die Richtung finden. Dafür Kontext laden:

```bash
ls content/Denker/ content/DenkerVita/
```

Dann 3–4 konkrete Richtungen vorschlagen, z.B.:
- Einen **bestehenden Denker vertiefen** (Originalaufnahmen zu jemandem, der schon eine Note hat)
- Eine **Lücke füllen** — Denker aus der Gedankendatenbank-Vision, die noch fehlen (Frankl, Jung, Fromm, Watts, Krishnamurti, griechische Philosophie-Vorlesungen …)
- Ein **Thema** statt einer Person (Demokratie, Bewusstsein, Überwachung …)
- **Überraschung** — Claude wählt frei, was den Korpus am meisten bereichern würde

## Schritt 2 — Suchen

Quellen in dieser Reihenfolge (alle drei dürfen pro Runde angezapft werden):

### 2a — archive.org (Hauptquelle für historische Denker)

**Immer Titel-Suche, nie Volltext** — Volltext ertrinkt in Erwähnungen:

```bash
curl -s "https://archive.org/advancedsearch.php?q=title%3A%28%22SUCHBEGRIFF%22%29+AND+mediatype%3A%28movies+OR+audio%29&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=year&fl%5B%5D=collection&rows=20&output=json" \
  | python3 -c "import json,sys; r=json.load(sys.stdin)['response']; print('TOTAL:', r['numFound']); [print(d.get('year','?'), '|', d['title'][:85], '|', d.get('collection',['?'])[0] if isinstance(d.get('collection'),list) else d.get('collection','?'), '| archive.org/details/'+d['identifier']) for d in r['docs']]"
```

(Suchbegriff URL-encoden: Leerzeichen → `+`, `"` → `%22`.)

**Gold-Collections** (gezielt durchsuchbar mit `collection:NAME` statt `title:`):
- `pacifica_radio_archives` — Originalinterviews 1950er–70er (Fromm, Watts, Maslow, Huxley, Baldwin …)
- Offizielle Stiftungs-Uploads (z.B. Krishnamurti-Archiv-Sammlungen)

**Item-Details + Dateien prüfen:**

```bash
curl -s "https://archive.org/metadata/IDENTIFIER" | python3 -c "
import json,sys; m=json.load(sys.stdin)
md=m['metadata']
print('Titel:', md.get('title')); print('Jahr:', md.get('year', md.get('date','?')))
print('Collection:', md.get('collection')); print('Lizenz:', md.get('licenseurl','keine Angabe'))
print('Beschreibung:', str(md.get('description',''))[:300])
print('--- Dateien:')
[print(f['name'], f.get('length','?')+'s' if 'length' in f else '', f.get('size','?'),'bytes') for f in m['files'] if f['name'].endswith(('.mp3','.mp4','.ogg','.flac','.wav','.mkv'))]
"
```

### 2b — media.ccc.de (Netzpolitik, KI, Überwachung, Gesellschaft)

```bash
curl -s "https://api.media.ccc.de/public/events/search?q=SUCHBEGRIFF" \
  | python3 -c "import json,sys; [print(e.get('release_date','?')[:10], '|', e['title'][:80], '|', e['frontend_link']) for e in json.load(sys.stdin)['events'][:10]]"
```

### 2c — PeerTube via SepiaSearch (Bildungs-Instanzen, Uni-Vorträge)

```bash
curl -s "https://search.joinpeertube.org/api/v1/search/videos?search=SUCHBEGRIFF&count=10" \
  | python3 -c "import json,sys; [print(v['publishedAt'][:10], '|', v['name'][:80], '|', v['url']) for v in json.load(sys.stdin)['data']]"
```

## Schritt 3 — Provenienz prüfen (Pflicht vor jeder Präsentation)

Für die Denker-Rubrik zählt die *echte* Stimme. Heuristiken:

| Signal | Bedeutung |
|---|---|
| Collection = `pacifica_radio_archives`, Stiftungs-/Instituts-Sammlung | ✅ Gold — Original |
| Eigenständiger Identifier, plausibles Jahr, Beschreibung mit Aufnahmekontext | ✅ vermutlich Original |
| Identifier beginnt mit `youtube-` oder `save-tube` | ⚠️ nur ein YouTube-Spiegel — Originalquelle prüfen, ggf. trotzdem wertvoll wenn das Original gelöscht ist |
| "AI reconstruction", "AI voice", "reading of" im Titel | ❌ verwerfen — keine echte Stimme |
| Podcast-Folgen *über* den Denker | ❌ für Denker-Rubrik verwerfen (ggf. als Zeitgeist-Kandidat merken) |

Zusätzlich: Jahr + Kontext müssen plausibel sein (lebte die Person da? wo wurde aufgenommen?). Bei Zweifeln kurz websuchen — das ist ein natürlicher Mini-Sherlock.

## Schritt 4 — Einen Fund präsentieren

**Immer nur EINEN Fund pro Runde.** Format:

```
🏛️ Fund: [Titel]

| | |
|---|---|
| **Wer/Was** | [Denker, Kontext der Aufnahme] |
| **Jahr** | [Aufnahmejahr] |
| **Quelle** | [archive.org/details/... bzw. Link] |
| **Provenienz** | [Original / Spiegel / Collection] |
| **Länge** | [Dauer] |
| **Sprache** | [de/en/…] |

💭 Warum wertvoll für die Gedankenwelten:
[2–3 Sätze — echte Einschätzung, nicht Verkaufstext. Anknüpfung an
bestehende Notes/DenkerVitas nennen, wenn vorhanden.]

→ Nehmen wir den? (ja / nächster / merken / Richtung wechseln)
```

**Reaktionen:**
- **ja** → Schritt 5
- **nächster** → zurück zu Schritt 2/4, nächstbesten Fund zeigen (abgelehnte Funde in der Session nicht wiederholen)
- **merken** → in `_inbox/Gedankenarchiv-Funde.md` eintragen (Titel, Link, Einzeiler warum), dann nächsten zeigen
- **Richtung wechseln** → zurück zu Schritt 1

Nach ~5 Ablehnungen in Folge: ehrlich sagen, dass die Richtung vielleicht nicht trägt, und Kurswechsel vorschlagen.

## Schritt 5 — Switch auf den gedankenwelt-Skill

Bei Zuschlag endet das Gedankenarchiv und **der Skill `gedankenwelt` wird invoked** (Skill-Tool, mit dem Fund-Link als Argument). Ab da läuft alles in der normalen Pipeline — das Gedankenarchiv mischt sich nicht mehr ein.

Dem Switch diese Hinweise mitgeben (als Kontext für die Pipeline):

- **Quelle:** die Item-URL (`archive.org/details/…` bzw. media.ccc.de/PeerTube-Link) — diese URL gehört später auch in `Quellen & Links.md`, nicht nur "Audio-Datei"
- **Download:** archive.org → direkte Datei-URL `https://archive.org/download/IDENTIFIER/DATEINAME` per `curl -L -o` (oder yt-dlp); media.ccc.de / PeerTube → yt-dlp wie gewohnt
- **Transkription:** Archiv-Material hat fast nie Untertitel → mlx-whisper. ⚠️ Bei alten Aufnahmen (vor ~1990) oder schlechter Audioqualität `mlx-community/whisper-large-v3` statt `turbo` — robuster bei Rauschen.
- **Provenienz-Notizen** aus Schritt 3 (Jahr, Aufnahmekontext, Collection) — wertvoll für Frontmatter und Faktencheck

---

## Qualitätsfilter

- ✅ Originalstimmen, historische Interviews, vollständige Vorträge, Vorlesungen mit Substanz
- ✅ Konferenz-Talks die zur Gedankenwelten-Ausrichtung passen (Demokratie, KI, Gesellschaft, Philosophie, Bewusstsein)
- ❌ AI-Rekonstruktionen, Hörbuch-Lesungen durch Dritte, Podcast-Meta-Gespräche über Denker
- ❌ Rein technische Deep-Dives ohne gesellschaftliche/philosophische Dimension
- Im Zweifel: lieber einen Fund weniger zeigen als einen schwachen.
