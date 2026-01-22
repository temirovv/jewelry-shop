from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from .models import Category, Product, ProductImage


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    fields = ["image", "is_main", "order", "image_preview"]
    readonly_fields = ["image_preview"]
    tab = True

    @display(description="Ko'rinish")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" class="rounded-lg shadow-sm" style="max-width: 80px; max-height: 80px; object-fit: cover;" />',
                obj.image.url
            )
        return format_html('<span class="text-gray-400">—</span>')


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["name", "slug", "display_icon", "order", "display_status"]
    list_editable = ["order"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order"]
    search_fields = ["name", "slug"]
    list_filter_submit = True

    @display(description="Icon", label=True)
    def display_icon(self, obj):
        return obj.icon or "—"

    @display(
        description="Status",
        label={
            True: "success",
            False: "danger",
        },
    )
    def display_status(self, obj):
        return obj.is_active


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = [
        "display_image",
        "name",
        "category",
        "display_price",
        "display_weight",
        "in_stock",
        "is_featured",
        "created_at",
    ]
    list_display_links = ["display_image", "name"]
    list_filter = ["category", "metal_type", "in_stock", "is_featured", "created_at"]
    search_fields = ["name", "description"]
    list_editable = ["in_stock", "is_featured"]
    list_filter_submit = True
    inlines = [ProductImageInline]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "created_at"
    list_per_page = 20
    save_on_top = True

    fieldsets = (
        (None, {
            "fields": ("name", "description", "category"),
            "classes": ["tab"],
        }),
        ("Narx", {
            "fields": ("price", "old_price"),
            "classes": ["tab"],
        }),
        ("Xususiyatlar", {
            "fields": ("metal_type", "weight", "size", "proba"),
            "classes": ["tab"],
        }),
        ("Holat", {
            "fields": ("in_stock", "is_featured", "is_active"),
            "classes": ["tab"],
        }),
        ("Vaqt", {
            "fields": ("created_at", "updated_at"),
            "classes": ["tab"],
        }),
    )

    @display(description="Rasm")
    def display_image(self, obj):
        main_image = obj.images.filter(is_main=True).first() or obj.images.first()
        if main_image:
            # Check for file or URL
            image_url = None
            if main_image.image:
                image_url = main_image.image.url
            elif main_image.image_url:
                image_url = main_image.image_url

            if image_url:
                return format_html(
                    '<img src="{}" class="rounded-lg shadow-sm" style="width: 50px; height: 50px; object-fit: cover;" />',
                    image_url
                )
        return format_html(
            '<div class="flex items-center justify-center w-12 h-12 bg-amber-100 rounded-lg">'
            '<span class="text-amber-600">💎</span></div>'
        )

    @display(description="Narx", ordering="price")
    def display_price(self, obj):
        price_formatted = "{:,.0f}".format(obj.price)
        if obj.old_price:
            old_price_formatted = "{:,.0f}".format(obj.old_price)
            discount = int((1 - float(obj.price) / float(obj.old_price)) * 100)
            return format_html(
                '<div><span class="font-semibold text-primary-600">{} so\'m</span>'
                '<br><span class="text-xs line-through text-gray-400">{}</span>'
                ' <span class="text-xs text-red-500">-{}%</span></div>',
                price_formatted, old_price_formatted, discount
            )
        return format_html(
            '<span class="font-semibold">{} so\'m</span>',
            price_formatted
        )

    @display(description="Og'irlik")
    def display_weight(self, obj):
        if obj.weight:
            return format_html(
                '<span class="text-gray-600">{} gr</span>',
                obj.weight
            )
        return "—"

