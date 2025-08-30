from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.

class NewUser(AbstractUser):
    last_login = models.DateTimeField(_('最后登录时间'), blank=True, null=True, auto_now=True)
    last_active = models.DateTimeField(_('最后活跃时间'), blank=True, null=True, auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.id.__str__() + '---' + self.username + '---' + self.last_name + '---' + self.first_name

    def update_last_active(self):
        self.last_active = timezone.now()
        self.save(update_fields=['last_active'])

    class Meta(AbstractUser.Meta):
        default_permissions = ()
        permissions = [
            ("view_user", "查看 用户"),
            ("add_user", "添加 用户"),
            ("change_user", "修改 用户"),
            ("delete_user", "删除 用户"),
        ]
        swappable = 'AUTH_USER_MODEL'
        pass