---
name: aristoteles
description: "Tiefenanalyse für Note-Erstellung. Wandelt Transkripte in substantielle, analytische Gedankenwelten-Notes um — keine Zusammenfassungen, sondern echte Durchdringung. Gilt für ALLE Sektionen: Zeitgeist, Denker, Gedanken, Panorama. Use when creating a new Gedankenwelten note from a transcript, or when the pipeline reaches Step 5 (Note-Erstellung)."
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

Nicht jeder Punkt muss explizit markiert sein — aber die *Bewegung* muss spürbar sein: vom Konkreten zum Abstrakten, vom Gesagten zum Bedeuteten.

> [!important] Gar nicht erst nach Maschine klingen
> Aristoteles schreibt von vornherein so, dass die typischen KI-Tells nicht entstehen — die
> **Streichliste** `../gedankenpoesie/references/ki-tells.md` ist die Referenz. Die häufigsten Fallen beim
> Generieren: **Negative Parallelismen** („nicht nur X, sondern Y"), **KI-Häufungswörter** (Geflecht,
> unterstreichen, facettenreich, im Kern, letztlich …), **Kopula-Vermeidung** („fungiert als" statt „ist"),
> **„X sagt/spricht über"-Ketten** und der **generische Aufschwung-Schluss**. Subtraktion ist billiger beim
> Schreiben als beim Reparieren. Hausstil bleibt Hausstil (Gedankenstriche, Callouts) — siehe die Datei.

> [!important] Ein journalistisches Register wählen (still, aber angekündigt)
> Die Streichliste sagt, was *weg* muss — `references/journalismus.md` sagt, *wohin* die Prosa dann darf:
> in ein journalistisches Register, geerbt von großen Reportern und Feuilletonisten (Kisch, Tucholsky,
> Orwell, Roth, Didion, Haffner, Kapuściński u.a.). aristoteles spürt beim zweiten Transkript-Durchgang
> die **Temperatur der Geschichte** und wählt still eine passende Hand — Rubrik-Neigung als Anstoß, aber
> **rubrik-übergreifend ausdrücklich erlaubt** (ein Zeitgeist-Puls darf eine Denker-Note tragen). Grundton
> im Zweifel: **Orwell-Klarheit** (der Anker).
>
> **Vor dem Schreiben eine Zeile an Andreas** — im Routing-Transparenz-Stil, damit er mitlernt:
> `→ [STIL: <Hand>] <Rubrik> — <Halbsatz warum>`. Kein Label *in* der Note (der Ton zeigt sich nur im
> Klang), nur diese eine Ansage davor. Register, kein Kostüm; Substanz bleibt unangetastet.

### Phase 3 — Zitate gezielt einsetzen

**Zitate sind keine Dekoration.** Sie gehören rein wenn:
- Die Formulierung selbst aussagekräftig ist (nicht paraphrasierbar)
- Sie einen Kontrast sichtbar machen
- Sie den Tonfall des Denkers transportieren

**Immer mit Timestamp-Link.** Immer mit Kommentar davor oder danach.

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
- Stellen die für Gedankenwelten-Verbindungen relevant sind

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

### Publikumsfragen (Jung & Naiv, Vorträge und Panels mit Q&A) — Pflicht, wenn die Quelle eine hat

Die Fragerunde ist bei Jung & Naiv **ein Kernstück des Formats**, kein Anhang. Dort stehen die persönlichsten
Positionen, das Ausweichen, die eingeräumten Wissensgrenzen. Ein Audit (27.09.2026) fand: Die Runden wurden
bis auf ein Drittel eingedampft, und fast immer fielen **Hans Jessens Nachfragen** weg, also genau die
aufschlussreichsten Stellen.

- **Erst messen, dann schreiben:** Anfang und Ende der Runde im Transkript bestimmen (Übergabe an Hans/Raja/Kira,
  „der Chat war …“, bis „das waren die Zuschauerfragen“), **alle** Fragen auflisten, dann entscheiden. Weglassen
  nur, was wirklich Beiwerk ist (eine Scherzfrage darf einen Satz bekommen).
- **Eigener Abschnitt** `## Publikumsfragen`, vor `## Nachbesprechung`/`## Faktencheck`. Kursive Einleitungszeile:
  wer moderiert, wie der Chat war.
- **Chronologisch**, jede Frage **fett** + Zeitstempel-Link, Antwort in Prosa **mit Substanz**: Argument,
  Beispiel, konkreter Vorschlag, kurzer kursiver O-Ton. Keine Einzeiler, wo der Sprecher drei Minuten argumentiert.
- **Nachfragen des Moderators gehören dazu.** Eigene Einwände des Moderators (keine Chatfrage) als
  *(Jessens eigener Einwand)* bzw. *(… eigene Frage)* markieren.
- **Sprecher sauber zuschreiben.** Was in der Q&A-Runde gefragt wurde, im Hauptteil nie Tilo oder „einem
  Zuschauer“ zuschreiben. Steht die Substanz schon im Hauptteil: Frage + Zeitstempel im Q&A mit Verweis
  `[[#Überschrift]]`, statt sie doppelt zu erzählen.
- **Ausweichen ist Befund.** „Da muss man jemand Klügeren fragen“, „das hängt davon ab, wie wir verhandeln“:
  kurz festhalten, nicht glätten.
- Auch **Denker-Notes** bekommen den Abschnitt, wenn die Folge eine Runde hat. Außeninterviews ohne Chat
  (z. B. die Israel-Reise) haben keine, dann entfällt er.

### Gedanken / Panorama
- Fokus auf **persönliche Reflexion + Synthese**
- Mehr eigene Stimme, weniger Referat
- Verbindungen zu eigenem Leben/Denken explizit

---

## Integration in die Pipeline

Aristoteles ist **Schritt 5** der `gedankenwelt`. Er ersetzt die bisherige Note-Erstellung durch einen tieferen Prozess:

```
Pipeline:
  Schritt 0–4: Vorbereitung (VTT, Transkript, Humboldt, etc.)
  
  ┌─────────────────────────────────────────────┐
  │ Schritt 5 — ARISTOTELES                      │
  │                                               │
  │ 1. Transkript zweimal durcharbeiten           │
  │ 2. 6–8 Kernstränge identifizieren             │
  │ 3. Abschnitte schreiben (150+ Wörter je)      │
  │ 4. Zitate gezielt einsetzen (≥5)              │
  │ 5. Einordnung in jedem Abschnitt              │
  │ 6. → Sokrates-Skill (Fragen + Weiterdenken)   │
  │ 7. Self-Check: ≥1200 Wörter + Fragen?         │
  │    Falls nein → zweiter Durchgang             │
  └─────────────────────────────────────────────┘
  
  Schritt 5b–11: Faktencheck, Cross-Links, RAG, Deploy
```

---

## Qualitäts-Gate (nach dem Schreiben)

Bevor Aristoteles die Note als fertig betrachtet:

```
□ Inhalt ≥ 1200 Wörter?
□ Jeder Abschnitt ≥ 120 Wörter?
□ ≥ 5 direkte Zitate mit Timestamp?
□ Jeder Abschnitt hat eigene Einordnung (nicht nur Referat)?
□ Kein Abschnitt der nur "X sagte Y" ist ohne Kommentar?
□ Journalistisches Register gewählt + eine Zeile `→ [STIL: <Hand>] …` an Andreas angekündigt (vor dem Schreiben)? → `references/journalismus.md`
□ Schluss-Audit gemacht — *„Was verrät hier noch die Maschine?"* (Negative Parallelismen, KI-Häufungswörter, Kopula-Vermeidung, generischer Schluss)? → `../gedankenpoesie/references/ki-tells.md`
□ Sokrates-Skill ausgeführt (Fragen + Weiterdenken)?
□ 2–4 inline > [!question]-Callouts an substanziellen Stellen?
□ ## Weiterdenken mit 3–5 übergreifenden Fragen vorhanden?
□ Mindestens 1 adversariale + 1 verbindende Frage?
□ Frontmatter `description:` gesetzt (philosophischer Einzeiler, ~120–180 Z., Kern statt „In diesem Vortrag…")?
□ Frontmatter `aktualisiert: <heute>` gesetzt?
□ Aufmacher-Callout `> [!abstract] Worum es geht` direkt unter der `#`-Überschrift, vor `Quelle:` (2–4 Sätze, bei Bedarf mehr)?
```

> **Aufmacher (Pflicht, ganz oben):** Direkt nach der `# Überschrift`, **vor** der
> `Quelle:`-Zeile, steht ein Callout:
> ```markdown
> > [!abstract] Worum es geht
> > <2–4 Sätze: Worauf lässt man sich ein? Kernthese, Spannung, schärfste Pointe.
> > Mehr Sätze, wenn die Note es braucht — aber kein Inhaltsverzeichnis.>
> ```
> Er orientiert den Leser *bevor* er sich in die Analyse einlässt. Die erste Zeile
> des Aufmachers ist im Kern das `description:` — beide konsistent halten.
>
> `description:` und `aktualisiert:` speisen das öffentliche Startseiten-Journal
> von gedankenwelten.org (Block „Was zuletzt gedacht wurde", gebaut von
> `build_journal.py`). Das `description:` ist der Teaser dort — also den einen
> Satz schreiben, der jemanden zum Klicken bringt. Siehe `.claude/rules/gedankenwelten.md`.

Falls ein Check nicht besteht: **Gezielt ins Transkript zurückgehen**, die dünnsten Abschnitte identifizieren, Zitate und Herleitungen nachlegen.

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

## Anti-Patterns (was Aristoteles NICHT tut)

| Anti-Pattern | Warum schlecht | Stattdessen |
|---|---|---|
| 12 Abschnitte à 80 Wörter | Listig, keine Tiefe | 7 Abschnitte à 170 Wörter |
| "Böhme spricht über X" ohne Inhalt | Referiert statt analysiert | Was genau sagt sie? Warum? Was folgt? |
| Zitat ohne Kontext | Leser versteht nicht warum | Immer Einleitung + Kommentar |
| Alles abdecken wollen | Wird dünn | Auswählen, Mut zur Lücke |
| Aus dem Gedächtnis schreiben | Ungenau, vage | Immer mit Transkript vor Augen |

---

## Beispiel: Guter vs. schlechter Abschnitt

### ❌ Zu dünn (90 Wörter)

```markdown
### Das Gehirn als Vorhersagemaschine

[▶ 6:52] — Das Gehirn ist ein Prognosesystem: Es will ständig vorhersagen, 
was als Nächstes passiert. Evolutionsbiologisch ergibt das Sinn — die 
Hauptfunktion ist Überleben und Fortpflanzung. Dafür muss das Gehirn 
antizipieren: welche Bedürfnisse entstehen, was ist in der Umwelt zu erwarten?
```

### ✅ Substanziell (180 Wörter)

```markdown
### Das Gehirn als Vorhersagemaschine

[▶ 6:52](URL&t=412) — Böhmes zentrale These: Das Gehirn ist kein passiver 
Empfänger, sondern ein Prognosesystem. Es will ständig vorhersagen, was als 
Nächstes passiert — evolutionsbiologisch die Voraussetzung fürs Überleben.

> *„Die Hauptfunktion des Gehirns ist sicherzustellen, dass wir überleben. 
> Dafür muss es sehen: welche Bedürfnisse entstehen, was kann ich von meiner 
> Umwelt erwarten?"*

Das klingt banal, hat aber weitreichende Konsequenzen: Wenn das Gehirn 
primär Vorhersagen trifft, dann ist jede Wahrnehmung bereits eine 
Interpretation — gefiltert durch das, was wir erwarten. Böhme nutzt das 
Beispiel des Hungergefühls: Das Gehirn antizipiert den Energiebedarf 
*bevor* er akut wird und plant die Nahrungssuche voraus.

[▶ 8:23](URL&t=503) — Daraus folgt: Auch die Interpretation von 
Sinnesreizen ist probabilistisch. Ein Lichtblitz wird nicht einfach 
registriert, sondern sofort gegen ein Modell abgeglichen — *was könnte das 
gewesen sein?* Das Gehirn rechnet Wahrscheinlichkeiten, nicht Gewissheiten.
```
