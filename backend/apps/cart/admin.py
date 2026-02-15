from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display, action
from .models import Cart, CartItem


class CartItemInline(TabularInline):
    model = CartItem
    extra = 0
    raw_id_fields = ["product"]
    fields = ["display_product", "product", "quantity", "size", "display_subtotal"]
    readonly_fields = ["display_product", "display_subtotal"]
    tab = True

    @display(description="Mahsulot")
    def display_product(self, obj):
        if obj.product:
            return format_html(
                '<span class="font-medium">{}</span>'
                '<br><span class="text-xs text-gray-400">{:,.0f} so\'m</span>',
                obj.product.name,
                obj.product.price,
            )
        return "—"

    @display(description="Jami")
    def display_subtotal(self, obj):
        if obj.pk and obj.product:
            return format_html(
                '<span class="font-semibold">{:,.0f} so\'m</span>',
                obj.subtotal,
            )
        return "—"


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ["display_user", "display_items_count", "display_total", "display_status", "updated_at"]
    list_display_links = ["display_user"]
    inlines = [CartItemInline]
    readonly_fields = ["created_at", "updated_at"]
    search_fields = ["user__first_name", "user__username", "user__telegram_id"]
    list_filter_submit = True
    date_hierarchy = "updated_at"
    list_per_page = 20
    actions = ["clear_carts", "delete_empty_carts"]

    @display(description="Foydalanuvchi")
    def display_user(self, obj):
        if obj.user:
            return format_html(
                '<div><span class="font-medium">{}</span>'
                '<br><span class="text-xs text-gray-400">@{}</span></div>',
                obj.user.first_name or "Noma'lum",
                obj.user.username or obj.user.telegram_id,
            )
        return "—"

    @display(description="Mahsulotlar")
    def display_items_count(self, obj):
        count = obj.items_count
        if count > 0:
            return format_html(
                '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">{} ta</span>',
                count,
            )
        return format_html('<span class="text-gray-400">Bo\'sh</span>')

    @display(description="Jami")
    def display_total(self, obj):
        total = obj.total
        if total > 0:
            return format_html(
                '<span class="font-semibold">{:,.0f} so\'m</span>',
                total,
            )
        return "—"

    @display(description="Holat")
    def display_status(self, obj):
        if obj.items_count > 0:
            return format_html(
                '<span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">Faol</span>'
            )
        return format_html(
            '<span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">Bo\'sh</span>'
        )

    @action(description="Savatlarni tozalash", icon="delete_sweep")
    def clear_carts(self, request, queryset):
        count = 0
        for cart in queryset:
            count += cart.items.count()
            cart.items.all().delete()
        self.message_user(request, f"{count} ta element {queryset.count()} ta savatdan o'chirildi.")

    @action(description="Bo'sh savatlarni o'chirish", icon="cleaning_services")
    def delete_empty_carts(self, request, queryset):
        empty = [c.pk for c in queryset if c.items_count == 0]
        deleted = Cart.objects.filter(pk__in=empty).delete()[0]
        self.message_user(request, f"{deleted} ta bo'sh savat o'chirildi.")
