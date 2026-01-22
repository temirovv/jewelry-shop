from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display, action
from .models import Order, OrderItem


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["subtotal", "display_product"]
    raw_id_fields = ["product"]
    fields = ["display_product", "product", "quantity", "price", "size", "subtotal"]
    tab = True

    @display(description="Mahsulot")
    def display_product(self, obj):
        if obj.product:
            return format_html(
                '<span class="font-medium">{}</span>',
                obj.product.name
            )
        return "—"


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = [
        "display_id",
        "display_user",
        "display_status",
        "display_total",
        "phone",
        "created_at",
    ]
    list_display_links = ["display_id", "display_user"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__first_name", "user__phone", "phone", "id"]
    readonly_fields = ["total", "created_at", "updated_at"]
    inlines = [OrderItemInline]
    ordering = ["-created_at"]
    list_filter_submit = True
    date_hierarchy = "created_at"
    list_per_page = 20
    save_on_top = True
    actions = ["mark_confirmed", "mark_processing", "mark_shipped", "mark_delivered"]

    fieldsets = (
        ("Buyurtma", {
            "fields": ("user", "status"),
            "classes": ["tab"],
        }),
        ("Aloqa", {
            "fields": ("phone", "delivery_address", "comment"),
            "classes": ["tab"],
        }),
        ("Moliya", {
            "fields": ("total",),
            "classes": ["tab"],
        }),
        ("Vaqt", {
            "fields": ("created_at", "updated_at"),
            "classes": ["tab"],
        }),
    )

    @display(description="ID")
    def display_id(self, obj):
        return format_html(
            '<span class="font-mono font-semibold text-primary-600">#{:05d}</span>',
            obj.id
        )

    @display(description="Mijoz")
    def display_user(self, obj):
        if obj.user:
            return format_html(
                '<div><span class="font-medium">{}</span>'
                '<br><span class="text-xs text-gray-400">@{}</span></div>',
                obj.user.first_name or "Noma'lum",
                obj.user.username or obj.user.telegram_id
            )
        return "—"

    @display(
        description="Holat",
        label={
            "pending": "warning",
            "confirmed": "info",
            "processing": "primary",
            "shipped": "secondary",
            "delivered": "success",
            "cancelled": "danger",
        },
    )
    def display_status(self, obj):
        return obj.status

    @display(description="Jami", ordering="total")
    def display_total(self, obj):
        return format_html(
            '<span class="font-semibold">{:,.0f} so\'m</span>',
            obj.total
        )

    @action(description="Tasdiqlash", icon="check_circle")
    def mark_confirmed(self, request, queryset):
        queryset.update(status="confirmed")
        self.message_user(request, f"{queryset.count()} ta buyurtma tasdiqlandi.")

    @action(description="Jarayonda", icon="sync")
    def mark_processing(self, request, queryset):
        queryset.update(status="processing")
        self.message_user(request, f"{queryset.count()} ta buyurtma jarayonga o'tkazildi.")

    @action(description="Yuborildi", icon="local_shipping")
    def mark_shipped(self, request, queryset):
        queryset.update(status="shipped")
        self.message_user(request, f"{queryset.count()} ta buyurtma yuborildi.")

    @action(description="Yetkazildi", icon="done_all")
    def mark_delivered(self, request, queryset):
        queryset.update(status="delivered")
        self.message_user(request, f"{queryset.count()} ta buyurtma yetkazildi.")
