from django.test import TestCase
from rest_framework.test import APIClient

from apps.users.models import TelegramUser


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
