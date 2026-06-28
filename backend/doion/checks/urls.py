from django.urls import include, path
from rest_framework.routers import DefaultRouter

from doion.checks.views import ChequeListingViewSet
from doion.checks.views import IssuerProfileViewSet

router = DefaultRouter()
router.register("listings", ChequeListingViewSet, basename="listing")
router.register("issuer-profiles", IssuerProfileViewSet, basename="issuer-profile")

urlpatterns = [
    path("", include(router.urls)),
]
