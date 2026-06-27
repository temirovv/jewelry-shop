from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient

from apps.products.models import Brand, Category, Product, ProductImage, Banner


class CategoryModelTest(TestCase):
    def test_slug_auto_generated(self):
        cat = Category.objects.create(name="Makiyaj")
        self.assertEqual(cat.slug, "makiyaj")

    def test_str(self):
        cat = Category.objects.create(name="Parfyumeriya")
        self.assertEqual(str(cat), "Parfyumeriya")


class BrandModelTest(TestCase):
    def test_slug_auto_generated(self):
        brand = Brand.objects.create(name="Maybelline")
        self.assertEqual(brand.slug, "maybelline")

    def test_str(self):
        brand = Brand.objects.create(name="Dior")
        self.assertEqual(str(brand), "Dior")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Teri parvarishi", slug="skincare")
        self.brand = Brand.objects.create(name="L'Oréal", slug="loreal")
        self.product = Product.objects.create(
            name="Namlovchi yuz kremi",
            price=Decimal("150000"),
            old_price=Decimal("200000"),
            category=self.category,
            brand=self.brand,
            product_type="skincare",
            volume="50 ml",
        )

    def test_str(self):
        self.assertEqual(str(self.product), "Namlovchi yuz kremi")

    def test_discount_percent(self):
        self.assertEqual(self.product.discount_percent, 25)

    def test_discount_percent_no_old_price(self):
        self.product.old_price = None
        self.product.save()
        self.assertEqual(self.product.discount_percent, 0)

    def test_main_image_none(self):
        self.assertIsNone(self.product.main_image)

    def test_main_image_without_file(self):
        """Agar image file yo'q bo'lsa, None qaytarishi kerak."""
        ProductImage.objects.create(
            product=self.product,
            is_main=True,
        )
        self.assertIsNone(self.product.main_image)


class BannerModelTest(TestCase):
    def test_str(self):
        banner = Banner.objects.create(title="Yangi kolleksiya")
        self.assertEqual(str(banner), "Yangi kolleksiya")

    def test_default_emoji(self):
        banner = Banner.objects.create(title="Test")
        self.assertEqual(banner.emoji, "💄")


class ProductAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Teri parvarishi", slug="skincare")
        self.brand_loreal = Brand.objects.create(name="L'Oréal", slug="loreal")
        self.brand_nivea = Brand.objects.create(name="Nivea", slug="nivea")
        self.product = Product.objects.create(
            name="Namlovchi yuz kremi",
            price=Decimal("150000"),
            category=self.category,
            brand=self.brand_loreal,
            product_type="skincare",
            volume="50 ml",
            in_stock=True,
            is_featured=True,
        )
        Product.objects.create(
            name="Tana suti",
            price=Decimal("70000"),
            category=self.category,
            brand=self.brand_nivea,
            product_type="bodycare",
            volume="400 ml",
        )

    def test_list_products(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_retrieve_product(self):
        response = self.client.get(f"/api/products/{self.product.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Namlovchi yuz kremi")

    def test_filter_by_category(self):
        response = self.client.get("/api/products/", {"category": "skincare"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_filter_by_brand(self):
        response = self.client.get("/api/products/", {"brand": "loreal"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_filter_by_product_type(self):
        response = self.client.get("/api/products/", {"product_type": "bodycare"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_search_products(self):
        response = self.client.get("/api/products/", {"search": "yuz"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_featured_products(self):
        response = self.client.get("/api/products/featured/")
        self.assertEqual(response.status_code, 200)

    def test_list_categories(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 200)

    def test_list_brands(self):
        response = self.client.get("/api/brands/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_banners(self):
        Banner.objects.create(title="Test Banner")
        response = self.client.get("/api/banners/")
        self.assertEqual(response.status_code, 200)
