from rest_framework.routers import DefaultRouter

from doion.moderation.views import ModerationViewSet

router = DefaultRouter()
router.register(r"", ModerationViewSet, basename="moderation")

app_name = "moderation"
urlpatterns = router.urls
