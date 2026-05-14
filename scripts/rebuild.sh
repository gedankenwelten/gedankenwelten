#!/bin/bash
# rebuild.sh — Rebuildet die Gedankenwelten-Wiki im Docker-Container.
#
# Wird automatisch aufgerufen nach:
#   - git pull (via post-merge Hook)
#   - Note-Erstellung durch KI-Pipeline
#
# Kann auch manuell aufgerufen werden:
#   ./scripts/rebuild.sh
#
# Was passiert:
#   1. Prüft ob der Docker-Container läuft
#   2. Triggert einen Full-Rebuild von Quartz im Container
#   3. Wartet bis der Build fertig ist

set -euo pipefail

COMPOSE_PROJECT="gedankenwelten"
CONTAINER_NAME="${COMPOSE_PROJECT}-wiki-1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Farben (nur wenn Terminal)
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    RED='\033[0;31m'
    NC='\033[0m'
else
    GREEN='' YELLOW='' RED='' NC=''
fi

log()  { echo -e "${GREEN}▸${NC} $1"; }
warn() { echo -e "${YELLOW}▸${NC} $1"; }
err()  { echo -e "${RED}✗${NC} $1" >&2; }

# Prüfe ob Docker läuft
if ! docker info >/dev/null 2>&1; then
    err "Docker läuft nicht. Bitte Docker starten."
    exit 1
fi

# Prüfe ob Container existiert und läuft
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    warn "Container '${CONTAINER_NAME}' läuft nicht."
    warn "Starte mit: cd ${PROJECT_DIR} && docker compose up -d"

    # Versuche zu starten wenn docker-compose.yml vorhanden
    if [ -f "${PROJECT_DIR}/docker-compose.yml" ]; then
        log "Starte Container automatisch..."
        cd "$PROJECT_DIR"
        docker compose up -d --build 2>&1
        log "Container gestartet — Wiki unter http://localhost:9999"
        exit 0
    fi
    exit 1
fi

# Rebuild: Container neustarten damit Quartz alle Dateien neu baut
log "Rebuilde Gedankenwelten-Wiki..."

cd "$PROJECT_DIR"
docker compose restart wiki 2>&1

# Warte auf Build-Abschluss (max 120s)
log "Warte auf Quartz-Build..."
TIMEOUT=120
ELAPSED=0
while [ $ELAPSED -lt $TIMEOUT ]; do
    if docker logs --since "${ELAPSED}s" "$CONTAINER_NAME" 2>&1 | grep -q "Started a Quartz server"; then
        NOTES=$(docker logs --since "${ELAPSED}s" "$CONTAINER_NAME" 2>&1 | grep "Parsed" | tail -1)
        log "✓ Wiki rebuilt — ${NOTES:-Build abgeschlossen}"
        log "  → http://localhost:9999"
        exit 0
    fi
    sleep 2
    ELAPSED=$((ELAPSED + 2))
done

warn "Build dauert länger als erwartet. Logs prüfen mit: docker logs -f ${CONTAINER_NAME}"
exit 0
