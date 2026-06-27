import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    """Mahsulotlar filtri"""

    category = django_filters.CharFilter(field_name="category__slug")
    brand = django_filters.CharFilter(field_name="brand__slug")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    product_type = django_filters.CharFilter(field_name="product_type")
    skin_type = django_filters.CharFilter(field_name="skin_type")
    is_featured = django_filters.BooleanFilter(field_name="is_featured")
    in_stock = django_filters.BooleanFilter(field_name="in_stock")

    class Meta:
        model = Product
        fields = ["category", "brand", "product_type", "skin_type", "is_featured", "in_stock"]
