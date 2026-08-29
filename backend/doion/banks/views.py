"""Public read-only bank catalog API."""

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from doion.banks.models import Bank
from doion.banks.serializers import BankSerializer


class BankViewSet(ReadOnlyModelViewSet):
    serializer_class = BankSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    http_method_names = ["get", "head", "options"]
    queryset = Bank.objects.filter(is_active=True).order_by("display_name")

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
