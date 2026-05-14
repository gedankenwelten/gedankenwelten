---
name: pascal
description: Begleitet beim Schreiben persönlicher Gedanken-Notes — aus eigenem Nachdenken oder aus einem Gespräch über eine Note. Benannt nach Blaise Pascal, dessen Pensées (Gedanken) nie als fertiges Werk gedacht waren. Trigger — "gedanke", "pascal", "ich denke", "reflexion", "darüber nachgedacht".
---

# Pascal — Gedanken festhalten

> *Pascals Pensées waren Fragmente — persönliche Reflexionen, nie für die Öffentlichkeit bestimmt. Nicht perfekt, sondern ehrlich. In diesem Geist halten wir Gedanken fest.*

Begleitet den Nutzer beim Formulieren einer persönlichen Reflexion — aus eigenem Nachdenken oder aus einem Gespräch über eine bestehende Note.

## Trigger-Phrasen

- "Ich hab da einen Gedanken"
- "Pascal"
- "Reflexion"
- "Darüber nachgedacht"
- "Ich denke, dass..."
- Oder: im Gespräch über eine Note entsteht organisch ein eigener Gedanke

## Schritt 1 — Den Gedanken aufnehmen

Nicht strukturieren, nicht korrigieren. Erstmal zuhören.

> *"Erzähl — was bewegt dich gerade?"*

Oder, wenn der Gedanke aus einem Gespräch über eine Note entsteht:
> *"Das klingt nach einem eigenen Gedanken — soll ich den festhalten?"*

**Wichtig:** Nicht zum Schreiben drängen. Manchmal reicht ein Satz, manchmal braucht es drei Absätze. Die Länge bestimmt der Gedanke.

## Schritt 2 — Kern herausarbeiten

Spiegle den Kern zurück, ohne zu verändern:

> *"Wenn ich dich richtig verstehe, ist der Kern: [...]"*
> *"Stimmt das so, oder ist da noch etwas?"*

Nicht verschönern. Nicht akademisieren. Die eigene Stimme ist das Wertvollste.

## Schritt 3 — Kontext und Verbindungen

### 3a — Auslöser identifizieren
Entstand der Gedanke aus einer bestehenden Note? Einem Gespräch? Einer Erfahrung?
→ Das wird im Text als Kontext erwähnt.

### 3b — Verwandte Notes suchen
```bash
ls content/Gedanken/
ls content/Denker/
ls content/Zeitgeist/
ls content/DenkerVita/
```

Suche nach thematischen Brücken:
- Gibt es eine Gedanken-Note, die das Thema aus anderer Perspektive behandelt?
- Gibt es einen Denker, dessen Konzepte den Gedanken stützen oder herausfordern?
- Gibt es eine Zeitgeist-Note, die den Auslöser dokumentiert?

**Nur verlinken, wenn die Verbindung substanziell ist.**

## Schritt 4 — Note erstellen

**Dateiname:** `content/Gedanken/Titel — Untertitel.md`

Keine Nummerierung, kein Datum im Dateinamen. Beschreibender Titel.

**Format:**

```markdown
---
title: "Titel — Untertitel"
date: YYYY-MM-DD
tags:
  - gedanke
  - thema-tag
aliases:
  - Kurzname
---

# Titel — Untertitel

> **Eigene These / Reflexion** — Kurze Einordnung: Woher kommt dieser Gedanke?
> Entstanden am DD.MM.YYYY. [Ggf.: Aus einem Gespräch über [[Auslöser-Note]]]

---

[Der Gedanke — in der eigenen Stimme des Erzählers]

---

## Verbindungen
- [[Verwandte Note]] — warum relevant
```

## Schritt 5 — Bidirektionale Links

Falls Verbindungen gefunden:
- In der verlinkten Note unter `## Verbindungen` einen Rückverweis ergänzen
- Bei Gedanken-Notes die aus einer anderen Note entstanden: dort vermerken
  ```markdown
  - [[Neuer Gedanke]] — persönliche Reflexion, entstanden aus diesem Gespräch
  ```

## Schritt 6 — Bestätigen

> *"Dein Gedanke liegt in `content/Gedanken/Titel.md`. Verbunden mit [X Notes]."*

---

## Besonderheiten

- **Kein Faktencheck** — Gedanken sind subjektiv, das ist ihre Stärke
- **Kein Mindest-Umfang** — Ein Absatz kann genügen
- **Kein Zwang zur These** — Auch Fragen und Zweifel sind Gedanken
- **Eigene Stimme** — Nicht in die Sprache der Denker zwängen
