from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient

from apps.users.models import TelegramUser
from apps.products.models import Category, Product
from apps.orders.models import Order, OrderItem
from apps.delivery.models import Region, DeliveryZone


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = TelegramUser.objects.create(
            telegram_id=111222333, first_name="Test"
        )
        self.category = Category.objects.create(name="Uzuklar", slug="uzuklar")
        self.product = Product.objects.create(
            name="Oltin uzuk",
            price=Decimal("1500000"),
            category=self.category,
            product_type="skincare",
            volume="50 ml",
        )

    def test_create_order(self):
        order = Order.objects.create(user=self.user, phone="+998901234567")
        self.assertEqual(str(order), f"#{order.id} - Test")
        self.assertEqual(order.status, "pending")

    def test_order_item_subtotal(self):
        order = Order.objects.create(user=self.user, phone="+998901234567")
        item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            price=Decimal("1500000"),
        )
        self.assertEqual(item.subtotal, Decimal("3000000"))

    def test_calculate_total(self):
        order = Order.objects.create(user=self.user, phone="+998901234567")
        OrderItem.objects.create(
            order=order, product=self.product, quantity=2, price=Decimal("1500000")
        )
        order.calculate_total()
        self.assertEqual(order.total, Decimal("3000000"))

    def test_order_item_auto_price(self):
        order = Order.objects.create(user=self.user, phone="+998901234567")
        item = OrderItem(order=order, product=self.product, quantity=1)
        item.save()
        self.assertEqual(item.price, Decimal("1500000"))

    def test_payment_method_default(self):
        order = Order.objects.create(user=self.user, phone="+998901234567")
        self.assertEqual(order.payment_method, "cash")
        self.assertFalse(order.is_paid)

    def test_order_item_freezes_cost_price(self):
        """cost_price berilmasa, mahsulot tannarxidan avtomatik muzlatiladi."""
        self.product.cost_price = Decimal("900000")
        self.product.save()
        order = Order.objects.create(user=self.user, phone="+998901234567")
        item = OrderItem(order=order, product=self.product, quantity=1)
        item.save()
        self.assertEqual(item.cost_price, Decimal("900000"))

    def test_order_item_profit(self):
        """Foyda = (sotuv − tannarx) × miqdor."""
        order = Order.objects.create(user=self.user, phone="+998901234567")
        item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=3,
            price=Decimal("1500000"),
            cost_price=Decimal("1000000"),
        )
        self.assertEqual(item.profit, Decimal("1500000"))

    def test_cost_price_frozen_after_product_price_change(self):
        """Buyurtmadagi tannarx keyingi mahsulot narx o'zgarishidan ta'sirlanmaydi."""
        self.product.cost_price = Decimal("900000")
        self.product.save()
        order = Order.objects.create(user=self.user, phone="+998901234567")
        item = OrderItem.objects.create(
            order=order, product=self.product, quantity=1, price=Decimal("1500000"),
            cost_price=self.product.cost_price,
        )
        # Mahsulot tannarxi keyin o'zgaradi
        self.product.cost_price = Decimal("1200000")
        self.product.save()
        item.refresh_from_db()
        self.assertEqual(item.cost_price, Decimal("900000"))


class OrderAPITest(TestCase):
    """Order API testlari."""

    def setUp(self):
        self.client = APIClient()
        self.user = TelegramUser.objects.create(
            telegram_id=123456789, first_name="Test User"
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Uzuklar", slug="uzuklar")
        self.product = Product.objects.create(
            name="Oltin uzuk",
            price=Decimal("1500000"),
            category=self.category,
            product_type="skincare",
            volume="50 ml",
            in_stock=True,
        )

    def test_create_order(self):
        """DEBUG=True da mock user bilan buyurtma yaratish."""
        response = self.client.post(
            "/api/orders/",
            {
                "items": [{"product_id": self.product.id, "quantity": 1}],
                "phone": "+998901234567",
                "payment_method": "cash",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["phone"], "+998901234567")
        self.assertEqual(len(response.data["items"]), 1)

    def test_create_order_freezes_cost_price(self):
        """Buyurtma yaratilganda tannarx muzlatiladi."""
        self.product.cost_price = Decimal("1000000")
        self.product.save()
        response = self.client.post(
            "/api/orders/",
            {
                "items": [{"product_id": self.product.id, "quantity": 2}],
                "phone": "+998901234567",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        item = OrderItem.objects.get(order_id=response.data["id"])
        self.assertEqual(item.cost_price, Decimal("1000000"))
        self.assertEqual(item.profit, Decimal("1000000"))  # (1.5M − 1M) × 2

    def test_cost_price_not_exposed_in_api(self):
        """Mijozga tannarx API javobida ko'rinmasligi kerak."""
        self.product.cost_price = Decimal("1000000")
        self.product.save()
        response = self.client.post(
            "/api/orders/",
            {
                "items": [{"product_id": self.product.id, "quantity": 1}],
                "phone": "+998901234567",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertNotIn("cost_price", response.data["items"][0])
        self.assertNotIn("cost_price", response.data["items"][0].get("product", {}))

    def test_create_order_no_phone(self):
        response = self.client.post(
            "/api/orders/",
            {
                "items": [{"product_id": self.product.id, "quantity": 1}],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_list_orders(self):
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, 200)

    def test_create_order_invalid_phone(self):
        response = self.client.post(
            "/api/orders/",
            {
                "items": [{"product_id": self.product.id, "quantity": 1}],
                "phone": "123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_order_stock_out(self):
        self.product.in_stock = False
        self.product.save()
        response = self.client.post(
            "/api/orders/",
            {
                "items": [{"product_id": self.product.id, "quantity": 1}],
                "phone": "+998901234567",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("sotuvda yo'q", response.data["error"])

    def test_create_order_empty_items(self):
        response = self.client.post(
            "/api/orders/",
            {"items": [], "phone": "+998901234567"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_order_missing_product(self):
        response = self.client.post(
            "/api/orders/",
            {
                "items": [{"product_id": 99999, "quantity": 1}],
                "phone": "+998901234567",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_order_with_delivery_zone(self):
        region = Region.objects.create(name="Test viloyat")
        zone = DeliveryZone.objects.create(
            region=region,
            name="Test zona",
            fee=Decimal("50000"),
            free_threshold=Decimal("2000000"),
        )
        response = self.client.post(
            "/api/orders/",
            {
                "items": [{"product_id": self.product.id, "quantity": 1}],
                "phone": "+998901234567",
                "delivery_zone_id": zone.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Decimal(response.data["delivery_fee"]), Decimal("50000"))

    def test_create_order_free_delivery_over_threshold(self):
        region = Region.objects.create(name="Test viloyat")
        zone = DeliveryZone.objects.create(
            region=region,
            name="Test zona",
            fee=Decimal("50000"),
            free_threshold=Decimal("1000000"),
        )
        response = self.client.post(
            "/api/orders/",
            {
                "items": [{"product_id": self.product.id, "quantity": 1}],
                "phone": "+998901234567",
                "delivery_zone_id": zone.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Decimal(response.data["delivery_fee"]), Decimal("0"))

    def test_order_detail_only_own(self):
        """Foydalanuvchi faqat o'zinikini ko'ra oladi."""
        other_user = TelegramUser.objects.create(
            telegram_id=777, first_name="Other"
        )
        other_order = Order.objects.create(user=other_user, phone="+998900000000")
        response = self.client.get(f"/api/orders/{other_order.id}/")
        self.assertEqual(response.status_code, 404)
