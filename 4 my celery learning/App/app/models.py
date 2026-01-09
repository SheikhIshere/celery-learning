# location App/app/models.py
from django.db import models

# Create your models here.


class BasicApp(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True)
    is_deleted = models.BooleanField(default=False)
