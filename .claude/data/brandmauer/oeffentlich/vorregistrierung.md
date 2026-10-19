# Vorregistrierung — Brandmauer in den Kommentarspalten

*Festgelegt am 17.10.2026, bevor ein einziger Auszug des Korpus kodiert wurde. Gesehen waren bis dahin nur
die Seite vom 21.08.2026 (Strukturtest) und die Zitate der beiden Sammel-Agenten (owner-inbox-Bericht folgt).
Danach nicht mehr verändert; Präzisierungen nur als datierte Nachträge unten, und nur verschärfend.*

Gehört zur geplanten Spur „Fällt die Brandmauer in den Kommentarspalten?“ (Arbeitstitel).

## Korpus

- **DLF „Die Presseschau aus deutschen Zeitungen“**, wörtliche Kommentarauszüge mit Blatt und Datum.
  - 2021–2026: deutschlandfunk.de/die-presseschau-aus-deutschen-zeitungen-NNNN.html (vollständig, soweit online)
  - 2016–2021: Wayback-Machine-Schnappschüsse der alten Adressen `.433.de.html` und `.2287.de.html`
    (Stichprobe, ungleichmäßig; 2013–2015 nur 7 Tage — als Lücke ausgewiesen, nicht hochgerechnet)
- Einheit ist der **Absatz** = in der Regel ein Kommentar eines Blatts.
- Grenzen, offen benannt: Die Auswahl trifft die DLF-Redaktion (Ziel: Spektrum abbilden). Die Messung zeigt das
  gespiegelte Meinungsbild, keine Vollerhebung. Regionalzeitungen sind stark vertreten, Bezahlmedien ohne
  Presseschau-Zitat fehlen. Online-only-Stimmen (NIUS, Tichy, Apollo) fehlen ganz.

## Sieb (Vorkommen, maschinell, auf Vollständigkeit angelegt)

Ein Absatz kommt in die Kodierung, wenn er (a) einen **Akteurbezug** und (b) einen **Umgangsbezug** enthält.

- **AfD-Spur (a):** `AfD|Alternative für Deutschland|Höcke|Weidel|Gauland|Chrupalla|Petry|Meuthen|Siegmund|Rechtspopulist|Rechtsextrem|rechtsradikal|rechten Rand|Rechtsaußen`
- **Linke-Spur (a):** `Linke|Linkspartei|Linken|PDS|Ramelow|Reichinnek|Schwerdtner|van Aken|Eralp|Linksaußen|Linksextrem|SED-Nachfolge`
- **Umgangsbezug (b):** `Brandmauer|Zusammenarbeit|zusammenarbeit|Koalition|koalier|toleri|Minderheitsregierung|Unvereinbarkeit|ausgrenz|Ausgrenz|abgrenz|Abgrenz|Tabubruch|Dammbruch|Stimmen der AfD|mit der AfD|mit den Linken|mit der Linken|Mehrheit|entzaubern|Entzauberung|Schmuddel|ignorier|normalisier|Normalisier|Cordon|Kooperation|kooperier|Pakt|Bündnis`

Das Sieb wird an zwei zufälligen Jahrgängen gegen eine Handdurchsicht geprüft (Trefferquote wird berichtet).

## Kodierung (Haltung — urteilt Claude, jeder Absatz einzeln, keine Vorsortierung durch ein Modell)

Kodiert wird die **Stimme des Blatts**, nicht zitierte Politiker. Gibt ein Blatt nur eine Politikeraussage wieder,
ohne eigene Wertung → D.

**AfD-Achse**

| Code | Bedeutung |
|---|---|
| **D** | deskriptiv / Prognose / Lagebericht, keine eigene Haltung zur Abgrenzung |
| **H** | **halten**: verteidigt die Abgrenzung, warnt vor Zusammenarbeit, Tabubruch-Vorwurf, Normalisierungswarnung, Verbotsforderung |
| **K** | **Kritik an Wort, Ritual oder Wirkung** der Brandmauer, *ohne* eine Zusammenarbeit zu befürworten („abgrenzen statt ausgrenzen“, „inhaltlich stellen“, „Moralisierung hilft der AfD“, „Brandmauer gescheitert“ ohne Konsequenz) |
| **L1** | **Mehrheiten mit AfD-Stimmen / Sachabstimmungen hinnehmbar**, Koalition ausdrücklich oder erkennbar nein |
| **L2** | **Zusammenarbeit befürwortet oder Brandmauer abzuschaffen**: Tolerierung, Koalition, „mit der AfD reden/verhandeln“ als Regierungsoption, „Wählerwillen akzeptieren“ im Sinn einer Regierungsbeteiligung |

**Linke-Achse** (dieselbe Logik, gespiegelt): D · **H** (Abgrenzung nach links halten/verschärfen) · **K** · **L1** (Mehrheiten mit Linken-Stimmen hinnehmbar) · **L2** (Zusammenarbeit/Tolerierung/Koalition befürwortet, Unvereinbarkeitsbeschluss aufheben).

**Flagge S (Symmetrie)**, wo der Absatz AfD und Linke vergleicht: **S=** (gleichsetzend, „beide Ränder“), **S≠** (ausdrücklich unterscheidend).

Zweifelsregel: Zwischen zwei Codes gilt der **vorsichtigere** (näher an D bzw. H). So kann die Kodierung eine
Verschiebung eher unter- als überschätzen — wer recht behalten will, soll es schwer haben.

**Reliabilität:** 10 % der Absätze (Zufall, Seed festgehalten) werden in einem zweiten Durchgang blind neu kodiert;
die Übereinstimmung (Prozent und Cohens κ) wird berichtet.

## Hypothesen und was sie widerlegt

**H1 — „Die Brandmauer fällt in den Kommentarspalten“** (Andreas' Eindruck).
Gemessen: Anteil L1+L2 an allen haltungstragenden Absätzen (H+K+L1+L2) der AfD-Achse, je Halbjahr.
- *Gestützt*, wenn der Anteil in 2025-H2 bis 2026-H2 um mindestens 10 Prozentpunkte über 2019-H2 bis 2021-H1 liegt.
- *Widerlegt*, wenn er nicht höher liegt (Differenz ≤ 0).
- Dazwischen: *nicht entscheidbar*, so berichtet.
- Nebenmaß: Anteil K (die Vorstufe) getrennt ausgewiesen.

**H2 — „Polarisierung der Häuser“** (Andreas, 17.10.: kein Mainstream, sondern Lager, „war schon immer so“).
Gemessen je Zeitraum (2016–2019 · 2020–2022 · 2023–2024 · 2025–2026), nur Blätter mit ≥ 5 haltungstragenden Absätzen:
die Spannweite der Blatt-Anteile L1+L2 und die Zahl der Blätter mit mindestens einem L-Absatz.
- *Polarisierung wächst*, wenn die Spannweite steigt **und** die H-lastigen Blätter H-lastig bleiben (ihr H-Anteil sinkt nicht um mehr als 10 Punkte).
- *Gleichlauf statt Polarisierung*, wenn sich alle Blätter in dieselbe Richtung bewegen (Spannweite konstant oder fallend).
- „War schon immer so“ ist *gestützt*, wenn die Spannweite schon 2016–2019 groß war (≥ 30 Punkte zwischen den Rändern), *widerlegt*, wenn sie damals klein war.

**H3 — „So weit, wie sie können“** (Andreas: Befürworter der Zusammenarbeit offenbaren sich erst, wenn es gefahrlos ist; vgl. Kuran, *preference falsification*).
Unterscheidende Vorhersage gegenüber ehrlichem Umdenken:
- (a) **Stufenfolge:** Blätter, die 2025–2026 L-Absätze haben, zeigen davor K-Absätze (K vor L). *Widerspricht H3*, wenn die Mehrheit dieser Blätter vorher nur H oder D zeigt.
- (b) **Kaskade:** Der L-Anteil springt in einem kurzen Fenster nach einem Erlaubnis-Ereignis (Wahlsieg, Umfragehoch, Tabubruch ohne Folgen: 01/2025, 09/2026) deutlich stärker als im Trend davor. Kuran sagt Sprünge voraus, ehrliches Umdenken eher Gleiten. *Widerspricht H3*, wenn die Verschiebung gleichmäßig verläuft.
- Grenze, vorab eingestanden: Absicht ist nicht messbar. Auch ehrliches Umdenken kann einem Ereignis folgen. H3 kann
  durch diese Daten **geschwächt**, aber nicht **bewiesen** werden.

**H4 — „Nach links wird ausgebaut“** (Andreas' Eindruck).
Gemessen: Anteil H an den haltungstragenden Absätzen der Linke-Achse, je Zeitraum, und Anteil S= an allen Vergleichsabsätzen.
- *Gestützt*, wenn der H-Anteil links 2025–2026 um ≥ 10 Punkte über 2019–2021 liegt.
- *Widerlegt*, wenn er gleich bleibt oder sinkt.
- Zusatz **Asymmetrie** (aus der Stimmen-Recherche als Verdacht): Blätter mit L-Anteil rechts haben einen höheren H-Anteil links. Geprüft als Rangkorrelation über die Blätter; berichtet, keine Schwelle.

## Was diese Messung nicht entscheidet

Ob die Brandmauer *richtig* ist. Die Spur misst, wie die Kommentarspalten sich bewegen, nicht, wohin sie sich bewegen sollten.

---

## Nachtrag 1 — 17.10.2026, vor der Kodierung (verschärfend)

Handprüfung des Siebs an den Seiten Juni–Oktober 2026: Von 120 Absätzen mit Akteur-, aber ohne Umgangsbezug
waren mehrere eindeutig einschlägig (FR 14.10.2026 „keinen Antidemokraten zum Ministerpräsidenten zu wählen“;
Hamburger Abendblatt 08.10.2026 „verhilft wohl die CDU der AfD ins Amt“; FR 07.10.2026 „Rausch diesen Posten
zu verweigern“; Weser-Kurier 22.09.2026 zur Linken „niemals auch nur in die Nähe des Chefsessels“). Auch eine
erweiterte Wortliste fing nur 41 von 120.

**Darum:** Kodiert wird **jeder Absatz mit Akteurbezug** (AfD- oder Linke-Liste oben). Der Umgangsbezug wird nur
noch als Merkmal mitgespeichert, nicht mehr als Filter. Die Kategorien, Hypothesen und Schwellen bleiben unverändert.

**Blindkodierung:** Die Absätze werden in Zufallsreihenfolge (Seed 20261017) vorgelegt, ohne Datum und ohne
Seitenkontext. Das Blatt bleibt sichtbar, weil es im Text steht. So kann der erwartete Zeittrend nicht in die
Einzelurteile einsickern.

## Nachtrag 2 — 17.10.2026, vor der Kodierung (nur Korpus, keine Kategorien)

Das Online-Archiv des DLF reicht nicht bis 2021 zurück, sondern beginnt am **23.02.2023** (ältere Seiten sind
depubliziert; Stichproben bis Nr. 6201 gerade wie ungerade: 404). Das Korpus setzt sich darum so zusammen:

| Zeitraum | Quelle | Dichte |
|---|---|---|
| 2015–2021 | Wayback, alte Adressen `.433`/`.2287` | 301 Tage (2020: 105) |
| Nov 2021 – Feb 2023 | Wayback, neue Adresse `die-presseschau-…-NNNN` | 387 Schnappschüsse, ≈ 25 je Monat |
| 23.02.2023 – 17.10.2026 | DLF online | eine Seite je Tag |

Die Wayback-Jahre sind Stichproben, die Online-Jahre fast vollständig. Darum werden alle Vergleiche über **Anteile**
gerechnet, nie über absolute Zahlen, und je Zeitraum wird die Zahl der zugrunde liegenden Tage ausgewiesen. Ein
Tagesdatum, das nur aus dem Archiv-Zeitstempel stammt (20 Seiten), ist als unsicher markiert.

## Nachtrag 3 — 17.10.2026, nach der Kodierung (Bericht, keine Änderung an Kategorien oder Schwellen)

- **Kodiert:** alle 1.919 Absätze (32 Stapel à 60, Seed 20261017), verblindet. Auslegungsregeln 1–105 entstanden
  während der Kodierung und präzisieren das Codebuch; sie stehen mit Stapelnummer in `kodierung/kodierregeln.md`.
- **Zuverlässigkeit:** 192 Absätze (10 %, Seed 20261018) zweitkodiert, ohne Einsicht in den ersten Durchgang.
  AfD-Achse 94,8 % (κ 0,91), Linke-Achse 99,0 % (κ 0,97), S-Flagge 99,5 % (κ 0,85); unter den Absätzen mit Haltung
  86 %. **Einschränkung:** derselbe Kodierer in beiden Durchgängen — gemessen ist die Stabilität, nicht die
  Übereinstimmung zweier Kodierer. Ausgewertet wird der erste Durchgang.
- **Blattnamen:** Nach dem Entblinden normalisiert (Genitiv, Artikel, Schreibvarianten; Kürzel wie „CDU-V“ durch das
  im Text genannte Blatt ersetzt, vier Fälle von Hand). Code in `kodierung/auswertung.py`.
- **H2, Zeitraum 2016–2019:** Kein Blatt erreicht dort 5 Haltungsabsätze. Der Test „war schon immer so“ ist mit
  diesem Korpus **nicht durchführbar**; so berichtet, nicht ersetzt.
- **Ergebnisse** in `kodierung/auswertung.md`; Bericht in `owner-inbox/Bericht-Medien-Brandmauer.md`.

## Nachtrag 4 — 19.10.2026, vor der Veröffentlichung der Spur (Klarstellung, Zweitkodierung, Daten)

- **Erlaubnis-Ereignis präzisiert.** Die Falsifikationsbedingung der Spur (Entwurf 17.10.) nannte eine Landesregierung,
  „die von der AfD mitgetragen oder toleriert wird“. Anlass: Ulrich Siegmund will sich im Dezember 2026 in
  Sachsen-Anhalt zum Ministerpräsidenten wählen lassen; am 06.10.2026 wurde Tobias Rausch (AfD) mit mindestens vier
  Stimmen aus anderen Fraktionen Landtagspräsident (geheime Wahl). Neu, **vor** jeder Nachmessung und vor der
  Veröffentlichung: „von der AfD **geführt**, mitgetragen oder toleriert, auch ein AfD-Ministerpräsident, der mit
  Stimmen anderer Fraktionen gewählt wird“. Das ist verschärfend: Mehr Ereignisse können die These widerlegen.
  Schwellen und Messverfahren unverändert.
- **Zweitkodierung durch einen Menschen.** Andreas kodiert verblindet 60 Absätze der AfD-Achse
  (`kodierung/zweitkodierung.py`, Seed 20261019). Geschichtet nach dem ersten Durchgang: alle 12 L, 18 K, 15 H, 15 D,
  damit die seltenen Codes vorkommen. Blattnamen im Text geschwärzt, kein Datum, Zufallsreihenfolge; er sieht
  Codebuch, Zweifelsregel und (aufklappbar) die Auslegungsregeln ohne die Linke-Achse. Berichtet werden
  Übereinstimmung und κ auf der Stichprobe (wegen der Schichtung keine Schätzung für das ganze Korpus), die
  Kreuztabelle und jede Abweichung. Der erste Durchgang bleibt die Auswertungsgrundlage; ändert sich das Bild,
  wird das berichtet, nicht nachträglich umkodiert.
- **Daten öffentlich.** Mit der Spur werden Vorregistrierung, Codebuch, Auslegungsregeln, die Codes je Absatz mit
  Datum, Blatt und Fundstelle (DLF-Seitennummer bzw. Wayback-Zeitstempel) und das Auswertungsskript veröffentlicht.
  Die Absatztexte nicht (Rechte beim DLF bzw. den Blättern); sie sind über die Fundstelle auffindbar.

## Nachtrag 4a — 19.10.2026, während der Zweitkodierung (Vereinfachung der Antworten)

Nach 23 Absätzen meldete Andreas, die fünf Codes seien an komplexen Kommentartexten kaum sicher zu vergeben
(Zwischenstand: 43 % Übereinstimmung, κ 0,30). Für die restlichen 37 stehen darum vier Antworten in Alltagssprache
zur Wahl: verteidigt (H) · kritisiert ohne Zusammenarbeit (K) · hält Zusammenarbeit oder AfD-Mehrheiten für in
Ordnung (L = L1+L2) · nichts davon (D). Die ersten 23 werden genauso zusammengefasst. Verglichen wird auf diesen vier
Stufen, dazu Hinnahme ja/nein und Haltung ja/nein. Seine Einzelcodes hat Andreas vor dem Ende nicht mit meinen
verglichen gesehen; mitgeteilt wurden ihm nur der Zwischenstand und die zwei Richtungen der Abweichung.
