from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import AiChatSession, AiRequest
from .serializers import AiChatSessionSerializer, AiRequestCreateSerializer

from drf_spectacular.utils import extend_schema


@extend_schema(tags=['chat session'])
class AiChatSessionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Sessions: allow POST (create), GET (list) and GET (retrieve).
    Also provides POST /sessions/{id}/send/ to create an AiRequest tied to this session.
    """
    queryset = AiChatSession.objects.all().order_by("-updated_at")
    serializer_class = AiChatSessionSerializer

    def create(self, request, *args, **kwargs):
        """
        POST /sessions/ -> create a new session.
        Title optional in request.data; default to "New Chat".
        """
        title = request.data.get("title") or "New Chat"
        session = AiChatSession.objects.create(title=title)
        serializer = self.get_serializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def send(self, request, pk=None):
        """
        POST /sessions/{id}/send/ -> create AiRequest tied to this session.
        Uses AiRequestCreateSerializer for validation (blocks if last request is PENDING/RUNNING).
        """
        session = self.get_object()
        message = request.data.get("message", "")

        data = {
            "session": session.id,
            "message": message,
        }

        serializer = AiRequestCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        ai_request = serializer.save()

        out = AiRequestCreateSerializer(ai_request).data
        return Response(out, status=status.HTTP_201_CREATED)


@extend_schema(tags=['chat request'])
class AiRequestViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    AiRequest: only GET endpoints (list and retrieve).
    Creation of requests should go through sessions/{id}/send/.
    """
    queryset = AiRequest.objects.all().order_by("-created_at")
    serializer_class = AiRequestCreateSerializer
