from rest_framework import serializers

from .models import Region, DeliveryZone


class DeliveryZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryZone
        fields = [
            "id",
            "region",
            "name",
            "fee",
            "free_threshold",
            "estimated_days",
        ]


class RegionSerializer(serializers.ModelSerializer):
    zones = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = ["id", "name", "zones"]

    def get_zones(self, obj):
        zones = obj.zones.filter(is_active=True).order_by("ordering", "name")
        return DeliveryZoneSerializer(zones, many=True).data
