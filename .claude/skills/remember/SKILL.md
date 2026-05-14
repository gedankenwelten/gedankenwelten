---
name: remember
description: Speichert eine Erinnerung oder wichtige Information in .mnemosyne.md. Trigger-Phrasen — "merke dir das", "remember this", "notier dir", "das ist wichtig".
---

# Remember — Erinnerungen speichern

Wenn der Nutzer etwas festhalten möchte, wird es persistent in `.mnemosyne.md` gespeichert.

## Trigger-Phrasen

- "merke dir das bitte"
- "merk dir das"
- "remember this"
- "notier dir"
- "das ist wichtig"
- oder sinngemäß ähnlich

## Schritt 1 — Was merken?

Identifiziere den Inhalt:
- Was der Nutzer **explizit** sagt (*"merke dir, dass ich X bevorzuge"*)
- Oder der **unmittelbare Kontext** davor (das letzte besprochene Thema)
- Wenn unklar: kurz nachfragen — *"Soll ich mir [X] merken?"*

## Schritt 2 — Sicherheits-Check (IMMER ZUERST)

Prüfe ob der Inhalt **Credentials** enthält (Passwörter, Tokens, API-Keys, Secrets).

**Falls ja:** Freundlich ablehnen:
> *"Credentials speichere ich nicht — die gehören in Umgebungsvariablen oder einen Passwort-Manager. Kann ich dir anders helfen?"*

Nicht weitermachen.

## Schritt 3 — Speichern

1. `.mnemosyne.md` öffnen
2. Falls die Datei nicht existiert: Erstellen mit dem Standard-Template (siehe CLAUDE.md Schritt 3)
3. Unter `## Erinnerungen` als Bullet-Point ergänzen:
   ```markdown
   - **[DD.MM.YYYY]** Inhalt der Erinnerung
   ```
4. Kurz bestätigen: *"Notiert ✓"*

## Schritt 4 — Keine Duplikate

Vor dem Speichern: Prüfe ob eine sehr ähnliche Erinnerung bereits existiert.
- Falls ja: Aktualisieren statt doppelt anlegen
- Falls ähnlich aber anders: Beide behalten, der Nutzer weiß es besser
