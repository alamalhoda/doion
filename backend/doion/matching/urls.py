from django.urls import include, path
from rest_framework.routers import DefaultRouter

from doion.matching.views import MatchViewSet

router = DefaultRouter()
router.register(r"matches", MatchViewSet, basename="match")

app_name = "matching"
urlpatterns = [
    path("", include(router.urls)),
]
