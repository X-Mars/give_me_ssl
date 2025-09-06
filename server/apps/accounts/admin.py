from django.contrib import admin
from .models import WeComUser, DingTalkUser, FeiShuUser


@admin.register(WeComUser)
class WeComUserAdmin(admin.ModelAdmin):
    list_display = ('wecom_userid', 'user', 'nickname', 'mobile', 'created_at')
    search_fields = ('wecom_userid', 'nickname', 'mobile')


@admin.register(DingTalkUser)
class DingTalkUserAdmin(admin.ModelAdmin):
    list_display = ('union_id', 'user', 'nickname', 'mobile', 'created_at')
    search_fields = ('union_id', 'nickname', 'mobile')


@admin.register(FeiShuUser)
class FeiShuUserAdmin(admin.ModelAdmin):
    list_display = ('open_id', 'user', 'nickname', 'mobile', 'created_at')
    search_fields = ('open_id', 'nickname', 'mobile')
