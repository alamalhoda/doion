from __future__ import annotations

import re
from typing import Any

from rest_framework import serializers

from doion.documents.models import Document
from doion.identity.models import Profile
from doion.identity.models import Verification
from doion.identity.services import LEGAL_NATIONAL_ID_LENGTH
from doion.identity.services import NATURAL_NATIONAL_ID_LENGTH
from doion.identity.services import CreateVerificationService
from doion.identity.services import RegisterService
from doion.identity.services import get_or_create_profile
from doion.users.models import User

DIGITS_ONLY_PATTERN = re.compile(r"^\d+$")


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True, default="")
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True, default="")
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True, default="")
    role = serializers.ChoiceField(choices=["check_holder", "investor"])
    user_type = serializers.ChoiceField(choices=Profile.UserType.choices)

    def validate_username(self, value: str) -> str:
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_phone(self, value: str) -> str:
        if value and User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )
        if attrs["user_type"] == Profile.UserType.LEGAL and not (attrs.get("name") or "").strip():
            raise serializers.ValidationError(
                {"name": "Company name is required for Legal Entities."}
            )
        return attrs

    def create(self, validated_data: dict[str, Any]) -> User:
        return RegisterService().execute(validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=False)
    name = serializers.CharField(source="user.name", required=False, allow_blank=True)
    phone = serializers.CharField(source="user.phone", required=False, allow_blank=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "email",
            "name",
            "phone",
            "role",
            "user_type",
            "bio",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "role",
            "user_type",
            "is_verified",
            "created_at",
            "updated_at",
        ]

    def update(self, instance: Profile, validated_data: dict[str, Any]) -> Profile:
        user_data = validated_data.pop("user", {})
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        if user_data:
            user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.role", read_only=True)
    user_type = serializers.CharField(source="profile.user_type", read_only=True)
    is_verified = serializers.BooleanField(source="profile.is_verified", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "name",
            "phone",
            "role",
            "user_type",
            "is_verified",
        ]
        read_only_fields = ["id", "role", "user_type", "is_verified"]

    def update(self, instance: User, validated_data: dict[str, Any]) -> User:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "document_type", "file", "file_size"]


class VerificationSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    user_type = serializers.CharField(source="user.profile.user_type", read_only=True)

    class Meta:
        model = Verification
        fields = [
            "id",
            "full_name",
            "national_id",
            "company_name",
            "user_type",
            "status",
            "rejection_reason",
            "rejection_code",
            "documents",
        ]
        read_only_fields = [
            "id",
            "user_type",
            "status",
            "rejection_reason",
            "rejection_code",
            "documents",
        ]


class VerificationCreateSerializer(serializers.ModelSerializer):
    national_id_front = serializers.FileField(write_only=True)
    national_id_back = serializers.FileField(write_only=True)
    selfie = serializers.FileField(write_only=True, required=False)
    national_id = serializers.CharField(required=True, allow_blank=False, max_length=11)
    full_name = serializers.CharField(required=True, allow_blank=False, max_length=255)
    company_name = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        max_length=255,
    )

    class Meta:
        model = Verification
        fields = [
            "full_name",
            "national_id",
            "company_name",
            "national_id_front",
            "national_id_back",
            "selfie",
        ]

    def validate_national_id(self, value: str) -> str:
        if not DIGITS_ONLY_PATTERN.fullmatch(value):
            raise serializers.ValidationError("National ID must contain digits only.")
        return value

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        request = self.context["request"]
        profile = get_or_create_profile(request.user)
        user_type = profile.user_type
        national_id = attrs["national_id"]
        company_name = (attrs.get("company_name") or "").strip()
        attrs["company_name"] = company_name

        if user_type == Profile.UserType.NATURAL:
            if len(national_id) != NATURAL_NATIONAL_ID_LENGTH:
                raise serializers.ValidationError(
                    {
                        "national_id": (
                            "National ID must be exactly 10 digits for Natural Persons."
                        )
                    }
                )
            if company_name:
                raise serializers.ValidationError(
                    {
                        "company_name": (
                            "Company name must be empty for Natural Persons."
                        )
                    }
                )
            attrs["company_name"] = ""
        elif user_type == Profile.UserType.LEGAL:
            if len(national_id) != LEGAL_NATIONAL_ID_LENGTH:
                raise serializers.ValidationError(
                    {
                        "national_id": (
                            "National ID must be exactly 11 digits for Legal Entities."
                        )
                    }
                )
            if not company_name:
                raise serializers.ValidationError(
                    {"company_name": "Company Name is required for Legal Entities."}
                )
        else:
            raise serializers.ValidationError(
                {"user_type": "Unsupported profile user type."}
            )

        return attrs

    def create(self, validated_data: dict[str, Any]) -> Verification:
        return CreateVerificationService().execute(
            user=self.context["request"].user,
            validated_data=validated_data,
        )
