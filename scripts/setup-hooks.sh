#!/bin/bash
# setup-hooks.sh — Installiert Git-Hooks für automatische Wiki-Rebuilds.
# Wird einmalig nach dem Klonen ausgeführt, oder automatisch via `npm run setup`.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HOOKS_DIR="$(dirname "$SCRIPT_DIR")/.git/hooks"

if [ ! -d "$HOOKS_DIR" ]; then
    echo "Kein .git/hooks Verzeichnis gefunden — bist du im Repo-Root?"
    exit 1
fi

cp "${SCRIPT_DIR}/post-merge" "${HOOKS_DIR}/post-merge"
chmod +x "${HOOKS_DIR}/post-merge"

echo "✓ Git-Hooks installiert."
echo "  → Wiki wird nach 'git pull' automatisch rebuilt (wenn Docker läuft)."
