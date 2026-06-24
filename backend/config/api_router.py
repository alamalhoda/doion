from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from doion.users.api.views import LoginViewSet
from doion.users.api.views import RefreshViewSet
from doion.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("auth/login", LoginViewSet, basename="login")
router.register("auth/refresh", RefreshViewSet, basename="refresh")

app_name = "api"
urlpatterns = router.urls
