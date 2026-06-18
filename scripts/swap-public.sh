#!/bin/bash
# swap-public.sh — atomarer Swap von public_new/ → public/ auf dem Pi.
# Wird vom Mac-Deploy (gwship) nach dem rsync aufgerufen.
# Nutzt DENSELBEN flock wie pull-and-build.sh (/tmp/gw-build.lock) → kann
# nie gleichzeitig mit dem 3-Uhr-Cron-Build swappen.

set -euo pipefail
cd /home/luc/services/gedankenwelten

exec 200>/tmp/gw-build.lock
flock -n 200 || { echo "[$(date '+%F %T')] build/swap läuft bereits — abgebrochen"; exit 1; }

# Sicherheit: nur swappen, wenn der frische Build wirklich vollständig ist
[ -f public_new/index.html ] || { echo "FEHLER: public_new/index.html fehlt — kein Swap"; exit 1; }

rm -rf public_old
[ -e public ] && mv public public_old
mv public_new public
rm -rf public_old
chmod -R o+r public

echo "[$(date '+%F %T')] swap-public done — neue Version live"
