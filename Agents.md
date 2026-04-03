# Agents.md — Gedankenwelten-Online

Übersicht aller Agenten und Skills, die in der Gedankenwelten-Pipeline eingesetzt werden.

---

## Produktions-Pipeline (Note erstellen)

### Humboldt — Sprecher-Recherche
**Rolle:** Vor dem Download den Sprecher/Autor recherchieren und einordnen.
**Input:** Name, Thema, Kontext
**Output:** Kompaktes Briefing — Wer ist die Person? Relevante Werke, politische/intellektuelle Einordnung, Kontext zum Thema.
**Verwendung:** Füllt den `> [!info] Wer spricht?`-Callout in jeder Note.

---

### Sherlock — Faktencheck
**Rolle:** Behauptungen in einer Note gegen Quellen prüfen.
**Input:** Vollständiger Note-Text
**Output:** Zwei Blöcke:
1. `## Faktencheck` — mit `[!success]`, `[!warning]`, `[!danger]` Callouts
2. `## Weiterführende Quellen (Sherlock)` — falls relevante Quellen gefunden
**Verwendung:** Pflicht bei jeder Zeitgeist-Note.

---

### Montaigne — Cross-Linking
**Rolle:** Thematische Verbindungen zwischen der neuen Note und bestehenden Notes finden.
**Input:** Neue Note (Volltext) + Liste aller bestehenden Notes mit Tags
**Output:** Liste von `[[Links]] — Begründung`
**Verwendung:** Schritt 6 der Pipeline — neue Note verlinkt bestehende, bestehende Notes werden bidirektional aktualisiert.

---

## Qualitätssicherung (Community-Pipeline)

### Skill — Note-Erstellung mit Hash (geplant)
**Rolle:** Offizieller Skill für Contributors. Erstellt Note nach Template und signiert sie mit `skill_hash`.
**Mechanismus:**
```
skill_hash = sha256(content + PUBLIC_SALT)
```
**Zweck:** Beweist Skill-Nutzung. Erkennt manuelle Nachbearbeitung nach Erstellung.

---

### GitHub Action — Verifikation & Signatur (geplant)
**Rolle:** Serverseitige zweite Schicht der Integritätssicherung.
**Prüft:**
- Template-Struktur eingehalten?
- Faktencheck-Abschnitt vorhanden?
- Pflicht-Frontmatter vollständig?
- `skill_hash` valide (Content unverändert seit Skill-Erstellung)?
- Community-Upvotes erreicht?
**Signiert bei Erfolg:**
```
verified_hash = sha256(content + SECRET_SALT_1 + SECRET_SALT_2)
```
Salts liegen ausschließlich in GitHub Secrets — verlassen den Server nie.

---

## Quervernetzungs-Skill (geplant)

### Verbindungs-Agent für Eigene Stimmen
**Rolle:** Analysiert neue Einträge in `## Eigene Stimmen` und findet thematische Resonanzen mit anderen Kommentaren im gesamten Vault.
**Mechanismus:** Embedding-Index über alle Eigene-Stimmen-Einträge, Ähnlichkeitssuche beim neuen Eintrag.
**Output:** Links zwischen Kommentaren verschiedener Notes — Menschen und ihre Gedanken werden verbunden, nicht nur Notes.

---

## Gesamt-Architektur

```
Contributor
    ↓ verwendet
Skill (lokal)
    ↓ erstellt Note mit skill_hash
GitHub PR
    ↓ durchläuft
GitHub Action
    ↓ prüft + signiert mit verified_hash
Community-Upvotes
    ↓
Maintainer-Review
    ↓
Merge → Quartz → gedankenwelten.de
```

---

## Philosophie der Agenten

Kein Agent trifft endgültige Urteile — sie liefern Material für menschliche Entscheidungen. Humboldt recherchiert, Sherlock prüft, Montaigne verbindet. Der Mensch urteilt. Das System macht Transparenz zur Pflicht, nicht zur Option.
