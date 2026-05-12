#!/usr/bin/env python3
"""
VTT → TXT Konverter mit klickbaren Zeitstempel-Links.
Verwendung: python3 vtt_to_txt.py <input.vtt> <output.txt> <youtube_url> [interval_seconds]
"""
import re
import sys


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
    cues = []
    for block in re.split(r'\n\n+', content):
        lines = block.strip().split('\n')
        arrow_line = next((l for l in lines if '-->' in l), None)
        if not arrow_line:
            continue
        parts = arrow_line.split('-->')
        start_sec = parse_time(parts[0])
        end_sec = parse_time(parts[1].split()[0])
        # YouTube auto-subs: skip long cues (only keep micro-transition cues)
        # Whisper/mlx-whisper: skip this filter (sentence-level cues are long)
        # "local" = Whisper without YouTube link; any URL = try YouTube links
        # Auto-detect Whisper format by cue duration (sentence-level = >1s)
        is_whisper = youtube_url == "local"
        if not is_whisper and end_sec - start_sec > 1.0:
            # Long cue → likely Whisper-generated VTT, not YouTube auto-sub
            is_whisper = True
        if not is_whisper and end_sec - start_sec > 0.05:
            continue
        text_lines = []
        for line in lines:
            if '-->' in line or re.match(r'^\d+$', line.strip()):
                continue
            clean = re.sub(r'<[^>]+>', '', line).strip()
            if clean:
                text_lines.append(clean)
        if text_lines:
            cues.append((int(start_sec), text_lines[0]))
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
