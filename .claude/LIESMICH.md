# Die Werkstatt der Gedankenwelten

Hier liegt, womit die Notes auf [gedankenwelten.org](https://gedankenwelten.org) entstehen: die **Skills**
(Anleitungen für einen KI-Assistenten wie Claude Code), die **Agenten**, die **Regeln** und **Playbooks**,
und die kleinen **Skripte**, die sie brauchen. Damit kannst du die Methode selbst nutzen — für deine eigene
Sammlung oder als Fork dieses Repos.

## Woher das kommt

Die Gedankenwelten wachsen in einem privaten Obsidian-Vault namens *Cortex*. Diese Dateien sind **wörtlich
von dort übernommen** und werden bei jeder Veröffentlichung neu gespiegelt — sie sind also immer der Stand,
mit dem tatsächlich gearbeitet wird, keine eigens geglättete Fassung. Ausgenommen ist nur eine Datei:
`skills/gedankenpoesie/voices/luc.md`, die Beschreibung von Lucs eigener Schreibstimme; ihre Beispiele aus
privaten Texten sind durch öffentliche ersetzt.

## Was du anpassen musst

Beim Spiegeln wird Infrastruktur durch Platzhalter ersetzt:

| Platzhalter | steht für |
|---|---|
| `<vault>/` | den Wurzelordner deiner Sammlung |
| `content/` | den Notes-Ordner (im Cortex heißt er `Gedankenwelten/`) |
| `<dein-rag-server>` | einen eigenen RAG-Dienst (Qdrant + Embeddings, bei uns über n8n) — optional |
| `<server>`, `<dein-wiki>`, `<tailnet-adresse>` | den eigenen Server, die eigene Wiki, eine Adresse im eigenen Netz |

Manches ist an die Cortex-Umgebung gebunden und läuft bei dir erst mit Ersatz oder gar nicht:
das Logging (`Cortex-Log.md`, `journal/`, `index.md`, `Opus/OVERVIEW.md`), der Deploy auf einen eigenen
Server, die RAG-Suche über den Bestand. **Lesend über den ganzen Bestand suchen** kannst du ohne eigene
Infrastruktur über den öffentlichen MCP-Server: `https://mcp.gedankenwelten.org/mcp`.

Einige Skills verweisen auf Werkzeuge, die privat bleiben (Leserstatistik, Nachrichten-Kuration, der
nächtliche Video-Späher, Server-Pflege) — die Verweise darfst du überlesen.

Schlüssel liegen nie im Code: Skripte lesen sie aus der Umgebung (`FAL_KEY` für Banner über fal.ai,
`SEMANTIC_SCHOLAR_API_KEY` optional für die Forschungssuche, `CORTEX_OPENALEX_MAILTO` für OpenAlex).

## Was drin ist

**Die Pipeline:** `gedankenwelt` (vom Video, Podcast oder Artikel zur fertigen Note) mit `aristoteles`
(Tiefenanalyse), den Agenten `humboldt` (Menschen hinter der Note, DenkerVita), `sherlock` (Faktencheck)
und `montaigne` (Verbindungen), dazu `sokrates` (Fragen), `gedankenpoesie` (Stimme und Wandspruch),
`gedankenart` (das Banner), `galilei` (Forschung mit DOI), `heraklit` (eine Note vertiefen).

**Schreiben und Denken:** `pascal` (eigene Gedanken), `epikur` (gute Nachrichten), `deeptalk` (Denkgespräch).

**Finden:** `gedankenarchiv`, `gedankenglobal`, `sepia`, `kurato`, `kairos`.

**Pflege:** `gedankenwelten-links`, `geistesblitzumzug`, `gedankenwelt-kurator`, `cortex-lint`.

**Regeln:** `haltung.md` (die Seele: wie hier gedacht und gesprochen wird — zuerst lesen),
`gedankenwelten.md`, `pipeline.md`, `tags.md`, `web-recherche.md`. **Playbooks:** Spuren,
Influencer-Kompass, Atelier.

## Lizenz

Wie der Code in diesem Repo: MIT. Die Notes: CC BY-SA 4.0. Wer etwas daraus macht, darf es gern erzählen.
