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

## 3-QADAM: Loyihani klonlash

```bash
sudo mkdir -p /var/www && cd /var/www
git clone https://github.com/YOUR_USERNAME/jewelry-shop.git
cd jewelry-shop
mkdir -p backups
```

---

## 4-QADAM: Frontend build

```bash
docker run --rm -v $(pwd)/frontend:/app -w /app \
  -e VITE_API_URL=https://luxgold.uz/api \
  node:20-alpine sh -c "npm ci && npm run build"
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
```

> SECRET_KEY: `python3 -c "import secrets; print(secrets.token_urlsafe(50))"`

---

## 6-QADAM: Docker nginx portini o'zgartirish

```bash
nano docker-compose.prod.yml
```

Nginx bo'limida portni o'zgartiring:
- `"80:80"` → `"8080:80"`
- `"443:443"` qatorini o'chiring

---

## 7-QADAM: Containerlarni ishga tushirish

```bash
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml ps
```

Tekshirish: `curl http://localhost:8080/api/products/`

---

## 8-QADAM: Superuser yaratish

```bash
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

---

## 9-QADAM: SSL sertifikat olish

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

## 10-QADAM: Nginx HTTPS config

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

## 11-QADAM: Tekshirish

| URL | Natija |
|-----|--------|
| https://luxgold.uz | Frontend |
| https://luxgold.uz/api/products/ | API |
| https://luxgold.uz/admin/ | Admin |

---

## 12-QADAM: Telegram Bot

1. @BotFather → `/mybots` → bot tanlash
2. `Bot Settings` → `Menu Button` → `Configure menu button`
3. URL: `https://luxgold.uz`, Text: `Do'kon`

---

## 13-QADAM: GitHub Secrets (CI/CD)

Serverda:
```bash
ssh-keygen -t ed25519 -C "github-actions" -f ~/.ssh/github_deploy -N ""
cat ~/.ssh/github_deploy.pub >> ~/.ssh/authorized_keys
cat ~/.ssh/github_deploy   # GitHub Secret ga nusxalang
```

GitHub → Settings → Secrets → Actions:

| Secret | Qiymat |
|--------|--------|
| `PROD_SSH_HOST` | Server IP |
| `PROD_SSH_USER` | root |
| `PROD_SSH_KEY` | Private key |
| `PROD_PROJECT_PATH` | /var/www/jewelry-shop |
| `TELEGRAM_DEPLOY_BOT_TOKEN` | Bot token |
| `TELEGRAM_DEPLOY_CHAT_ID` | Telegram ID |

---

## Foydali buyruqlar

```bash
cd /var/www/jewelry-shop

docker compose -f docker-compose.prod.yml logs -f backend     # Loglar
docker compose -f docker-compose.prod.yml up -d --build        # Qayta build
docker compose -f docker-compose.prod.yml exec -T db \
  pg_dump -U postgres jewelry_db > backups/backup-$(date +%Y%m%d-%H%M%S).sql
sudo certbot renew --dry-run                                    # SSL tekshirish
```
