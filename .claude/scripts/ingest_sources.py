#!/usr/bin/env python3
"""Embed the Gedankenwelten source index into Qdrant.

Reads `.claude/data/sources.jsonl` (produced by extract_sources.py), embeds each
source with BAAI/bge-m3 and upserts one point per source into the Qdrant collection
`gedankenwelten_sources`. The MCP `find_sources` tool queries this collection.

Designed to run on the Pi from the gedankenwelten-mcp image (model + deps baked in):

    docker run --rm --network host \\
      -v ~/services/cortex/.claude/scripts:/scripts:ro \\
      -v ~/services/cortex/.claude/data:/data:ro \\
      -e QDRANT_URL=http://127.0.0.1:6333 \\
      gedankenwelten-mcp-gedankenwelten-mcp:latest \\
      python3 /scripts/ingest_sources.py --input /data/sources.jsonl

Incremental by default: points whose content hash is unchanged are skipped, so
re-running after adding a single note only embeds the new/changed sources.
Use --recreate for a clean full rebuild.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
)

VECTOR_NAME = "text"          # must match the server's query (using="text")
VECTOR_SIZE = 1024            # bge-m3 dense dim
NAMESPACE = uuid.UUID("6f1d3b2a-0000-4000-8000-000000000001")  # stable id namespace


def embed_text(rec: dict) -> str:
    """Build the text that represents this source for semantic retrieval.

    Context-rich: the source's own identity (title + description) PLUS the citing
    note titles and topic tags. Tested against title-only and title+note-title
    variants — this composition is the only one that reliably surfaces the
    genuinely on-topic sources for abstract topic queries (e.g. "Faschismus" →
    Gramsci, Quent, FES-Mitte-Studie), because many sources have bare link-text
    titles ("Fox News", "Bundestag") with no semantic anchor of their own.
    Tail noise from heavily-tagged notes is handled by the `tag`/`type` filters
    on find_sources, not by stripping context here. Junk titles are cleaned at
    extraction time (extract_sources.py), so the context is the signal that
    differentiates otherwise-identical bare titles.
    """
    parts = [rec.get("title", "")]
    if rec.get("description"):
        parts.append(rec["description"])
    if rec.get("note_titles"):
        parts.append(" / ".join(rec["note_titles"][:4]))
    if rec.get("tags"):
        parts.append(" ".join(rec["tags"]))
    return " — ".join(p for p in parts if p)


def content_hash(rec: dict) -> str:
    basis = embed_text(rec) + "|" + rec.get("type", "") + "|" + str(sorted(rec.get("notes", [])))
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()


def point_id(url: str) -> str:
    return str(uuid.uuid5(NAMESPACE, url))


def load_records(path: str) -> list[dict]:
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def ensure_collection(client: QdrantClient, name: str, recreate: bool) -> None:
    exists = client.collection_exists(name)
    if exists and recreate:
        client.delete_collection(name)
        exists = False
    if not exists:
        client.create_collection(
            collection_name=name,
            vectors_config={VECTOR_NAME: VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)},
        )
        print(f"Collection '{name}' angelegt.")


def existing_hashes(client: QdrantClient, name: str) -> dict[str, str]:
    """Map point_id -> stored content hash, for incremental skip."""
    hashes: dict[str, str] = {}
    offset = None
    while True:
        points, offset = client.scroll(
            collection_name=name, with_payload=["_hash"], with_vectors=False,
            limit=512, offset=offset,
        )
        for p in points:
            hashes[str(p.id)] = (p.payload or {}).get("_hash", "")
        if offset is None:
            break
    return hashes


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="Path to sources.jsonl")
    ap.add_argument("--collection", default=os.getenv("SOURCES_COLLECTION", "gedankenwelten_sources"))
    ap.add_argument("--qdrant-url", default=os.getenv("QDRANT_URL", "http://127.0.0.1:6333"))
    ap.add_argument("--recreate", action="store_true", help="Drop and rebuild the collection")
    ap.add_argument("--purge-missing", action="store_true",
                    help="Delete points whose URL is no longer in the input")
    ap.add_argument("--batch", type=int, default=64)
    args = ap.parse_args()

    records = load_records(args.input)
    print(f"{len(records)} Quellen aus {args.input} geladen.")

    client = QdrantClient(url=args.qdrant_url, timeout=120)
    ensure_collection(client, args.collection, args.recreate)

    prior = {} if args.recreate else existing_hashes(client, args.collection)
    if prior:
        print(f"{len(prior)} bestehende Punkte gefunden (für inkrementellen Skip).")

    from sentence_transformers import SentenceTransformer
    model = None  # lazy: only load if there is something to embed

    current_ids: set[str] = set()
    to_embed: list[tuple[str, dict, str]] = []  # (pid, record, hash)
    skipped = 0
    for rec in records:
        pid = point_id(rec["url"])
        current_ids.add(pid)
        h = content_hash(rec)
        if prior.get(pid) == h:
            skipped += 1
            continue
        to_embed.append((pid, rec, h))

    print(f"Zu embedden: {len(to_embed)} | übersprungen (unverändert): {skipped}")

    if to_embed:
        model = SentenceTransformer(os.getenv("EMBED_MODEL", "BAAI/bge-m3"))
        upserted = 0
        for i in range(0, len(to_embed), args.batch):
            chunk = to_embed[i:i + args.batch]
            texts = [embed_text(r) for _, r, _ in chunk]
            vecs = model.encode(texts, normalize_embeddings=True)
            points = []
            for (pid, rec, h), vec in zip(chunk, vecs):
                payload = dict(rec)
                payload["_hash"] = h
                points.append(PointStruct(id=pid, vector={VECTOR_NAME: vec.tolist()}, payload=payload))
            client.upsert(collection_name=args.collection, points=points)
            upserted += len(points)
            print(f"  upserted {upserted}/{len(to_embed)}")
        print(f"Fertig: {upserted} Quellen ingestiert.")

    if args.purge_missing and not args.recreate:
        prior_ids = set(prior.keys())
        stale = list(prior_ids - current_ids)
        if stale:
            client.delete(collection_name=args.collection, points_selector=stale)
            print(f"{len(stale)} veraltete Quellen entfernt.")

    info = client.get_collection(args.collection)
    print(f"Collection '{args.collection}': {info.points_count} Punkte.")


if __name__ == "__main__":
    main()
