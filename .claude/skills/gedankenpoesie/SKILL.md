---
name: gedankenpoesie
description: "Hebt eine Gedankenwelten-Note in eine eigene Schreibstimme — das gedankenart für die Sprache. Liest die Note, schlägt aus einer offenen Palette eine Stimme vor (Luc ist die warme Haussprache, kein Default), entscheidet gemeinsam, dann veredelt es die Prosa. Tiefe + Wahrheit + Poesie, nicht übertrieben. Manuell triggern mit Note-Pfad/URL oder als Pipeline-Schritt 5c. Trigger — 'gedankenpoesie', 'stimme geben', 'poetischer machen', 'veredeln'."
---

# Gedankenpoesie — jeder Note ihre eigene Stimme

So wie `gedankenart` das **Bild** einer Note sucht, sucht `gedankenpoesie` ihre **Stimme**. Liest die Note,
wählt mit dir eine passende Schreibhand aus einer offenen Palette, hebt dann die Prosa in diese Klangfarbe.
Der mechanische KI-Standardklang entsteht nur, *weil* ohne Stimm-Vorgabe das Durchschnittsregister greift —
dieser Skill setzt die Vorgabe von Anfang an.

> [!tip] Das Ziel: der Leser verliert sich — und findet sich
> Die Stimme ist **kein Schmuck**. Ihr Ziel ist eine *Auflösung*: ein Text, so dicht und strömend, dass der
> Leser sich beim Lesen **verliert** und zugleich in den Worten **wiederfindet** — sich ohne Filter dem
> Inhalt öffnet. Das ist *anattā* auf der Ebene des Lesens. Alles Weitere — Subtraktion, Erzählen statt
> Aufzählen, das gemeinsame Herz — dient diesem **einen** Zweck: wegräumen, was den Leser *außerhalb* des
> Textes hält. Die Note ist eine **Geschichte, in der man sich verliert**, keine Aufzählung, die man abhakt.

> [!important] Substanz zuerst — Stimme ist Kür
> Dieser Skill ändert **nie, *was* eine Note sagt — nur *wie*.** Claims, Zahlen, Faktencheck-Verdikte,
> Callouts, Sokrates-Fragen, Wikilinks, der `## Verbindungen`-Block bleiben **unangetastet**. Erst die
> Substanz (Aristoteles · Sherlock · Montaigne), dann die Stimme. Eine lyrische Umformulierung darf eine
> Sherlock-Einordnung („vereinfacht" / „falsch") niemals verwischen.

> [!danger] Glätten ist der Tod der Stimme
> Eine Note, die **schon** eine echte Stimme hat (ein Luc-Text, ein Pascal-Gedanke, etwas das bereits
> trägt), wird **nicht angefasst.** Das Modell glättet sonst die rohen, echten Brüche zu kompetentem
> Pastiche. Im Zweifel: Hände weg, sag es, stopp.

## Wann

- **Standalone (Hauptweg):** `/gedankenpoesie <note-pfad-oder-url>` — jederzeit, auf jede Note. Die meisten
  Gedanken kommen nicht aus der Pipeline (sie kommen von Pascal, von dir, aus dem Archiv).
- **In der Pipeline:** Schritt 5c — *nach* Substanz (5) und Faktencheck (5b), *vor* Cross-Linking/Ingest.
  Rubrik-Default: **Gedanken → ja**, Zeitgeist/Denker/Geistesblitz → angeboten, Default nein (ihr Register
  ist analytisch). Nie Pflicht.
- **Am stärksten** in der **Gedanken**-Rubrik — sie kehrt bewusst zur Poesie zurück, ihrer Herkunft.

## Die zwei Rollen

- **Veredeln (der Kern):** fertige Note → in eine Stimme heben. Das *Heraklit für die Sprache* — Heraklit
  vertieft den Gehalt, dieser Skill veredelt den Klang.
- **Begleiten (mit Pascal):** vom leeren Blatt → zusammen mit `pascal`. Pascal hält den *Gedanken*,
  gedankenpoesie die *Klangfarbe*. So konkurriert es nicht mit Pascal und umgeht die schärfste Stelle der
  ehrlichen Grenze (vom Nichts würde das Modell erfinden *und* stilisieren — höchstes Pastiche-Risiko).

---

## Ablauf — dialogisch, nie stiller Automat

### Schritt 1 — Note laden, lesen, den Modus erkennen

Vault-Pfad → `Read`. URL → `defuddle parse <URL> --md` (Fallback Jina `curl -s "http://localhost:3033/<URL>"`).

Den **Kern, die Temperatur, das zentrale Bild** finden (wie gedankenart Schritt 2). Und: **welchen Modus**
hat der Text — Parabel/Geschichte · Prosa-Reflexion · Vers · Aphorismus? Der Modus steuert später die
Few-Shot-Wahl.

### Schritt 2 — Erst prüfen: braucht *und verträgt* die Note eine Stimme?

- **Schon gestimmt?** (Luc-Text, Pascal-Gedanke, liest sich schon getragen) → **Hände weg**, sag es, stopp.
- **Analytisch by design?** (Zeitgeist mit Faktencheck-Schwerpunkt) → höchstens behutsam, nicht ins Lyrische zwingen.
- Sonst → weiter.

### Schritt 3 — Eine Stimme für *diese* Note finden (Palette, kein Menü)

Die ehrliche Frage: **Welche Schreibstimme würde genau diese Note sprechen?** Nicht „welcher Dichter passt
zum Thema" (das führt zu Reflexen), sondern: dieser eine Ton, diese Temperatur — wessen Hand trägt *sie*?

- **Luc = die warme Haussprache** (wie Klee beim Bild). Greif danach, wenn er die Note *wirklich* trägt —
  nicht als Default, in den man fällt.
- Die ganze Literaturgeschichte ist die Palette. Ein paar Hände als Anstoß, nicht als Auswahlliste:

| Hand | Klingt nach |
|---|---|
| **Luc** | Atem statt Absatz, Ein-Wort-Herzschläge, stille Landung, Du-Anrede, Sein über Schein → `voices/luc.md` |
| **Rilke** | Ding-Gedicht, ins Herz gewendetes Bild, Ernst, *Du musst dein Leben ändern* |
| **Novalis** | Romantisieren, das Gewöhnliche geheimnisvoll machen, blaue Blume |
| **Hölderlin** | das Erhabene, Hymnik, Götter und Ströme, feierlicher Ernst |
| **Hafis** | Tanz der Worte, Wein und Rose, heitere Weisheit, Ost-West-Brücke |

> **Regel:** Öffentliche Hände (Rilke, Hölderlin …) kennt das Modell aus dem Training — ein kurzes
> Klang-Profil genügt. **Luc** kennt es nicht → eigene Datendatei `voices/luc.md` mit Few-Shot. Genau diese
> Asymmetrie ist das Prinzip: die private Haussprache braucht echte Beispiele, die öffentlichen nicht.

**2–3 Vorschläge mit je einem Satz Begründung → gemeinsam entscheiden.** Erst dann wird geschrieben.

### Schritt 4 — Klang laden

- **Luc:** `voices/luc.md` lesen **und** 2–4 Modus-passende Texte aus dem Few-Shot-Register **live** einlesen
  (`Read` auf die Pfade dort). Imitiert wird aus echten Beispielen, nicht aus Adjektiven.
- **Andere Hand:** das Klang-Profil oben + was das Modell von ihr ohnehin trägt. Bei Bedarf 1–2 echte
  Strophen als Anker zitieren (öffentlich/gemeinfrei).

### Schritt 5 — Veredeln: Subtraktion zuerst

1. **Substanz einfrieren** (siehe Kasten oben).
2. **Erst wegnehmen:** das gepolsterte Bindegewebe („darüber hinaus", „es lässt sich festhalten"),
   generische Übergänge, „X sagt/macht"-Ketten, Doppelungen. Die Stimme liegt oft schon darunter.
   → **Gegen die Streichliste prüfen: `references/ki-tells.md`** (die auditierbaren KI-Tells — allen voran
   **Negative Parallelismen** „nicht nur X, sondern Y", KI-Häufungswörter, Kopula-Vermeidung „fungiert als").
3. **Dann heben:** Atem, Bild, Du, stille Landung — was die gewählte Hand *tut*.
4. **Maß halten:** *nicht übertrieben*. Selbst-Check pro Abschnitt: „Schmuck addiert — oder Dämpfendes
   entfernt?" Im Zweifel weniger.

Und drei Prinzipien, die aus dem Sog kommen — alle dienen dem Ziel ganz oben (der Leser soll *hineinsinken*):

- **Erzähle eine Bewegung, keine Aufzählung.** Eine Note ist ein *Weg*, kein Stapel von Konzepten — ein
  Bogen mit Atem (z.B. Ohnmacht → etwas zieht → sich verlieren → sich wiederfinden → Heimkehr). Prüfe:
  liest sich das als *eine Bewegung* oder als Liste? Die Reihenfolge dient dem Sog, nicht der Vollständigkeit.
- **Viele Bilder? Gib ihnen ein gemeinsames Herz.** Häufen sich Metaphern (Faden, Same, Funke …), dann
  weder stapeln noch reflexhaft streichen — sondern unter *ein* Bild binden, das alle trägt (Ricards
  Flamme, die eine Kerze entzündet, *ist* Faden + Same + Funke in einem). Ein gemeinsames Herz löst das
  Aufzählungs-Gefühl eleganter als Kürzen — Subtraktion entfernt dann nur noch, was *diese eine* Bewegung bremst.
- **Leicht, nicht predigend.** Die Stimme darf leicht sein; kein erhobener Zeigefinger. Selbst der negative
  Faden trägt Frucht — das nimmt den Druck, makellos „richtig" oder hocheffizient sein zu müssen. Eine
  Beobachtung, die einlädt, nie eine Lehre, die fordert.

### Schritt 6 — Schluss-Audit, dann zeigen

- **Erst das Schluss-Audit** (aus `references/ki-tells.md`): eine ehrliche Zeile beantworten —
  *„Was verrät hier noch die Maschine?"* — und genau **die eine** Stelle nachschleifen. Nicht den ganzen
  Text neu glätten (Glätten ist der Tod der Stimme). Ein zweiter Durchgang fängt, was der erste überlas.
- **Vorher/Nachher** zeigen (oder einen klar markierten Entwurf), **nie still überschreiben.**
- Die **ehrliche Grenze**: das Modell evoziert, ist nicht. Die rohesten Brüche setzt **du** — die letzte
  Hand ist deine.

---

## Nach dem Veredeln (wenn die Note bleibt)

- **`aktualisiert:`** nur bumpen, wenn die Note dadurch **substanziell besser lesbar** wurde (bei Gedanken
  ist eine echte Stimm-Hebung das wert) — **nie** bei kosmetischem Mikro-Edit.
- **RAG re-ingest**, wenn der Text wesentlich geändert wurde (`ingest-gedankenwelten`).
- **Deploy** wie üblich (commit · push · `sync-from-cortex.sh`), falls öffentlich.

## Verwandt

- **Schwester-Skill `gedankenart`** — das Bild zur Stimme.
- **`heraklit`** vertieft den Gehalt · **`pascal`** begleitet das Schreiben (Begleiten-Modus läuft mit ihm).
- Stimm-Daten: `voices/luc.md` (Maß + Punkt + Few-Shot-Register + ehrliche Grenze).
- Streichliste: `references/ki-tells.md` (auditierbare KI-Tells + Schluss-Audit + „Seele" — geteilt mit
  `aristoteles`; geerbt vom Hermes-`humanizer`).
