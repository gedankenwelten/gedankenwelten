#!/usr/bin/env python3
"""
systemone — die gemeinsame Schnittstelle zu System-One-Modellen (Jev) für Cortex.

Ein System-One-Modell schreibt keinen Text, es *ordnet ein*: Es liest einen Text (`state`) und
beantwortet typisierte Fragen mit einer Wahrscheinlichkeit — `noul` (ja/nein), `choice` (eine aus
einer Liste), `score` (auf einer Skala). Schnell (~0,3 s), billig (~0,00005 $ je Abschnitt).
→ Ideenschmiede „System-One-Modelle", Memory `project_jev_system_one`.

Eine Schnittstelle statt verstreuter API-Aufrufe: Fällt der Anbieter weg, tritt hier ein anderes
Modell ein (Laya lokal, Gemma), ohne dass Sherlock, Galilei oder Diogenes etwas merken.

Drei Regeln, gelernt am 23. und 26.09.2026 — vor jeder neuen Frage lesen:
  1. **Vorkommen, nicht Rollen.** „Kommt X vor?" trägt (Los-Sieb: fast vollständig). „Welche Rolle
     spielt X?" oder „Stützt der Text die These?" holt die Grundstimmung des Textes herein, mit
     falscher Sicherheit. Verhältnisse beurteilt ein Sprachmodell oder der Mensch.
  2. **Nur öffentlicher Text.** Der Anbieter sitzt in den USA, ohne Speicher-Zusage. Nie Garten-
     Einsendungen, owner-inbox, Life, Fallakten, Persönliches.
  3. **Kriterien in die Frage, nie in den Text.** Fremde Seiten können versuchen, die Antwort zu
     steuern (Prompt Injection über den `state`).
  Und: Jev *sortiert und torwächtert*, es urteilt nie. Sein Ausgang ist ein Kandidat, kein Befund.

Backend: OpenRouter `POST /api/v1/systemone`, Modell `typesafe/jev-1.13`, Key `OPEN_ROUTER_API_KEY`.
Nur Python-Standardbibliothek — läuft auf Mac und Pi.

Als Modul:
  from systemone import frage, vorkommen
  a = frage(text, {"typ": {"type": "choice", "instructions": "…", "criteria": {"a": "…", "b": "…"}}})
  p = vorkommen(text, "Wird über Losverfahren gesprochen?")          # → 0.0 … 1.0

Als Werkzeug (z.B. für Sherlock — viele Seiten vorsieben, nur die tragenden lesen):
  python3 systemone.py ja "Enthält die Seite eine Zahl zu X?" seite1.md seite2.md …
  python3 systemone.py json '{"typ": {…}}' datei.txt
  (statt Dateien: `-` liest einen Text von stdin)
"""
import concurrent.futures as cf
import json
import os
import sys
import time
import urllib.error
import urllib.request

URL = "https://openrouter.ai/api/v1/systemone"
MODELL = "typesafe/jev-1.13"
MAX_ZEICHEN = 60000  # ~32K Token Kontext inkl. Frage; darüber wird gekürzt


def _env(name, default=""):
    """Umgebung, sonst Cortex-`.env` (quote-aware) — damit auch Cron-Läufe den Key finden."""
    if os.environ.get(name):
        return os.environ[name]
    for pfad in (os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env"), os.path.expanduser("~/.env")):
        try:
            with open(pfad, encoding="utf-8") as fh:
                for zeile in fh:
                    zeile = zeile.strip()
                    if zeile.startswith(name + "="):
                        v = zeile.split("=", 1)[1].strip()
                        if len(v) >= 2 and v[0] in "\"'" and v[-1] == v[0]:
                            v = v[1:-1]
                        return v
        except OSError:
            continue
    return default


def frage(state, questions, modell=MODELL, versuche=6):
    """Schickt einen Text mit typisierten Fragen. Gibt {"answers": …, "cost": …} zurück.
    Wiederholt bei Überlast (429/5xx) mit wachsender Pause; wirft RuntimeError sonst."""
    key = _env("OPEN_ROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPEN_ROUTER_API_KEY fehlt (Cortex-.env)")
    body = json.dumps({"model": modell, "state": state[:MAX_ZEICHEN], "questions": questions}).encode()
    fehler = ""
    for i in range(versuche):
        req = urllib.request.Request(URL, data=body, headers={
            "Authorization": "Bearer " + key, "Content-Type": "application/json"})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=60))
            return {"answers": r["answers"], "cost": (r.get("usage") or {}).get("cost", 0)}
        except urllib.error.HTTPError as e:
            fehler = f"{e.code} {e.read().decode(errors='replace')[:200]}"
            if e.code not in (429, 500, 502, 503, 520):
                break
        except (urllib.error.URLError, TimeoutError) as e:
            fehler = str(e)
        time.sleep(3 * (i + 1))
    raise RuntimeError(f"systemone: {fehler}")


def wahrscheinlichkeit(antwort):
    """noul/boolean-Antwort → Zahl (die Schnittstellen benennen das Feld verschieden)."""
    return antwort.get("noul", antwort.get("probability", 0.0))


def vorkommen(state, frage_text):
    """Die Frageform, die trägt: Kommt X im Text vor? → Wahrscheinlichkeit 0…1."""
    r = frage(state, {"x": {"type": "noul", "instructions": frage_text}})
    return wahrscheinlichkeit(r["answers"]["x"])


def viele(texte, questions, parallel=16):
    """Dieselben Fragen an viele Texte, parallel. Gibt Liste von Ergebnissen (oder {"error": …})."""
    def eins(t):
        try:
            return frage(t, questions)
        except RuntimeError as e:
            return {"error": str(e)}
    with cf.ThreadPoolExecutor(parallel) as ex:
        return list(ex.map(eins, texte))


def _lies(pfade):
    for p in pfade:
        if p == "-":
            yield "stdin", sys.stdin.read()
        else:
            with open(p, encoding="utf-8", errors="replace") as fh:
                yield p, fh.read()


def main():
    if len(sys.argv) < 4 or sys.argv[1] not in ("ja", "json"):
        print(__doc__.split("Als Werkzeug")[1].strip())
        sys.exit(2)
    modus, arg, dateien = sys.argv[1], sys.argv[2], sys.argv[3:]
    namen, texte = zip(*_lies(dateien))
    if modus == "ja":
        qs = {"x": {"type": "noul", "instructions": arg}}
        erg = viele(texte, qs)
        zeilen = []
        for n, e in zip(namen, erg):
            p = wahrscheinlichkeit(e["answers"]["x"]) if "answers" in e else None
            zeilen.append((p if p is not None else -1, n, e.get("error", "")))
        for p, n, err in sorted(zeilen, reverse=True):
            print(f"{p:5.2f}  {n}" if p >= 0 else f"  —    {n}  ({err[:80]})")
    else:
        erg = viele(texte, json.loads(arg))
        print(json.dumps(dict(zip(namen, erg)), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
