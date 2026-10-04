#!/usr/bin/env python3
"""Fertige fal.ai-Jobs nachträglich abholen.

Hintergrund (01.08.2026): Die fal-Queue für `flux-2-pro` steht zeitweise still und
wird dann in einem Schwung durchgelassen — Rechenzeit 7–38 s, Wartezeit 11–32 min.
Das 3-Minuten-Fenster in `gen_banner.py` hat daraus zehnmal ein „FLUX antwortet nicht"
gemacht, obwohl die Bilder kurz darauf fertig dalagen. Kein Job geht verloren; man
braucht nur die request_id oder die Historie.

    # Was liegt in einem Zeitraum? (Default: heute)
    python3 .claude/scripts/fal_fetch.py --list
    python3 .claude/scripts/fal_fetch.py --list --von 2026-07-25 --bis 2026-08-02

    # Einen bestimmten Job abholen
    python3 .claude/scripts/fal_fetch.py <request_id> --out mein-banner

    # Alles aus einem Zeitraum in einen Ordner sichern
    python3 .claude/scripts/fal_fetch.py --list --von 2026-08-01 --hole /tmp/fal

Ohne --out landen Bilder im Zielordner (Default: Scratchpad-nahes /tmp/fal-fetch),
nicht in content/assets — die Ablage bleibt eine bewusste Entscheidung.
"""

import argparse
import datetime as dt
import json
import os
import sys
import urllib.request

CORTEX = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HISTORY = "https://rest.alpha.fal.ai/requests/"
QUEUE = "https://queue.fal.run"


def load_key() -> str:
    with open(os.path.join(CORTEX, ".env")) as f:
        for line in f:
            if line.startswith("FAL_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("FEHLER: FAL_KEY fehlt in <vault>/.env")


def get(url: str, key: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Key {key}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def history(key: str, von: str, bis: str) -> list[dict]:
    url = f"{HISTORY}?start_time={von}T00:00:00Z&end_time={bis}T00:00:00Z"
    items = get(url, key).get("items", [])
    return sorted(items, key=lambda i: i.get("queued_at", ""))


def bild_url(rec: dict) -> str | None:
    imgs = (rec.get("json_output") or {}).get("images") or []
    return imgs[0]["url"] if imgs else None


def hole(url: str, ziel: str) -> str:
    os.makedirs(os.path.dirname(ziel) or ".", exist_ok=True)
    urllib.request.urlretrieve(url, ziel)
    return ziel


def main() -> None:
    p = argparse.ArgumentParser(description="Fertige fal.ai-Jobs nachträglich abholen")
    p.add_argument("request_id", nargs="?", help="Einzelnen Job abholen")
    p.add_argument("--endpoint", default="fal-ai/flux-2-pro",
                   help="Nur für Einzelabruf per request_id")
    p.add_argument("--list", action="store_true", help="Historie auflisten")
    p.add_argument("--von", default=None, help="Startdatum YYYY-MM-DD (Default: heute)")
    p.add_argument("--bis", default=None, help="Enddatum YYYY-MM-DD (Default: morgen)")
    p.add_argument("--hole", metavar="ORDNER", default=None,
                   help="Alle gelisteten Bilder in diesen Ordner laden")
    p.add_argument("--out", default=None, help="Zieldatei für den Einzelabruf")
    args = p.parse_args()

    key = load_key()
    heute = dt.date.today()
    von = args.von or heute.isoformat()
    bis = args.bis or (heute + dt.timedelta(days=1)).isoformat()

    if args.request_id:
        rec = get(f"{QUEUE}/{args.endpoint}/requests/{args.request_id}", key)
        if rec.get("detail"):
            sys.exit(f"Noch nicht fertig: {rec['detail']}")
        url = bild_url(rec)
        if not url:
            sys.exit(f"Kein Bild in der Antwort: {json.dumps(rec)[:300]}")
        ziel = args.out or f"/tmp/fal-fetch/{args.request_id[:8]}.jpg"
        if not ziel.endswith((".jpg", ".png")):
            ziel += ".jpg"
        print(hole(url, ziel))
        return

    if not args.list:
        p.error("Entweder eine request_id oder --list angeben.")

    items = history(key, von, bis)
    print(f"{len(items)} Requests {von} … {bis}"
          f"{'  (API-Limit 50 pro Abfrage)' if len(items) >= 50 else ''}\n")
    for i in items:
        url = bild_url(i)
        q = i.get("queued_at", "")[:19].replace("T", " ")
        mark = "🖼" if url else "  "
        print(f"{mark} {q}Z  {i['request_id'][:8]}  {i.get('status_code')}  "
              f"{i['endpoint'][:28]:28s}  {(i.get('json_input') or {}).get('prompt','')[:60]}")
        if url and args.hole:
            ziel = os.path.join(args.hole, f"{i['request_id'][:8]}.jpg")
            hole(url, ziel)
            print(f"     → {ziel}")


if __name__ == "__main__":
    main()
