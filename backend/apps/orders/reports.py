"""Moliyaviy hisobot — davr bo'yicha tushum, tannarx va foyda hisoblash.

Soliq rejimi va xarajat jurnali hali kiritilmagan (qaror kutilmoqda) — bu modul
faqat sotuv ma'lumotidan yalpi foydani (tushum − tannarx) hisoblaydi.
Davr `created_at` (buyurtma sanasi) bo'yicha olinadi.
"""
from datetime import date, timedelta
from decimal import Decimal

from django.db.models import Count, DecimalField, F, Sum
from django.utils import timezone

from .models import Order, OrderItem


def _q(value):
    return value or Decimal("0")


def resolve_period(period: str, start=None, end=None):
    """Period kalitidan (start_date, end_date, label) qaytaradi."""
    today = timezone.localdate()
    if period == "custom" and start and end:
        return start, end, f"{start:%d.%m.%Y} — {end:%d.%m.%Y}"
    if period == "last_month":
        first_this = today.replace(day=1)
        last_prev = first_this - timedelta(days=1)
        first_prev = last_prev.replace(day=1)
        return first_prev, last_prev, f"O'tgan oy ({first_prev:%B %Y})"
    if period == "last_7":
        return today - timedelta(days=6), today, "Oxirgi 7 kun"
    # default: this_month
    first = today.replace(day=1)
    return first, today, f"Shu oy ({first:%B %Y})"


def compute_financial_report(start: date, end: date) -> dict:
    """Berilgan sana oralig'i uchun moliyaviy ko'rsatkichlarni hisoblaydi."""
    orders = Order.objects.filter(
        created_at__date__gte=start, created_at__date__lte=end
    )
    active = orders.exclude(status="cancelled")
    cancelled = orders.filter(status="cancelled")

    order_agg = active.aggregate(
        count=Count("id"),
        revenue=Sum("total"),
        delivery=Sum("delivery_fee"),
    )
    item_agg = OrderItem.objects.filter(order__in=active).aggregate(
        product_revenue=Sum(
            F("price") * F("quantity"), output_field=DecimalField()
        ),
        cogs=Sum(F("cost_price") * F("quantity"), output_field=DecimalField()),
    )

    product_revenue = _q(item_agg["product_revenue"])
    cogs = _q(item_agg["cogs"])
    gross_profit = product_revenue - cogs
    margin = (
        int(gross_profit / product_revenue * 100) if product_revenue else 0
    )

    by_payment = {
        row["payment_method"]: {
            "count": row["count"],
            "revenue": _q(row["revenue"]),
        }
        for row in active.values("payment_method").annotate(
            count=Count("id"), revenue=Sum("total")
        )
    }

    paid = active.filter(is_paid=True).aggregate(
        count=Count("id"), revenue=Sum("total")
    )
    unpaid = active.filter(is_paid=False).aggregate(
        count=Count("id"), revenue=Sum("total")
    )
    cancelled_agg = cancelled.aggregate(count=Count("id"), value=Sum("total"))

    return {
        "start": start,
        "end": end,
        "orders_count": order_agg["count"] or 0,
        "revenue": _q(order_agg["revenue"]),           # tushum (yetkazish bilan)
        "delivery_fees": _q(order_agg["delivery"]),
        "product_revenue": product_revenue,            # mahsulot tushumi
        "cogs": cogs,                                  # tannarx
        "gross_profit": gross_profit,                  # yalpi foyda
        "margin": margin,                              # foyda ulushi %
        "cash": by_payment.get("cash", {"count": 0, "revenue": Decimal("0")}),
        "transfer": by_payment.get(
            "transfer", {"count": 0, "revenue": Decimal("0")}
        ),
        "paid": {"count": paid["count"] or 0, "revenue": _q(paid["revenue"])},
        "unpaid": {
            "count": unpaid["count"] or 0,
            "revenue": _q(unpaid["revenue"]),
        },
        "cancelled": {
            "count": cancelled_agg["count"] or 0,
            "value": _q(cancelled_agg["value"]),
        },
    }
