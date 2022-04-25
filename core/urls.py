# -*- encoding: utf-8 -*-

# from django.conf import settings
# from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.registration.urls")),
    path("", include("apps.ajsc.urls")),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
