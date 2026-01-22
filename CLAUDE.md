# Loyiha Konteksti: Jewelry Marketplace WebApp (Premium UI)

## 1. Loyiha haqida
**Tavsif:** Telegram WebApp orqali ishlaydigan, premium dizaynga ega zargarlik buyumlari do‘koni.
**Maqsad:** O‘rikzor narxlarini "Brand" darajasidagi qadoq va vizual ko‘rinishda taqdim etish.

## 2. Texnologik Stack (UPDATED)
**Backend (API & Logic):**
- **Core:** Python 3.12, Django 5.x, DRF.
- **DB:** PostgreSQL 16.
- **Bot:** Aiogram 3.x.

**Frontend (High-End UI):**
- **Framework:** **React 18** (Vite orqali qurilgan).
- **Language:** **TypeScript** (Majburiy).
- **Styling:** **Tailwind CSS** (Tezkor dizayn uchun).
- **UI Library:** **Shadcn/UI** (Hozirgi trenddagi eng chiroyli va minimalist komponentlar).
- **Animations:** **Framer Motion** (Sahifalar o‘rtasida silliq o‘tish va "micro-interactions" uchun).
- **State Management:** **Zustand** (Redux'dan yengilroq).
- **Icons:** Lucide React.
- **Integration:** `@twa-dev/sdk` (Telegram WebApp SDK bilan ishlash uchun).

## 3. Loyiha Arxitekturasi (Monorepo)
```text
root/
├── backend/            # Django (DRF + Admin)
├── bot/                # Aiogram service
├── frontend/           # React + Vite (SPA)
│   ├── src/
│   │   ├── components/ # Shadcn UI komponentlari (Button, Card, Sheet)
│   │   ├── pages/      # Home, ProductDetail, Cart, Checkout
│   │   ├── lib/        # Utils va API client (Axios)
│   │   └── hooks/      # Custom hooks (useTelegram, useCart)
│   └── public/
├── docker-compose.yml
└── CLAUDE.md
```

## 4. Kod Standartlari

**Umumiy qoidalar:**
- Barcha kod **TypeScript** da yoziladi (strict mode).
- Har bir komponent alohida papkada: `ComponentName/index.tsx`, `ComponentName.types.ts`.
- API so'rovlar faqat `lib/api/` ichida bo'ladi.
- Console.log production'da ishlatilmaydi.

**Naming Conventions:**
- Komponentlar: `PascalCase` (ProductCard, CartSheet).
- Funksiyalar/hooks: `camelCase` (useCart, fetchProducts).
- Fayllar: `kebab-case` yoki `PascalCase` komponentlar uchun.
- CSS klasslar: Tailwind utilities (custom CSS minimal).

**Commit formati:** Conventional Commits
```
feat: yangi mahsulot kartasi komponenti
fix: cart hisoblash xatosi tuzatildi
refactor: API client qayta yozildi
```

## 5. Muhim Buyruqlar

```bash
# Frontend
cd frontend && npm run dev      # Development server
cd frontend && npm run build    # Production build
cd frontend && npm run lint     # ESLint tekshiruvi

# Backend
cd backend && python manage.py runserver
cd backend && python manage.py migrate

# Docker
docker-compose up -d            # Barcha servislarni ishga tushirish
```

## 6. API Endpoints (Asosiy)

```
GET    /api/products/          # Mahsulotlar ro'yxati
GET    /api/products/{id}/     # Bitta mahsulot
POST   /api/cart/              # Savatga qo'shish
GET    /api/cart/              # Savat ko'rish
POST   /api/orders/            # Buyurtma yaratish
```

## 7. Telegram WebApp Integratsiya

- `window.Telegram.WebApp` orqali kirish.
- `useTelegram` hook orqali user ma'lumotlari.
- MainButton va BackButton boshqaruvi.
- Theme colors Telegram'dan olinadi.

## 8. Men (Claude) uchun qoidalar

- Har doim TypeScript ishlatsin.
- Shadcn/UI komponentlaridan foydalansin.
- Tailwind CSS bilan styling qilsin.
- Framer Motion bilan animatsiyalar.
- Kichik, qayta ishlatiladigan komponentlar yaratsin.
- Xatoliklarni try-catch bilan ushlasin.
- Loading va error holatlarini ko'rsatsin.
- Mobile-first yondashuv.
- Telegram WebApp UX qoidalariga rioya qilsin.