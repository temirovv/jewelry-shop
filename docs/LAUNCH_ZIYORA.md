# Ziyora — Launch Runbook (ziyora.uz)

MVP launch: buyurtmalar ilova orqali qabul qilinadi, telefon orqali tasdiqlanadi va
yetkaziladi. To'lov: **naqd / karta o'tkazma** (online to'lov keyingi bosqichda).

Deploy avtomatik: `main` branchga push → GitHub Actions CD → VPS'da `scripts/deploy.sh deploy`.

---

## 0. Repo tomonida bajarilgan (kod)

- [x] Domen konfiguratsiyasi `ziyora.uz` ga o'tkazildi (`.env.example`, `deploy.sh`, bot, docs)
- [x] `cost_price` (tannarx) — Product + OrderItem muzlatish + admin foyda ustuni
- [x] Eski jewelry test bug (`weight`) va lint tozalandi — 62 test OK

---

## 1. DNS (bir marta)

`ziyora.uz` domen A-record'ini VPS IP manziliga yo'naltiring:

```
A    ziyora.uz        → <VPS_IP>
A    www.ziyora.uz    → <VPS_IP>
```

Tekshirish: `ping ziyora.uz` → VPS IP chiqishi kerak.

---

## 2. Server `.env` (VPS'da, `<PROJECT_PATH>/.env`)

`.env.example` dan nusxa oling va real qiymatlarni to'ldiring:

```env
SECRET_KEY=<kuchli-tasodifiy-kalit>
DEBUG=False
ALLOWED_HOSTS=ziyora.uz,www.ziyora.uz
DOMAIN=ziyora.uz

DB_NAME=ziyora_db
DB_USER=postgres
DB_PASSWORD=<kuchli-parol>
DB_HOST=db
DB_PORT=5432

# @ziyorauz_bot tokeni (BotFather'dan)
TELEGRAM_BOT_TOKEN=<bot-token>
BOT_TOKEN=<bot-token>
ADMIN_IDS=<sizning-telegram-id>
WEBAPP_URL=https://ziyora.uz

CORS_ALLOWED_ORIGINS=https://ziyora.uz,https://www.ziyora.uz
CSRF_TRUSTED_ORIGINS=https://ziyora.uz,https://www.ziyora.uz
VITE_API_URL=https://ziyora.uz/api
VITE_BOT_USERNAME=ziyorauz_bot
API_BASE_URL=http://backend:8000/api

# Superuser (admin panel)
DJANGO_SUPERUSER_USERNAME=<admin-login>
DJANGO_SUPERUSER_PASSWORD=<admin-parol>
DJANGO_SUPERUSER_EMAIL=temirovv21@gmail.com
```

> `SECRET_KEY` generatsiya: `python -c "import secrets; print(secrets.token_urlsafe(50))"`

---

## 3. Toza boshlash — eski jewelry ma'lumotlarini o'chirish (VPS'da)

Seed data **umuman ishlatilmaydi**. Eski jewelry DB volume'ini tozalab, toza `ziyora_db` yaratiladi:

```bash
cd <PROJECT_PATH>
docker compose -f docker-compose.prod.yml down -v   # volume'lar bilan o'chirish
```

> `-v` postgres volume'ini ham o'chiradi → keyingi deploy'da toza `ziyora_db` yaratiladi,
> migratsiyalar ishlaydi, superuser yaratiladi. Katalog bo'sh bo'ladi (faqat admin panel).

---

## 4. Deploy — `main` ga merge

Lokalda (yoki PR orqali):

```bash
git checkout main
git merge feature/cosmetics-marketplace
git push origin main
```

Push → CI (lint + 62 test) → o'tsa CD avtomatik VPS'ga deploy qiladi.
Telegram'ga deploy natijasi (OK/XATO) xabari keladi.

---

## 5. SSL sertifikat (bir marta, VPS'da)

DNS ishlagach:

```bash
cd <PROJECT_PATH>
./scripts/deploy.sh ssl
```

Let's Encrypt sertifikat oladi va host-nginx HTTPS config'ini yozadi (301 redirect http→https).

---

## 6. BotFather sozlash (@ziyorauz_bot)

`@BotFather` da:
- `/setmenubutton` → botni tanlang → URL: `https://ziyora.uz` → tugma matni: `Do'kon`
- (ixtiyoriy) `/setdomain` → `ziyora.uz` (Login Widget uchun)
- Bot rasmi, nomi, tavsifini Ziyora brendiga moslang

---

## 7. Kontent kiritish (admin panel)

`https://ziyora.uz/admin/` → superuser bilan kiring:

1. **Brendlar** — nom, logo, davlat, `is_featured`
2. **Kategoriyalar** — nom, icon (emoji)
3. **Mahsulotlar** — nom, narx, **tannarx (cost_price)**, brend, kategoriya, tur, rasmlar
   - ⚠️ Tannarxni to'ldiring — birinchi buyurtmadan foyda hisobi yig'iladi
4. **Bannerlar** — bosh sahifa carousel
5. **Yetkazish** — Regionlar + zonalar + narxlar
6. **Bannerlar/mahsulotlarni** `is_active` = ✓

---

## 8. Smoke test (launch tekshiruvi)

- [ ] `https://ziyora.uz` ochiladi (HTTPS, yashil qulf)
- [ ] Telegram'da `@ziyorauz_bot` → Menu tugma → WebApp ochiladi
- [ ] Mahsulot ko'rinadi, savatga qo'shiladi
- [ ] Test buyurtma → admin panelda ko'rinadi + botga xabar keladi
- [ ] Buyurtma statusini o'zgartirish → mijozga Telegram xabar
- [ ] Admin: mahsulot foyda ustuni to'g'ri (`sotuv − tannarx`)
- [ ] Admin → **Moliyaviy hisobot** (`/admin/hisobot/`) ochiladi, Excel yuklab olinadi

---

## Keyingi bosqichlar (launch'dan keyin)

- Online to'lov — Payme (YaTT/MChJ + sandbox integratsiya)
- Moliyaviy hisobotni kengaytirish: **soliq foizi** (rejim aniqlangach) + **xarajat jurnali**
  (reklama, kuryer, Payme komissiyasi) → sof foyda. Asosiy hisobot sahifasi tayyor (`/admin/hisobot/`).
- i18n (uz/ru)
