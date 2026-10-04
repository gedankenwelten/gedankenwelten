---
name: kairos
description: "Findet den besonderen Tag von heute (Welttag, Aktionstag, Gedenktag) und schlägt 1–2 dazu passende Videos aus den Gedankenwelten-Playlisten vor — mit einer kleinen Erzählung über den Tag (was, woher, wozu). Maschine sammelt, Mensch wählt. Trigger — '/kairos', 'kairos', 'welcher tag ist heute', 'besonderer tag', 'tag des'."
---

# /kairos — der Tag, der etwas bedeutet

*Kairos* ist der rechte, qualitative Augenblick — im Gegensatz zu *chronos*, der bloß
verstreichenden Zeit. Jeder Tag im Jahr trägt eine Bedeutung, die über sein Datum hinausgeht:
Welttage, Aktionstage, Gedenktage. Dieser Skill findet die Bedeutung von **heute**, schaut nach,
ob in den Gedankenwelten-Playlisten etwas Passendes liegt, und legt dir 1–2 Videos plus eine kleine
Erzählung über den Tag vor — als **Vorschlag**. Die Wahl und der Schnitt bleiben bei dir; die Note
baust du danach selbst mit `/gedankenwelt`.

> [!info] Haltung
> **Maschine sammelt, Mensch urteilt.** Kairos sammelt Tag, Kandidaten und Kontext — das Urteil,
> welches Video es wird und ob überhaupt, ist deins. Und: **nichts erfinden.** Liegt heute kein Tag,
> der zu den Gedankenwelten passt, sagt Kairos das ehrlich und drängt keine Krampf-Note auf
> (Adhiṭṭhāna — „heute nichts" ist ein vollständiger Befund).

---

## Ablauf

### → Routing

```
→ [CLAUDE] Tag-Findung + Themen-Match + Tag-Erzählung | Urteil über Relevanz
→ [LOCAL: yt-dlp] YouTube-Playlist-Items laden (Mac-nativ, Browser-Cookies)
```

### Schritt 1 — Welcher Tag ist heute?

Heutiges Datum nehmen (`date +%d.%m.%Y`) und per **Websuche** herausfinden, welche besonderen Tage
heute liegen. Keine eigene gepflegte Liste — jedes Mal frisch suchen.

```
WebSearch: "<Tag>. <Monat> international day observance welttag aktionstag"
```

Die Treffer **gegen die Gedankenwelten-Themen filtern** — nicht jeder Kuriositäten-Tag zählt
(„Tag des Händeschüttelns", „Swim a Lap Day" sind kein Gedankenwelten-Stoff). Relevant ist, was an
die Rubriken andockt:

- **Menschenrechte, Demokratie, Widerstand, Frieden** (z.B. Tag der Menschenrechte, gegen Folter, der Pressefreiheit)
- **Gesellschaft & Gerechtigkeit** (Frauen, Migration, soziale Ungleichheit, Diplomatie)
- **Philosophie, Psychologie, Bewusstsein** (Welttag der Philosophie, der psychischen Gesundheit, des Glücks)
- **Wissenschaft, Wissen, Schöpferkraft** (Geistesblitz-nah)
- **Erde, Umwelt, Klima**
- **Kultur, Sprache, Erinnerung** (Welttag der kulturellen Vielfalt, der Muttersprache)

Bei mehreren relevanten Tagen den stärksten / interessantesten wählen — und die anderen nur kurz nennen.

> Bewegliche Tage (Muttertag = 2. Sonntag im Mai, Vatertag, …) ergeben sich aus der Websuche für
> das konkrete Datum — nicht selbst rechnen, die Suche kennt das Jahr.

**Wenn kein relevanter Tag:** ehrlich melden (siehe Schritt 5b). **Nicht** auf kommende Tage
ausweichen, **nichts** erfinden.

### Schritt 2 — Die Tag-Erzählung

Zum gewählten Tag einen kleinen Textbaustein schreiben — **kein Lexikon-Eintrag**, sondern in der
Gedankenwelten-Stimme (erzählen statt aufzählen, → `haltung.md`):

- **Was** ist der Tag?
- **Woher** kommt er — wer hat ihn wann ausgerufen, aus welchem Anlass?
- **Wozu** gibt es ihn — welche Frage, welches Anliegen hält er wach? (Das *Wozu* ist der Kern.)

Bei Bedarf für Herkunft/Stifter eine zweite gezielte Websuche. 4–8 Sätze. Dieser Baustein ist
**kein Wegwerf-Output** — er wandert später als Aufmacher-Kontext oder eigener Abschnitt in die Note.

> [!important] Callout-Reihenfolge im Note-Kopf (für die spätere `/gedankenwelt`-Bearbeitung)
> Wenn aus dem Vorschlag eine Note wird, gilt eine feste Reihenfolge ganz oben:
> 1. **`> [!abstract] Worum es geht`** — steht **immer ganz oben**, direkt unter der `# Überschrift`.
>    (Andreas nutzt diesen Block später für Vorschauen/Teaser — er muss der erste sein und bleiben.)
> 2. **Tag-Callout** (`> [!info] Anlass — <Name des Tages>`) — direkt **unter** „Worum es geht", noch **über** der DenkerVita / dem „Wer spricht?"-Callout. Hier lebt die Tag-Erzählung.
> 3. dann `Quelle:`-Zeile und der `> [!info] Wer spricht?`-Callout (mit DenkerVita-Link).

> [!important] Tagesnote → Pflicht-Tag `kalender`
> Jede aus einem kairos-Vorschlag entstandene Note bekommt in den Frontmatter-`tags:` den Tag
> **`kalender`** (zusätzlich zum Rubrik-Typ-Tag). So sind alle Tagesnotes — quer durch die Rubriken —
> über einen Tag auffindbar. Der Tag gehört zur Note, nicht zum Vorschlag: beim Übergang in
> `/gedankenwelt` mitgeben. → `.claude/rules/tags.md`.

### Schritt 3 — Playlisten laden (über die YouTube-API, kontogebunden)

Alle Gedankenwelten-Playlisten aus der `.env` durchsuchen — **über die API** mit
`.claude/scripts/yt_playlist.py list`, **nicht** über yt-dlp+Browser-Cookies. Grund: Andreas wechselt
oft, welches Konto in welchem Browser eingeloggt ist; Cookie-basiertes Lesen ist dadurch unzuverlässig
(leere/falsche Listen). Das OAuth-Token ist **kontogebunden und stabil**, egal welcher Browser gerade
wo eingeloggt ist. → Details: [[project_youtube_mac_native_oauth]].

> [!important] Konto = Präfix der Env-Variable
> `<konto-1>_*`-Listen → Konto **`<konto-1>`**, `<konto-2>_*`-Listen → Konto **`<konto-2>`**. Beide sind
> autorisiert (Token in `~/.config/cortex-youtube/`). `yt_playlist.py list <konto> <env-name>` löst den
> .env-Namen selbst zur Playlist-ID auf und gibt `Titel | videoId` aus.

| Env-Variable | Konto | Inhalt |
|---|---|---|
| `<konto-1>_gedankenwelten` | <konto-1> | Hauptkanal — Gedankenwelten |
| `<konto-1>_gedankenwelten_global` | <konto-1> | Hauptkanal — globale Stimmen |
| `<konto-1>_republica` | <konto-1> | re:publica 26 (alle Talks) |
| `<konto-2>_gedankenwelten` | <konto-2> | Zweitkanal — Gedankenwelten |
| `<konto-2>_gedankenwelten_global` | <konto-2> | Zweitkanal — globale Stimmen |
| `<konto-2>_gedankenwelten_pro` | <konto-2> | **Diogenes-Pool** — was der nächtliche Späher gefunden hat (seit 10.09.2026) |

> [!tip] `gedankenwelten_pro` — der Diogenes-Pool gehört dazu (seit 10.09.2026)
> Was der nächtliche Späher findet, liegt in `<konto-2>_gedankenwelten_pro` — inzwischen der größte und
> thematisch breiteste Vorrat, gerade in den Feldern, die der Vault noch nicht hat. Kairos sucht dort
> mit. Ein Fund aus dem Pool ist kein Fund von außen (Schritt 5a), sondern ein regulärer Kandidat —
> im Report aber als **Diogenes-Fund** kenntlich machen und die Nacht nennen, aus der er stammt
> (`.claude/data/diogenes/<datum>-<host>.json`). Diogenes' `urteil` und `warum` sind dann schon
> geschrieben — nicht neu erfinden, sondern auf den Tag hin lesen.

```bash
PY=~/.config/cortex-youtube/venv/bin/python
YT=<vault>/.claude/scripts/yt_playlist.py

for pl in <konto-1>_gedankenwelten <konto-1>_gedankenwelten_global <konto-1>_republica; do
  echo "===== $pl ====="; "$PY" "$YT" list <konto-1> "$pl"
done
for pl in <konto-2>_gedankenwelten <konto-2>_gedankenwelten_global <konto-2>_gedankenwelten_pro; do
  echo "===== $pl ====="; "$PY" "$YT" list <konto-2> "$pl"
done
```

Ausgabe je Zeile: `Titel | videoId`. Reicht fürs Matching meist; braucht ein Kandidat mehr Kontext,
dessen Beschreibung gezielt mit yt-dlp nachladen (`yt-dlp --print "%(description)s" "https://youtu.be/<ID>"`).

> **„token expired" / Auth-Fehler?** Das OAuth-Token des Kontos ist abgelaufen (Testing-Modus → 7 Tage).
> Einmal `"$PY" "$YT" auth <konto>` ausführen — der Link wird ausgegeben, im richtigen Browser-Konto
> bestätigen (`<konto-1>`→Firefox, `<konto-2>`→Chrome). Danach hält es wieder (dauerhaft, wenn der
> Consent-Screen auf „In production" steht).

### Schritt 4 — Match: passt ein Video zum Tag?

Titel + Beschreibungen aller geladenen Videos gegen das **Thema des Tages** prüfen. Echtes Urteil,
kein Stichwort-Zählen: Würde dieses Video eine Note tragen, die *zu diesem Tag* etwas zu sagen hat?

- **1–2 Treffer** → als Kandidaten vorschlagen, je mit kurzer Begründung *warum es zum Tag passt*.
- Lieber **ein** wirklich passendes Video als zwei mittelmäßige.

### Schritt 4b — Bestand: passen bestehende Notes zum Tag? (seit 06.07.2026)

Zusätzlich zu den neuen Videos den **Bestand** prüfen: Gibt es Gedankenwelten-Notes, die zum Tag
passen? (RAG-Query auf `query-gedankenwelten` mit dem Tages-Thema und/oder `Gedankenwelten.md` scannen.)
Beispiel: Zum Geburtstag des Dalai Lama passen die Goenka- und die Ricard-Note.

- **1–3 Bestands-Notes** als eigenen Block im Report vorschlagen, je mit einem Satz *warum sie zum Tag passt*.
- **Was bei Zuschlag passiert:** Nur das `aktualisiert:`-Frontmatter der Note auf **heute** setzen —
  so floatet sie im Startseiten-Journal von gedankenwelten.org wieder hoch. Das ist eine bewusste,
  von Andreas gewollte Ausnahme von der „nie bei reinem Cross-Linking bumpen"-Regel: Der Tag *ist*
  der Anlass des Resurfacing. Danach normal committen + syncen (das Journal baut sich beim Sync neu).
- **Kein Zusatz in der Note selbst:** Bestands-Notes bekommen **keinen** Anlass-Callout, **keinen**
  `kalender`-Tag und keine Texterwähnung des Tages — der Tag gilt nur für dieses eine Jahr, die Note
  ist zeitlos.
- Bestand ersetzt die Video-Suche nicht — beides anbieten, Andreas wählt (Video, Bestand, beides oder nichts).

### Schritt 5a — Fallback: nichts in den Playlisten

Passt kein Video aus den Playlisten, **ein** passendes von außen suchen — zwei Engines:

1. **Websuche/YouTube** — ein Vortrag, Interview oder eine Doku zum Thema des Tages, die zur
   Gedankenwelten-Ausrichtung passt (Substanz, kein Clickbait, möglichst bekannte/profilierte Stimme).
2. **Das freie Netz (PeerTube via SepiaSearch)** — die `sepia`-Engine
   (`.claude/skills/sepia/SKILL.md`, Schritt 2+3): SepiaSearch-API mit dem Tages-Thema als Query
   (EN+DE, `durationMin=1200`), Metadaten via yt-dlp, **Provenienz-Zeile Pflicht**. Dort liegt oft,
   was YouTube nicht hochspült — gerade bei Menschenrechts-, Süd- und Aktivisten-Themen.

Funde als Vorschlag mit Link + Begründung ausgeben, **klar als Fund-von-außen** markiert (nicht aus
den Playlisten), PeerTube-Funde zusätzlich als „aus dem freien Netz (PeerTube)".

### Schritt 5b — Fallback: gar kein relevanter Tag

Liegt heute kein Gedankenwelten-relevanter Tag, das ehrlich sagen:

```
🗓️ Heute, <Datum>, liegt kein Tag, der zu den Gedankenwelten passt.
(Gefunden: <ggf. die irrelevanten Kuriositäten-Tage, einzeilig>)
Kein Zwang — wir können trotzdem frei aus den Playlisten wählen, wenn du magst.
```

---

## Abschluss-Report

```
🕊️ /kairos — <Datum>

📅 Tag: <Name des Tages>
   <2–3 Sätze Tag-Erzählung: was · woher · wozu>

🎬 Vorschlag aus den Playlisten:
   1. „<Titel>" — <Kanal/Playlist>
      → warum es zum Tag passt: <Begründung>
      https://www.youtube.com/watch?v=<VIDEO_ID>
   [ggf. 2.]

   [oder bei Fallback 5a:]
🔎 Nichts in den Playlisten — Fund von außen:
   „<Titel>" (<Quelle>) — <Begründung>
   <Link>

📚 Aus dem Bestand (passt zum Tag, Schritt 4b):
   - [[<Note>]] — <warum sie zum Tag passt>
   [max. 3; bei Zuschlag nur aktualisiert: bumpen — kein Callout, kein kalender-Tag]

📝 Tag-Erzählung (für die Note):
   <der volle Textbaustein aus Schritt 2>

→ Wenn dir ein Video zusagt: starte /gedankenwelt mit dem Link.
  Die Tag-Erzählung kommt als Aufmacher-Kontext in die Note.
→ Wenn dir Bestands-Notes zusagen: sag welche — sie werden nur gebumpt.
```

Kairos **erstellt keine Note** und ruft `/gedankenwelt` **nicht** selbst auf — er legt vor, du wählst.

---

## Konstanten (Referenz)

```
LOADER    = ~/.config/cortex-youtube/venv/bin/python .claude/scripts/yt_playlist.py list <konto> <env-name>
            (kontogebundene API; löst .env-Namen → Playlist-ID; gibt "Titel | videoId")
KONTEN    = <konto-1> · <konto-2>   (beide autorisiert; Token in ~/.config/cortex-youtube/)
PLAYLISTS = <konto-1>_gedankenwelten · <konto-1>_gedankenwelten_global · <konto-1>_republica  (Konto <konto-1>)
            <konto-2>_gedankenwelten · <konto-2>_gedankenwelten_global · <konto-2>_gedankenwelten_pro  (Konto <konto-2>)
NACHSCHAU = <konto-2>_gedankenwelten_nachschau  (Ziel nach Verarbeitung — IMMER <konto-2>, egal welches Quell-Konto)
ARCHIV    = <konto-2>_gedankenwelten_archiv  (IMMER zusätzliches Ziel — die eigentliche Archivierung; seit 03.07.26)
WRITE     = yt_playlist.py add|remove|cleanup|dedupe|sweep …   (Umzug macht gedankenwelt Schritt 11b,
            nicht kairos: add <konto-2> …nachschau + add <konto-2> …archiv + cleanup <videoId>
            — cleanup entfernt aus ALLEN Quell-Playlisten (auch Dubletten) + verifiziert;
              Exit ≠ 0 laut melden)
PFLEGE    = sweep --dry-run   (archiviertes, das noch in Quell-Listen hängt)
            dedupe <konto> <playlist> --dry-run   (mehrfach eingetragene Videos einer Liste)
            — zwei verschiedene Probleme, sweep sieht Dubletten nicht
```
