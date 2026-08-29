from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from doion.marketplace.views import MarketplaceViewSet

app_name = "marketplace"

router = DefaultRouter()
router.register("listings", MarketplaceViewSet, basename="listing")

urlpatterns = [
    path("marketplace/", include(router.urls)),
]
