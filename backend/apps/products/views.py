from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from .models import Banner, Brand, Category, Product
from .serializers import (
    BannerSerializer,
    BrandSerializer,
    CategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer,
)
from .filters import ProductFilter


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    """Bannerlar API"""

    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Kategoriyalar API"""

    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    """Brendlar API"""

    serializer_class = BrandSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Brand.objects.filter(is_active=True)
            .annotate(products_count=Count("products"))
        )

    @action(detail=False, methods=["get"])
    def featured(self, request):
        """Tavsiya qilingan brendlar"""
        queryset = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Mahsulotlar API"""

    queryset = (
        Product.objects.filter(is_active=True)
        .select_related("category", "brand")
        .prefetch_related("images")
    )
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description", "brand__name"]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer

    @action(detail=False, methods=["get"])
    def featured(self, request):
        """Tavsiya qilingan mahsulotlar"""
        queryset = self.get_queryset().filter(is_featured=True)[:10]
        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def new_arrivals(self, request):
        """Yangi mahsulotlar"""
        queryset = self.get_queryset().order_by("-created_at")[:10]
        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)
