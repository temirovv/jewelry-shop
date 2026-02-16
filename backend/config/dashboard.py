from django.utils import timezone
from datetime import timedelta

from apps.orders.models import Order
from apps.products.models import Product, Category
from apps.users.models import TelegramUser
from apps.cart.models import Cart


def get_dashboard_callback(request, context):
    today = timezone.now()
    month_ago = today - timedelta(days=30)
    week_ago = today - timedelta(days=7)

    # Umumiy statistika
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status="pending").count()
    total_revenue = sum(
        o.total for o in Order.objects.filter(status="delivered")
    ) or 0
    month_revenue = sum(
        o.total for o in Order.objects.filter(
            status="delivered", created_at__gte=month_ago
        )
    ) or 0

    total_users = TelegramUser.objects.filter(is_active=True).count()
    new_users_week = TelegramUser.objects.filter(created_at__gte=week_ago).count()

    total_products = Product.objects.filter(is_active=True).count()
    out_of_stock = Product.objects.filter(is_active=True, in_stock=False).count()
    active_carts = Cart.objects.filter(items__isnull=False).distinct().count()

    # So'nggi buyurtmalar
    recent_orders = Order.objects.select_related("user").order_by("-created_at")[:5]

    # Top mahsulotlar (buyurtma soni bo'yicha)
    from django.db.models import Count
    top_products = Product.objects.filter(
        is_active=True,
        orderitem__isnull=False,
    ).annotate(
        order_count=Count("orderitem")
    ).order_by("-order_count")[:5]

    context.update({
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "total_revenue": f"{total_revenue:,.0f}",
        "month_revenue": f"{month_revenue:,.0f}",
        "total_users": total_users,
        "new_users_week": new_users_week,
        "total_products": total_products,
        "out_of_stock": out_of_stock,
        "active_carts": active_carts,
        "recent_orders": recent_orders,
        "top_products": top_products,
    })

    return context
