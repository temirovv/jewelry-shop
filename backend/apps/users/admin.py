from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum
from unfold.admin import ModelAdmin
from unfold.decorators import display, action
from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(ModelAdmin):
    list_display = [
        "display_avatar",
        "display_name",
        "username",
        "phone",
        "display_orders_count",
        "display_total_spent",
        "display_language",
        "display_status",
        "created_at",
    ]
    list_display_links = ["display_avatar", "display_name"]
    list_filter = ["is_active", "language", "created_at"]
    search_fields = ["first_name", "last_name", "username", "phone", "telegram_id"]
    readonly_fields = ["telegram_id", "created_at", "updated_at"]
    ordering = ["-created_at"]
    list_filter_submit = True
    date_hierarchy = "created_at"
    list_per_page = 25
    actions = ["activate_users", "deactivate_users"]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count("orders"),
            total_spent=Sum("orders__total"),
        )

    fieldsets = (
        ("Telegram Ma'lumotlari", {
            "fields": ("telegram_id", "first_name", "last_name", "username"),
            "classes": ["tab"],
        }),
        ("Aloqa", {
            "fields": ("phone",),
            "classes": ["tab"],
        }),
        ("Sozlamalar", {
            "fields": ("language", "is_active"),
            "classes": ["tab"],
        }),
        ("Vaqt", {
            "fields": ("created_at", "updated_at"),
            "classes": ["tab"],
        }),
    )

    @display(description="Avatar")
    def display_avatar(self, obj):
        initials = (obj.first_name[0] if obj.first_name else "?").upper()
        colors = ["amber", "blue", "green", "purple", "pink", "indigo"]
        color = colors[obj.telegram_id % len(colors)]
        return format_html(
            '<div class="flex items-center justify-center w-10 h-10 rounded-full bg-{}-100 text-{}-600 font-semibold">{}</div>',
            color, color, initials
        )

    @display(description="Ism")
    def display_name(self, obj):
        full_name = f"{obj.first_name or ''} {obj.last_name or ''}".strip()
        return format_html(
            '<div><span class="font-medium">{}</span>'
            '<br><span class="text-xs text-gray-400">ID: {}</span></div>',
            full_name or "Noma'lum",
            obj.telegram_id
        )

    @display(
        description="Til",
        label={
            "uz": "primary",
            "ru": "info",
        },
    )
    def display_language(self, obj):
        return obj.language

    @display(description="Buyurtmalar", ordering="orders_count")
    def display_orders_count(self, obj):
        count = getattr(obj, "orders_count", 0)
        if count > 0:
            return format_html(
                '<span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">{} ta</span>',
                count,
            )
        return format_html('<span class="text-gray-400">0</span>')

    @display(description="Jami xarid", ordering="total_spent")
    def display_total_spent(self, obj):
        total = getattr(obj, "total_spent", None)
        if total is not None and total > 0:
            formatted = f"{int(total):,}".replace(",", " ")
            return format_html(
                '<span class="font-semibold">{} so\'m</span>',
                formatted,
            )
        return "—"

    @display(
        description="Holat",
        label={True: "success", False: "danger"},
    )
    def display_status(self, obj):
        return obj.is_active

    @action(description="Faollashtirish", icon="check_circle")
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} ta foydalanuvchi faollashtirildi.")

    @action(description="O'chirish", icon="block")
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} ta foydalanuvchi o'chirildi.")
