from rest_framework import viewsets, permissions
from .models import Certificate
from .serializers import CertificateSerializer


class CertificateViewSet(viewsets.ModelViewSet):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        return Certificate.objects.filter(user=self.request.user)

    def perform_create(self, serializer):  # type: ignore[override]
        serializer.save(user=self.request.user)
