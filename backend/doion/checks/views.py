from django.db import IntegrityError
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from doion.checks.models import ChequeListing
from doion.checks.models import IssuerProfile
from doion.checks.serializers import (
    ChequeListingCreateSerializer,
    ChequeListingSerializer,
    DocumentUploadSerializer,
    IssuerProfileSerializer)
from doion.core.permissions import IsCheckHolder


class IsListingOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IssuerProfileViewSet(ModelViewSet):
    serializer_class = IssuerProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = IssuerProfile.objects.all()


class ChequeListingViewSet(ModelViewSet):
    serializer_class = ChequeListingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.profile.role in ["moderator", "admin"]:
            return ChequeListing.objects.all()
        return ChequeListing.objects.filter(owner=user)

    def get_serializer_class(self):
        if self.action == "create":
            return ChequeListingCreateSerializer
        return ChequeListingSerializer

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            raise serializers.ValidationError(
                {
                    "cheque_serial_number": [
                        "A listing with this cheque serial number already exists for this issuer and bank"
                    ]
                }
            )

    def update(self, request, *args, **kwargs):
        listing = self.get_object()
        if listing.status not in [ChequeListing.Status.PENDING_MODERATION, ChequeListing.Status.REJECTED]:
            return Response(
                {"error": {"code": "PERMISSION_ERROR", "message": "Listing cannot be modified in current status"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if listing.owner != request.user:
            return Response(
                {"error": {"code": "PERMISSION_ERROR", "message": "Only owner can edit listing"}},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="my")
    def my_listings(self, request):
        queryset = ChequeListing.objects.filter(owner=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="documents")
    def upload_document(self, request, pk=None):
        listing = self.get_object()
        if listing.owner != request.user:
            return Response(
                {"error": {"code": "PERMISSION_ERROR", "message": "Only owner can upload documents"}},
                status=status.HTTP_403_FORBIDDEN,
            )
        parser_classes = (MultiPartParser, FormParser)
        serializer = DocumentUploadSerializer(data=request.data, context={"listing": listing})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
