#!/bin/bash
set -e

ENVIRONMENT=${1:-staging}
MAX_RETRIES=3
RETRY_INTERVAL=10

if [ "$ENVIRONMENT" = "production" ] || [ "$ENVIRONMENT" = "prod" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
    BACKEND_URL="http://localhost:8000/api/products/"
    FRONTEND_URL="http://localhost/"
else
    COMPOSE_FILE="docker-compose.staging.yml"
    BACKEND_URL="http://localhost:8000/api/products/"
    FRONTEND_URL="http://localhost/"
fi

echo "Health check for ${ENVIRONMENT}..."

check_service() {
    local url=$1
    local name=$2
    if curl -sf --max-time 10 "${url}" > /dev/null 2>&1; then
        echo "  ✓ ${name} — OK"
        return 0
    else
        echo "  ✗ ${name} — FAIL"
        return 1
    fi
}

check_containers() {
    local down_containers
    down_containers=$(docker compose -f "${COMPOSE_FILE}" ps --format json 2>/dev/null | grep -v '"running"' | grep -v '"Up"' || true)
    if [ -z "$down_containers" ]; then
        echo "  ✓ All containers — Running"
        return 0
    else
        echo "  ✗ Some containers are not running"
        docker compose -f "${COMPOSE_FILE}" ps
        return 1
    fi
}

for i in $(seq 1 $MAX_RETRIES); do
    echo ""
    echo "Attempt ${i}/${MAX_RETRIES}..."

    PASSED=true

    check_containers || PASSED=false
    check_service "${BACKEND_URL}" "Backend API" || PASSED=false
    check_service "${FRONTEND_URL}" "Frontend" || PASSED=false

    if [ "$PASSED" = true ]; then
        echo ""
        echo "✅ Health check passed!"
        exit 0
    fi

    if [ "$i" -lt "$MAX_RETRIES" ]; then
        echo "Retrying in ${RETRY_INTERVAL}s..."
        sleep $RETRY_INTERVAL
    fi
done

echo ""
echo "❌ Health check failed after ${MAX_RETRIES} attempts"
exit 1
