from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["subtotal"]
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "total", "phone", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__first_name", "user__phone", "phone"]
    readonly_fields = ["total", "created_at", "updated_at"]
    inlines = [OrderItemInline]
    ordering = ["-created_at"]

    fieldsets = (
        (None, {"fields": ("user", "status")}),
        ("Aloqa", {"fields": ("phone", "delivery_address", "comment")}),
        ("Moliya", {"fields": ("total",)}),
        ("Vaqt", {"fields": ("created_at", "updated_at")}),
    )
