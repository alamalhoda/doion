from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from doion.checks.models import ChequeListing
from doion.core.permissions import IsModerator
from doion.moderation.exceptions import ModerationResubmitLimitExceeded
from doion.moderation.models import ModerationDecision
from doion.moderation.serializers import (
    DecisionRequestSerializer,
    ModerationDecisionSerializer,
    QueueListingSerializer,
)
from doion.moderation.services import ModerationService


class ModerationViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated, IsModerator]
    queryset = ChequeListing.objects.all()

    @action(detail=False, methods=["get"], url_path="queue")
    def queue(self, request):
        queryset = ChequeListing.objects.filter(
            status=ChequeListing.Status.PENDING_MODERATION
        ).order_by("created_at")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = QueueListingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = QueueListingSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="decision")
    def decision(self, request, pk=None):
        listing = self.get_object()

        input_serializer = DecisionRequestSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        decision_val = input_serializer.validated_data["decision"]
        rejection_code = input_serializer.validated_data.get("rejection_code")
        rejection_note = input_serializer.validated_data.get("rejection_note", "")

        decision_map = {
            "approve": ModerationDecision.Decision.APPROVED,
            "reject": ModerationDecision.Decision.REJECTED,
        }
        model_decision = decision_map.get(decision_val, decision_val)

        try:
            if decision_val == "approve":
                ModerationService.approve_listing(listing.id, request.user)
            else:
                if not rejection_code:
                    raise serializers.ValidationError(
                        {"rejection_code": "This field is required for rejection."}
                    )
                ModerationService.reject_listing(
                    listing.id, request.user, rejection_code, rejection_note
                )
        except ValueError as exc:
            raise serializers.ValidationError(
                {"error": {"code": "VALIDATION_ERROR", "message": str(exc)}}
            ) from exc

        decision_record = ModerationDecision.objects.create(
            listing=listing,
            moderator=request.user,
            decision=model_decision,
            rejection_code=rejection_code if decision_val == "reject" else None,
            rejection_note=rejection_note,
        )

        return Response(
            ModerationDecisionSerializer(decision_record).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"], url_path="resubmit")
    def resubmit(self, request, pk=None):
        listing = self.get_object()

        if listing.status != ChequeListing.Status.REJECTED:
            return Response(
                {"error": {"code": "VALIDATION_ERROR", "message": "Only rejected listings can be resubmitted"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if listing.resubmit_count >= 3:
            raise ModerationResubmitLimitExceeded()

        listing.status = ChequeListing.Status.PENDING_MODERATION
        listing.save(update_fields=["status", "updated_at"])

        return Response(QueueListingSerializer(listing).data)
