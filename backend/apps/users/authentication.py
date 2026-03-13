import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl

from django.conf import settings
from rest_framework.authentication import BaseAuthentication

from .models import TelegramUser

# auth_date expiry: 24 hours
AUTH_DATE_MAX_AGE = 86400


class TelegramAuthentication(BaseAuthentication):
    """Telegram WebApp initData orqali autentifikatsiya"""

    def authenticate(self, request):
        # Bot uchun alohida auth (X-Bot-Token header)
        bot_user = self._authenticate_bot(request)
        if bot_user is not None:
            return bot_user

        init_data = request.headers.get("X-Telegram-Init-Data")

        # Development uchun mock user (DEBUG=True va header yo'q bo'lsa)
        if not init_data and settings.DEBUG:
            user, _ = TelegramUser.objects.get_or_create(
                telegram_id=123456789,
                defaults={
                    "first_name": "Test",
                    "last_name": "User",
                    "username": "testuser",
                },
            )
            return (user, None)

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

    def _authenticate_bot(self, request):
        """Bot API so'rovlarini X-Bot-Token header orqali autentifikatsiya"""
        bot_token = request.headers.get("X-Bot-Token")
        telegram_user_id = request.headers.get("X-Telegram-User-Id")

        if not bot_token or not telegram_user_id:
            return None

        # Bot token ni tekshirish
        if bot_token != settings.BOT_TOKEN:
            return None

        try:
            user = TelegramUser.objects.get(telegram_id=int(telegram_user_id))
            return (user, None)
        except (TelegramUser.DoesNotExist, ValueError):
            return None

    def validate_init_data(self, init_data: str) -> bool:
        """Telegram imzosini tekshirish"""
        if not settings.TELEGRAM_BOT_TOKEN:
            return False

        try:
            parsed = dict(parse_qsl(init_data))
            hash_value = parsed.pop("hash", None)
            if not hash_value:
                return False

            # auth_date expiry tekshiruvi
            auth_date_str = parsed.get("auth_date")
            if auth_date_str:
                try:
                    auth_date = int(auth_date_str)
                    if time.time() - auth_date > AUTH_DATE_MAX_AGE:
                        return False
                except (ValueError, TypeError):
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
