import hashlib
import hmac
import json
import time
from urllib.parse import urlencode

from django.test import RequestFactory, TestCase, override_settings

from apps.users.authentication import TelegramAuthentication
from apps.users.models import TelegramUser

BOT_TOKEN = "123456:TEST-token"


def make_init_data(user_id=42, auth_date=None, include_auth_date=True):
    """Telegram imzolagandek initData yasash."""
    fields = {"user": json.dumps({"id": user_id, "first_name": "Ali"})}
    if include_auth_date:
        fields["auth_date"] = str(auth_date or int(time.time()))
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(fields.items()))
    secret = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    fields["hash"] = hmac.new(
        secret, data_check_string.encode(), hashlib.sha256
    ).hexdigest()
    return urlencode(fields)


@override_settings(DEBUG=False, TELEGRAM_BOT_TOKEN=BOT_TOKEN, BOT_TOKEN=BOT_TOKEN)
class TelegramAuthenticationTest(TestCase):
    def setUp(self):
        self.auth = TelegramAuthentication()
        self.factory = RequestFactory()

    def _authenticate(self, **headers):
        return self.auth.authenticate(self.factory.get("/", headers=headers))

    def test_valid_init_data(self):
        result = self._authenticate(X_Telegram_Init_Data=make_init_data())
        self.assertIsNotNone(result)
        self.assertEqual(result[0].telegram_id, 42)

    def test_missing_auth_date_rejected(self):
        init_data = make_init_data(include_auth_date=False)
        self.assertIsNone(self._authenticate(X_Telegram_Init_Data=init_data))

    def test_expired_auth_date_rejected(self):
        init_data = make_init_data(auth_date=int(time.time()) - 2 * 86400)
        self.assertIsNone(self._authenticate(X_Telegram_Init_Data=init_data))

    def test_tampered_hash_rejected(self):
        init_data = make_init_data().replace("Ali", "Vali")
        self.assertIsNone(self._authenticate(X_Telegram_Init_Data=init_data))

    def test_blocked_user_is_anonymous(self):
        TelegramUser.objects.create(telegram_id=42, first_name="Ali", is_active=False)
        self.assertIsNone(self._authenticate(X_Telegram_Init_Data=make_init_data()))

    def test_no_header_is_anonymous_without_debug(self):
        self.assertIsNone(self._authenticate())

    def test_bot_token_auth(self):
        TelegramUser.objects.create(telegram_id=42, first_name="Ali")
        result = self._authenticate(X_Bot_Token=BOT_TOKEN, X_Telegram_User_Id="42")
        self.assertEqual(result[0].telegram_id, 42)

    def test_bot_token_wrong_rejected(self):
        TelegramUser.objects.create(telegram_id=42, first_name="Ali")
        result = self._authenticate(X_Bot_Token="wrong", X_Telegram_User_Id="42")
        self.assertIsNone(result)

    def test_bot_token_blocked_user_rejected(self):
        TelegramUser.objects.create(telegram_id=42, first_name="Ali", is_active=False)
        result = self._authenticate(X_Bot_Token=BOT_TOKEN, X_Telegram_User_Id="42")
        self.assertIsNone(result)

    @override_settings(BOT_TOKEN="")
    def test_empty_bot_token_setting_rejects_everything(self):
        TelegramUser.objects.create(telegram_id=42, first_name="Ali")
        result = self._authenticate(X_Bot_Token="x", X_Telegram_User_Id="42")
        self.assertIsNone(result)
