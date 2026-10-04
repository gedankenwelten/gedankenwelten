---
name: gedankenart
description: "Erstellt und generiert ein Gedankenwelten-Banner (1200x500) für eine Note oder DenkerVita — Prompt komponieren, über die fal.ai-API generieren (gen_banner.py), einbetten, deployen. Wählt frei eine Künstlerhand, die genau diese Note übersetzt — Klee ist die warme Haussprache, aber kein Default. Jede Note verdient ihre eigene Kreation. Manuell triggern mit einem Link zur Note."
---

# Gedankenart — Banner-Generator

Erstellt das Banner einer Gedankenwelten-Note oder DenkerVita: Prompt komponieren, **direkt über
die fal.ai-API generieren** (seit 03.07.2026), einbetten, deployen.
Format: 1200×500px. Stil: wird aus dem Inhalt der Note abgeleitet.

## Ablauf

### Schritt 1 — Note laden

```bash
defuddle parse <URL> --md
```

Fallback bei leerem Output: Jina Reader (`curl -s "http://localhost:3033/<URL>"`).

### Schritt 2 — Den Kern finden

Die Note lesen und eine einzige Frage beantworten:

**Was ist das Bild, das diese Note verdient?**

Nicht: was sind die Themen? Nicht: welche Struktur bietet sich an? Sondern: wenn diese Note ein Gemälde wäre — was würde man sehen?

Dafür relevant:
- Der `[!abstract]`-Callout — destillierter Kern
- Die stärkste Metapher oder das stärkste Bild im Fließtext
- Das zentrale Spannungsfeld — Gegensatz, Bewegung, Verwandlung
- Ton und Temperatur der Note: kühl/warm, ruhig/aufgewühlt, abstrakt/körperlich

### Schritt 3 — Eine Hand für diese Note finden

Eine Frage, ehrlich gestellt: **Welche Künstlerhand würde genau diese Note malen?**

Nicht *welcher Stil passt zum Thema* — das führt zu Reflexen (jede politische Note → rote Keile). Sondern: Diese eine Gedankenwelt, mit ihrem Ton, ihrer Temperatur, ihrem zentralen Bild — wessen Hand übersetzt *sie*? Jede Note verdient ihre eigene Kreation. Die Gedanken sind frei, die Künste auch.

Die ganze Kunstgeschichte ist die Palette — nicht eine Liste. Europäische Moderne, klar; aber auch japanischer Holzschnitt (Hokusai, Hiroshige), visionäre Linien (Blake, Redon), spirituelle Diagramme (Hilma af Klint), Surrealismus (Remedios Varo, de Chirico), soziales Mitgefühl (Kollwitz, Ben Shahn), volle Menschenszenen (Bruegel), persische Miniatur, mexikanischer Muralismus, Holzschnitt-Expressionismus, Witz und Linie (Steinberg, Miró), Farbfeld und Stille (Rothko, Agnes Martin). Was die Note trägt, gilt — auch ein Stil, der hier noch nie auftauchte.

**Paul Klee bleibt die warme Haussprache** — Aquarell, flache Geometrie, geerdete Palette, oft mit eingewobenen Worten (siehe das Urner-Banner). Greif danach, wenn er diese Note *wirklich* trägt — nicht als Default, in den man fällt, wenn einem nichts Besseres einfällt.

Ein paar Hände, die wir schon nutzten — als Anstoß, nicht als Auswahlmenü:

| Hand | Klingt nach |
|---|---|
| **Klee** | Aquarell, Bauhaus-Geometrie, geerdet, verspielt, Worte im Bild |
| **Kandinsky** | Innere Klänge, konzentrische Kreise, Schwingung, intensive Farbe |
| **Cy Twombly** | Geste, Kratzer, Text als Spur, mediterrane Wärme, fragmentarisch |
| **Mondrian** | Reduktion, schwarzes Gitter, Primärfarben, binäre Struktur |
| **El Lissitzky** | Rot/Schwarz/Weiß, konstruktivistische Dynamik, Agitation |
| **Egon Schiele** | Körper, Verletzlichkeit, angespannte Linien, gebrochene Figur |

> [!note] Vielfalt ist Nebenprodukt, keine Regel
> Das **einzige** Ziel ist, die Person (DenkerVita) oder das Thema (Note) im Bild stark darzustellen —
> Bilder sagen mehr als tausend Worte. Es gibt **keine feste Anti-Wiederholungs-Regel**: Wenn ein schon
> verwendeter Stil am besten passt, ist genau das die richtige Wahl. Die letzten Banner in
> `content/assets/` darfst du als *Inspiration* anschauen — aber **nicht als Ausschlussliste**.
> „War zuletzt schon dran" ist kein Grund gegen einen Stil. Der Fehler geht in beide Richtungen: weder in
> Klee/Lissitzky zurückfallen, weil sie „immer passen", noch einen passenden Stil meiden, nur weil er
> kürzlich dran war. Vielfalt entsteht von selbst, wenn du ehrlich aufs Motiv schaust.

Die Wahl ist deine. Triff sie bewusst, begründe sie dir in einem Satz — und steh dazu.

### Schritt 4 — Prompt komponieren

Freie Komposition. Keine vorgeschriebene Struktur.

**Was erlaubt ist:**
- Links-Mitte-Rechts wenn es passt — aber kein Muss
- Zentrum-dominiert, Oben-Unten, Vorher-Nachher, freie Verteilung
- Text im Bild wenn er trägt — aber kein Muss
- Ein einziges starkes Bild ohne Labels
- Mehrere kleine Szenen, eine große Geste, ein abstraktes Feld

**Was immer gilt:**
- Format: 1200×500px, breites Banner
- Konkrete Objekte und Figuren statt abstrakte Beschreibungen
- Keine realistischen Gesichter
- No photorealism

Der Prompt beschreibt was im Bild ist — nicht was es bedeutet. Das Modell malt, nicht erklärt.

> [!tip] Material und Werkzeug nennen, nicht nur die Hand (gelernt am 03.08.2026)
> „Im Stil von X" liefert die *Farben* einer Künstlerhand. Wer zusätzlich **Werkzeug, Farbauftrag und
> Oberfläche** beschreibt, bekommt die **Haptik** — und die trägt ein Banner deutlich weiter, weil das
> Bild dann eine physische Existenz vortäuscht statt eines Filters.
>
> Belegt an fünf Bannern desselben Tages:
> - **Etel Adnan** → *„thick unblended oil paint applied with a palette knife", „visible knife strokes
>   and ridges of paint", „matte finish"* → die Farbwülste heben sich sichtbar von der Fläche ab,
>   als läge echte Ölfarbe auf. Der Effekt, den Andreas als „3D" bemerkte.
> - **Kurt Schwitters** → *„torn edges", „aged adhesive stains", „small geometric wooden elements"* →
>   Tiefe aus geschichtetem Material statt aus Farbe.
> - **Käthe Kollwitz** → *„charcoal and lithographic crayon on grey laid paper", „the grain of the paper
>   showing through"* → das Papier wird als Papier lesbar.
>
> **Kein Pflichtfeld — nur wo die Körperlichkeit der Note dient.** Sonst wird daraus eine Tapete: jedes
> Banner plötzlich spachtelrauh, und die Regel frisst die Stilvielfalt (→ `feedback_gedankenart_stilvielfalt`).
> Die Gegenprobe steht im gleichen Lauf: Der Lawrence für die GfbV-Note wollte ausdrücklich *„flat opaque
> tempera", „matte surface"* — flache Plakatflächen, weil das Bild eine erzählende Tafel ist und kein Objekt.
> Klees Aquarell wollte dünne Waschungen. Beiden hätte Impasto den Gedanken kaputtgemacht.
>
> Wenn es passt, reicht ein Halbsatz zu **Träger, Auftrag oder Finish** — nicht zu allen drei. Sinnvoll
> vor allem dort, wo die Malerei selbst Thema ist: Beharrlichkeit (Adnan malt denselben Berg hundertmal),
> Zusammengesetztes (Schwitters), Handgemachtes gegen Glätte. Bei Poster-, Vektor- oder Druckregistern
> **weglassen**.

### Schritt 5 — Bild generieren (API, seit 03.07.2026)

Das Bild wird **direkt über die fal.ai-API** generiert — kein manuelles Web-UI mehr:

```bash
python3 .claude/scripts/gen_banner.py \
  --prompt "<der komponierte Prompt>" \
  --out "<NOTE-SLUG>-banner"
# optional: --model recraft --style vector_illustration  (für grafische Linien-/Vektor-Stile)
```

- Generiert 1216×512 (FLUX.2 Pro), croppt zentriert auf exakt 1200×500, legt das JPEG
  direkt in `content/assets/` ab. Kosten ~2–4 ct/Bild. Key: `FAL_KEY` in `.env`.
- **Prompt-Länge:** mittellang funktioniert am besten — ein Hauptmotiv, 2–3 Nebenelemente,
  Palette, Stil-Nennung. Keine Schachtelsatz-Epen.
- **Danach das Bild ansehen** (Read auf die JPG) und ehrlich urteilen: Trägt es? Bei Schwächen
  Prompt schärfen und neu generieren (billig). Dem User das Ergebnis zeigen.
- Danach ein Satz: welche eine Entscheidung (Stil, Komposition, Motiv) den Unterschied macht.
- *Fallback:* Wenn die API klemmt, den Prompt kopierbereit ausgeben (alter Weg — User generiert
  extern, z.B. Grok imagine, und gibt Paste/Pfad zurück).

> [!warning] Gefälschte Künstlersignaturen — die untere rechte Ecke prüfen (29.08.2026)
> Bei Händen, deren Signatur zum Stil gehört, setzt FLUX sie **mit ins Bild** — ein Kürzel, das ein
> echtes Gemälde dieser Person behauptet. Belegt an zwei Bannern desselben Laufs (Bernard Buffet für
> die Sartre-Vita, Georges Rouault für die Weil-Vita); beim Buffet blieb sie auch stehen, nachdem der
> Prompt sie ausdrücklich verboten hatte — *„absolutely no signature, no monogram, no initials"* half
> nichts. Negativ-Prompting greift hier nicht.
>
> Die Hand **nennen** wir offen im 🎨-Block; ein Signaturkürzel im Bild ist etwas anderes. Also nach
> jeder Generierung die Ecken ansehen und, wenn nötig, mit einer gespiegelten Nachbarfläche überdecken —
> das ist billiger und treffsicherer als neu zu würfeln:
>
> ```bash
> # Patch aus der Fläche links daneben, horizontal gespiegelt über die Signatur gelegt
> ffmpeg -y -i banner.jpg -filter_complex \
>   "[0:v]crop=140:115:930:385,hflip[patch];[0:v][patch]overlay=1060:385" -q:v 2 out.jpg
> ```
>
> Werte an das Bild anpassen (`crop=B:H:X:Y`, `overlay=X:Y`) und das Ergebnis nochmal ansehen. Eine
> ruhige, gleichmäßige Quellfläche in derselben Beleuchtung schließt unsichtbar an.

> [!warning] „Timeout" heißt fast nie Ausfall — es heißt Queue
> Die fal-Queue für `flux-2-pro` steht zeitweise still und wird dann in einem Schwung durchgelassen:
> **Rechenzeit 7–38 s, Wartezeit 11–32 min** (gemessen 01.08.2026, Warteposition 1097). Am selben Tag
> galten deshalb **zehn** Läufe als „FLUX antwortet nicht" — die Bilder lagen alle fertig da.
> - Bei Timeout **nicht** sofort auf Recraft ausweichen, sondern `--wait 1800` setzen. Das Skript meldet
>   die Warteposition beim Start und alle 60 s ein Lebenszeichen; lange Läufe gehören in den Hintergrund.
> - Jede Einreichung steht in `.claude/data/fal-jobs.jsonl`. Nachträglich abholen:
>   `python3 .claude/scripts/fal_fetch.py <request_id>` — oder `--list` für die fal-Historie
>   (auch für Läufe, die **vor** dem Protokoll lagen; API-Limit 50 pro Abfrage).
> - **Recraft ist kein gleichwertiger Ersatz.** Es folgt dem Stilwort und verwirft die Komposition:
>   Mehr-Element-Szenen (Figur *und* Himmel *und* Detail am Rand) kann es nicht, Prompts sind auf
>   1000 Zeichen begrenzt (sonst HTTP 422). Für erzählende Banner lohnt das Warten auf FLUX.

### Schritt 6 — Bild einbetten

Das generierte Banner in die Note einbetten — **so und nicht anders**:

> [!danger] Kein `banner:`-Frontmatter
> Das `banner:`-Feld im Frontmatter wird von **keiner** Quartz-Komponente gerendert — weder im
> privaten Cortex-Wiki noch auf gedankenwelten.org. Banner werden **als Bild-Embed im Note-Body**
> eingebettet, direkt unter der `# Überschrift`. Nur das rendert auf beiden Seiten.

**1. Asset liegt schon richtig** — `gen_banner.py` legt es als `content/assets/<NOTE-SLUG>-banner.jpg` ab.
Namenskonvention: Note-Slug + `-banner` (Em-Dash entfernt, Leerzeichen → `-`), bei DenkerVitas
`<Vorname-Nachname>-vita-banner`. Nur beim manuellen Fallback selbst kopieren:

```bash
# Note-Slug = URL-Slug: "Koschi Politik — Trump gegen Papst Leo" → "Koschi-Politik-Trump-gegen-Papst-Leo"
cp "<QUELLE>" "content/assets/<NOTE-SLUG>-banner.jpg"
```

**2. Embed unter die `# Überschrift`** — voller Vault-Pfad, Breite `|1200`, danach Easter-Egg-Callout:

```markdown
# <Titel der Note>

![[content/assets/<NOTE-SLUG>-banner.jpg|1200]]

<details><summary>🎨</summary>

**<Künstlername>** — <Stil, Palette, Kernmotiv>. <Warum genau diese Hand für genau diese Note — ein, zwei Sätze.>

*Prompt:* <Der vollständige Bildgenerierungs-Prompt, kopierbereit.>

</details>

> [!abstract] Worum es geht
...
```

Das Embed steht **vor** dem `[!abstract]`-Callout bzw. der `Quelle:`-Zeile — ganz oben im Body,
unmittelbar nach der `#`-Zeile. Der `<details>`-Block folgt direkt auf das Bild — ein winziges
`▶ 🎨` ohne Farbe oder Icon, nur für Neugierige. Darin: Künstler, Kompositionslogik, Warum —
und der vollständige Prompt zum Nachgenerieren. Kein farbiger Callout-Kasten.

**3. Deploy auf beide Seiten** (Banner gehören *immer* auf beide — privat + online):

```bash
# Cortex committen (privates Wiki baut daraus)
git add -A && git commit -m "<sektion>: <Note> — Banner-Bild hinzugefügt (<Stil>-Stil)"
git push
ssh <server> "~/services/cortex/scripts/pull-and-rebuild.sh"

# gedankenwelten.org (öffentlich) — EIN Befehl, Assets inklusive
<vault>/.claude/scripts/sync-from-cortex.sh
```

> [!tip] Assets laufen automatisch mit
> `sync-from-cortex.sh` synct den kompletten `content/assets/`-Ordner ins öffentliche Repo,
> baut das Journal, committet und pusht zu GitHub — der Pi-Cron baut dann gedankenwelten.org neu.
> Solange das Bild in `content/assets/` liegt und per Embed referenziert ist, landet es
> automatisch online. **Nie** das alte `~/services/gedankenwelten/scripts/sync.sh` benutzen — das
> überträgt keine Assets.

Referenz für ein korrekt eingebettetes Banner:
`content/Gedanken/Das unsichtbare Netzwerk — Potenziale und Gefahren.md`
