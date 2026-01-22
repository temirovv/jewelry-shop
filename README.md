# 💎 Jewelry Shop - Telegram WebApp

Premium zargarlik buyumlari do'koni - Telegram WebApp platformasida.

![Jewelry Shop Banner](docs/banner.png)

## 📋 Loyiha haqida

**Jewelry Shop** - bu Telegram WebApp orqali ishlaydigan zamonaviy e-commerce platforma. Foydalanuvchilar to'g'ridan-to'g'ri Telegram ichida zargarlik buyumlarini ko'rishlari, savatga qo'shishlari va buyurtma berishlari mumkin.

### ✨ Xususiyatlar

- 🛍️ **Premium UI** - Shadcn/UI va Framer Motion bilan chiroyli dizayn
- 📱 **Telegram WebApp** - To'liq Telegram integratsiyasi
- 🔐 **Xavfsiz autentifikatsiya** - Telegram initData orqali
- 🛒 **Savat tizimi** - Real-time yangilanish
- 📦 **Buyurtma boshqaruvi** - Status tracking
- 🌙 **Dark/Light mode** - Telegram temasiga moslanadi
- 🚀 **Docker ready** - Oson deployment

## 🏗️ Arxitektura

```
jewelry-shop/
├── frontend/          # React + Vite + TypeScript
│   ├── src/
│   │   ├── components/   # UI komponentlar
│   │   ├── pages/        # Sahifalar
│   │   ├── hooks/        # Custom hooks
│   │   ├── stores/       # Zustand stores
│   │   ├── lib/          # Utils va API
│   │   └── types/        # TypeScript types
│   └── ...
├── backend/           # Django + DRF
│   ├── apps/
│   │   ├── users/        # Telegram foydalanuvchilar
│   │   ├── products/     # Mahsulotlar
│   │   ├── orders/       # Buyurtmalar
│   │   └── cart/         # Savat
│   └── config/           # Django settings
├── bot/               # Aiogram 3.x
│   ├── handlers/         # Message handlers
│   ├── keyboards/        # Inline keyboards
│   └── ...
└── docker-compose.yml
```

## 🛠️ Texnologiyalar

### Frontend
| Texnologiya | Versiya | Maqsad |
|-------------|---------|--------|
| React | 18.x | UI Framework |
| TypeScript | 5.x | Type safety |
| Vite | 5.x | Build tool |
| Tailwind CSS | 3.x | Styling |
| Shadcn/UI | latest | UI Components |
| Framer Motion | 11.x | Animations |
| Zustand | 4.x | State management |
| @twa-dev/sdk | latest | Telegram WebApp |

### Backend
| Texnologiya | Versiya | Maqsad |
|-------------|---------|--------|
| Python | 3.12 | Runtime |
| Django | 5.x | Web framework |
| DRF | 3.14+ | REST API |
| PostgreSQL | 16 | Database |

### Bot
| Texnologiya | Versiya | Maqsad |
|-------------|---------|--------|
| Aiogram | 3.x | Telegram Bot API |

## 🚀 Ishga tushirish

### Talablar

- Node.js 20+
- Python 3.12+
- PostgreSQL 16+
- Docker & Docker Compose (ixtiyoriy)

### 1. Loyihani klonlash

```bash
git clone https://github.com/your-username/jewelry-shop.git
cd jewelry-shop
```

### 2. Environment sozlash

```bash
# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.example frontend/.env

# Bot
cp bot/.env.example bot/.env
```

### 3. Development rejimida ishga tushirish

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

#### Bot
```bash
cd bot
pip install -r requirements.txt
python main.py
```

### 4. Docker bilan ishga tushirish

```bash
docker-compose up -d
```

## 📡 API Endpoints

### Products
```
GET    /api/categories/           # Kategoriyalar
GET    /api/products/             # Mahsulotlar
GET    /api/products/{id}/        # Bitta mahsulot
GET    /api/products/featured/    # Featured mahsulotlar
```

### Cart
```
GET    /api/cart/                 # Savatni ko'rish
POST   /api/cart/add/             # Savatga qo'shish
PATCH  /api/cart/items/{id}/      # Miqdorni yangilash
DELETE /api/cart/items/{id}/remove/  # O'chirish
DELETE /api/cart/clear/           # Tozalash
```

### Orders
```
GET    /api/orders/               # Buyurtmalar ro'yxati
POST   /api/orders/               # Yangi buyurtma
GET    /api/orders/{id}/          # Bitta buyurtma
```

## 🔐 Telegram Autentifikatsiya

Backend Telegram WebApp `initData` orqali foydalanuvchini aniqlaydi:

```python
# Request header
X-Telegram-Init-Data: <initData string>
```

## 📱 Screenshots

<p float="left">
  <img src="docs/screenshot-1.png" width="200" />
  <img src="docs/screenshot-2.png" width="200" />
  <img src="docs/screenshot-3.png" width="200" />
</p>

## 📝 License

MIT License - batafsil [LICENSE](LICENSE) faylida.

## 👨‍💻 Muallif

Loyiha Claude Code yordamida yaratildi.

---

<p align="center">
  Made with ❤️ for Jewelry lovers
</p>
