from rest_framework import serializers
from .models import PlatformSetting


class PlatformSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformSetting
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
