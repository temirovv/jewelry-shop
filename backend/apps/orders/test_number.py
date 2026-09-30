import re
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from apps.orders.models import Order
from apps.products.models import Category, Product
from apps.users.models import TelegramUser

NUMBER_RE = re.compile(r"^ZY-[23456789ABCDEFGHJKLMNPQRSTUVWXYZ]{6}$")


class OrderNumberTest(TestCase):
    def setUp(self):
        self.user = TelegramUser.objects.create(telegram_id=1, first_name="Ali")

    def test_number_generated(self):
        order = Order.objects.create(user=self.user, phone="+998901234567")
        self.assertRegex(order.number, NUMBER_RE)

    def test_number_stable_on_save(self):
        order = Order.objects.create(user=self.user, phone="+998901234567")
        number = order.number
        order.status = "confirmed"
        order.save(update_fields=["status"])
        order.refresh_from_db()
        self.assertEqual(order.number, number)

    def test_collision_retried(self):
        Order.objects.create(user=self.user, phone="1", number="ZY-AAAAAA")
        with patch(
            "apps.orders.models.generate_order_number",
            side_effect=["ZY-AAAAAA", "ZY-BBBBBB"],
        ):
            order = Order.objects.create(user=self.user, phone="2")
        self.assertEqual(order.number, "ZY-BBBBBB")


@patch("apps.orders.views.send_order_notification")
class OrderNumberAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = TelegramUser.objects.create(telegram_id=1, first_name="Ali")
        self.client.force_authenticate(user=self.user)
        category = Category.objects.create(name="Parfyum", slug="parfyum")
        self.product = Product.objects.create(
            name="Light Blue", price=Decimal("100000"), category=category
        )

    def test_response_has_number_not_id(self, _notify):
        response = self.client.post(
            "/api/orders/",
            {
                "items": [{"product_id": self.product.id, "quantity": 1}],
                "phone": "+998901234567",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertRegex(response.data["number"], NUMBER_RE)
        self.assertNotIn("id", response.data)

    def test_detail_by_number(self, _notify):
        order = Order.objects.create(user=self.user, phone="+998901234567")
        response = self.client.get(f"/api/orders/{order.number}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["number"], order.number)

    def test_detail_by_internal_id_not_found(self, _notify):
        order = Order.objects.create(user=self.user, phone="+998901234567")
        self.assertEqual(self.client.get(f"/api/orders/{order.id}/").status_code, 404)
