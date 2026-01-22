from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ["image", "is_main", "order", "image_preview"]
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"

    image_preview.short_description = "Ko'rinish"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "icon", "order", "is_active"]
    list_editable = ["order", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "price",
        "old_price",
        "weight",
        "in_stock",
        "is_featured",
        "created_at",
    ]
    list_filter = ["category", "metal_type", "in_stock", "is_featured", "created_at"]
    search_fields = ["name", "description"]
    list_editable = ["in_stock", "is_featured"]
    inlines = [ProductImageInline]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (None, {"fields": ("name", "description", "category")}),
        ("Narx", {"fields": ("price", "old_price")}),
        ("Xususiyatlar", {"fields": ("metal_type", "weight", "size", "proba")}),
        ("Holat", {"fields": ("in_stock", "is_featured", "is_active")}),
        ("Vaqt", {"fields": ("created_at", "updated_at")}),
    )
