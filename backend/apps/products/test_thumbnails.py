import io
import shutil
import tempfile
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image
from rest_framework.test import APIClient

from apps.products.models import Category, Product, ProductImage
from apps.products import thumbnails
from apps.products.thumbnails import THUMB_WIDTH, get_thumbnail_url

TEST_MEDIA_ROOT = tempfile.mkdtemp(prefix="ziyora-test-thumbs-")


def upload(name="pic.jpg", size=(2000, 1500), mode="RGB", fmt="JPEG", exif=None):
    buf = io.BytesIO()
    img = Image.new(mode, size, "red" if mode == "RGB" else (255, 0, 0, 0))
    img.save(buf, format=fmt, **({"exif": exif} if exif else {}))
    return SimpleUploadedFile(name, buf.getvalue())


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ThumbnailTest(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        category = Category.objects.create(name="Parfyum", slug="parfyum")
        self.product = Product.objects.create(
            name="Light Blue", price=Decimal("1"), category=category
        )

    def _image(self, **kwargs):
        return ProductImage.objects.create(product=self.product, image=upload(**kwargs))

    def _open(self, url):
        return Image.open(Path(TEST_MEDIA_ROOT) / url.removeprefix("/media/"))

    def test_resized_webp_keeps_aspect_ratio(self):
        url = get_thumbnail_url(self._image().image, THUMB_WIDTH)
        self.assertTrue(url.endswith(".webp"))
        with self._open(url) as thumb:
            self.assertEqual(thumb.format, "WEBP")
            self.assertEqual(thumb.size, (400, 300))

    def test_small_image_not_upscaled(self):
        url = get_thumbnail_url(self._image(size=(120, 80)).image, THUMB_WIDTH)
        with self._open(url) as thumb:
            self.assertEqual(thumb.size, (120, 80))

    def test_transparency_kept(self):
        image = self._image(name="cut.png", mode="RGBA", fmt="PNG")
        with self._open(get_thumbnail_url(image.image, THUMB_WIDTH)) as thumb:
            self.assertEqual(thumb.mode, "RGBA")

    def test_exif_orientation_applied(self):
        exif = Image.Exif()
        exif[0x0112] = 6  # 90° burilgan — telefon rasmlari
        image = self._image(size=(2000, 1000), exif=exif)
        with self._open(get_thumbnail_url(image.image, THUMB_WIDTH)) as thumb:
            self.assertEqual(thumb.size, (400, 800))

    def test_generated_once(self):
        image = self._image()
        with patch.object(thumbnails, "_render", wraps=thumbnails._render) as render:
            get_thumbnail_url(image.image, THUMB_WIDTH)
            get_thumbnail_url(image.image, THUMB_WIDTH)
        self.assertEqual(render.call_count, 1)

    def test_broken_file_returns_none(self):
        image = ProductImage.objects.create(
            product=self.product, image=SimpleUploadedFile("bad.jpg", b"not an image")
        )
        with self.assertLogs("apps.products.thumbnails", level="ERROR"):
            self.assertIsNone(get_thumbnail_url(image.image, THUMB_WIDTH))

    def test_api_returns_thumbnail_and_large(self):
        self._image()
        response = APIClient().get(f"/api/products/{self.product.slug}/")
        img = response.data["images"][0]
        self.assertTrue(img["thumbnail"].startswith("http://testserver/media/thumbs/400/"))
        self.assertTrue(img["large"].startswith("http://testserver/media/thumbs/1080/"))
        self.assertTrue(img["image"].endswith(".jpg"))
