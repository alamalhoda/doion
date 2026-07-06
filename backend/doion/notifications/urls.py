from rest_framework.routers import DefaultRouter

from doion.notifications.views import NotificationViewSet

router = DefaultRouter()
router.register(r"notifications", NotificationViewSet, basename="notifications")

app_name = "notifications"
urlpatterns = router.urls