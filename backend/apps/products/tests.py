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


class ProductAdminFormTest(TestCase):
    """Admin'da mahsulot qo'shish formasi to'liq render bo'lishi kerak.

    Unfold nomsiz (None) fieldset'ni "tab" klassi bilan hech qayerda
    chiqarmaydi — natijada majburiy maydonlar ko'rinmay qoladi va saqlashda
    "Please correct the errors below" xatosi hech qaysi maydonga ishora
    qilmaydi.
    """

    def setUp(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="test_admin", password="test_pass_12345"
        )
        self.client.force_login(admin_user)

    def test_all_form_fields_rendered_on_add_page(self):
        response = self.client.get("/admin/products/product/add/")
        self.assertEqual(response.status_code, 200)

        html = response.content.decode()
        form = response.context["adminform"].form
        missing = [name for name in form.fields if f'id_{name}"' not in html]
        self.assertEqual(missing, [], f"Formada ko'rinmayotgan maydonlar: {missing}")

    def test_every_fieldset_tab_has_a_name(self):
        from apps.products.admin import ProductAdmin

        for name, options in ProductAdmin.fieldsets:
            if "tab" in options.get("classes", []):
                self.assertTrue(name, "Tab fieldset nomsiz bo'lishi mumkin emas")


class CostPriceOptionalTest(TestCase):
    """Tannarx ixtiyoriy: bo'sh qoldirilsa 0 bo'lib saqlanishi kerak.

    Maydon `null=False`, shuning uchun faqat `blank=True` yetarli emas —
    bo'sh forma `None` beradi va saqlashda NOT NULL xatosi chiqadi.
    """

    def setUp(self):
        self.category = Category.objects.create(name="Makiyaj", slug="makiyaj")

    def test_cost_price_is_not_required_in_form(self):
        from django.forms import modelform_factory

        Form = modelform_factory(Product, fields=["name", "price", "category", "cost_price"])
        self.assertFalse(Form().fields["cost_price"].required)

    def test_empty_cost_price_saved_as_zero(self):
        product = Product.objects.create(
            name="Tannarxsiz", price=Decimal("120000"),
            category=self.category, cost_price=None,
        )
        product.refresh_from_db()
        self.assertEqual(product.cost_price, Decimal("0"))

    def test_admin_accepts_blank_cost_price(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="cost_admin", password="test_pass_12345"
        )
        self.client.force_login(admin_user)

        response = self.client.post("/admin/products/product/add/", {
            "name": "Bo'sh tannarx", "description": "",
            "category": str(self.category.pk), "brand": "",
            "price": "200000", "old_price": "", "cost_price": "",
            "product_type": "skincare", "skin_type": "all",
            "volume": "", "shade": "", "ingredients": "",
            "shelf_life_months": "", "country_of_origin": "",
            "in_stock": "on", "is_active": "on",
            "images-TOTAL_FORMS": "0", "images-INITIAL_FORMS": "0",
            "images-MIN_NUM_FORMS": "0", "images-MAX_NUM_FORMS": "1000",
            "_save": "Save",
        })
        self.assertEqual(response.status_code, 302, "Bo'sh tannarx bilan saqlanishi kerak")
        self.assertEqual(Product.objects.get(name="Bo'sh tannarx").cost_price, Decimal("0"))

    def test_unit_profit_without_cost_price(self):
        product = Product.objects.create(
            name="Tannarxsiz 2", price=Decimal("90000"), category=self.category,
        )
        self.assertEqual(product.unit_profit, Decimal("90000"))


class ProductImportTest(TestCase):
    """CSV/XLSX import — brend va kategoriya nom bo'yicha bog'lanadi."""

    def setUp(self):
        self.category = Category.objects.create(name="Makiyaj", slug="makiyaj")
        self.brand = Brand.objects.create(name="TestBrand")

    def test_import_resolves_fk_by_name_and_costs(self):
        import tablib

        from apps.products.admin import ProductResource

        resource = ProductResource()
        dataset = tablib.Dataset()
        dataset.headers = [
            "name", "description", "price", "old_price", "cost_price",
            "category", "brand", "product_type", "skin_type", "volume",
            "shade", "ingredients", "shelf_life_months", "country_of_origin",
            "in_stock", "is_featured", "is_active",
        ]
        dataset.append([
            "Matte lab bo'yog'i", "Matte lab", "150000", "", "100000",
            "Makiyaj", "TestBrand", "makeup", "all", "5 ml",
            "Nude 02", "Vitamin E", "24", "Koreya", "1", "1", "1",
        ])

        result = resource.import_data(dataset, dry_run=False)
        self.assertFalse(result.has_errors())

        product = Product.objects.get(name="Matte lab bo'yog'i")
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.brand, self.brand)
        self.assertEqual(product.price, Decimal("150000"))
        self.assertEqual(product.cost_price, Decimal("100000"))
        self.assertEqual(product.product_type, "makeup")
