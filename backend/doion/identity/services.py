"""Identity domain services."""

from __future__ import annotations

from django.contrib.auth.models import AbstractBaseUser
from rest_framework.exceptions import PermissionDenied

from doion.identity.models import Verification

KYC_REQUIRED_MESSAGE = "Approved KYC verification is required before this action"


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
