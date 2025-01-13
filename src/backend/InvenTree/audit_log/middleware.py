import json
import time

from django.conf import settings


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not getattr(settings, 'AUDIT_LOG_ENABLED', True):
            return self.get_response(request)

        start_time = time.time()

        # Read and store the request body safely
        request_body = b''
        if request.content_type == 'application/json':
            try:
                # Read and reset the request stream
                request_body = request.body
                request._body = request_body  # Reassign body for downstream use
                payload = json.loads(request_body)
            except json.JSONDecodeError:
                payload = {}
        elif request.method in ['POST', 'PUT', 'PATCH']:
            payload = request.POST.dict()
        else:
            payload = {}

        response = self.get_response(request)

        # Log the request and response
        try:
            from .models import AuditLog

            log_entry = AuditLog(
                request_method=request.method,
                request_url=request.get_full_path(),
                request_headers=json.dumps(dict(request.headers)),
                request_payload=json.dumps(payload),
                response_status=response.status_code,
                response_payload=str(response.content)[:1000],  # Limit response size
                user_id=request.user.id if request.user.is_authenticated else None,
                ip_address=request.META.get('REMOTE_ADDR'),
                duration_ms=int((time.time() - start_time) * 1000),
            )

            # Extract entity info from URL
            parts = request.path.strip('/').split('/')
            if len(parts) >= 2:
                log_entry.entity = parts[0]
                if parts[1].isdigit():
                    log_entry.entity_id = int(parts[1])

            log_entry.save()

        except Exception as e:
            print(f'Audit Log Error: {e!s}')

        return response
