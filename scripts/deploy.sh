#!/bin/bash
set -e

ENVIRONMENT=${1:-staging}

if [ "$ENVIRONMENT" = "production" ] || [ "$ENVIRONMENT" = "prod" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
    ENV_LABEL="Production"
elif [ "$ENVIRONMENT" = "staging" ]; then
    COMPOSE_FILE="docker-compose.staging.yml"
    ENV_LABEL="Staging"
else
    echo "Usage: ./scripts/deploy.sh [staging|production]"
    exit 1
fi

echo "============================================"
echo "  Deploying to ${ENV_LABEL}"
echo "============================================"

echo ""
echo "==> Pulling latest code..."
git pull origin "$(git branch --show-current)"

echo ""
echo "==> Building containers..."
docker compose -f "${COMPOSE_FILE}" build --no-cache

echo ""
echo "==> Starting services..."
docker compose -f "${COMPOSE_FILE}" up -d

echo ""
echo "==> Waiting for services to start..."
sleep 30

echo ""
echo "==> Running migrations..."
docker compose -f "${COMPOSE_FILE}" exec -T backend python manage.py migrate --noinput

echo ""
echo "==> Collecting static files..."
docker compose -f "${COMPOSE_FILE}" exec -T backend python manage.py collectstatic --noinput

echo ""
echo "==> Cleaning up old images..."
docker image prune -f

echo ""
echo "============================================"
echo "  ${ENV_LABEL} deploy completed!"
echo "============================================"
