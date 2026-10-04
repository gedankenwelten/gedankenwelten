# Rules — Tag-Taxonomie

Kanonische Tags für den gesamten Cortex. Neue Tags nur anlegen wenn kein bestehender passt.

---

## Gedankenwelten — Tags

### Typ (Pflicht)
| Tag | Bedeutung |
|---|---|
| `zeitgeist` | Interview, Vortrag, Podcast — Geist der Zeit |
| `denker` | Tiefenanalyse eines Denkers / einer Denkerin |
| `gedanke` | Persönliche Reflexion |
| `panorama` | Thematische Synthese-Note — bündelt mehrere Notes zu einem Thema |
| `geistesblitz` | Grundsätzliches Wissen & menschliche Schöpferkraft — Wissenschaft, Philosophie, Psychologie, Technik. Erklärt die Welt und das Außergewöhnliche am Menschen (nicht tagesaktuell wie `zeitgeist`, nicht an eine Stimme gebunden wie `denker`). |
| `spur` | Lebende, investigative These-in-progress — *News als Prozess*. Ein Phänomen über die Zeit verfolgt, mit Falsifikationsbedingung, Verlauf und Gleichmut-Spiegel. Die einzige Rubrik mit Zeit-Dimension. → Playbook (on-demand): `.claude/playbooks/spuren.md` |
| `kultur` | Land und Leute, wie man sie selten zu sehen bekommt — gelebte Kultur, Alltag, das Fremde von innen. Durch Reisende, die wirklich hinsehen, oder Einheimische, die ihre Heimat erzählen. Nicht der *Diskurs* über ein Land (`zeitgeist`), nicht eine *Stimme* tief (`denker`), nicht *Wissen über die Welt* (`geistesblitz`) — das gelebte *Wie* eines Ortes. Erzählende, bildreiche Form, kein Faktencheck. |

### Format (optional)
| Tag | Bedeutung |
|---|---|
| `gespräch` | Dialog auf Augenhöhe — zwei gleichwertige Stimmen erkunden gemeinsam ein Thema. Kein klares Interviewer/Interviewter-Gefälle. Typisch: Co-Host-Formate (Die Neuen Zwanziger, Gilda con Arne), ausnahmsweise auch besonders dialogische Gastgespräche. |
| `kalender` | **Tagesnote** — aus dem Sinn eines besonderen Tages geboren (Welttag, Aktionstag, Gedenktag, Unabhängigkeitstag …), gewählt über `/kairos`. Sammelt alle Notes mit datiertem Anlass unter einem Dach — quer durch die Rubriken (meist `zeitgeist`, auch `kultur`/`geistesblitz`). Trägt den Anlass-Callout im Note-Kopf. Wird von `/kairos` automatisch vergeben. |
| `satire` | **Satire als Erkenntnisform** — Kabarett, Comedy und Satire, die einen Sachverhalt nicht kommentiert, sondern *aufschlüsselt* (Die Anstalt, ZDF Magazin Royale). Nur setzen, wo die satirische Form selbst das Argument trägt und belegt ist — nicht für jeden pointierten Beitrag. |

### Autor (Pflicht bei `gedanke` & `panorama`)

Persönliche Notes tragen einen **Autoren-Tag** — sie sind einer Stimme zuzuordnen, nicht bloß einer Quelle. Gilt für die Rubriken **Gedanken** und **Panorama** (nicht für Zeitgeist/Denker/Geistesblitz/Kultur — die verweisen auf externe Sprecher). Der Meta-Index `Panorama.md` bleibt ausgenommen.

| Tag | Autor |
|---|---|
| `luc` | **Andreas Schmieder** (Künstlername *Luc*) — der Betreiber des Cortex, Default-Autor persönlicher Notes |
| `claude` | von **Claude** verfasste Reflexionen (z.B. die „Claude — …"-Notes) |

Weitere Autoren, die künftig hinzukommen, erhalten je einen **eigenen** Tag (Künstler-/Klarname, kleingeschrieben). Der Autoren-Tag steht direkt nach dem Typ-Tag.

### Jahr (Pflicht bei Zeitgeist)
`year-2024`, `year-2025`, `year-2026`

### Thema (min. 1–3)

**Politik & Gesellschaft:**
`demokratie` · `autoritarismus` · `faschismus` · `kapitalismus` · `neoliberalismus` · `populismus` · `rechtsextremismus` · `widerstand`

**USA / International:**
`usa` · `trump` · `oligarchie` · `geopolitik` · `migration` · `immigration`

**Deutschland:**
`deutschland` · `afd` · `bundesregierung` · `energiepolitik` · `wahlen`

**KI & Technologie:**
`ki` · `anthropic` · `claude` · `technologie` · `überwachung` · `datenschutz`

**Philosophie & Denken:**
`philosophie` · `psychologie` · `ethik` · `erkenntnistheorie` · `buddhismus` · `vipassana` · `paradox` · `komplexität` · `dialogique`

> `paradox` · `komplexität` · `dialogique` sind bewusst gesetzte **Verknüpfungsknoten** (roter Faden „Das Paradox", seit 01.07.2026). `dialogique` = Morins *principe dialogique* (zwei nötige, gegensätzliche Logiken ohne Synthese zusammenhalten). Auf thematisch tragende Notes setzen, nicht streuen.

**Wirtschaft:**
`wirtschaft` · `inflation` · `schulden` · `soziale-ungleichheit` · `wohnen`

> `drogenpolitik` = Drogenhilfe, Schadensminderung, Drug-Checking, Konsumräume, Kriminalisierung vs. Gesundheitsansatz — gesetzt mit [[Mark Benecke — Zu Besuch in der Drogenhilfe Halle]] (zusammen mit `sucht`).

> `wohnen` = Wohnungsmarkt, Mieten, Bodenpreise, sozialer Wohnungsbau, Eigentum an Wohnraum — gesetzt mit [[Die Anstalt — Warum Wohnen unbezahlbar wird]].

**Medien:**
`medien` · `propaganda` · `desinformation` · `meinungsfreiheit` · `symbole`

> `symbole` = Zeichen, Gesten und ihre Deutungskämpfe (Kaperung, Rückeroberung, Codes) — gesetzt mit [[Panorama/Gekaperte Zeichen]].

**Kultur & Welt** (für `kultur`-Notes):
`reise` · `alltag` · `tradition` · `religion` · `kulinarik` · `gastfreundschaft` · Region als Land-Tag (`jemen`, `iran`, `indien` …)

---

## Opus — Tags

### Typ (Pflicht)
| Tag | Bedeutung |
|---|---|
| `methodik` | Workflows, Wissensmanagement, Produktivität |
| `homeserver` | Raspberry Pi, Self-Hosting, Infrastruktur |
| `projekt` | FunnyProducts, Breathe, konkrete Projekte |
| `life` | Persönliche Notizen, Veranstaltungen |

### Technik
`docker` · `tailscale` · `vpn` · `dns` · `caddy` · `nginx` · `ubuntu` · `raspberry-pi`

### KI & Werkzeuge
`ki` · `claude-code` · `llm` · `embeddings` · `rag` · `obsidian` · `zweites-gehirn`

### PKA / Methodik
`pka` · `pkm` · `context-engineering` · `hooks` · `sub-agents`

---

## Regeln

- Tags in **Kleinbuchstaben mit Bindestrich** (`ki-modelle`, nicht `KI Modelle`)
- Kein Tag für einzelne Personen (Personenname gehört in den Titel, nicht als Tag)
- **Opus:** Maximal 5 Tags pro Note — lieber weniger, treffender
- **Gedankenwelten:** Kein hartes Limit — Tags dienen der Auffindbarkeit auf gedankenwelten.org. Trotzdem nur relevante Tags, kein Spam.
- `meta` und `index` nur für Struktur-Dateien (Opus.md, OVERVIEW.md etc.)
