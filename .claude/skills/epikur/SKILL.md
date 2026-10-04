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
- "epikur"
- "ich hab was positives erlebt"
- oder sinngemäß: jemand möchte etwas Positives festhalten

## Schritt 1 — Gespräch führen

Nicht nach Feldern fragen. Stattdessen offen einladen:

> *"Erzähl mal — was hat dich berührt?"*

Lass den Nutzer frei erzählen. Frag bei Bedarf nach:
- *"Wann war das?"* (falls kein Datum erkennbar)
- *"Was hat dich daran besonders bewegt?"* (falls der Kern noch unklar ist)

## Schritt 2 — Verdichten

Fasse das Erzählte zu 2–5 Sätzen zusammen. Zeige den Entwurf:

> *"So könnte deine GoodNews aussehen — passt das?"*

Halte den Ton des Erzählers bei. Nicht glätten, nicht verschönern.

## Schritt 3 — Verbindungen finden

Durchsuche das bestehende Wissen nach thematischen Anknüpfungspunkten:

### 3a — Zeitgeist- und Panorama-Notes
```bash
ls content/Zeitgeist/ content/Panorama/ 2>/dev/null
```

### 3b — Denker und DenkerVita
```bash
ls content/Denker/ content/DenkerVita/ 2>/dev/null
```
Gibt es einen Denker, dessen Konzepte zur GoodNews passen?

### 3c — Gedanken
```bash
ls content/Gedanken/
```

**Nur verlinken, wenn die Verbindung substanziell ist.**

## Schritt 4 — Tag auswählen

| Tag | Für |
|---|---|
| `persönlich` | Eigenes Erlebnis |
| `welt` | Nachricht aus der Welt |
| `natur` | Umwelt, Tiere, Ökosysteme |
| `menschen` | Menschlichkeit, Hilfsbereitschaft |
| `wissenschaft` | Durchbrüche, Fortschritt |
| `politik` | Positive politische Entwicklung |

## Schritt 5 — Note erstellen

**Dateiname:** `content/GoodNews/YYYY-MM-DD-kurztitel.md`

**Format:**

```markdown
---
title: "Kurzer Titel"
date: YYYY-MM-DD
tags:
  - goodnews
  - tag
aliases:
  - Kurzname
---

# Kurzer Titel

[Die verdichteten 2–5 Sätze]

---

## Verbindungen
- [[Verwandte Note]] — warum relevant
```

## Schritt 6 — Bidirektionale Links + Bestätigen

1. In verlinkten Notes Rückverweise ergänzen
2. Kurz berichten: *"Deine GoodNews liegt in ... Verbunden mit [X Notes]."*

---

## Qualitätsfilter

- ✅ Positive Erlebnisse, gute Nachrichten, Dankbarkeit
- ❌ Klagen, Theorien, Werbung, ungeprüfte Behauptungen
- Sanft umlenken: *"Das klingt eher nach einem Gedanken — soll ich daraus eine Reflexion machen?"*
