from django.urls import include, path
from rest_framework.routers import DefaultRouter
from doion.identity.api.views import (
    ModerationVerificationDecisionView,
    ModerationVerificationListView,
    VerificationViewSet,
)

router = DefaultRouter()
router.register("verifications", VerificationViewSet, basename="verification")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "moderation/kyc/",
        ModerationVerificationListView.as_view(),
        name="moderation-kyc-list",
    ),
    path(
        "moderation/kyc/<int:pk>/decision/",
        ModerationVerificationDecisionView.as_view(),
        name="moderation-kyc-decision",
    ),
]
