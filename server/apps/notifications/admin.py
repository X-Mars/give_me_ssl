from django.contrib import admin
from .models import NotificationChannel, NotificationTemplate


@admin.register(NotificationChannel)
class NotificationChannelAdmin(admin.ModelAdmin):
    list_display = ('channel', 'user', 'enabled', 'created_at')
    list_filter = ('channel', 'enabled')
    search_fields = ('channel', 'user__username')


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
