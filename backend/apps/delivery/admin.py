from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display

from .models import Region, DeliveryZone


class DeliveryZoneInline(TabularInline):
    model = DeliveryZone
    extra = 0
    fields = ["name", "fee", "free_threshold", "estimated_days", "is_active", "ordering"]
    tab = True


@admin.register(Region)
class RegionAdmin(ModelAdmin):
    list_display = ["name", "display_zones_count", "is_active", "ordering"]
    list_editable = ["ordering", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]
    ordering = ["ordering", "name"]
    inlines = [DeliveryZoneInline]

    @display(description="Zonalar")
    def display_zones_count(self, obj):
        return format_html(
            '<span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs '
            'font-medium bg-primary-100 text-primary-800">{} ta</span>',
            obj.zones.count(),
        )


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(ModelAdmin):
    list_display = [
        "name",
        "region",
        "display_fee",
        "display_free_threshold",
        "estimated_days",
        "is_active",
    ]
    list_editable = ["is_active"]
    list_filter = ["region", "is_active"]
    search_fields = ["name", "region__name"]
    ordering = ["region__ordering", "ordering", "name"]
    autocomplete_fields = ["region"]

    @display(description="Narx", ordering="fee")
    def display_fee(self, obj):
        if obj.fee and obj.fee > 0:
            formatted = f"{obj.fee:,.0f}".replace(",", " ")
            return format_html('<span class="font-medium">{} so\'m</span>', formatted)
        return format_html('<span class="text-green-600">Bepul</span>')

    @display(description="Bepul chegara", ordering="free_threshold")
    def display_free_threshold(self, obj):
        if obj.free_threshold and obj.free_threshold > 0:
            formatted = f"{obj.free_threshold:,.0f}".replace(",", " ")
            return format_html('<span class="text-xs">{} so\'m</span>', formatted)
        return format_html('<span class="text-gray-400 text-xs">—</span>')
