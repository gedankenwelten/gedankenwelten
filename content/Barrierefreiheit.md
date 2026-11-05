---
title: Barrierefreiheit
description: Die Gedankenwelten sollen sich auch hören lassen. Wie man sich mit Screenreader und Tastatur bewegt, was schon geht und wo es noch hakt.
date: 2026-11-05
tags: []
aliases:
  - Accessibility
  - Barrierefrei
---

Die Gedankenwelten sollen sich nicht nur lesen, sondern auch hören lassen. Wer die Seite nicht sieht, schlecht sieht oder lieber mit der Tastatur arbeitet, soll hier ohne Umwege ankommen. Diese Seite sagt, was dafür getan ist und wo es noch hakt.

## Mit dem Screenreader

**Zum Text springen.** Der erste Halt mit der Tabulatortaste ist ein Link, der direkt zum Anfang der Note führt, an der Kopfleiste vorbei.

**Überschriften.** Jede Note ist in Abschnitte mit Überschriften gegliedert. Über die Überschriftenliste deines Screenreaders (bei VoiceOver der Rotor, bei NVDA und JAWS die Taste H) springst du von Abschnitt zu Abschnitt.

**Bilder.** Jedes Bild hat eine Beschreibung: die Banner über den Notes, Vortragsfolien, Standbilder und Gemälde. Bei Grafiken nennt die Beschreibung alle Zahlen, die im Bild stehen.

**Was vorgelesen wird.** Die Notes stecken voller Zeichen, die für das Auge Beiwerk sind und vorgelesen stören würden. Darum liest die Stimme eine eigene Fassung:

- Studien werden mit DOI belegt. Statt der langen Nummer hörst du den Namen und „(DOI)“, etwa „Lutz u. a. 2004 (DOI)“, der Link führt zur Studie.
- Zeitmarken wie 13:11 sind Knöpfe: „Video ab Minute 13“. Sie spielen das Video an der Stelle ab, über die du gerade liest.
- Der Verweispfeil heißt „siehe“, die Tilde vor einer Zahl „etwa“.
- Englische Zitate und Titel sind als Englisch ausgezeichnet, die Stimme wechselt dort die Aussprache. Erkannt wird das beim Bau der Seite. Ganz kurze Titel aus zwei, drei Wörtern liest sie weiter deutsch.

## Mit der Tastatur

| Taste | was sie tut |
|---|---|
| `Tab` | von Link zu Link, der erste führt zum Text |
| `⌘ K`, `Strg K` oder `/` | Suche im Bestand |
| `P` | das Video zur Note an der Stelle hören, wo du liest, noch einmal `P` schließt es |
| `←` `→` | bei offenem Video zehn Sekunden zurück oder vor |
| `Shift ←` `Shift →` | bei offenem Video zur vorigen oder nächsten Zeitmarke |
| `Esc` | schließt Video, Suche und Vorschau |

## Sehen

Oben rechts stehen drei Schriftgrößen und der Schalter für die dunkle Ansicht. Die Seite lässt sich auch mit dem Browser beliebig vergrößern, auf dem Telefon mit zwei Fingern. Kleine graue Schrift hat einen Kontrast von mindestens 4,5 zu 1, so wie es die Richtlinien für Barrierefreiheit (WCAG) verlangen.

Belege stehen leise im Text: klein und blass in einer Klammer, mit Autor, Jahr und Einordnung wie „Übersichtsarbeit“ oder „Preprint“. So bleibt der Satz vorn, und wer prüfen will, findet die Studie trotzdem mit einem Klick. Die DOI-Nummer erscheint, wenn man mit der Maus darüberfährt.

## Hören statt lesen

Jeder Browser kann die Seite vorlesen: Edge mit „Laut vorlesen“, Safari mit „Seite anhören“, Firefox und Chrome über die Leseansicht. Die Leseansicht von Firefox bekommt dieselbe Fassung wie ein Screenreader, ohne Nummern und Zeichen.

## Im Gespräch mit deinem Assistenten

Der bequemste Weg führt gar nicht über die Seite. Die Gedankenwelten lassen sich an Claude anschließen, an andere KI-Assistenten auch, und dann fragst du einfach im Gespräch, schriftlich oder gesprochen. Der Assistent holt die passenden Notes, nennt Quellen und Links, und im Sprachmodus liest er dir vor, was du hören willst. Keine Seite, durch die man sich tasten muss, keine Knöpfe.

**Einrichten, einmal und ohne Anmeldung:** In Claude unter *Einstellungen → Konnektoren* (englisch *Settings → Connectors*) einen Konnektor hinzufügen und die Adresse `https://mcp.gedankenwelten.org/mcp` eintragen. Danach steht der Zugang auf allen Geräten bereit, auch in der App auf dem Telefon. Für andere Assistenten steht die Anleitung auf der Seite [[MCP|MCP-Server]].

**Dann frag zum Beispiel:**

- „Was ist neu in den Gedankenwelten?“
- „Was wurde im letzten Monat über Demokratie geschrieben?“
- „Was sagt die Gedankenwelt zu Hannah Arendt?“
- „Lies mir das KI-Panorama vor.“
- „Welche Quellen nennen die Gedankenwelten zur Frage, ob Migration kriminell macht?“

### Lange Notes hören

Manche Notes dauern vorgelesen eine Dreiviertelstunde, und überfliegen kann man beim Hören nicht. Darum gibt der Zugang dem Assistenten mehr als den Text:

- **Erst die Gliederung.** Bittest du ihn, eine Note vorzulesen, nennt er zuerst, worum es geht, wie viele Abschnitte sie hat und wie lange jeder dauert. Dann fragt er, womit er anfangen soll. Du antwortest mit der Nummer („Abschnitt 4“) oder mit ein paar Worten aus der Überschrift („die Frage nach der Verantwortung“).
- **Ein Teil nach dem anderen.** Längere Abschnitte kommen in Teilen, in den Panoramen etwa Sachstand, Die Stimmen und Die Reibung. Nach jedem Teil sagt er, was als Nächstes kommt und wie lange es dauert, und fragt, ob er weitermachen soll.
- **Anhalten und weiterhören.** Sag „Stopp“, wann immer du willst. Später geht es mit „Lies weiter ab den Stimmen“ oder „ab dem dritten Absatz“ an der Stelle weiter.
- **Die Kurzfassung.** „Die Kurzfassung bitte“ bringt in etwa fünf Minuten, worum es geht, die schärfste Spannung jeder Frage und die Fragen zum Weiterdenken.
- **Belege ohne Zahlenkolonnen.** Beim Vorlesen bleiben die Sätze ganz. Von einem Beleg hörst du nur, was für einer es ist, etwa „Preprint“. Am Ende eines Teils sagt der Assistent, wie viele Belege dahinterstehen. „Welche Quellen stehen dahinter?“ bringt sie dir.
- **Genau oder frei.** Der Assistent erzählt gern mit eigenen Worten. „Lies wörtlich“ bringt den Text so, wie er in der Note steht.

Wer den Zugang schon vor dem 5. November 2026 eingerichtet hat, verbindet ihn einmal neu (trennen und wieder hinzufügen). Dann kennt der Assistent die neuen Möglichkeiten.

Die Antworten kommen von deinem Assistenten, mit seinen eigenen Worten. Wer es genau wissen will, lässt sich die Note selbst geben: Jede Antwort nennt den Link dazu. Notes zu schweren Themen tragen einen Hinweis auf kostenlose Hilfe, und der Assistent ist gebeten, ihn weiterzugeben.

## Was noch nicht geht

- **Der Gedankenraum** ist ein Raum zum Anschauen, gebaut in 3D. Für einen Screenreader bleibt er stumm. Jede Note, die dort hängt, gibt es auch als Text.
- **Der Stern** unter jeder Note zeichnet die Nachbarschaft als Bild. Die wichtigsten Verbindungen stehen auch als Liste daneben, unter „Verwandt“.
- **Die Videos** laufen im Player von YouTube. Wie gut der sich bedienen lässt, liegt nicht bei uns.

## Etwas hakt?

Dann sag es uns: über *Feedback* in der Fußzeile oder per Mail an [luc@gedankenwelten.org](mailto:luc@gedankenwelten.org). Am meisten hilft die Stelle, an der es hakt, und womit du liest. Wir können nicht jede Hürde selbst hören, also sind wir auf solche Hinweise angewiesen.

Besonders gern hören wir von Menschen, die mit Screenreader, Braillezeile oder Sprachassistent lesen. Was wir bisher gebaut haben, haben wir selbst ausprobiert, mit VoiceOver und im Sprachmodus eines Assistenten. Wie es sich anfühlt, wenn man jeden Tag so liest, wisst ihr besser. Erzähl uns, was trägt und was stört, wir bauen danach weiter.
