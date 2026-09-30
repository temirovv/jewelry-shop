from decimal import Decimal
from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework.throttling import SimpleRateThrottle

from apps.orders.models import Order, OrderItem
from apps.orders.utils import send_order_notification
from apps.products.models import Category, Product
from apps.users.models import TelegramUser


class OrderSecurityTestBase(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.user = TelegramUser.objects.create(telegram_id=555, first_name="Test")
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Kategoriya", slug="kat")
        self.product = Product.objects.create(
            name="Dolce & Gabbana <Light Blue>",
            price=Decimal("100000"),
            category=self.category,
        )

    def tearDown(self):
        cache.clear()

    def _order(self, **overrides):
        payload = {
            "items": [{"product_id": self.product.id, "quantity": 1}],
            "phone": "+998901234567",
            "payment_method": "cash",
            **overrides,
        }
        return self.client.post("/api/orders/", payload, format="json")


@patch("apps.orders.views.send_order_notification")
class OrderInputValidationTest(OrderSecurityTestBase):
    def test_non_integer_product_id_is_400(self, _notify):
        response = self._order(items=[{"product_id": "abc", "quantity": 1}])
        self.assertEqual(response.status_code, 400)

    def test_long_size_is_400(self, _notify):
        response = self._order(
            items=[{"product_id": self.product.id, "quantity": 1, "size": "x" * 51}]
        )
        self.assertEqual(response.status_code, 400)

    def test_null_size_accepted(self, _notify):
        response = self._order(
            items=[{"product_id": self.product.id, "quantity": 1, "size": None}]
        )
        self.assertEqual(response.status_code, 201)

    def test_too_many_items_is_400(self, _notify):
        items = [{"product_id": self.product.id, "quantity": 1}] * 51
        self.assertEqual(self._order(items=items).status_code, 400)


# THROTTLE_RATES klass atributi import paytida settings'dan olinadi,
# shuning uchun override_settings emas, lug'atning o'zini vaqtincha o'zgartiramiz
@override_settings(
    CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
)
@patch.dict(SimpleRateThrottle.THROTTLE_RATES, {"orders": "2/hour"})
@patch("apps.orders.views.send_order_notification")
class OrderThrottleTest(OrderSecurityTestBase):
    def test_order_creation_is_throttled(self, _notify):
        self.assertEqual(self._order().status_code, 201)
        self.assertEqual(self._order().status_code, 201)
        self.assertEqual(self._order().status_code, 429)

    def test_order_list_not_throttled_by_orders_scope(self, _notify):
        self._order()
        self._order()
        for _ in range(3):
            self.assertEqual(self.client.get("/api/orders/").status_code, 200)


@override_settings(BOT_TOKEN="token", ADMIN_IDS=[1])
class OrderNotificationEscapeTest(OrderSecurityTestBase):
    def test_user_input_is_html_escaped(self):
        self.user.first_name = "<b>Hacker</b>"
        self.user.save()
        order = Order.objects.create(
            user=self.user,
            phone="+998<9>",
            delivery_address="Toshkent & <i>",
            comment='<a href="https://evil.example">Tasdiqlash</a> <3',
        )
        OrderItem.objects.create(order=order, product=self.product, quantity=1)

        with patch("apps.orders.utils._send_telegram_message") as send:
            send_order_notification(order)

        message = send.call_args.args[2]
        self.assertNotIn("<a href", message)
        self.assertNotIn("<b>Hacker", message)
        self.assertIn("&lt;3", message)
        self.assertIn("Dolce &amp; Gabbana &lt;Light Blue&gt;", message)
        self.assertIn("Toshkent &amp; &lt;i&gt;", message)
        # Bizning o'z formatlashimiz saqlanib qoladi
        self.assertIn("<b>Mijoz:</b>", message)


class InputValidationTest(OrderSecurityTestBase):
    def test_cart_long_size_is_400(self):
        response = self.client.post(
            "/api/cart/add/",
            {"product_id": self.product.id, "quantity": 1, "size": "x" * 51},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_cart_quantity_capped_at_99(self):
        for _ in range(3):
            self.client.post(
                "/api/cart/add/",
                {"product_id": self.product.id, "quantity": 50},
                format="json",
            )
        response = self.client.get("/api/cart/")
        self.assertEqual(response.data["items"][0]["quantity"], 99)

    def test_favorite_toggle_non_integer_is_400(self):
        response = self.client.post(
            "/api/users/favorites/toggle/", {"product_id": "abc"}, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_zones_non_integer_region_is_empty(self):
        response = self.client.get("/api/delivery/zones/?region=abc")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])
