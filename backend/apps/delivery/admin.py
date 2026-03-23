from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import BTSRegion, BTSCity, BTSBranch


@admin.register(BTSRegion)
class BTSRegionAdmin(ModelAdmin):
    list_display = ["bts_id", "name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(BTSCity)
class BTSCityAdmin(ModelAdmin):
    list_display = ["bts_id", "name", "region"]
    list_filter = ["region"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(BTSBranch)
class BTSBranchAdmin(ModelAdmin):
    list_display = ["bts_id", "name", "city", "address"]
    list_filter = ["city__region"]
    search_fields = ["name", "address"]
    ordering = ["name"]
