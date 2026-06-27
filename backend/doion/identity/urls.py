from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from doion.identity.api.views import ProfileViewSet
from doion.identity.api.views import RegisterViewSet
from doion.identity.api.views import UserMeViewSet

app_name = "identity"

router = DefaultRouter()
router.register("register", RegisterViewSet, basename="register")
router.register("me", UserMeViewSet, basename="me")
router.register("profile", ProfileViewSet, basename="profile")

urlpatterns = [
    path("identity/", include(router.urls)),
]
