# CLAUDE.md — Gedankenwelten-Online

Gedankenwelten-Online ist die öffentliche, community-getriebene Plattform, die aus dem privaten Gedankenwelten-Vault hervorgeht.

**Vision:** Ein offener Ort für politisches und philosophisches Denken — der nicht nur erklärt was ist, sondern Menschen hilft, handlungsfähig und resilient zu bleiben. Gegenmodell zum algorithmischen Outrage-Loop.

**Fundament:** Vipassana — Beobachten ohne zu reagieren, Verstehen ohne zu urteilen.

---

## Projektstruktur

```
Gedankenwelten-Online/
  CLAUDE.md           ← diese Datei
  Agents.md           ← Beschreibung aller Agenten und Skills
  docs/               ← Konzeptdokumente, Spezifikationen
  templates/          ← Note-Templates für Contributors
  scripts/            ← GitHub Actions, Hash-Generierung, Validierung
  quartz/             ← Quartz-Konfiguration für öffentliche Website
```

---

## Note-Struktur

Jede öffentliche Note hat folgende Pflicht-Sektionen:

```markdown
## Inhalt
[Kern-Content, faktengeprüft, hash-geschützt]

## Faktencheck
[!success] Bestätigt ...
[!warning] Vereinfacht ...
[!danger] Falsch ...

## Lösungen
[Konkrete Handlungsoptionen, lokale Initiativen, was funktioniert]

## Eigene Stimmen
### [@username] — YYYY-MM-DD
[Freie Meinung, Essay, Widerspruch — außerhalb des Hash-Schutzes]

## Positive Erfahrungen
[Persönliche Alltagserfahrungen, was trägt, was heilt]
```

---

## Integritätssystem (zwei Schichten)

**Schicht 1 — Skill (lokal):**
- Skill generiert `skill_hash` aus Content + PUBLIC_SALT
- Beweist Skill-Nutzung, erkennt manuelle Nachbearbeitung
- Wer ohne Skill schreibt oder danach editiert: Hash ungültig

**Schicht 2 — GitHub Action (server):**
- Action generiert `verified_hash` serverseitig mit SECRET_SALTs aus GitHub Secrets
- Salts verlassen den Server nie
- Erst nach bestandener Validierung wird signiert und gemergt

---

## Community-Prozess

1. Contributor verwendet den offiziellen Skill → Note mit `skill_hash` entsteht
2. PR einreichen — ohne `verified_hash`
3. GitHub Action prüft: Template korrekt? Faktencheck vorhanden? Skill-Hash valide?
4. Community-Upvotes (Mindestanzahl von verifizierten Contributoren)
5. Maintainer-Review
6. Action signiert mit `verified_hash` und merged

---

## Geist des Projekts

- Nicht neutral — sondern **dokumentierte Perspektive mit Faktencheck**
- Nicht nur Kritik — immer auch Lösungen und positive Erfahrungen
- Nicht anonym — jede Stimme hat einen Namen
- Nicht algorithmisch — keine Engagement-Optimierung, keine Outrage-Mechanik
- Verbunden mit **Breathe** — Körper und Geist als vollständiger Ansatz zur Resilienz

---

## Verbindung mit anderen Projekten

| Projekt | Verbindung |
|---|---|
| **Gedankenwelten** (privat) | Ursprung und laufender Content-Pool |
| **Breathe** | Körperliche Resilienz als Gegenstück zur mentalen |
| **Pi** | Hosting der öffentlichen Website via Quartz |
