# Brandmauer in den Kommentarspalten — Daten und Methode

Offene Daten zur Spur [„Fällt die Brandmauer in den Kommentarspalten?“](https://gedankenwelten.org) auf
gedankenwelten.org. Jeder Befund der Spur soll sich nachprüfen lassen, ohne dem Schreiber glauben zu müssen.

## Was hier liegt

| Datei | Inhalt |
|---|---|
| `vorregistrierung.md` | Korpus, Codebuch, Hypothesen und Schwellen, festgelegt am 17.10.2026 vor der Kodierung, mit datierten Nachträgen |
| `auslegungsregeln.md` | 105 Regeln, die während der Kodierung entstanden; sie präzisieren das Codebuch, ändern es nicht |
| `codes.csv` | ein Code je Absatz, 1.919 Absätze |
| `auswertung.md` | die Tabellen der ersten Messung (Korpus, Halbjahre, H1–H4) |
| `nachrechnen.py` | rechnet die Kernzahlen aus `codes.csv` nach, nur Python-Standardbibliothek |

## codes.csv

| Spalte | Bedeutung |
|---|---|
| `id` | Kennung des Absatzes (Hash des Wortlauts) |
| `datum` | Tag der Presseschau; `datum_unsicher` = 1, wenn er nur aus dem Archiv-Zeitstempel stammt |
| `blatt` | die zitierte Zeitung, nach dem Entblinden vereinheitlicht |
| `quelle` | `dlf` (deutschlandfunk.de), `wayback-neu` und `wayback` (Internet Archive) |
| `fundstelle` | Link zur Presseschau-Seite; bei `wayback` nur der Archiv-Zeitstempel (die alten Adressen lösen nicht mehr sauber auf) |
| `afd`, `linke` | Haltung zum Umgang mit der Partei: `D` · `H` · `K` · `L1` · `L2`, `-` = kein Bezug |
| `symmetrie` | `S=` (gleichsetzend), `S≠` (unterscheidend), `-` |

**Codes:** D beschreibend · H die Abgrenzung halten · K Kritik an Wort, Ritual oder Wirkung der Brandmauer,
ohne Zusammenarbeit zu befürworten · L1 Mehrheiten mit Stimmen der Partei hinnehmbar · L2 Zusammenarbeit
befürwortet. Kodiert wurde die Stimme des Blatts, nicht zitierte Politiker. Im Zweifel galt der vorsichtigere
Code. Die genauen Grenzen stehen in `vorregistrierung.md` und `auslegungsregeln.md`.

## Was fehlt, und warum

- **Die Absatztexte.** Die Rechte liegen beim Deutschlandfunk und den Blättern. Über `fundstelle` und `blatt`
  findet man jeden Absatz im Original.
- **Ein unabhängiger zweiter Kodierer.** Kodiert hat Claude (Anthropic), verblindet: ohne Datum und Seitenkontext,
  in Zufallsreihenfolge. Die Zweitkodierung von 10 % (κ 0,91 auf der AfD-Achse) stammt vom selben Kodierer und misst
  darum Stabilität, keine Übereinstimmung. Ein menschlicher Zweitkodierer über eine Stichprobe läuft (Nachtrag 4);
  das Ergebnis wird hier nachgetragen.
- **Ein öffentlicher Zeitstempel der Vorregistrierung.** Sie wurde am 17.10.2026 in einem privaten Repository
  eingecheckt. Öffentlich nachvollziehbar ist sie ab ihrer ersten Veröffentlichung hier.

## Grenzen der Messung

Die Presseschau ist eine Auswahl der DLF-Redaktion mit dem Auftrag, das Spektrum abzubilden, keine Vollerhebung.
Vor dem 23.02.2023 stammen die Seiten aus dem Internet Archive und sind lückenhaft, darum werden nur Anteile
verglichen, nie absolute Zahlen. Online-Medien ohne Presseschau-Zitat fehlen ganz.

Lizenz: CC BY-SA 4.0, wie gedankenwelten.org.
