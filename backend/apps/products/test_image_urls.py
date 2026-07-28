"""Rasm URL'lari reverse proxy ortida ham to'g'ri sxema bilan qurilishi kerak.

Production'da nginx TLS'ni tugatadi va Django'ga `X-Forwarded-Proto: https`
yuboradi. Agar SECURE_PROXY_SSL_HEADER sozlanmagan bo'lsa, Django so'rovni
HTTP deb hisoblaydi va `build_absolute_uri()` `http://` URL yasaydi — HTTPS
sahifada bunday rasm mixed content sifatida bloklanadi.
"""

import io
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image
from rest_framework.test import APIClient

from apps.products.models import Category, Product, ProductImage
from apps.users.models import TelegramUser

# Test yuklamalari haqiqiy MEDIA_ROOT ga tushib qolmasligi uchun
TEST_MEDIA_ROOT = tempfile.mkdtemp(prefix="ziyora-test-media-")


def make_image(name="pic.jpg"):
    buf = io.BytesIO()
    Image.new("RGB", (10, 10), "red").save(buf, format="JPEG")
    buf.seek(0)
    return SimpleUploadedFile(name, buf.read(), content_type="image/jpeg")


class MediaTempMixin:
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ImageUrlSchemeTest(MediaTempMixin, TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Makiyaj", image=make_image("cat.jpg"))
        self.product = Product.objects.create(
            name="Rasmli mahsulot", price=100000, category=self.category
        )
        ProductImage.objects.create(product=self.product, image=make_image(), is_main=True)

    def test_product_image_url_is_https_behind_proxy(self):
        response = self.client.get("/api/products/", HTTP_X_FORWARDED_PROTO="https")
        image_url = response.data["results"][0]["images"][0]["image"]
        self.assertTrue(
            image_url.startswith("https://"),
            f"Proxy ortida rasm URL'i https bo'lishi kerak, keldi: {image_url}",
        )

    def test_category_image_url_is_https_behind_proxy(self):
        response = self.client.get("/api/categories/", HTTP_X_FORWARDED_PROTO="https")
        image_url = response.data[0]["image"]
        self.assertTrue(
            image_url.startswith("https://"),
            f"Proxy ortida kategoriya rasmi https bo'lishi kerak, keldi: {image_url}",
        )

    def test_plain_http_request_still_returns_http(self):
        """Proxy header'siz (lokal dev) URL http bo'lib qolishi kerak."""
        response = self.client.get("/api/products/")
        image_url = response.data["results"][0]["images"][0]["image"]
        self.assertTrue(image_url.startswith("http://"))


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class OrderCreateImageUrlTest(MediaTempMixin, TestCase):
    """Buyurtma yaratish javobi ham to'liq (absolyut) rasm URL'i qaytarishi kerak."""

    def setUp(self):
        self.client = APIClient()
        self.user = TelegramUser.objects.create(telegram_id=555002, first_name="Test")
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Makiyaj")
        self.product = Product.objects.create(
            name="Rasmli mahsulot", price=100000, category=self.category
        )
        ProductImage.objects.create(product=self.product, image=make_image(), is_main=True)

    def test_create_order_response_has_absolute_image_url(self):
        response = self.client.post(
            "/api/orders/",
            {
                "items": [{"product_id": self.product.id, "quantity": 1}],
                "phone": "998901234567",
                "delivery_address": "Toshkent",
                "payment_method": "cash",
            },
            format="json",
            HTTP_X_FORWARDED_PROTO="https",
        )
        self.assertEqual(response.status_code, 201)
        image_url = response.data["items"][0]["product"]["images"][0]["image"]
        self.assertTrue(
            image_url.startswith("https://"),
            f"Buyurtma yaratish javobida absolyut https URL kutilgan, keldi: {image_url}",
        )
