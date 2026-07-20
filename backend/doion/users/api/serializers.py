from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from doion.users.models import User

LOGIN_REQUIRED_MESSAGE = "Both identifier and password are required."


class UserSerializer(serializers.ModelSerializer[User]):
    role = serializers.CharField(read_only=True)
    is_verified = serializers.BooleanField(source="profile.is_verified", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "name", "phone", "role", "is_verified", "url"]
        extra_kwargs = {
            "url": {"view_name": "api_v1:user-detail", "lookup_field": "username"},
        }


class LoginSerializer(serializers.Serializer[User]):
    """Serializer for user login with flexible identifier."""

    identifier = serializers.CharField(
        required=True,
        help_text="Username, email, or phone number",
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs: dict) -> dict:
        """Validate login credentials.

        Args:
            attrs: The validated data.

        Returns:
            Validated attrs with user attached.

        Raises:
            serializers.ValidationError: If credentials are invalid.
        """
        identifier = attrs.get("identifier")
        password = attrs.get("password")

        if identifier and password:
            return attrs
        raise serializers.ValidationError(LOGIN_REQUIRED_MESSAGE)


class LoginTokenSerializer(TokenObtainPairSerializer):
    """Custom token serializer to include user data in response."""

    @classmethod
    def get_token(cls, user: User) -> dict:
        """Get token with custom claims.

        Args:
            user: The authenticated user.

        Returns:
            Token dictionary.
        """
        token = super().get_token(user)
        token["name"] = user.name
        token["email"] = user.email
        return token

    def validate(self, attrs: dict) -> dict:
        """Validate and return token with user data.

        Args:
            attrs: The validated data.

        Returns:
            Validated data with user info.
        """
        data = super().validate(attrs)
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "name": self.user.name,
            "phone": self.user.phone or "",
            "role": self.user.role,
        }
        return data


class RefreshSerializer(serializers.Serializer[User]):
    """Serializer for token refresh."""

    refresh = serializers.CharField(
        required=True,
        help_text="Refresh token",
    )
