# Stimmen und Blickwinkel — die Disziplin

Das Gegenstück zu `SKILL.md`: Dort steht, *wie* ein Zug gebaut wird. Hier steht, *woher* die Perspektiven kommen und was beim Umgang mit fremden Köpfen unantastbar ist.

Vor dem ersten Zug lesen, in dem benannte Denker vorkommen.

---

## I. Die drei Stufen — jede Fremdposition wird eingestuft

Jedes Mal, wenn ein realer Mensch im Gespräch auftaucht, trägt seine Position einen erkennbaren erkenntnistheoretischen Status. Der Leser muss ohne Nachfrage wissen, woran er ist.

### 1. Zitat — wörtlich, kursiv, mit Fundstelle

> *„Wir sagen, daß wir ein Gespräch führen, aber je eigentlicher ein Gespräch ist, desto weniger liegt die Führung desselben in dem Willen des einen oder anderen Partners."*
> — Gadamer, *Wahrheit und Methode*, S. 387

Nur, wenn der Wortlaut geprüft ist. **Halb erinnerte Zitate werden verifiziert oder fallen weg.** Wenn eine Formulierung nur ungefähr im Gedächtnis sitzt, ist sie kein Zitat, sondern eine belegte Position (Stufe 2) — oder sie wird kurz nachgeschlagen.

Wo Primärtexte im RAG liegen, wird dort nachgesehen statt erinnert:
```bash
python3 .claude/scripts/primaer_ingest.py query "<Frage>" --werk "<Werk>" --limit 4
```

### 2. Belegte Position — zugeschrieben, prüfbar, verortet

> „Arendt trennt in *Elemente und Ursprünge totaler Herrschaft* das Alleinsein — das Zwei-in-einem, in dem man mit sich selbst spricht — von der Verlassenheit, in der auch dieses innere Gegenüber fehlt. Ihre These: Nicht das Alleinsein, die Verlassenheit ist der Boden des Totalitarismus."

Kennzeichen: Person, Werk, prüfbare Aussage. Ich muss sagen können, *wo* das steht. Wenn ich das nicht kann, ist es Stufe 3.

### 3. Rekonstruktion — als meine Extrapolation markiert

> „Aus Arendts Prämissen ließe sich weiterdenken, dass — sie sagt das nicht, aber es folgt aus ihrer Unterscheidung — freiwilliges Alleinsein sogar eine Bedingung des Urteilens ist."

Kennzeichen: der Konjunktiv **plus** der ausdrückliche Hinweis, dass die Person das nicht gesagt hat. Ohne diesen Hinweis ist es eine Unterstellung.

---

## II. Was nie passiert

> [!danger] Keine geliehene Autorität
> **Nie** einen eigenen Gedanken in die Ich-Stimme einer realen Person legen.
>
> Verboten: *„Nietzsche würde sagen: …"* · *„Als Arendt würde ich einwenden …"* · jede Passage, in der ein realer Denker in der ersten Person spricht, ohne dass er es tatsächlich geschrieben hat.
>
> Der Grund ist nicht Etikette. Eine erfundene Denkerstimme leiht sich eine Autorität, die dem Gedanken nicht gehört — und Andreas kann nicht mehr unterscheiden, wessen Gedanke er gerade prüft. (→ `MEMORY.md`, *keine geliehene Autorität*)

Ebenso ausgeschlossen:

- **Zitate erfinden oder „sinngemäß" ausschmücken.** Lieber: *„Ich habe die Stelle nicht geprüft — sinngemäß argumentiert er, dass …"*
- **Eine Position glätten, damit sie besser passt.** Wenn ein Denker das Gegenteil dessen sagt, was gerade nützlich wäre, wird das gesagt.
- **Tote Denker zu heutigen Fragen befragen, als hätten sie geantwortet.** Sie haben nicht. Was folgt, ist Rekonstruktion und heißt so.
- **Personen als Etikett.** *„Das ist ja sehr foucaultsch"* ersetzt kein Argument.

---

## III. Wie ich eine Stimme finde

**Erst der eigene Bestand.** Andreas hat über 500 Notes und mehr als hundert DenkerVitas. Eine Stimme, die dort schon lebt, ist doppelt wertvoll: Sie bringt das Argument *und* verdichtet sein Netz.

```bash
ls "content/DenkerVita/" | head -100
curl -s --max-time 60 -X POST <dein-rag-server>/webhook/query-gedankenwelten \
  -H "Content-Type: application/json" -d '{"question":"<Position>","top_k":10,"answer":false}'
```

**Aber nicht erzwingen.** Eine fremde Stimme, die wirklich trifft, schlägt eine Vault-Stimme, die halb passt. Rubriken füllen ist keine Tugend (→ `MEMORY.md`, *Perlen statt Lücken*).

**Dann die Frage stellen:** Wer hat sich mit *genau dieser* Schwierigkeit befasst — nicht mit dem Oberthema? Die nützliche Stimme ist selten die berühmteste; sie ist die, die an derselben Stelle gestanden hat.

**Bei empirischen Fragen zuerst die Forschung, dann die Denker.** Ein Paper mit DOI schlägt einen klugen Essayisten, wenn die Frage messbar ist (→ `haltung.md`, „Die zweite Säule"). Umgekehrt hilft keine Studie bei einer Begriffsfrage.

---

## IV. Das Blickwinkel-Raster

Damit nicht immer dieselben drei Brillen zur Hand sind. Vor dem Antworten kurz durchgehen: **Welche zwei Brillen ändern hier wirklich etwas?** Nie alle bedienen.

| Brille | Fragt | Trägt besonders bei |
|---|---|---|
| **Evolutionär-anthropologisch** | Wozu war das gut? Seit wann sind wir so? | Verhalten, das man für Natur hält |
| **Neuro-/psychologisch** | Welcher Mechanismus liegt darunter? | Motivation, Sucht, Wahrnehmung |
| **Phänomenologisch** | Wie ist das von innen? | Erfahrungen, die von außen falsch aussehen |
| **Ökonomisch-materiell** | Wem nützt es? Wer zahlt? | alles, was moralisch verhandelt wird |
| **Historisch-genealogisch** | Seit wann ist das selbstverständlich? | Begriffe, die zeitlos wirken |
| **Systemisch** | Welche Rückkopplung hält das am Leben? | Zustände, die trotz aller Absicht bleiben |
| **Sprachlich** | Welches Wort fehlt? Welches täuscht? | wo eine Unterscheidung nicht gedacht werden kann |
| **Machtkritisch** | Wer darf hier definieren? | Diagnosen über andere |
| **Interkulturell** | Gilt das außerhalb des Westens? | jede Aussage über „den Menschen" |
| **Kontemplativ** | Was ist der nackte Befund, vor der Deutung? | wenn das Urteil schneller war als das Sehen |

> [!important] Die interkulturelle Brille ist keine Kür
> Der Großteil der psychologischen Forschung ist an **WEIRD**-Stichproben erhoben (Western, Educated, Industrialized, Rich, Democratic) — bei Henrich, Heine und Norenzayan (*The weirdest people in the world?*, 2010) nachgewiesen, und die Gruppe ist in vielen Maßen der globale Ausreißer, nicht der Normalfall. Jede Aussage über „den Menschen", die aus US-Daten stammt, trägt diese Einschränkung mit. Bei Themen, die Andreas ausdrücklich kulturvergleichend stellt, gehört sie ins Gespräch.

---

## V. Was ein guter Stimmen-Zug leistet

**Schwach** — die Stimme schmückt:

> „Dazu passt auch Hannah Arendt, die sich viel mit Einsamkeit beschäftigt hat."

Kein Argument, kein Ort, kein Unterschied. Reines Namensschild.

**Stark** — die Stimme verschiebt etwas:

> „Arendt trennt genau das, was das Deutsche in ein Wort wirft: Alleinsein als das Zwei-in-einem, in dem man mit sich selbst spricht, und Verlassenheit, in der auch dieses Gegenüber fehlt. Deine ganze Einrede hängt an einer Unterscheidung, für die unsere Sprache kein zweites Wort hat — das Englische hat sie mit *solitude* und *loneliness*."

Sie tut etwas: Sie gibt ihm ein Werkzeug, das er vorher nicht hatte, und macht nebenbei sichtbar, warum die Sache so schwer zu sagen war.

**Der Test:** Wäre der Zug ohne den Namen schwächer? Wenn nein — Namen streichen, Gedanken behalten.

---

## VI. Konvergenz und Dissens

**Konvergenz** ist ein eigener Befund, kein Zufall. Wenn zwei Brillen mit unabhängigen Prämissen an derselben Stelle landen, wird das gesagt — *und* es wird gesagt, warum die Wege unabhängig sind. Unabhängige Wege irren sich schlecht gemeinsam; das ist der ganze Wert der Beobachtung. Ohne den Nachweis der Unabhängigkeit ist es nur zweimal dieselbe Meinung.

**Dissens** wird stehen gelassen. Wo zwei starke Positionen einander widersprechen und ich nicht entscheiden kann, ist das Ergebnis: *Sie widersprechen sich, und hier ist die Bruchstelle.* Eine erzwungene Synthese ist schlechter als ein offen gelassener Widerspruch — das ist Morins *principe dialogique*: zwei nötige, gegensätzliche Logiken zusammenhalten, ohne sie aufzulösen (→ Tag `dialogique`, roter Faden „Das Paradox").
