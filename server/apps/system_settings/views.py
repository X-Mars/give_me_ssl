from rest_framework import viewsets, permissions
from .models import PlatformSetting
from .serializers import PlatformSettingSerializer


class PlatformSettingViewSet(viewsets.ModelViewSet):
    serializer_class = PlatformSettingSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = PlatformSetting.objects.all()
