"""Rechnet die Kernzahlen der Spur aus codes.csv nach (nur Standardbibliothek).

    python3 nachrechnen.py

AfD-Achse je Halbjahr: H, K, L1, L2, Anteil der Hinnahme (L1+L2) und der Kritik (K) an allen
Absätzen mit Haltung (H+K+L1+L2). Dazu H1 wie vorregistriert: Basis 2019-H2 bis 2021-H1 gegen
2025-H2 bis 2026-H2."""
import collections, csv
from pathlib import Path

rows = list(csv.DictReader(open(Path(__file__).with_name("codes.csv"), encoding="utf-8")))
halb = lambda d: f"{d[:4]}-H{1 if int(d[5:7]) <= 6 else 2}"
tab = collections.defaultdict(collections.Counter)
for r in rows:
    if r["afd"] in ("H", "K", "L1", "L2"):
        tab[halb(r["datum"])][r["afd"]] += 1

pct = lambda a, b: f"{a / b:5.1%} ({a}/{b})" if b else "     –"
print(f"{len(rows)} Absätze\n\nHalbjahr    H    K   L1   L2   Hinnahme (L)        Kritik (K)")
for h in sorted(tab):
    c = tab[h]; n = sum(c.values()); l = c["L1"] + c["L2"]
    print(f"{h}  {c['H']:>4} {c['K']:>4} {c['L1']:>4} {c['L2']:>4}   {pct(l, n):<18}  {pct(c['K'], n)}")


def zeitraum(von, bis):
    c = sum((tab[h] for h in tab if von <= h <= bis), collections.Counter())
    return c["L1"] + c["L2"], c["K"], sum(c.values())


for name, (von, bis) in {"Basis": ("2019-H2", "2021-H1"), "jetzt": ("2025-H2", "2026-H2")}.items():
    l, k, n = zeitraum(von, bis)
    print(f"\nH1 {name} {von}–{bis}: Hinnahme {pct(l, n)}, Kritik {pct(k, n)}")
