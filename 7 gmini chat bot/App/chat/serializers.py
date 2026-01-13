from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'conversation', 'role', 'text', 'provider_response', 'created_at')
        read_only_fields = ('id', 'provider_response', 'created_at')


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)


class Meta:
    model = Conversation
    fields = ('id', 'owner', 'title', 'created_at', 'updated_at', 'messages')
    read_only_fields = ('id', 'created_at', 'updated_at')