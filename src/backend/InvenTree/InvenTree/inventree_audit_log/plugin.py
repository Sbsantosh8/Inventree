# inventree_audit_log/plugin.py
from django.urls import include, path

from inventree.plugin import AppMixin, InvenTreePlugin


class AuditLogPlugin(AppMixin, InvenTreePlugin):
    NAME = 'AuditLog'
    SLUG = 'audit_log'
    TITLE = 'Audit Log Plugin'
    DESCRIPTION = 'Comprehensive request-response logging system'
    VERSION = '1.0.0'

    AUTHOR = 'Your Name'
    WEBSITE = 'https://github.com/yourusername/inventree-audit-log'
    LICENSE = 'MIT'

    def setup_urls(self):
        return [path('audit/', include('inventree_audit_log.urls'))]

    def setup_settings(self):
        settings = {
            'AUDIT_LOG_ENABLED': {
                'name': 'Enable Audit Logging',
                'description': 'Enable comprehensive audit logging',
                'default': True,
                'type': 'boolean',
            },
            'AUDIT_LOG_RETENTION_DAYS': {
                'name': 'Log Retention Period',
                'description': 'Number of days to keep audit logs',
                'default': 90,
                'type': 'integer',
            },
        }
        return settings
