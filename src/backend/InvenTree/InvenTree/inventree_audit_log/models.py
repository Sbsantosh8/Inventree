# inventree_audit_log/models.py
from django.db import models
from django.utils import timezone


class AuditLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    entity = models.CharField(max_length=255, null=True)
    entity_id = models.BigIntegerField(null=True)
    action = models.CharField(max_length=255)

    request_method = models.CharField(max_length=10)
    request_url = models.TextField()
    request_headers = models.TextField(null=True)
    request_payload = models.TextField(null=True)

    response_status = models.IntegerField()
    response_payload = models.TextField(null=True)
    error_message = models.TextField(null=True)

    user_id = models.BigIntegerField(null=True)
    ip_address = models.CharField(max_length=45, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    duration_ms = models.BigIntegerField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['entity', 'entity_id']),
            models.Index(fields=['user_id']),
            models.Index(fields=['response_status']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f'{self.action} on {self.entity} at {self.timestamp}'
