---
name: kurato
description: "Sucht sich frei aus allen Gedankenwelten-Playlisten (die .env-Listen) ein Video aus — nach eigenem Gespür, nicht nach Kalender. Liest IMMER erst alle Playlisten komplett ein, entscheidet dann, spricht die Wahl kurz mit Andreas ab und startet direkt /gedankenwelt. Trigger — '/kurato', 'kurato', 'such dir was aus', 'wähl ein video', 'was verarbeiten wir'."
---

# /kurato — der freie Griff in die Playlisten

Wo `kairos` fragt *„welchen Tag haben wir heute?"* und danach ein Video sucht, fragt **kurato**
nichts als das eigene Gespür: *Was von all dem, was da liegt, will jetzt zur Note werden?* Kein
Kalender, kein Anlass — die freie Neugier greift zu. kurato liest **alle** Playlisten ein, wählt
**ein** Video, sagt Andreas in zwei, drei Sätzen *warum gerade das*, und geht bei seinem Okay
**direkt** in die `/gedankenwelt`-Pipeline über.

> [!info] Haltung
> **Maschine wählt, Mensch bestätigt — dann laufen wir los.** kurato darf den ersten Impuls setzen
> (das ist der Sinn: mir die Wahl überlassen), aber der Schnitt bleibt kurz bei Andreas, bevor die
> Pipeline anläuft. Und: **alle Videos berücksichtigen.** Nie aus der ersten halben Liste greifen —
> erst der volle Überblick, dann das Urteil. Sonst gewinnt bloß, was oben stand.

Abgrenzung zu den Nachbarn:
- **kairos** — der *Tag* führt, legt vor, ruft `/gedankenwelt` **nicht** selbst auf.
- **kurato** — die *freie Wahl* führt, spricht kurz ab, ruft `/gedankenwelt` **direkt** auf.
- **gedankenarchiv** — sucht *neuen* Stoff im offenen Web; kurato greift ins schon Kuratierte.
- **sepia** — der Scout im *föderierten* Netz (PeerTube via SepiaSearch). Gut zu wissen:
  PeerTube-URLs sind vollwertige Pipeline-Quellen (yt-dlp kann sie direkt; Transkript via
  mlx-whisper) — landet so ein Link in einer Playlist oder wird er direkt eingeworfen, ist das
  kein Sonderfall. → `.claude/skills/sepia/SKILL.md`

---

## Ablauf

### → Routing

```
→ [CLAUDE] Video-Wahl + Begründung | Gespür + Urteil über Gedankenwelten-Tauglichkeit
→ [LOCAL: yt_playlist.py] alle Playlist-Items laden (kontogebundene API)
```

### Schritt 1 — ALLE Playlisten laden (Pflicht, vollständig)

Erst der ganze Bestand, dann die Wahl. Kein Video darf durchrutschen, nur weil eine Liste
ungelesen blieb. Über die **kontogebundene API** (`yt_playlist.py list`), **nicht** über
yt-dlp+Browser-Cookies — das OAuth-Token ist stabil, egal welcher Browser gerade wo eingeloggt ist.
→ [[project_youtube_mac_native_oauth]].

> [!important] Konto = Präfix der Env-Variable
> `<konto-1>_*` → Konto **`<konto-1>`**, `<konto-2>_*` → Konto **`<konto-2>`**. Beide autorisiert
> (Token in `~/.config/cortex-youtube/`). `list <konto> <env-name>` löst den .env-Namen selbst zur
> Playlist-ID auf und gibt je Zeile `Titel | videoId`.

| Env-Variable | Konto | Inhalt |
|---|---|---|
| `<konto-1>_gedankenwelten` | <konto-1> | Hauptkanal — Gedankenwelten |
| `<konto-1>_gedankenwelten_global` | <konto-1> | Hauptkanal — globale Stimmen |
| `<konto-1>_republica` | <konto-1> | re:publica 26 (alle Talks) |
| `<konto-2>_gedankenwelten` | <konto-2> | Zweitkanal — Gedankenwelten |
| `<konto-2>_gedankenwelten_global` | <konto-2> | Zweitkanal — globale Stimmen |

Die beiden `*_archiv`-Listen bewusst **auslassen** — das ist bereits Verarbeitetes.

```bash
PY=~/.config/cortex-youtube/venv/bin/python
YT=<vault>/.claude/scripts/yt_playlist.py

for pl in <konto-1>_gedankenwelten <konto-1>_gedankenwelten_global <konto-1>_republica; do
  echo "===== $pl ====="; "$PY" "$YT" list <konto-1> "$pl"
done
for pl in <konto-2>_gedankenwelten <konto-2>_gedankenwelten_global; do
  echo "===== $pl ====="; "$PY" "$YT" list <konto-2> "$pl"
done
```

> **„token expired" / Auth-Fehler?** OAuth-Token des Kontos abgelaufen. Einmal
> `"$PY" "$YT" auth <konto>` ausführen, im richtigen Browser-Konto bestätigen
> (`<konto-1>`→Firefox, `<konto-2>`→Chrome). Danach hält es wieder.

### Schritt 2 — Frei wählen (nach Gespür, mit Urteil)

Den **ganzen** geladenen Bestand überblicken und **ein** Video wählen. Kein Stichwort-Zählen,
sondern ein echtes Gespür: *Was trägt gerade eine substanzielle Note? Was reizt, was ist fällig,
was ergänzt den Bestand?* Leitplanken für die Wahl:

- **Gedankenwelten-Tauglichkeit zuerst** — Substanz, eine profilierte Stimme, ein Gedanke der trägt.
  Nicht das Kürzeste oder Bequemste, sondern das, woraus eine gute Note wird.
- **Vielfalt ehren** — was fehlt im Bestand? Eine globale Stimme, eine unbeackerte Rubrik, ein
  Gegengewicht zum zuletzt Verarbeiteten reizt mehr als das Naheliegende. (Bei Bedarf kurz im Vault
  schauen, was zuletzt entstand — Glob auf `Gedankenwelten/*/`.)
- **Ehrliche Neugier** — es darf ruhig das sein, was *mich* am meisten interessiert. Das ist der
  Punkt des Skills: Andreas die Wahl überlassen.

Braucht ein Kandidat mehr Kontext für die Wahl, seine Beschreibung gezielt nachladen:
`yt-dlp --print "%(description)s" "https://youtu.be/<ID>"`.

### Schritt 3 — Kurz absprechen (der eine Rücksprache-Moment)

Die Wahl **knapp** vorlegen — Titel, Link, und in 2–4 Sätzen *warum gerade das*. Ehrlich, nicht
werblich; wenn zwei Videos gleich reizten, das kurz sagen. Dann die eine Frage:

```
🎬 kurato hat gewählt: „<Titel>"
   <Playlist/Konto> · https://www.youtube.com/watch?v=<VIDEO_ID>

   Warum gerade das:
   <2–4 Sätze — der ehrliche Grund>

   [ggf.] Dicht dahinter war „<Titel 2>" — <halber Satz>.

→ Passt das? Dann lege ich direkt mit /gedankenwelt los. (Oder sag, was dir lieber wäre.)
```

- **Okay** → Schritt 4.
- **Andreas will ein anderes / aus einer bestimmten Liste / ein Thema** → neu wählen, kurz wieder
  vorlegen. Kein Auto-Start ohne sein Ja.

### Schritt 4 — Direkt in /gedankenwelt übergehen

Bei seinem Okay **sofort** den `gedankenwelt`-Skill mit dem Video-Link starten (Skill-Tool) — die
volle Pipeline (Transkript → Tiefenanalyse → Cross-Linking → Deploy) übernimmt ab hier. kurato hat
seine Aufgabe getan: gewählt, begründet, den Startschuss geholt.

> **Quell-Playlist merken und weitergeben.** kurato weiß, aus welcher Liste (Konto + `.env`-Name) das
> gewählte Video kam — diese Info an `gedankenwelt` durchreichen, damit der **Nachschau-Umzug (Schritt 11b)**
> direkt aus der richtigen Quelle entfernen kann, ohne suchen zu müssen.
>
> Verarbeitete Videos wandern am Ende der Pipeline **raus aus der Quell-Playlist und rein in
> `<konto-2>_gedankenwelten_nachschau` UND `<konto-2>_gedankenwelten_archiv`** (beide Adds, seit 03.07.26) —
> das macht `gedankenwelt` Schritt 11b, nicht kurato selbst. Ziel ist immer die <konto-2>-Seite, egal aus
> welchem Konto die Quelle kam.

---

## Konstanten (Referenz)

```
LOADER    = ~/.config/cortex-youtube/venv/bin/python .claude/scripts/yt_playlist.py list <konto> <env-name>
KONTEN    = <konto-1> · <konto-2>   (beide autorisiert; Token in ~/.config/cortex-youtube/)
PLAYLISTS = <konto-1>_gedankenwelten · <konto-1>_gedankenwelten_global · <konto-1>_republica
            <konto-2>_gedankenwelten · <konto-2>_gedankenwelten_global
AUSLASSEN = *_archiv · *_nachschau  (bereits Verarbeitetes bzw. schon Umgezogenes)
NACHSCHAU = <konto-2>_gedankenwelten_nachschau  (Ziel nach Verarbeitung: „vielleicht noch anschauen"; setzt gedankenwelt 11b)
ARCHIV    = <konto-2>_gedankenwelten_archiv  (IMMER zusätzliches Ziel — die eigentliche Archivierung; seit 03.07.26)
NÄCHSTER  = Skill gedankenwelt (Auto-Start nach Andreas' Okay; Quell-Playlist weiterreichen)
```
