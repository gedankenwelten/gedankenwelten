# Rules — Gedankenwelten

## Ordnerstruktur

```
content/
  Denker/          ← Tiefenanalysen einzelner Denker/Quellen
  Zeitgeist/       ← Interviews, Vorträge, Podcasts — Geist der Zeit
  DenkerVita/      ← Ausführliche Biografie-Profile
  Panorama/        ← Thematische Synthese-Notes (min. 3 Notes zum Thema)
  Gedanken/        ← Persönliche Reflexionen und Essays
  Vipassana/       ← Vipassana-Konzepte und Meditationspraxis
  Transkripte/     ← Rohe Transkripte und VTT-Dateien (nicht auf Website)
  known-speakers.md   ← DenkerVita-Index mit Status
  Quellen & Links.md  ← Index aller externen Quellen
```

- Neue Denker-Notes → `content/Denker/`
- Neue Zeitgeist-Notes → `content/Zeitgeist/`
- Neue DenkerVitas → `content/DenkerVita/`
- Neue Panoramas → `content/Panorama/` (manuell, wenn ≥3 Notes dasselbe Thema)
- Persönliche Reflexionen → `content/Gedanken/`
- Vipassana-Konzepte → `content/Vipassana/`

## Lokale Wiki

Die Wiki läuft als Docker-Container und baut sich bei Dateiänderungen automatisch neu:

```bash
docker compose up        # Wiki starten → http://localhost:9999
docker compose up -d     # Im Hintergrund starten
docker compose down      # Stoppen
```

Wenn der Container läuft: **jede gespeicherte Note erscheint automatisch in der Wiki** — kein manueller Rebuild nötig.

## Panorama

Panoramas sind thematische Synthese-Seiten — kein Nachrichtenindex, sondern verdichtete Perspektive.

**Wann anlegen:** Manuell, wenn mindestens 3 Notes dasselbe Thema aus verschiedenen Winkeln beleuchten.

**Frontmatter:**
```yaml
---
title: "Panorama — [Thema]"
tags:
  - panorama
  - [thema-tags]
erstellt: YYYY-MM-DD
---
```

## DenkerVita

DenkerVitas sind vollwertige, öffentliche Profile — sichtbar in der lokalen Wiki und auf gedankenwelten.org.

**Frontmatter:**
```yaml
---
title: <Name> — DenkerVita
tags: [denker-vita, <thema>]
---
```

**Link in Notes:** Jede Note die eine Person behandelt, bekommt am Ende des Speaker-Abschnitts:
```
→ [[DenkerVita/<Name>|DenkerVita]]
```

## Pflicht-Checkliste: Neue Note abschließen

1. **Sokrates-Fragen**: 2–4 inline `> [!question]`-Callouts + `## Weiterdenken` am Ende. → Sokrates-Skill aufrufen.
2. **Sherlock-Faktencheck**: Pflicht bei Zeitgeist-Notes.
3. **Montaigne Cross-Linking**: Verbindungen zu bestehenden Notes.
4. **Quellen & Links.md**: Eintrag anlegen.
5. **Commit & Push**: `git add -A && git commit -m "note-pipeline: …" && git push`

Die lokale Wiki baut sich beim nächsten File-Save automatisch neu — kein Extra-Schritt nötig.

## Sokrates-Fragen

Jede Note bekommt Fragen — verteilt im Text UND gesammelt am Ende. **Der Sokrates-Skill (`sokrates`) ist die Referenz für Fragetypen, Qualität und Format.**

### Inline-Fragen (2–4 pro Note)
```markdown
> [!question] Weitergedacht
> Wenn [These] — *was bedeutet das für [konkreten Aspekt]?*
```

### `## Weiterdenken` — Abschluss (Pflicht)
```markdown
---

## Weiterdenken

> [!question] Was Sokrates vielleicht gefragt hätte
> - Wenn [Kernthese] stimmt — *was folgt daraus?*
> - [Sprecher] sagt [X] — aber widerspricht das nicht [Y]?
> - Wem nützt es, wenn wir [Annahme] für selbstverständlich halten?
> - Was wäre das stärkste Gegenargument?
```

**Regeln:** Nicht rhetorisch · min. 1 herausfordernde Frage · 3–5 Fragen insgesamt.

---

## Zeitgeist-Notes: Faktencheck

| Callout | Bedeutung |
|---|---|
| `> [!success] Bestätigt` | Claim durch Quellen belegt |
| `> [!warning] Vereinfacht` | Grob richtig, aber verzerrt |
| `> [!danger] Falsch` | Faktisch nicht haltbar |
