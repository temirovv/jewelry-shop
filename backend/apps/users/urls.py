from django.urls import path
from . import views

urlpatterns = [
    path("me/", views.get_current_user, name="current-user"),
    path("me/update/", views.update_current_user, name="update-user"),
]
