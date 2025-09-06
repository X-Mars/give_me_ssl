from django.contrib import admin
from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('domain', 'provider', 'status', 'expires_at', 'user', 'created_at')
    list_filter = ('provider', 'status')
    search_fields = ('domain',)
