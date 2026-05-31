---
title: Datenschutzerklärung
date: 2026-05-31
tags: []
aliases:
  - Privacy Policy
---

# Datenschutzerklärung

Stand: 31. Mai 2026

## 1. Verantwortlicher

Andreas Schmieder
c/o IP-Management #10397
Ludwig-Erhard-Str. 18
20459 Hamburg

E-Mail: [luc@gedankenwelten.org](mailto:luc@gedankenwelten.org)

---

## 2. Webseite (gedankenwelten.org)

### Hosting

Diese Website wird über Cloudflare Pages ausgeliefert. Cloudflare verarbeitet technisch notwendige Verbindungsdaten (IP-Adresse, Zeitstempel, aufgerufene Seite). Details: [Cloudflare Privacy Policy](https://www.cloudflare.com/privacypolicy/).

### Analyse

Wir verwenden [Umami](https://umami.is/) — eine datenschutzfreundliche, cookielose Webanalyse. Umami erhebt **keine personenbezogenen Daten**, setzt **keine Cookies** und speichert **keine IP-Adressen**. Die erhobenen Daten (Seitenaufrufe, Verweildauer, Referrer) sind vollständig anonymisiert und werden auf unserer eigenen Infrastruktur verarbeitet.

### Cookies

Diese Website verwendet **keine Cookies**.

---

## 3. MCP-Server (mcp.gedankenwelten.org)

### Was ist der MCP-Server?

Der MCP-Server (Model Context Protocol) ermöglicht die semantische Suche über die Gedankenwelten-Wissensbasis. Nutzer verbinden sich mit ihrem eigenen KI-Assistenten (z.B. Claude, Cursor) und können Inhalte durchsuchen und lesen.

### Datenverarbeitung

| Datenkategorie | Verarbeitung |
|---|---|
| **Suchanfragen** | Werden zur Verarbeitung in Vektor-Embeddings umgewandelt. **Nicht gespeichert, nicht geloggt.** |
| **OAuth-Tokens** | Nur im Arbeitsspeicher (in-memory). Gehen bei Server-Neustart verloren. **Keine persistente Speicherung.** |
| **Client-Registrierungen** | Nur im Arbeitsspeicher. Client-Name und Redirect-URI werden für die OAuth-Sitzung gehalten. **Keine persistente Speicherung.** |
| **IP-Adressen** | Werden durch Cloudflare verarbeitet (Proxy). Der MCP-Server selbst loggt **keine IP-Adressen**. |
| **Inhalte der Wissensbasis** | Alle durchsuchbaren Inhalte sind öffentlich auf [gedankenwelten.org](https://gedankenwelten.org) verfügbar. |

### Keine Nutzerverfolgung

Der MCP-Server:
- speichert **keine Nutzerprofile**
- verwendet **kein Tracking**
- gibt **keine Daten an Dritte** weiter
- verarbeitet **keine personenbezogenen Daten** über die technische Verbindung hinaus

### Datenweitergabe

Die über den MCP-Server abgerufenen Inhalte werden an den KI-Assistenten des Nutzers übermittelt (z.B. Claude von Anthropic). Die Verarbeitung durch den KI-Assistenten unterliegt den Datenschutzbestimmungen des jeweiligen Anbieters.

---

## 4. Inhalte und Urheberrecht

Alle Inhalte auf gedankenwelten.org sind öffentlich zugänglich. Direkte Zitate aus Interviews und Vorträgen werden mit Quellenangabe und Zeitstempel verwendet und dienen der wissenschaftlichen Auseinandersetzung.

---

## 5. Ihre Rechte

Da wir keine personenbezogenen Daten speichern, fallen die meisten DSGVO-Betroffenenrechte (Auskunft, Löschung, Berichtigung) praktisch nicht an. Sollten Sie dennoch Fragen haben, wenden Sie sich an: [luc@gedankenwelten.org](mailto:luc@gedankenwelten.org)

---

## 6. Änderungen

Diese Datenschutzerklärung kann aktualisiert werden. Die aktuelle Version ist stets unter [gedankenwelten.org/Datenschutz](https://gedankenwelten.org/Datenschutz) abrufbar.

---

Siehe auch: [[Impressum|Impressum]] · [[MCP|MCP-Server Dokumentation]]
