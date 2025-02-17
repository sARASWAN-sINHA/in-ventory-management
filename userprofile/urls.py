"""Urls for userprofile app."""

from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import ProfileViewSet, SetUserToGroupView


router = DefaultRouter(trailing_slash=False)
router.register("profile", ProfileViewSet, basename="profile")
router.register("set", SetUserToGroupView, basename="set-group")


urlpatterns = [
    path("", include(router.urls)),
]
