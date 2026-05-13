#!/bin/bash
# sync-from-cortex.sh — Syncs Gedankenwelten notes from Cortex to the public repo
# Only .md files and image attachments. No transcripts, audio, or internal files.

set -euo pipefail

CORTEX_GW="$HOME/Cortex/Gedankenwelten"
PUBLIC_CONTENT="$HOME/Gedankenwelten/content"

# Folders to sync (only .md files)
SYNC_DIRS=(Denker DenkerVita Gedanken Zeitgeist Vipassana Panorama)

# Standalone files to sync
SYNC_FILES=("Quellen & Links.md" "Impressum.md" "known-speakers.md")

changed=false

# Sync each folder — only .md files, delete removed ones
for dir in "${SYNC_DIRS[@]}"; do
    if [ -d "$CORTEX_GW/$dir" ]; then
        mkdir -p "$PUBLIC_CONTENT/$dir"
        rsync -a \
            --include='*/' \
            --include='*.md' \
            --include='*.png' \
            --include='*.jpg' \
            --include='*.jpeg' \
            --include='*.svg' \
            --include='*.webp' \
            --exclude='*' \
            "$CORTEX_GW/$dir/" "$PUBLIC_CONTENT/$dir/"
    fi
done

# Sync standalone files
for file in "${SYNC_FILES[@]}"; do
    if [ -f "$CORTEX_GW/$file" ]; then
        cp "$CORTEX_GW/$file" "$PUBLIC_CONTENT/$file"
    fi
done

# Check for changes and commit
cd "$HOME/Gedankenwelten"
if ! git diff --quiet HEAD 2>/dev/null || [ -n "$(git ls-files --others --exclude-standard)" ]; then
    changed=true
    git add content/
    git commit -m "sync: Notes aus Cortex aktualisiert ($(date '+%d.%m.%Y %H:%M'))"
    git push origin main
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Synced and pushed changes"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] No changes to sync"
fi
