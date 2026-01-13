from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    """Represents a conversation (chat session) between a user and the assistant."""
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='conversations')
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f'Conversation {self.id} - {self.title or "untitled"}'


class Message(models.Model):
    ROLE_CHOICES = (
    ('user', 'User'),
    ('assistant', 'Assistant'),
    ('system', 'System'),
    )
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    role = models.CharField(max_length=16, choices=ROLE_CHOICES)
    text = models.TextField()
    provider_response = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f'<{self.role}>: {self.text[:50]}'