#!/usr/bin/env python3
"""sprecher_check.py — vor dem Schreiben: Reicht die Abschrift, und wer spricht wann?

Seit 31.10.2026. Anlass: Drei viel gelesene Notes (Mühlhoff, Flassbeck, Redecker) legten Sprechern
Sätze in den Mund, die andere gesagt hatten. Die Ursachen im Fehler-Register heißen
`interviewer-verwechselt` und `txt-statt-vtt`:
  - Bei Mühlhoff (Jung & Naiv 818) brach die Abschrift nach 31 von 240 Minuten ab; die Note entstand
    aus Bruchstücken ohne Zeitmarken, und Hans Jessen wurde sechsmal zu Tilo Jung.
  - Bei Flassbeck sprach in zwei Fünfteln des Reaktionsvideos der Kommentator Maurice Höfgen.
Andreas, 31.10.: „mach das bitte mit den sprechern trennen.“ Darum zwei billige Prüfungen vor Schritt 5:

  sprecher_check.py abdeckung <URL|ID> <datei.vtt|.txt>
      Videolänge (yt-dlp) gegen die letzte echte Zeitmarke der Abschrift; erkennt Whisper-Schleifen
      („Bis dahin“ x 40) und leere Strecken. Exit 1, wenn weniger als 95 % abgedeckt sind.

  sprecher_check.py schnitte <URL|ID> [--transkript datei.vtt] [--db -80] [--min 0.04]
      Für Reaktionsvideos und zusammengeschnittene Formate: lädt nur den Ton, sucht harte digitale
      Stille (Schnittkanten; ein Saal-Mitschnitt hat nie −80 dB) und misst die Lautheit je Abschnitt.
      Ausgabe: Abschnitte mit Zeit, Lautheit und Textanfang — die Hauptinstanz hört an den Kanten
      kurz hinein und setzt die Sprecher ([NAME] je Abschnitt) in eine Arbeitskopie der Abschrift.
      Ein Werkzeug fürs Urteil, kein Urteil: Inhaltliche Hinweise („wie eben von mir erwähnt“,
      „gemeint ist …“) und das Bild (stillstehendes Vortragsvideo) entscheiden mit.

  sprecher_check.py reaktion <URL|ID>
      Liest Titel, Kanal und Beschreibung und sagt, ob es nach Reaktionsvideo aussieht, samt
      Links in der Beschreibung, die das Original sein könnten. Regel: wenn das Original existiert,
      ist es die Quelle; das Reaktionsvideo höchstens Zweitquelle für den Kommentar.

  sprecher_check.py stimmlage <URL|ID|audio> [--transkript datei.vtt] [--von 7:30 --bis 10:40]
                     [--ref Brown=3:10-3:20 --ref Johnson=4:40-4:50] [--schritt 1]
      Seit 20.11.2026. Wer spricht, wenn das Bild auf den Zuhörer schneidet? Misst je Sekunde den
      Grundton der Stimme (Autokorrelation, 70–400 Hz) und ordnet ihn den Referenzstimmen zu, die man
      an eindeutigen Stellen angibt (Standbild, Vorstellung); ohne --ref teilt es in „tief“/„hoch“.
      Ausgabe: zusammenhängende Strecken mit Sprecher, Hz und Textanfang. Anlass: Wendy Brown (INET) —
      Standbilder allein waren an drei Stellen mehrdeutig, der Grundton trennte Brown (~170 Hz) und
      Rob Johnson (~110 Hz) eindeutig; drei Sätze Johnsons standen als Browns in der Note.
      Grenzen: Zwei Stimmen ähnlicher Lage (zwei Männer, zwei Frauen) trennt es schlecht, Musik und
      Lachen stören, an Sprecherwechseln liegt es eine Sekunde daneben. Ohne --ref ist die Zweiteilung grob
      (tiefere Stellen der hohen Stimme kippen nach „tief“), darum immer Referenzen setzen. Werkzeug fürs
      Urteil, kein Urteil.
"""
import argparse, json, os, re, subprocess, sys, tempfile

YTDLP = "/opt/homebrew/bin/yt-dlp"


def vid(x):
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", x)
    return m.group(1) if m else x


def meta(v):
    out = subprocess.run([YTDLP, "-J", "--skip-download", f"https://www.youtube.com/watch?v={v}"],
                         capture_output=True, text=True, timeout=120)
    if out.returncode:
        sys.exit(f"yt-dlp: {out.stderr.strip()[:200]}")
    return json.loads(out.stdout)


def hms(s):
    s = int(s)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def sec(t):
    parts = [float(p) for p in t.replace(",", ".").split(":")]
    return sum(v * 60 ** i for i, v in enumerate(reversed(parts)))


def cues(path):
    """(start, text) aus VTT oder aus einer TXT mit ▶-Zeitmarken."""
    raw = open(path, encoding="utf-8", errors="replace").read()
    res = []
    if "-->" in raw:
        t, seen = None, set()
        for line in raw.splitlines():
            m = re.match(r"\s*([\d:.,]+)\s*-->", line)
            if m:
                t = sec(m.group(1)); continue
            line = re.sub(r"<[^>]+>", "", line).strip()
            if t is not None and line and line != "WEBVTT" and not line.isdigit():
                # YouTube-Autountertitel rollen: dieselbe Zeile steht in zwei, drei Cues hintereinander
                if res and (line == res[-1][1] or (line, int(t // 10)) in seen):
                    continue
                seen.add((line, int(t // 10)))
                res.append((t, line))
    else:
        for m in re.finditer(r"\[▶ ([\d:]+)\][^\n]*\n?([^\[]*)", raw):
            for line in m.group(2).splitlines():
                if line.strip():
                    res.append((sec(m.group(1)), line.strip()))
    return res


def abdeckung(a):
    v = vid(a.video)
    dur = meta(v).get("duration") or 0
    cs = cues(a.datei)
    if not cs:
        sys.exit("Keine Zeitmarken in der Abschrift gefunden.")
    # In 5-Minuten-Fenstern zählen: Gesprochenes hat viele Wörter und kaum Wiederholung. Whisper füllt
    # zerfallene Strecken mit „Ja.“ x 600 oder „Bis dahin“ — das sind Zeitmarken ohne Inhalt (Mühlhoff 818).
    W = 300
    schlecht = []
    for w0 in range(0, int(max(dur, cs[-1][0])), W):
        win = [t for t0, t in cs if w0 <= t0 < w0 + W]
        words = sum(len(t.split()) for t in win)
        if words < 150 or len(set(win)) < 10:
            schlecht.append(w0)
    fenster = max(1, int(dur // W) + (1 if dur % W else 0))
    # Anfang (Intro-Musik) und Ende (Abspann, Verabschiedung) dürfen dünn sein: vorn 5, hinten 10 Minuten Toleranz
    innen = [w for w in schlecht if W <= w < dur - 2 * W]
    pct = 100 * (fenster - len([w for w in schlecht if w < dur])) / fenster
    print(f"Video {hms(dur)} · letzte Zeitmarke {hms(cs[-1][0])} · Fenster mit echtem Text {pct:.0f} %")
    # zusammenhängende schlechte Strecken melden
    strecken, s0 = [], None
    for w in sorted(innen):
        if s0 is None:
            s0, s1 = w, w + W
        elif w == s1:
            s1 = w + W
        else:
            strecken.append((s0, s1)); s0, s1 = w, w + W
    if s0 is not None:
        strecken.append((s0, s1))
    for a0, a1 in strecken[:10]:
        print(f"⚠ kein verwertbarer Text {hms(a0)} → {hms(min(a1, dur))} (leer, Schleife oder Halluzination)")
    if cs[-1][0] < 0.95 * dur:
        print(f"⚠ Abschrift endet bei {hms(cs[-1][0])}, das Video bei {hms(dur)}")
    if strecken or cs[-1][0] < 0.95 * dur:
        print("→ Abschrift unvollständig. YouTube-Untertitel neu ziehen (yt-dlp --write-auto-sub) oder Whisper"
              " mit --condition-on-previous-text False; nie aus Bruchstücken ohne Zeitmarken schreiben.")
        sys.exit(1)
    print("✓ Abschrift reicht bis zum Ende.")


def schnitte(a):
    v = vid(a.video)
    with tempfile.TemporaryDirectory() as d:
        audio = os.path.join(d, "a.m4a")
        r = subprocess.run([YTDLP, "-f", "ba[ext=m4a]/ba", "-o", audio, f"https://www.youtube.com/watch?v={v}"],
                           capture_output=True, text=True, timeout=900)
        if r.returncode or not os.path.exists(audio):
            sys.exit(f"Ton nicht geladen: {r.stderr.strip()[:200]}")
        sd = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", audio, "-af",
                             f"silencedetect=noise={a.db}dB:d={a.min}", "-f", "null", "-"],
                            capture_output=True, text=True).stderr
        starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", sd)]
        ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", sd)]
        kanten = sorted({round((s + e) / 2, 1) for s, e in zip(starts, ends)})
        dur = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", sd).groups()[0]) * 3600 + \
            float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", sd).groups()[1]) * 60 + \
            float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", sd).groups()[2])
        grenzen = [0.0] + kanten + [dur]
        tx = cues(a.transkript) if a.transkript else []
        print(f"{len(kanten)} harte Schnittkanten (≤ {a.db} dB, ≥ {a.min}s) in {hms(dur)}\n")
        print(f"{'von':>8} {'bis':>8} {'Dauer':>6} {'LUFS':>6}  Textanfang")
        for s0, s1 in zip(grenzen, grenzen[1:]):
            if s1 - s0 < 2:
                continue
            ld = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-ss", str(s0), "-t", str(s1 - s0), "-i", audio,
                                 "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
            m = re.findall(r"I:\s+(-?[\d.]+) LUFS", ld)
            lufs = m[-1] if m else "?"
            text = " ".join(t for t0, t in tx if s0 <= t0 < s1)[:70]
            print(f"{hms(s0):>8} {hms(s1):>8} {int(s1 - s0):>5}s {lufs:>6}  {text}")
        print("\nLautheitssprünge von mehreren LU an einer Kante deuten auf einen Wechsel Studio ↔ Saal."
              " An jeder Kante kurz hineinhören, dann die Sprecher in der Arbeitskopie markieren.")


def _ton(quelle, d):
    """Ton als 16-kHz-Mono-Float-Array; Quelle: lokale Datei oder YouTube-URL/ID."""
    import numpy as np
    if os.path.exists(quelle):
        src = quelle
    else:
        src = os.path.join(d, "a.m4a")
        r = subprocess.run([YTDLP, "-f", "ba[ext=m4a]/ba", "-o", src, f"https://www.youtube.com/watch?v={vid(quelle)}"],
                           capture_output=True, text=True, timeout=900)
        if r.returncode or not os.path.exists(src):
            sys.exit(f"Ton nicht geladen: {r.stderr.strip()[:200]}")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def _f0(x, sr=16000, frame=0.04):
    """Grundton je 40-ms-Rahmen (Hz, nan = stimmlos/leise), Autokorrelation über FFT."""
    import numpy as np
    n = int(sr * frame)
    k = len(x) // n
    fr = x[:k * n].reshape(k, n).astype(np.float64)
    fr -= fr.mean(axis=1, keepdims=True)
    rms = np.sqrt((fr ** 2).mean(axis=1))
    spec = np.fft.rfft(fr, 2 * n, axis=1)
    ac = np.fft.irfft(np.abs(spec) ** 2, axis=1)[:, :n]
    # unverzerrt: ohne die Teilung bevorzugt die Autokorrelation kurze Verschiebungen und meldet tiefe
    # Stimmen eine halbe Oktave zu hoch (Johnson 137 statt 107 Hz, geeicht an Brown/INET 20.11.2026)
    ac = ac / (n - np.arange(n))[None, :] * n
    lo, hi = int(sr / 400), int(sr / 70)
    lag = lo + np.argmax(ac[:, lo:hi], axis=1)
    peak = ac[np.arange(k), lag]
    f = sr / lag
    leise = rms < max(0.01, np.percentile(rms, 30))
    f[leise | (peak < 0.3 * ac[:, 0])] = np.nan
    return f


def stimmlage(a):
    import numpy as np
    with tempfile.TemporaryDirectory() as d:
        x = _ton(a.quelle, d)
    f = _f0(x)
    per = int(round(a.schritt / 0.04))
    nwin = len(f) // per
    hz = np.array([np.nanmedian(w) if np.isfinite(w).sum() >= 3 else np.nan
                   for w in f[:nwin * per].reshape(nwin, per)])
    t0 = sec(a.von) if a.von else 0
    t1 = sec(a.bis) if a.bis else nwin * a.schritt
    # Referenzen: Name=von-bis → Median-Grundton
    refs = {}
    for r in a.ref or []:
        name, span = r.split("=", 1)
        r0, r1 = (sec(v) for v in span.split("-"))
        seg = f[int(r0 / 0.04):int(r1 / 0.04)]
        refs[name] = float(np.nanmedian(seg))
    if not refs:  # zwei Gruppen nach dem Grundton (log), grob
        v = np.log(hz[np.isfinite(hz)])
        c = np.percentile(v, [25, 75])
        for _ in range(20):
            lab = np.abs(v[:, None] - c[None]).argmin(1)
            c = np.array([v[lab == i].mean() if (lab == i).any() else c[i] for i in (0, 1)])
        refs = {"tief": float(np.exp(c[0])), "hoch": float(np.exp(c[1]))}
    print("Referenzen: " + " · ".join(f"{n} ~{v:.0f} Hz" for n, v in refs.items()))
    namen, mitte = list(refs), np.array(list(refs.values()))
    # Zuordnung je Fenster: nächste Referenz auf der log-Skala; zu weit weg → „?“
    lab = []
    for h in hz:
        if not np.isfinite(h):
            lab.append(None); continue
        dist = np.abs(np.log(h) - np.log(mitte))
        i = int(dist.argmin())
        lab.append(namen[i] if dist[i] < 0.35 else "?")
    # glätten: ein einzelnes abweichendes Fenster zwischen zwei gleichen übernimmt die Nachbarn
    for i in range(1, len(lab) - 1):
        if lab[i - 1] and lab[i - 1] == lab[i + 1] and lab[i] != lab[i - 1]:
            lab[i] = lab[i - 1]
    tx = cues(a.transkript) if a.transkript else []
    print(f"\n{'von':>8} {'bis':>8} {'Sprecher':<12} {'Hz':>5}  Textanfang")
    strecke = None
    def aus(s):
        if s and s[1] - s[0] >= a.schritt * 2:
            text = " ".join(t for c0, t in tx if s[0] <= c0 < s[1])[:70]
            print(f"{hms(s[0]):>8} {hms(s[1]):>8} {s[2]:<12} {np.nanmedian(s[3]):>5.0f}  {text}")
    for i, l in enumerate(lab):
        t = i * a.schritt
        if t < t0 or t >= t1 or l is None:
            continue
        if strecke and strecke[2] == l and t - strecke[1] <= 2 * a.schritt:
            strecke[1] = t + a.schritt; strecke[3].append(hz[i])
        else:
            aus(strecke); strecke = [t, t + a.schritt, l, [hz[i]]]
    aus(strecke)
    print("\nStrecken unter zwei Sekunden sind weggelassen. An jedem Wechsel ins Standbild sehen oder hineinhören;"
          " „?“ heißt: keine Referenz passt (dritte Stimme, Musik, Lachen).")


REAKT = re.compile(r"reag|reakt|react|kommentier|analysier[et] .*vortrag|spricht:|rechnet .*ab|\| ?\w+ reagiert", re.I)


def reaktion(a):
    m = meta(vid(a.video))
    titel, kanal, beschr = m.get("title", ""), m.get("channel", ""), m.get("description", "")
    treffer = bool(REAKT.search(titel) or REAKT.search(beschr[:600]))
    links = sorted(set(re.findall(r"https?://(?:www\.)?(?:youtube\.com/watch\?v=[\w-]{11}|youtu\.be/[\w-]{11})", beschr)))
    print(f"Titel: {titel}\nKanal: {kanal} · Länge {hms(m.get('duration') or 0)}")
    print("→ sieht nach REAKTIONSVIDEO aus" if treffer else "→ kein deutliches Reaktions-Signal (trotzdem hinhören)")
    for l in links[:8]:
        print("  mögliches Original:", l)
    if treffer:
        print("Regel: Original als Quelle nehmen. Gibt es keins, vor dem Schreiben `schnitte` laufen lassen und"
              " jeden Satz einem Sprecher zuordnen; in der Note steht dann ausdrücklich, wer kommentiert.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("abdeckung"); s.add_argument("video"); s.add_argument("datei"); s.set_defaults(f=abdeckung)
    s = sub.add_parser("schnitte"); s.add_argument("video"); s.add_argument("--transkript")
    s.add_argument("--db", type=float, default=-80); s.add_argument("--min", type=float, default=0.04); s.set_defaults(f=schnitte)
    s = sub.add_parser("reaktion"); s.add_argument("video"); s.set_defaults(f=reaktion)
    s = sub.add_parser("stimmlage"); s.add_argument("quelle", help="YouTube-URL/ID oder lokale Ton-/Videodatei")
    s.add_argument("--transkript"); s.add_argument("--von"); s.add_argument("--bis")
    s.add_argument("--ref", action="append", help="Name=von-bis an einer eindeutigen Stelle, mehrfach")
    s.add_argument("--schritt", type=float, default=1.0); s.set_defaults(f=stimmlage)
    a = p.parse_args(); a.f(a)
