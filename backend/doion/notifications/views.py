from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from doion.notifications.constants import NotificationStatus
from doion.notifications.models import Notification
from doion.notifications.models import NotificationPreference
from doion.notifications.serializers import NotificationMarkReadSerializer
from doion.notifications.serializers import NotificationPreferenceSerializer
from doion.notifications.serializers import NotificationSerializer


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["type", "status"]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")

    def get_filter_for_is_read(self, queryset):
        is_read = self.request.query_params.get("is_read")
        if is_read is not None:
            is_read_val = is_read.lower() == "true"
            if is_read_val:
                return queryset.filter(status=NotificationStatus.READ)
            return queryset.exclude(status=NotificationStatus.READ)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = self.get_filter_for_is_read(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data["unread_count"] = self.get_queryset().exclude(
                status=NotificationStatus.READ,
            ).count()
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = NotificationMarkReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get("is_read"):
            instance.status = NotificationStatus.READ
            instance.read_at = timezone.now()
            instance.save(update_fields=["status", "read_at"])

        return Response(NotificationSerializer(instance).data)

    @action(detail=False, methods=["post"], url_path="mark-all-read")
    def mark_all_read(self, request):
        updated = self.get_queryset().exclude(status=NotificationStatus.READ).update(
            status=NotificationStatus.READ,
            read_at=timezone.now(),
        )
        return Response(
            {"message": f"{updated} notifications marked as read"},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get", "patch"], url_path="preferences")
    def preferences(self, request):
        preference, _ = NotificationPreference.objects.get_or_create(user=request.user)

        if request.method == "GET":
            serializer = NotificationPreferenceSerializer(preference)
            return Response(serializer.data)

        serializer = NotificationPreferenceSerializer(
            preference, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
