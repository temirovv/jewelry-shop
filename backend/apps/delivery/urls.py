from rest_framework.routers import DefaultRouter

from .views import RegionViewSet, DeliveryZoneViewSet

router = DefaultRouter()
router.register("regions", RegionViewSet, basename="region")
router.register("zones", DeliveryZoneViewSet, basename="zone")

urlpatterns = router.urls
