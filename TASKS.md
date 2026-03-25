# Jewelry Shop — Launch Oldidagi Tasklar

## Yuqori muhimlik

- [x] **Bot placeholder'larni to'ldirish** — +998993323155, @Age_Of_AI, temirovv21@gmail.com bilan to'ldirildi
- [x] **backend/.env ni gitignore qilish** — allaqachon `.gitignore` da, repoda track qilinmagan
- [x] **`/placeholder.svg` qo'shish** — `frontend/public/placeholder.svg` yaratildi, barcha referenslar yangilandi

## O'rta muhimlik

- [ ] **Online to'lov integratsiyasi** — Payme/Click/Uzum API bilan to'lov qabul qilish (hozir faqat naqd va o'tkazma)
- [ ] **Buyurtma tafsilot sahifasi** — `/order/:id` route qo'shish (frontend), `getOrder(id)` API allaqachon tayyor
- [ ] **Narx filtr UI** — SearchPage ga min/max narx input qo'shish (backend `ProductFilter` allaqachon tayyor)

## Past muhimlik

- [ ] **Foydalanuvchi buyurtma bekor qilish** — buyurtma "pending" holatida bo'lsa bekor qilish tugmasi
- [ ] **Sevimlilar backend sync** — server tomonida saqlash (qurilma almashtirsa yo'qolmasligi uchun)
- [ ] **Mahsulot stock miqdori** — `in_stock` boolean → sonli `stock_quantity` (nechta qolganini ko'rsatish)
- [ ] **Mahsulot sharhlari/reytingi** — foydalanuvchilar baho va izoh qoldirishi
- [ ] **Ishlatilmagan kodni tozalash** — `getProductsByCategory` (products.ts), `console.error` (client.ts)
