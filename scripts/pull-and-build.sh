#!/bin/bash
# pull-and-build.sh — Zero-Downtime Build für Gedankenwelten.
#
# Baut in public_new/, dann atomarer Swap mit public/.
# Während des Builds (3 Min) serviert Caddy weiter die alte Version.

set -euo pipefail

REPO="/home/luc/services/gedankenwelten"
cd "$REPO"

# Prüfen ob es neue Commits gibt — nur dann bauen
OLD_HEAD=$(git rev-parse HEAD)
git fetch origin --quiet
NEW_HEAD=$(git rev-parse origin/main)

if [ "$OLD_HEAD" = "$NEW_HEAD" ]; then
    exit 0
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] pull-and-build: $OLD_HEAD → $NEW_HEAD"

git reset --hard origin/main

# In temporäres Verzeichnis bauen (public/ bleibt live)
rm -rf public_new
npx quartz build -o public_new

chmod -R o+r public_new/

# Atomarer Swap: alte Version erst ersetzen wenn neuer Build fertig ist
mv public public_old
mv public_new public
rm -rf public_old

echo "[$(date '+%Y-%m-%d %H:%M:%S')] pull-and-build done (zero-downtime)"
