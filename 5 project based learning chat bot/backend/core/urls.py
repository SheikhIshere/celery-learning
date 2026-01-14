from rest_framework.routers import DefaultRouter
from .views import AiChatSessionViewSet, AiRequestViewSet

router = DefaultRouter()
router.register(r"sessions", AiChatSessionViewSet, basename="sessions")
router.register(r"requests", AiRequestViewSet, basename="requests")

urlpatterns = router.urls
