from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from doion.compliance.views import AuditEventViewSet
from doion.compliance.views import ComplianceStatsView
from doion.compliance.views import FeatureFlagViewSet

router = DefaultRouter()
router.register("feature-flags", FeatureFlagViewSet, basename="feature-flag")

app_name = "compliance"

urlpatterns = [
    path(
        "compliance/",
        include([
            path("", include(router.urls)),
            path("stats/", ComplianceStatsView.as_view({"get": "list"}), name="stats"),
            path("audit/", AuditEventViewSet.as_view({"get": "list"}), name="audit-list"),
        ]),
    ),
]
