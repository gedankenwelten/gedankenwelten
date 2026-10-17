#!/usr/bin/env python3
"""Statistik-Grafiken für Gedankenwelten-Notes — eigene Grafik, fremde Zahlen, Quelle unten drin.

Eine kleine JSON-Datei beschreibt die Grafik, das Skript zeichnet sie als SVG in Inter (der Schrift
der Website), rendert sie mit Chrome headless in doppelter Auflösung und legt das zugeschnittene PNG
in content/assets/ ab. Wann eine Grafik passt: gedankenwelt-Skill, Schritt 5e.

    python3 .claude/scripts/statistik_grafik.py spec.json --out Note-Slug-Thema
    python3 .claude/scripts/statistik_grafik.py spec.json --out x --nur-html   # nur HTML ansehen

Drei Formen (Feld "art"):

  balken   {"zeilen": [["Beschriftung", 7.9], ...], "einheit": " %", "max": 25,
            "farben": [1, 2, 2]}            # optional je Zeile; mit "legende": [[1,"…"],[2,"…"]]
  hantel   {"gruppen": [["Überschrift", [["Zeile", vorher, nachher], ...]], ...],
            "max": 12, "referenz": [1, "1 = gleiches Risiko"],
            "legende": ["roh", "bereinigt"]}  # Farbe 2 = vorher, Farbe 1 = nachher
  tabelle  {"spalten": [{"titel": "Land", "art": "text"},
                        {"titel": "Bevölkerung", "art": "zahl"},
                        {"titel": "Tatverdächtige", "art": "balken", "farbe": 2, "max": 7255},
                        {"titel": "je 100.000", "art": "balken", "farbe": 1, "nachkomma": 1}],
            "zeilen": [["Deutschland", 71036222, 7255, 10.2], ...]}

Gemeinsam: "titel", "untertitel", "quelle" (Pflicht — Datenquelle; die Lizenzzeile hängt das Skript
an). Zahlen deutsch formatiert (7.255 · 10,2). Balken beginnen immer bei null.
"""
import argparse
import html
import json
import os
import subprocess
import sys
from pathlib import Path

CORTEX = Path(__file__).resolve().parents[2]
ASSETS = CORTEX / "Gedankenwelten" / "assets"
SCHRIFT = Path.home() / "Development" / "gedankenwelten-neu" / "public" / "schrift"
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
LIZENZ = "Grafik: gedankenwelten.org, CC BY-SA 4.0"

# Farben: geprüft mit dem dataviz-Validator (CVD- und Kontrast-Checks bestanden, heller Grund)
F = {1: "#2a78d6", 2: "#eb6834"}
TXT, TXT2, MUTED, GRID, SURF, BAND = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0", "#fcfcfb", "#f3f2ee"
W = 800            # CSS-Breite der Seite; das PNG wird doppelt so breit
IW = W - 64        # Innenbreite


def zahl(v, nachkomma=None):
    if nachkomma is None:
        nachkomma = 0 if float(v).is_integer() else 1
    s = f"{v:,.{nachkomma}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def esc(s):
    return html.escape(str(s), quote=False)


def t(x, y, s, size=13.5, fill=TXT, anchor="start", weight=400, halo=False, num=False):
    extra = f' stroke="{SURF}" stroke-width="5" paint-order="stroke"' if halo else ""
    style = ' style="font-variant-numeric:tabular-nums"' if num else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}"{extra}{style}>{esc(s)}</text>')


def balken_pfad(x, y, w, h, fill):
    """Balken mit runden Enden nur an der Datenseite, an der Null-Linie gerade."""
    w = max(w, 2)
    r = min(4, w / 2, h / 2)
    return (f'<path d="M{x:.1f} {y:.1f} H{x + w - r:.1f} a{r} {r} 0 0 1 {r} {r} V{y + h - r:.1f} '
            f'a{r} {r} 0 0 1 -{r} {r} H{x:.1f} Z" fill="{fill}"/>')


def legende(eintraege, rund=True):
    radius = "50%" if rund else "3px"
    teile = "".join(f'<span><i style="background:{F[f]};border-radius:{radius}"></i>{esc(txt)}</span>'
                    for f, txt in eintraege)
    return f'<div class="lg">{teile}</div>'


def svg(teile, hoehe, viewbox=None):
    vb = viewbox or f"0 0 {IW} {hoehe}"
    return (f'<svg width="{IW}" height="{hoehe:.0f}" viewBox="{vb}" style="overflow:visible">'
            + "".join(teile) + "</svg>")


# ---------------------------------------------------------------- Formen

def form_balken(s):
    zeilen, einheit = s["zeilen"], s.get("einheit", "")
    mx = s.get("max") or max(v for _, v in zeilen) * 1.12
    farben = s.get("farben") or [1] * len(zeilen)
    breite = IW - 70
    teile, y = [], 0
    for (lab, v), f in zip(zeilen, farben):
        teile.append(t(0, y + 14, lab, fill=TXT2))
        w = breite * v / mx
        teile.append(balken_pfad(0, y + 22, w, 18, F[f]))
        teile.append(t(w + 8, y + 36, zahl(v, s.get("nachkomma")) + einheit, size=14, weight=600))
        y += 58
    leg = legende(s["legende"], rund=False) if s.get("legende") else ""
    return leg, svg(teile, y)


def form_hantel(s):
    mx = s["max"]
    L, R = 230, IW - 40
    x = lambda v: L + (R - L) * v / mx
    zeilen, y = [], 8
    for kopf, reihen in s["gruppen"]:
        y += 10
        zeilen.append(("kopf", kopf, y))
        y += 24
        for lab, a, b in reihen:
            zeilen.append(("reihe", lab, a, b, y))
            y += 32
    H = y + 30
    teile = []
    schritt = s.get("schritt") or (2 if mx <= 12 else 5 if mx <= 30 else 10)
    v = 0
    while v <= mx + 1e-9:
        teile.append(f'<line x1="{x(v):.1f}" y1="0" x2="{x(v):.1f}" y2="{H - 26}" stroke="{GRID}"/>')
        teile.append(t(x(v), H - 8, zahl(v), size=12, fill=MUTED, anchor="middle"))
        v += schritt
    if s.get("referenz"):
        rv, rtxt = s["referenz"]
        teile.append(f'<line x1="{x(rv):.1f}" y1="0" x2="{x(rv):.1f}" y2="{H - 26}" stroke="{TXT2}" '
                     f'stroke-width="1.5" stroke-dasharray="4 3"/>')
        teile.append(t(x(rv) + 6, 12, rtxt, size=11.5, fill=TXT2))
    for z in zeilen:
        if z[0] == "kopf":
            teile.append(t(0, z[2] + 14, z[1], size=13, weight=600))
            continue
        _, lab, a, b, yy = z
        cy = yy + 12
        teile.append(t(14, cy + 4.5, lab, fill=TXT2))
        teile.append(f'<line x1="{x(min(a, b)):.1f}" y1="{cy}" x2="{x(max(a, b)):.1f}" y2="{cy}" '
                     f'stroke="#c9c8c2" stroke-width="2"/>')
        for v, f in ((a, 2), (b, 1)):
            teile.append(f'<circle cx="{x(v):.1f}" cy="{cy}" r="6.5" fill="{F[f]}" stroke="{SURF}" stroke-width="2"/>')
        rechts, links = (a, b) if a >= b else (b, a)
        teile.append(t(x(rechts) + 11, cy + 4.5, zahl(rechts, 1), size=12.5))
        teile.append(t(x(links) - 11, cy + 4.5, zahl(links, 1), size=12.5, anchor="end", halo=True))
    leg = legende([(2, s["legende"][0]), (1, s["legende"][1])]) if s.get("legende") else ""
    return leg, svg(teile, H)


def form_tabelle(s):
    spalten, zeilen = s["spalten"], s["zeilen"]
    # Breiten: Text 150, Zahl 110, Balken 190 (Balken 70 % + Zahl) — dann auf die Innenbreite skalieren
    roh = [{"text": 150, "zahl": 115, "balken": 190}[c["art"]] for c in spalten]
    k = IW / sum(roh)
    breiten = [r * k for r in roh]
    xs = [sum(breiten[:i]) for i in range(len(breiten))]
    for c, i in zip(spalten, range(len(spalten))):
        if c["art"] == "balken" and "max" not in c:
            c["max"] = max(z[i] for z in zeilen)
    RH, top, teile = 31, 34, []
    for c, x0, w in zip(spalten, xs, breiten):
        rechts = c["art"] == "zahl"
        teile.append(t(x0 + (w - 14 if rechts else 0), 14, c["titel"], size=12.5, fill=TXT2, weight=600,
                       anchor="end" if rechts else "start"))
    teile.append(f'<line x1="0" y1="{top - 10}" x2="{IW}" y2="{top - 10}" stroke="{TXT2}"/>')
    for r, z in enumerate(zeilen):
        y = top + r * RH
        cy = y + RH / 2
        if r % 2 == 0:
            teile.append(f'<rect x="-6" y="{y}" width="{IW + 12}" height="{RH}" fill="{BAND}"/>')
        for c, x0, w, v in zip(spalten, xs, breiten, z):
            if c["art"] == "text":
                teile.append(t(x0, cy + 4.5, v))
            elif c["art"] == "zahl":
                teile.append(t(x0 + w - 14, cy + 4.5, zahl(v, c.get("nachkomma")), fill=TXT2, anchor="end", num=True))
            else:
                bw = (w * 0.62) * v / c["max"]
                teile.append(f'<rect x="{x0:.1f}" y="{cy - 6}" width="{max(bw, 2):.1f}" height="12" rx="2" fill="{F[c.get("farbe", 1)]}"/>')
                teile.append(t(x0 + max(bw, 2) + 7, cy + 4.5, zahl(v, c.get("nachkomma")), weight=c.get("gewicht", 400), num=True))
    H = top + len(zeilen) * RH + 6
    return "", svg(teile, H, viewbox=f"-6 0 {IW + 12} {H}")


FORMEN = {"balken": form_balken, "hantel": form_hantel, "tabelle": form_tabelle}


def seite(s, leg, korpus):
    fonts = ",".join(f"url({(SCHRIFT / n).as_uri()}) format('woff2')"
                     for n in ("inter-normal-latin.woff2", "inter-normal-latin-ext.woff2") if (SCHRIFT / n).exists())
    face = f"@font-face{{font-family:Inter;src:{fonts};font-weight:100 900}}" if fonts else ""
    quelle = s["quelle"].rstrip(" .") + " · " + LIZENZ
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{face}
html,body{{margin:0;background:{SURF}}}
.c{{width:{W}px;box-sizing:border-box;padding:28px 32px 22px;font-family:Inter,-apple-system,sans-serif;color:{TXT};background:{SURF}}}
h1{{font-size:21px;font-weight:600;margin:0 0 6px;letter-spacing:-.01em;line-height:1.3}}
p.s{{font-size:14px;color:{TXT2};margin:0 0 14px;line-height:1.45}}
.lg{{display:flex;flex-wrap:wrap;gap:6px 22px;font-size:13px;color:{TXT2};margin:0 0 12px}}
.lg span{{display:inline-flex;align-items:center;gap:7px}}
.lg i{{width:11px;height:11px;display:inline-block}}
.src{{font-size:11.5px;color:{MUTED};margin-top:10px;line-height:1.45}}
svg text{{font-family:Inter,-apple-system,sans-serif}}
</style></head><body><div class="c"><h1>{esc(s["titel"])}</h1>
{f'<p class="s">{esc(s["untertitel"])}</p>' if s.get("untertitel") else ""}{leg}{korpus}
<div class="src">{esc(quelle)}</div></div></body></html>"""


def rendern(html_pfad, png_pfad):
    roh = png_pfad.with_suffix(".roh.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--allow-file-access-from-files", "--force-device-scale-factor=2",
                    "--window-size=800,1600", f"--screenshot={roh}", html_pfad.as_uri()],
                   check=True, capture_output=True)
    subprocess.run(["magick", str(roh), "-bordercolor", SURF, "-fuzz", "1%", "-trim", "+repage",
                    "-bordercolor", SURF, "-border", "56", str(png_pfad)], check=True)
    roh.unlink(missing_ok=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", help="JSON-Datei mit der Beschreibung der Grafik")
    ap.add_argument("--out", required=True, help="Dateiname ohne Endung, z.B. Note-Slug-Anzeigerate")
    ap.add_argument("--ziel", default=str(ASSETS), help="Zielordner (Default: content/assets)")
    ap.add_argument("--nur-html", action="store_true", help="nur die HTML-Seite schreiben")
    a = ap.parse_args()
    s = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    for feld in ("art", "titel", "quelle"):
        if not s.get(feld):
            sys.exit(f"Feld fehlt: {feld} (die Quelle ist Pflicht)")
    if s["art"] not in FORMEN:
        sys.exit(f"Unbekannte Form {s['art']!r} — möglich: {', '.join(FORMEN)}")
    leg, korpus = FORMEN[s["art"]](s)
    ziel = Path(a.ziel)
    ziel.mkdir(parents=True, exist_ok=True)
    html_pfad = Path(a.spec).with_suffix(".html")
    html_pfad.write_text(seite(s, leg, korpus), encoding="utf-8")
    if a.nur_html:
        print(html_pfad)
        return
    png = ziel / f"{a.out}.png"
    rendern(html_pfad.resolve(), png)
    print(png)


if __name__ == "__main__":
    main()
