from django.urls import path
from . import views

urlpatterns = [
    path("delivery/regions/", views.regions_list, name="delivery-regions"),
    path("delivery/cities/", views.cities_list, name="delivery-cities"),
    path("delivery/calculate/", views.calculate_delivery, name="delivery-calculate"),
]
