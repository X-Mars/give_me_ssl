from rest_framework import serializers
from .models import ProviderCredential


class ProviderCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderCredential
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
