from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny

from audit.filters import AuditLogFilter
from audit.models import AuditLog
from audit.v1.serializers import AuditLogSerializer


class AuditLogViewSets(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get"]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AuditLogFilter
    ordering_fields = ["created_at"]
