from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework import serializers

from doion.documents.models import Document
from doion.identity.models import Profile, Verification
from doion.users.models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True, default="")
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True, default="")
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True, default="")
    role = serializers.ChoiceField(choices=["check_holder", "investor"])

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_phone(self, value):
        if value and User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        role = validated_data.pop("role")
        password = validated_data.pop("password")
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data.get("email", ""),
                password=password,
                name=validated_data.get("name", ""),
                phone=validated_data.get("phone", ""),
                role=role,
            )
            profile = Profile.objects.create(user=user, role=role)
            group_name = "Investor" if role == "investor" else "CheckHolder"
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        return user


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
            "bio",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "role", "is_verified", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        user_fields = {"email", "name", "phone"}
        user_data = {}
        for attr, value in list(validated_data.items()):
            if attr in user_fields:
                user_data[attr] = value
                validated_data.pop(attr)
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.role", read_only=True)
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
            "is_verified",
        ]
        read_only_fields = ["id", "role", "is_verified"]

    def update(self, instance, validated_data):
        profile = instance.profile
        user = instance
        for attr, value in validated_data.items():
            setattr(user, attr, value)
        user.save()
        return user


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "document_type", "file", "file_size"]


class VerificationSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Verification
        fields = [
            "id",
            "full_name",
            "national_id",
            "company_name",
            "status",
            "rejection_reason",
            "rejection_code",
            "documents",
        ]
        read_only_fields = [
            "id",
            "status",
            "rejection_reason",
            "rejection_code",
            "documents",
        ]


class VerificationCreateSerializer(serializers.ModelSerializer):
    national_id_front = serializers.FileField(write_only=True)
    national_id_back = serializers.FileField(write_only=True)
    selfie = serializers.FileField(write_only=True, required=False)

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

    def create(self, validated_data):
        front = validated_data.pop("national_id_front")
        back = validated_data.pop("national_id_back")
        selfie = validated_data.pop("selfie", None)

        verification = Verification.objects.create(**validated_data)

        Document.objects.create(
            owner=verification.user,
            related_object_type="verification",
            related_object_id=verification.id,
            document_type=Document.DocumentType.NATIONAL_ID_FRONT,
            file=front,
            file_size=front.size,
        )
        Document.objects.create(
            owner=verification.user,
            related_object_type="verification",
            related_object_id=verification.id,
            document_type=Document.DocumentType.NATIONAL_ID_BACK,
            file=back,
            file_size=back.size,
        )
        if selfie:
            Document.objects.create(
                owner=verification.user,
                related_object_type="verification",
                related_object_id=verification.id,
                document_type=Document.DocumentType.SELFIE,
                file=selfie,
                file_size=selfie.size,
            )

        from doion.identity.signals import verification_submitted
        verification_submitted.send(sender=self.__class__, verification=verification)

        return verification
