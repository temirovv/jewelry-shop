.PHONY: help dev staging prod down build logs test lint migrate collectstatic shell backup clean

help: ## Barcha buyruqlar ro'yxati
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'

# === Muhitlar ===

dev: ## Development muhitni ishga tushirish
	docker compose up -d

staging: ## Staging muhitni ishga tushirish
	docker compose -f docker-compose.staging.yml up -d

prod: ## Production muhitni ishga tushirish
	docker compose -f docker-compose.prod.yml up -d

down: ## Barcha containerlarni to'xtatish
	docker compose down

# === Build ===

build: ## Containerlarni qayta build qilish
	docker compose build --no-cache

build-staging: ## Staging containerlarni build qilish
	docker compose -f docker-compose.staging.yml build --no-cache

build-prod: ## Production containerlarni build qilish
	docker compose -f docker-compose.prod.yml build --no-cache

# === Logs ===

logs: ## Container loglarini ko'rish
	docker compose logs -f

logs-backend: ## Backend loglarini ko'rish
	docker compose logs -f backend

logs-bot: ## Bot loglarini ko'rish
	docker compose logs -f bot

# === Test & Lint ===

test: ## Backend testlarni ishga tushirish
	cd backend && python manage.py test --verbosity=2

lint: ## Backend va frontend lint
	cd backend && ruff check . --exclude=migrations,__pycache__
	cd frontend && npm run lint

lint-fix: ## Backend lint xatolarini avtomatik tuzatish
	cd backend && ruff check . --fix --exclude=migrations,__pycache__

typecheck: ## Frontend TypeScript tekshiruvi
	cd frontend && npx tsc --noEmit

# === Database ===

migrate: ## Migratsiyalarni ishga tushirish
	docker compose exec backend python manage.py migrate

makemigrations: ## Yangi migratsiya yaratish
	docker compose exec backend python manage.py makemigrations

shell: ## Django shell ochish
	docker compose exec backend python manage.py shell

backup: ## Database backup yaratish
	@mkdir -p backups
	docker compose exec -T db pg_dump -U postgres jewelry_db > backups/backup-$$(date +%Y%m%d-%H%M%S).sql
	@echo "Backup yaratildi: backups/"

restore: ## Oxirgi backupdan tiklash (make restore FILE=backups/backup-xxx.sql)
	@if [ -z "$(FILE)" ]; then echo "Usage: make restore FILE=backups/backup-xxx.sql"; exit 1; fi
	cat $(FILE) | docker compose exec -T db psql -U postgres jewelry_db

# === Static ===

collectstatic: ## Static fayllarni yig'ish
	docker compose exec backend python manage.py collectstatic --noinput

# === Deploy ===

deploy-staging: ## Staging serverga deploy
	chmod +x scripts/deploy.sh
	./scripts/deploy.sh deploy staging

deploy-prod: ## Production serverga deploy
	chmod +x scripts/deploy.sh
	./scripts/deploy.sh deploy

healthcheck: ## Healthcheck ishga tushirish
	chmod +x scripts/deploy.sh
	./scripts/deploy.sh health $(ENV)

# === Cleanup ===

clean: ## Barcha containerlar va volumelarni o'chirish
	docker compose down -v
	docker image prune -f
