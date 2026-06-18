#!/bin/bash
# pull-and-build.sh — Zero-Downtime Build für Gedankenwelten.
#
# Baut in public_new/, dann atomarer Swap mit public/.
# Während des Builds (~3 Min) serviert Caddy weiter die alte Version.

set -euo pipefail

REPO="/home/luc/services/gedankenwelten"
cd "$REPO"

# Nur EIN Build gleichzeitig. Ohne diesen Lock rasen Cron + manueller Lauf auf
# den Swap (mv public public_old; mv public_new public) und zerlegen public/.
# (18.06.2026: genau das hatte die Site offline genommen.)
exec 200>/tmp/gw-build.lock
flock -n 200 || { echo "[$(date '+%F %T')] build läuft bereits — übersprungen"; exit 0; }

# Prüfen ob es neue Commits gibt — nur dann bauen.
# ABER: auch bauen, wenn public/ kaputt ist (kein index.html) → Selbstheilung,
# falls ein früherer Swap abgebrochen ist.
OLD_HEAD=$(git rev-parse HEAD)
git fetch origin --quiet
NEW_HEAD=$(git rev-parse origin/main)

if [ "$OLD_HEAD" = "$NEW_HEAD" ] && [ -f public/index.html ]; then
    exit 0
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] pull-and-build: $OLD_HEAD → $NEW_HEAD"

git reset --hard origin/main

# In temporäres Verzeichnis bauen (public/ bleibt live)
rm -rf public_new
npx quartz build -o public_new

chmod -R o+r public_new/

# Atomarer Swap: alte Version erst ersetzen wenn neuer Build fertig ist.
# Durch flock gegen parallele Läufe geschützt; defensiv gegen Reste.
rm -rf public_old
[ -e public ] && mv public public_old
mv public_new public
rm -rf public_old

# Neue/geänderte Seiten an IndexNow melden (Bing & Co.) — Sitemap ist jetzt frisch
python3 "$REPO/scripts/indexnow_ping.py" || true

echo "[$(date '+%Y-%m-%d %H:%M:%S')] pull-and-build done (zero-downtime)"
