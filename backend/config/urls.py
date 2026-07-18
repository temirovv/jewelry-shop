from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.orders.report_views import financial_report_view

urlpatterns = [
    # Admin include'dan OLDIN — aks holda admin/ uni ushlab qoladi
    path("admin/hisobot/", financial_report_view, name="financial_report"),
    path("admin/", admin.site.urls),
    path("api/", include("apps.products.urls")),
    path("api/", include("apps.orders.urls")),
    path("api/", include("apps.cart.urls")),
    path("api/users/", include("apps.users.urls")),
    path("api/delivery/", include("apps.delivery.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
