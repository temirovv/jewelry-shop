from rest_framework import serializers
from .models import BTSRegion, BTSCity


class BTSRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BTSRegion
        fields = ["id", "bts_id", "name"]


class BTSCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BTSCity
        fields = ["id", "bts_id", "name"]


class DeliveryCalculateSerializer(serializers.Serializer):
    region_id = serializers.IntegerField()
    city_id = serializers.IntegerField()
