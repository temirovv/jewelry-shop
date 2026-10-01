from django.contrib.auth.models import User
from django.test import TestCase, override_settings

HOST_NGINX = "172.18.0.1"  # docker nginx ko'radigan host nginx manzili
DOCKER_NGINX = "172.18.0.3"  # gunicorn ko'radigan REMOTE_ADDR


def chain(client_ip, spoofed=()):
    """Prod'dagi X-Forwarded-For: [mijoz yuborgan soxta qiymatlar], mijoz, host nginx."""
    return ", ".join([*spoofed, client_ip, HOST_NGINX])


@override_settings(AXES_ENABLED=True, AXES_FAILURE_LIMIT=3)
class AdminLoginLockoutTest(TestCase):
    def setUp(self):
        User.objects.create_superuser("boss", "b@b.uz", "togri-parol-123")

    def _login(self, password, xff):
        return self.client.post(
            "/admin/login/?next=/admin/",
            {"username": "boss", "password": password},
            HTTP_X_FORWARDED_FOR=xff,
            REMOTE_ADDR=DOCKER_NGINX,
        )

    def _fail(self, times, xff):
        for _ in range(times):
            self._login("xato", xff)

    def test_locked_after_limit_even_with_correct_password(self):
        self._fail(3, chain("203.0.113.7"))
        response = self._login("togri-parol-123", chain("203.0.113.7"))
        self.assertEqual(response.status_code, 429)
        self.assertContains(response, "bloklandi", status_code=429)

    def test_other_client_not_affected(self):
        # Hammasi bir xil REMOTE_ADDR'dan keladi — blok IP bo'yicha ajralishi shart
        self._fail(3, chain("203.0.113.7"))
        response = self._login("togri-parol-123", chain("198.51.100.9"))
        self.assertEqual(response.status_code, 302)

    def test_spoofed_forwarded_for_does_not_bypass(self):
        for i in range(3):
            self._login("xato", chain("203.0.113.7", spoofed=[f"6.6.6.{i}"]))
        response = self._login(
            "togri-parol-123", chain("203.0.113.7", spoofed=["9.9.9.9", "8.8.8.8"])
        )
        self.assertEqual(response.status_code, 429)

    def test_success_resets_counter(self):
        self._fail(2, chain("203.0.113.7"))
        self.assertEqual(self._login("togri-parol-123", chain("203.0.113.7")).status_code, 302)
        self.client.logout()
        self._fail(2, chain("203.0.113.7"))
        self.assertEqual(self._login("togri-parol-123", chain("203.0.113.7")).status_code, 302)
