from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "icon", "image"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_main"]


class ProductListSerializer(serializers.ModelSerializer):
    """Mahsulotlar ro'yxati uchun"""

    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "old_price",
            "images",
            "category",
            "metal_type",
            "weight",
            "in_stock",
            "is_featured",
            "discount_percent",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Bitta mahsulot uchun to'liq ma'lumot"""

    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "old_price",
            "images",
            "category",
            "metal_type",
            "weight",
            "size",
            "proba",
            "in_stock",
            "is_featured",
            "discount_percent",
            "created_at",
        ]
