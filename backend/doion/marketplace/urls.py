from django.urls import path

from doion.marketplace.views import MarketplaceViewSet

app_name = "marketplace"

urlpatterns = [
    path("marketplace/listings/", MarketplaceViewSet.as_view({"get": "list"}), name="listing-list"),
]
