# inventree_audit_log/views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include, path
from django.utils.decorators import method_decorator

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import AuditLog
from .serializers import AuditLogSerializer


@method_decorator(staff_member_required, name='dispatch')
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = AuditLog.objects.all().order_by('-timestamp')

        # Apply filters
        entity = self.request.query_params.get('entity', None)
        if entity:
            queryset = queryset.filter(entity=entity)

        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(response_status=status)

        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset


from rest_framework.response import Response
from rest_framework.views import APIView


class MetadataView(APIView):
    def get(self, request, *args, **kwargs):
        model = kwargs.get('model')
        if model:
            metadata = {
                'fields': [field.name for field in model._meta.get_fields()],
                'verbose_name': model._meta.verbose_name,
                'verbose_name_plural': model._meta.verbose_name_plural,
            }
            return Response(metadata)
        return Response({'error': 'No model provided'}, status=400)


audit_log_api_urls = [
    # Base URL for audit log API endpoints
    path(
        'audit/',
        include([
            path(
                '<int:pk>/',
                include([
                    path(
                        'metadata/',
                        MetadataView.as_view(),
                        {'model': AuditLog},
                        name='api-audit-log-metadata',
                    ),
                    path(
                        '',
                        AuditLogViewSet.as_view({'get': 'retrieve'}),
                        name='api-audit-log-detail',
                    ),
                ]),
            ),
            # Filter parameters can be passed as query params
            path(
                'filter/',
                include([
                    path(
                        'entity/',
                        AuditLogViewSet.as_view({'get': 'list'}),
                        name='api-audit-log-filter-entity',
                    ),
                    path(
                        'status/',
                        AuditLogViewSet.as_view({'get': 'list'}),
                        name='api-audit-log-filter-status',
                    ),
                    path(
                        'user/',
                        AuditLogViewSet.as_view({'get': 'list'}),
                        name='api-audit-log-filter-user',
                    ),
                ]),
            ),
            path(
                '', AuditLogViewSet.as_view({'get': 'list'}), name='api-audit-log-list'
            ),
        ]),
    )
]
