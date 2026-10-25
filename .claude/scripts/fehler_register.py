#!/usr/bin/env python3
"""
fehler_register.py — das Gedächtnis von /aristarch: jeder gefundene Fehler eine Zeile.

Seit 25.10.2026 (Andreas: „wo wir fehler festhalten, die erkannt werden … vielleicht erkennen wir
wiederkehrende vermeidbare fehler"). Wozu: Ein einzelner Fehler wird korrigiert, ein Muster wird an der
Quelle abgestellt — als Regel dort, wo der Fehler entsteht (Skill, Pipeline, Prompt), nicht als
Nachlauf. Darum feste Felder statt Fließtext: nur so lässt sich zählen.

  fehler_register.py eintragen --note "content/Zeitgeist/X.md" --schwere rot \\
      --kategorie zitat-sprecher --urheber wir --ursache interviewer-verwechselt \\
      --was "Satz von Jung stand als Satz von X" --korrektur "X zugeordnet → Jung" [--herkunft pipeline]
  fehler_register.py auswertung [--tage 90]     # Muster: was wiederholt sich, was davon ist unseres
  fehler_register.py liste [--note TEIL]        # die letzten Einträge

Datei: .claude/data/aristarch/fehler.jsonl (eine JSON-Zeile je Fehler, append-only).
"""
import argparse, json, sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATEI = ROOT / ".claude" / "data" / "aristarch" / "fehler.jsonl"

SCHWERE = ["rot", "orange", "gelb", "riskant", "klein"]          # 🔴 🟠 🟡 ⚖️ ⚪
KATEGORIE = ["zitat-wortlaut", "zitat-sprecher", "zeitmarke", "name", "zahl", "datum", "zuordnung",
             "studie-doi", "eigene-einordnung", "faktencheck-urteil", "lebende-person", "veraltet",
             "link", "bild", "transkription", "sonstiges"]
URHEBER = ["sprecher", "wir", "transkript"]   # wer den Fehler in die Welt gesetzt hat
URSACHE = ["paraphrase-als-zitat", "interviewer-verwechselt", "txt-statt-vtt", "aus-gedaechtnis",
           "sekundaerquelle", "zusammengezogen", "zu-glatt-formuliert", "veraltet", "unbekannt", "sonstiges"]
HERKUNFT = ["pipeline", "altbestand", "vertiefung", "unbekannt"]   # frisch aus /gedankenwelt oder alt
ZEICHEN = dict(zip(SCHWERE, ["🔴", "🟠", "🟡", "⚖️", "⚪"]))


def lesen():
    if not DATEI.exists():
        return []
    return [json.loads(z) for z in DATEI.read_text(encoding="utf-8").splitlines() if z.strip()]


def eintragen(a):
    e = {"datum": date.today().isoformat(), "note": a.note,
         "rubrik": a.note.split("/")[1] if a.note.count("/") >= 2 else "",
         "schwere": a.schwere, "kategorie": a.kategorie, "urheber": a.urheber,
         "ursache": a.ursache if a.urheber == "wir" else "", "herkunft": a.herkunft,
         "was": a.was, "korrektur": a.korrektur, "korrigiert": not a.offen}
    DATEI.parent.mkdir(parents=True, exist_ok=True)
    with DATEI.open("a", encoding="utf-8") as f:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"{ZEICHEN[a.schwere]} eingetragen: {a.kategorie} · {a.urheber} · {Path(a.note).stem}")


def auswertung(a):
    alle = lesen()
    if a.tage:
        ab = (date.today() - timedelta(days=a.tage)).isoformat()
        alle = [e for e in alle if e["datum"] >= ab]
    if not alle:
        return print("Noch keine Einträge.")
    notes = {e["note"] for e in alle}
    wir = [e for e in alle if e["urheber"] == "wir"]
    print(f"FEHLER-REGISTER — {len(alle)} Fehler in {len(notes)} Notes"
          + (f" (letzte {a.tage} Tage)" if a.tage else "") + f", davon {len(wir)} unsere\n")
    print("Schwere:    " + " · ".join(f"{ZEICHEN[s]} {n}" for s, n in Counter(e["schwere"] for e in alle).most_common()))
    print("Urheber:    " + " · ".join(f"{k} {n}" for k, n in Counter(e["urheber"] for e in alle).most_common()))
    print("Herkunft:   " + " · ".join(f"{k} {n}" for k, n in Counter(e["herkunft"] for e in alle).most_common()))
    print("\nKategorien (alle):")
    for k, n in Counter(e["kategorie"] for e in alle).most_common():
        print(f"  {n:>3}  {k}")
    if wir:
        print("\nUnsere Fehler — Ursachen (hier liegt, was sich an der Quelle abstellen lässt):")
        for k, n in Counter(e["ursache"] or "unbekannt" for e in wir).most_common():
            print(f"  {n:>3}  {k}" + ("   ← Muster: Regel am Entstehungsort?" if n >= 3 else ""))
        frisch = [e for e in wir if e["herkunft"] == "pipeline"]
        if frisch:
            print(f"\n  Davon frisch aus /gedankenwelt: {len(frisch)} — "
                  + ", ".join(f"{k} {n}" for k, n in Counter(e["ursache"] or "unbekannt" for e in frisch).most_common(4)))
    je = Counter(e["rubrik"] for e in alle)
    print("\nRubriken:   " + " · ".join(f"{k} {n}" for k, n in je.most_common()))


def liste(a):
    alle = [e for e in lesen() if not a.note or a.note.lower() in e["note"].lower()]
    for e in alle[-a.n:]:
        print(f"{e['datum']}  {ZEICHEN[e['schwere']]} {e['kategorie']:<18} {e['urheber']:<10} "
              f"{Path(e['note']).stem[:50]}\n            {e['was']}  →  {e['korrektur']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="befehl", required=True)
    e = sub.add_parser("eintragen")
    e.add_argument("--note", required=True)
    e.add_argument("--schwere", required=True, choices=SCHWERE)
    e.add_argument("--kategorie", required=True, choices=KATEGORIE)
    e.add_argument("--urheber", required=True, choices=URHEBER)
    e.add_argument("--ursache", default="unbekannt", choices=URSACHE)
    e.add_argument("--herkunft", default="unbekannt", choices=HERKUNFT)
    e.add_argument("--was", required=True, help="was falsch dastand, ein Satz")
    e.add_argument("--korrektur", required=True, help="was jetzt dasteht, ein Satz")
    e.add_argument("--offen", action="store_true", help="gefunden, aber (noch) nicht korrigiert")
    w = sub.add_parser("auswertung")
    w.add_argument("--tage", type=int, default=0)
    l = sub.add_parser("liste")
    l.add_argument("--note", default="")
    l.add_argument("-n", type=int, default=20)
    a = ap.parse_args()
    {"eintragen": eintragen, "auswertung": auswertung, "liste": liste}[a.befehl](a)


if __name__ == "__main__":
    sys.exit(main())
