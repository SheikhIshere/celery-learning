from django.db import models


class Recipe(models.Model):
    """Represents a recipe in the system."""
    name = models.CharField(max_length=255)
    steps = models.TextField()

    def __str__(self):
        return self.name
    

class AiChatSession(models.Model):
    """ tracks an ai chat session """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AiRequest(models.Model):
    """ represent an ai request """
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'

    STATUS_OPTIONS = (
        (PENDING, 'Pending'),
        (RUNNING, 'Running'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
    )
    status = models.CharField(choices=STATUS_OPTIONS)
    session = models.ForeignKey(
        AiChatSession,
        on_delete=models.CASCADE,
        null=True,
        blank=True    
    )

    message = models.JSONField()
    response = models.JSONField()

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

