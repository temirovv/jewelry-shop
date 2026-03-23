#!/bin/bash
set -e

# ============================================
#  Jewelry Shop — Automated DB Backup
#  Cron: 0 3 * * * /path/to/scripts/backup-db.sh
# ============================================

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$PROJECT_DIR/backups"
RETAIN_DAYS=${RETAIN_DAYS:-7}
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup-$TIMESTAMP.sql.gz"

# Load env
ENV_FILE="${1:-$PROJECT_DIR/.env}"
if [ -f "$ENV_FILE" ]; then
    DB_USER=$(grep -E '^DB_USER=' "$ENV_FILE" | cut -d'=' -f2 | tr -d ' ')
    DB_NAME=$(grep -E '^DB_NAME=' "$ENV_FILE" | cut -d'=' -f2 | tr -d ' ')
fi
DB_USER="${DB_USER:-postgres}"
DB_NAME="${DB_NAME:-jewelry_db}"
DB_CONTAINER="${DB_CONTAINER:-jewelry_db}"

mkdir -p "$BACKUP_DIR"

echo "[$(date)] Starting database backup..."

# Dump and compress
docker exec "$DB_CONTAINER" pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"

if [ $? -eq 0 ] && [ -s "$BACKUP_FILE" ]; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "[$(date)] Backup created: $BACKUP_FILE ($SIZE)"
else
    echo "[$(date)] ERROR: Backup failed!" >&2
    rm -f "$BACKUP_FILE"
    exit 1
fi

# Clean old backups (keep last RETAIN_DAYS days)
find "$BACKUP_DIR" -name "backup-*.sql.gz" -mtime +$RETAIN_DAYS -delete 2>/dev/null
REMAINING=$(find "$BACKUP_DIR" -name "backup-*.sql.gz" | wc -l)
echo "[$(date)] Cleanup done. $REMAINING backups retained."
