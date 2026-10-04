#!/usr/bin/env python3
"""
VTT → TXT Konverter mit klickbaren Zeitstempel-Links.
Verwendung: python3 vtt_to_txt.py <input.vtt> <output.txt> <youtube_url> [interval_seconds]
"""
import re
import sys
from collections import deque


def parse_time(ts):
    ts = ts.strip().replace(',', '.')
    parts = ts.split(':')
    try:
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        return int(parts[0]) * 60 + float(parts[1])
    except:
        return 0


def vtt_to_txt_with_timestamps(vtt_file, txt_file, youtube_url, interval_seconds=45):
    with open(vtt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    blocks = re.split(r'\n\n+', content)

    # Format EINMAL fuer die ganze Datei bestimmen, nicht pro Cue.
    # YouTube-Auto-Subs ("rolling captions") bestehen aus abwechselnd langen
    # Anzeige-Cues und 10-ms-Mikrocues; nur der Mikrocue traegt die neu
    # hinzugekommene Zeile. Wer das pro Cue entscheidet, kippt beim ersten
    # langen Cue in den Whisper-Zweig und schreibt jede Zeile 2-3x heraus.
    micro = 0
    for block in blocks:
        arrow_line = next((l for l in block.strip().split('\n') if '-->' in l), None)
        if not arrow_line:
            continue
        a, b = arrow_line.split('-->')
        if parse_time(b.split()[0]) - parse_time(a) <= 0.05:
            micro += 1
    is_whisper = youtube_url == "local" or micro < 5

    cues = []
    # Rolling Captions: der Mikrocue zeigt die stehengebliebenen Zeilen plus die
    # neu hinzugekommene(n). Wir merken uns die zuletzt ausgegebenen Zeilen und
    # nehmen aus jedem Cue genau das, was noch nicht dastand.
    zuletzt = deque(maxlen=8)
    zuletzt_set = set()
    for block in blocks:
        lines = block.strip().split('\n')
        arrow_line = next((l for l in lines if '-->' in l), None)
        if not arrow_line:
            continue
        parts = arrow_line.split('-->')
        start_sec = parse_time(parts[0])
        end_sec = parse_time(parts[1].split()[0])
        # Frueher wurden bei Auto-Subs alle Cues ueber 0,05 s uebersprungen, weil
        # "nur die Mikrocues den neuen Text tragen". Das stimmt fuer die Mitte
        # einer Untertitel-Seite, nicht fuer ihr Ende: Die letzte Zeile einer
        # Seite steht ausschliesslich im langen Anzeige-Cue und ging so komplett
        # verloren -- rund ein Fuenftel des Gesprochenen, und zwar immer das
        # Satzende. Jetzt laufen alle Cues durch; was doppelt ist, faengt das
        # Rolling-Set unten ab.
        text_lines = []
        for line in lines:
            if '-->' in line or re.match(r'^\d+$', line.strip()):
                continue
            clean = re.sub(r'<[^>]+>', '', line).strip()
            if clean:
                text_lines.append(clean)
        if text_lines:
            # Manuelle/Whisper-Untertitel: Cue ist ein ganzer Satz ueber mehrere
            # Zeilen umgebrochen -> alle Zeilen zusammenfuegen, sonst faellt der
            # halbe Satz weg.
            if is_whisper:
                text = ' '.join(text_lines)
            else:
                # Auto-Sub-Mikrocue: neu ist, was seit den letzten Cues nicht
                # dastand -- meist eine Zeile, beim Seitenwechsel der Rolling
                # Captions aber zwei auf einmal. Frueher wurde blind die letzte
                # genommen; das halbierte jeden zweizeiligen Cue und riss Saetze
                # mitten durch (~20 % des Gesprochenen fielen weg).
                neu_zeilen = [l for l in text_lines if l not in zuletzt_set]
                if not neu_zeilen:
                    continue
                text = ' '.join(neu_zeilen)
            for l in text_lines:
                if l in zuletzt_set:
                    continue
                if len(zuletzt) == zuletzt.maxlen:
                    zuletzt_set.discard(zuletzt[0])
                zuletzt.append(l)
                zuletzt_set.add(l)
            cues.append((int(start_sec), text))
    seen = set()
    unique_cues = [(s, t) for s, t in cues if t not in seen and not seen.add(t)]
    output_parts = []
    last_ts = -interval_seconds
    for sec, text in unique_cues:
        if sec - last_ts >= interval_seconds:
            mm, ss = sec // 60, sec % 60
            sep = '&' if '?' in youtube_url else '?'
            output_parts.append(f"\n[▶ {mm}:{ss:02d}]({youtube_url}{sep}t={sec})")
            last_ts = sec
        output_parts.append(text)
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_parts).strip())
    print(f"Done: {txt_file}")


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Verwendung: python3 vtt_to_txt.py <input.vtt> <output.txt> <youtube_url> [interval_seconds]")
        sys.exit(1)
    vtt_file = sys.argv[1]
    txt_file = sys.argv[2]
    youtube_url = sys.argv[3]
    interval = int(sys.argv[4]) if len(sys.argv) > 4 else 45
    vtt_to_txt_with_timestamps(vtt_file, txt_file, youtube_url, interval)
