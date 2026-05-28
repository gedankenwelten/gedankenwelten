# Beitragen zu Gedankenwelten

Schön, dass du hier bist. Gedankenwelten lebt davon, dass Menschen ihre Gedanken teilen — nicht perfekt, sondern ehrlich.

---

## 🌱 GoodNews schreiben

Die einfachste Art beizutragen: Teile eine gute Nachricht.

1. Fork dieses Repository
2. Erstelle eine Datei in `content/GoodNews/` — Format: `YYYY-MM-DD-kurztitel.md`
3. Schreibe 2–5 Sätze über etwas Positives (persönlich oder aus der Welt)
4. Öffne einen Pull Request

Details zum Format und den Tags findest du in [`content/GoodNews/README.md`](content/GoodNews/README.md).

> Im Vipassana-Sinne: Wenn es jemandem helfen könnte, es zu lesen — dann darf es stehen.

---

## 📝 Inhaltliche Beiträge

Du hast einen Fehler in einer Note gefunden? Einen toten Link? Einen Faktencheck, der aktualisiert werden sollte?

- **Fehler melden:** Öffne ein [Issue](https://github.com/gedankenwelten/gedankenwelten/issues)
- **Korrektur einreichen:** Fork → Änderung in `content/` → Pull Request
- **Neue Note vorschlagen:** Öffne ein Issue mit dem Titel `Vorschlag: [Thema]`

### Was wir nicht annehmen

- Inhalte, die bestehende Notes grundlegend umschreiben (das sind persönliche Reflexionen)
- Werbung, SEO-Texte, KI-generierte Massenbeiträge
- Politische Stellungnahmen ohne inhaltliche Substanz

---

## 🔧 Technische Beiträge

Verbesserungen an Tooling, Scripts, Docker-Setup oder KI-Konfiguration sind willkommen.

1. Fork + Branch erstellen
2. Änderungen machen und lokal testen (`docker compose up -d`)
3. Pull Request mit kurzer Beschreibung öffnen

### Code-Konventionen

- Shell-Scripts: `#!/usr/bin/env bash`, `set -euo pipefail`
- Commit-Messages: Deutsch oder Englisch, Kleinbuchstaben, beschreibend
- Keine Secrets, API-Keys oder persönliche Daten committen

---

## 🛡️ Automatische Sicherheitsprüfung

Jeder Pull Request wird automatisch auf **versteckten Text** geprüft (`injection-scan`). Hintergrund: Gedankenwelten-Notes werden auch von KI-Assistenten gelesen und weiterverarbeitet. Versteckter Text könnte versuchen, diese Assistenten zu manipulieren (*Prompt Injection*) — oder auf der veröffentlichten Seite unsichtbar mitlaufen.

Der Check **blockiert** einen PR bei:

- HTML-Kommentaren (verstecktem Text in `<!--`-Markern)
- unsichtbarem Text (weiße Schrift, Schriftgröße ≤ 1px, `display:none`)
- unsichtbaren Unicode-Zeichen (Zero-Width, Tag-Characters, Bidi-Override)

Das ist nichts Persönliches — es betrifft nur die Tarnung, nie den Inhalt. Schreib offen, was du denkst; sichtbarer Text wird nie blockiert. Wer über KI-Sicherheit schreibt und dabei Beispiel-Phrasen zitiert, bekommt höchstens einen **Hinweis** (keine Blockade).

Der Scanner liegt offen unter [`scripts/injection_scan.py`](scripts/injection_scan.py) — du kannst ihn vor dem Einreichen lokal laufen lassen:

```bash
python3 scripts/injection_scan.py content/**/*.md
```

---

## 🤝 Umgangsformen

Gedankenwelten hat keinen ausufernden Code of Conduct — nur drei Prinzipien:

1. **Ehrlichkeit** — Schreibe, was du denkst, nicht was gut klingt
2. **Respekt** — Auch bei Widerspruch: die Person hinter dem Text sehen
3. **Substanz** — Lieber ein guter Satz als zehn leere

---

## 📜 Lizenz

Mit deinem Beitrag stimmst du zu:

- **Inhalte** in `content/` werden unter [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) veröffentlicht
- **Code** wird unter [MIT](LICENSE) veröffentlicht

Details in der [LICENSE](LICENSE)-Datei.
