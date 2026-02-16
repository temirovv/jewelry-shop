from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient

from apps.products.models import Category, Product, ProductImage, Banner


class CategoryModelTest(TestCase):
    def test_slug_auto_generated(self):
        cat = Category.objects.create(name="Uzuklar")
        self.assertEqual(cat.slug, "uzuklar")

    def test_str(self):
        cat = Category.objects.create(name="Marjonlar")
        self.assertEqual(str(cat), "Marjonlar")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Uzuklar", slug="uzuklar")
        self.product = Product.objects.create(
            name="Oltin uzuk",
            price=Decimal("1500000"),
            old_price=Decimal("2000000"),
            category=self.category,
            metal_type="gold",
            weight=Decimal("5.50"),
        )

    def test_str(self):
        self.assertEqual(str(self.product), "Oltin uzuk")

    def test_discount_percent(self):
        self.assertEqual(self.product.discount_percent, 25)

    def test_discount_percent_no_old_price(self):
        self.product.old_price = None
        self.product.save()
        self.assertEqual(self.product.discount_percent, 0)

    def test_main_image_none(self):
        self.assertIsNone(self.product.main_image)

    def test_main_image_with_url_only(self):
        """image_url bor, image yo'q — image_url qaytarishi kerak."""
        ProductImage.objects.create(
            product=self.product,
            image_url="https://example.com/img.jpg",
            is_main=True,
        )
        self.assertEqual(self.product.main_image, "https://example.com/img.jpg")


class BannerModelTest(TestCase):
    def test_str(self):
        banner = Banner.objects.create(title="Yangi kolleksiya")
        self.assertEqual(str(banner), "Yangi kolleksiya")

    def test_default_emoji(self):
        banner = Banner.objects.create(title="Test")
        self.assertEqual(banner.emoji, "💎")


class ProductAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Uzuklar", slug="uzuklar")
        self.product = Product.objects.create(
            name="Oltin uzuk",
            price=Decimal("1500000"),
            category=self.category,
            metal_type="gold",
            weight=Decimal("5.50"),
            in_stock=True,
            is_featured=True,
        )
        Product.objects.create(
            name="Kumush uzuk",
            price=Decimal("500000"),
            category=self.category,
            metal_type="silver",
            weight=Decimal("3.20"),
        )

    def test_list_products(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_retrieve_product(self):
        response = self.client.get(f"/api/products/{self.product.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Oltin uzuk")

    def test_filter_by_category(self):
        response = self.client.get("/api/products/", {"category": "uzuklar"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_filter_by_metal_type(self):
        response = self.client.get("/api/products/", {"metal_type": "gold"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_search_products(self):
        response = self.client.get("/api/products/", {"search": "Oltin"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_featured_products(self):
        response = self.client.get("/api/products/featured/")
        self.assertEqual(response.status_code, 200)

    def test_list_categories(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 200)

    def test_list_banners(self):
        Banner.objects.create(title="Test Banner")
        response = self.client.get("/api/banners/")
        self.assertEqual(response.status_code, 200)
