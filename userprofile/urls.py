"""Urls for userprofile app."""

from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import ProfileViewSet


router = DefaultRouter(trailing_slash=False)
router.register('', ProfileViewSet, basename="profile")

urlpatterns = [path("", include(router.urls))]
