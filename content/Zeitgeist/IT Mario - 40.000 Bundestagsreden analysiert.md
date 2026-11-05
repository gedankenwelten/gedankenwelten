---
title: "IT Mario — 40.000 Bundestagsreden analysiert: Welche Partei ist wirklich gefährlich?"
description: "Eine KI liest über 40.000 Bundestagsreden, ohne zu wissen, von welcher Partei sie stammen. Beim Vorwurf liegt das BSW knapp vor der AfD, beim Populismus führt die AfD deutlich."
aktualisiert: 2026-05-24
raetsel: "Das Auge kennt keine Namen. Es zählt nur, wie spitz ein Satz ist."
date: 21.05.2026
tags:
  - zeitgeist
  - demokratie
  - ki
  - deutschland
  - afd
  - technologie
  - year-2026
aliases:
  - IT Mario Bundestag Analyse
---

# IT Mario — 40.000 Bundestagsreden analysiert

![[assets/IT-Mario-40000-Bundestagsreden-banner.jpg|Aquarell: Viele kleine Strichfiguren sitzen in einem halbrunden Plenarsaal, darüber schweben bunte Sprechblasen und rote Zacken, von einem großen Auge oben laufen Linien zu ihnen.|1200]]

<details><summary>🎨</summary>

**Paul Klee** (angelehnt) — ein Halbrund aus kleinen Strichfiguren, über ihnen Sprechblasen, manche rund und ruhig, manche gezackt und rot; darüber ein großes Auge aus feinen Kreisen, von dem dünne Messlinien zu den Sätzen hinablaufen. Klee, weil seine Bilder zwischen Zeichen und Rechnung spielen, ernst und ein wenig ironisch, und genau das ist eine Maschine, die Parlamentsreden auf Zacken abtastet, ohne zu wissen, wer spricht.

*Prompt:* A painting in the style of Paul Klee, wide panoramic banner, 12:5 aspect ratio. Delicate watercolor and oil transfer on warm parchment, playful geometric signs, soft ochre, rose, slate blue and green. A semicircular parliament hemicycle seen slightly from above, built from rows of tiny abstract stick figures and little rectangles like seats; from some figures rise small colored speech shapes, some round and calm, some jagged and red. Above the hemicycle a large calm circular eye made of fine concentric lines, from which thin straight measuring lines descend to the speech shapes, like a gentle instrument weighing them. Whimsical, thoughtful, slightly ironic mood. No text, no letters, no numbers, no flags, no party logos.

</details>

> [!abstract] Worum es geht
> Eine KI liest über 40.000 Bundestagsreden, ohne zu wissen, von welcher Partei sie stammen. Beim Vorwurf liegt das
> BSW knapp vor der AfD, beim Populismus führt die AfD deutlich, beim Faktencheck schneidet sie am schlechtesten ab.
> Der Datenanalyst IT Mario legt Prompts und Bewertungen offen und zerlegt eine Weidel-Rede in drei Merkmale des
> Populismus. Wir halten seine Befunde neben die Forschung (PopBERT kommt zum selben Ergebnis) und fragen, was ein
> Sprachmodell als Richter über politische Sprache leisten kann und was nicht.

Quelle: [40.000 Reden analysiert: Welche Partei ist WIRKLICH gefährlich?](https://www.youtube.com/watch?v=1LH7PZAPq-Y) (21.05.2026)

> [!info] Wer spricht?
> **IT Mario** — Datenanalyst und Data-Science-Content-Creator, der komplexe Analysen für ein breites Publikum zugänglich macht. Sein Kanal fokussiert auf datengetriebene Recherche: YouTube-Werbemessung, Kommentaranalyse, KI-Erklärvideos — und jetzt Bundestags-Rhetorik.
>
> Keine politikwissenschaftliche Ausbildung, aber methodische Transparenz als Stärke: alle Bewertungen öffentlich in Google Spreadsheets, Datenquelle offen auf Zenodo. Er sagt selbst: *„Ich bin auch nur irgendein YouTuber, der euch irgendwas erzählt. Ihr müsst selber nachdenken."*
>
> Einordnung: Techniker-Perspektive auf politische Sprache — keine Parteilinie, keine akademische Agenda. Wert liegt in der Transparenz und Reproduzierbarkeit, Grenze in der fehlenden politikwissenschaftlichen Validierung.
>
> → [[DenkerVita/IT Mario|DenkerVita]]

---

## Die Datenbasis — 80.000 Reden, offen und nachvollziehbar

[▶ 0:45](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=45)

Der methodische Ausgangspunkt ist solide: IT Mario nutzt den Datensatz aus dem [Zenodo-Archiv von Sean Fobbe](https://zenodo.org/communities/sean-fobbe-data/), der alle Bundestags-Stenogramme als maschinenlesbare Daten aufbereitet hat. Das Ergebnis: knapp 80.000 Reden ab 2013, inklusive Metadaten (Partei, Datum, Redner, Kommentare aus dem Plenum). Für die Scoring-Analyse werden die ca. 45.000 Reden ab 2020 verwendet.

Dieser Datensatz ist öffentlich, frei verfügbar, und institutionell zuverlässig — das Bundestag-Protokoll ist kein Meinungsdokument, sondern ein amtliches Schriftstück. Damit hat IT Mario eine bessere Primärquelle als viele Medienberichte über parlamentarische Rhetorik.

Bevor er in die KI-Analyse geht, wirft er einen kurzen Blick auf die Metadaten: den Anteil der Redner mit akademischem Titel (CDU/CSU führt mit 20,6 %, AfD liegt mit 15 % im Mittelfeld, Linke bildet mit 8,8 % das Schlusslicht), Wortschatz (Type-Token-Ratio: AfD überraschend an der Spitze, CDU/CSU vorletzter Platz), und Heiterkeitseinträge im Protokoll als Näherungswert für Lacher im Plenum (AfD führt). Diese Metadaten-Analyse ist methodisch harmlos — sie beschreibt, wertet noch nicht.

> [!note] Eigene Einschätzung
> Der Wortschatz-Befund ist kontraintuitiv und verdient mehr Aufmerksamkeit als IT Mario ihm gibt: Dass die AfD nach dieser Schätzung den größten Wortschatz im Plenum hat, widerspricht dem Klischee der primitiven Demagogen. Die Type-Token-Ratio ist allerdings ein grobes Maß, das stark von der Länge der Texte abhängt. Und Wortschatzreichtum sagt nichts über Wahrheitsgehalt oder argumentative Redlichkeit — Komplexität kann auch strategisch zur Verschleierung eingesetzt werden.

---

## Methodik: KI als Richter über politische Sprache

[▶ 3:01](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=181)

Drei Metriken, ein Modell, null Partei-Wissen. IT Marios Design ist methodisch durchdacht:

**Vorwurfs-Score (1–10):** Wie viel Aggressivität und Schuldzuweisung steckt in der Rede? 1 = lösungsorientiert, kooperativ. 10 = harte Angriffe, Ad-hominem-Kritik, massive Schuldzuweisung.

**Populismus-Score (1–10):** 1 = Komplexität und Pluralismus werden anerkannt. 10 = populistisches Volk-gegen-Elite-Narrativ.

**Sachlichkeits-Score (1–10):** 1 = hochgradig emotionalisiert. 10 = extrem technokratisch und zahlenbasiert.

Das Modell: GPT-4o-mini für die Scoring-Aufgabe, GPT-4o für den Faktencheck. Der entscheidende methodische Schachzug: das Modell sieht nur den Redetext — es weiß nicht, von wem die Rede stammt oder welcher Partei. IT Mario selbst formuliert es treffend:

> *„Das hat auch zum Vorteil, dass nicht meine voreingenommene politische Meinung mit einfließt."* [▶ 3:01](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=181)

Alle Rohdaten liegen öffentlich als Google Spreadsheet vor — jeder kann Stichproben manuell nachprüfen.

> [!question] Weitergedacht
> Das Modell sieht keine Partei — aber es wurde mit Daten trainiert, die Parteien kennen. *Spiegelt sich in GPT-4o-minis Sprachverständnis bereits eine politische Einordnung wider, die die Scores systematisch verschiebt?* IT Mario benennt diesen Bias, kann ihn aber nicht quantifizieren.

---

## Vorwurfs-Score: Wer wirft am meisten vor?

[▶ 4:32](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=272)

Das erste Ergebnis überrascht: BSW führt den Vorwurfs-Score mit 7,07 Punkten an — knapp vor der AfD mit 7,06. Die vorwurfsloseste Partei ist die SPD. IT Mario kommentiert das nüchtern:

> *„Die AfD wirft also so wie BSW viel vor, aber sie sind ja auch die Oppositionspartei und ihre Aufgabe ist es ja auch auf die Fehler der Regierung hinzuweisen."* [▶ 6:05](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=365)

Das ist ein wichtiger analytischer Schritt: Vorwürfe sind in der parlamentarischen Opposition strukturell erwartet. Dass das BSW, die *neue* Oppositionspartei, knapp vorne liegt, ist eigentlich die Nachricht. Sahra Wagenknechts persönlich vorgetragene Rede erhält 10 von 10 Punkten:

> *„Was heute hier verhandelt wird, ist das wahnwitzigste Aufrüstungspaket und der größte Wahlbetrug in der Geschichte der Bundesrepublik Deutschland."* [▶ 5:18](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=318)

Das ist parlamentarische Rhetorik, die bewusst die Grenzen des Faktenbaren strapaziert. Der Vorwurfs-Score allein reicht nicht, um zwischen legitimer Opposition und systematischem Populismus zu unterscheiden — das übernimmt der nächste Score.

> [!note] Eigene Einschätzung
> Dass BSW und AfD im Vorwurfs-Score so nah beieinander liegen, ist eine der interessantesten Erkenntnisse des Videos — und wird von IT Mario fast beiläufig behandelt. Das Muster „charismatische Frontperson + maximale moralische Entrüstung" verbindet beide Parteien quer durch das politische Spektrum. Was sie trennt, liegt woanders: in der politikwissenschaftlichen Unterscheidung zwischen linkem und rechtem Populismus.

---

## Populismus-Score: Die Anatomie einer Mobilisierungsrede

[▶ 6:52](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=412)

Beim Populismus-Score führt die AfD deutlich. IT Mario macht hier das Wichtigste des ganzen Videos: Er analysiert *warum* — und das ist erstklassig. Er nimmt Alice Weidels Rede (10/10 Punkte) und zerlegt sie in drei Merkmale populistischer Rhetorik:

**1. Antielitarismus** — Die Regierung wird nicht nur kritisiert, sondern moralisch delegitimiert:

> *„Dieser Haushaltsentwurf ist ein historisches Dokument, ein Dokument der unverantwortlichen Sorglosigkeit inmitten einer Krise, die unsere Freiheit [...] und das Fundament unseres Wohlstandes [...] zutiefst erschüttert."* [▶ 8:22](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=502)

Kein Finanzplan, sondern ein Angriff auf die Freiheit. Die rhetorische Inflation ist Methode.

**2. Antipluralismus** — Gesellschaft wird in zwei Blöcke gespalten: Elite vs. echtes Volk:

> *„Die Folgen ihrer verantwortungslosen, grenzenlosen Asylpolitik tragen die Bürger in Form von gestiegener Unsicherheit und Kriminalität."* [▶ 9:09](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=549)

Auf der einen Seite die böse Elite, auf der anderen das leidende Volk — nur die AfD spricht für letzteres.

**3. Komplexitätsreduktion** — Komplizierte Sachverhalte werden auf ein einziges Bild heruntergebrochen:

> *„Deutschland benehme sich wie ein gefühlsgeleiteter Hippistaat."* [▶ 10:40](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=640)

Staatsrecht, internationale Verträge, Fluchtursachen — alles kollabiert zu einem Klischee. Das Ziel ist nicht Debatte, sondern Mobilisierung. IT Mario zitiert hier Höcke selbst als unfreiwilligen Kommentar:

> *„Wer die Begriffe prägt, der prägt die Sprache. Wer die Sprache prägt, der prägt das Denken. Wer das Denken prägt, prägt den politischen Diskurs."* [▶ 11:25](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=685)

> [!note] Eigene Einschätzung
> Die ersten beiden Merkmale entsprechen dem Kern der verbreiteten Definition von Cas Mudde: eine moralische Gegenüberstellung von reinem Volk und korrupter Elite, mit Antipluralismus als Folge (die PopBERT-Studie stützt sich ausdrücklich auf Mudde). Die Komplexitätsreduktion gehört dort nicht zur Definition, sie ist eher ein Stilmerkmal. IT Mario spricht selbst von den „typischen drei Merkmalen“, ohne eine Quelle zu nennen. Gerade die Grenzbegriffe bleiben dadurch unscharf.

> [!question] Weitergedacht
> Gilt Komplexitätsreduktion als populistisches Merkmal — oder als *erforderliche* Vereinfachung in einer Demokratie, die auch Nicht-Akademiker erreichen muss? *Ab wann wird aus notwendiger Klarheit schädliche Vereinfachung?*

---

## Wer lügt wie oft? Der Faktencheck der KI

[▶ 12:56](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=776)

Der methodisch anspruchsvollste Teil: Aus je 200 zufällig ausgewählten Reden pro Partei extrahiert GPT-4o drei bis fünf falsifizierbare Tatsachenbehauptungen und bewertet sie als *richtig*, *falsch* oder *Kontext fehlt*. Das Ergebnis:

- **SPD** führt mit ca. 70 % korrekten Aussagen
- **AfD** bildet das Schlusslicht — nicht nur relativ die wenigsten korrekten, sondern auch absolut die meisten eindeutig falschen Aussagen

Zwei Beispiele, die IT Mario ausführt:

*Beatrix von Storch, 2020*: Behauptung, 7 Millionen Arbeitnehmer seien in Kurzarbeit. Tatsächlich lag der Peak bei 6 Millionen (Quelle: Bundesagentur für Arbeit). Die Zahl ist falsch — aber die Zahl macht das Argument nicht besser oder schlechter, sie skaliert es nur leicht über.

*Bernd Schattner* (AfD): *„Deutschland hat die höchste Steuerquote der Welt. 42 % des Einkommens gehen im Durchschnitt an den Staat.“* IT Mario hält beides für falsch: Frankreich und skandinavische Länder hätten eine höhere Steuerquote, und die 42 % bezögen sich auf den Spitzensteuersatz. Die erste Hälfte trifft zu. Bei der zweiten ist seine Erklärung nur eine mögliche Lesart, denn je nach Maß liegt die durchschnittliche Abgabenlast auf Löhne in dieser Größenordnung oder darüber *(Deutschland hat eine der höchsten Abgabenlasten auf Löhne in der OECD → [[#Faktencheck|Faktencheck]])*.

> *„Entweder stellt sich Bernd Schattner hier in den Bundestag und lügt offensichtlich oder er hat die einfachsten Zahlen falsch. Beides fatal in einem Raum, in dem über die Zukunft von ganz Deutschland bestimmt wird."* [▶ 15:58](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=958)

---

## Was IT Mario gut macht — und was die Wissenschaft besser löst

Das Video verdient ehrliche methodische Einordnung. Was funktioniert gut:

**Transparenz über alles:** Rohdaten, Prompts, Spreadsheets — alles offen. Das ist mehr als viele journalistische Analysen leisten.

**Parteien-Blindheit des Modells:** Das blinde Bewerten ist der klügste Designentscheid. Das Modell weiß nicht, welche Partei es bewertet, und das nimmt eine erhebliche Bias-Quelle heraus.

**Vergleichbare Ergebnisse:** IT Mario nennt die PopBERT-Studie nicht, landet aber beim Populismus an derselben Spitze. Das spricht für den Befund, auch wenn die Wege verschieden sind.

Was die Wissenschaft anders — und besser — macht:

**PopBERT** (*Political Analysis*) ist das akademische Gegenstück: ein BERT-Modell, trainiert auf menschlich annotierten Bundestagsreden von 2013 bis 2021, auf Populismus kalibriert. Kernbefund: die höchsten Werte bei der AfD, gefolgt von der Linken, die Regierungsparteien am unteren Ende; seit ihrem Einzug 2017 führt die AfD deutlich. [→ Paper: Political Analysis](https://www.cambridge.org/core/journals/political-analysis/article/popbert-detecting-populism-and-its-host-ideologies-in-the-german-bundestag/06C14C50B50D5A7AB45C4A7C8A5AD945)

**Was IT Mario fehlt:**

1. **Kein Inter-Rater-Agreement:** GPT-4o-mini wurde nie gegen menschliche Politologen validiert. Wir wissen nicht, ob das Modell dasselbe unter „Populismus" versteht wie die Forschung.

2. **Statistische Signifikanz:** Die Unterschiede zwischen Parteien (z.B. AfD 7,06 vs. BSW 7,07 beim Vorwurfs-Score) sind marginal — es fehlen Konfidenzintervalle oder Signifikanztests.

3. **Kleine Stichprobe beim Faktencheck:** Gezogen wurden zufällig 200 Reden je Partei, daraus je drei bis fünf Behauptungen. Aus welchen Jahren und Themen sie stammen, sagt das Video nicht, und Konfidenzintervalle fehlen auch hier.

4. **GPT-Bias als blinder Fleck:** IT Mario benennt das Problem kurz — *„solche Sprachmodelle haben auch eine gewisse Bias, die sie aufgrund der Trainingsdaten in sich tragen"* — zieht daraus aber keine analytische Konsequenz. Wenn OpenAI-Modelle auf englischsprachigen Internetdaten trainiert wurden, die politisch linksliberal tendieren: Systematisch welche Texte werden dann als „populistisch" erkannt?

5. **Temporale Blindheit:** Die Analyse behandelt 2020–heute als homogenen Block. Populismus-Intensität verändert sich je nach politischem Klima — Wahlkampfphasen, Krisen, Koalitionsverhandlungen.

> [!note] Eigene Einschätzung
> Die Methodenkritik schmälert das Video nicht — sie schärft es. IT Mario macht etwas Wertvolles: Er zeigt, dass auch ein Einzelner mit öffentlichen Daten und einem guten Prompt-Design zu robusten Befunden kommen kann. Der Unterschied zu einem akademischen Paper liegt nicht in den Ergebnissen, sondern in der Fehlerquantifizierung. Er weiß, dass er *ungefähr* recht hat. Das Paper weiß, *wie sehr* es recht hat.

---

## Eine Randbemerkung über Bias — von IT Mario zu Gedankenwelten

IT Marios größte methodische Schwäche ist ausgerechnet seine selbsterklärte Stärke: die Neutralitätsbehauptung. *„Es ist also für mich maximal objektiv gestaltet“*, sagt er, und im nächsten Satz, dass solche Sprachmodelle einen Bias aus ihren Trainingsdaten tragen, gegen den er nichts tun könne ([▶ 4:32](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=272)). Er weiß also um die Grenze und hofft, sie durch Design klein zu halten; in der Videobeschreibung bleibt davon nur „maximal objektiv“.

Das ist ehrenwert. Und es ist ein Irrtum.

Es gibt keine Analyse ohne Perspektive. Nicht bei GPT-4o, das aus menschlichem Schreiben destilliert wurde. Nicht bei einem Politologen, der seine Annotationskriterien festlegt. Und nicht bei einem Wissensarchiv wie Gedankenwelten. Der Unterschied liegt nicht in der Anwesenheit oder Abwesenheit eines Standpunkts — sondern darin, ob man ihn kennt und offenlegt.

Gedankenwelten macht keinen Hehl daraus: Es gibt eine Perspektive. Aufklärung, Reflexion, Demokratie als schützenswertes Gut. Keine Parteilinie, kein Dogma — aber auch kein gespieltes Nichts. Die Einladung lautet nicht: *„Glaubt uns."* Sie lautet: *„Denkt selbst. Die Quellen liegen offen."* Das ist dieselbe Haltung, die IT Mario am Ende seines Videos einnimmt:

> *„Meine Message ist, es steht alles im Internet. Guckt es euch an, nehmt zuverlässige Quellen, analysiert die selber und bildet euch eure eigene Meinung."* [▶ 17:30](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=1050)

Der Bias ist real — hier wie dort. Die Frage ist nicht, ob er existiert. Die Frage ist, ob er transparent gemacht wird und ob die unbequemen Wahrheiten trotzdem reingelassen werden. Die AfD-Wortschatz-Überraschung, BSWs Vorwurfsführung, die Methodikgrenzen des eigenen Ansatzes — IT Mario lässt sie alle rein. Das ist die Bedingung: nicht Neutralität, sondern Ehrlichkeit. *Die Gedanken sind frei* — aber erst recht, wenn man weiß, welcher Garten sie wachsen lässt.

> [!note] Eigene Einschätzung
> Was IT Mario in 18 Minuten macht, teilt eine Grundhaltung mit diesem Archiv: Man benennt den eigenen Standpunkt, statt ihn hinter Neutralitätsvokabular zu verstecken — und man lässt trotzdem rein, was der Wahrheit dient, auch wenn es die eigene Position belastet. Das AfD-Wortschatz-Ergebnis, BSWs Vorwurfsführung, die Methodikgrenzen des eigenen Ansatzes: IT Mario zeigt sie alle. Nicht weil er naiv offen ist, sondern weil er methodisch konsequent ist.
>
> Die Hürde ist nicht: *Bin ich offen?* Die Hürde ist: *Hat dieser Befund sein Dogma abgelegt — oder dient er nur einer Erzählung?* Wer das unterscheiden kann, braucht keine starre Mauer. Eine elastische reicht — und hält mehr aus.

---

## Faktencheck

> [!success] Bestätigt — Bundestags-Datensatz (Zenodo)
> Der verwendete Datensatz ist real: Sean Fobbe stellt alle Bundestags-Stenogramme als strukturierte Daten auf Zenodo zur Verfügung. Quelle: [Zenodo Community Sean Fobbe](https://zenodo.org/communities/sean-fobbe-data/)

> [!success] Bestätigt — Kurzarbeit-Peak 6 Millionen (nicht 7)
> Von Storchs Behauptung, 7 Millionen seien in Kurzarbeit gewesen, ist falsch. Der Peak 2020 lag bei ca. 6 Millionen Kurzarbeitern. Quelle: [Bundesagentur für Arbeit — Kurzarbeit Zeitreihe](https://statistik.arbeitsagentur.de/SiteGlobals/Forms/Suche/Einzelheftsuche_Formular.html?topic_f=kurzarbeit-zr2)

> [!warning] Vereinfacht — „Höchste Steuerquote der Welt, 42 % im Durchschnitt“ und IT Marios Gegenrechnung
> Bernd Schattner (AfD) sagt, Deutschland habe die höchste Steuerquote der Welt, 42 % des Einkommens gingen im Durchschnitt an den Staat ([▶ 15:11](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=911)). Die erste Hälfte ist falsch: Bei der Abgabenlast auf Löhne liegt Belgien vorn (52,6 % der Arbeitskosten für einen Alleinstehenden mit Durchschnittslohn, 2024). Deutschland gehört aber mit über 45 % zu den fünf Ländern mit der höchsten Last, zusammen mit Österreich, Belgien, Frankreich und Italien. IT Marios Erklärung, die 42 % seien der Spitzensteuersatz, ist darum nur eine Lesart: Rechnet man Sozialabgaben ein, liegt die durchschnittliche Last auf einen Lohn in dieser Größenordnung oder darüber. Falsch ist der Superlativ, nicht die Zahl an sich. Quelle: [OECD, Taxing Wages 2025, Überblick](https://www.oecd.org/en/publications/2025/04/taxing-wages-2025_20d1a01d/full-report/overview_715add19.html)

> [!note] Korrigiert am 05.11.2026
> Wir hatten Schattners Satz eine „strategische Verwechslung“ genannt und IT Marios Spitzensteuersatz-Deutung als Tatsache übernommen. Beides trug nicht: Die Absicht ist unbelegt, und je nach Maß ist die Größenordnung von 42 % vertretbar. Der Name lautet Bernd, nicht Werner Schattner. Außerdem korrigiert: „Akademikeranteil“ war der Anteil mit akademischem Titel; IT Mario schränkt sein „maximal objektiv“ im Video selbst ein; die Gleichsetzung der drei Merkmale mit Muddes Definition; ein Satz über das limbische System bei Haidt.

> [!warning] Vereinfacht — „Maximal objektiv durch KI"
> IT Mario beschreibt das Verfahren als „für mich maximal objektiv“, weil das Modell die Partei nicht kennt, und räumt den Trainings-Bias selbst ein ([▶ 4:32](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=272)). Unterschätzt wird trotzdem: LLMs tragen systematische Trainingsdaten-Biases, die nicht durch Parteien-Blindheit eliminiert werden. Das Modell könnte bestimmte Rhetorikstile konsistent anders bewerten als andere — unabhängig von der Partei. Kein unabhängiger Validierungsprozess wurde durchgeführt. *Keine unabhängige Quelle für die Bias-Quantifizierung gefunden.*

> [!warning] Vereinfacht — Gleiche Fehlerquote für alle als fairer Maßstab
> IT Mario argumentiert: *„Diese Fehlerquote ist ja für alle Parteien gleich, deswegen ist das ein faires Verfahren."* Das stimmt nur, wenn GPT-4o auch tatsächlich für alle Parteien gleich oft irrt. Wenn das Modell bestimmte Typen von Behauptungen (z.B. quantitative Aussagen vs. normative Wertungen) unterschiedlich gut erkennt — und Parteien machen unterschiedliche Typen von Behauptungen — wäre die Fehlerquote strukturell ungleich. *Keine unabhängige Quelle.*

---

## Weiterführende Quellen

*Aus der Video-Beschreibung:*
- [Zenodo — Bundestag-Daten (Sean Fobbe)](https://zenodo.org/communities/sean-fobbe-data/records?q=&l=list&p=1&s=10&sort=newest)
- [Bundesagentur für Arbeit — Kurzarbeit Zeitreihe](https://statistik.arbeitsagentur.de/SiteGlobals/Forms/Suche/Einzelheftsuche_Formular.html?topic_f=kurzarbeit-zr2)
- [OECD Taxing Wages 2024](https://www.oecd.org/en/publications/taxing-wages-2024_dbcbac85-en.html)

*Wissenschaftlicher Kontext:*
- [PopBERT — Detecting Populism in the German Bundestag (Political Analysis, Cambridge 2024)](https://www.cambridge.org/core/journals/political-analysis/article/popbert-detecting-populism-and-its-host-ideologies-in-the-german-bundestag/06C14C50B50D5A7AB45C4A7C8A5AD945) — Peer-reviewed BERT-Modell mit menschlich annotierten Bundestags-Reden; methodisch robuster Vergleichsmaßstab
- [Scharloth — Ist die AfD eine populistische Partei? Korpuslinguistische Analyse](https://www.scharloth.com/publikationen/AfD_Scharloth.pdf) — Linguistische Analyse von AfD-Rhetorik mit Operationalisierung der drei Populismus-Dimensionen
- [Böckler-Impuls — Wie die AfD von Ängsten profitiert](https://www.boeckler.de/de/boeckler-impuls-wie-die-afd-von-angsten-profitiert-70656.htm) — Empirische Daten zur Angst-basierten Mobilisierung

---

## Verbindungen

### → [[Zeitgeist/MONITOR — AfD-Erfolg trotz Skandalen]]
Matthias Quents These, die AfD werde für die „Erlösung von der Komplexität" gewählt, deckt sich präzise mit IT Marios empirischem Befund: Komplexitätsreduktion ist eines der drei messbaren Populismus-Merkmale. Die MONITOR-Note liefert die politische Einordnung, IT Mario die quantitative Untermauerung.

### → [[Zeitgeist/Andreas Kemper — Technofaschismus und die AfD]]
Kemper weist Höckes Pseudonym durch linguistische Sprachmarker nach — ein vordigitales Äquivalent zu IT Marios KI-gestützter Rhetorik-Analyse. Beide nutzen Sprache als Beweis für politische Identität, mit verschiedenen Methoden aber ähnlichem Erkenntnisziel.

### → [[Zeitgeist/Katharina Nocun — Wie KI-Content das politische Vorfeld der extremen Rechten praegt]]
Spiegelverkehrte Perspektive: Nocun analysiert, wie KI rechte Propaganda *produziert* — IT Mario analysiert, wie KI rechte Rhetorik *misst*. Dasselbe Werkzeug, zwei entgegengesetzte Rollen. Zusammen ergibt sich ein vollständigeres Bild vom Verhältnis zwischen KI und politischer Sprache.

### → [[Zeitgeist/Philip Manow — Autoritäre Zeiten: Die Macht der Wähler]]
Manow diagnostiziert den strukturellen Populismus-Nährboden (Souveränitätsverlust, Komplexitätsdruck), den IT Marios Populismus-Score auf Redeebene messbar macht. Theorie (Manow) und Empirie (IT Mario) schließen sich hier direkt zusammen.

### → [[Denker/Jonathan Haidt — Kann ein gespaltenes Amerika heilen]]
Haidts Stammespsychologie hilft zu verstehen, warum Antielitarismus und Antipluralismus so wirkmächtig sind: Wer das Wir-gegen-die anspricht, erreicht die schnelle, intuitive Seite des Urteilens, bevor die Begründung nachkommt. Die Populismus-Merkmale wirken genau auf dieser Ebene.

### → [[Denker/Aladin El-Mafaalani — Misstrauensgemeinschaften und was die AfD wirklich stoppt (taz FUTURZWEI-Talk)]]
El-Mafaalanis Befund über wachsendes Misstrauen gegenüber Expertise erklärt das Dilemma von IT Marios Methode: Ein datengestützter Befund über die AfD wird von AfD-Wählern nicht als Argument wahrgenommen, sondern als Beweis für „Systemmedien".

### → [[Zeitgeist/BissenBlaBla — Bilanz rechter Regierungen]]
Beide teilen denselben epistemischen Ansatz: politische Analyse durch öffentlich zugängliche, methodisch transparente Daten — BissenBlaBla via internationale Indizes, IT Mario via offene Spreadsheets und Zenodo. Methodische Transparenz als gemeinsame Gegenstrategie.

### → [[Panorama/NoAfD]]
Das Panorama bündelt das gesamte AfD-Analysecorpus der Gedankenwelten. IT Marios Datenanalyse ergänzt die qualitativen Analysen (Kemper, Quent, Manow) um eine quantitative Schicht — eine der wenigen empirisch gestützten Aussagen im Corpus.

---

## Weiterdenken

> [!question] Was Sokrates vielleicht gefragt hätte
> - Wenn ein KI-Modell Populismus erkennt, das selbst aus populistisch verzerrten Trainingsdaten gelernt hat — *erkennt es dann Populismus, oder spiegelt es ihn?*
> - IT Mario sagt: „Ich will keine Partei an der Macht haben, die nachweislich am meisten lügt." — Aber *was genau ist eine Lüge im Bundestag?* Eine falsche Zahl? Eine falsche Kausalität? Ein bewusst irreführender Kontext? Haben verschiedene Parteien verschiedene Lüge-Stile — und welcher ist schlimmer?
> - Die AfD hat laut IT Mario den größten Wortschatz aller Parteien im Plenum. Gleichzeitig den höchsten Populismus-Score. *Widerspricht das der These, Populismus sei eine Vereinfachungsstrategie — oder bestätigt es sie?*
> - PopBERT und IT Mario kommen zu vergleichbaren Ergebnissen auf verschiedenen Wegen. *Was sagt uns diese Konvergenz? Dass die Methode gut ist — oder dass das Ergebnis so offensichtlich ist, dass jeder Ansatz es findet?*
> - *Dürfen wir auf Basis von KI-generierten Scores politische Urteile fällen — und wenn nein: warum vertrauen wir dann Meinungsumfragen, die ähnliche Schwächen haben?*

### → [[Gedanken/Die elastische Brandmauer — Was sein Dogma abgelegt hat, darf rein]]
Aus der Reflexion über dieses Video entstand der Gedanke zur elastischen Brandmauer: IT Marios AfD-Wortschatz-Überraschung und BSW-Befund als Beispiele für unbequeme Wahrheiten, die durch eine ehrliche Methode kommen — und damit zeigen, dass hier nicht nach Lager sortiert wird.
