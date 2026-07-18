
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from doion.checks.models import ChequeListing
from doion.marketplace.filters import MarketplaceFilter
from doion.marketplace.serializers import MarketplaceLatestSerializer, MarketplaceListingSerializer


class MarketplaceViewSet(ReadOnlyModelViewSet):
    serializer_class = MarketplaceListingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = MarketplaceFilter
    ordering_fields = ["created_at", "face_amount", "suggested_discount_rate", "due_date"]
    ordering = ["-created_at"]
    search_fields = ["bank_name"]

    CACHE_KEY_PREFIX = "marketplace:listings"
    CACHE_TTL = 60

    def get_permissions(self):
        if self.action == "latest_listings":
            return [AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        return (
            ChequeListing.objects.filter(status=ChequeListing.Status.PUBLISHED)
            .select_related("issuer", "owner")
            .order_by("-created_at")
        )

    def list(self, request, *args, **kwargs):
        page = request.query_params.get("page", "1")
        cache_key = f"{self.CACHE_KEY_PREFIX}:{page}"
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=self.CACHE_TTL)
        return response

    @action(detail=False, methods=["get"], url_path="latest")
    def latest_listings(self, request):
        queryset = (
            ChequeListing.objects.filter(status=ChequeListing.Status.PUBLISHED)
            .select_related("issuer", "owner")
            .order_by("-created_at")[:4]
        )
        serializer = MarketplaceLatestSerializer(queryset, many=True)
        return Response(serializer.data)
