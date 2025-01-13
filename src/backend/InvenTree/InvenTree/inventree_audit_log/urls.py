# inventree_audit_log/urls.py
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .api import AuditLogViewSet

router = DefaultRouter()
router.register(r'logs', AuditLogViewSet)

urlpatterns = [path('', include(router.urls))]
