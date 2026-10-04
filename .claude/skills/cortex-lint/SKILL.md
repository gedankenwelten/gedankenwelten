---
name: cortex-lint
description: "Konsistenz-Audit für die Gedankenwelten — findet inhaltliche Widersprüche ZWISCHEN Notes, veraltete Thesen, Redundanz-ohne-Querlink und Frontmatter-/Tag-Lücken. RAG-gestützt, Urteil bei Claude. Schreibt einen Vorschlags-Report nach owner-inbox/ — editiert nie still. Abgegrenzt von gedankenwelten-links (Wikilinks) und rag-reconcile (Qdrant-Drift). Trigger — 'cortex-lint', 'konsistenz prüfen', 'widersprüche finden', 'note gegen bestand prüfen', 'lint'."
---

# cortex-lint — der Konsistenz-Spiegel

`gedankenwelten-links` prüft, ob *Links* stimmen. `rag-reconcile` prüft, ob *Qdrant* mit der Platte
übereinstimmt. **Niemand prüft, ob zwei Notes sich inhaltlich *widersprechen* — oder ob eine These
veraltet ist.** Genau diese Lücke schließt cortex-lint. Geerbt vom `lint` aus Hermes' `llm-wiki`-Skill,
aber auf unsere RAG-Infrastruktur und die Vipassana-Ehrlichkeitslogik zugeschnitten.

> [!important] Vorschlagen, nicht eingreifen — „Maschine sammelt, Mensch urteilt"
> cortex-lint **editiert nie eine Note still.** Es sammelt Befunde und legt einen Report in `owner-inbox/`.
> Andreas entscheidet, was davon umgesetzt wird. Das Urteil über einen Widerspruch ist *Urteil* — es läuft
> auf voller Qualität (Claude), nie heruntergeroutet. Das Einsammeln der Kandidaten (RAG-Pulls) darf stumpf sein.

> [!note] Vipassana: ein Widerspruch ist kein Makel (anicca)
> Notes sind Snapshots; Realität und Verstehen ändern sich. Ein Widerspruch zwischen einer alten und einer
> neuen Note ist oft kein Fehler, sondern **gewachsenes Denken** — der Lint macht ihn nur *sichtbar*, damit
> Andreas wählen kann: auflösen, beide stehenlassen (mit Querlink „siehe Gegenposition"), oder die ältere
> als überholt markieren. *Befund vor Deutung.*

---

## Was cortex-lint prüft (und was nicht)

| Dimension | Prüft cortex-lint? | Wer sonst |
|---|---|---|
| **Inhaltliche Widersprüche** zwischen Notes (gegensätzliche Claims zum selben Sachverhalt) | ✅ Kern | — |
| **Veraltete Thesen** (eine Note behauptet etwas, das eine neuere überholt/korrigiert) | ✅ Kern | — |
| **Redundanz ohne Querlink** (zwei Notes behandeln dasselbe, verlinken sich aber nicht) | ✅ | (Montaigne legt Links *neu* an) |
| **Frontmatter-Lücken** (`description:`/`aktualisiert:` fehlt; `confidence:` bei empirie-lastigen Notes) | ✅ | — |
| **Tag-Inkonsistenz** (Synonyme statt kanonischer Tag aus `tags.md`) | ✅ | — |
| Kaputte/fehlende Wikilinks | ❌ | `gedankenwelten-links` |
| Qdrant ↔ Platte-Drift, Waisen-Vektoren | ❌ | `rag-reconcile` |

---

## Drei Modi

### Modus A — Einzelnote gegen den Bestand *(der Hauptweg)*

„Prüf *diese* Note gegen alles, was wir schon haben." Ideal frisch nach einer neuen Note (Pipeline-Anschluss).

1. Kernthesen der Note herausziehen (2–4 prüfbare Claims, keine Wertungen).
2. RAG nach thematisch nächsten Notes fragen (Payload exakt wie Montaigne):
   ```bash
   curl -s -X POST "<dein-rag-server>/webhook/query-gedankenwelten" \
     -H "Content-Type: application/json" \
     -d '{"question": "<die Kernthesen als Frage>", "top_k": 15, "answer": false}'
   ```
   Antwort ist ein **JSON-Array** → immer `[0]` nehmen, dann `sources` (mit `title`, `source_id`, `score`).
3. Die Top-8 Kandidaten lesen (nach `source_id`-Pfad).
4. **Urteilen** — für jedes Paar (neue Note ↔ Kandidat): Widerspruch? Überholung? Redundanz ohne Link?
5. Report schreiben (s.u.).

### Modus B — Thema / Cluster

„Ist unser Bild von *Migration* / *KI-Risiko* / *Vipassana* in sich stimmig?" Ein Tag oder Thema als Anker
→ RAG-Cluster ziehen → **interne** Konsistenz des Clusters prüfen (widersprechen sich Notes *innerhalb* des
Themas?). Gut vor dem Anlegen eines Panoramas.

### Modus C — Sweep *(optional, batch)*

Eine Queue durcharbeiten — sinnvollerweise die zuletzt geänderten Notes (`git log` der letzten N Tage) oder
eine Rubrik. Jede Note bekommt einen Modus-A-Durchlauf.

> [!warning] Kein stilles Kappen
> Bei großem Bestand (~500 Notes) ist ein Voll-Sweep teuer. Wenn gekappt wird (Top-N, eine Rubrik, ein
> Zeitfenster), **im Report explizit sagen, was *nicht* geprüft wurde.** Eine Abdeckungslücke, die wie
> Vollständigkeit aussieht, ist schlimmer als eine offen benannte.

---

## Routing

- **Stumpf (lokal/automatisch ok):** die RAG-Pulls, das Sammeln der Kandidaten, Frontmatter-/Tag-Checks
  (rein mechanisch — `description:`/`aktualisiert:` da? Tag in `tags.md`-Taxonomie?).
- **Urteil (Claude, volle Qualität):** ob zwei Claims sich *wirklich* widersprechen oder nur verschieden
  rahmen; ob eine These *überholt* oder bloß *ergänzt* ist. Das ist Bedeutung, nie heruntergeroutet.

---

## Report-Format (`owner-inbox/cortex-lint-YYYY-MM-DD.md`)

Befunde nach Schwere gruppieren. Jeder Befund **auditierbar**: die zwei Notes, die *wörtlichen* Claims, ein
Vorschlag — nie ein stiller Fix.

```markdown
# cortex-lint — <Datum> · <Modus + Scope>

> Geprüft: <was genau>. **Nicht geprüft: <was ausgelassen wurde>.**

## 🔴 Widersprüche (Urteil nötig)
### <Note A> ↔ <Note B>
- **A behauptet:** „<wörtliches Zitat>" (`Pfad`, aktualisiert: <Datum>)
- **B behauptet:** „<wörtliches Zitat>" (`Pfad`, aktualisiert: <Datum>)
- **Art:** echter Sachwiderspruch / verschiedene Rahmung / A überholt durch B
- **Vorschlag:** auflösen in B · beide mit Querlink „siehe Gegenposition" · A als überholt markieren
- **Konfidenz des Lints:** hoch/mittel/niedrig

## 🟡 Veraltet / überholt
## 🟢 Redundanz ohne Querlink  (→ ggf. Montaigne)
## ⚪ Frontmatter / Tags
```

**`confidence:`-Frontmatter (optional, aus den Spuren geliehen):** Bei Notes mit starken *empirischen*
Claims darf der Lint ein `confidence:`-Feld *vorschlagen* (nie selbst setzen). Es sagt: „wie sicher ist die
Kernbehauptung dieser Note?" — und macht spätere Überholungen ehrlich sichtbar. **Nie massenhaft ausrollen;**
nur dort vorschlagen, wo ein Konflikt oder eine Überholung es konkret motiviert.

---

## Nach dem Lint

- Report liegt in `owner-inbox/` → Andreas reviewt, entscheidet pro Befund.
- Umgesetzte inhaltliche Änderungen: normale Note-Pflicht (ggf. `aktualisiert:` bump bei echter Korrektur,
  RAG re-ingest der geänderten Note, Deploy).
- Neue Querlinks: über **Montaigne** bidirektional einpflegen (cortex-lint *findet*, Montaigne *verlinkt*).
- `aktualisiert:` der Altnotes **nicht** anfassen, wenn nur ein Querlink dazukommt (Backlink-Falle → Journal).

## Verwandt

- `gedankenwelten-links` — Wikilink-Integrität (orthogonal).
- `rag-reconcile.sh` — Qdrant ↔ Platte (orthogonal).
- **Montaigne** — legt die vorgeschlagenen Querlinks an.
- `spuren.md` — Herkunft von `confidence:` + der Ehrlichkeits-Register-Idee.
