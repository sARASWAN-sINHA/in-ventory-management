from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import AssetTypeViewSet, AssetViewSet

router = DefaultRouter(trailing_slash=False)
router.register("asset-type", AssetTypeViewSet, basename="asset-type")
router.register("asset", AssetViewSet, basename="asset")

urlpatterns = [
    path("", include(router.urls)),
]