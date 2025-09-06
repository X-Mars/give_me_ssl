from rest_framework.routers import DefaultRouter
from .views import PlatformSettingViewSet

router = DefaultRouter()
router.register('platform-settings', PlatformSettingViewSet, basename='platform-setting')
