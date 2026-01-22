from .models import Order


def get_pending_orders_count(request):
    """Return pending orders count for sidebar badge."""
    count = Order.objects.filter(status="pending").count()
    return count if count > 0 else None
