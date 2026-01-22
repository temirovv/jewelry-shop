from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.get_cart, name="cart"),
    path("cart/add/", views.add_to_cart, name="cart-add"),
    path("cart/items/<int:item_id>/", views.update_cart_item, name="cart-update"),
    path("cart/items/<int:item_id>/remove/", views.remove_from_cart, name="cart-remove"),
    path("cart/clear/", views.clear_cart, name="cart-clear"),
]
