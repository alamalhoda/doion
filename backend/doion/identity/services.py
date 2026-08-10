"""Identity domain services."""

from __future__ import annotations

from typing import Any

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from rest_framework.exceptions import PermissionDenied

from doion.documents.models import Document
from doion.identity.models import Profile
from doion.identity.models import Verification
from doion.users.models import User

KYC_REQUIRED_MESSAGE = "Approved KYC verification is required before this action"

NATURAL_NATIONAL_ID_LENGTH = 10
LEGAL_NATIONAL_ID_LENGTH = 11


def user_has_approved_kyc(user: AbstractBaseUser) -> bool:
    """Return True when the user has at least one approved verification."""
    if not user or not getattr(user, "is_authenticated", False):
        return False
    return Verification.objects.filter(
        user=user,
        status=Verification.Status.APPROVED,
    ).exists()


def require_approved_kyc(user: AbstractBaseUser) -> None:
    """Raise PermissionDenied when the user lacks an approved KYC verification."""
    if not user_has_approved_kyc(user):
        raise PermissionDenied(KYC_REQUIRED_MESSAGE)


def get_or_create_profile(user: User) -> Profile:
    """Return the user's profile, creating a natural-person default if missing."""
    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={
            "role": user.role or Profile.Role.CHECK_HOLDER,
            "user_type": Profile.UserType.NATURAL,
        },
    )
    return profile


class RegisterService:
    """Create a User, Profile, and auth group atomically."""

    def execute(self, validated_data: dict[str, Any]) -> User:
        role = validated_data["role"]
        user_type = validated_data["user_type"]
        password = validated_data["password"]

        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data.get("email", ""),
                password=password,
                name=validated_data.get("name", ""),
                phone=validated_data.get("phone", ""),
                role=role,
            )
            Profile.objects.create(
                user=user,
                role=role,
                user_type=user_type,
            )
            group_name = "Investor" if role == "investor" else "CheckHolder"
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        return user


class CreateVerificationService:
    """Create a Verification record and attached identity documents."""

    def execute(
        self,
        *,
        user: User,
        validated_data: dict[str, Any],
    ) -> Verification:
        front: UploadedFile = validated_data.pop("national_id_front")
        back: UploadedFile = validated_data.pop("national_id_back")
        selfie: UploadedFile | None = validated_data.pop("selfie", None)

        with transaction.atomic():
            verification = Verification.objects.create(user=user, **validated_data)

            Document.objects.create(
                owner=user,
                related_object_type="verification",
                related_object_id=verification.id,
                document_type=Document.DocumentType.NATIONAL_ID_FRONT,
                file=front,
                file_size=front.size,
            )
            Document.objects.create(
                owner=user,
                related_object_type="verification",
                related_object_id=verification.id,
                document_type=Document.DocumentType.NATIONAL_ID_BACK,
                file=back,
                file_size=back.size,
            )
            if selfie:
                Document.objects.create(
                    owner=user,
                    related_object_type="verification",
                    related_object_id=verification.id,
                    document_type=Document.DocumentType.SELFIE,
                    file=selfie,
                    file_size=selfie.size,
                )

            from doion.identity.signals import verification_submitted

            verification_submitted.send(
                sender=self.__class__,
                verification=verification,
            )

        return verification
