---
name: aristarch
description: "Prüft eine bestehende Gedankenwelten-Note oder DenkerVita auf Fehler — Zitate gegen das Transkript, Namen, Zahlen, Daten, Studien, unsere eigenen Sätze, Aussagen über lebende Personen, Links. Nur Fehler, nicht vertiefen (das ist /heraklit). Liefert eine Befundliste, korrigiert erst mit Andreas' Ja. Typisch als zweiter Durchgang nach /gedankenwelt. Trigger — '/aristarch', 'aristarch', 'prüf die note', 'review', 'auf fehler prüfen', 'gegenlesen'."
---

# Aristarch — Vers für Vers

> Aristarchos von Samothrake leitete um 150 v. Chr. die Bibliothek von Alexandria und prüfte
> Homer Vers für Vers. Was er für unecht hielt, strich er nicht, er setzte einen Obelos daneben.
> Im Deutschen heißt ein strenger Kritiker bis heute „Aristarch“.

Aristarchs Aufgabe: **eine Note auf Fehler prüfen, sonst nichts.** Kein neuer Abschnitt, keine
schönere Stimme, keine Nachbesprechung. Nur die Frage: *Stimmt, was da steht?*

Anlass (25.10.2026): Über jeder Note steht seither offen „mit KI geschrieben“, und auf
`/Wie-die-Notes-entstehen` steht ehrlich, dass nicht jede Note Satz für Satz gelesen wurde.
Andreas will darum nach einem `/gedankenwelt`-Lauf oder für eine beliebige alte Note sagen können:
„prüf die auf Fehler.“ Die Fälle Oetting, Marcant, Arendt und Koschi haben gezeigt, dass auch
gelobte Notes echte Fehler tragen — beim Sprecher **und bei uns**.

---

## Abgrenzung

| Skill | Frage |
|---|---|
| `/aristarch` | Stimmt, was da steht? |
| `/heraklit` | Was fehlt noch, was liegt verborgen? |
| `/moin` 3a („Nachschärfen“) | Prüfen **und dann** das volle Programm (Stimme, Sokrates, Nachbesprechung) |
| Sherlock | Faktencheck fremder Behauptungen mit Quellen — Aristarch kann ihn rufen |
| `/cortex-lint` | Widersprüche **zwischen** Notes |

Fällt beim Prüfen auf, dass eine Note dünn oder veraltet ist: **notieren, nicht ausbauen.** Am Ende
ein Satz „wäre ein Fall für /heraklit“ oder „braucht *Was seither geschah*“.

**Modernisierung immer mit ansprechen (seit 25.10.2026).** Andreas: „wir modernisieren ja gleich auch
immer.“ Darum gehört zu jeder Befundliste ein Block **Modernisierung**: was der Note gegenüber dem
heutigen Standard fehlt (→ Schritt 3a unten). Die Vertiefung selbst bleibt bei /heraklit, aber die
Standard-Bausteine werden im selben Durchgang nachgezogen. **Fehlt ein Banner, direkt `/gedankenart`**,
ohne erst zu fragen.

---

## Ablauf

### 1. Note und Quelle finden

- Note per Pfad, Titel oder URL (gedankenwelten.org-Slug → Datei: `Gedankenwelten/<Rubrik>/<Name>.md`).
- **Transkript:** `Quelle:`-Zeile der Note, `content/Quellen & Links.md`, `content/Transkripte/`.
  **Bei Namen die VTT nehmen, nicht die TXT** (die TXT glättet Eigennamen). Fehlt das Transkript, mit
  yt-dlp neu ziehen (→ `rules/pipeline.md`).
- **DenkerVita:** keine Transkript-Quelle. Geprüft wird an Primärquellen (Lehrstuhl-/Institutsseite,
  DNB, Verlag, eigene Website, seriöse Presse). Wikipedia ist ein Wegweiser, kein Beleg.

**Bekannte Muster zuerst:** `python3 .claude/scripts/fehler_register.py auswertung` zeigt, welche
Fehler bisher am häufigsten waren, vor allem unsere eigenen und ihre Ursachen. Danach gezielt suchen.

### 2. Durchgehen — in dieser Reihenfolge

1. **Zitate.** Jedes wörtliche Zitat gegen das Transkript: Wortlaut, **Sprecher** (Interviewer ≠
   Gast, Publikumsfrage ≠ Antwort), Zeitmarke. Paraphrasen in Anführungszeichen sind ein Fehler.
2. **Namen, Zahlen, Daten, Zuordnungen.** Wer hat was wann gesagt, getan, gegründet, geschrieben?
   Wer war beschimpft, ausgestiegen, verurteilt (Oetting: der Vater, nicht Brandt; Marcant: Felix
   stieg aus, nicht Marcant)?
3. **Studien und empirische Claims.** Gegen die Forschung, nicht die Presse:
   `python3 .claude/scripts/wiss_search.py "…"`. Jeder DOI:
   `python3 .claude/scripts/doi_pruefung.py --note "<pfad>"` (Exit 1 = Phantom-DOI, Rücknahme oder **fremdes Paper**: das Zitat nennt Autoren, die nicht zum DOI gehören).
   Nie einen DOI aus dem Gedächtnis.
4. **Unsere eigenen Sätze** — hier liegen die gefährlichsten Fehler, weil niemand sie dem Sprecher
   zuschreiben kann: Aufmacher-Callout, `description:`, Einordnungen, Faktencheck-Callouts (stimmt
   das Urteil „falsch/vereinfacht“ selbst?), Nachbesprechung, Bildunterschriften, Wandspruch.
   **Verbindungssätze** gegen die Kernthese der verlinkten Note lesen: Wird dort eine Stimme zur Stütze
   gemacht, die in ihrer eigenen Note das Gegenteil vertritt, oder ein Organisationszusammenhang behauptet,
   den keine Note belegt? (Aly, Arendt, NIUS in der CPAC-Note, 28.10.2026; Regel für Montaigne →
   `agents/montaigne.md`, „Die verlinkte Stimme nicht verbiegen“.)
   **Belegverben** („belegt“, „weist nach“, „dokumentiert“) nur, wo ein `[!success]` sie trägt — der
   Schnellcheck steht im Aristoteles-Skill unter „Belegverben gehören dem Faktencheck“.
   **Steigerungen** („der genaueste“, „als Einziger“, „vollständig“, „gilt als“) ebenso — Schnellcheck im
   Aristoteles-Skill unter „Steigerungen tragen Beweislast“.
5. **Lebende Personen** (Persönlichkeitsrecht, → Abmahnrisiko): Jede **Tatsachenbehauptung** über
   einen lebenden Menschen braucht einen Beleg; Meinung muss als Meinung erkennbar sein. Verdachts-
   äußerungen nur als solche, mit Quelle. Mitgliedschaften, Strafverfahren, Ämter, Zitate besonders
   genau („Linken-Mitglied statt parteilos“, Der Dara, 23.10.).
6. **Links.** Wikilinks: `python3 .claude/scripts/check_links.py` (oder gezielt die Note).
   Externe Links: `python3 .claude/scripts/link_pruefung.py --note "<pfad>"` (über den Pi, YouTube per oEmbed).
   Zeitstempel-Links springen an die richtige Stelle? Externe Links leben noch?
7. **Bilder.** Standbilder nur aus frei lizenzierten Videos, mit Lizenzangabe; keine Screenshots aus
   Filmen und Serien großer Rechteinhaber.

### Maßstab (aus `rules/pipeline.md`, Sherlock-Leitlinien)

- **Transkriptionsfehler** (vertauschte Zahlen, phonetische Verwechslung, falsch geschriebener Name):
  **still korrigieren**, nicht als Befund aufblasen — nur in der Liste als ⚪ nennen.
- Kleine Nuancen ohne strategischen Wert sind kein Fehler. Interessant ist, was dem Sprecher nützt
  und nicht hält — und was **wir** verzerrt haben.
- **Spirituelle/kontemplative Notes:** Interpretationen kanonischer Texte und Praxisbeschreibungen
  nicht flaggen; nur Zahlen, Daten, historische Zuordnungen.
- Den Sprecher ernst nehmen: Was sagt er *tatsächlich* (mit seinen eigenen Einschränkungen)?

### 3. Befundliste

Erst die Liste, dann die Hand. Format:

| # | Stelle | Steht da | Stimmt | Beleg | Schwere |
|---|---|---|---|---|---|
| 1 | „## Die Wahrheit“, 2. Absatz | „…“ | „…“ | Transkript ▶ 12:34 / DOI / URL | 🔴 |

**Schwere:**
- 🔴 **falsch** — sachlich nicht haltbar, oder Zitat falsch zugeordnet
- 🟠 **ungenau** — grob richtig, aber verzerrt; erzeugt einen falschen Eindruck
- 🟡 **unbelegt** — kann stimmen, steht aber ohne Beleg da
- ⚖️ **riskant** — Tatsachenbehauptung über eine lebende Person ohne tragfähigen Beleg
- ⚪ **Kleinkram** — Transkriptions-/Tippfehler, Zeitmarke daneben, toter Link

Darunter in zwei Sätzen: **Gesamturteil** (trägt die Note?) und was außerhalb von Aristarchs Auftrag
auffiel (dünn → /heraklit, veraltet → *Was seither geschah*).

### 3a. Modernisierung — was fehlt gegenüber heute?

Kurz abhaken und in der Antwort nennen, dann im selben Durchgang nachziehen:

```bash
f="<pfad>"; for k in "assets/.*banner" "^description:" "^raetsel:" "\[!abstract\]" "^## Weiterdenken" "\[!question\]" "^stimme:"; do printf "%-20s %s\n" "$k" "$(grep -c "$k" "$f")"; done
```

- **Banner** fehlt → `/gedankenart` (direkt, Andreas 25.10.2026)
- **`description:`**, **Aufmacher-Callout** `> [!abstract] Worum es geht`, **Wandspruch** `raetsel:`
  (→ `rules/gedankenwelten.md`, Pflicht-Checkliste)
- **Sokrates-Fragen** (2–4 inline, `## Weiterdenken`), wo sie fehlen
- **Zeitgeist:** `## Was seither geschah` mit Stand-Datum (→ `/moin` 3a)
- **Vita:** echte Videos statt Suchlinks, Werke mit ISBN, Notes-Liste aus dem Bestand, `raetsel:`
- Kommt Substanz dazu (Was seither geschah, neue Abschnitte), wird `aktualisiert:` gebumpt;
  bei reiner Korrektur und bloßen Standard-Bausteinen (Banner, Wandspruch, description) nicht.

Bei vielen Behauptungen gegen externe Quellen: **ein** Sherlock-Agent mit gebündeltem Auftrag
(Opus, Haushalt: höchstens 4 Agenten, `rules/routing.md`). Bei einer Vita **ein** Humboldt-Agent zum
Prüfen an Primärquellen. Zitate gegen das Transkript liest die Hauptinstanz selbst.

### 4. Korrigieren — erst mit Andreas' Ja

Andreas sagt „alles“, „nur 🔴“ oder „1, 3, 5“. Sagt er von vornherein „korrigier direkt“, gilt das
für diesen Lauf.

- **Fehler des Sprechers:** bleibt im Text, was er sagt; dazu Faktencheck-Callout und ein Marker im
  Fließtext, der in wenigen Worten sagt, **was** nicht stimmt, mit Pfeil:
  `*(das Urteil von 2023 sieht vor allem die Berkut → [[#Faktencheck|Faktencheck]])*` —
  das Urteilswort gehört in den Callout, nicht in den Fließtext.
- **Unser Fehler:** einfach richtigstellen. Bei einem Fehler, den Leser schon gelesen haben können und
  der Gewicht hat, im Faktencheck oder am Ende eine kurze offene Korrekturnotiz (`> [!note] Korrigiert
  am TT.MM.JJJJ: …`) — so, wie die Seite es verspricht: „Wir korrigieren schnell und offen.“
- **⚖️ riskant:** belegen oder entschärfen (als Einschätzung kennzeichnen, mit Quelle) oder streichen.
  Im Zweifel streichen.
- **`aktualisiert:` NICHT bumpen** — Korrekturen sind keine Vertiefung (`rules/gedankenwelten.md`).
- **Querprüfen (seit 26.10.2026):** Jede inhaltliche Korrektur mit ein, zwei Stichwörtern in der
  Nachbarschaft suchen — in der Note außerhalb des Faktenchecks, in allen Backlinks, in den verlinkten
  Vitas. Verbindungssätze altern still: Die Lavender-Korrektur stand oben in der Grenzgänger-Note, ein
  Verbindungssatz weiter unten behauptete noch das Alte, und die Varoufakis-Note trug einen Fehler
  derselben Art. Jeden Treffer beurteilen (alte Behauptung, Korrektur oder nur das Wort?), Fundstellen
  in fremden Notes ohne Bump mitkorrigieren und ins Register.
  ```bash
  python3 .claude/scripts/korrektur_quer.py --note "$NOTE" "Lavender" "Ziele identifiz"   # --bestand: ganzer Ordner
  ```
- Vor dem Deploy `doi_pruefung.py --note`, falls DOIs angefasst wurden, und immer
  `link_pruefung.py --note` (tote Links → Exit 1; „gesperrt“ heißt Paywall — Herkunft prüfen).

### 5. Ins Fehler-Register

Jeder Befund eine Zeile, auch die des Sprechers und der ⚪-Kleinkram, auch was (noch) nicht korrigiert
wurde (`--offen`). Andreas, 25.10.2026: „vielleicht erkennen wir wiederkehrende vermeidbare fehler,
die auf dauer passieren.“ Ein Fehler wird korrigiert, ein **Muster** wird an der Quelle abgestellt:
als Regel dort, wo es entsteht (Skill, Pipeline-Schritt, Prompt), nicht als Nachlauf.

```bash
python3 .claude/scripts/fehler_register.py eintragen --note "$NOTE" \
  --schwere rot|orange|gelb|riskant|klein \
  --kategorie zitat-wortlaut|zitat-sprecher|zeitmarke|name|zahl|datum|zuordnung|studie-doi|eigene-einordnung|faktencheck-urteil|lebende-person|veraltet|link|bild|transkription|sonstiges \
  --urheber sprecher|wir|transkript \
  --ursache paraphrase-als-zitat|interviewer-verwechselt|txt-statt-vtt|aus-gedaechtnis|sekundaerquelle|zusammengezogen|zu-glatt-formuliert|veraltet|unbekannt|sonstiges \
  --herkunft pipeline|altbestand|vertiefung \
  --was "was dastand, ein Satz" --korrektur "was jetzt dasteht, ein Satz"
```

- `--urheber wir` heißt: Der Fehler stammt aus unserem Text, nicht aus dem Mund des Sprechers.
  Nur dann zählt `--ursache`, und genau dort liegt das Vermeidbare.
- `--herkunft pipeline` bei einer frischen Note aus `/gedankenwelt` (der zweite Durchgang, für den
  Aristarch gebaut ist), `altbestand` bei alten Notes.
- Zeigt `auswertung` bei einer Ursache **„← Muster“** (≥ 3), in der Antwort an Andreas einen
  Vorschlag machen, wo die Regel hingehört — umgesetzt wird erst mit seinem Ja.

### 6. Abschluss

```bash
NOTE="Gedankenwelten/<Rubrik>/<Name>.md"
# RAG neu einlesen (Response ist ein JSON-Array)
python3 -c "
import json,sys
p=sys.argv[1]; print(json.dumps({'path': p, 'content': open(p).read(), 'media_type': 'text'}))
" "$NOTE" | curl -s --max-time 420 -X POST "<dein-rag-server>/webhook/ingest-gedankenwelten" \
  -H "Content-Type: application/json" -d @- | head -c 200

git add "$NOTE" .claude/data/aristarch/fehler.jsonl && git commit -m "aristarch: <Name> — <n> Fehler korrigiert" && git push
<vault>/.claude/scripts/sync-from-cortex.sh      # öffentlich (gwship läuft mit)
```

**Cortex-Log** (neueste oben):

```markdown
## [TT.MM.JJJJ] note-updated | Aristarch: <Autor — Titel>

**Note:** [[<Pfad ohne .md>]] · ohne Bump
**Befunde:** 🔴 n · 🟠 n · 🟡 n · ⚖️ n · ⚪ n — korrigiert: <welche>
**Wichtigstes:** <ein, zwei Sätze: was stand da, was stimmt>
```

Kein Journal-Eintrag für eine reine Korrektur — es sei denn, ein Fehler hatte Gewicht.

---

## Checkliste

- [ ] Transkript (VTT bei Namen) bzw. Primärquellen bei der Vita
- [ ] Zitate · Namen/Zahlen/Daten · Studien/DOIs · unsere Sätze · lebende Personen · Links · Bilder
- [ ] Befundliste mit Schwere, Gesamturteil
- [ ] Modernisierung angesprochen und nachgezogen (Banner → `/gedankenart`, description, Aufmacher, raetsel, Sokrates, Was seither geschah)
- [ ] Korrekturen nach Andreas' Ja, ohne `aktualisiert:`-Bump
- [ ] Jede Korrektur quergeprüft (`korrektur_quer.py`): Note, Backlinks, Vitas
- [ ] `link_pruefung.py --note` → Exit 0
- [ ] Jeder Befund ins Fehler-Register (`fehler_register.py eintragen`), Muster ansprechen
- [ ] RAG, Commit (Note + `.claude/data/aristarch/fehler.jsonl`), Sync, Cortex-Log
