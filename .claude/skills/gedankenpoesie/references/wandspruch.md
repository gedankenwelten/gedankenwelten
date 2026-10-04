# Der Wandspruch — `raetsel:` im Frontmatter

Im **Gedankenraum** (gedankenwelten.org/raum) ist jede Note ein hoher Saal; ihr Banner hängt groß an der
Stirnwand. Darüber steht, leise Ton in Ton, ein einziger **geheimnisvoller Satz** — erst sichtbar, wenn man
dem Bild nahekommt. Seit 04.10.2026 entsteht er mit der Note: `gedankenwelt` Schritt 10d, für die Note und
für jede neue DenkerVita des Laufs. Er steht im Frontmatter:

```yaml
raetsel: "Hinein führt eine Jacke. Heraus führt manchmal ein Kind."
```

## Was der Satz ist

- Ein **Rätsel, das den Inhalt nicht verrät.** Ein Bild, ein Paradox, eine leise Frage. Wer die Note kennt,
  soll nicken; wer sie nicht kennt, soll hineingehen wollen. Er fasst nicht zusammen — das tut das
  Wandschild daneben (`description:` / „Worum es geht").
- **Kurz:** höchstens ~80 Zeichen, ein oder zwei Sätze.
- **Keine Namen** und keine Schlagwörter aus dem Titel.
- Aus der **Note selbst** geschöpft: die eine Szene, das eine Bild, der eine Gedanke, der sie trägt — oft
  ein Detail, das nur wer sie gelesen hat wiedererkennt („Ein Kasten Bier auf dem Asphalt").
- Bei **DenkerVitas** deutet er auf den Menschen — seine Wunde, seine Frage, eine Szene aus dem Leben —,
  nie auf Lebensdaten allein.

## Die Hand

Jeder Satz hat **seine eigene Hand** — die Stimme, die genau diese Note sprechen würde (gedankenpoesie,
Schritt 3). Die ganze Literaturgeschichte ist die Palette: Brecht, Kafka, Celan, Bachmann, Domin, Kaléko,
Rilke, Novalis, Heine, Tucholsky, Kästner, Morgenstern, Ringelnatz, Pessoa, Borges, Szymborska, Jandl,
Hafis, Rumi, Laotse, Bashō, Langston Hughes … **In der Art** einer Hand — nie ein echtes Zitat, nie die
Ich-Stimme einer realen Person. Note und Vita derselben Person bekommen **verschiedene Bilder**.

**Luc** (Andreas' Stimme, `voices/luc.md`) ist die warme Haussprache — kein Default. Wo er die Note trägt
(Gedanken, Stille, Vertrauen, Geduld, Sehnsucht, Sein über Schein): Atem statt Absatz, ein Wort als
Herzschlag, das Du, ein sinnliches Bild (Pforte, Hafen, Garten, Nacht), stille Landung.

Die gewählte Hand in einer Zeile ankündigen: `→ [WANDSPRUCH: <Hand>] „<Satz>"` — damit Andreas mitlernt.

## Streichen (→ `ki-tells.md`)

Negative Parallelismen („nicht X, sondern Y"), Häufungswörter, Kalendersprüche, Pathos, generische
Weisheit. Kein Vipassana-Vokabular außer in Vipassana-Notes. Bei Gaza/Hamas: Hamas nie implizit
entlasten. Bei Personen mit offenen Vorwürfen: nur das Bild, keine Anschuldigung.
Schluss-Audit: „Was verrät hier noch die Maschine?" — genau das nachschleifen.

## Eichung (Satz · Hand)

- Arendt, Denken ohne Geländer: „Eine Treppe, von der jemand das Geländer abgeschraubt hat – und sie trägt trotzdem."
- Rosa, Resonanz: „Was dich berühren soll, darfst du nicht besitzen."
- How to Sell a Genocide: „Der Stuhl blieb leer. Die Sendung lief. Wer fragte, wer fehlte?" · Brecht
- Rechte Codes: „Eine Zahl, die grüßt. Nur die Eigenen grüßen zurück." · Celan
- Steelpan: „Man nahm ihnen die Trommel. Sie stimmten das Ölfass." · Langston Hughes
- Bewusstsein: „nagel. zucken. alles erklärt. nur nicht: au." · Jandl
- Marquardt, Zeit: „Du hast keine Zeit. Du bist welche." · Luc
- Misstrauensgemeinschaften: „Geld, das würden sie dir leihen. Glauben — nein." · Luc
- Glück des Schmieds: „Jeder schmiedet sein Glück. Wer aber besaß die Kohle?" · Brecht
- Sokotra: „Drachenblutbäume. In der Höhle ein Alter, der nichts mehr vermisst." · Bashō
- Kafka (Vita): „Am Tag zählte er fremde Unfälle. Nachts schrieb er seinen eigenen." · Pessoa

## Wo die Sätze liegen

- **Neu:** `raetsel:` im Frontmatter der Note — die Website liest es dort zuerst (`src/lib/notizen.mjs`).
- **Die ersten 679** (03./04.10.2026, sechs Schreiber + Durchsicht): `~/Development/gedankenwelten-neu/src/data/raum-raetsel.json`,
  die Hand je Satz in `~/Development/gedankenraum/raetsel-haende.json`. Ein Satz im Frontmatter schlägt den aus der Sammlung —
  so lässt sich jeder alte Satz in Obsidian ändern, indem man `raetsel:` in die Note schreibt.
