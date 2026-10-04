---
name: gedankenglobal
description: Entdeckt globale, nicht-westliche Denkerinnen und Denker für die Gedankenwelten — arbeitet mit dem Globale-Stimmen-Backlog, präsentiert einen Kandidaten nach dem anderen und gräbt bei Bedarf neue Stimmen jenseits des westlichen Such-Bias aus. Bei Zuschlag Switch auf den gedankenwelt-Skill. Trigger — "/gedankenglobal", "gedankenglobal", "globale stimmen", "globale denker".
---

# Gedankenglobal — Globale Stimmen entdecken

> *Die Gedankenwelten sollen über die westliche Bubble hinaus denken — andere Ontologien, andere Diagnosen, andere Zukunftsentwürfe. Claude versteht alle Sprachen und dient als Brücke: Die Muttersprache eines Denkers ist kein Ausschlusskriterium.*

Interaktive Entdecker-Session wie das Gedankenarchiv, aber mit eigenem Kompass: **nicht-westliche und globale Denkerinnen und Denker**. Arbeitsgedächtnis ist das bestehende Backlog — der Skill liest es, präsentiert Kandidaten, pflegt es und gräbt bei Bedarf neue Stimmen aus.

## Trigger

- `/gedankenglobal` (optional mit Richtung: `/gedankenglobal Lateinamerika`, `/gedankenglobal neue Stimmen`)
- "globale stimmen", "globale denker", "nicht-westliche denker"

## Arbeitsgedächtnis (immer zuerst laden)

```bash
cat "Gedankenwelten/Globale Stimmen - Backlog.md"
```

Das Backlog enthält: ✅ Verarbeitet · 📋 Warteschlange (hoch/mittel, mit kuratierten Video-Tabellen) · 💡 Ideen für später · 🌍 Westliche Lücken · und die **Werkzeugtabelle gegen den Such-Bias** (Bilibili, Wikipedia ja/ar, Naver, Berggruen/Kyoto/Tang Prize, YouTube in Zielsprache).

---

## Routing

```
→ [CLAUDE] Kuration + Kandidaten-Urteil | kulturelle Nuance erforderlich
→ [LOCAL: curl/jina] Websuche, Videosuche, Preis-Listen
```

---

## Schritt 1 — Modus wählen

Zwei Modi, je nach Stimmung des Users (im Zweifel kurz fragen):

| Modus | Was passiert |
|---|---|
| **🎯 Aus der Warteschlange** (Default) | Kandidaten aus dem Backlog präsentieren — die Recherche ist dort schon kuratiert |
| **🔭 Neue Stimmen ausgraben** | Mit den Bias-freien Werkzeugen neue Denker finden und ins Backlog aufnehmen |

Richtungs-Argument (`Lateinamerika`, `islamische Philosophie`, `Afrika` …) filtert beide Modi.

## Schritt 2a — Modus Warteschlange

Kandidaten in dieser Reihenfolge anbieten:
1. **Priorität hoch** (im Backlog markiert)
2. **Mittlere Priorität**
3. **Ideen für später** (hier erst kurz nachrecherchieren: lebt die Person noch? gibt es gute Videos?)
4. **Westliche Lücken** nur erwähnen, wenn der User explizit auch westliche Stimmen will

**Einen Kandidaten pro Runde** präsentieren — das „Warum?" aus dem Backlog ist die Basis, aber mit eigenem Urteil anreichern: Anknüpfungspunkte an bestehende Notes nennen (z.B. Tianxia ↔ Geopolitik-Notes, Ch'ixi ↔ Yin-Yang-Gedanke). Format:

```
🌍 Kandidat: [Name] — [Herkunft]

[Warum diese Stimme die Gedankenwelten bereichert — 2–4 Sätze,
inkl. Brücken zu bestehenden Notes/Denkern]

**Sprache:** [Sprache(n)] · **Passend für:** [Rubrik]

📺 Bester Einstieg:
| Titel | Kanal | Jahr | Link |
[1–3 Videos aus dem Backlog, bestes zuerst — Verfügbarkeit kurz prüfen]

→ Nehmen wir [Name]? (ja / nächster / Modus wechseln)
```

## Schritt 2b — Modus Neue Stimmen

Die Werkzeugtabelle aus dem Backlog nutzen — **nicht** einfach Google/Ecosia auf Englisch, das reproduziert den Bias:

- **Preis-Listen** (Berggruen, Kyoto, Tang) per Jina/Defuddle abrufen → Laureates gegen Backlog + `known-speakers.md` abgleichen
- **Wikipedia in Zielsprache** (ja/ar/es/zh) für Kontext zu einem Namen
- **YouTube/Bilibili in Zielsprache** für verfügbare Vorträge (yt-dlp kann Bilibili)
- Ergänzend: archive.org für historische Stimmen des Globalen Südens (→ Mechanik wie im Skill `gedankenarchiv`)

**Kompass für die Auswahl:**
- ✅ Eigenständige Denktradition oder Perspektive, die im Korpus fehlt (nicht: westliche Thesen mit anderem Pass)
- ✅ Substanzielle Vorträge/Interviews verfügbar (Sprache egal — Claude übersetzt)
- ✅ Regionale Vielfalt im Blick: Was fehlt? (Afrika südlich der Sahara, Südostasien, Ozeanien, indigene Stimmen …)
- ❌ Personen, die nur *über* den Globalen Süden sprechen, statt aus ihm heraus

Jeden ernsthaften Neufund **ins Backlog eintragen** (gleiche Struktur: Warum? / Sprache / Hauptwerke / Video-Tabelle) — auch wenn er heute nicht gewählt wird. Das Backlog ist der bleibende Wert der Session. `aktualisiert:` im Backlog-Frontmatter bumpen.

## Schritt 3 — Switch auf den gedankenwelt-Skill

Bei Zuschlag endet Gedankenglobal und **der Skill `gedankenwelt` wird invoked** (Skill-Tool, mit dem gewählten Video-Link als Argument). Dem Switch mitgeben:

- **Sprache des Materials** — bei nicht-deutschem/englischem Material: Transkription mit mlx-whisper `--language XX`; die Note entsteht auf Deutsch, Claude ist die Brücke. Originalzitate zweisprachig bringen (Original + Übersetzung).
- **Rubrik-Hinweis** aus dem Backlog (Zeitgeist vs. Denker — globale Stimmen mit eigenem Denkgebäude sind oft Denker-Material)
- **Katalog:** Die Note gehört in `Gedankenwelten.md` zusätzlich in die Sektion **„Globale Stimmen"**
- **DenkerVita:** Humboldt wie üblich — bei nicht-westlichen Denkern auch nicht-englische Quellen nutzen (Wikipedia in Zielsprache)

## Schritt 4 — Backlog pflegen (nach Abschluss der Pipeline)

Wenn die Note fertig ist:
1. Kandidat von der Warteschlange nach **✅ Verarbeitet** verschieben (mit Note-Link)
2. Fußzeile *„Zuletzt aktualisiert"* + nächste Priorität anpassen
3. `aktualisiert:` im Frontmatter bumpen

---

## Qualitätsfilter

- ✅ Originalstimmen mit eigenem Denkgebäude — Vorträge, lange Interviews, Vorlesungen
- ✅ Perspektiven, die westliche Selbstverständlichkeiten produktiv irritieren
- ❌ Reine Sekundär-Erklärvideos über einen Denker (außer als Einstiegs-Ergänzung)
- ❌ Exotisierung — eine Stimme zählt wegen ihres Denkens, nicht wegen ihrer Herkunft allein
- Yin-Yang-Grundsatz gilt: auch globale Stimmen kritisch lesen, Sherlock-Faktencheck wie immer
