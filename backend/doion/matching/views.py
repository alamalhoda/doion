from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from doion.checks.models import ChequeListing
from doion.core.permissions import IsCheckHolder, IsInvestor
from doion.matching.constants import Status
from doion.matching.exceptions import InvalidMatchStatus, MatchNotAllowed
from doion.matching.models import Match
from doion.matching.serializers import (
    MatchCreateSerializer,
    MatchSerializer,
    MatchStatusUpdateSerializer,
)
from doion.matching.services import MatchingService


class MatchViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Match.objects.select_related("listing", "investor", "check_holder").all()
    serializer_class = MatchSerializer

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, "role", None)
        if role == "check_holder":
            return Match.objects.filter(check_holder=user).select_related("listing", "investor", "check_holder")
        if role == "investor":
            return Match.objects.filter(investor=user).select_related("listing", "investor", "check_holder")
        return Match.objects.none()

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="my")
    def my(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], url_path="status")
    def status(self, request, pk=None):
        match = self.get_object()
        serializer = MatchStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data
        match.status = validated["status"]
        if validated.get("final_discount_rate") is not None:
            match.final_discount_rate = validated["final_discount_rate"]
        if validated.get("terms") is not None:
            match.terms = validated["terms"]
        match.save(update_fields=["status", "final_discount_rate", "terms", "updated_at"])

        return Response(MatchSerializer(match).data)

    def create(self, request):
        serializer = MatchCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        listing_id = serializer.validated_data["listing_id"]
        message = serializer.validated_data.get("message", "")

        try:
            listing = ChequeListing.objects.select_for_update().get(id=listing_id)
        except ChequeListing.DoesNotExist as exc:
            raise MatchNotAllowed("Listing not found") from exc

        if getattr(request.user, "role", None) != "investor":
            raise MatchNotAllowed("Only investors can create matches")

        try:
            match = MatchingService.create_match(listing_id, request.user)
        except (MatchNotAllowed, InvalidMatchStatus) as exc:
            raise MatchNotAllowed(str(exc)) from exc

        if message:
            match.message = message
            match.save(update_fields=["message", "updated_at"])

        response_serializer = MatchSerializer(match)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="accept")
    def accept(self, request, pk=None):
        match = self.get_object()

        if getattr(request.user, "role", None) != "check_holder":
            raise MatchNotAllowed("Only check holders can accept matches")

        try:
            updated = MatchingService.accept_match(match.id, request.user)
        except (MatchNotAllowed, InvalidMatchStatus) as exc:
            raise MatchNotAllowed(str(exc)) from exc

        return Response(MatchSerializer(updated).data)

    @action(detail=True, methods=["post"], url_path="decline")
    def decline(self, request, pk=None):
        match = self.get_object()

        if getattr(request.user, "role", None) != "check_holder":
            raise MatchNotAllowed("Only check holders can decline matches")

        note = request.data.get("note", "")

        try:
            updated = MatchingService.decline_match(match.id, request.user, note)
        except (MatchNotAllowed, InvalidMatchStatus) as exc:
            raise MatchNotAllowed(str(exc)) from exc

        return Response(MatchSerializer(updated).data)

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel(self, request, pk=None):
        match = self.get_object()

        try:
            updated = MatchingService.cancel_match(match.id, request.user)
        except (MatchNotAllowed, InvalidMatchStatus) as exc:
            raise MatchNotAllowed(str(exc)) from exc

        return Response(MatchSerializer(updated).data)

    @action(detail=True, methods=["post"], url_path="confirm-off-platform")
    def confirm_off_platform(self, request, pk=None):
        match = self.get_object()

        if getattr(request.user, "role", None) != "check_holder":
            raise MatchNotAllowed("Only check holders can confirm settlement")

        try:
            updated = MatchingService.confirm_off_platform(match.id, request.user)
        except (MatchNotAllowed, InvalidMatchStatus) as exc:
            raise MatchNotAllowed(str(exc)) from exc

        return Response(MatchSerializer(updated).data)
