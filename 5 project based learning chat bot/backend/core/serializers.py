from rest_framework import serializers
from .models import AiChatSession, AiRequest


class AiChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiChatSession
        fields = [
            "id",
            "title",
            "messages",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["messages", "created_at", "updated_at"]



class AiRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiRequest
        fields = [
            "id",
            "session",
            "message",
            "status",
            "response",
            "created_at",
        ]
        read_only_fields = ["status", "response", "created_at"]

    def validate(self, attrs):
        message = attrs.get("message", "")
        session = attrs.get("session")

        # Message validation
        if not message or not message.strip():
            raise serializers.ValidationError(
                {"message": "Message cannot be empty."}
            )

        # 3️⃣ BLOCK if last request is still running or pending
        last_request = (
            AiRequest.objects
            .filter(session=session)
            .order_by("-created_at")
            .first()
        )

        if last_request and last_request.status in (
            AiRequest.PENDING,
            AiRequest.RUNNING,
        ):
            raise serializers.ValidationError(
                "Please wait for the previous response to complete."
            )

        return attrs
