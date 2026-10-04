#!/usr/bin/env python3
"""Register der Nachbesprechungen — und die Frage, ob daraus ein Panorama wächst.

Eine Nachbesprechung (Pipeline-Schritt 5d) nimmt zwei, drei Themen einer Note noch einmal auf.
Führt ein Thema in ein wachsendes Panorama, ist es dort aufgehoben. Führt es nirgendwohin
(„Waise"), ginge es ohne Register verloren. Dieses Skript hält beide fest:

  extract   liest alle `## Nachbesprechung`-Abschnitte aus den Notes → .claude/data/nachbesprechungen.jsonl
            (die Note bleibt die einzige Wahrheit; das Register wird nur daraus gebaut)
  ingest    bettet jedes Thema ein → Qdrant-Collection `gedankenwelten_nachbesprechungen` (Hash-Skip)
  query     semantische Suche: „gab es schon eine Nachbesprechung zu …?"
  analyse   bündelt die Waisen und hält sie gegen die Fragen der wachsenden Panoramen:
            Kandidaten für ein neues Panorama (≥3 Themen aus ≥3 Notes), Waisen, die in ein
            bestehendes Panorama gehören könnten, und Einzelgänger.

Maschine sammelt, Mensch urteilt: `analyse` schlägt vor, es legt nichts an.

Eichung (29.09.2026, an den 14 Themen mit bekanntem Panorama, bge-m3-Kosinus):
  Thema ↔ Frage des eigenen Panoramas   Median 0,73 (min 0,42)
  Thema ↔ beste fremde Panorama-Frage    Median 0,57, max 0,66 (Schwester-Panorama)
  Thema ↔ Thema, gleiches Panorama       Median 0,53  ┐ überlappen — Thema-Thema-Nähe ist
  Thema ↔ Thema, verschiedene Panoramen  max 0,68    ┘ ein schwaches Signal
Darum beide Schwellen 0,70 (Präzision vor Vollständigkeit) und bei jeder Waise die nächsten
Nachbarn mit Zahl — das Urteil sieht, was knapp darunter liegt. Nachschärfen, wenn der Bestand wächst.

Embeddings: lokaler Mac-Embed-Server (bge-m3, http://localhost:11435/embed), Qdrant via SSH (Pi).
Muster und Helfer wie in cortex_memory.py.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.request
import uuid

PROJECT_DIR = pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR", "<vault>/"))
GW = PROJECT_DIR / "Gedankenwelten"
RUBRIKEN = ["Zeitgeist", "Denker", "Geistesblitz", "Kultur", "Gedanken", "Spuren", "GoodNews"]
REGISTER = PROJECT_DIR / ".claude" / "data" / "nachbesprechungen.jsonl"

EMBED_URL = "http://localhost:11435/embed"
SSH_HOST = "<server>"
QDRANT = "http://127.0.0.1:6333"
COLLECTION = "gedankenwelten_nachbesprechungen"
VECTOR_NAME = "text"
VECTOR_SIZE = 1024
NAMESPACE = uuid.UUID("6f1d3b2a-0000-4000-8000-00000000b5e7")  # nachbesprechungen
EMBED_BATCH = 16
MAX_EMBED_CHARS = 3000

# Panorama-Abschnitte, die keine Frage sind
PANORAMA_STRUKTUR = re.compile(
    r"^(Nachbesprechungen|Verbindungen|Weiterdenken|Notes|Offene Fragen|Warum dieses Thema|Externe Quellen)",
    re.I)


# ---------- Helfer ----------

def qdrant(method: str, path: str, body: dict | None = None) -> dict:
    cmd = ["ssh", "-o", "ConnectTimeout=10", SSH_HOST,
           "curl", "-s", "-X", method, f"'{QDRANT}{path}'",
           "-H", "'Content-Type: application/json'"]
    if body is not None:
        cmd += ["-d", "@-"]
    result = subprocess.run(cmd, input=json.dumps(body) if body is not None else None,
                            capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"SSH/Qdrant fehlgeschlagen: {result.stderr.strip()[:300]}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"Qdrant-Antwort kein JSON: {result.stdout[:300]}")


def embed(texts: list[str]) -> list[list[float]]:
    vecs: list[list[float]] = []
    for i in range(0, len(texts), EMBED_BATCH):
        batch = [t[:MAX_EMBED_CHARS] for t in texts[i:i + EMBED_BATCH]]
        req = urllib.request.Request(EMBED_URL, data=json.dumps({"texts": batch}).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=180) as resp:
            vecs.extend(json.load(resp)["embeddings"])
    return vecs


def cos(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            if v and not line.startswith(" "):
                fm[k.strip()] = v.strip().strip("\"'")
    return fm


def panorama_namen() -> set[str]:
    return {p.stem for p in (GW / "Panorama").glob("*.md")}


def link_ziele(text: str) -> list[str]:
    """[[Ziel#Anker|Text]] → 'Ziel' (ohne Pfad, ohne Anker)."""
    out = []
    for ziel in re.findall(r"\[\[([^\]|#]+)", text):
        out.append(ziel.strip().split("/")[-1])
    return out


def klartext(md: str) -> str:
    t = re.sub(r"\[\[[^\]|]+\|([^\]]+)\]\]", r"\1", md)          # [[x|y]] → y
    t = re.sub(r"\[\[([^\]#]+)(#[^\]]+)?\]\]", r"\1", t)          # [[x]] → x
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)                # [t](url) → t
    t = re.sub(r"https?://\S+", "", t)
    t = re.sub(r"[*_>`]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def iso(d: str) -> str:
    for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.datetime.strptime(d, fmt).date().isoformat()
        except ValueError:
            pass
    return d


# ---------- extract ----------

def themen_aus_note(pfad: pathlib.Path) -> list[dict]:
    text = pfad.read_text(encoding="utf-8")
    m = re.search(r"^## Nachbesprechung\s*$(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        return []
    fm = frontmatter(text)
    abschnitt = m.group(1)
    panos = panorama_namen()
    rel = str(pfad.relative_to(PROJECT_DIR))
    themen = []
    for tm in re.finditer(r"^### (.+?)\s*$(.*?)(?=^### |\Z)", abschnitt, re.S | re.M):
        frage, body = tm.group(1).strip(), tm.group(2)
        ziele = link_ziele(body)
        panoramen = sorted({z for z in ziele if z in panos})
        bestand = sorted({z for z in ziele if z not in panos and z != pfad.stem})
        klar = klartext(body)
        themen.append({
            "id": f"{rel}#{frage}",
            "note": rel,
            "note_titel": fm.get("title", pfad.stem),
            "rubrik": pfad.parent.name,
            "frage": frage,
            "anker": f"{pfad.stem}#{frage.replace(':', '')}",
            "datum": iso(fm.get("aktualisiert", "") or fm.get("date", "")),
            "status": "panorama" if panoramen else "waise",
            "panoramen": panoramen,
            "bestand": bestand,
            "woerter": len(klar.split()),
            "text": klar[:4000],
        })
    return themen


def cmd_extract(args) -> list[dict]:
    themen = []
    for rubrik in RUBRIKEN:
        for pfad in sorted((GW / rubrik).glob("*.md")):
            themen.extend(themen_aus_note(pfad))
    REGISTER.parent.mkdir(parents=True, exist_ok=True)
    with REGISTER.open("w", encoding="utf-8") as f:
        for t in themen:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")
    waisen = sum(t["status"] == "waise" for t in themen)
    noten = len({t["note"] for t in themen})
    print(f"{len(themen)} Themen aus {noten} Notes → {REGISTER.relative_to(PROJECT_DIR)} "
          f"({len(themen) - waisen} im Panorama, {waisen} Waisen)")
    return themen


def lade_register() -> list[dict]:
    if not REGISTER.exists():
        return cmd_extract(None)
    return [json.loads(l) for l in REGISTER.read_text(encoding="utf-8").splitlines() if l.strip()]


def embed_text(t: dict) -> str:
    return f"Frage: {t['frage']}\n{t['text']}"


# ---------- ingest ----------

def point_id(t: dict) -> str:
    return str(uuid.uuid5(NAMESPACE, t["id"]))


def content_hash(t: dict) -> str:
    return hashlib.sha1((embed_text(t) + t["status"]).encode("utf-8")).hexdigest()


def cmd_ingest(args) -> None:
    themen = cmd_extract(None) if not args.no_extract else lade_register()
    exists = any(c["name"] == COLLECTION
                 for c in qdrant("GET", "/collections")["result"]["collections"])
    if not exists:
        qdrant("PUT", f"/collections/{COLLECTION}",
               {"vectors": {VECTOR_NAME: {"size": VECTOR_SIZE, "distance": "Cosine"}}})
        print(f"Collection '{COLLECTION}' angelegt.")
    prior, offset = {}, None
    while exists:
        body = {"limit": 512, "with_payload": ["_hash"], "with_vector": False}
        if offset:
            body["offset"] = offset
        res = qdrant("POST", f"/collections/{COLLECTION}/points/scroll", body).get("result") or {}
        for p in res.get("points", []):
            prior[str(p["id"])] = (p.get("payload") or {}).get("_hash", "")
        offset = res.get("next_page_offset")
        if not offset:
            break
    aktuell = {point_id(t): t for t in themen}
    todo = [(pid, t) for pid, t in aktuell.items() if prior.get(pid) != content_hash(t)]
    stale = [pid for pid in prior if pid not in aktuell]
    if stale:
        qdrant("POST", f"/collections/{COLLECTION}/points/delete?wait=true", {"points": stale})
        print(f"{len(stale)} verschwundene Themen entfernt.")
    print(f"Zu embedden: {len(todo)} | unverändert: {len(aktuell) - len(todo)}")
    if todo:
        vecs = embed([embed_text(t) for _, t in todo])
        points = []
        for (pid, t), v in zip(todo, vecs):
            payload = {k: t[k] for k in t}
            payload["_hash"] = content_hash(t)
            points.append({"id": pid, "vector": {VECTOR_NAME: v}, "payload": payload})
        resp = qdrant("PUT", f"/collections/{COLLECTION}/points?wait=true", {"points": points})
        if resp.get("status") != "ok":
            raise RuntimeError(f"Upsert fehlgeschlagen: {json.dumps(resp)[:300]}")
    info = qdrant("GET", f"/collections/{COLLECTION}")
    print(f"Collection '{COLLECTION}': {info['result']['points_count']} Themen.")


# ---------- query ----------

def cmd_query(args) -> None:
    vec = embed([args.text])[0]
    body = {"query": vec, "using": VECTOR_NAME, "limit": args.limit, "with_payload": True}
    if args.waisen:
        body["filter"] = {"must": [{"key": "status", "match": {"value": "waise"}}]}
    pts = (qdrant("POST", f"/collections/{COLLECTION}/points/query", body).get("result") or {}).get("points", [])
    for p in pts:
        pl = p["payload"]
        print(f"[{p['score']:.3f}] {pl['status']:8} {pl['datum']}  {pl['frage']}")
        print(f"          [[{pl['anker']}]]")
    if not pts:
        print("Keine Treffer.")


# ---------- analyse ----------

def panorama_fragen() -> list[dict]:
    """Die ##-Fragen der wachsenden Panoramen, mit dem Anfang ihres Sachstands."""
    fragen = []
    for pfad in sorted((GW / "Panorama").glob("*.md")):
        text = pfad.read_text(encoding="utf-8")
        if "panorama-art: wachsend" not in text:
            continue
        titel = frontmatter(text).get("title", pfad.stem)
        for m in re.finditer(r"^## (.+?)\s*$(.*?)(?=^## |\Z)", text, re.S | re.M):
            kopf = m.group(1).strip()
            if PANORAMA_STRUKTUR.match(kopf):
                continue
            fragen.append({"panorama": pfad.stem, "titel": titel, "frage": kopf,
                           "text": f"Frage: {kopf}\n{klartext(m.group(2))[:1500]}"})
    return fragen


def cmd_analyse(args) -> None:
    themen = cmd_extract(None)
    waisen = [t for t in themen if t["status"] == "waise"]
    fragen = panorama_fragen()
    print(f"{len(fragen)} Panorama-Fragen in {len({f['panorama'] for f in fragen})} wachsenden Panoramen.\n")
    if not waisen:
        print("Keine Waisen — jedes Thema hat ein Panorama.")
        return
    vw = embed([embed_text(t) for t in waisen])
    vf = embed([f["text"] for f in fragen]) if fragen else []

    # 1) Bündel unter den Waisen (Single-Linkage über der Schwelle)
    n = len(waisen)
    eltern = list(range(n))

    def wurzel(i):
        while eltern[i] != i:
            eltern[i] = eltern[eltern[i]]
            i = eltern[i]
        return i

    paare = []
    for i in range(n):
        for j in range(i + 1, n):
            s = cos(vw[i], vw[j])
            if s >= args.schwelle and waisen[i]["note"] != waisen[j]["note"]:
                eltern[wurzel(i)] = wurzel(j)
                paare.append((s, i, j))
    buendel: dict[int, list[int]] = {}
    for i in range(n):
        buendel.setdefault(wurzel(i), []).append(i)

    kandidaten = [b for b in buendel.values() if len({waisen[i]["note"] for i in b}) >= args.min_notes]
    keimend = [b for b in buendel.values() if 2 <= len(b) and b not in kandidaten]

    def zeige(b):
        for i in sorted(b, key=lambda i: waisen[i]["datum"]):
            t = waisen[i]
            print(f"   · {t['frage']}  — [[{t['anker']}]] ({t['datum']})")
        inner = [s for s, i, j in paare if i in b and j in b]
        if inner:
            print(f"     Nähe innen: {min(inner):.2f}–{max(inner):.2f}")

    print(f"## Kandidaten für ein neues Panorama (≥{args.min_notes} Notes, Kosinus ≥ {args.schwelle})")
    if kandidaten:
        for k, b in enumerate(kandidaten, 1):
            print(f"\n{k}.")
            zeige(b)
    else:
        print("   keine — noch zu wenig Stoff.")

    print("\n## Keimend (2 Themen aus verschiedenen Notes, die zueinander finden)")
    if keimend:
        for b in keimend:
            zeige(b)
            print()
    else:
        print("   keine")

    # 2) Waisen, die in ein bestehendes Panorama gehören könnten
    print(f"\n## Waisen nahe einer Panorama-Frage (Kosinus ≥ {args.panorama_schwelle})")
    treffer = False
    for i, t in enumerate(waisen):
        if not vf:
            break
        s, k = max((cos(vw[i], v), k) for k, v in enumerate(vf))
        if s >= args.panorama_schwelle:
            treffer = True
            f = fragen[k]
            print(f"   · {t['frage']}  ({s:.2f})\n     → [[{f['panorama']}#{f['frage'].replace(':', '')}|{f['titel']} — {f['frage']}]]")
    if not treffer:
        print("   keine")

    # 3) Einzelgänger — mit den nächsten Nachbarn (Themen und Panorama-Fragen), fürs Urteil
    alle_v = embed([embed_text(t) for t in themen])
    allein = [b[0] for b in buendel.values() if len(b) == 1]
    print(f"\n## Einzelgänger ({len(allein)}) — nächste Nachbarn fürs Urteil")
    for i in sorted(allein, key=lambda i: waisen[i]["datum"], reverse=True):
        t = waisen[i]
        print(f"   · {t['frage']}  — [[{t['anker']}]] ({t['datum']})")
        nach = sorted(((cos(vw[i], v), u) for u, v in zip(themen, alle_v)
                       if u["note"] != t["note"]), key=lambda x: -x[0])[:2]
        for s, u in nach:
            wo = ", ".join(u["panoramen"]) or "Waise"
            print(f"       {s:.2f}  Thema: {u['frage']} ({wo})")
        if vf:
            s, k = max((cos(vw[i], v), k) for k, v in enumerate(vf))
            print(f"       {s:.2f}  Panorama: {fragen[k]['titel']} — {fragen[k]['frage']}")

    print("\n*Schwellen geeicht am 29.09.2026 (n=14, siehe Docstring). Die Maschine schlägt vor — ob ein Bündel "
          "eine Frage trägt, entscheidet das Urteil, angelegt wird nur mit Andreas' Ja.*")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("extract").set_defaults(fn=cmd_extract)
    p = sub.add_parser("ingest")
    p.add_argument("--no-extract", action="store_true", help="vorhandenes Register nehmen")
    p.set_defaults(fn=cmd_ingest)
    p = sub.add_parser("query")
    p.add_argument("text")
    p.add_argument("--limit", type=int, default=8)
    p.add_argument("--waisen", action="store_true", help="nur Themen ohne Panorama")
    p.set_defaults(fn=cmd_query)
    p = sub.add_parser("analyse")
    p.add_argument("--schwelle", type=float, default=0.70, help="Kosinus für Bündel unter Waisen")
    p.add_argument("--panorama-schwelle", type=float, default=0.70, help="Kosinus Waise ↔ Panorama-Frage")
    p.add_argument("--min-notes", type=int, default=3)
    p.set_defaults(fn=cmd_analyse)
    args = ap.parse_args()
    try:
        args.fn(args)
    except (RuntimeError, OSError) as e:
        sys.exit(f"Fehler: {e}")


if __name__ == "__main__":
    main()
