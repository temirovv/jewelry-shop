from django.test import TestCase
from rest_framework.test import APIClient

from apps.users.models import TelegramUser, Favorite
from apps.products.models import Category, Product


class TelegramUserModelTest(TestCase):
    def test_create_user(self):
        user = TelegramUser.objects.create(
            telegram_id=123456789,
            first_name="John",
            last_name="Doe",
            username="johndoe",
        )
        self.assertEqual(str(user), "John (123456789)")

    def test_full_name(self):
        user = TelegramUser.objects.create(
            telegram_id=111, first_name="Ali", last_name="Valiyev"
        )
        self.assertEqual(user.full_name, "Ali Valiyev")

    def test_full_name_no_last(self):
        user = TelegramUser.objects.create(telegram_id=222, first_name="Ali")
        self.assertEqual(user.full_name, "Ali")

    def test_default_language(self):
        user = TelegramUser.objects.create(telegram_id=333, first_name="Test")
        self.assertEqual(user.language, "uz")

    def test_is_active_default(self):
        user = TelegramUser.objects.create(telegram_id=444, first_name="Test")
        self.assertTrue(user.is_active)


class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = TelegramUser.objects.create(
            telegram_id=123456789, first_name="Test User"
        )
        self.client.force_authenticate(user=self.user)

    def test_get_current_user(self):
        response = self.client.get("/api/users/me/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "Test User")


class FavoriteTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = TelegramUser.objects.create(
            telegram_id=987654321, first_name="Fav User"
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Uzuklar", slug="uzuklar")
        self.product = Product.objects.create(
            name="Oltin uzuk",
            price=1000000,
            weight=3.5,
            category=self.category,
        )

    def test_favorite_unique(self):
        Favorite.objects.create(user=self.user, product=self.product)
        with self.assertRaises(Exception):
            Favorite.objects.create(user=self.user, product=self.product)

    def test_list_empty(self):
        response = self.client.get("/api/users/favorites/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_toggle_add(self):
        response = self.client.post(
            "/api/users/favorites/toggle/",
            {"product_id": self.product.id},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["is_favorite"])
        self.assertEqual(Favorite.objects.filter(user=self.user).count(), 1)

    def test_toggle_remove(self):
        Favorite.objects.create(user=self.user, product=self.product)
        response = self.client.post(
            "/api/users/favorites/toggle/",
            {"product_id": self.product.id},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["is_favorite"])
        self.assertEqual(Favorite.objects.filter(user=self.user).count(), 0)

    def test_toggle_invalid_product(self):
        response = self.client.post(
            "/api/users/favorites/toggle/",
            {"product_id": 99999},
            format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_clear(self):
        Favorite.objects.create(user=self.user, product=self.product)
        response = self.client.delete("/api/users/favorites/clear/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Favorite.objects.filter(user=self.user).count(), 0)
