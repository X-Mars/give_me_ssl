from rest_framework import viewsets, permissions
from .models import ProviderCredential
from .serializers import ProviderCredentialSerializer


class ProviderCredentialViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderCredentialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        return ProviderCredential.objects.filter(user=self.request.user)

    def perform_create(self, serializer):  # type: ignore[override]
        serializer.save(user=self.request.user)
