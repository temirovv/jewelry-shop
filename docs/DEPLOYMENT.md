# Deploy Guide — luxgold.uz

## 1-QADAM: Server tayyorlash

```bash
sudo apt update && sudo apt upgrade -y

# Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh && rm get-docker.sh
sudo usermod -aG docker $USER

# Docker Compose, Nginx, Certbot, Git
sudo apt install -y docker-compose-plugin nginx certbot python3-certbot-nginx git

# Firewall
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

> `usermod` dan keyin `exit` qilib qayta SSH kiring.

---

## 2-QADAM: DNS sozlash

Domen provayderingiz panelida:

```
A    luxgold.uz        → SERVER_IP
A    www.luxgold.uz    → SERVER_IP
```

Tekshirish: `ping luxgold.uz`

---

## 3-QADAM: Deploy key yaratish (Private repo uchun)

Repo private bo'lgani uchun serverda SSH deploy key yaratish kerak:

```bash
ssh-keygen -t ed25519 -C "deploy-key" -f ~/.ssh/deploy_key -N ""
cat ~/.ssh/deploy_key.pub
```

GitHub'da: **Repo** → **Settings** → **Deploy keys** → **Add deploy key**
- Title: `Production Server`
- Key: yuqoridagi `cat` natijasini paste qiling
- "Allow write access" ni **belgilamang** (faqat o'qish kerak)

Tekshirish:

```bash
GIT_SSH_COMMAND="ssh -i ~/.ssh/deploy_key -o StrictHostKeyChecking=no" \
  git ls-remote git@github.com:temirovv/jewelry-shop.git
```

---

## 4-QADAM: Loyihani klonlash

```bash
sudo mkdir -p /var/www && cd /var/www

GIT_SSH_COMMAND="ssh -i ~/.ssh/deploy_key -o StrictHostKeyChecking=no" \
  git clone git@github.com:temirovv/jewelry-shop.git

cd jewelry-shop
mkdir -p backups

# Git'ga deploy key ni doimo ishlatishni sozlash
git config core.sshCommand "ssh -i ~/.ssh/deploy_key -o StrictHostKeyChecking=no"
```

---

## 5-QADAM: .env fayl yaratish

```bash
nano .env
```

```env
SECRET_KEY=juda-uzun-murakkab-kalit
DEBUG=False
ALLOWED_HOSTS=luxgold.uz,www.luxgold.uz

DB_NAME=jewelry_db
DB_USER=postgres
DB_PASSWORD=KuChLi_PaRoL_123!
DB_HOST=db
DB_PORT=5432

TELEGRAM_BOT_TOKEN=your-bot-token
BOT_TOKEN=your-bot-token
ADMIN_IDS=your_telegram_id
WEBAPP_URL=https://luxgold.uz

CORS_ALLOWED_ORIGINS=https://luxgold.uz,https://www.luxgold.uz
API_BASE_URL=http://backend:8000/api

VITE_API_URL=https://luxgold.uz/api
```

> SECRET_KEY: `python3 -c "import secrets; print(secrets.token_urlsafe(50))"`

---

## 6-QADAM: Containerlarni ishga tushirish

Frontend build avtomatik — `docker compose up` o'zi `npm ci && npm run build` qiladi:

```bash
cd /var/www/jewelry-shop
docker compose -f docker-compose.prod.yml up -d --build
```

5 ta container: `db`, `backend`, `frontend` (build qilib chiqadi), `bot`, `nginx`

Tekshirish:

```bash
docker compose -f docker-compose.prod.yml ps
curl http://localhost:8080/api/products/
curl http://localhost:8080/
```

---

## 7-QADAM: Superuser yaratish

```bash
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

---

## 8-QADAM: SSL sertifikat olish

```bash
sudo rm -f /etc/nginx/sites-enabled/default

sudo tee /etc/nginx/sites-available/luxgold > /dev/null <<'EOF'
server {
    listen 80;
    server_name luxgold.uz www.luxgold.uz;
    location / { proxy_pass http://127.0.0.1:8080; }
}
EOF

sudo ln -sf /etc/nginx/sites-available/luxgold /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

sudo certbot --nginx -d luxgold.uz -d www.luxgold.uz
```

---

## 9-QADAM: Nginx HTTPS config

```bash
sudo nano /etc/nginx/sites-available/luxgold
```

```nginx
server {
    listen 80;
    server_name luxgold.uz www.luxgold.uz;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name luxgold.uz www.luxgold.uz;

    ssl_certificate /etc/letsencrypt/live/luxgold.uz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/luxgold.uz/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo nginx -t && sudo systemctl restart nginx
```

---

## 10-QADAM: Tekshirish

Brauzerda:
- https://luxgold.uz — Frontend
- https://luxgold.uz/api/products/ — API
- https://luxgold.uz/admin/ — Admin panel

---

## 11-QADAM: Telegram Bot sozlash

1. @BotFather → `/mybots` → bot tanlash
2. `Bot Settings` → `Menu Button` → `Configure menu button`
3. URL: `https://luxgold.uz`, Text: `Do'kon`

---

## 12-QADAM: GitHub Secrets (CI/CD avtomatik deploy)

### A) Serverda GitHub Actions uchun SSH key

```bash
ssh-keygen -t ed25519 -C "github-actions" -f ~/.ssh/github_actions -N ""
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys
cat ~/.ssh/github_actions   # GitHub Secret ga nusxalang
```

### B) GitHub → Settings → Secrets → Actions

| Secret                       | Qiymat                          |
|------------------------------|---------------------------------|
| `PROD_SSH_HOST`              | Server IP manzili               |
| `PROD_SSH_USER`              | root (yoki deploy user)         |
| `PROD_SSH_KEY`               | `~/.ssh/github_actions` private |
| `PROD_PROJECT_PATH`          | `/var/www/jewelry-shop`         |
| `TELEGRAM_DEPLOY_BOT_TOKEN`  | Bot token                       |
| `TELEGRAM_DEPLOY_CHAT_ID`    | Sizning Telegram ID             |

### Natija:
- `main` ga push → avtomatik production deploy
- `develop` ga push → avtomatik staging deploy
- Har bir deploy Telegram'ga xabar yuboradi

---

## Foydali buyruqlar

```bash
cd /var/www/jewelry-shop

# Qo'lda deploy
chmod +x scripts/deploy.sh
./scripts/deploy.sh production

# Loglar
docker compose -f docker-compose.prod.yml logs -f backend

# Database backup
docker compose -f docker-compose.prod.yml exec -T db \
  pg_dump -U postgres jewelry_db > backups/backup-$(date +%Y%m%d-%H%M%S).sql

# SSL tekshirish
sudo certbot renew --dry-run
```
