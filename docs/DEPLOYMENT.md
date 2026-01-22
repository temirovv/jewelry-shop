# 🚀 Deployment Guide

## Production Deployment

### 1. Server talablari

- Ubuntu 22.04+ yoki boshqa Linux
- Docker & Docker Compose
- Nginx (reverse proxy uchun)
- SSL sertifikat (Let's Encrypt)
- Domain nomi

### 2. Domain sozlash

```bash
# A record
your-domain.com -> SERVER_IP
api.your-domain.com -> SERVER_IP
```

### 3. Server tayyorlash

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin

# Install Nginx
sudo apt install nginx certbot python3-certbot-nginx
```

### 4. SSL sertifikat olish

```bash
sudo certbot --nginx -d your-domain.com -d api.your-domain.com
```

### 5. Nginx konfiguratsiya

```nginx
# /etc/nginx/sites-available/jewelry

# Frontend
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Backend API
server {
    listen 443 ssl http2;
    server_name api.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /var/www/jewelry/staticfiles/;
    }

    location /media/ {
        alias /var/www/jewelry/media/;
    }
}

# HTTP -> HTTPS redirect
server {
    listen 80;
    server_name your-domain.com api.your-domain.com;
    return 301 https://$host$request_uri;
}
```

### 6. Environment fayllar

```bash
# .env (root directory)
BOT_TOKEN=your-bot-token
WEBAPP_URL=https://your-domain.com
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=api.your-domain.com
CORS_ALLOWED_ORIGINS=https://your-domain.com
```

### 7. Deploy

```bash
# Clone project
git clone https://github.com/your-username/jewelry-shop.git
cd jewelry-shop

# Start services
docker-compose -f docker-compose.yml up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 8. Database migration

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

---

## Telegram Bot sozlash

### 1. BotFather orqali

1. @BotFather ga `/newbot` yuboring
2. Bot nomini kiriting
3. Bot username kiriting
4. TOKEN oling

### 2. WebApp sozlash

1. @BotFather ga `/mybots` yuboring
2. Botingizni tanlang
3. `Bot Settings` -> `Menu Button` -> `Configure menu button`
4. WebApp URL kiriting: `https://your-domain.com`

### 3. Bot tokenni .env ga qo'shing

```bash
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

---

## Monitoring

### Docker logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f bot
```

### Health check

```bash
# Backend
curl https://api.your-domain.com/api/categories/

# Frontend
curl https://your-domain.com
```

---

## Backup

### Database backup

```bash
docker-compose exec db pg_dump -U postgres jewelry_db > backup.sql
```

### Media backup

```bash
tar -czvf media_backup.tar.gz ./backend/media
```

### Restore

```bash
cat backup.sql | docker-compose exec -T db psql -U postgres jewelry_db
```

---

## CI/CD (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /var/www/jewelry-shop
            git pull origin main
            docker-compose up -d --build
```
