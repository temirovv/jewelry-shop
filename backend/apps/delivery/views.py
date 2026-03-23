import logging

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .bts_client import BTSAPIError
from .models import BTSRegion, BTSCity
from .serializers import BTSRegionSerializer, BTSCitySerializer, DeliveryCalculateSerializer
from .services import calculate_delivery_cost

logger = logging.getLogger(__name__)


@api_view(["GET"])
@permission_classes([AllowAny])
def regions_list(request):
    """GET /api/delivery/regions/ — BTS viloyatlar ro'yxati."""
    regions = BTSRegion.objects.all()
    serializer = BTSRegionSerializer(regions, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def cities_list(request):
    """GET /api/delivery/cities/?region=X — BTS shaharlar ro'yxati."""
    region_bts_id = request.query_params.get("region")
    if not region_bts_id:
        return Response(
            {"error": "region parametri talab qilinadi"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    cities = BTSCity.objects.filter(region__bts_id=region_bts_id)
    serializer = BTSCitySerializer(cities, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def calculate_delivery(request):
    """POST /api/delivery/calculate/ — BTS narx hisoblash."""
    serializer = DeliveryCalculateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        result = calculate_delivery_cost(
            region_id=serializer.validated_data["region_id"],
            city_id=serializer.validated_data["city_id"],
        )
        return Response(result)
    except BTSAPIError as e:
        logger.error(f"BTS API error: {e}")
        return Response(
            {"error": f"BTS xatolik: {e}"},
            status=status.HTTP_502_BAD_GATEWAY,
        )
    except Exception as e:
        logger.error(f"BTS delivery calculation failed: {e}")
        return Response(
            {"error": "Yetkazib berish narxini hisoblashda kutilmagan xatolik"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
