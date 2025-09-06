from __future__ import annotations

from django.db import models


class PlatformSetting(models.Model):
    key = models.CharField(max_length=128, unique=True)
    value = models.TextField()
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
