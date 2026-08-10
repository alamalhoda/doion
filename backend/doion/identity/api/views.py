from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from doion.identity.api.serializers import (
    ProfileSerializer,
    RegisterSerializer,
    UserMeSerializer,
    VerificationCreateSerializer,
    VerificationSerializer,
)
from doion.identity.api.permissions import IsModerator
from doion.identity.models import Verification
from doion.users.models import User


class RegisterViewSet(GenericViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "register"

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "name": user.name,
                    "role": user.role,
                    "user_type": user.profile.user_type,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class ProfileViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        from doion.identity.services import get_or_create_profile

        return get_or_create_profile(self.request.user)


class UserMeViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserMeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        from doion.identity.services import get_or_create_profile

        get_or_create_profile(self.request.user)
        return self.request.user


class VerificationViewSet(ModelViewSet):
    serializer_class = VerificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Verification.objects.select_related("user", "user__profile")
        if self.request.user.profile.role in ["moderator", "admin"]:
            return qs.all()
        return qs.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return VerificationCreateSerializer
        return VerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        verification = serializer.save()
        output = VerificationSerializer(
            verification,
            context=self.get_serializer_context(),
        )
        return Response(output.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="me")
    def my_verification(self, request):
        verification = Verification.objects.filter(user=request.user).order_by(
            "-created_at"
        ).first()
        if not verification:
            return Response(
                {"detail": "No verification found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(verification)
        return Response(serializer.data)


class ModerationVerificationListView(APIView):
    permission_classes = [IsModerator]

    def get(self, request):
        verifications = (
            Verification.objects.filter(status=Verification.Status.PENDING)
            .select_related("user", "user__profile")
            .order_by("created_at")
        )
        serializer = VerificationSerializer(verifications, many=True)
        return Response(serializer.data)


class ModerationVerificationDecisionView(APIView):
    permission_classes = [IsModerator]

    def post(self, request, pk):
        verification = get_object_or_404(Verification, pk=pk)
        decision = request.data.get("decision")
        rejection_code = request.data.get("rejection_code")
        rejection_note = request.data.get("rejection_note", "")

        if decision == "approve":
            verification.status = Verification.Status.APPROVED
            verification.rejection_reason = ""
            verification.rejection_code = ""
            verification.save()

            from doion.identity.signals import verification_approved
            verification_approved.send(
                sender=self.__class__, verification=verification
            )
            return Response({"status": "approved"})

        if decision == "reject":
            if not rejection_code:
                return Response(
                    {"error": "rejection_code is required for rejection"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            verification.status = Verification.Status.REJECTED
            verification.rejection_reason = rejection_note
            verification.rejection_code = rejection_code
            verification.save()

            from doion.identity.signals import verification_rejected
            verification_rejected.send(
                sender=self.__class__,
                verification=verification,
                rejection_code=rejection_code,
                rejection_note=rejection_note,
            )
            return Response({"status": "rejected"})

        return Response(
            {"error": "Invalid decision. Must be approve or reject"},
            status=status.HTTP_400_BAD_REQUEST,
        )
