# Ziyora — Kontent to'ldirish ro'yxati

Platformani real mijozlar uchun to'ldirish bo'yicha ish ro'yxati.
Admin panel: `https://ziyora.uz/admin/`

---

## 0. Avval qaror qilinadigan
- [ ] Nechta **brend** bilan boshlaymiz (5–10 tavsiya)
- [ ] Nechta **mahsulot** (minimal 15–20 ta ochilish uchun)
- [ ] **Ustama (margin)** siyosati — tannarx ustiga necha %
- [ ] Mahsulot **rasmlari** manbasi (o'zingiz suratga olasizmi / brenddan)

## 1. Kategoriyalar (poydevor — birinchi kiritiladi)
Admin → Kategoriyalar. Har biriga: nom + emoji ikonka.
- [ ] Teri parvarishi 🧴
- [ ] Makiyaj 💄
- [ ] Parfyumeriya 🌸
- [ ] Soch parvarishi 💇‍♀️
- [ ] Tana parvarishi 🧼

## 2. Brendlar
Admin → Brendlar. Har biriga:
- [ ] Nomi
- [ ] Logo (kvadrat, PNG/SVG)
- [ ] Ishlab chiqaruvchi davlat
- [ ] Qisqa tavsif
- [ ] `is_featured` (bosh sahifada ko'rsatiladimi)

## 3. Mahsulotlar ⭐ (asosiy ish)
Har bir mahsulot uchun yig'iladigan ma'lumot:
- [ ] Nomi
- [ ] Tavsif (2–4 gap)
- [ ] Sotuv narxi
- [ ] **Tannarx (cost_price)** — ⚠️ foyda hisoboti uchun majburiy
- [ ] Eski narx (chegirma bo'lsa)
- [ ] Brend + Kategoriya
- [ ] Turi: `skincare` / `makeup` / `perfume` / `haircare` / `bodycare`
- [ ] Teri turi: `all` / `dry` / `oily` / `combination` / `normal` / `sensitive`
- [ ] Hajmi (masalan 50 ml)
- [ ] Rang/ton (makiyaj uchun, masalan "Nude 02")
- [ ] Tarkibi (asosiy ingredientlar)
- [ ] Yaroqlilik muddati (oy)
- [ ] Ishlab chiqarilgan davlat
- [ ] `in_stock`, `is_featured`

> 💡 Ko'p mahsulot bo'lsa — `docs/product-import-shablon.csv` ni to'ldirib,
> admin → Mahsulotlar → **Import** orqali bir vaqtda yuklang (bittalab emas).
> Import ustunlari va ruxsat etilgan qiymatlar shablon ichida izohlangan.

## 4. Mahsulot rasmlari
> ⚠️ Rasmlar CSV import orqali yuklanmaydi — admin panelда qo'lda qo'shiladi.
- [ ] Har mahsulotga kamida 1 ta, yaxshisi 3–5 ta rasm
- [ ] Bittasi **asosiy** (`is_main`)
- [ ] Bir xil uslub (fon, yorug'lik), kvadrat nisbat

## 5. Bannerlar (bosh sahifa carousel)
- [ ] 2–4 ta banner: sarlavha, matn, emoji/rasm, gradient, link

## 6. Yetkazib berish (tekshirish — seed data bor)
- [ ] 14 viloyat + 40+ zona narxlarini tekshiring/to'g'rilang
- [ ] Bepul yetkazish chegarasi (hozir 500 000 so'm) to'g'rimi
- [ ] Standart narx (hozir 30 000 so'm) to'g'rimi

## 7. Aloqa/ma'lumot (tekshirish)
- [ ] Bot aloqa: telefon, Telegram, ish vaqti (`bot/handlers/callbacks.py`)

---

## 🎯 Minimal ochilish chegarasi
4–5 kategoriya · 3–5 brend · **15–20 mahsulot** (rasm + tannarx) · 1–2 banner · yetkazish tasdiqlangan
