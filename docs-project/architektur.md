# Architektur — Gedankenwelten-Online

Technische Gesamtarchitektur der öffentlichen Plattform.

---

## Überblick

Gedankenwelten-Online besteht aus drei Schichten:

```
gedankenwelten.de
    ├── /notes        ← Quartz (statische Notes + interaktiver Graph)
    ├── /discuss      ← Web-App (Diskussionen, Rating, Community)
    └── /api          ← Backend (PR-Status, Upvotes, Hash-Validierung)
```

Domain: **gedankenwelten.org** — gemietet März 2026 über Domain Factory.
Hosting: Raspberry Pi — Caddy als Webserver, Cloudflare für Domain + HTTPS.

---

## Schicht 1 — Quartz (Notes & Graph)

**Was es ist:** Open Source Static Site Generator, spezialisiert auf Obsidian-Vaults. Basis: Hugo.

**Was es liefert:**
- Note-Rendering mit interaktivem Graphen (Verbindungen zwischen Notes sichtbar)
- Volltext-Suche über alle Notes
- Wikilink-Navigation (`[[Note]]` → klickbarer Link)
- Dark/Light Mode, responsiv

**Anpassbarkeit:** Vollständig — Quartz ist Open Source. Templates, Styles, Komponenten können überschrieben werden.

**Deployment:** Build-Pipeline via GitHub Action → statische Files → Pi

---

## Schicht 2 — Web-App (Community & Diskussion)

Eigene Webanwendung, die Quartz umgibt und erweitert.

**Funktionen:**
- **PR-Diskussionen** — eingebettet direkt neben der Note, nicht auf GitHub; liest GitHub API
- **Rating-System** — Upvotes für offene PRs (Community-Qualitätssicherung), Bewertung bestehender Notes
- **Eigene Stimmen** — Kommentar-Interface für die `## Eigene Stimmen`-Sektion
- **Quervernetzung** — zeigt verbundene Kommentare aus anderen Notes (Stimmen-Vernetzungs-Agent)
- **Contributor-Profil** — wer hat was beigetragen, welche Notes, welche Stimmen

**Auth:** GitHub OAuth — kein eigenes Account-System, nutzt bestehende GitHub-Identitäten

**Tech-Stack:**
- **SvelteKit** oder **Astro** — leichtgewichtig, Pi-freundlich, schnelle Build-Zeiten
- **SQLite** — für Ratings, Upvotes, Kommentar-Metadaten (läuft problemlos auf Pi)
- **GitHub API** — PR-Status, Kommentare, Reviews als Datenquelle

---

## Schicht 3 — Backend / API

Minimales Backend auf dem Pi.

**Aufgaben:**
- Hash-Validierung (Schicht 1 des Integritätssystems — PUBLIC_SALT)
- Upvote-Speicherung und -Abfrage
- Webhook-Empfang von GitHub (PR geöffnet/gemergt → Cache invalidieren)
- Quartz-Rebuild triggern nach Merge

**Datenbank:** SQLite

```
tables:
  upvotes       (pr_id, user_id, timestamp)
  ratings       (note_slug, user_id, value, timestamp)
  comments      (note_slug, user_id, section, body, timestamp)
```

---

## GitHub als Rückgrat

GitHub ist das eigentliche Content-Backend — kein eigenes CMS nötig.

| Was | Wo |
|---|---|
| Notes (Markdown) | Git-Repository |
| PR-Diskussionen | GitHub Pull Request Comments |
| Änderungshistorie | Git-History |
| Contributor-Identitäten | GitHub OAuth |
| Secrets (Salts) | GitHub Secrets |
| CI/CD | GitHub Actions |

Die Web-App baut eine schöne Oberfläche *vor* GitHub — der Content bleibt im Repo.

---

## Integritätssystem

Drei Schichten — das Timing-Fenster zwischen Skill und PR wird geschlossen:

**Schicht 1 — Skill (lokal, PUBLIC_SALT):**
```
skill_hash = sha256(content + PUBLIC_SALT)
```
Beweist Skill-Nutzung. Erkennt manuelle Nachbearbeitung nach Erstellung.

**Schicht 2 — Backend-Registrierung (während Skill läuft):**

Der Skill sendet den Hash *direkt ans Backend*, noch bevor der Contributor den PR öffnet. Das Backend ist die Quelle der Wahrheit — nicht die Datei.

```bash
# Am Ende des Skills automatisch:
curl -X POST https://api.gedankenwelten.de/register-hash \
  -H "Authorization: Bearer $CONTRIBUTOR_TOKEN" \
  -d '{
    "hash": "...",
    "skill_version": "1.2",
    "note_type": "zeitgeist",
    "timestamp": "2026-03-28T10:00:00Z"
  }'
```

Backend speichert:
```
{ hash, timestamp, skill_version, note_type, contributor_id }
```

GitHub Action fragt beim PR: *"Kenn ich diesen Hash?"*
- Hash bekannt + Timestamp plausibel + Content stimmt überein → valide
- Hash unbekannt → automatisch abgelehnt
- Timestamp zu alt (z.B. >48h) → manuelles Review

**Zusätzliche Sicherheit durch Backend-Registrierung:**
- **Timestamp-Validierung** — schließt das Fenster zwischen Skill und PR
- **Skill-Version** — veraltete Versionen können ab einem Stichtag abgelehnt werden
- **Rate-Limiting** — verhindert Spam-PRs von einem Contributor
- **Audit-Trail** — jeder Hash ist rückverfolgbar auf Zeitpunkt und Skill-Version

**Schicht 3 — GitHub Action (SECRET_SALTs):**
```
verified_hash = sha256(content + SECRET_SALT_1 + SECRET_SALT_2)
```
Generiert serverseitig nach bestandener Validierung. Salts verlassen GitHub Secrets nie.

---

### Drei Sicherheitszonen im Überblick

| Zone | Wo | Was | Schließt |
|---|---|---|---|
| **1** | Skill lokal | `skill_hash` in Note | Skill-Nutzung nachweisbar |
| **2** | Backend-API | Hash vor PR registriert | Timing-Fenster zwischen Skill und PR |
| **3** | GitHub Action | `verified_hash` mit SECRET_SALTs | Manipulation nach Registrierung |

Jede Zone kann unabhängig scheitern — alle drei müssen bestehen.

---

## Community-Flow

```
Contributor
    ↓ verwendet Skill lokal
Note mit skill_hash
    ↓ Pull Request öffnen
GitHub PR
    ↓ Web-App zeigt PR zur Diskussion
Community diskutiert + votet
    ↓ Mindest-Upvotes erreicht
GitHub Action validiert
    (Template? Faktencheck? skill_hash valide? Upvotes?)
    ↓ Maintainer-Review
Merge
    ↓ Action generiert verified_hash + committed zurück
    ↓ Quartz rebuild getriggert
gedankenwelten.de aktualisiert
```

---

## Deployment auf Pi

```
/home/pi/gedankenwelten/
    quartz/         ← geclontes/gebautes Quartz
    app/            ← SvelteKit/Astro Web-App
    api/            ← Backend (Node/Python)
    data/           ← SQLite-Datenbank
    caddy/          ← Caddyfile
```

**Caddy-Konfiguration (Grundstruktur):**
```
gedankenwelten.de {
    handle /api/*   { reverse_proxy localhost:3001 }
    handle /app/*   { reverse_proxy localhost:3000 }
    handle /*       { root * /home/pi/gedankenwelten/quartz/public
                      file_server }
}
```

---

## Verbindung mit Breathe

Langfristig: Breathe-Inhalte (Übungen, Techniken) werden von Gedankenwelten-Notes direkt verlinkt — wenn eine Note Ohnmacht oder Überwältigung thematisiert, erscheint ein Breathe-Link als Handlungsangebot. Technisch: Cross-Domain-Links oder spätere Integration auf einer gemeinsamen Plattform.

---

## Offene Entscheidungen

- **Framework:** SvelteKit vs. Astro — beide Pi-tauglich, Entscheidung bei Implementierungsbeginn
- **Sprache:** Nur Deutsch zum Launch, Englisch als spätere Erweiterung
- **Moderations-Schwelle:** Wie viele Upvotes für PR-Freigabe?
- **Privatsphäre:** Welche Notes bleiben im privaten Vault (Gedanken-Ordner)?
