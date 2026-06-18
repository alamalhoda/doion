import logging

from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractBaseUser

logger = logging.getLogger(__name__)


class LoginService:
    """Service for user authentication with flexible identifier support."""

    def authenticate(self, identifier: str, password: str) -> AbstractBaseUser | None:
        """Authenticate user by username, email, or phone.

        Args:
            identifier: Username, email, or phone number.
            password: User password.

        Returns:
            Authenticated user or None if credentials invalid.
        """
        user = self._find_user_by_identifier(identifier)
        if user is None:
            logger.info("Login attempt with non-existent identifier: %s", identifier)
            return None

        if not user.is_active:
            logger.info("Login attempt for inactive user: %s", identifier)
            return None

        authenticated_user = authenticate(
            username=user.username,
            password=password,
        )
        if authenticated_user is None:
            logger.info("Failed login attempt for identifier: %s", identifier)

        return authenticated_user

    def _find_user_by_identifier(self, identifier: str) -> AbstractBaseUser | None:
        """Find user by username, email, or phone.

        Args:
            identifier: The identifier to search for.

        Returns:
            User instance or None.
        """
        from doion.users.models import User

        try:
            return User.objects.get(username=identifier)
        except User.DoesNotExist:
            pass

        try:
            return User.objects.get(email=identifier)
        except User.DoesNotExist:
            pass

        try:
            return User.objects.get(phone=identifier)
        except User.DoesNotExist:
            return None