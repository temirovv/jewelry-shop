#!/bin/bash
set -e

# ============================================
#  Jewelry Shop — Healthcheck Script
#  Usage:
#    ./scripts/healthcheck.sh               # Production (default)
#    ./scripts/healthcheck.sh staging        # Staging
#    ./scripts/healthcheck.sh production     # Production
# ============================================

ENVIRONMENT=${1:-production}
MAX_RETRIES=3
RETRY_INTERVAL=10
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ "$ENVIRONMENT" = "staging" ]; then
    COMPOSE_FILE="docker-compose.staging.yml"
    LABEL="STAGING"
else
    ENVIRONMENT="production"
    COMPOSE_FILE="docker-compose.prod.yml"
    LABEL="PRODUCTION"
fi

ok()  { echo -e "\033[1;32m✓ $1\033[0m"; }
err() { echo -e "\033[1;31m✗ $1\033[0m"; }
log() { echo -e "\n\033[1;36m==> $1\033[0m"; }

log "Healthcheck — ${LABEL}"

for i in $(seq 1 $MAX_RETRIES); do
    echo ""
    echo "--- Urinish ${i}/${MAX_RETRIES} ---"
    PASSED=true

    # Containerlar tekshiruvi
    RUNNING=$(docker compose -f "$PROJECT_DIR/$COMPOSE_FILE" ps --status running -q 2>/dev/null | wc -l)
    if [ "$RUNNING" -ge 3 ]; then
        ok "Containerlar: ${RUNNING} ta ishlayapti"
    else
        err "Containerlar: faqat ${RUNNING} ta ishlayapti"
        PASSED=false
    fi

    # Backend API tekshiruvi
    if curl -sf --max-time 10 http://localhost:8080/api/products/ > /dev/null 2>&1; then
        ok "Backend API — javob bermoqda"
    else
        err "Backend API — javob bermayapti"
        PASSED=false
    fi

    # Frontend tekshiruvi
    if curl -sf --max-time 10 http://localhost:8080/ > /dev/null 2>&1; then
        ok "Frontend — javob bermoqda"
    else
        err "Frontend — javob bermayapti"
        PASSED=false
    fi

    if [ "$PASSED" = true ]; then
        echo ""
        ok "${LABEL} — Barcha servislar sog'lom!"
        exit 0
    fi

    if [ "$i" -lt "$MAX_RETRIES" ]; then
        echo "Qayta urinish ${RETRY_INTERVAL} soniyadan keyin..."
        sleep $RETRY_INTERVAL
    fi
done

echo ""
err "${LABEL} — Healthcheck muvaffaqiyatsiz!"
exit 1
