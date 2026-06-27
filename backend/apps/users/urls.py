from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("favorites", views.FavoriteViewSet, basename="favorite")

urlpatterns = [
    path("me/", views.get_current_user, name="current-user"),
    path("me/update/", views.update_current_user, name="update-user"),
    path("", include(router.urls)),
]
