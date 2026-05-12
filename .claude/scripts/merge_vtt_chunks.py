#!/usr/bin/env python3
"""
merge_vtt_chunks.py — Merges chunked Whisper VTT files into a single VTT.

Corrects timestamps by adding the chunk offset (chunk_index * chunk_duration)
so the final VTT has continuous, correct timestamps.

Usage:
    python3 merge_vtt_chunks.py <chunks_dir> <output_vtt> --chunk-duration <seconds>

Example:
    python3 merge_vtt_chunks.py /tmp/whisper_chunks/ \
        "Gedankenwelten/Transkripte/output.vtt" \
        --chunk-duration 1500
"""

import argparse
import re
from pathlib import Path


def parse_timestamp(ts: str) -> float:
    """Parse VTT timestamp (HH:MM:SS.mmm or MM:SS.mmm) to seconds."""
    match = re.match(r"(\d+):(\d+):(\d+)\.(\d+)", ts)
    if match:
        h, m, s, ms = match.groups()
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
    match = re.match(r"(\d+):(\d+)\.(\d+)", ts)
    if match:
        m, s, ms = match.groups()
        return int(m) * 60 + int(s) + int(ms) / 1000
    raise ValueError(f"Invalid timestamp: {ts}")


def format_timestamp(seconds: float) -> str:
    """Format seconds to VTT timestamp (HH:MM:SS.mmm)."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def merge_vtt_chunks(chunks_dir: Path, output_path: Path, chunk_duration: int):
    """Merge sorted VTT chunk files with timestamp correction."""
    vtt_files = sorted(chunks_dir.glob("chunk_*.vtt"))
    if not vtt_files:
        print(f"No chunk_*.vtt files found in {chunks_dir}")
        return

    timestamp_re = re.compile(
        r"(\d+:\d+(?::\d+)?\.\d+)\s*-->\s*(\d+:\d+(?::\d+)?\.\d+)"
    )

    merged_lines = ["WEBVTT", ""]

    for i, vtt_file in enumerate(vtt_files):
        offset = i * chunk_duration
        content = vtt_file.read_text(encoding="utf-8")
        lines = content.strip().split("\n")

        # Skip WEBVTT header and any blank lines after it
        j = 0
        while j < len(lines) and (
            lines[j].startswith("WEBVTT")
            or lines[j].startswith("Kind:")
            or lines[j].startswith("Language:")
            or lines[j].strip() == ""
        ):
            j += 1

        for line in lines[j:]:
            match = timestamp_re.match(line)
            if match:
                start = parse_timestamp(match.group(1)) + offset
                end = parse_timestamp(match.group(2)) + offset
                merged_lines.append(
                    f"{format_timestamp(start)} --> {format_timestamp(end)}"
                )
            else:
                merged_lines.append(line)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(merged_lines) + "\n", encoding="utf-8")
    print(f"Merged {len(vtt_files)} chunks → {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Merge chunked Whisper VTT files with timestamp correction."
    )
    parser.add_argument("chunks_dir", type=Path, help="Directory with chunk_*.vtt files")
    parser.add_argument("output", type=Path, help="Output VTT file path")
    parser.add_argument(
        "--chunk-duration",
        type=int,
        default=1500,
        help="Duration of each chunk in seconds (default: 1500 = 25 min)",
    )
    args = parser.parse_args()
    merge_vtt_chunks(args.chunks_dir, args.output, args.chunk_duration)


if __name__ == "__main__":
    main()
