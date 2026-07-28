from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.decorators import display, action
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from .models import Banner, Brand, Category, Product, ProductImage


class ProductResource(resources.ModelResource):
    """Mahsulotlarni CSV/XLSX orqali import/export. Brend va kategoriya
    NOM bo'yicha bog'lanadi (ular avval yaratilgan bo'lishi kerak)."""

    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(Category, field="name"),
    )
    brand = fields.Field(
        column_name="brand",
        attribute="brand",
        widget=ForeignKeyWidget(Brand, field="name"),
    )

    class Meta:
        model = Product
        import_id_fields = ("name",)  # nom bo'yicha moslashtiriladi (id ustuni shart emas)
        skip_unchanged = True
        report_skipped = True
        fields = (
            "id", "name", "description", "price", "old_price", "cost_price",
            "category", "brand", "product_type", "skin_type", "volume", "shade",
            "ingredients", "shelf_life_months", "country_of_origin",
            "in_stock", "is_featured", "is_active",
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
            'style="width: 80px; height: 40px; background: linear-gradient(135deg, #ec4899, #be185d);">'
            '<span style="color: white; font-size: 18px;">{}</span></div>',
            obj.emoji or "💄",
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


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ["display_logo", "name", "country", "display_products_count", "order", "display_status"]
    list_display_links = ["display_logo", "name"]
    list_editable = ["order"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order", "name"]
    search_fields = ["name", "country"]
    list_filter = ["is_featured", "is_active"]
    list_filter_submit = True
    readonly_fields = ["logo_preview", "created_at"]

    fieldsets = (
        ("Asosiy", {
            "fields": ("name", "slug", "country", "description"),
            "classes": ["tab"],
        }),
        ("Logo", {
            "fields": ("logo", "logo_preview"),
            "classes": ["tab"],
        }),
        ("Sozlamalar", {
            "fields": ("is_featured", "is_active", "order", "created_at"),
            "classes": ["tab"],
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("products"))

    @display(description="Logo")
    def display_logo(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" class="rounded-lg shadow-sm" '
                'style="width: 48px; height: 48px; object-fit: contain; background:#fff;" />',
                obj.logo.url,
            )
        return format_html(
            '<div class="flex items-center justify-center w-12 h-12 bg-pink-100 rounded-lg">'
            '<span class="text-pink-600 font-semibold">{}</span></div>',
            (obj.name[:2].upper() if obj.name else "?"),
        )

    @display(description="Mahsulotlar", ordering="products_count")
    def display_products_count(self, obj):
        count = getattr(obj, "products_count", 0)
        if count > 0:
            return format_html(
                '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">{} ta</span>',
                count,
            )
        return format_html('<span class="text-gray-400">0</span>')

    @display(description="Holat", label={True: "success", False: "danger"})
    def display_status(self, obj):
        return obj.is_active

    @display(description="Logo ko'rinishi")
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" class="rounded-xl shadow-md" '
                'style="max-width: 200px; max-height: 120px; object-fit: contain;" />',
                obj.logo.url,
            )
        return format_html('<span class="text-gray-400">Logo yuklanmagan</span>')


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    resource_classes = [ProductResource]
    list_display = [
        "display_image",
        "name",
        "brand",
        "category",
        "display_type",
        "display_price",
        "display_profit",
        "display_volume",
        "in_stock",
        "is_featured",
        "created_at",
    ]
    list_display_links = ["display_image", "name"]
    list_filter = ["category", "brand", "product_type", "skin_type", "in_stock", "is_featured", "created_at"]
    search_fields = ["name", "description", "brand__name"]
    list_editable = ["in_stock", "is_featured"]
    list_filter_submit = True
    inlines = [ProductImageInline]
    readonly_fields = ["created_at", "updated_at", "unit_profit_display"]
    date_hierarchy = "created_at"
    list_per_page = 20
    save_on_top = True
    actions = ["duplicate_products", "mark_in_stock", "mark_out_of_stock", "mark_featured", "unmark_featured"]

    fieldsets = (
        ("Asosiy", {
            "fields": ("name", "description", "category", "brand"),
            "classes": ["tab"],
        }),
        ("Narx", {
            "fields": ("price", "old_price", "cost_price", "unit_profit_display"),
            "classes": ["tab"],
        }),
        ("Xususiyatlar", {
            "fields": ("product_type", "skin_type", "volume", "shade", "ingredients", "shelf_life_months", "country_of_origin"),
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
        description="Tur",
        label={
            "skincare": "info",
            "makeup": "primary",
            "perfume": "warning",
            "haircare": "secondary",
            "bodycare": "success",
        },
    )
    def display_type(self, obj):
        return obj.get_product_type_display()

    @display(description="Rasm")
    def display_image(self, obj):
        images = list(obj.images.all())
        main_image = next((i for i in images if i.is_main), None) or (
            images[0] if images else None
        )
        if main_image and main_image.image:
            return format_html(
                '<img src="{}" class="rounded-lg shadow-sm" '
                'style="width: 50px; height: 50px; object-fit: cover;" />',
                main_image.image.url,
            )
        return format_html(
            '<div class="flex items-center justify-center w-12 h-12 bg-pink-100 rounded-lg">'
            '<span class="text-pink-600">💄</span></div>'
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

    @display(description="Foyda", ordering="cost_price")
    def display_profit(self, obj):
        if not obj.cost_price:
            return format_html('<span class="text-gray-400 text-xs">tannarx yo\'q</span>')
        profit = obj.unit_profit
        margin = int(profit / obj.price * 100) if obj.price else 0
        color = "text-green-600" if profit > 0 else "text-red-600"
        profit_formatted = "{:,.0f}".format(profit).replace(",", " ")
        return format_html(
            '<div><span class="font-semibold {}">{} so\'m</span>'
            '<br><span class="text-xs text-gray-400">{}%</span></div>',
            color, profit_formatted, margin,
        )

    @display(description="Bir dona foyda")
    def unit_profit_display(self, obj):
        if not obj.pk:
            return format_html('<span class="text-gray-400">Saqlangandan keyin</span>')
        if not obj.cost_price:
            return format_html('<span class="text-gray-400">Tannarx kiritilmagan</span>')
        profit = obj.unit_profit
        margin = int(profit / obj.price * 100) if obj.price else 0
        profit_formatted = "{:,.0f}".format(profit).replace(",", " ")
        return format_html(
            '<span class="font-semibold text-green-600">{} so\'m ({}%)</span>',
            profit_formatted, margin,
        )

    @display(description="Hajm")
    def display_volume(self, obj):
        if obj.volume:
            return format_html(
                '<span class="text-gray-600">{}</span>',
                obj.volume
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

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("brand", "category").prefetch_related("images")

