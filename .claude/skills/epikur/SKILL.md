---
name: epikur
description: Begleitet beim Verfassen einer GoodNews-Nachricht — gesprächsweise, heilsam, mit Verbindungen zu Notes, Denkern und DenkerVita. Benannt nach Epikur — Freude durch Einfachheit, Freundschaft und den offenen Garten. Trigger — "gute nachricht", "goodnews", "epikur", "ich hab was positives".
---

# Epikur — Gute Nachrichten aufbereiten

> *Epikur öffnete seinen Garten für alle — Frauen, Sklaven, Fremde. Nicht Konsum bringt Freude, sondern Einfachheit und Freundschaft. In diesem Geist sammeln wir gute Nachrichten.*

Begleitet den Nutzer beim Schreiben einer GoodNews-Nachricht — gesprächsweise, nicht als Formular. Findet Verbindungen zum bestehenden Wissen.

## Trigger-Phrasen

- "Ich hab eine gute Nachricht"
- "goodnews"
- "gute nachricht teilen"
- "ich hab was positives erlebt"
- "good news"
- oder sinngemäß: jemand möchte etwas Positives festhalten

## Schritt 1 — Gespräch führen

Nicht nach Feldern fragen. Stattdessen offen einladen:

> *"Erzähl mal — was hat dich berührt?"*

Lass den Nutzer frei erzählen. Frag bei Bedarf nach:
- *"Wann war das?"* (falls kein Datum erkennbar)
- *"Was hat dich daran besonders bewegt?"* (falls der Kern noch unklar ist)

**Kein Zwang zur Kürze** im Gespräch — die Verdichtung kommt im nächsten Schritt.

## Schritt 2 — Verdichten

Fasse das Erzählte zu 2–5 Sätzen zusammen. Zeige den Entwurf:

> *"So könnte deine GoodNews aussehen — passt das?"*

Halte den Ton des Erzählers bei. Nicht glätten, nicht verschönern — die eigene Stimme ist das Wertvollste.

## Schritt 3 — Verbindungen finden

Durchsuche das bestehende Wissen nach thematischen Anknüpfungspunkten:

### 3a — Andere GoodNews
```bash
ls project-news/*.md | grep -v README
```
Lies die bestehenden GoodNews und prüfe: Gibt es thematische Brücken? Ähnliche Erfahrungen? Ergänzende Perspektiven?

### 3b — Zeitgeist- und Panorama-Notes
```bash
ls content/Zeitgeist/ content/Panorama/ 2>/dev/null
```
Suche nach Notes, die das gleiche Thema behandeln — z.B. eine GoodNews über Naturschutz könnte zur Good-News-Reihe oder zu Umwelt-Notes passen.

### 3c — Denker und DenkerVita
```bash
ls content/Denker/ content/DenkerVita/
```
Gibt es einen Denker, dessen Konzepte zur GoodNews passen?
- Nachbarin bringt Kuchen → Erich Fromm, *Haben oder Sein*
- Naturerlebnis → Matthieu Ricard, *Altruismus*
- Politischer Fortschritt → Hannah Arendt, *Handeln*

**Nur verlinken, wenn die Verbindung substanziell ist** — nicht erzwingen.

### 3d — Gedanken
```bash
ls content/Gedanken/
```
Persönliche Reflexionen, die zum Thema passen könnten.

## Schritt 4 — Tag auswählen

Basierend auf dem Inhalt den passenden Tag bestimmen:

| Tag | Für |
|---|---|
| `persönlich` | Eigenes Erlebnis |
| `welt` | Nachricht aus der Welt |
| `natur` | Umwelt, Tiere, Ökosysteme |
| `menschen` | Menschlichkeit, Hilfsbereitschaft |
| `wissenschaft` | Durchbrüche, Fortschritt |
| `politik` | Positive politische Entwicklung |

Mehrere Tags sind erlaubt.

## Schritt 5 — Datei erstellen

**Dateiname:** `project-news/YYYY-MM-DD-kurztitel.md`

**Format:**

```markdown
---
author: [Name aus .mnemosyne.md oder nachfragen]
date: YYYY-MM-DD
tags: [tag1, tag2]
---
# Kurzer Titel

[Die verdichteten 2–5 Sätze]

---

## Verbindungen

- [[content/Zeitgeist/Note Name|Kurztitel]] — warum relevant
- [[content/DenkerVita/Denker Name|Denker]] — konzeptuelle Brücke
- [Andere GoodNews](../project-news/YYYY-MM-DD-titel.md) — thematische Nähe
```

**Verbindungen-Abschnitt nur einfügen, wenn Verbindungen gefunden wurden.** Keine leeren Abschnitte.

## Schritt 6 — Bestätigen

Zeige die fertige GoodNews und frage:

> *"Sieht gut aus? Dann lege ich sie an."*

Bei Änderungswünschen: anpassen und nochmal zeigen.

## Schritt 7 — Ablegen und berichten

1. Datei in `project-news/` erstellen
2. Falls Verbindungen zu bestehenden Notes gefunden:
   - In der verlinkten Note unter `## Verbindungen` einen Rückverweis ergänzen (bidirektional)
3. Kurz berichten:
   > *"Deine GoodNews liegt in `project-news/YYYY-MM-DD-titel.md`. Verbunden mit [X Notes]. Per `git add -A && git commit && git push` kannst du sie teilen."*

---

## Qualitätsfilter (aus project-news/README.md)

### ✅ Ja
- Positive Erlebnisse, gute Nachrichten, Dankbarkeit
- Im Vipassana-Sinne heilsam

### ❌ Nein
- Klagen, Theorien, Werbung, ungeprüfte Behauptungen

### Sanftes Umlenken
Wenn der Inhalt nicht als GoodNews passt:
> *"Das klingt eher nach einem Gedanken als nach einer GoodNews — soll ich daraus eine Reflexion in `content/Gedanken/` machen?"*

Im Zweifelsfall: Wenn es jemandem helfen könnte, es zu lesen — dann darf es stehen.
