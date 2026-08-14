from django.utils import timezone

from django.db.models import Count, Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.pagination import PageNumberPagination

from doion.checks.models import ChequeListing
from doion.compliance.models import AuditEvent
from doion.compliance.models import FeatureFlag
from doion.compliance.permissions import IsModeratorOrAdmin
from doion.compliance.serializers import AuditEventSerializer
from doion.compliance.serializers import FeatureFlagSerializer
from doion.identity.models import Verification
from doion.notifications.constants import NotificationStatus
from doion.notifications.models import Notification
from doion.users.models import User


class StandardResultPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class FeatureFlagViewSet(ModelViewSet):
    queryset = FeatureFlag.objects.all()
    serializer_class = FeatureFlagSerializer
    permission_classes = [IsModeratorOrAdmin]
    lookup_field = "key"
    lookup_url_kwarg = "key"

    def get_permissions(self):
        # Public clients need display flags such as show_risk_tier.
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsModeratorOrAdmin()]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_system:
            return Response(
                {
                    "error": {
                        "code": "PERMISSION_ERROR",
                        "message": "System flags cannot be modified via API.",
                    }
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_path="toggle")
    def toggle(self, request, key=None):
        instance = self.get_object()
        if instance.is_system:
            return Response(
                {
                    "error": {
                        "code": "PERMISSION_ERROR",
                        "message": "System flags cannot be toggled via API.",
                    }
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        instance.is_enabled = not instance.is_enabled
        instance.save(update_fields=["is_enabled"])
        return Response(FeatureFlagSerializer(instance).data)


class ComplianceStatsView(GenericViewSet):
    permission_classes = [IsModeratorOrAdmin]
    pagination_class = None

    def list(self, request, *args, **kwargs):
        today = timezone.now().date()
        listings = ChequeListing.objects.aggregate(
            total=Count("id"),
            published=Count("id", filter=Q(status=ChequeListing.Status.PUBLISHED)),
            pending_moderation=Count(
                "id", filter=Q(status=ChequeListing.Status.PENDING_MODERATION)
            ),
            rejected=Count("id", filter=Q(status=ChequeListing.Status.REJECTED)),
            expired=Count("id", filter=Q(status=ChequeListing.Status.EXPIRED)),
            matched=Count("id", filter=Q(status=ChequeListing.Status.MATCHED)),
        )
        users = User.objects.aggregate(
            total=Count("id"),
            kyc_pending=Count("id", filter=Q(verifications__status=Verification.Status.PENDING)),
            kyc_approved=Count("id", filter=Q(verifications__status=Verification.Status.APPROVED)),
        )
        verifications = Verification.objects.aggregate(
            pending=Count("id", filter=Q(status=Verification.Status.PENDING)),
        )
        notifications = Notification.objects.aggregate(
            unread=Count(
                "id",
                filter=~Q(
                    status__in=[NotificationStatus.READ, NotificationStatus.FAILED]
                ),
            ),
        )
        return Response(
            {
                "listings": listings,
                "users": users,
                "verifications": verifications,
                "notifications": notifications,
            }
        )


class AuditEventViewSet(ModelViewSet):
    queryset = AuditEvent.objects.all().order_by("-created_at")
    serializer_class = AuditEventSerializer
    permission_classes = [IsModeratorOrAdmin]
    pagination_class = StandardResultPagination
    http_method_names = ["get", "head"]
