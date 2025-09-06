from __future__ import annotations

from django.db import models
from django.conf import settings


class Certificate(models.Model):
    PROVIDER_CHOICES = [
        ('lets_encrypt', 'Let\'s Encrypt'),
        ('aliyun', 'Aliyun'),
        ('huawei', 'Huawei Cloud'),
        ('tencent', 'Tencent Cloud'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    domain = models.CharField(max_length=255)
    provider = models.CharField(max_length=32, choices=PROVIDER_CHOICES)
    status = models.CharField(max_length=32, default='pending')
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):  # pragma: no cover
        return f'{self.domain} ({self.provider})'
