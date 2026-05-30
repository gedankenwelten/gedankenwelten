#!/bin/bash
# Maintainer-only: Sync Notes aus dem privaten Cortex-Vault ins öffentliche Repo.
# Setzt $HOME/Cortex/Gedankenwelten voraus — nur für den Repo-Maintainer gedacht.
# Externe Nutzer: einfach `git clone` + `docker compose up` — Content ist bereits im Repo.
# Aufruf: ./scripts/sync.sh [--dry-run]

set -e

if [ ! -d "$HOME/Cortex/Gedankenwelten" ]; then
  echo "Cortex nicht gefunden unter $HOME/Cortex/Gedankenwelten"
  echo "Dieses Script ist nur für den Repo-Maintainer gedacht."
  echo "Externe Nutzer: Content ist bereits im Repo — einfach docker compose up."
  exit 1
fi

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
echo "Syncing GoodNews..."
rsync -av $DRY   --exclude="*.vtt"   --exclude="*.mp3"   --exclude="index.md"   "$CORTEX/GoodNews/" "$QUARTZ/GoodNews/"

echo ""
echo "Syncing Vipassana..."
rsync -av --delete $DRY   --exclude="*.vtt"   --exclude="*.mp3"   --exclude="*.mp4"   --exclude="index.md"   "$CORTEX/Vipassana/" "$QUARTZ/Vipassana/"

echo ""
echo "Sync abgeschlossen."

# Post-Sync: Wikilink-Prefix "Gedankenwelten/" strippen
# Im Cortex-Vault sind Pfade wie [[Gedankenwelten/DenkerVita/Name]] korrekt,
# aber im Quartz-Content gibt es kein Gedankenwelten/-Verzeichnis.
if [[ -z "$DRY" ]]; then
  echo ""
  echo "Fixing wikilinks (stripping Gedankenwelten/ prefix)..."
  find "$QUARTZ" -name "*.md" -exec sed -i '' 's/\[\[Gedankenwelten\//\[\[/g' {} +
  FIXED=$(grep -rl '\[\[Gedankenwelten/' "$QUARTZ" --include="*.md" 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$FIXED" -gt 0 ]]; then
    echo "⚠ Noch $FIXED Dateien mit Gedankenwelten/-Prefix übrig"
  else
    echo "✓ Alle Gedankenwelten/-Prefixe entfernt"
  fi
fi

echo ""
echo "Nächste Schritte: git add -A && git commit -m 'sync: Notes aktualisiert' && git push"
