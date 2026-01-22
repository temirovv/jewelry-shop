from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from .models import Cart, CartItem


class CartItemInline(TabularInline):
    model = CartItem
    extra = 0
    raw_id_fields = ["product"]
    fields = ["display_product", "product", "quantity", "size"]
    readonly_fields = ["display_product"]
    tab = True

    @display(description="Mahsulot")
    def display_product(self, obj):
        if obj.product:
            return format_html(
                '<span class="font-medium">{}</span>'
                '<br><span class="text-xs text-gray-400">{:,.0f} so\'m</span>',
                obj.product.name,
                obj.product.price
            )
        return "—"


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ["display_user", "display_items_count", "display_total", "updated_at"]
    list_display_links = ["display_user"]
    inlines = [CartItemInline]
    readonly_fields = ["created_at", "updated_at"]
    search_fields = ["user__first_name", "user__username", "user__telegram_id"]
    list_filter_submit = True
    date_hierarchy = "updated_at"

    @display(description="Foydalanuvchi")
    def display_user(self, obj):
        if obj.user:
            return format_html(
                '<div><span class="font-medium">{}</span>'
                '<br><span class="text-xs text-gray-400">@{}</span></div>',
                obj.user.first_name or "Noma'lum",
                obj.user.username or obj.user.telegram_id
            )
        return "—"

    @display(description="Mahsulotlar")
    def display_items_count(self, obj):
        count = obj.items_count
        if count > 0:
            return format_html(
                '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">{} ta</span>',
                count
            )
        return format_html(
            '<span class="text-gray-400">Bo\'sh</span>'
        )

    @display(description="Jami")
    def display_total(self, obj):
        total = obj.total
        if total > 0:
            return format_html(
                '<span class="font-semibold">{:,.0f} so\'m</span>',
                total
            )
        return "—"
