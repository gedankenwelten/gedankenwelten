#!/bin/bash
# Sync Notes aus dem privaten Cortex-Vault ins öffentliche Quartz-Repo.
# Aufruf: ./scripts/sync.sh [--dry-run]

set -e

CORTEX="$HOME/Cortex/Gedankenwelten"
QUARTZ="$(cd "$(dirname "$0")/.." && pwd)/content"

DRY=""
if [[ "$1" == "--dry-run" ]]; then
  DRY="--dry-run"
  echo "DRY RUN — keine Änderungen werden gespeichert"
fi

echo "Syncing Denker..."
rsync -av --delete $DRY   --exclude="*.vtt"   --exclude="*.mp3"   --exclude="index.md"   "$CORTEX/Denker/" "$QUARTZ/Denker/"

echo ""
echo "Syncing Zeitgeist..."
rsync -av --delete $DRY   --exclude="*.vtt"   --exclude="*.mp3"   --exclude="index.md"   "$CORTEX/Zeitgeist/" "$QUARTZ/Zeitgeist/"

echo ""
echo "Syncing DenkerVita..."
rsync -av --delete $DRY   --exclude="*.vtt"   --exclude="*.mp3"   "$CORTEX/DenkerVita/" "$QUARTZ/DenkerVita/"

echo ""
echo "Syncing Gedanken..."
rsync -av --delete $DRY   --exclude="*.vtt"   --exclude="*.mp3"   --exclude="index.md"   "$CORTEX/Gedanken/" "$QUARTZ/Gedanken/"

echo ""
echo "Syncing Panorama..."
rsync -av --delete $DRY   --exclude="*.vtt"   --exclude="*.mp3"   --exclude="index.md"   "$CORTEX/Panorama/" "$QUARTZ/Panorama/"

echo ""
echo "Syncing Vipassana..."
rsync -av --delete $DRY   --exclude="*.vtt"   --exclude="*.mp3"   --exclude="*.mp4"   --exclude="index.md"   "$CORTEX/Vipassana/" "$QUARTZ/Vipassana/"

echo ""
echo "Sync abgeschlossen."
echo "Nächste Schritte: git add -A && git commit -m 'sync: Notes aktualisiert' && git push"
