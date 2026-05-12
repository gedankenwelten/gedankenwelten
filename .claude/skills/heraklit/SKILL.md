---
name: heraklit
description: "Vertieft eine bestehende Gedankenwelten-Note nachträglich. Findet das Verborgene, ergänzt Substanz, Zitate und Einordnung. Use when a note already exists but needs more depth — 'da könnte man mehr draus machen'. Works on ALL sections: Zeitgeist, Denker, Panorama."
---

# Heraklit — Das Verborgene freilegen

> *„Die Natur liebt es, sich zu verbergen."*
> — Heraklit, Fragment B123

Heraklits Aufgabe: Eine bestehende Note nehmen und **tiefer graben** — das herausholen, was beim ersten Durchgang unter der Oberfläche geblieben ist.

---

## Wann Heraklit gerufen wird

- Eine Note fällt bei den Aristoteles-Metriken durch (< 1200 Wörter Inhalt)
- Cross-Linking zeigt: die Note ist zu dünn, um substantielle Verbindungen zu tragen
- Neue Erkenntnisse aus anderen Notes werfen neues Licht auf bestehendes Material
- Die Note wirkt wie eine Zusammenfassung statt wie eine Analyse

---

## Methode: Wie Heraklit arbeitet

### Schritt 1 — Diagnose: Was fehlt?

Bestehende Note lesen und gegen Aristoteles-Metriken prüfen:

```bash
# Wörter im Inhalt
sed -n '/^## Inhalt/,/^## Faktencheck\|^## Verbindungen\|^## Weiterführende/p' "NOTE.md" | wc -w

# Abschnitte zählen
grep -c "^###" "NOTE.md"

# Zitate zählen
grep -c '> \*"' "NOTE.md"
```

Diagnose dokumentieren:
- Welche Abschnitte sind zu dünn? (< 120 Wörter)
- Wo fehlen Zitate?
- Wo fehlt eigene Einordnung?
- Welche Themen aus dem Transkript wurden übergangen?

### Schritt 2 — Zurück zum Transkript

Das Transkript gezielt durchsuchen — nicht nochmal alles lesen, sondern:

1. **Dünne Abschnitte:** Grep nach Schlüsselwörtern → relevante Passage finden → Zitat + Herleitung nachlegen
2. **Fehlende Themen:** Was wurde im ersten Durchgang übersprungen, das doch substanziell ist?
3. **Bessere Zitate:** Manchmal gibt es eine prägnantere Formulierung weiter hinten im Gespräch

### Schritt 3 — Vertiefen (nicht aufblähen!)

> [!warning] Heraklit bläht nicht auf — er vertieft.
> Kein Füllmaterial. Keine Wiederholungen in anderen Worten.
> Jedes neue Wort muss den Wert der Note erhöhen.

**Was Heraklit hinzufügt:**
- Fehlende Zitate mit Timestamp-Link
- Herleitungen: *Wie* kommt der Sprecher zu dieser These?
- Konsequenzen: *Was folgt* daraus, was der Sprecher selbst nicht ausspricht?
- Kontextualisierung: Einordnung in größere Zusammenhänge
- Eigene Einschätzung (bei Denker-Notes: `> [!note]`-Callouts)
- Eventuell: einen neuen `###`-Abschnitt für ein übergangenes Kernthema

**Was Heraklit NICHT tut:**
- Bestehende gute Formulierungen umschreiben
- Abschnitte aufteilen die gut sind wie sie sind
- Verbindungen oder Faktencheck ändern (das ist nicht sein Job)
- Die Struktur der Note komplett umbauen

### Schritt 4 — Aristoteles-Fragen nachrüsten

Wenn die Note **keine** `> [!question]`-Callouts und keinen `## Weiterdenken`-Abschnitt hat, fügt Heraklit diese hinzu:

**Inline-Fragen (2–4):**
- Fertige Abschnitte durchgehen: Wo provoziert der Inhalt eine offene Frage?
- `> [!question] Weitergedacht` nach den substanziellsten Stellen

**Abschluss-Abschnitt:**
```markdown
---

## Weiterdenken

> [!question] Was Aristoteles vielleicht gefragt hätte
> - [3–5 übergreifende, nicht-rhetorische Fragen]
```

**Qualitäts-Check für Fragen:**
- Mindestens 1 adversariale Frage (Herausforderung)
- Mindestens 1 verbindende Frage (Brücke zu anderem Denker/Note)
- Keine Frage ist trivial oder googlebar

### Schritt 5 — Qualitäts-Check

Nach dem Vertiefen erneut prüfen:
```
□ Inhalt ≥ 1200 Wörter?
□ Jeder Abschnitt ≥ 120 Wörter?
□ ≥ 5 direkte Zitate mit Timestamp?
□ Keine „Zusammenfassungs-Absätze" mehr ohne Substanz?
□ 2–4 inline > [!question]-Callouts vorhanden?
□ ## Weiterdenken mit 3–5 Fragen vorhanden?
```

### Schritt 6 — Commit

```bash
git add -A && git commit -m "heraklit: [Autor] — vertieft"
git push origin main
```

---

## Checkliste

- [ ] Diagnose: Was fehlt? (Metriken + inhaltlich)
- [ ] Transkript gezielt durchsucht
- [ ] Dünne Abschnitte vertieft (Zitate, Herleitungen)
- [ ] Eventuell neuen Abschnitt für übergangenes Thema
- [ ] Aristoteles-Fragen nachrüsten (inline + Weiterdenken)
- [ ] Qualitäts-Check bestanden (≥1200 Wörter Inhalt)
- [ ] Commit & Push
