import hashlib
import hmac
import json
from urllib.parse import parse_qsl

from django.conf import settings
from rest_framework.authentication import BaseAuthentication

from .models import TelegramUser


class TelegramAuthentication(BaseAuthentication):
    """Telegram WebApp initData orqali autentifikatsiya"""

    def authenticate(self, request):
        init_data = request.headers.get("X-Telegram-Init-Data")
        if not init_data:
            return None

        if not self.validate_init_data(init_data):
            return None

        user_data = self.parse_user_data(init_data)
        if not user_data:
            return None

        user, _ = TelegramUser.objects.update_or_create(
            telegram_id=user_data["id"],
            defaults={
                "first_name": user_data.get("first_name", ""),
                "last_name": user_data.get("last_name", ""),
                "username": user_data.get("username", ""),
            },
        )

        return (user, None)

    def validate_init_data(self, init_data: str) -> bool:
        """Telegram imzosini tekshirish"""
        if not settings.TELEGRAM_BOT_TOKEN:
            return True  # Development uchun

        try:
            parsed = dict(parse_qsl(init_data))
            hash_value = parsed.pop("hash", None)
            if not hash_value:
                return False

            data_check_string = "\n".join(
                f"{k}={v}" for k, v in sorted(parsed.items())
            )

            secret_key = hmac.new(
                b"WebAppData",
                settings.TELEGRAM_BOT_TOKEN.encode(),
                hashlib.sha256,
            ).digest()

            calculated_hash = hmac.new(
                secret_key,
                data_check_string.encode(),
                hashlib.sha256,
            ).hexdigest()

            return calculated_hash == hash_value
        except Exception:
            return False

    def parse_user_data(self, init_data: str) -> dict | None:
        """initData dan user ma'lumotlarini olish"""
        try:
            parsed = dict(parse_qsl(init_data))
            user_json = parsed.get("user")
            if user_json:
                return json.loads(user_json)
        except Exception:
            pass
        return None
