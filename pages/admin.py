from django.contrib import admin
from .models import Visit

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'path', 'method', 'ip_address_anonymized', 'user_agent_truncated')
    list_filter = ('method', 'timestamp')
    search_fields = ('path', 'user_agent', 'referer')
    readonly_fields = ('timestamp', 'path', 'method', 'user_agent', 'ip_address_anonymized', 'referer')

    def user_agent_truncated(self, obj):
        return obj.user_agent[:50] + '...' if obj.user_agent and len(obj.user_agent) > 50 else obj.user_agent
    user_agent_truncated.short_description = 'User Agent'

    def has_add_permission(self, request):
        return False # Analytics are read-only

