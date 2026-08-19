from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from doion.banks.views import BankViewSet
from doion.checks.api.urls import urlpatterns as checks_urlpatterns
from doion.compliance.urls import urlpatterns as compliance_urlpatterns
from doion.identity.api.urls import urlpatterns as verification_urlpatterns
from doion.identity.urls import urlpatterns as identity_urls
from doion.integrations.urls import urlpatterns as integrations_urlpatterns
from doion.marketplace.urls import urlpatterns as marketplace_urlpatterns
from doion.matching.urls import urlpatterns as matching_urlpatterns
from doion.moderation.urls import urlpatterns as moderation_urlpatterns
from doion.notifications.urls import urlpatterns as notifications_urlpatterns
from doion.users.api.views import LoginViewSet
from doion.users.api.views import RefreshViewSet
from doion.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("banks", BankViewSet, basename="bank")
router.register("auth/login", LoginViewSet, basename="login")
router.register("auth/refresh", RefreshViewSet, basename="refresh")

urlpatterns = (
    router.urls
    + identity_urls
    + verification_urlpatterns
    + checks_urlpatterns
    + marketplace_urlpatterns
    + matching_urlpatterns
    + moderation_urlpatterns
    + notifications_urlpatterns
    + integrations_urlpatterns
    + compliance_urlpatterns
)
