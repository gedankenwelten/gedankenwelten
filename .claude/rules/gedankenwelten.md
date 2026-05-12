# Rules — Gedankenwelten

## Ordnerstruktur

```
content/
  Denker/          ← Obsidian-Notes pro Denker/Quelle (.md)
  DenkerVita/      ← Ausführliche Biografie-Profile pro Person (.md)
  Transkripte/     ← Rohe Transkripte und VTT-Dateien (.txt, .vtt) — nicht auf Website
  Zeitgeist/       ← Interviews & Vorträge zum Geist der Zeit (alle Spektren)
  Panorama/        ← Thematische Synthese-Notes (min. 3 Notes zum Thema)
  known-speakers.md   ← DenkerVita-Index mit Status
  Quellen & Links.md  ← Index aller externen Quellen
```

- Neue Denker-Notes → `content/Denker/`
- Neue Zeitgeist-Notes → `content/Zeitgeist/`
- Neue DenkerVitas → `content/DenkerVita/` (angelegt von Humboldt)
- Neue Panoramas → `content/Panorama/` (manuell, on demand)

## Panorama

Panoramas sind thematische Synthese-Seiten — kein Nachrichtenindex, sondern verdichtete Perspektive auf ein Thema.

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

DenkerVitas sind vollwertige, öffentliche Profile — sichtbar auf gedankenwelten.org.

**Frontmatter:**
```yaml
---
title: <Name> — DenkerVita
tags: [denker-vita, <thema>, <herkunft>]
---
```

**Struktur:** Biografie · Bücher & Publikationen (mit Kauflinks) · Empfehlenswerte Videos · Kernthesen · Politische Einordnung (wenn relevant) · Verbindungen zu anderen Denkern (via Montaigne) · Notes

**Link in Notes:** Jede Note die eine Person behandelt, bekommt am Ende des Speaker-Abschnitts:
```
→ [[DenkerVita/<Name>|DenkerVita]]
```

## Pflicht-Checkliste: Neue Note abschließen

1. **Aristoteles-Fragen**: 2–4 inline `> [!question]`-Callouts + `## Weiterdenken` mit 3–5 Fragen.
2. **Cross-Linking**: Sherlock + Montaigne.
3. **Quellen & Links.md**: Eintrag anlegen.
4. **Commit & Push**: Änderungen einchecken.

## Aristoteles-Fragen: Zum Weiterdenken anregen

Jede Note bekommt Fragen — verteilt im Text UND gesammelt am Ende.

### Inline-Fragen (nach wichtigen Sektionen)

```markdown
> [!question] Weitergedacht
> Wenn das Gehirn primär Vorhersagen trifft — *kann es dann überhaupt überrascht werden?*
```

**Frequenz:** 2–4 inline-Fragen pro Note.

### `## Weiterdenken` — Abschluss-Abschnitt (Pflicht)

```markdown
---

## Weiterdenken

> [!question] Was Aristoteles vielleicht gefragt hätte
> - Wenn [Kernthese] stimmt — *was folgt daraus für [konkreten Lebensbereich]?*
> - [Sprecher] sagt [X] — aber widerspricht das nicht [Y]?
> - Wem nützt es, wenn wir [Annahme] für selbstverständlich halten?
> - Was wäre das stärkste Gegenargument zu [zentrale These]?
```

**Regeln:** Nicht rhetorisch · mindestens eine herausfordernde Frage · 3–5 Fragen insgesamt.

---

## Zeitgeist-Notes: Faktencheck

| Callout | Bedeutung |
|---|---|
| `> [!success] Bestätigt` | Claim ist durch Quellen belegt |
| `> [!warning] Vereinfacht / Nicht eindeutig belegt` | Claim ist grob richtig, aber verzerrt |
| `> [!danger] Falsch` | Claim ist faktisch nicht haltbar |
