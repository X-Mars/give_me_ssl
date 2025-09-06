from rest_framework.routers import DefaultRouter
from .views import NotificationChannelViewSet, NotificationTemplateViewSet

router = DefaultRouter()
router.register('notification-channels', NotificationChannelViewSet, basename='notification-channel')
router.register('notification-templates', NotificationTemplateViewSet, basename='notification-template')
