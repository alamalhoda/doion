import logging

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import ExpiredTokenError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from doion.identity.services import get_or_create_profile
from doion.users.models import User
from doion.users.services import LoginService

from .serializers import LoginSerializer
from .serializers import RefreshSerializer
from .serializers import UserSerializer

logger = logging.getLogger(__name__)

INVALID_CREDENTIALS_MESSAGE = "Invalid credentials"
REFRESH_AUTH_ERROR = "Invalid refresh token"


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        get_or_create_profile(request.user)
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class LoginViewSet(GenericViewSet):
    """ViewSet for user login with flexible identifier support."""

    serializer_class = LoginSerializer
    permission_classes = []

    def create(self, request):
        """Authenticate user and return JWT tokens.

        Args:
            request: The HTTP request.

        Returns:
            Response with access token and user data.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = LoginService().authenticate(
            identifier=serializer.validated_data["identifier"],
            password=serializer.validated_data["password"],
        )

        if user is None:
            raise AuthenticationFailed(INVALID_CREDENTIALS_MESSAGE)

        profile = get_or_create_profile(user)
        refresh = RefreshToken.for_user(user)
        response_data = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "user_type": profile.user_type,
                "phone": user.phone or "",
            },
        }

        logger.info("User %s logged in successfully", user.id)
        return Response(status=status.HTTP_200_OK, data=response_data)


class RefreshViewSet(GenericViewSet):
    """ViewSet for token refresh using SimpleJWT."""

    serializer_class = RefreshSerializer
    permission_classes = []

    def create(self, request):
        """Refresh access token using refresh token.

        Args:
            request: The HTTP request with refresh token.

        Returns:
            Response with new access token and user data.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]
        try:
            token = RefreshToken(refresh_token)
            user_id = token.payload.get("user_id")
            user = User.objects.get(id=user_id)
        except (
            TokenError,
            ExpiredTokenError,
            User.DoesNotExist,
            TypeError,
            ValueError,
        ) as exc:
            raise AuthenticationFailed(REFRESH_AUTH_ERROR) from exc

        new_refresh = RefreshToken.for_user(user)
        profile = get_or_create_profile(user)
        response_data = {
            "access": str(new_refresh.access_token),
            "refresh": str(new_refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "user_type": profile.user_type,
                "phone": user.phone or "",
            },
        }

        logger.info("User %s refreshed tokens successfully", user.id)
        return Response(status=status.HTTP_200_OK, data=response_data)
