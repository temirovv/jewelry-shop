# 📡 API Documentation

## Base URL

```
Development: http://localhost:8000/api
Production: https://your-domain.com/api
```

## Authentication

Barcha so'rovlar Telegram WebApp `initData` orqali autentifikatsiya qilinadi.

```http
X-Telegram-Init-Data: query_id=AAHdF6IQAAAAAN0XohBzYOWP&user=%7B%22id%22%3A...
```

---

## Products API

### Get Categories

Kategoriyalar ro'yxati

```http
GET /categories/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Uzuklar",
    "slug": "rings",
    "icon": "💍",
    "image": null
  }
]
```

### Get Products

Mahsulotlar ro'yxati (pagination bilan)

```http
GET /products/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| category | string | Kategoriya slug |
| metal_type | string | gold, silver, platinum, white_gold |
| min_price | number | Minimal narx |
| max_price | number | Maksimal narx |
| is_featured | boolean | Featured mahsulotlar |
| in_stock | boolean | Sotuvda bor |
| search | string | Qidiruv |
| ordering | string | price, -price, created_at |
| page | number | Sahifa raqami |

**Response:**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Oltin uzuk 585",
      "price": 2500000,
      "old_price": 3000000,
      "images": [
        {
          "id": 1,
          "image": "/media/products/ring-1.jpg",
          "is_main": true
        }
      ],
      "category": {
        "id": 1,
        "name": "Uzuklar",
        "slug": "rings"
      },
      "metal_type": "gold",
      "weight": 3.5,
      "in_stock": true,
      "is_featured": true,
      "discount_percent": 17
    }
  ]
}
```

### Get Single Product

```http
GET /products/{id}/
```

**Response:**
```json
{
  "id": 1,
  "name": "Oltin uzuk 585",
  "description": "Klassik dizayn...",
  "price": 2500000,
  "old_price": 3000000,
  "images": [...],
  "category": {...},
  "metal_type": "gold",
  "weight": 3.5,
  "size": "17",
  "proba": "585",
  "in_stock": true,
  "is_featured": true,
  "discount_percent": 17,
  "created_at": "2024-01-01T12:00:00Z"
}
```

### Get Featured Products

```http
GET /products/featured/
```

---

## Cart API

### Get Cart

```http
GET /cart/
```

**Response:**
```json
{
  "id": 1,
  "items": [
    {
      "id": 1,
      "product": {...},
      "quantity": 2,
      "size": "17",
      "subtotal": 5000000
    }
  ],
  "total": 5000000,
  "items_count": 2
}
```

### Add to Cart

```http
POST /cart/add/
```

**Request Body:**
```json
{
  "product_id": 1,
  "quantity": 1,
  "size": "17"
}
```

### Update Cart Item

```http
PATCH /cart/items/{item_id}/
```

**Request Body:**
```json
{
  "quantity": 3
}
```

### Remove from Cart

```http
DELETE /cart/items/{item_id}/remove/
```

### Clear Cart

```http
DELETE /cart/clear/
```

---

## Orders API

### Get Orders

```http
GET /orders/
```

**Response:**
```json
[
  {
    "id": 1,
    "status": "pending",
    "status_display": "Kutilmoqda",
    "total": 5000000,
    "phone": "+998901234567",
    "delivery_address": "Toshkent sh...",
    "items": [...],
    "created_at": "2024-01-01T12:00:00Z"
  }
]
```

### Create Order

```http
POST /orders/
```

**Request Body:**
```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "size": "17"
    }
  ],
  "phone": "+998901234567",
  "delivery_address": "Toshkent sh...",
  "comment": "Iltimos, ertalab yetkazing"
}
```

### Get Single Order

```http
GET /orders/{id}/
```

---

## Error Responses

**400 Bad Request:**
```json
{
  "error": "Xato ma'lumot"
}
```

**401 Unauthorized:**
```json
{
  "error": "Avtorizatsiya talab qilinadi"
}
```

**404 Not Found:**
```json
{
  "error": "Topilmadi"
}
```
