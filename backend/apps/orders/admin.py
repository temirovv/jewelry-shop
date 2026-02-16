from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.forms import ExportForm
from unfold.decorators import display, action
from import_export import resources
from import_export.admin import ExportMixin
from .models import Order, OrderItem
from .utils import send_status_notification


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = (
            "id", "user__first_name", "user__telegram_id",
            "status", "total", "payment_method", "is_paid",
            "phone", "delivery_address", "comment",
            "created_at", "updated_at",
        )
        export_order = fields


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
class OrderAdmin(ExportMixin, ModelAdmin):
    export_form_class = ExportForm
    resource_classes = [OrderResource]
    list_display = [
        "display_id",
        "display_user",
        "display_status",
        "display_items_count",
        "display_payment",
        "display_total",
        "phone",
        "display_address",
        "created_at",
    ]
    list_display_links = ["display_id", "display_user"]
    list_filter = ["status", "payment_method", "is_paid", "created_at"]
    search_fields = ["user__first_name", "user__phone", "phone", "id"]
    readonly_fields = ["total", "created_at", "updated_at"]
    inlines = [OrderItemInline]
    ordering = ["-created_at"]
    list_filter_submit = True
    date_hierarchy = "created_at"
    list_per_page = 20
    save_on_top = True
    actions = ["mark_confirmed", "mark_processing", "mark_shipped", "mark_delivered", "mark_cancelled", "mark_paid", "mark_unpaid"]

    fieldsets = (
        ("Buyurtma", {
            "fields": ("user", "status"),
            "classes": ["tab"],
        }),
        ("Aloqa", {
            "fields": ("phone", "delivery_address", "comment"),
            "classes": ["tab"],
        }),
        ("To'lov", {
            "fields": ("payment_method", "is_paid", "total"),
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
            '<span class="font-mono font-semibold text-primary-600">#{}</span>',
            str(obj.id).zfill(5)
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
        total_formatted = f"{obj.total:,.0f}".replace(",", " ")
        return format_html(
            '<span class="font-semibold">{} so\'m</span>',
            total_formatted
        )

    @display(description="To'lov")
    def display_payment(self, obj):
        method = obj.get_payment_method_display()
        if obj.is_paid:
            return format_html(
                '<span class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-green-100 text-green-800">{} • To\'langan</span>',
                method
            )
        return format_html(
            '<span class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-yellow-100 text-yellow-800">{} • Kutilmoqda</span>',
            method
        )

    @action(description="To'langan deb belgilash", icon="payments")
    def mark_paid(self, request, queryset):
        queryset.update(is_paid=True)
        self.message_user(request, f"{queryset.count()} ta buyurtma to'langan deb belgilandi.")

    @action(description="To'lanmagan deb belgilash", icon="money_off")
    def mark_unpaid(self, request, queryset):
        queryset.update(is_paid=False)
        self.message_user(request, f"{queryset.count()} ta buyurtma to'lanmagan deb belgilandi.")

    def _bulk_status_update(self, request, queryset, new_status, message):
        """Ommaviy status yangilash va notification yuborish."""
        for order in queryset.select_related("user"):
            order.status = new_status
            order.save(update_fields=["status"])
            try:
                send_status_notification(order, new_status)
            except Exception:
                pass
        self.message_user(request, message)

    @action(description="Tasdiqlash", icon="check_circle")
    def mark_confirmed(self, request, queryset):
        self._bulk_status_update(
            request, queryset, "confirmed",
            f"{queryset.count()} ta buyurtma tasdiqlandi.",
        )

    @action(description="Jarayonda", icon="sync")
    def mark_processing(self, request, queryset):
        self._bulk_status_update(
            request, queryset, "processing",
            f"{queryset.count()} ta buyurtma jarayonga o'tkazildi.",
        )

    @action(description="Yuborildi", icon="local_shipping")
    def mark_shipped(self, request, queryset):
        self._bulk_status_update(
            request, queryset, "shipped",
            f"{queryset.count()} ta buyurtma yuborildi.",
        )

    @action(description="Yetkazildi", icon="done_all")
    def mark_delivered(self, request, queryset):
        self._bulk_status_update(
            request, queryset, "delivered",
            f"{queryset.count()} ta buyurtma yetkazildi.",
        )

    @action(description="Bekor qilish", icon="cancel")
    def mark_cancelled(self, request, queryset):
        self._bulk_status_update(
            request, queryset, "cancelled",
            f"{queryset.count()} ta buyurtma bekor qilindi.",
        )

    @display(description="Mahsulotlar")
    def display_items_count(self, obj):
        count = obj.items.count()
        return format_html(
            '<span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">{} ta</span>',
            count,
        )

    def save_model(self, request, obj, form, change):
        """Holat o'zgarganda foydalanuvchiga Telegram xabar yuborish."""
        if change and "status" in form.changed_data:
            super().save_model(request, obj, form, change)
            try:
                send_status_notification(obj, obj.status)
            except Exception:
                pass
        else:
            super().save_model(request, obj, form, change)

    @display(description="Manzil")
    def display_address(self, obj):
        if obj.delivery_address:
            addr = obj.delivery_address
            short = addr[:25] + "..." if len(addr) > 25 else addr
            return format_html('<span class="text-xs">{}</span>', short)
        return format_html('<span class="text-gray-400 text-xs">Ko\'rsatilmagan</span>')
