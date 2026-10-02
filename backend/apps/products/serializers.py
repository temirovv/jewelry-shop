from rest_framework import serializers
from .models import Banner, Brand, Category, Product, ProductImage
from .thumbnails import LARGE_WIDTH, THUMB_WIDTH, get_thumbnail_url


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
    thumbnail = serializers.SerializerMethodField()
    large = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "image", "thumbnail", "large", "is_main"]

    def _absolute(self, url):
        if not url:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(url) if request else url

    def get_image(self, obj):
        return self._absolute(obj.image.url) if obj.image else None

    def get_thumbnail(self, obj):
        return self._absolute(get_thumbnail_url(obj.image, THUMB_WIDTH))

    def get_large(self, obj):
        return self._absolute(get_thumbnail_url(obj.image, LARGE_WIDTH))


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
            "slug",
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
            "slug",
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
