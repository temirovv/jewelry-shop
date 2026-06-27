from rest_framework import viewsets, permissions

from .models import Region, DeliveryZone
from .serializers import RegionSerializer, DeliveryZoneSerializer


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    """Faol viloyatlar ro'yxati (zonalari bilan)."""

    queryset = (
        Region.objects.filter(is_active=True)
        .prefetch_related("zones")
        .order_by("ordering", "name")
    )
    serializer_class = RegionSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class DeliveryZoneViewSet(viewsets.ReadOnlyModelViewSet):
    """Yetkazish zonalari. ?region=ID filterini qo'llab-quvvatlaydi."""

    serializer_class = DeliveryZoneSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        qs = DeliveryZone.objects.filter(is_active=True).select_related("region")
        region_id = self.request.query_params.get("region")
        if region_id:
            qs = qs.filter(region_id=region_id)
        return qs.order_by("region__ordering", "ordering", "name")
