# inventree_audit_log/admin.py
from django.contrib import admin

from .models import AuditLog


class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'entity',
        'entity_id',
        'action',
        'request_method',
        'request_url',
        'response_status',
        'user_id',
        'ip_address',
        'timestamp',
        'duration_ms',
    )
    list_filter = ('entity', 'action', 'response_status', 'user_id', 'timestamp')
    search_fields = ('entity', 'entity_id', 'action', 'request_url', 'response_status')
    readonly_fields = ('id', 'timestamp', 'user_id', 'ip_address')

    ordering = ('-timestamp',)


admin.site.register(AuditLog, AuditLogAdmin)
