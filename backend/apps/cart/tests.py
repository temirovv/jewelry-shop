from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient

from apps.users.models import TelegramUser
from apps.products.models import Category, Product
from apps.cart.models import Cart, CartItem


class CartModelTest(TestCase):
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

    def test_cart_create(self):
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(str(cart), "Savat - Test")
        self.assertEqual(cart.total, 0)
        self.assertEqual(cart.items_count, 0)

    def test_cart_item_subtotal(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=3)
        self.assertEqual(item.subtotal, Decimal("4500000"))

    def test_cart_total(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        self.assertEqual(cart.total, Decimal("3000000"))

    def test_cart_items_count(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=5)
        self.assertEqual(cart.items_count, 5)


class CartAPITest(TestCase):
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

    def test_get_cart(self):
        response = self.client.get("/api/cart/")
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart(self):
        response = self.client.post(
            "/api/cart/add/",
            {"product_id": self.product.id, "quantity": 2},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data["items"]), 1)

    def test_add_duplicate_increases_quantity(self):
        self.client.post(
            "/api/cart/add/",
            {"product_id": self.product.id, "quantity": 1},
            format="json",
        )
        self.client.post(
            "/api/cart/add/",
            {"product_id": self.product.id, "quantity": 2},
            format="json",
        )
        response = self.client.get("/api/cart/")
        self.assertEqual(response.data["items"][0]["quantity"], 3)

    def test_clear_cart(self):
        self.client.post(
            "/api/cart/add/",
            {"product_id": self.product.id, "quantity": 1},
            format="json",
        )
        response = self.client.delete("/api/cart/clear/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["items"]), 0)

    def test_add_out_of_stock(self):
        self.product.in_stock = False
        self.product.save()
        response = self.client.post(
            "/api/cart/add/",
            {"product_id": self.product.id, "quantity": 1},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
