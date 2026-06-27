from rest_framework import serializers
from .models import Banner, Brand, Category, Product, ProductImage


class BannerSerializer(serializers.ModelSerializer):
    """Banner serializeri"""

    class Meta:
        model = Banner
        fields = ["id", "title", "subtitle", "emoji", "gradient", "link", "image"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "icon", "image"]


class BrandSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    products_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Brand
        fields = ["id", "name", "slug", "logo", "country", "description", "is_featured", "products_count"]

    def get_logo(self, obj):
        if not obj.logo:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.logo.url)
        return obj.logo.url


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_main"]

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class ProductListSerializer(serializers.ModelSerializer):
    """Mahsulotlar ro'yxati uchun"""

    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
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
            "brand",
            "product_type",
            "volume",
            "in_stock",
            "is_featured",
            "discount_percent",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Bitta mahsulot uchun to'liq ma'lumot"""

    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
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
            "brand",
            "product_type",
            "skin_type",
            "volume",
            "shade",
            "ingredients",
            "shelf_life_months",
            "country_of_origin",
            "in_stock",
            "is_featured",
            "discount_percent",
            "created_at",
        ]
