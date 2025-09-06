from rest_framework.routers import DefaultRouter
from .views import ProviderCredentialViewSet

router = DefaultRouter()
router.register('provider-credentials', ProviderCredentialViewSet, basename='provider-credential')
