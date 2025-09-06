from __future__ import annotations

from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class WeComUser(TimeStampedModel):  # 企业微信
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wecom_accounts')
    wecom_userid = models.CharField(max_length=128, unique=True)
    avatar = models.URLField(blank=True)
    mobile = models.CharField(max_length=32, blank=True)
    nickname = models.CharField(max_length=64, blank=True)

    def __str__(self) -> str:  # pragma: no cover
        return f'WeComUser<{self.wecom_userid}>'


class DingTalkUser(TimeStampedModel):  # 钉钉
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dingtalk_accounts')
    union_id = models.CharField(max_length=128, unique=True)
    avatar = models.URLField(blank=True)
    mobile = models.CharField(max_length=32, blank=True)
    nickname = models.CharField(max_length=64, blank=True)

    def __str__(self) -> str:  # pragma: no cover
        return f'DingTalkUser<{self.union_id}>'


class FeiShuUser(TimeStampedModel):  # 飞书
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feishu_accounts')
    open_id = models.CharField(max_length=128, unique=True)
    avatar = models.URLField(blank=True)
    mobile = models.CharField(max_length=32, blank=True)
    nickname = models.CharField(max_length=64, blank=True)

    def __str__(self) -> str:  # pragma: no cover
        return f'FeiShuUser<{self.open_id}>'
