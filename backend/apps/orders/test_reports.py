from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from apps.orders.models import Order, OrderItem
from apps.orders.reports import compute_financial_report
from apps.products.models import Category, Product
from apps.users.models import TelegramUser


class FinancialReportTest(TestCase):
    def setUp(self):
        self.user = TelegramUser.objects.create(
            telegram_id=555111, first_name="Report"
        )
        self.category = Category.objects.create(name="Makiyaj", slug="makiyaj")
        self.product = Product.objects.create(
            name="Lab bo'yog'i",
            price=Decimal("150000"),
            cost_price=Decimal("100000"),
            category=self.category,
            product_type="makeup",
        )
        self.today = timezone.localdate()

    def _make_order(self, status="delivered", is_paid=True, qty=2, method="cash"):
        order = Order.objects.create(
            user=self.user, phone="+998901112233",
            status=status, is_paid=is_paid, payment_method=method,
        )
        OrderItem.objects.create(
            order=order, product=self.product, quantity=qty,
            price=Decimal("150000"), cost_price=Decimal("100000"),
        )
        order.calculate_total()
        return order

    def test_report_profit_math(self):
        self._make_order(qty=2)  # tushum 300k, tannarx 200k, foyda 100k
        rep = compute_financial_report(self.today, self.today)
        self.assertEqual(rep["orders_count"], 1)
        self.assertEqual(rep["product_revenue"], Decimal("300000"))
        self.assertEqual(rep["cogs"], Decimal("200000"))
        self.assertEqual(rep["gross_profit"], Decimal("100000"))
        self.assertEqual(rep["margin"], 33)  # 100k / 300k

    def test_payment_and_paid_breakdown(self):
        self._make_order(method="cash", is_paid=True, qty=1)
        self._make_order(method="transfer", is_paid=False, qty=1)
        rep = compute_financial_report(self.today, self.today)
        self.assertEqual(rep["cash"]["count"], 1)
        self.assertEqual(rep["transfer"]["count"], 1)
        self.assertEqual(rep["paid"]["count"], 1)
        self.assertEqual(rep["unpaid"]["count"], 1)

    def test_cancelled_excluded_from_totals(self):
        self._make_order(status="delivered", qty=2)
        self._make_order(status="cancelled", qty=5)
        rep = compute_financial_report(self.today, self.today)
        self.assertEqual(rep["orders_count"], 1)  # bekor qilingan kirmaydi
        self.assertEqual(rep["gross_profit"], Decimal("100000"))
        self.assertEqual(rep["cancelled"]["count"], 1)

    def test_empty_period_no_error(self):
        rep = compute_financial_report(self.today, self.today)
        self.assertEqual(rep["orders_count"], 0)
        self.assertEqual(rep["gross_profit"], Decimal("0"))
        self.assertEqual(rep["margin"], 0)


class FinancialReportViewTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", password="pass12345", email="a@a.uz"
        )
        self.client.login(username="admin", password="pass12345")

    def test_report_page_renders(self):
        resp = self.client.get("/admin/hisobot/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Moliyaviy hisobot")

    def test_xlsx_export(self):
        resp = self.client.get("/admin/hisobot/?period=this_month&export=xlsx")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("spreadsheetml", resp["Content-Type"])
        self.assertIn("attachment", resp["Content-Disposition"])

    def test_requires_staff(self):
        self.client.logout()
        resp = self.client.get("/admin/hisobot/")
        self.assertEqual(resp.status_code, 302)  # login sahifasiga
