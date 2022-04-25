from xml.etree.ElementInclude import include

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.registration.urls")),
    path("", include("apps.ajsc.urls")),
]
