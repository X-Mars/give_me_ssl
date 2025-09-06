from django.contrib import admin
from .models import ProviderCredential


@admin.register(ProviderCredential)
class ProviderCredentialAdmin(admin.ModelAdmin):
    list_display = ('provider', 'user', 'created_at')
    list_filter = ('provider',)
    search_fields = ('provider', 'user__username')
