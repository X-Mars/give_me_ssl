from __future__ import annotations

from django.db import models
from django.conf import settings


class ProviderCredential(models.Model):
    PROVIDER_CHOICES = [
        ('aliyun', 'Aliyun'),
        ('lets_encrypt', 'Let\'s Encrypt'),
        ('huawei', 'Huawei Cloud'),
        ('tencent', 'Tencent Cloud'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='provider_credentials')
    provider = models.CharField(max_length=32, choices=PROVIDER_CHOICES)
    access_key = models.CharField(max_length=256)
    secret_key = models.CharField(max_length=256)
    extra = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'provider')
