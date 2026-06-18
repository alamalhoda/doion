from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from doion.users.api.views import LoginViewSet, UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("login", LoginViewSet, basename="login")

app_name = "api"
urlpatterns = router.urls