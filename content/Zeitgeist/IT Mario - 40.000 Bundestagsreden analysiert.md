---
title: "IT Mario — 40.000 Bundestagsreden analysiert: Welche Partei ist wirklich gefährlich?"
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

Quelle: [40.000 Reden analysiert: Welche Partei ist WIRKLICH gefährlich?](https://www.youtube.com/watch?v=1LH7PZAPq-Y) (21.05.2026)

> [!info] Wer spricht?
> **IT Mario** — Datenanalyst und Data-Science-Content-Creator, der komplexe Analysen für ein breites Publikum zugänglich macht. Sein Kanal fokussiert auf datengetriebene Recherche: YouTube-Werbemessung, Kommentaranalyse, KI-Erklärvideos — und jetzt Bundestags-Rhetorik.
>
> Keine politikwissenschaftliche Ausbildung, aber methodische Transparenz als Stärke: alle Bewertungen öffentlich in Google Spreadsheets, Datenquelle offen auf Zenodo. Er sagt selbst: *„Ich bin auch nur irgendein YouTuber, der euch irgendwas erzählt. Ihr müsst selber nachdenken."*
>
> Einordnung: Techniker-Perspektive auf politische Sprache — keine Parteilinie, keine akademische Agenda. Wert liegt in der Transparenz und Reproduzierbarkeit, Grenze in der fehlenden politikwissenschaftlichen Validierung.
>
> → [[Gedankenwelten/DenkerVita/IT Mario|DenkerVita]]

---

## Die Datenbasis — 80.000 Reden, offen und nachvollziehbar

[▶ 0:45](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=45)

Der methodische Ausgangspunkt ist solide: IT Mario nutzt den Datensatz aus dem [Zenodo-Archiv von Sean Fobbe](https://zenodo.org/communities/sean-fobbe-data/), der alle Bundestags-Stenogramme als maschinenlesbare Daten aufbereitet hat. Das Ergebnis: knapp 80.000 Reden ab 2013, inklusive Metadaten (Partei, Datum, Redner, Kommentare aus dem Plenum). Für die Scoring-Analyse werden die ca. 45.000 Reden ab 2020 verwendet.

Dieser Datensatz ist öffentlich, frei verfügbar, und institutionell zuverlässig — das Bundestag-Protokoll ist kein Meinungsdokument, sondern ein amtliches Schriftstück. Damit hat IT Mario eine bessere Primärquelle als viele Medienberichte über parlamentarische Rhetorik.

Bevor er in die KI-Analyse geht, wirft er einen kurzen Blick auf die Metadaten: Akademikeranteil (CDU/CSU führt mit 20,6 %, AfD liegt mit 15 % im Mittelfeld, Linke bildet mit 8,8 % das Schlusslicht), Wortschatz (Type-Token-Ratio: AfD überraschend an der Spitze, CDU/CSU vorletzter Platz), und Heiterkeitseinträge im Protokoll als Näherungswert für Lacher im Plenum (AfD führt). Diese Metadaten-Analyse ist methodisch harmlos — sie beschreibt, wertet noch nicht.

> [!note] Eigene Einschätzung
> Der Wortschatz-Befund ist kontraintuitiv und verdient mehr Aufmerksamkeit als IT Mario ihm gibt: Dass die AfD den größten dokumentierten Wortschatz im Plenum hat, widerspricht dem Klischee der primitiven Demagogen. Gleichzeitig sagt Wortschatzreichtum nichts über Wahrheitsgehalt oder argumentative Redlichkeit — Komplexität kann auch strategisch zur Verschleierung eingesetzt werden.

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

Das ist ein wichtiger analytischer Schritt: Vorwürfe sind in der parlamentarischen Opposition strukturell erwartet. Dass BSW — die *neue* Oppositionspartei mit einer Frontfrau, die ihr politisches Kapital aus moralischer Empörung schöpft — knapp vorne liegt, ist eigentlich die eigentliche Nachricht. Sahra Wagenknechts persönlich vorgetragene Rede erhält 10 von 10 Punkten:

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
> Diese drei Merkmale — Antielitarismus, Antipluralismus, Komplexitätsreduktion — sind keine Erfindung IT Marios. Sie entsprechen der klassischen Definition von Cas Mudde, dem führenden Populismus-Forscher. IT Mario hat intuitiv richtig analysiert, ohne die Primärliteratur zu kennen. Das ist sowohl Stärke (unabhängige Konvergenz) als auch Schwäche (fehlende Präzision der Grenzbegriffe).

> [!question] Weitergedacht
> Gilt Komplexitätsreduktion als populistisches Merkmal — oder als *erforderliche* Vereinfachung in einer Demokratie, die auch Nicht-Akademiker erreichen muss? *Ab wann wird aus notwendiger Klarheit schädliche Vereinfachung?*

---

## Faktencheck: Wer lügt wie oft?

[▶ 12:56](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=776)

Der methodisch anspruchsvollste Teil: Aus je 200 zufällig ausgewählten Reden pro Partei extrahiert GPT-4o drei bis fünf falsifizierbare Tatsachenbehauptungen und bewertet sie als *richtig*, *falsch* oder *Kontext fehlt*. Das Ergebnis:

- **SPD** führt mit ca. 70 % korrekten Aussagen
- **AfD** bildet das Schlusslicht — nicht nur relativ die wenigsten korrekten, sondern auch absolut die meisten eindeutig falschen Aussagen

Zwei Beispiele, die IT Mario ausführt:

*Beatrix von Storch, 2020*: Behauptung, 7 Millionen Arbeitnehmer seien in Kurzarbeit. Tatsächlich lag der Peak bei 6 Millionen (Quelle: Bundesagentur für Arbeit). Die Zahl ist falsch — aber die Zahl macht das Argument nicht besser oder schlechter, sie skaliert es nur leicht über.

*Werner Schattner*: *„Deutschland hat die höchste Steuerquote der Welt, 42 % des Einkommens gehen im Durchschnitt an den Staat."* Beides falsch: Frankreich und Skandinavien liegen höher; die 42 % sind der Spitzensteuersatz, nicht der Durchschnitt — und betreffen nur Einkommen über einem Schwellenwert. Das ist kein Versprecher, das ist eine strategische Verwechslung.

> *„Entweder stellt sich Bern Schattner hier in den Bundestag und lügt offensichtlich oder er hat die einfachsten Zahlen falsch. Beides fatal in einem Raum, in dem über die Zukunft von ganz Deutschland bestimmt wird."* [▶ 15:58](https://www.youtube.com/watch?v=1LH7PZAPq-Y&t=958)

---

## Was IT Mario gut macht — und was die Wissenschaft besser löst

Das Video verdient ehrliche methodische Einordnung. Was funktioniert gut:

**Transparenz über alles:** Rohdaten, Prompts, Spreadsheets — alles offen. Das ist mehr als viele journalistische Analysen leisten.

**Parteien-Blindheit des Modells:** Das blind scoring ist der klügste Designentscheid. Kein menschlicher Annotator weiß, welche Partei er bewertet — das eliminiert eine erhebliche Bias-Quelle.

**Emergente Validierung:** IT Mario kannte die PopBERT-Studie vermutlich nicht, landet aber bei vergleichbaren Ergebnissen. Das ist unabhängige Konvergenz.

Was die Wissenschaft anders — und besser — macht:

**PopBERT (Cambridge, 2024)** ist das akademische Äquivalent: Ein BERT-Modell, trainiert auf menschlich annotierten Bundestags-Reden von 2013–2021, speziell auf Populismus kalibriert. Kernbefund: AfD und Linke führen den Populismus-Score, AfD stark im rechten Host-Populismus. [→ Paper: Political Analysis, 2024](https://www.cambridge.org/core/journals/political-analysis/article/popbert-detecting-populism-and-its-host-ideologies-in-the-german-bundestag/06C14C50B50D5A7AB45C4A7C8A5AD945)

**Was IT Mario fehlt:**

1. **Kein Inter-Rater-Agreement:** GPT-4o-mini wurde nie gegen menschliche Politologen validiert. Wir wissen nicht, ob das Modell dasselbe unter „Populismus" versteht wie die Forschung.

2. **Statistische Signifikanz:** Die Unterschiede zwischen Parteien (z.B. AfD 7,06 vs. BSW 7,07 beim Vorwurfs-Score) sind marginal — es fehlen Konfidenzintervalle oder Signifikanztests.

3. **Selektionsbias beim Faktencheck:** Welche 200 Reden pro Partei wurden für den Faktencheck gezogen? Zufällig oder nach Thema? Das beeinflusst das Ergebnis erheblich.

4. **GPT-Bias als blinder Fleck:** IT Mario benennt das Problem kurz — *„solche Sprachmodelle haben auch eine gewisse Bias, die sie aufgrund der Trainingsdaten in sich tragen"* — zieht daraus aber keine analytische Konsequenz. Wenn OpenAI-Modelle auf englischsprachigen Internetdaten trainiert wurden, die politisch linksliberal tendieren: Systematisch welche Texte werden dann als „populistisch" erkannt?

5. **Temporale Blindheit:** Die Analyse behandelt 2020–heute als homogenen Block. Populismus-Intensität verändert sich je nach politischem Klima — Wahlkampfphasen, Krisen, Koalitionsverhandlungen.

> [!note] Eigene Einschätzung
> Die Methodenkritik schmälert das Video nicht — sie schärft es. IT Mario macht etwas Wertvolles: Er zeigt, dass auch ein Einzelner mit öffentlichen Daten und einem guten Prompt-Design zu robusten Befunden kommen kann. Der Unterschied zu einem akademischen Paper liegt nicht in den Ergebnissen, sondern in der Fehlerquantifizierung. Er weiß, dass er *ungefähr* recht hat. Das Paper weiß, *wie sehr* es recht hat.

---

## Eine Randbemerkung über Bias — von IT Mario zu Gedankenwelten

IT Marios größte methodische Schwäche ist ausgerechnet seine selbsterklärte Stärke: die Neutralitätsbehauptung. *„Maximal objektiv gestaltet"* — das sagt jemand, der weiß, dass sein Modell Biases trägt, aber hofft, sie durch Design zu neutralisieren.

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

> [!success] Bestätigt — Deutschland keine höchste Steuerquote weltweit
> Die Behauptung, Deutschland habe die höchste Steuerquote der Welt, ist falsch. Frankreich, Belgien und skandinavische Länder liegen teils deutlich höher. Quelle: [OECD Taxing Wages 2024](https://www.oecd.org/en/publications/taxing-wages-2024_dbcbac85-en.html)

> [!warning] Vereinfacht — „Maximal objektiv durch KI"
> IT Mario beschreibt das Verfahren als „maximal objektiv", weil das Modell die Partei nicht kennt. Das übersieht: LLMs tragen systematische Trainingsdaten-Biases, die nicht durch Parteien-Blindheit eliminiert werden. Das Modell könnte bestimmte Rhetorikstile konsistent anders bewerten als andere — unabhängig von der Partei. Kein unabhängiger Validierungsprozess wurde durchgeführt. *Keine unabhängige Quelle für die Bias-Quantifizierung gefunden.*

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

### → [[Gedankenwelten/Zeitgeist/MONITOR — AfD-Erfolg trotz Skandalen]]
Matthias Quents These, die AfD werde für die „Erlösung von der Komplexität" gewählt, deckt sich präzise mit IT Marios empirischem Befund: Komplexitätsreduktion ist eines der drei messbaren Populismus-Merkmale. Die MONITOR-Note liefert die politische Einordnung, IT Mario die quantitative Untermauerung.

### → [[Gedankenwelten/Zeitgeist/Andreas Kemper — Technofaschismus und die AfD]]
Kemper weist Höckes Pseudonym durch linguistische Sprachmarker nach — ein vordigitales Äquivalent zu IT Marios KI-gestützter Rhetorik-Analyse. Beide nutzen Sprache als Beweis für politische Identität, mit verschiedenen Methoden aber ähnlichem Erkenntnisziel.

### → [[Gedankenwelten/Zeitgeist/Katharina Nocun — Wie KI-Content das politische Vorfeld der extremen Rechten praegt]]
Spiegelverkehrte Perspektive: Nocun analysiert, wie KI rechte Propaganda *produziert* — IT Mario analysiert, wie KI rechte Rhetorik *misst*. Dasselbe Werkzeug, zwei entgegengesetzte Rollen. Zusammen ergibt sich ein vollständigeres Bild vom Verhältnis zwischen KI und politischer Sprache.

### → [[Gedankenwelten/Zeitgeist/Philip Manow — Autoritäre Zeiten: Die Macht der Wähler]]
Manow diagnostiziert den strukturellen Populismus-Nährboden (Souveränitätsverlust, Komplexitätsdruck), den IT Marios Populismus-Score auf Redeebene messbar macht. Theorie (Manow) und Empirie (IT Mario) schließen sich hier direkt zusammen.

### → [[Gedankenwelten/Denker/Jonathan Haidt — Kann ein gespaltenes Amerika heilen]]
Haidts Stammespsychologie erklärt, warum Antielitarismus und Antipluralismus so wirkmächtig sind: Wer das Stammesgefühl anspricht, gewinnt, weil das limbische System schneller reagiert als der präfrontale Kortex. Die drei Populismus-Merkmale sind Haidts Theorie in angewandter Form.

### → [[Gedankenwelten/Denker/Aladin El-Mafaalani — Misstrauensgemeinschaften und was die AfD wirklich stoppt (taz FUTURZWEI-Talk)]]
El-Mafaalanis Befund über wachsendes Misstrauen gegenüber Expertise erklärt das Dilemma von IT Marios Methode: Ein datengestützter Befund über die AfD wird von AfD-Wählern nicht als Argument wahrgenommen, sondern als Beweis für „Systemmedien".

### → [[Gedankenwelten/Zeitgeist/BissenBlaBla — Bilanz rechter Regierungen]]
Beide teilen denselben epistemischen Ansatz: politische Analyse durch öffentlich zugängliche, methodisch transparente Daten — BissenBlaBla via internationale Indizes, IT Mario via offene Spreadsheets und Zenodo. Methodische Transparenz als gemeinsame Gegenstrategie.

### → [[Gedankenwelten/Panorama/NoAfD]]
Das Panorama bündelt das gesamte AfD-Analysecorpus des Cortex. IT Marios Datenanalyse ergänzt die qualitativen Analysen (Kemper, Quent, Manow) um eine quantitative Schicht — eine der wenigen empirisch gestützten Aussagen im Corpus.

---

## Weiterdenken

> [!question] Was Sokrates vielleicht gefragt hätte
> - Wenn ein KI-Modell Populismus erkennt, das selbst aus populistisch verzerrten Trainingsdaten gelernt hat — *erkennt es dann Populismus, oder spiegelt es ihn?*
> - IT Mario sagt: „Ich will keine Partei an der Macht haben, die nachweislich am meisten lügt." — Aber *was genau ist eine Lüge im Bundestag?* Eine falsche Zahl? Eine falsche Kausalität? Ein bewusst irreführender Kontext? Haben verschiedene Parteien verschiedene Lüge-Stile — und welcher ist schlimmer?
> - Die AfD hat laut IT Mario den größten Wortschatz aller Parteien im Plenum. Gleichzeitig den höchsten Populismus-Score. *Widerspricht das der These, Populismus sei eine Vereinfachungsstrategie — oder bestätigt es sie?*
> - PopBERT und IT Mario kommen zu vergleichbaren Ergebnissen auf verschiedenen Wegen. *Was sagt uns diese Konvergenz? Dass die Methode gut ist — oder dass das Ergebnis so offensichtlich ist, dass jeder Ansatz es findet?*
> - *Dürfen wir auf Basis von KI-generierten Scores politische Urteile fällen — und wenn nein: warum vertrauen wir dann Meinungsumfragen, die ähnliche Schwächen haben?*

### → [[Gedankenwelten/Gedanken/Die elastische Brandmauer — Was sein Dogma abgelegt hat, darf rein]]
Aus der Reflexion über dieses Video entstand der Gedanke zur elastischen Brandmauer: IT Marios AfD-Wortschatz-Überraschung und BSW-Befund als Beispiele für unbequeme Wahrheiten, die durch eine ehrliche Methode kommen — und damit zeigen, dass hier nicht nach Lager sortiert wird.
