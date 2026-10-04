#!/usr/bin/env python3
"""Extract structured sources from Gedankenwelten notes into a queryable index.

Walks Zeitgeist/Denker/DenkerVita notes, pulls every source link out of the
relevant regions (the `Quelle:` line, `## Weiterführende Quellen`, `## Faktencheck`,
DenkerVita `## Bücher & Publikationen` / `## Empfehlenswerte Videos & Vorträge`),
classifies each by URL, deduplicates by normalised URL and writes one JSON record
per unique source to `.claude/data/sources.jsonl`.

This index is the single source of truth that gets embedded into the Qdrant
collection `gedankenwelten_sources` (see ingest_sources.py on the Pi) and exposed
through the MCP `find_sources` tool.

Usage:
    extract_sources.py                 # full rescan, rebuilds sources.jsonl
    extract_sources.py --note PATH     # re-extract a single note, merge into index
    extract_sources.py --stats         # print coverage stats, write nothing
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

# --- Paths -------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
VAULT = SCRIPT_DIR.parent.parent  # .../Cortex
GW = VAULT / "content"
NOTE_DIRS = [GW / "Zeitgeist", GW / "Denker", GW / "Spuren", GW / "Geistesblitz",
             GW / "Kultur", GW / "GoodNews", GW / "Panorama"]

# Wachsende Panoramas (seit 26.09.2026) tragen ihre Forschung inline im Sachstand
# jeder Frage — dort zählt jeder `## `-Abschnitt außer diesen Rahmen-Abschnitten.
PANORAMA_SKIP = {"nachbesprechungen, die hierher führen", "verbindungen", "weiterdenken"}
VITA_DIR = GW / "DenkerVita"
OUT_PATH = SCRIPT_DIR.parent / "data" / "sources.jsonl"

# --- Markdown link regex -----------------------------------------------------
# [text](url) — url may contain parens-free path; we stop at the first ')'.
MD_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
# Trailing prose after a link on a bullet line: "- [..](..) — description"
DESC_AFTER = re.compile(r"\)\s*[—–-]\s*(.+?)\s*$")

# --- URL classification ------------------------------------------------------
def classify(url: str) -> str:
    h = urlsplit(url).netloc.lower()
    path = urlsplit(url).path.lower()
    if "genialokal." in h:
        return "book"
    if "youtube." in h or "youtu.be" in h:
        return "video"
    if "steady.page" in h or "steadyhq" in h or path.endswith(".mp3") or "podcast" in h:
        return "podcast"
    if "wikipedia.org" in h:
        return "wikipedia"
    study_hosts = ("doi.org", "jamanetwork", "bmj.com", "plos.org", "journals.plos",
                   "pnas.org", "nature.com", "sciencedirect", "springer", "tandfonline",
                   "arxiv.org", "ncbi.nlm.nih.gov", "pubmed", "researchgate", "ssrn.com",
                   "cambridge.org", "oup.com", "wiley.com", "sagepub")
    if any(s in h for s in study_hosts) or (path.endswith(".pdf") and ".edu" in h):
        return "study"
    official = ("freedomhouse.org", "v-dem.net", "transparency.org", "transparency.de",
                "worldbank.org", "imf.org", "oecd.org", "bpb.de", "destatis.de",
                "europa.eu", "ec.europa.eu", "statista", "indec.gob", "reporter-ohne-grenzen",
                "bundestag.de", "bundesregierung.de", "un.org", "who.int", "eurostat")
    if any(s in h for s in official) or h.endswith(".gov") or ".gov." in h:
        return "official-data"
    return "article"


def normalise_url(url: str) -> str:
    """Canonical form for dedup: drop tracking params + fragment, lowercase host,
    strip trailing slash. Keep YouTube ?v= and other meaningful query params."""
    url = url.rstrip(".,;)\"'")  # strip trailing punctuation that leaked into the match
    s = urlsplit(url)
    host = s.netloc.lower()
    # youtu.be/<id> -> youtube watch
    query = [(k, v) for k, v in parse_qsl(s.query)
             if not k.lower().startswith("utm_") and k.lower() not in ("fbclid", "gclid", "feature")]
    # keep deterministic order
    q = urlencode(sorted(query))
    path = s.path.rstrip("/")
    return urlunsplit((s.scheme.lower(), host, path, q, ""))


def source_id(norm_url: str) -> str:
    return hashlib.sha1(norm_url.encode("utf-8")).hexdigest()


# --- Note parsing ------------------------------------------------------------
def parse_frontmatter(text: str) -> tuple[str, list[str]]:
    """Return (title, tags) from a minimal YAML frontmatter block."""
    title, tags = "", []
    if not text.startswith("---"):
        return title, tags
    end = text.find("\n---", 3)
    if end == -1:
        return title, tags
    fm = text[3:end]
    in_tags = False
    for line in fm.splitlines():
        if line.startswith("title:"):
            title = line.split(":", 1)[1].strip().strip('"').strip("'")
            in_tags = False
        elif line.startswith("tags:"):
            in_tags = True
            rest = line.split(":", 1)[1].strip()
            if rest.startswith("["):  # inline list: tags: [a, b]
                tags = [t.strip().strip('"').strip("'") for t in rest.strip("[]").split(",") if t.strip()]
                in_tags = False
        elif in_tags and re.match(r"\s*-\s+", line):
            tags.append(re.sub(r"\s*-\s+", "", line).strip().strip('"').strip("'"))
        elif in_tags and not line.startswith(" ") and ":" in line:
            in_tags = False
    return title, tags


# Section headings that contain sources, with their default origin label.
SECTION_ORIGINS = {
    "quellen": "weiterfuehrend",  # Spuren-Rubrik: Quellen-Sektion je Sweep
    "weiterführende quellen": "weiterfuehrend",
    "weiterfuehrende quellen": "weiterfuehrend",
    "faktencheck": "faktencheck",
    # Vertiefung nach dem Video (seit 26.09.2026): Forschung und Fälle inline im Satz.
    "nachbesprechung": "nachbesprechung",
    "bücher & publikationen": "denkervita-book",
    "buecher & publikationen": "denkervita-book",
    "bücher und publikationen": "denkervita-book",
    "empfehlenswerte videos & vorträge": "denkervita-video",
    "empfehlenswerte videos & vortraege": "denkervita-video",
    "empfehlenswerte videos und vorträge": "denkervita-video",
}

# Sub-labels inside "Weiterführende Quellen" refine the origin.
SUBLABELS = [
    ("video-beschreibung", "video-description"),
    ("video-description", "video-description"),
    ("im video verlinkt", "in-video"),
    ("im video", "in-video"),
    ("sherlock", "sherlock"),
]


def iter_source_regions(body: str, growing: bool = False):
    """Yield (origin, region_text) for every region of a note that holds sources.

    Always yields the leading `Quelle:` line(s) as origin 'primary', plus any
    matched `## ` section until the next `## ` heading.
    """
    lines = body.splitlines()

    # Primary source: the `Quelle:` line(s) before the first '##'
    for ln in lines:
        if ln.startswith("## "):
            break
        if re.match(r"^\s*Quelle\b", ln):
            yield "primary", ln

    # Section scan
    current_origin = None
    buf: list[str] = []
    for ln in lines:
        m = re.match(r"^##\s+(.+?)\s*$", ln)
        if m:
            if current_origin is not None:
                yield current_origin, "\n".join(buf)
            buf = []
            heading = m.group(1).strip().lower()
            current_origin = SECTION_ORIGINS.get(heading)
            if current_origin is None and growing and heading not in PANORAMA_SKIP:
                current_origin = "panorama-sachstand"
            continue
        if current_origin is not None:
            buf.append(ln)
    if current_origin is not None and buf:
        yield current_origin, "\n".join(buf)


def refine_origin(default_origin: str, region: str, line: str) -> str:
    """For Weiterführende-Quellen regions, pick origin from the nearest sub-label."""
    if default_origin != "weiterfuehrend":
        return default_origin
    # find the last sublabel marker at or before this line
    chosen = "weiterfuehrend"
    for rline in region.splitlines():
        low = rline.lower()
        for needle, origin in SUBLABELS:
            if needle in low and rline.strip().startswith("*"):
                chosen = origin
        if rline == line:
            break
    return chosen


def extract_from_note(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    title, tags = parse_frontmatter(text)
    # body after frontmatter
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            body = text[end + 4:]
    rel = str(path.relative_to(VAULT))
    note_title = title or path.stem

    found: list[dict] = []
    growing = "panorama-art: wachsend" in text[:1500]
    for default_origin, region in iter_source_regions(body, growing):
        for line in region.splitlines():
            for m in MD_LINK.finditer(line):
                link_text = m.group(1).strip()
                raw_url = m.group(2).strip()
                norm = normalise_url(raw_url)
                if not norm.startswith("http"):
                    continue
                # timestamp links (▶ 31:13) are in-video navigation, not sources
                if is_timestamp(link_text):
                    continue
                title = clean_title(link_text)
                # derive a readable title from the URL when the link text is junk
                if is_junk_title(title):
                    title = title_from_url(norm)
                desc = ""
                dm = DESC_AFTER.search(line[m.end() - 1:])
                if dm:
                    desc = dm.group(1).strip().strip("*")
                origin = refine_origin(default_origin, region, line)
                found.append({
                    "url": norm,
                    "raw_url": raw_url,
                    "title": title,
                    "description": desc,
                    "type": classify(norm),
                    "origin": origin,
                    "note": rel,
                    "note_title": note_title,
                    "tags": tags,
                })
    return found


def clean_title(t: str) -> str:
    # collapse whitespace, strip markdown emphasis
    t = re.sub(r"\s+", " ", t).strip().strip("*").strip()
    return t


# Uninformative link texts that carry no semantic signal on their own.
JUNK_TITLES = {
    "wikipedia", "hier", "link", "mehr", "klick", "klicken", "hier klicken",
    "youtube", "youtube-kanal", "free youtube-kanal", "quelle", "artikel",
    "studie", "video", "website", "webseite", "zum artikel", "mehr dazu",
    "weiterlesen", "siehe hier", "this study", "study", "source", "report",
    "genialokal", "genial lokal", "buch", "zum buch", "amazon",
}
TIMESTAMP_RE = re.compile(r"^[▶▸►\s]*\d{1,2}:\d{2}(:\d{2})?\s*$")


def is_timestamp(t: str) -> bool:
    return bool(TIMESTAMP_RE.match(t.strip()))


def is_junk_title(t: str) -> bool:
    tl = t.strip().lower()
    return tl in JUNK_TITLES or len(tl) <= 1


def title_from_url(url: str) -> str:
    """Derive a readable title from the URL when the link text is uninformative."""
    from urllib.parse import unquote, parse_qs
    s = urlsplit(url)
    host = s.netloc.replace("www.", "")
    if "wikipedia.org" in host and "/wiki/" in url:
        art = unquote(url.split("/wiki/")[-1]).replace("_", " ").split("#")[0]
        return f"Wikipedia — {art}" if art else "Wikipedia"
    if "genialokal" in host:
        q = (parse_qs(s.query).get("q") or [""])[0].replace("+", " ").strip()
        return f"Buch: {q}" if q else "Buchsuche (genialokal)"
    path = unquote(s.path).strip("/")
    if path:
        last = path.split("/")[-1]
        last = re.sub(r"\.(html?|php|aspx?|pdf|jsp)$", "", last)
        last = last.replace("-", " ").replace("_", " ").strip()
        if last and not last.isdigit() and len(last) > 2:
            return f"{host}: {last[:80]}"
    return host


# --- Index assembly ----------------------------------------------------------
def merge_records(records: list[dict]) -> dict[str, dict]:
    """Merge per-link records into one entry per unique URL."""
    index: dict[str, dict] = {}
    for r in records:
        sid = source_id(r["url"])
        if sid not in index:
            index[sid] = {
                "id": sid,
                "title": r["title"],
                "url": r["url"],
                "type": r["type"],
                "description": r["description"],
                "origin": r["origin"],
                "notes": [r["note"]],
                "note_titles": [r["note_title"]],
                "tags": list(dict.fromkeys(r["tags"])),
            }
        else:
            e = index[sid]
            if r["note"] not in e["notes"]:
                e["notes"].append(r["note"])
                e["note_titles"].append(r["note_title"])
            for tg in r["tags"]:
                if tg not in e["tags"]:
                    e["tags"].append(tg)
            # prefer a longer/non-empty description and title
            if len(r["description"]) > len(e["description"]):
                e["description"] = r["description"]
            if len(r["title"]) > len(e["title"]) and len(r["title"]) < 200:
                e["title"] = r["title"]
    return index


def collect_all_notes() -> list[Path]:
    paths: list[Path] = []
    for d in NOTE_DIRS:
        if d.exists():
            paths += sorted(d.glob("*.md"))
    if VITA_DIR.exists():
        paths += [p for p in sorted(VITA_DIR.glob("*.md")) if "Alle Denker" not in p.name]
    return paths


def write_index(index: dict[str, dict]) -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        for entry in sorted(index.values(), key=lambda e: (e["type"], e["title"].lower())):
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load_index() -> dict[str, dict]:
    index: dict[str, dict] = {}
    if OUT_PATH.exists():
        for line in OUT_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                e = json.loads(line)
                index[e["id"]] = e
    return index


# --- CLI ---------------------------------------------------------------------
def full_scan(stats_only: bool = False) -> None:
    notes = collect_all_notes()
    all_records: list[dict] = []
    notes_with_sources = 0
    for p in notes:
        recs = extract_from_note(p)
        if recs:
            notes_with_sources += 1
        all_records += recs
    index = merge_records(all_records)
    by_type: dict[str, int] = {}
    for e in index.values():
        by_type[e["type"]] = by_type.get(e["type"], 0) + 1

    print(f"Notes gescannt:        {len(notes)}")
    print(f"Notes mit Quellen:     {notes_with_sources}")
    print(f"Quell-Links gesamt:    {len(all_records)}")
    print(f"Eindeutige Quellen:    {len(index)}")
    print("Nach Typ:")
    for t, c in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {t:14s} {c}")
    if stats_only:
        return
    write_index(index)
    print(f"\nGeschrieben: {OUT_PATH.relative_to(VAULT)} ({len(index)} Einträge)")


def single_note(note_path: str) -> None:
    p = Path(note_path)
    if not p.is_absolute():
        p = VAULT / note_path
    if not p.exists():
        print(f"Note nicht gefunden: {p}", file=sys.stderr)
        sys.exit(1)
    rel = str(p.relative_to(VAULT))
    index = load_index()
    # drop this note's associations so removed links disappear
    for e in list(index.values()):
        if rel in e["notes"]:
            i = e["notes"].index(rel)
            e["notes"].pop(i)
            if i < len(e["note_titles"]):
                e["note_titles"].pop(i)
            if not e["notes"]:
                del index[e["id"]]
    # re-add current links
    new_index = merge_records(extract_from_note(p))
    for sid, entry in new_index.items():
        if sid in index:
            ex = index[sid]
            for n, nt in zip(entry["notes"], entry["note_titles"]):
                if n not in ex["notes"]:
                    ex["notes"].append(n)
                    ex["note_titles"].append(nt)
            for tg in entry["tags"]:
                if tg not in ex["tags"]:
                    ex["tags"].append(tg)
        else:
            index[sid] = entry
    write_index(index)
    print(f"Note '{rel}' verarbeitet → {len(new_index)} Quellen. Index: {len(index)} Einträge.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--note", help="Re-extract a single note and merge into the index")
    ap.add_argument("--stats", action="store_true", help="Print stats only, write nothing")
    args = ap.parse_args()
    if args.note:
        single_note(args.note)
    else:
        full_scan(stats_only=args.stats)


if __name__ == "__main__":
    main()
