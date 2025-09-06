from rest_framework import serializers
from .models import NotificationChannel, NotificationTemplate


class NotificationChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationChannel
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
