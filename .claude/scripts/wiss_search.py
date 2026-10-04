#!/usr/bin/env python3
"""
wiss_search — die gemeinsame wissenschaftliche Retrieval-Schicht für Cortex.

Die stumpfe Sammel-Schicht (Routing-Prinzip): verschmilzt drei freie wissenschaftliche APIs zu *einem*
normalisierten Ergebnis. Das *Urteil* — ist ein Paper relevant, solide, Konsens oder Ausreißer, koppelt es
an welche Note — macht Claude (Sherlock beim Faktencheck, /galilei bei der Note-Kopplung), nie dieses Skript.

Quellen (alle frei, kein Pflicht-Key):
  · OpenAlex          — Index + Zitationsgraph (~250 Mio. Werke, CC0, polite pool via mailto)
  · Semantic Scholar  — TLDR-Zusammenfassung + Publikationstyp (Review/Meta-Analyse-Erkennung)
  · Europe PMC        — Biomed-Abdeckung, wo OpenAlex/S2 dünn sind (nur mit --field biomed)

Das `soliditaet`-Feld ist der Gleichmut-Spiegel der Wissenschaft: es unterscheidet Meta-Analyse von
Einzelstudie von Preprint. Eine Studie ist ein Datenpunkt, kein Wahrheits-Stempel.

Nur Python-Standardbibliothek (urllib + json) — kein pip, läuft auf Mac UND Pi.

Aufruf:
  python3 wiss_search.py "claim oder thema" [--top 5] [--field biomed] [--json] [--year-from 2015]

Ausgabe: menschenlesbar (default) oder --json (Array, DOI-dedupliziert, für die Skills).

--sieb: ordnet jedes Abstract zusätzlich mit Jev ein (→ systemone.py): Studientyp, Untersuchungsgegenstand,
berichtet Zahlen? Reines *Einordnen* als zweite Stimme neben dem regelbasierten `soliditaet` — nie das
Urteil über Relevanz oder Tragfähigkeit (das bleibt bei Claude/Andreas). Kostet ~0,00005 $ je Paper.
"""
import sys
import os
import json
import time
import argparse
import urllib.request
import urllib.parse
import urllib.error

def _env(name, default=""):
    """Liest eine Variable aus der Umgebung — und, falls dort nicht gesetzt, direkt
    aus der Cortex-`.env`. Quote-aware (entfernt umschließende " oder '), damit es
    egal ist, ob die .env-Werte gequotet sind (Mac) oder nicht (Pi) und ob jemand
    vorher `source .env` gemacht hat. So findet auch ein Cron-Lauf den Key."""
    if os.environ.get(name):
        return os.environ[name]
    for env_path in (os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env"), os.path.expanduser("~/.env")):
        try:
            with open(env_path, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line.startswith(name + "="):
                        v = line.split("=", 1)[1].strip()
                        if len(v) >= 2 and v[0] in "\"'" and v[-1] == v[0]:
                            v = v[1:-1]
                        return v
        except OSError:
            continue
    return default


# Polite pool: OpenAlex bittet um eine Kontakt-Mail im Request — bringt uns in den schnellen Pool.
MAILTO = _env("CORTEX_OPENALEX_MAILTO", "deine@adresse.example")
# Optionaler S2-Key hebt das Rate-Limit (1 req/s); ohne Key teilt man sich einen stark
# gedrosselten Pool (429 → graceful skip). NIE parallel feuern — das Limit ist kumulativ.
S2_KEY = _env("SEMANTIC_SCHOLAR_API_KEY")
UA = "Mozilla/5.0 (compatible; CortexWissSearch/1.0; +https://gedankenwelten.org)"

TIMEOUT = 20


def _get(url, headers=None, versuche=3):
    """Holt JSON — mit Wiederholung bei 429/5xx.

    Ohne das fiel eine gedrosselte Quelle *still* aus: Der Aufrufer (Sherlock, /galilei) sah
    dann einfach weniger Treffer und hielt das fuer den Forschungsstand. Beobachtet am
    05.08.2026 — Semantic Scholar antwortete auf denselben gueltigen Key erst 429, beim
    zweiten Versuch drei Sekunden spaeter 200. Ein einzelner Fehlversuch ist hier also kein
    Befund, sondern Rauschen; genau das darf eine Evidenz-Schicht nicht verwechseln.
    """
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    for i in range(versuche):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            # 429 = gedrosselt, 5xx = Delle beim Anbieter. Beides geht oft beim naechsten Mal.
            if e.code in (429, 500, 502, 503, 504) and i < versuche - 1:
                time.sleep(2 ** i * 1.5)   # 1,5 s · 3 s · 6 s
                continue
            raise


def _norm_doi(doi):
    if not doi:
        return None
    doi = doi.lower().strip()
    for p in ("https://doi.org/", "http://doi.org/", "doi.org/"):
        if doi.startswith(p):
            doi = doi[len(p):]
    return doi or None


def _classify(typ, pub_types, venue):
    """Soliditäts-Typ aus den Roh-Signalen der APIs — der Gleichmut-Spiegel."""
    blob = " ".join(filter(None, [typ or "", " ".join(pub_types or []), venue or ""])).lower()
    if "meta-analysis" in blob or "meta analysis" in blob or "metaanalysis" in blob:
        return "meta-analyse"
    if "review" in blob or "systematic" in blob:
        return "review"
    if "preprint" in blob or "arxiv" in venue.lower() if venue else False:
        return "preprint"
    if any(s in (venue or "").lower() for s in ("arxiv", "biorxiv", "medrxiv", "ssrn", "preprint")):
        return "preprint"
    return "primär"


def _reconstruct_abstract(inv):
    """OpenAlex liefert Abstracts invertiert (Wort -> Positionen) — hier zurück in Text."""
    if not inv:
        return None
    positions = {}
    for word, idxs in inv.items():
        for i in idxs:
            positions[i] = word
    if not positions:
        return None
    return " ".join(positions[i] for i in sorted(positions))


def search_openalex(query, top, year_from):
    qs = {"search": query, "per_page": str(top), "mailto": MAILTO}
    if year_from:
        qs["filter"] = f"from_publication_date:{year_from}-01-01"
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(qs)
    try:
        data = _get(url)
    except Exception as e:
        sys.stderr.write(f"[openalex] {e}\n")
        return []
    out = []
    for w in data.get("results", []):
        loc = w.get("primary_location") or {}
        src = loc.get("source") or {}
        venue = src.get("display_name") or ""
        authors = [a.get("author", {}).get("display_name") for a in w.get("authorships", [])][:6]
        out.append({
            "title": w.get("display_name"),
            "authors": [a for a in authors if a],
            "year": w.get("publication_year"),
            "venue": venue,
            "doi": _norm_doi(w.get("doi")),
            "abstract": _reconstruct_abstract(w.get("abstract_inverted_index")),
            "tldr": None,
            "citation_count": w.get("cited_by_count", 0),
            "is_oa": (w.get("open_access") or {}).get("is_oa", False),
            "oa_url": (w.get("open_access") or {}).get("oa_url"),
            "soliditaet": _classify(w.get("type"), None, venue),
            "source": "openalex",
        })
    return out


def search_s2(query, top, year_from):
    fields = "title,abstract,year,authors,venue,citationCount,externalIds,tldr,publicationTypes,openAccessPdf"
    qs = {"query": query, "limit": str(top), "fields": fields}
    if year_from:
        qs["year"] = f"{year_from}-"
    url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode(qs)
    headers = {"x-api-key": S2_KEY} if S2_KEY else None
    try:
        data = _get(url, headers=headers)
    except Exception as e:
        sys.stderr.write(f"[s2] {e} (Rate-Limit? on-demand ok)\n")
        return []
    out = []
    for p in data.get("data", []) or []:
        ext = p.get("externalIds") or {}
        venue = p.get("venue") or ""
        oa = p.get("openAccessPdf") or {}
        tldr = (p.get("tldr") or {}).get("text")
        out.append({
            "title": p.get("title"),
            "authors": [a.get("name") for a in (p.get("authors") or [])][:6],
            "year": p.get("year"),
            "venue": venue,
            "doi": _norm_doi(ext.get("DOI")),
            "abstract": p.get("abstract"),
            "tldr": tldr,
            "citation_count": p.get("citationCount", 0),
            "is_oa": bool(oa.get("url")),
            "oa_url": oa.get("url"),
            "soliditaet": _classify(None, p.get("publicationTypes"), venue),
            "source": "semantic-scholar",
        })
    return out


def search_europepmc(query, top, year_from):
    q = query + (f" AND PUB_YEAR:[{year_from} TO 3000]" if year_from else "")
    qs = {"query": q, "format": "json", "pageSize": str(top), "resultType": "core"}
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(qs)
    try:
        data = _get(url)
    except Exception as e:
        sys.stderr.write(f"[europepmc] {e}\n")
        return []
    out = []
    for r in (data.get("resultList") or {}).get("result", []):
        venue = r.get("journalTitle") or ""
        out.append({
            "title": r.get("title"),
            "authors": [a.strip() for a in (r.get("authorString") or "").split(",") if a.strip()][:6],
            "year": int(r["pubYear"]) if r.get("pubYear", "").isdigit() else None,
            "venue": venue,
            "doi": _norm_doi(r.get("doi")),
            "abstract": r.get("abstractText"),
            "tldr": None,
            "citation_count": r.get("citedByCount", 0),
            "is_oa": r.get("isOpenAccess") == "Y",
            "oa_url": None,
            "soliditaet": _classify(r.get("pubType"), None, venue),
            "source": "europepmc",
        })
    return out


def merge(lists):
    """DOI-dedupliziert; reichert S2-TLDR in OpenAlex-Treffer mit gleichem DOI an."""
    by_doi = {}
    no_doi = []
    order = []
    for paper in [p for lst in lists for p in lst]:
        doi = paper.get("doi")
        if not doi:
            no_doi.append(paper)
            continue
        if doi in by_doi:
            ex = by_doi[doi]
            # TLDR und Abstract auffüllen, höhere Zitationszahl behalten
            ex["tldr"] = ex.get("tldr") or paper.get("tldr")
            ex["abstract"] = ex.get("abstract") or paper.get("abstract")
            ex["citation_count"] = max(ex.get("citation_count") or 0, paper.get("citation_count") or 0)
            if paper.get("soliditaet") in ("meta-analyse", "review") and ex.get("soliditaet") == "primär":
                ex["soliditaet"] = paper["soliditaet"]
        else:
            by_doi[doi] = paper
            order.append(doi)
    return [by_doi[d] for d in order] + no_doi


SIEB_FRAGEN = {
    "studientyp": {"type": "choice", "instructions": "What kind of study is this?", "criteria": {
        "meta-analyse": "Meta-analysis pooling results of several studies",
        "syst-review": "Systematic review without pooled statistics",
        "review": "Narrative or non-systematic review, overview",
        "experiment": "Randomized controlled trial or experiment with intervention",
        "beobachtung": "Observational study: cohort, cross-sectional, case-control, survey",
        "qualitativ": "Qualitative study: interviews, case study, ethnography",
        "theorie": "Theory, model, essay, commentary, no own data"}},
    "untersucht": {"type": "choice", "instructions": "Who or what is studied?", "criteria": {
        "menschen": "Humans", "tiere": "Animals", "zellen": "Cells, tissue, in vitro",
        "simulation": "Computer model or simulation", "nicht-empirisch": "Nothing empirical"}},
    "zahlen": {"type": "noul", "instructions": "Does the abstract report a concrete quantitative result, such as an effect size, percentage or sample size?"},
}


def sieb(papers):
    """Jev ordnet jedes Paper mit Abstract/TLDR ein. Fehler → still ohne `s1`."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        import systemone
    except ImportError:
        return papers
    kandidaten = [p for p in papers if p.get("abstract") or p.get("tldr")]
    texte = [f"{p.get('title') or ''}\n\n{p.get('abstract') or p.get('tldr')}" for p in kandidaten]
    for p, e in zip(kandidaten, systemone.viele(texte, SIEB_FRAGEN)):
        if "answers" not in e:
            continue
        a = e["answers"]
        p["s1"] = {k: {"wahl": a[k]["choice"], "p": round(max(a[k]["probabilities"].values()), 2)}
                   for k in ("studientyp", "untersucht")}
        p["s1"]["zahlen"] = round(systemone.wahrscheinlichkeit(a["zahlen"]), 2)
    return papers


SOLID_RANK = {"meta-analyse": 3, "review": 2, "primär": 1, "preprint": 0}


def main():
    ap = argparse.ArgumentParser(description="Wissenschaftliche Retrieval-Schicht (OpenAlex/S2/Europe PMC)")
    ap.add_argument("query", help="Claim oder Thema")
    ap.add_argument("--top", type=int, default=5, help="Treffer pro Quelle (default 5)")
    ap.add_argument("--field", choices=["biomed"], help="biomed → Europe PMC zuschalten")
    ap.add_argument("--year-from", type=int, help="nur ab Jahr")
    ap.add_argument("--json", action="store_true", help="JSON-Array statt lesbar")
    ap.add_argument("--sieb", action="store_true", help="Abstracts zusätzlich mit Jev einordnen (Studientyp, Gegenstand, Zahlen)")
    args = ap.parse_args()

    lists = [
        search_openalex(args.query, args.top, args.year_from),
        search_s2(args.query, args.top, args.year_from),
    ]
    if args.field == "biomed":
        lists.append(search_europepmc(args.query, args.top, args.year_from))

    papers = merge(lists)
    if args.sieb:
        papers = sieb(papers)
    # leichte Sortierung: Solidität, dann Zitationen — aber nur als Vorschlag; das Urteil bleibt bei Claude
    papers.sort(key=lambda p: (SOLID_RANK.get(p.get("soliditaet"), 1), p.get("citation_count") or 0), reverse=True)

    if args.json:
        print(json.dumps(papers, ensure_ascii=False, indent=2))
        return

    if not papers:
        print("Keine Treffer (oder alle Quellen gedrosselt — siehe stderr).")
        return
    for i, p in enumerate(papers, 1):
        flag = "🟢 OA" if p.get("is_oa") else "🔒"
        sol = p.get("soliditaet", "?")
        cit = p.get("citation_count") or 0
        auth = ", ".join(p.get("authors") or []) or "—"
        print(f"\n[{i}] {p.get('title')}")
        print(f"    {auth} · {p.get('year') or '?'} · {p.get('venue') or '—'}")
        print(f"    {sol} · {cit} Zitationen · {flag} · {p.get('source')}")
        if p.get("s1"):
            j = p["s1"]
            print(f"    Jev: {j['studientyp']['wahl']} {j['studientyp']['p']:.2f} · {j['untersucht']['wahl']} "
                  f"{j['untersucht']['p']:.2f} · Zahlen {j['zahlen']:.2f}")
        if p.get("doi"):
            print(f"    doi:{p['doi']}  https://doi.org/{p['doi']}")
        if p.get("oa_url"):
            print(f"    Volltext: {p['oa_url']}")
        tl = p.get("tldr") or p.get("abstract")
        if tl:
            print(f"    » {tl[:280]}{'…' if len(tl) > 280 else ''}")


if __name__ == "__main__":
    main()
