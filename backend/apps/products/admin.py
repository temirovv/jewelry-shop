from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.decorators import display, action
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Banner, Category, Product, ProductImage


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = (
            "id", "name", "price", "old_price", "category__name",
            "metal_type", "weight", "size", "proba",
            "in_stock", "is_featured", "is_active", "created_at",
        )
        export_order = fields


@admin.register(Banner)
class BannerAdmin(ModelAdmin):
    list_display = [
        "display_preview",
        "title",
        "subtitle",
        "display_link",
        "order",
        "display_status",
    ]
    list_display_links = ["display_preview", "title"]
    list_editable = ["order"]
    ordering = ["order"]
    search_fields = ["title", "subtitle"]
    list_filter = ["is_active"]
    list_filter_submit = True
    list_per_page = 20
    readonly_fields = ["image_preview"]

    fieldsets = (
        ("Asosiy", {
            "fields": ("title", "subtitle", "emoji"),
            "classes": ["tab"],
        }),
        ("Ko'rinish", {
            "fields": ("image", "gradient", "image_preview"),
            "classes": ["tab"],
        }),
        ("Sozlamalar", {
            "fields": ("link", "order", "is_active"),
            "classes": ["tab"],
        }),
    )

    @display(description="Ko'rinish")
    def display_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" class="rounded-lg shadow-sm" '
                'style="width: 80px; height: 40px; object-fit: cover;" />',
                obj.image.url,
            )
        return format_html(
            '<div class="rounded-lg flex items-center justify-center" '
            'style="width: 80px; height: 40px; background: linear-gradient(135deg, #f59e0b, #d97706);">'
            '<span style="color: white; font-size: 18px;">{}</span></div>',
            obj.emoji or "💎",
        )

    @display(description="Link")
    def display_link(self, obj):
        if obj.link:
            return format_html(
                '<span class="text-xs text-blue-600">{}</span>',
                obj.link[:30] + "..." if len(obj.link) > 30 else obj.link,
            )
        return "—"

    @display(
        description="Holat",
        label={True: "success", False: "danger"},
    )
    def display_status(self, obj):
        return obj.is_active

    @display(description="Banner ko'rinishi")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" class="rounded-xl shadow-md" '
                'style="max-width: 400px; max-height: 200px; object-fit: cover;" />',
                obj.image.url,
            )
        return format_html('<span class="text-gray-400">Rasm yuklanmagan</span>')


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
    list_display = ["name", "slug", "display_icon", "display_products_count", "order", "display_status"]
    list_editable = ["order"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order"]
    search_fields = ["name", "slug"]
    list_filter = ["is_active"]
    list_filter_submit = True

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("products"))

    @display(description="Icon", label=True)
    def display_icon(self, obj):
        return obj.icon or "—"

    @display(description="Mahsulotlar", ordering="products_count")
    def display_products_count(self, obj):
        count = getattr(obj, "products_count", 0)
        if count > 0:
            return format_html(
                '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">{} ta</span>',
                count,
            )
        return format_html('<span class="text-gray-400">0</span>')

    @display(
        description="Holat",
        label={True: "success", False: "danger"},
    )
    def display_status(self, obj):
        return obj.is_active


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    resource_classes = [ProductResource]
    list_display = [
        "display_image",
        "name",
        "category",
        "display_metal",
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
    actions = ["duplicate_products", "mark_in_stock", "mark_out_of_stock", "mark_featured", "unmark_featured"]

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

    @display(
        description="Metall",
        label={
            "gold": "warning",
            "silver": "secondary",
            "platinum": "info",
            "white_gold": "primary",
        },
    )
    def display_metal(self, obj):
        return obj.metal_type

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

    @action(description="Nusxa ko'chirish", icon="content_copy")
    def duplicate_products(self, request, queryset):
        for product in queryset:
            images = list(product.images.all())
            product.pk = None
            product.name = f"{product.name} (nusxa)"
            product.save()
            for img in images:
                img.pk = None
                img.product = product
                img.save()
        self.message_user(request, f"{queryset.count()} ta mahsulot nusxalandi.")

    @action(description="Sotuvda deb belgilash", icon="check_circle")
    def mark_in_stock(self, request, queryset):
        queryset.update(in_stock=True)
        self.message_user(request, f"{queryset.count()} ta mahsulot sotuvda deb belgilandi.")

    @action(description="Sotuvda emas deb belgilash", icon="remove_circle")
    def mark_out_of_stock(self, request, queryset):
        queryset.update(in_stock=False)
        self.message_user(request, f"{queryset.count()} ta mahsulot sotuvda emas deb belgilandi.")

    @action(description="Maxsus deb belgilash", icon="star")
    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} ta mahsulot maxsus deb belgilandi.")

    @action(description="Maxsusdan chiqarish", icon="star_border")
    def unmark_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} ta mahsulot maxsusdan chiqarildi.")

