---
name: aristoteles
description: "Tiefenanalyse für Note-Erstellung. Wandelt Transkripte in substantielle, analytische Gedankenwelten-Notes um — keine Zusammenfassungen, sondern echte Durchdringung. Gilt für ALLE Sektionen: Zeitgeist, Denker, Panorama. Use when creating a new Gedankenwelten note from a transcript, or when the pipeline reaches Step 5 (Note-Erstellung)."
---

# Aristoteles — Tiefenanalyse bei der Note-Erstellung

> *„Das Ganze ist mehr als die Summe seiner Teile."*
> — Aristoteles, Metaphysik

Aristoteles' Aufgabe: Ein Transkript so durchdringen, dass die Note **mehr Wert hat als das Video selbst** — durch Strukturierung, Einordnung, Kontextualisierung und kritische Reflexion.

---

## Philosophie: Was Tiefe bedeutet

Eine Note ist **keine Zusammenfassung**. Sie ist eine **Analyse**.

| Zusammenfassung (❌) | Analyse (✅) |
|---|---|
| Listet Themen auf | Erklärt Zusammenhänge |
| Referiert was gesagt wurde | Ordnet ein, warum es relevant ist |
| Bleibt an der Oberfläche | Fragt: Was folgt daraus? |
| Deckt alles ab, dünn | Wählt aus, geht tief |
| ~90 Wörter pro Abschnitt | ~150–200 Wörter pro Abschnitt |

**Leitfrage für jeden Abschnitt:** Wenn jemand nur *diesen* Abschnitt liest — versteht er die Idee, ihre Herleitung und ihre Konsequenzen?

---

## Qualitätsmetriken (Pflicht-Checks nach Erstellung)

| Metrik | Minimum | Ziel |
|---|---|---|
| Wörter im `## Inhalt` | 1.200 | 1.500–2.000 |
| Inhalts-Abschnitte (`###`) | 5 | 6–8 |
| Wörter pro Abschnitt | 120 | 150–200 |
| Direkte Zitate (mit Timestamp) | 5 | 7–10 |
| Eigenständige Einordnung/Kommentar | Jeder Abschnitt | — |

**Self-Check nach dem Schreiben:**
```bash
# Schnellcheck: Wörter im Inhalt
sed -n '/^## Inhalt/,/^## Faktencheck/p' "NOTE.md" | wc -w
# Muss ≥ 1200 sein. Falls nicht: vertiefen.
```

---

## Methode: Wie Aristoteles arbeitet

### Phase 1 — Vollständig lesen, Kernstränge identifizieren

Das Transkript **zweimal** durcharbeiten:

1. **Erster Durchgang:** Überblick. Welche 6–8 Kernthemen/Thesen sind die tragenden Säulen?
2. **Zweiter Durchgang:** Gezielt Belege, Zitate, Beispiele für jede Kernthese sammeln.

> [!important] Nicht alles abdecken!
> Ein 72-Minuten-Gespräch hat 15+ Themen. Aristoteles wählt die **6–8 substanziellsten** aus. Lieber 7 tiefe Abschnitte als 12 dünne.

### Phase 2 — Abschnitte schreiben (pro Kernthese)

Jeder `###`-Abschnitt folgt dieser inneren Struktur:

```
1. Timestamp + Kontextsatz (was wird hier verhandelt?)
2. Herleitung (wie kommt der Sprecher zu dieser These?)
3. Kernaussage in eigenen Worten (Paraphrase)
4. Direktes Zitat (1–2 Sätze, mit Timestamp-Link)
5. Einordnung/Konsequenz (was folgt daraus? warum relevant?)
```

### Phase 3 — Zitate gezielt einsetzen

**Zitate sind keine Dekoration.** Sie gehören rein wenn:
- Die Formulierung selbst aussagekräftig ist (nicht paraphrasierbar)
- Sie einen Kontrast sichtbar machen
- Sie den Tonfall des Denkers transportieren

**Immer mit Timestamp-Link. Immer mit Kommentar davor oder danach.**

```markdown
[▶ 33:28](https://www.youtube.com/watch?v=VIDEO_ID&t=2008) — Böhme über die Macht der Sprache:

> *„Wir haben einfach nur durch Worte diese Fähigkeit, da so eine Art Schalter umzulegen."*

Das ist keine Metapher — der Präfrontalkortex reguliert tatsächlich tieferliegende Schmerzregionen, wenn sprachliche Neubewertung stattfindet.
```

### Phase 4 — Eigenständige Einordnung

Jeder Abschnitt braucht mindestens **einen Satz eigene Einordnung**. Das kann sein:
- Eine Konsequenz die der Sprecher nicht zieht
- Eine Einschränkung oder Grenze der These
- Ein Querbezug zu einem anderen Denker
- Eine Alltagsanwendung oder persönliche Resonanz

Bei Denker-Notes: explizite `> [!note] Eigene Einschätzung`-Callouts (min. 2–3).
Bei Zeitgeist-Notes: eingebettete Einordnung im Fließtext (subtiler, aber vorhanden).

---

## Abschnitts-Auswahl: Was kommt rein, was fällt raus?

**Rein (Kernstränge):**
- Zentrale Thesen des Sprechers
- Überraschende oder kontraintuitive Behauptungen
- Stellen wo der Sprecher andere Positionen kritisiert
- Konkrete Belege oder Studien die genannt werden

**Raus (Beiwerk):**
- Smalltalk / Höflichkeiten
- Wiederholungen in anderen Worten
- Nebenstränge die der Sprecher selbst abbricht
- Zu vage formulierte Passagen ohne Substanz

---

## Sektions-spezifische Anpassungen

### Zeitgeist-Notes
- Fokus auf **Argumentation + Evidenz**
- Zitate dürfen kürzer sein (1 Satz)
- Einordnung eingebettet im Fließtext
- Faktencheck ist Pflicht

### Denker-Notes
- Fokus auf **Konzepte + Herleitung + Eigene Einschätzung**
- Zitate dürfen länger sein (1–3 Sätze)
- Explizite `> [!note]`-Callouts (min. 2–3)
- Lebendige Biografie im Callout
- Faktencheck nur bei empirischen Claims

---

## Phase 5 — Sokrates: Denkbewegung auslösen

Nach dem Schreiben der Analyse wird der **Sokrates-Skill** aufgerufen (Modus 1 — Note-Fragen):

```
Aristoteles Phase 1–4: Analyse fertig
     ↓
→ Sokrates (Modus 1): Inline-Fragen + ## Weiterdenken generieren
     ↓
Aristoteles Qualitäts-Gate: Prüft Sokrates-Output
```

Sokrates generiert:
- **2–4 inline** `> [!question] Weitergedacht`-Callouts an substanziellen Stellen
- **`## Weiterdenken`** mit 3–5 übergreifenden Fragen (adversarial, verbindend, Konsequenz)

Alle Details zu Fragetypen, Qualitätsregeln und Format → siehe **Sokrates-Skill** (`sokrates`).

---

## Qualitäts-Gate (nach dem Schreiben)

```
□ Inhalt ≥ 1200 Wörter?
□ Jeder Abschnitt ≥ 120 Wörter?
□ ≥ 5 direkte Zitate mit Timestamp?
□ Jeder Abschnitt hat eigene Einordnung (nicht nur Referat)?
□ Kein Abschnitt der nur "X sagte Y" ist ohne Kommentar?
□ Sokrates-Skill ausgeführt (Fragen + Weiterdenken)?
□ 2–4 inline > [!question]-Callouts an substanziellen Stellen?
□ ## Weiterdenken mit 3–5 übergreifenden Fragen vorhanden?
□ Mindestens 1 adversariale + 1 verbindende Frage?
```

Falls ein Check nicht besteht: **Gezielt ins Transkript zurückgehen**, die dünnsten Abschnitte identifizieren, Zitate und Herleitungen nachlegen.

---

## Anti-Patterns (was Aristoteles NICHT tut)

| Anti-Pattern | Warum schlecht | Stattdessen |
|---|---|---|
| 12 Abschnitte à 80 Wörter | Listig, keine Tiefe | 7 Abschnitte à 170 Wörter |
| "Böhme spricht über X" ohne Inhalt | Referiert statt analysiert | Was genau sagt sie? Warum? Was folgt? |
| Zitat ohne Kontext | Leser versteht nicht warum | Immer Einleitung + Kommentar |
| Alles abdecken wollen | Wird dünn | Auswählen, Mut zur Lücke |
| Aus dem Gedächtnis schreiben | Ungenau, vage | Immer mit Transkript vor Augen |
