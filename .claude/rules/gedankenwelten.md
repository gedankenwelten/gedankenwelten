# Rules — Gedankenwelten

## Ordnerstruktur

```
Gedankenwelten/
  Denker/          ← Obsidian-Notes pro Denker/Quelle (.md)
  DenkerVita/      ← Ausführliche Biografie-Profile pro Person (.md)
  Transkripte/     ← Rohe Transkripte und VTT-Dateien (.txt, .vtt)
  Vipassana/       ← Goenka MP3s und Transkripte
  Zeitgeist/       ← Interviews & Vorträge zum Geist der Zeit (alle Spektren)
  Geistesblitz/    ← Grundsätzliches Wissen & Schöpferkraft (Wissenschaft, Philosophie, Psychologie, Technik)
  Kultur/          ← Land und Leute, gelebte Kultur — Reise- & Heimatberichte, das Fremde von innen
  Panorama/        ← Thematische Synthese-Notes (min. 3 Notes zum Thema)
  Gedanken/        ← Persönliche Notizen
  known-speakers.md   ← DenkerVita-Index mit Status (Stub / Vollanalyse)
  Quellen & Links.md  ← Index aller externen Quellen
```

- Neue Denker-Notes → `content/Denker/`
- Neue Zeitgeist-Notes → `content/Zeitgeist/`
- Neue Geistesblitz-Notes → `content/Geistesblitz/`
- Neue Kultur-Notes → `content/Kultur/`
- Neue DenkerVitas → `content/DenkerVita/` (angelegt von Humboldt)
- Neue Panoramas → `content/Panorama/` (manuell, on demand)
- Stil orientiert sich an bestehenden Notes (Frontmatter, Callouts, Wikilinks)

## Geistesblitz

Geistesblitz ist die Rubrik für **grundsätzliches Wissen und menschliche Schöpferkraft** — Wissenschaft, Philosophie, Psychologie, Technik. Notes, die die Welt erklären und das Außergewöhnliche am Menschen sichtbar machen: den Funken, der Erkennen und Erschaffen verbindet.

**Abgrenzung:**
- **Zeitgeist** → Geist der *Zeit*: tagesaktueller Diskurs, Politik, Gesellschaft, Interviews.
- **Denker** → das Denken *einer Person* in der Tiefe.
- **Geistesblitz** → das Wissen über die *Welt und den menschlichen Geist*: Forschungsstand, Wissenschaft, Erklärung — quellenbasiert, nicht an eine einzelne Stimme gebunden (z.B. Wissenschafts-Dokus, Erklärformate, Forschungsüberblicke).

**Wann hierher statt Zeitgeist?** Wenn der Kern eine zeitlose Frage über die Welt oder den Menschen ist („Können wir uns ändern?", „Wie entsteht Bewusstsein?") und nicht ein aktuelles Ereignis. Im Zweifel: Was überdauert das Jahr → Geistesblitz; was kommentiert das Jetzt → Zeitgeist.

**Frontmatter-Typ-Tag:** `geistesblitz` (statt `zeitgeist`). Sonst gilt die volle Note-Checkliste (Aufmacher-Callout, Sokrates-Fragen, Cross-Linking, `description:` + `aktualisiert:`). Faktencheck wie bei Zeitgeist, wenn empirische Claims im Spiel sind — bei Wissenschaftsthemen meist der Fall.

**Note-Stil:** wie eine Zeitgeist-Note aufgebaut (Sherlock-Faktencheck bei empirischen Claims), aber mit dem analytischen Anspruch einer Denker-Note (Konzepte als eigene Abschnitte, eigene Einordnung).

## Kultur

Kultur ist die Rubrik für **Land und Leute, wie man sie selten zu sehen bekommt** — gelebte Kultur, Alltag, das Fremde von innen. Notes, die ein Stück Welt erfahrbar machen: durch Reisende, die wirklich hinsehen, oder Einheimische, die ihre Heimat erzählen. Kein Postkarten-Bild, kein Diskurs *über* ein Land — das gelebte *Wie* eines Ortes, der Mensch im Konkreten.

**Abgrenzung:**
- **Zeitgeist** → der *Diskurs* über ein Land: Politik, Gesellschaft, aktuelle Lage, Interviews.
- **Denker** → das Denken *einer Person* in der Tiefe.
- **Geistesblitz** → *Wissen über* die Welt: Forschung, Erklärung, zeitlos.
- **Kultur** → das *gelebte Wie* eines Ortes: Alltag, Begegnung, Atmosphäre — erfahren und erzählt, nicht analysiert.

**Wann hierher?** Wenn der Kern eine Kultur *von innen* zeigt, statt sie zu kommentieren. Ein Reisevideo aus dem Jemen, ein Einheimischer über sein Dorf, der Alltag auf einem Markt → Kultur. Eine Analyse der jemenitischen Politik → Zeitgeist.

**Frontmatter-Typ-Tag:** `kultur` (statt `zeitgeist`). Region als Land-Tag (`jemen`, `iran` …) plus `reise`/`alltag`/`tradition` etc.

**Note-Stil — leicht & erzählend (bewusst anders als die analytischen Rubriken):**
- **Die Menschen zuerst, dann die Landschaft.** Der Kern jeder Kultur-Note sind die *Begegnungen* — wie der Reisende den Menschen begegnet und sie ihm. Die Landschaft wird ausgemalt (sie darf, sie soll), aber sie ist die Bühne; die Menschen sind das Stück. Gerade die kleinen, offenen Begegnungen (Kinder, Gastgeber, Fremde am Weg) bekommen Raum und Gesicht.
- **Die Wahrnehmung des Reisenden ist essenziell — sie ist der rote Faden.** Reisende wie Hans Maggi *reflektieren* fortlaufend, wie sie die Menschen wahrnehmen und was die Begegnungen mit ihnen machen (Staunen, Erschöpfung, Zugehörigkeit, die ehrliche Selbstkorrektur „mein Bild ist verzerrt, weil ich der exotische Gast bin"). Diese O-Ton-Wahrnehmungen sind kein Beiwerk, sondern das Herz der Rubrik — stark einweben, in der Stimme des Reisenden. (Trägt durch ganze Reisereihen — Weltreise, Afrika.)
- **Bilder aus dem Gesehenen.** Bei Standard-YouTube-Lizenz (kein Embed) trotzdem Frames ziehen und *selbst anschauen* (yt-dlp low-res → ffmpeg an den Transkript-Zeitstempeln → Read), um Landschaften und Gesichter aus dem Bild zu malen, nicht nur aus dem Wort. → `pipeline.md`.
- **Erzählen, nicht zergliedern.** Den Ort und die Menschen *erzählen* — eine Reise mit Atem, kein Stapel von Konzepten. Die Haltung von `gedankenpoesie` ist hier Default-nah, nicht Kür. Die Stimme darf *driften* (knapp-kinohaft bei Abenteuer, warm-staunend bei Begegnung, lyrisch bei Landschaft) — kein fixer Skill, eine gemischte Palette.
- **Bildreich.** Standbilder aus dem Video einbetten (→ `pipeline.md`, Schritt „Standbilder extrahieren") — bei Kultur fast immer sinnvoll, das Visuelle *ist* der Inhalt. Nur bei freier Lizenz.
- **Kein Sherlock-Faktencheck.** Gelebte Erfahrung ist kein überprüfbarer Claim (wie bei spirituellen Notes, → `pipeline.md`). **Ausnahme:** Macht der Reisende harte Behauptungen über Geschichte/Zahlen/Politik des Landes, wird *nur das* gezielt eingeordnet — nie die Erfahrung selbst.
- **Aufmacher-Callout** (`> [!abstract] Worum es geht`) und **`description:` + `aktualisiert:`** bleiben Pflicht (speisen das Startseiten-Journal).
- **Sokrates-Fragen** ja, aber **kontemplativ statt konfrontativ**: nicht „wo bricht das System", sondern „was erkenne ich über mein eigenes Zuhause, wenn ich dieses fremde sehe?".
- **Quellen & Links.md**, **Journal**, **Cortex-Log**, **Cross-Linking**, **Deploy** wie bei jeder Note.

**Migration:** Bestehende Zeitgeist-/Denker-Notes mit zeitlos-wissenschaftlichem Kern können hierher umziehen — Datei nach `content/Geistesblitz/` verschieben, Typ-Tag `zeitgeist`/`denker` → `geistesblitz` ändern, bare Wikilinks bleiben (Quartz löst über Dateiname auf), **path-qualifizierte Backlinks** (`[[Denker/…]]`) im ganzen Vault nachziehen, danach Eintrag in `Gedankenwelten.md` umhängen. → Skill **`/geistesblitzumzug`** macht den ganzen Ablauf (10 Vorschläge → Auswahl → vollständiger Umzug inkl. RAG + Deploy).

## Panorama

Panoramas sind thematische Synthese-Seiten — kein Nachrichtenindex, sondern eine verdichtete Perspektive auf ein Thema, das in mehreren Notes auftaucht.

**Wann anlegen:** Manuell, wenn mindestens 3 Notes dasselbe Thema aus verschiedenen Winkeln beleuchten. Nie automatisch bei jeder neuen Note.

**Zweiter Weg (seit 07/2026):** Panorama verhält sich zu den Gedanken wie Zeitgeist zu den Denkern — der Blick über *viele Fälle* statt ein einzelner Gedanke in der Tiefe. Ein Panorama darf darum auch aus eigener Recherche/Gespräch entstehen (Fälle aus der Welt nebeneinander gehängt, z.B. [[Panorama/Gekaperte Zeichen]]), nicht nur aus bestehenden Notes. Autoren-Tag bleibt Pflicht; die Struktur darf dann erzählender sein (persönlicher Einstieg statt Problem/Ursachen/Lösungen).

**Frontmatter:**
```yaml
---
title: "[Thema]"   # kein „Panorama —"-Präfix: die Rubrik rahmt schon, der Titel braucht keinen zweiten Rahmen (seit 07/2026)
tags:
  - panorama
  - [thema-tags]
erstellt: YYYY-MM-DD
---
```

**Struktur:** Kurze Einleitung (Kernproblem) · Perspektiven (je Winkel ein Abschnitt, mit verlinkten Notes) · Offene Fragen · Tabelle aller verlinkten Notes

**Pflege:** Panoramas sind Snapshots — stabil nach Erstellung. Neue Notes verlinken *darauf*, aber das Panorama wird nur bei Bedarf aktualisiert. Keine automatische Pflicht-Aktualisierung bei neuen Notes.

**Dritte Spielart: das wachsende Panorama (seit 26.09.2026).** Frontmatter `panorama-art: wachsend`. Statt Perspektiven stehen **offene Fragen** als `##`-Abschnitte (Beispiel: [[Panorama/Wie kann Demokratie funktionieren]]). Jede Frage trägt:
- den **Sachstand** — was man weiß, Forschung mit DOI inline, Fälle; ehrlich vermerkt, wo er noch fehlt
- **Die Stimmen** — je Stimme *ein* Satz zur Position, Name als Sprung auf den genauen Abschnitt (`[[Note#Überschrift|Name]]`); **6–8 sichtbar**, die am stärksten gegeneinander stehen, der Rest eingeklappt in `<details><summary>Weitere Stimmen (n)</summary>`
- **Die Reibung** — ein `> [!question]`, das die schärfste Spannung zwischen den Stimmen als Frage stellt

Am Ende `## Nachbesprechungen, die hierher führen` (Tabelle: Datum · Note · vertieft) — das ist der Wachstumsmechanismus. Gespeist wird es aus den **Nachbesprechungen** neuer Notes (→ `gedankenwelt`-Skill, Schritt 5d); anders als der Snapshot wird es also bei jeder passenden Note fortgeschrieben, und `aktualisiert:` wird dann gebumpt. **Streng auf die eine Frage zuschneiden** — was nur verwandt ist, wird verlinkt, nicht aufgenommen, sonst wächst es in die Breite statt in die Tiefe.

## DenkerVita

DenkerVitas sind vollwertige, öffentliche Profile — sichtbar auf gedankenwelten.org und im Cortex-Graph.

> [!important] Immer anlegen, sobald eine Note eine Person behandelt
> Eine DenkerVita ist **kein Werk-Nachweis**, sondern ein Fenster zum *Menschen* — man will über die
> Person etwas erfahren können. Darum gilt: Behandelt eine Note eine konkrete Person, bekommt sie eine
> Vita — **auch Augenzeugen, Aktivisten, Praktiker ohne publiziertes Werk**. Nicht „kein Buch → keine
> Vita". Die *Struktur* wird an die Person angepasst (siehe unten), die Vita selbst ist Pflicht.

**Frontmatter:**
```yaml
---
title: <Name> — DenkerVita
tags: [denker-vita, <thema>, <herkunft>]
---
```

**Struktur:** Biografie · Bücher & Publikationen (mit Kauflinks) · Empfehlenswerte Videos & Vorträge · Kernthesen · Politische Einordnung (wenn relevant) · Verbindungen zu anderen Denkern (via Montaigne) · Gedankenwelten-Notes

**Struktur anpassen, wenn kein klassisches Werk vorliegt** (Augenzeuge/Aktivist/Praktiker): „Bücher & Publikationen" durch **„Öffentliche Arbeit, Kanäle & Engagement"** ersetzen (Organisationen, YouTube/Instagram, Website/Spenden, Vorträge — mit Links). Biografie, Kernthesen, Politische Einordnung, Verbindungen, Cortex-Notes bleiben. Keine genialokal-Links erfinden, wo es keine Bücher gibt.

**Link in Notes:** Jede Note die eine Person behandelt, bekommt am Ende des Speaker-Abschnitts:
```
→ [[DenkerVita/<Name>|DenkerVita]]
```

**Workflow:** Humboldt erstellt die Vita → Montaigne befüllt "Verbindungen zu anderen Denkern"

## Deploy-Workflow

Nach dem Erstellen/Ändern einer Note: Commit, Push und Cortex-Wiki-Build triggern.

```bash
cd <vault>/
git add -A && git commit -m "<typ>: <beschreibung>"
git push
ssh <server> "cd ~/services/cortex && bash scripts/pull-and-rebuild.sh"
```

Danach die Note im Browser öffnen:

```bash
open "<dein-wiki>/<Pfad-ohne-.md>"
```

## Pflicht-Checkliste: Neue Note abschließen

Diese Schritte sind nach jeder neuen Zeitgeist- oder Denker-Note zwingend:

1. **Frontmatter — `description:` + `aktualisiert:`**: Jede Note bekommt ein `description:` (ein philosophischer Einzeiler, ~120–180 Zeichen, der den Kern fängt — kein „In diesem Vortrag…") **und** `aktualisiert: <heute>` (DD.MM.YYYY oder ISO). Beide speisen das öffentliche Startseiten-Journal von gedankenwelten.org. → siehe „Startseiten-Journal" unten.
2. **Aufmacher-Callout (ganz oben)**: Direkt unter der `# Überschrift`, **vor** der `Quelle:`-Zeile, steht ein `> [!abstract] Worum es geht`-Callout mit 2–4 Sätzen (mehr, wenn nötig) — *worauf lässt man sich ein?* Orientierung vor dem Lesen. Die erste Zeile entspricht im Kern dem `description:`.
3. **Sokrates-Fragen**: 2–4 inline `> [!question]`-Callouts + `## Weiterdenken` mit 3–5 übergreifenden Fragen. → Sokrates-Skill aufrufen.
4. **Cross-Linking**: Alle bestehenden Notes in `content/Zeitgeist/` und `content/Denker/` auf thematische Überschneidungen prüfen (Glob + Read). Relevante Verbindungen **bidirektional** einpflegen. ⚠️ **`aktualisiert:` der verlinkten Altnotes dabei NICHT anfassen** — sonst werden sie fälschlich ins Journal hochgespült.
5. **Quellen & Links.md**: Eintrag für die neue Quelle anlegen.
6. **Journal**: Eintrag in `journal/YYYY-MM.md` (neuester Monat) — Einzeiler-Teaser + Beschreibung. Wenn erster Eintrag des Monats: neue Datei anlegen.
7. **index.md (Cortex-Wiki)**: Journal-Teaser auf der privaten Startseite aktualisieren (max. 3–5 neueste). *(Das öffentliche gedankenwelten.org-Journal entsteht dagegen automatisch beim Sync — kein manueller Schritt.)*
8. **Cortex-Log**: `note-created`-Eintrag in `Cortex-Log.md` (append-only).
9. **Wandspruch**: `raetsel:` im Frontmatter — der geheimnisvolle Satz über dem Bild im Gedankenraum (/raum), für Note und neue Vita. → `.claude/skills/gedankenpoesie/references/wandspruch.md`
10. **Deploy**: Commit + Push + Build triggern — Note im Browser öffnen.

Ohne diese Schritte gilt die Note als unvollständig.

> [!tip] Kür (optional, nach der Substanz): Stimme geben — `gedankenpoesie`
> Nach der Pflicht-Checkliste darf eine Note in eine eigene **Schreibstimme** gehoben werden — der Skill
> **`/gedankenpoesie`** (das `gedankenart` für die Sprache). **Default ja für `Gedanken`** (kehrt zur
> Poesie zurück), Angebot für die analytischen Rubriken. Stimme ändert nur das *Wie*, nie das *Was*; schon
> gestimmte Notes (Luc-Texte, Pascal-Gedanken) bleiben unangetastet. → `.claude/skills/gedankenpoesie/`.

## Startseiten-Journal (gedankenwelten.org)

Die öffentliche Startseite zeigt unter „Was zuletzt gedacht wurde" automatisch die jüngsten Notes — gruppiert nach Rubrik (frischeste oben), sämtliche der letzten 7 Tage, mindestens 10. Erzeugt von `.claude/scripts/build_journal.py` (läuft im Sync), das zwischen den HTML-Kommentar-Markern `JOURNAL:START` … `JOURNAL:END` in `content/index.md` schreibt.

**Arbeitsteilung (Daten vs. Intelligenz):**
- *Skript* macht das Stumpfe & Zuverlässige: Selektion (7-Tage-Fenster, Soft-Cap 8/Rubrik + Überlauf-Link), Sortierung, Montage. Sortiert nach `aktualisiert:` (Fallback: Git-Erstellungsdatum) — **immun gegen Backlink-Edits**.
- *KI/Skills* liefern das Urteil: `description:` als Teaser (von `aristoteles` bei Erstellung), `aktualisiert:`-Bump bei echter Vertiefung (von `heraklit`).

`aktualisiert:` = Datum der letzten *inhaltlichen* Änderung. Nur bumpen, wenn wirklich Substanz dazukam — **nie** bei reinem Cross-Linking. So floatet eine ausgebaute Panorama-/Gedanken-Note bewusst hoch, eine bloß verlinkte nicht. Manuell neu bauen: Skill `/gedankenwelten-update`.

## Sokrates-Fragen: Zum Weiterdenken anregen

Jede Note bekommt Fragen — verteilt im Text UND gesammelt am Ende. Inspiriert von Sokrates' Maieutik: nicht belehren, sondern Denkbewegung auslösen. **Der Sokrates-Skill (`sokrates`) ist die Referenz für Fragetypen, Qualität und Format.**

### Inline-Fragen (nach wichtigen Sektionen)

Nach substanziellen `###`-Abschnitten kann ein `> [!question]`-Callout stehen — 1–2 Fragen die sich direkt aus dem Gelesenen ergeben:

```markdown
> [!question] Weitergedacht
> Wenn das Gehirn primär Vorhersagen trifft — *kann es dann überhaupt überrascht werden, oder simuliert es auch das?*
```

**Wann inline?** Nicht nach jedem Abschnitt (das ermüdet), sondern dort wo:
- Eine These besonders provokant oder kontraintuitiv ist
- Ein offensichtlicher Widerspruch im Raum steht
- Der Sprecher eine Konsequenz nicht zu Ende denkt

**Frequenz:** 2–4 inline-Fragen pro Note (bei 6–8 Abschnitten).

### `## Weiterdenken` — Abschluss-Abschnitt (Pflicht)

Am Ende jeder Note, nach `## Verbindungen`, steht:

```markdown
---

## Weiterdenken

> [!question] Was Sokrates vielleicht gefragt hätte
> - Wenn [Kernthese] stimmt — *was folgt daraus für [konkreten Lebensbereich]?*
> - [Sprecher] sagt [X] — aber widerspricht das nicht [Y aus anderer Note]?
> - Wem nützt es, wenn wir [Annahme] für selbstverständlich halten?
> - Was wäre das stärkste Gegenargument zu [zentrale These]?
```

**Regeln für gute Fragen:**
- Nicht rhetorisch (echte offene Fragen, auf die man nicht sofort antworten kann)
- Mindestens eine Frage die die Kernthese *herausfordert*, nicht bestätigt
- Gelegentlich Brücken zu anderen Denkern schlagen (via `[[Wikilink]]`)
- 3–5 Fragen, keine davon trivial oder googlebar
- Zum eigenen Schreiben einladen (→ neue Gedanken-Note)

### Sektions-spezifische Anpassung

| Sektion | Inline-Fragen | Weiterdenken-Stil |
|---|---|---|
| Zeitgeist | Nach kontraintuitiven Claims | Politisch-praktisch: *Was bedeutet das für uns?* |
| Denker | Nach Kernkonzepten | Philosophisch: *Wo bricht das System?* |
| Panorama | Nach Spannungsfeldern | Synthetisch: *Was fehlt in diesem Bild?* |
| Gedanken | Sparsam (ist schon persönlich) | Selbstreflexiv: *Was übersehe ich?* |

---

## Zeitgeist-Notes: Faktencheck

Jede Zeitgeist-Note bekommt einen Faktencheck-Abschnitt:

| Callout | Bedeutung |
|---|---|
| `> [!success] Bestätigt` | Claim ist durch Quellen belegt |
| `> [!warning] Vereinfacht / Nicht eindeutig belegt` | Claim ist grob richtig, aber verzerrt oder unvollständig |
| `> [!danger] Falsch` | Claim ist faktisch nicht haltbar |

Klare Ungenauigkeiten werden auch im Fließtext mit `*(Faktencheck: vereinfacht)*` bzw. `*(Faktencheck: falsch)*` markiert.

> [!important] Wissenschaft ist Kern-Säule (→ `haltung.md`, „Die zweite Säule")
> Ist ein Claim **empirisch** — Zahl, Wirkung, Ursache, Aussage aus Wissenschaft/Medizin/Psychologie —, wird
> er gegen die **Forschung** geprüft, nicht nur gegen die Presse. Standard-Werkzeug ist
> `.claude/scripts/wiss_search.py` (OpenAlex · Semantic Scholar · Europe PMC; auch der Skill `/galilei` und
> der Agent Sherlock nutzen es). Ein belegtes Paper gehört mit **DOI** in den `[!success]`-/`[!warning]`-Callout,
> samt Solidität (Meta-Analyse > Einzelstudie > Preprint) — nicht nur ein Web-Link. Das gilt rubrik-übergreifend
> (Zeitgeist, Denker, Geistesblitz), überall wo empirische Ansprüche im Spiel sind. Andreas ist Fan der
> Wissenschaft — sie ist die zweite Säule neben Vipassana und im Core immer mitzudenken.
