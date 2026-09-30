from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APIClient

from apps.products.models import Category, Product


class ProductSlugTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Parfyum", slug="parfyum")

    def _product(self, name, **kwargs):
        return Product.objects.create(
            name=name, price=Decimal("100000"), category=self.category, **kwargs
        )

    def test_slug_generated_from_name(self):
        self.assertEqual(self._product("Chanel No 5").slug, "chanel-no-5")

    def test_duplicate_names_get_unique_slugs(self):
        slugs = [self._product("Krem").slug for _ in range(3)]
        self.assertEqual(slugs, ["krem", "krem-2", "krem-3"])

    def test_slug_kept_on_rename(self):
        product = self._product("Eski nom")
        product.name = "Yangi nom"
        product.save()
        self.assertEqual(product.slug, "eski-nom")

    def test_numeric_name_does_not_give_numeric_slug(self):
        slug = self._product("1001").slug
        self.assertFalse(slug.isdigit())

    def test_symbol_only_name_gets_fallback(self):
        self.assertEqual(self._product("!!!").slug, "mahsulot")

    def test_numeric_slug_rejected_by_validation(self):
        product = Product(
            name="X", slug="12345", price=Decimal("1"), category=self.category
        )
        with self.assertRaises(ValidationError):
            product.full_clean()


class ProductSlugAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        category = Category.objects.create(name="Parfyum", slug="parfyum")
        self.product = Product.objects.create(
            name="Light Blue", price=Decimal("100000"), category=category
        )

    def test_retrieve_by_slug(self):
        response = self.client.get(f"/api/products/{self.product.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["slug"], "light-blue")

    def test_retrieve_by_legacy_id(self):
        response = self.client.get(f"/api/products/{self.product.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.product.id)

    def test_unknown_slug_404(self):
        self.assertEqual(self.client.get("/api/products/yoq-narsa/").status_code, 404)

    def test_inactive_product_hidden_by_slug(self):
        self.product.is_active = False
        self.product.save()
        response = self.client.get(f"/api/products/{self.product.slug}/")
        self.assertEqual(response.status_code, 404)

    def test_list_includes_slug(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.data["results"][0]["slug"], "light-blue")


class ProductDuplicateAdminTest(TestCase):
    def test_duplicate_action_gets_new_slug(self):
        admin = User.objects.create_superuser("admin", "a@a.uz", "pass12345")
        client = APIClient()
        client.force_login(admin)
        category = Category.objects.create(name="Parfyum", slug="parfyum")
        product = Product.objects.create(
            name="Light Blue", price=Decimal("100000"), category=category
        )
        client.post(
            "/admin/products/product/",
            {"action": "duplicate_products", "_selected_action": [product.pk]},
        )
        self.assertEqual(
            sorted(Product.objects.values_list("slug", flat=True)),
            ["light-blue", "light-blue-nusxa"],
        )
