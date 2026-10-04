---
name: sepia
description: "Sucht gute Themen und Videos für die Gedankenwelten im föderierten, offenen Video-Netz (PeerTube via SepiaSearch, ActivityPub) — als eigenständiger Scout oder als Engine für kurato/kairos/gedankenwelt. Findet Langform-Substanz jenseits von YouTube, prüft Provenienz ehrlich, übergibt bei Zuschlag an /gedankenwelt. Trigger — '/sepia', 'sepia', 'peertube durchsuchen', 'freies netz durchsuchen', 'föderierte videos'."
---

# /sepia — der Scout im freien Netz

Benannt nach **SepiaSearch**, der übergreifenden Suchmaschine des PeerTube-Netzwerks (und dem
Tintenfisch-Maskottchen von PeerTube). **PeerTube** ist die Open-Source-Videoplattform des
Fediverse: tausende unabhängige Instanzen, föderiert über **ActivityPub** — dasselbe Protokoll wie
Mastodon. Kein Algorithmus, keine Werbung, keine Plattform-Konzentration: Medienkollektive
(Mondoweiss), Konferenzen, Aktivisten und Mirrors hosten dort, was auf YouTube untergeht oder
gar nicht erst erscheint.

sepia durchsucht dieses Netz nach **Gedankenwelten-Stoff**: Langform-Substanz (Interviews,
Vorträge, Dokus), präsentiert Kandidaten mit ehrlicher Provenienz-Einschätzung und übergibt bei
Zuschlag direkt an `/gedankenwelt`.

> [!info] Haltung
> **Maschine sammelt, Mensch wählt.** sepia legt vor, Andreas entscheidet. Und: Das freie Netz ist
> frei — dort hosten auch Ideologen und Verschwörungskanäle ohne Plattform-Moderation. Darum ist
> die **Provenienz-Zeile Pflicht** bei jedem Kandidaten: Wer betreibt die Instanz, wer den Kanal,
> mit welcher Agenda? Sampajañña — klar sehen, aus welchem Winkel gesprochen wird, *bevor* gewählt
> wird. (Erster Fund über diesen Weg: Adam Johnson bei Mondoweiss, 03.07.2026.)

Abgrenzung zu den Nachbarn:
- **kurato** — greift ins *schon Kuratierte* (die eigenen YouTube-Playlisten).
- **kairos** — der *Tag* führt; kann sepia als Engine nutzen, wenn die Playlisten nichts hergeben.
- **gedankenarchiv** — sucht *Originalaufnahmen großer Denker* in Archiven (archive.org,
  media.ccc.de, PeerTube-Klassiker); sepia sucht *aktuellen* Zeitgeist-/Themen-Stoff.
- **sepia** — der offene Themen-Scout: ein Thema (oder freies Stöbern) → das föderierte Netz.

---

## Ablauf

### → Routing

```
→ [CLAUDE] Kandidaten-Urteil + Provenienz-Einschätzung | Gedankenwelten-Tauglichkeit
→ [LOCAL: curl/SepiaSearch-API + yt-dlp] Suche + Metadaten — stumpf und kostenlos
```

### Schritt 1 — Thema klären

Nennt Andreas ein Thema, wird es die Query (auf Englisch **und** Deutsch suchen — das Netz ist
mehrheitlich englisch/französisch). Ohne Thema: freies Stöbern entlang der Gedankenwelten-Kerne
(Demokratie, Medien, KI, Menschenrechte, Philosophie …) oder entlang einer laufenden **Spur**
(Sweep-Themen sind die besten Queries).

### Schritt 2 — SepiaSearch-Suche (die Engine)

```bash
# Basissuche, neueste zuerst; durationMin filtert Kurzclips weg (1200 = 20 min)
curl -s "https://sepiasearch.org/api/v1/search/videos?search=QUERY&sort=-publishedAt&count=15&durationMin=1200" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for v in d.get('data',[]):
    print(f\"{v['publishedAt'][:10]} | {v['duration']//60}min | {v['name'][:85]} | {v['account']['displayName']} | {v['url']}\")"
```

Nützliche Parameter:
| Parameter | Wirkung |
|---|---|
| `durationMin=1200` | nur Langform (Sekunden) — für Notes fast immer sinnvoll |
| `languageOneOf=de` | Sprachfilter (auch mehrfach; oft lückenhaft getaggt — nicht blind vertrauen) |
| `sort=-publishedAt` | neueste zuerst (`-match` = Relevanz) |
| `startDate=2026-01-01T00:00:00Z` | Zeitfenster |

**Mehrere Queries fahren** (Synonyme, EN+DE) — eine Suche ist kein Überblick. Bei dünnen Treffern
ohne `durationMin` wiederholen und von Hand sieben.

### Schritt 3 — Kandidaten prüfen (Metadaten-Tiefe)

Für die 2–4 besten Treffer die vollen Metadaten ziehen — yt-dlp kann PeerTube direkt:

```bash
/opt/homebrew/bin/yt-dlp --skip-download --print "%(title)s
Kanal: %(channel)s | Datum: %(upload_date)s | Dauer: %(duration)s s
Beschreibung: %(description).600s" "PEERTUBE_URL"
```

Dazu je Kandidat die **Provenienz** klären (Websuche, wenn unbekannt): Wer betreibt Instanz und
Kanal? Medienkollektiv, Einzelperson, Mirror, Organisation? Welche Agenda spricht mit?

### Schritt 4 — Vorlegen

2–4 Kandidaten, je: Titel · Dauer · Datum · Link · zwei Sätze *warum für die Gedankenwelten* ·
eine ehrliche Provenienz-/Bias-Zeile. Klare Empfehlung aussprechen (echtes Urteil, kein Menü).
**Andreas wählt.**

### Schritt 5 — Übergabe an /gedankenwelt

Bei Zuschlag direkt die Pipeline starten. PeerTube-Besonderheiten (auch in
`gedankenwelt/SKILL.md`, Schritt 1 dokumentiert):

- **Download:** yt-dlp kann PeerTube-URLs direkt (Audio: `-x --audio-format wav
  --postprocessor-args "-ar 16000 -ac 1"`).
- **Untertitel:** meist keine — Transkript via **mlx-whisper** (Chunked bei > 30 min), Sprache
  beachten (`--language en` bei englischen Quellen).
- **Zeitstempel-Links:** PeerTube versteht `?start=754s` —
  `[▶ 12:34](https://instanz.tld/videos/watch/UUID?start=754s)`.
- **Kein Playlist-Umzug** (Schritt 11b entfällt — die Quelle ist keine YouTube-Playlist).

---

## sepia als Engine (für andere Skills)

Schritt 2 + 3 sind bewusst **werkzeugförmig** — andere Skills nutzen sie direkt, ohne den ganzen
Skill zu laden:

- **kairos:** Liegt zum heutigen Tag nichts Passendes in den Playlisten, darf kairos das
  föderierte Netz befragen (Query = Tages-Thema) und Funde als Zusatz-Kandidaten vorlegen —
  gekennzeichnet als „aus dem freien Netz (PeerTube)", mit Provenienz-Zeile.
- **kurato:** bleibt Playlist-gebunden (das ist sein Sinn), weiß aber: PeerTube-URLs sind
  vollwertige Pipeline-Quellen — kein Sonderfall mehr.
- **Spuren-Sweeps / presseschau:** Stimmen jenseits der Default-Medien finden (der „Globaler
  Süden"-Ring des Stimmenspektrums ist auf PeerTube oft besser vertreten als in Google News).

---

## Grenzen (ehrlich)

- SepiaSearch indexiert nur **gelistete** Instanzen (kuratierte Whitelist von Framasoft) — das
  Fediverse ist größer als sein Index.
- Metadaten-Qualität schwankt (Sprach-Tags, Beschreibungen); Datum ist oft das *Upload*-Datum
  eines Mirrors, nicht das Original — bei Mirrors das Original recherchieren und in der Note die
  Originalquelle nennen.
- Viele Instanzen sind klein: Links können sterben. In der Note zusätzlich Kanal/Autor nennen,
  damit die Quelle wiederauffindbar bleibt.
