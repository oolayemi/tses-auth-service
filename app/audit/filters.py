from audit.models import AuditLog
from common.filter import DateFilter


class AuditLogFilter(DateFilter):
    class Meta:
        model = AuditLog
        fields = ['email', 'event']
