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
    a = p.parse_args(); a.f(a)
