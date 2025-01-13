# inventree_audit_log/apps.py
from django.apps import AppConfig


class AuditLogConfig(AppConfig):
    name = 'inventree_audit_log'
    verbose_name = 'InvenTree Audit Log'

    def ready(self):
        pass
