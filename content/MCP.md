---
title: Die Gedankenwelten im Gespräch
description: Man kann die Gedankenwelten lesen. Man kann sie auch fragen und sich vorlesen lassen, mit dem eigenen KI-Assistenten, ohne Anmeldung.
date: 2026-05-31
aktualisiert: 2026-11-12
tags: []
aliases:
  - MCP Server
  - MCP Documentation
  - Gedankenwelten MCP
---

# Die Gedankenwelten im Gespräch

> [!abstract] Fragen statt suchen
> Man kann die Gedankenwelten lesen. Man kann sie auch fragen. Wer sie an seinen KI-Assistenten anschließt, Claude zum Beispiel, spricht mit rund 700 Notes und über 400 Porträts wie mit jemandem, der sie alle gelesen hat. Er sucht die passenden Stellen, nennt die Quellen dahinter und liest auf Wunsch vor. Einmal einrichten, ohne Anmeldung, kostenlos.

## Was man damit kann

Du fragst, wie du einen Menschen fragen würdest, schriftlich oder gesprochen. Der Assistent holt sich die Abschnitte, die dazu passen, und antwortet daraus, mit Link auf jede Note, aus der er schöpft. Er kann eine Note ganz vorlesen, ein Thema über viele Notes hinweg zusammentragen oder die Studien und Bücher heraussuchen, auf die sich eine Aussage stützt.

Zum Beispiel:

- „Was ist neu in den Gedankenwelten?“
- „Was sagt die Gedankenwelt zu Hannah Arendt?“
- „Was wurde im letzten Monat über Demokratie geschrieben?“
- „Lies mir das KI-Panorama vor.“
- „Welche Quellen stehen hinter der Note über Ausländerkriminalität?“
- „Wo widersprechen sich Byung-Chul Han und Hartmut Rosa?“
- „Welche Notes hängen mit der über Harrys Bude zusammen?“

Am schönsten ist es im Sprachmodus, unterwegs, mit Kopfhörern. Eine lange Note lässt sich beim Hören nicht überfliegen, darum nennt der Assistent zuerst die Gliederung und fragt, womit er anfangen soll. Dann liest er Abschnitt für Abschnitt, fürs Ohr aufbereitet, und hält an, wo der Gedanke atmet. Wie das im Einzelnen geht und was man ihm sagen kann, steht auf der Seite [[Barrierefreiheit#Lange Notes hören|Barrierefreiheit]].

## Einrichten

### In Claude, in drei Schritten

1. In Claude (im Browser, am Rechner oder in der App) die **Einstellungen** öffnen, dort **Konnektoren** (englisch *Connectors*).
2. **Konnektor hinzufügen** wählen und diese Adresse eintragen:

```
https://mcp.gedankenwelten.org/mcp
```

3. Speichern. Eine Anmeldung gibt es nicht. Der Zugang steht danach auf allen Geräten bereit, auch in der App auf dem Telefon.

### Mit deinem Assistenten zusammen

Du nutzt einen anderen Assistenten oder kommst mit den Menüs nicht zurecht? Dann kopier diesen Text in ein neues Gespräch mit deiner KI. Sie fragt nach, welche App du benutzt, und führt dich durch die Einrichtung.

```
Ich möchte die Gedankenwelten (gedankenwelten.org) an dich anschließen. Das ist eine öffentliche Wissenssammlung mit Notes zu Philosophie, Demokratie, Psychologie und dem Zeitgeschehen, die über einen MCP-Server erreichbar ist.

Adresse: https://mcp.gedankenwelten.org/mcp
Transport: Streamable HTTP
Anmeldung: keine, der Zugang ist öffentlich und nur lesend

Frag mich bitte zuerst, welche App ich benutze und auf welchem Gerät. Dann führ mich Schritt für Schritt durch die Einrichtung, immer nur einen Schritt auf einmal, und warte, bis ich ihn erledigt habe. Wenn du nicht sicher weißt, wo eine Einstellung in meiner App liegt, sag das ehrlich, statt zu raten. Falls meine App keine MCP-Server unterstützt, sag es mir.

Wenn alles eingerichtet ist, probier es gleich aus: Frag die Gedankenwelten, was in den letzten Tagen neu dazugekommen ist, und erzähl es mir.
```

Wer den Zugang schon vor dem 7. November 2026 eingerichtet hat, verbindet ihn am besten einmal neu (trennen und wieder hinzufügen). Dann kennt der Assistent alle Möglichkeiten, auch das Vorlesen.

## Was du dabei wissen solltest

Die Antwort schreibt dein Assistent, nicht wir. Er arbeitet mit unseren Texten, aber er fasst zusammen, wählt aus und kann sich irren. Was in einer Note steht, gilt; die Links in seinen Antworten führen dorthin. Wo es dir auf eine Aussage ankommt, lies nach.

Du zahlst nichts an uns. Den Assistenten nutzt du mit deinem eigenen Konto, die Gedankenwelten stellen nur das Wissen bereit.

Wenn dir beim Fragen oder Zuhören etwas fehlt oder stört: [luc@gedankenwelten.org](mailto:luc@gedankenwelten.org). Jeder Hörtest hat bisher etwas verändert.

## Datenschutz

Der Zugang braucht keine Anmeldung und vergibt keine Kennungen. Fragen werden weder gespeichert noch protokolliert, es gibt kein Zugriffsprotokoll und keine Nachverfolgung. Zum Schutz vor Überlastung zählt der Server die Anfragen je IP-Adresse höchstens 60 Sekunden lang im Arbeitsspeicher; auf die Platte wird nichts geschrieben.

Um zu wissen, ob der Dienst überhaupt genutzt wird, führt der Server Tagessummen und sonst nichts: in wie vielen Gesprächen er genutzt wurde, in wie vielen Gesprächen jede Note geöffnet wurde (nur der Titel, einmal je Gespräch) und wie oft jedes Werkzeug aufgerufen wurde (nur der Name, bei den neuesten Notes auch der gewählte Zeitraum). Ob zwei Anfragen zum selben Gespräch gehören, weiß der Server nur aus der offenen Verbindung, und das auch nur bis Mitternacht im Arbeitsspeicher. Keine Fragen, keine Suchergebnisse, keine Adressen, keine Uhrzeiten, keine Kennungen. Mehr in der [[Datenschutz|Datenschutzerklärung]].

## Für Entwickler

Der Server spricht das Model Context Protocol (MCP) über **Streamable HTTP**, öffentlich und nur lesend.

```
https://mcp.gedankenwelten.org/mcp
```

**Claude Desktop** über die Konfigurationsdatei (`claude_desktop_config.json`, unter macOS in `~/Library/Application Support/Claude/`, unter Windows in `%APPDATA%\Claude\`), danach Claude Desktop neu starten:

```json
{
  "mcpServers": {
    "gedankenwelten": {
      "type": "streamable-http",
      "url": "https://mcp.gedankenwelten.org/mcp"
    }
  }
}
```

**Werkzeuge**

| Werkzeug | Was es tut |
|---|---|
| `search` | Semantische Suche über alle Notes, mit Abschnitt, Rubrik und Datum je Treffer. Optional mit Zeitraum (`days`, `since`, `until`), Datumsart (`erstellt`, `aktualisiert`) und Rubrik. |
| `read_note` | Eine Note ganz oder abschnittsweise. `section="toc"` liefert die Gliederung mit Hördauer, `mode="hoeren"` eine Fassung fürs Ohr (Belege auf ihre Einordnung verkürzt), `ab=` setzt mitten im Abschnitt wieder ein. |
| `latest_notes` | Was neu ist oder vertieft wurde, neueste zuerst, nach Rubrik und Zeitraum filterbar. *Aktualisiert* heißt: inhaltlich überarbeitet; bloßes Verlinken zählt nicht. |
| `list_thinkers` | Alle Denker-Notes und Porträts mit ihren Themen. |
| `explore_connections` | Zu einem Thema die verbundenen Notes; mit `note=` die Nachbarn einer Note: ausgehende Verweise, Rückverweise und nahe, noch unverbundene Notes. |
| `find_sources` | Die Quellen hinter einem Thema oder einer Note: Bücher, Studien (mit DOI), Videos, Artikel. Nach Art filterbar. |

**Technik**

| | |
|---|---|
| Inhalt | rund 700 Notes und über 400 Porträts (Stand November 2026), laufend ergänzt |
| Suchindex | Qdrant, rund 44.000 Abschnitte; Quellenverzeichnis mit rund 17.000 Einträgen |
| Einbettung | BAAI/bge-m3 (1024 Dimensionen), Vektorsuche |
| Sprache | vor allem Deutsch; Fragen auf Englisch funktionieren auch |
| Zugriff | nur lesend, ohne Anmeldung, keine Nutzerdaten (siehe oben) |

## In English

Gedankenwelten ("thought worlds") is a curated, mostly German knowledge base on philosophy, democracy, psychology and current affairs. Connect it to any MCP-capable assistant at `https://mcp.gedankenwelten.org/mcp` (Streamable HTTP, no login, read-only). In Claude: *Settings → Connectors → Add connector*, paste the address. Ask in English or German; your assistant searches the notes, links every note it draws from, finds the sources behind a claim and can read notes aloud section by section. No queries are stored; see the privacy section above.

---

[[Barrierefreiheit|Barrierefreiheit]] · [[Impressum|Impressum]] · [[Datenschutz|Datenschutzerklärung]]
