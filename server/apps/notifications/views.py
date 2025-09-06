from rest_framework import viewsets, permissions
from .models import NotificationChannel, NotificationTemplate
from .serializers import NotificationChannelSerializer, NotificationTemplateSerializer


class NotificationChannelViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationChannelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        return NotificationChannel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):  # type: ignore[override]
        serializer.save(user=self.request.user)


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = NotificationTemplate.objects.all()
