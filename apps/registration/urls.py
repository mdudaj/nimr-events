# -*- encoding: utf-8 -*-

from django.urls import include, path

urlpatterns = [
    path("accounts/", include("allauth.urls")),
]
