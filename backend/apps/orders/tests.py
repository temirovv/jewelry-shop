from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient

from apps.users.models import TelegramUser
from apps.products.models import Category, Product
from apps.orders.models import Order, OrderItem


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
            metal_type="gold",
            weight=Decimal("5.50"),
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
            metal_type="gold",
            weight=Decimal("5.50"),
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
