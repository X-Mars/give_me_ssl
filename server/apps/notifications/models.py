from __future__ import annotations

from django.db import models
from django.conf import settings


class NotificationChannel(models.Model):
    CHANNEL_CHOICES = [
        ('wecom_robot', 'WeCom Robot'),
        ('feishu_robot', 'Feishu Robot'),
        ('dingtalk_robot', 'DingTalk Robot'),
        ('system', 'System'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_channels')
    channel = models.CharField(max_length=32, choices=CHANNEL_CHOICES)
    webhook = models.CharField(max_length=512, blank=True)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationTemplate(models.Model):
    name = models.CharField(max_length=64)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
