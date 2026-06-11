#!/usr/bin/env python3
"""indexnow_ping.py — Meldet neue/geänderte Seiten an IndexNow (Bing, Yandex, Seznam, Naver).

Läuft auf dem Pi am Ende von pull-and-build.sh, direkt nach dem Atomic Swap:
Die Sitemap in public/ ist dann frisch und alle URLs sind live.

Mechanik: Sitemap (URL + lastmod) gegen State-File diffen → nur Neues/Geändertes
submitten. Beim allerersten Lauf (kein State) wird die komplette Sitemap gemeldet.
State liegt untracked im Repo-Verzeichnis und überlebt git reset --hard.
"""

import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

HOST = "gedankenwelten.org"
KEY = "910d8353cc9930fd91225252432ed779"
REPO = Path(__file__).resolve().parent.parent
SITEMAP = REPO / "public" / "sitemap.xml"
STATE = REPO / ".indexnow-state.json"
ENDPOINT = "https://api.indexnow.org/indexnow"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def read_sitemap() -> dict[str, str]:
    tree = ET.parse(SITEMAP)
    pages = {}
    for url in tree.getroot().findall("sm:url", NS):
        loc = url.findtext("sm:loc", default="", namespaces=NS).strip()
        lastmod = url.findtext("sm:lastmod", default="", namespaces=NS).strip()
        if loc:
            pages[loc] = lastmod
    return pages


def main() -> int:
    if not SITEMAP.exists():
        print(f"indexnow: {SITEMAP} fehlt — übersprungen")
        return 0

    pages = read_sitemap()
    old = json.loads(STATE.read_text()) if STATE.exists() else {}
    changed = [url for url, mod in pages.items() if old.get(url) != mod]

    if not changed:
        print("indexnow: keine neuen/geänderten URLs")
        return 0

    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": f"https://{HOST}/{KEY}.txt",
        "urlList": changed[:10000],
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
    except urllib.error.HTTPError as e:
        print(f"indexnow: HTTP {e.code} — {e.read().decode(errors='replace')[:200]}")
        return 1
    except Exception as e:
        print(f"indexnow: Fehler — {e}")
        return 1

    # 200 = ok, 202 = angenommen (Key wird noch verifiziert)
    print(f"indexnow: {len(changed)} URLs gemeldet (HTTP {status})")
    STATE.write_text(json.dumps(pages, ensure_ascii=False, indent=0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
