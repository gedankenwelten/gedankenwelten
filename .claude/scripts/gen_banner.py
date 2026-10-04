#!/usr/bin/env python3
"""
gen_banner.py — Gedankenwelten-Banner über die fal.ai-API generieren.

Erzeugt ein 1216x512-Bild (FLUX.2 Pro, alternativ Recraft V3 für grafische
Linien-Stile), croppt zentriert auf exakt 1200x500 und legt es als JPEG in
content/assets/ ab.

Nutzung:
    python3 .claude/scripts/gen_banner.py \
        --prompt "Persian miniature painting ..." \
        --out "Soroush-und-Heck-Politische-Tradition-des-Islam-banner"
        [--model flux|recraft]        (Default: flux)
        [--style <recraft-style>]     (nur recraft, Default: digital_illustration)
        [--dry-run]                   (nur Request zeigen, nichts senden)

Der API-Key kommt aus FAL_KEY in <vault>/.env (nie im Chat/Repo!).
Kosten: ~2-4 ct pro Bild (Stand 07/2026). Ausgabe: Pfad des fertigen Assets.
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request

CORTEX = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS = os.path.join(CORTEX, "content", "assets")
GEN_W, GEN_H = 1216, 512   # Vielfache von 32 (API-Anforderung)
OUT_W, OUT_H = 1200, 500   # Banner-Zielformat

ENDPOINTS = {
    "flux": "https://queue.fal.run/fal-ai/flux-2-pro",
    "recraft": "https://queue.fal.run/fal-ai/recraft/v3/text-to-image",
}


def load_key() -> str:
    env_path = os.path.join(CORTEX, ".env")
    with open(env_path) as f:
        for line in f:
            if line.startswith("FAL_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("FEHLER: FAL_KEY nicht in .env gefunden.")


def api(url: str, key: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"},
        method="POST" if payload is not None else "GET",
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


JOBLOG = os.path.join(CORTEX, ".claude", "data", "fal-jobs.jsonl")


def log_request(rid: str, model: str, prompt: str, response_url: str) -> None:
    """Jede Einreichung protokollieren — ein Timeout darf ein Ergebnis nie verlieren.

    Am 01.08.2026 galten zehn Läufe als „FLUX ist tot", waren aber nur Queue-Wartezeit
    (Rechenzeit 7–38 s, Queue 11–32 min). Die Bilder lagen fertig da, ohne dass jemand
    die request_id hatte. Abholen: `python3 .claude/scripts/fal_fetch.py <request_id>`.
    """
    try:
        os.makedirs(os.path.dirname(JOBLOG), exist_ok=True)
        rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "request_id": rid,
               "model": model, "response_url": response_url, "prompt": prompt}
        with open(JOBLOG, "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError:
        pass  # Protokoll ist Komfort, kein Grund den Lauf abzubrechen


def generate(model: str, prompt: str, style: str, key: str, wait: int = 180) -> str:
    """Startet den Queue-Job und liefert die Bild-URL zurück.

    `wait` = maximale Wartezeit in Sekunden. Der fal.ai-Queue ist zeitweise
    tausende Jobs tief (FLUX am 01.08.2026: Position 1097) — dann reichen die
    drei Default-Minuten nicht und `--wait 1800` ist der richtige Griff.
    """
    payload = {
        "prompt": prompt,
        "image_size": {"width": GEN_W, "height": GEN_H},
    }
    if model == "recraft":
        payload["style"] = style
    sub = api(ENDPOINTS[model], key, payload)
    status_url, response_url = sub["status_url"], sub["response_url"]
    rid = sub.get("request_id", "?")
    if (pos := sub.get("queue_position")) is not None:
        print(f"   Warteposition: {pos}", file=sys.stderr)
    log_request(rid, model, prompt, response_url)
    print(f"   request_id: {rid}", file=sys.stderr)

    deadline = time.monotonic() + wait
    last_note = 0.0
    while time.monotonic() < deadline:
        time.sleep(2)
        st = api(status_url, key)
        if st.get("status") == "COMPLETED":
            break
        if st.get("status") in ("FAILED", "ERROR"):
            sys.exit(f"FEHLER: Generierung fehlgeschlagen: {st}")
        if (elapsed := time.monotonic() - (deadline - wait)) - last_note >= 60:
            last_note = elapsed
            print(f"   … {int(elapsed)}s, Status {st.get('status')}", file=sys.stderr)
    else:
        sys.exit(f"FEHLER: Timeout nach {wait}s (Queue zu tief — mit --wait erhöhen).")

    result = api(response_url, key)
    images = result.get("images") or []
    if not images:
        sys.exit(f"FEHLER: Keine Bilder in der Antwort: {result}")
    return images[0]["url"]


def download_and_crop(url: str, out_name: str, no_crop: bool = False,
                      png: bool = False, out_dir: str | None = None) -> str:
    target_dir = out_dir or ASSETS
    os.makedirs(target_dir, exist_ok=True)
    tmp = f"/tmp/gen_banner_{os.getpid()}.png"
    urllib.request.urlretrieve(url, tmp)

    ext = "png" if png else "jpg"
    out_path = os.path.join(target_dir, f"{out_name}.{ext}")
    if no_crop:
        if png:
            os.replace(tmp, out_path)
            return out_path
        vf_args = []
    else:
        off_x, off_y = (GEN_W - OUT_W) // 2, (GEN_H - OUT_H) // 2
        vf_args = ["-vf", f"crop={OUT_W}:{OUT_H}:{off_x}:{off_y}"]
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, *vf_args,
         "-q:v", "2", out_path],
        check=True,
    )
    os.remove(tmp)
    return out_path


def main():
    p = argparse.ArgumentParser(description="Gedankenwelten-Banner via fal.ai")
    p.add_argument("--prompt", required=True)
    p.add_argument("--out", required=True, help="Asset-Name ohne Endung (Note-Slug + -banner)")
    p.add_argument("--model", choices=list(ENDPOINTS), default="flux")
    p.add_argument("--style", default="digital_illustration",
                   help="Recraft-Style (z.B. digital_illustration, vector_illustration)")
    p.add_argument("--width", type=int, default=None, help="Generierbreite (Vielfaches von 32)")
    p.add_argument("--height", type=int, default=None, help="Generierhöhe (Vielfaches von 32)")
    p.add_argument("--no-crop", action="store_true",
                   help="Rohbild ohne 1200x500-Crop speichern (z.B. Wortmarken)")
    p.add_argument("--png", action="store_true", help="Als PNG statt JPEG speichern")
    p.add_argument("--dir", default=None, help="Zielordner (Default: content/assets)")
    p.add_argument("--wait", type=int, default=180,
                   help="Max. Wartezeit in Sekunden (Default 180; bei tiefem fal-Queue z.B. 1800)")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    global GEN_W, GEN_H
    if args.width:
        GEN_W = args.width
    if args.height:
        GEN_H = args.height

    if args.dry_run:
        print(json.dumps({"endpoint": ENDPOINTS[args.model], "prompt": args.prompt,
                          "image_size": {"width": GEN_W, "height": GEN_H}}, indent=2))
        return

    key = load_key()
    print(f"→ [{args.model}] generiere {GEN_W}x{GEN_H} …", file=sys.stderr)
    url = generate(args.model, args.prompt, args.style, key, wait=args.wait)
    out = download_and_crop(url, args.out, no_crop=args.no_crop, png=args.png, out_dir=args.dir)
    print(out)


if __name__ == "__main__":
    main()
