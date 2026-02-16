#!/bin/bash
set -e

# ============================================
#  Jewelry Shop — Deploy Script
#  Usage:
#    ./scripts/deploy.sh setup          # Server tayyorlash (1 marta)
#    ./scripts/deploy.sh deploy         # To'liq deploy (production)
#    ./scripts/deploy.sh deploy staging # Staging deploy
#    ./scripts/deploy.sh ssl            # SSL sertifikat olish
#    ./scripts/deploy.sh backup         # Database backup
#    ./scripts/deploy.sh logs           # Loglarni ko'rish
#    ./scripts/deploy.sh status         # Servislar holati
#    ./scripts/deploy.sh rollback       # Oxirgi backupdan tiklash
# ============================================

COMMAND=${1:-help}
ENVIRONMENT=${2:-production}
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DOMAIN="luxgold.uz"

# Muhit sozlamalari
if [ "$ENVIRONMENT" = "staging" ]; then
    COMPOSE_FILE="docker-compose.staging.yml"
    BRANCH="develop"
    ENV_FILE=".env.staging"
    DIST_VOLUME="jewelry-shop_frontend_staging_dist"
    LABEL="STAGING"
else
    ENVIRONMENT="production"
    COMPOSE_FILE="docker-compose.prod.yml"
    BRANCH="main"
    ENV_FILE=".env"
    DIST_VOLUME="jewelry-shop_frontend_dist"
    LABEL="PRODUCTION"
fi

# .env dan DB sozlamalarini o'qish
if [ -f "$PROJECT_DIR/$ENV_FILE" ]; then
    DB_USER=$(grep -E '^DB_USER=' "$PROJECT_DIR/$ENV_FILE" | cut -d'=' -f2 | tr -d ' ')
    DB_NAME=$(grep -E '^DB_NAME=' "$PROJECT_DIR/$ENV_FILE" | cut -d'=' -f2 | tr -d ' ')
fi
DB_USER="${DB_USER:-postgres}"
DB_NAME="${DB_NAME:-jewelry_db}"

log() { echo -e "\n\033[1;36m==> $1\033[0m"; }
ok()  { echo -e "\033[1;32m✓ $1\033[0m"; }
err() { echo -e "\033[1;31m✗ $1\033[0m"; }

# ---- SETUP: Server tayyorlash ----
cmd_setup() {
    log "Serverni yangilash..."
    sudo apt update && sudo apt upgrade -y

    log "Docker o'rnatish..."
    if ! command -v docker &>/dev/null; then
        curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
        sudo sh /tmp/get-docker.sh && rm /tmp/get-docker.sh
        sudo usermod -aG docker "$USER"
        ok "Docker o'rnatildi"
    else
        ok "Docker allaqachon o'rnatilgan: $(docker --version)"
    fi

    log "Docker Compose, Nginx, Certbot o'rnatish..."
    sudo apt install -y docker-compose-plugin nginx certbot python3-certbot-nginx git curl
    ok "Paketlar o'rnatildi"

    log "Firewall sozlash..."
    sudo ufw allow OpenSSH
    sudo ufw allow 'Nginx Full'
    echo "y" | sudo ufw enable
    ok "Firewall yoqildi"

    log "Deploy key yaratish (private repo uchun)..."
    if [ ! -f ~/.ssh/deploy_key ]; then
        ssh-keygen -t ed25519 -C "deploy-key" -f ~/.ssh/deploy_key -N ""
        echo ""
        echo "============================================"
        echo "  Quyidagi key ni GitHub Deploy Keys ga"
        echo "  qo'shing (repo → Settings → Deploy keys):"
        echo "============================================"
        echo ""
        cat ~/.ssh/deploy_key.pub
        echo ""
        echo "Qo'shganingizdan keyin Enter bosing..."
        read -r
    else
        ok "Deploy key allaqachon mavjud"
    fi

    log "GitHub Actions SSH key yaratish..."
    if [ ! -f ~/.ssh/github_actions ]; then
        ssh-keygen -t ed25519 -C "github-actions" -f ~/.ssh/github_actions -N ""
        cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys
        echo ""
        echo "============================================"
        echo "  GitHub Secrets ga qo'shing:"
        echo "  PROD_SSH_KEY ="
        echo "============================================"
        cat ~/.ssh/github_actions
        echo ""
    else
        ok "GitHub Actions key allaqachon mavjud"
    fi

    log "Loyihani klonlash..."
    if [ ! -d /var/www/jewelry-shop ]; then
        sudo mkdir -p /var/www
        cd /var/www
        GIT_SSH_COMMAND="ssh -i ~/.ssh/deploy_key -o StrictHostKeyChecking=no" \
            git clone git@github.com:temirovv/jewelry-shop.git
        cd jewelry-shop
        git config core.sshCommand "ssh -i ~/.ssh/deploy_key -o StrictHostKeyChecking=no"
        mkdir -p backups
        ok "Loyiha klonlandi: /var/www/jewelry-shop"
    else
        ok "Loyiha allaqachon mavjud: /var/www/jewelry-shop"
    fi

    echo ""
    echo "============================================"
    echo "  Setup tugadi!"
    echo ""
    echo "  Keyingi qadamlar:"
    echo "  1) cd /var/www/jewelry-shop"
    echo "  2) nano .env          (env faylni to'ldiring)"
    echo "  3) ./scripts/deploy.sh deploy"
    echo "  4) ./scripts/deploy.sh ssl"
    echo "============================================"
}

# ---- DEPLOY: To'liq deploy ----
cmd_deploy() {
    cd "$PROJECT_DIR"
    echo ""
    echo "============================================"
    echo "  Deploying to ${LABEL}"
    echo "============================================"

    # Env fayl tekshirish
    if [ ! -f "$ENV_FILE" ]; then
        err "${ENV_FILE} topilmadi! Avval yarating."
        exit 1
    fi

    log "Kodni yangilash..."
    git fetch origin "$BRANCH"
    git reset --hard "origin/${BRANCH}"

    log "Eski frontend buildni tozalash..."
    docker compose -f "$COMPOSE_FILE" down frontend nginx 2>/dev/null || true
    docker volume rm "$DIST_VOLUME" 2>/dev/null || true

    log "Barcha servislarni build va ishga tushirish..."
    docker compose -f "$COMPOSE_FILE" up -d --build

    log "Servislar tayyor bo'lishini kutish..."
    sleep 15

    log "Eski imagelarni tozalash..."
    docker image prune -f

    log "Health check..."
    cmd_health

    echo ""
    ok "${LABEL} deploy muvaffaqiyatli!"
}

# ---- SSL: Sertifikat olish ----
cmd_ssl() {
    log "Nginx default configni o'chirish..."
    sudo rm -f /etc/nginx/sites-enabled/default

    log "Vaqtincha config yaratish..."
    sudo tee /etc/nginx/sites-available/luxgold > /dev/null <<NGINXEOF
server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};
    location / { proxy_pass http://127.0.0.1:8080; }
}
NGINXEOF

    sudo ln -sf /etc/nginx/sites-available/luxgold /etc/nginx/sites-enabled/
    sudo nginx -t && sudo systemctl restart nginx

    log "SSL sertifikat olish..."
    sudo certbot --nginx -d "$DOMAIN" -d "www.${DOMAIN}"

    log "HTTPS config yozish..."
    sudo tee /etc/nginx/sites-available/luxgold > /dev/null <<NGINXEOF
server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ${DOMAIN} www.${DOMAIN};

    ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
NGINXEOF

    sudo nginx -t && sudo systemctl restart nginx
    ok "SSL tayyor! https://${DOMAIN}"
}

# ---- BACKUP: Database backup ----
cmd_backup() {
    cd "$PROJECT_DIR"
    mkdir -p backups
    BACKUP_FILE="backups/backup-$(date +%Y%m%d-%H%M%S).sql"

    log "Database backup yaratish..."
    docker compose -f "$COMPOSE_FILE" exec -T db pg_dump -U "$DB_USER" "$DB_NAME" > "$BACKUP_FILE"

    # Oxirgi 5 ta backup saqlash
    ls -t backups/backup-*.sql 2>/dev/null | tail -n +6 | xargs -r rm --
    ok "Backup: ${BACKUP_FILE}"
}

# ---- ROLLBACK: Oxirgi backupdan tiklash ----
cmd_rollback() {
    cd "$PROJECT_DIR"
    LATEST=$(ls -t backups/backup-*.sql 2>/dev/null | head -1)

    if [ -z "$LATEST" ]; then
        err "Backup topilmadi!"
        exit 1
    fi

    log "Tiklanmoqda: ${LATEST}"
    cat "$LATEST" | docker compose -f "$COMPOSE_FILE" exec -T db psql -U "$DB_USER" "$DB_NAME"
    ok "Database tiklandi"
}

# ---- HEALTH: Servislar sog'ligini tekshirish ----
cmd_health() {
    cd "$PROJECT_DIR"
    MAX_RETRIES=3
    RETRY_INTERVAL=10

    for i in $(seq 1 $MAX_RETRIES); do
        PASSED=true

        # Containerlar
        RUNNING=$(docker compose -f "$COMPOSE_FILE" ps --status running -q 2>/dev/null | wc -l)
        if [ "$RUNNING" -ge 3 ]; then
            ok "Containerlar: ${RUNNING} ta ishlayapti"
        else
            err "Containerlar: faqat ${RUNNING} ta ishlayapti"
            PASSED=false
        fi

        # Backend
        if curl -sf --max-time 10 http://localhost:8080/api/products/ > /dev/null 2>&1; then
            ok "Backend API"
        else
            err "Backend API"
            PASSED=false
        fi

        # Frontend
        if curl -sf --max-time 10 http://localhost:8080/ > /dev/null 2>&1; then
            ok "Frontend"
        else
            err "Frontend"
            PASSED=false
        fi

        if [ "$PASSED" = true ]; then
            return 0
        fi

        if [ "$i" -lt "$MAX_RETRIES" ]; then
            echo "Qayta urinish ${RETRY_INTERVAL}s..."
            sleep $RETRY_INTERVAL
        fi
    done

    err "Health check muvaffaqiyatsiz!"
    return 1
}

# ---- LOGS ----
cmd_logs() {
    cd "$PROJECT_DIR"
    docker compose -f "$COMPOSE_FILE" logs -f ${3:-}
}

# ---- STATUS ----
cmd_status() {
    cd "$PROJECT_DIR"
    docker compose -f "$COMPOSE_FILE" ps
}

# ---- HELP ----
cmd_help() {
    echo ""
    echo "Jewelry Shop Deploy Script"
    echo ""
    echo "Usage: ./scripts/deploy.sh <command> [environment]"
    echo ""
    echo "Commands:"
    echo "  setup                 Server tayyorlash (Docker, Nginx, keys)"
    echo "  deploy [env]          To'liq deploy (default: production)"
    echo "  ssl                   SSL sertifikat olish"
    echo "  backup [env]          Database backup"
    echo "  rollback [env]        Oxirgi backupdan tiklash"
    echo "  health [env]          Health check"
    echo "  logs [env] [service]  Loglarni ko'rish"
    echo "  status [env]          Containerlar holati"
    echo ""
    echo "Environments: production (default), staging"
    echo ""
    echo "Examples:"
    echo "  ./scripts/deploy.sh setup"
    echo "  ./scripts/deploy.sh deploy"
    echo "  ./scripts/deploy.sh deploy staging"
    echo "  ./scripts/deploy.sh logs production backend"
    echo "  ./scripts/deploy.sh backup"
    echo ""
}

# ---- Komanda tanlash ----
case "$COMMAND" in
    setup)    cmd_setup ;;
    deploy)   cmd_deploy ;;
    ssl)      cmd_ssl ;;
    backup)   cmd_backup ;;
    rollback) cmd_rollback ;;
    health)   cmd_health ;;
    logs)     cmd_logs ;;
    status)   cmd_status ;;
    help)     cmd_help ;;
    *)        err "Noma'lum komanda: $COMMAND"; cmd_help; exit 1 ;;
esac
