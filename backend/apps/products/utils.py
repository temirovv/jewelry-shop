from .models import Product


def get_products_count(request):
    """Return total products count for sidebar badge."""
    return Product.objects.filter(is_active=True).count()
