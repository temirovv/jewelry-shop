# Jewelry Shop — Ishlar ro'yxati

**Joriy holat:** ~82% tayyor → **Maqsad:** 100% production-ready
**To'lov integratsiyasi oxirgi bosqichda** — avval core funksionallik yakunlansin.

---

## ✅ BAJARILGAN

### 1. Admin Panel
- [x] Banner admin — rasm preview, gradient preview, link, tabbed fieldsets
- [x] Sidebar — Bannerlar bo'limi, Dashboard link
- [x] Dashboard statistika — buyurtmalar, daromad, foydalanuvchilar, top mahsulotlar
- [x] Order admin — cancel action, manzil, items_count, notification
- [x] Product admin — duplicate, stock toggle, featured toggle, metall label
- [x] Category admin — mahsulotlar sonini ko'rsatish
- [x] Users admin — buyurtmalar soni, jami xarid summasi, actions
- [x] Cart admin — tozalash, bo'sh savatlar, subtotal, holat badge
- [x] Import/Export (django-import-export + Unfold)
- [x] Order tabs — jarayonda va bekor qilingan

### 2. Cart Backend Sinxronizatsiyasi
- [x] Cart API client (lib/api/cart.ts)
- [x] cartStore backend sinx, offline fallback, buyurtmadan keyin tozalash

### 3. Inventar Boshqaruvi
- [x] Buyurtma yaratilganda stock tekshiruvi
- [x] main_image model bug tuzatildi

### 4. Profil sahifasi
- [x] "Profil ma'lumotlari" va "Yordam" accordion'lari

### 5. Telegram Bot
- [x] /start, /help, /orders komandalar
- [x] Callback handlers — my_orders, contact, help, back_to_main, language
- [x] Buyurtma holati o'zgarganda notification (admin action'lardan ham)

### 6. Testlar — 40 test, barchasi passed
- [x] Products (5+8), Orders (5+3), Users (5+1), Cart (4+5)

### 7. Production Deploy
- [x] .env.example, docker-compose.prod.yml, nginx config

### 8. Kod sifati
- [x] Bo'sh catch bloklari, main_image bug, DRY refactor

---

## 🔴 PRIORITET 1: Core funksionallikni yakunlash

### 1.1. Delivery app integratsiyasi ✅
- [x] `Region` + `DeliveryZone` modellari + `Order.delivery_zone` FK
- [x] Region/zona bo'yicha delivery fee hisoblash (`calculate_fee()`)
- [x] Admin panelda regions + zones CRUD (Unfold + sidebar)
- [x] Checkout'ga region/tuman dropdown + fee preview
- [x] `GET /api/delivery/regions/` va `/zones/?region=X` endpointlari
- [x] Seed data: 14 region, 40+ zona (butun O'zbekiston)
- [x] `image_url` pre-existing migration/model mismatch tuzatildi
- [x] 40 test o'tdi, frontend lint toza

### 1.2. Favorites backend sinxronizatsiyasi ✅
- [x] `Favorite` model (user + product, unique_together) + migration
- [x] `FavoriteViewSet` — list / toggle / clear
- [x] Admin panel: Favorites CRUD + sidebar menu
- [x] Frontend `favoritesStore` — optimistic toggle + rollback + merge sync
- [x] App yuklanganda `syncFavorites()` — lokal + server birlashtiriladi
- [x] 6 ta favorite test qo'shildi (46/46 passed)

### 1.3. OrderViewSet to'liq tekshiruv ✅
- [x] Telefon validation (9–12 raqam)
- [x] `delivery_address` va `comment` uchun 500 belgilik cheklov
- [x] `Product.DoesNotExist` va `DeliveryZone.DoesNotExist` xatolarini to'g'ri qaytarish
- [x] Edge case testlar: invalid phone, stock out, empty items, missing product, zone fee, free delivery threshold, detail isolation
- [x] 53/53 test passed (+7 yangi)

---

## 🟡 PRIORITET 2: Frontend UX

### 2.1. Image gallery (ProductDetail)
- [ ] Embla Carousel yoki Swiper — swipe gallery
- [ ] Thumbnail navigation + active indicator
- [ ] Full-screen zoom modal
- [ ] Pinch-to-zoom (mobile)

### 2.2. i18n (uz / ru)
- [ ] `react-i18next` o'rnatish va konfiguratsiya
- [ ] `uz.json` va `ru.json` resource fayllari
- [ ] Hardcoded matnlarni `t()` ga o'tkazish
- [ ] User tilini Telegram `language_code`'dan olish
- [ ] Profile'da til almashtirish switcher

### 2.3. Profile to'ldirish
- [ ] Buyurtmalar tarixi tablar bilan (active / completed / cancelled)
- [ ] Shaxsiy ma'lumotlarni tahrirlash (telefon, default address)

---

## 🟢 PRIORITET 3: Production hardening

### 3.1. Logging va monitoring
- [ ] Sentry backend + frontend integratsiyasi
- [ ] Django logging konfiguratsiyasi
- [ ] React Error Boundary
- [ ] Healthcheck endpoint (`/api/health/`)

### 3.2. Performance
- [ ] N+1 query audit (django-silk / debug toolbar)
- [ ] Frontend bundle analiz (rollup-visualizer)
- [ ] PWA service worker (offline cache)
- [ ] Media CDN (Cloudflare yoki S3)

### 3.3. Security
- [ ] Production CORS/CSRF domain'lari
- [ ] Rate limiting (nginx level)
- [ ] SECRET_KEY rotation strategy

---

## 🟣 PRIORITET 4: TO'LOV INTEGRATSIYASI (ENG OXIRIDA)

### 4.1. Setup
- [ ] Provider tanlash: **Click** / **Payme** / **Octo** (O'zbekiston)
- [ ] Merchant account va test credentials
- [ ] `payments` app yaratish

### 4.2. Backend
- [ ] `Payment` model (order, amount, provider, transaction_id, status, timestamps)
- [ ] Provider client: `ClickClient`, `PaymeClient` (abstract base)
- [ ] `POST /api/payments/init/` — to'lov tashabbusi
- [ ] `POST /api/payments/webhook/{provider}/` — callback handler
- [ ] HMAC / signature verification
- [ ] `Order.is_paid` avtomatik yangilash signal orqali

### 4.3. Frontend
- [ ] Checkout'da payment method UI (Click / Payme / Naqd)
- [ ] Telegram WebApp `openLink` bilan redirect
- [ ] Payment status polling (yoki webhook push)
- [ ] Success / failure sahifalari + haptic feedback

### 4.4. Testing
- [ ] Sandbox muhitda to'liq oqim
- [ ] Edge case'lar: timeout, bekor qilish, double payment
- [ ] Refund oqimi (agar kerak bo'lsa)

---

## 📅 Taxminiy jadval

| Bosqich | Vazifalar | Kun |
|---------|-----------|-----|
| 1 | Delivery + Favorites + Order audit | 1–2 |
| 2 | Image gallery + i18n + Profile | 1–2 |
| 3 | Sentry + performance + security | 1 |
| 4 | **To'lov integratsiyasi** | 2–3 |

**Jami:** ~5–8 ish kuni 100% production-ready holatga.

---

## Boshlanish nuqtasi

**Keyingi qadam:** Prioritet 1.1 — Delivery app integratsiyasi.
