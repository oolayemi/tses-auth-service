import logging
from celery import shared_task

from audit.models import AuditLog

logger = logging.getLogger(__name__)


@shared_task
def write_audit_log(event: str, email: str, ip: str, meta: dict, user_agent: str | None = None):
    AuditLog.objects.create(
        event=event,
        email=email,
        ip_address=ip,
        user_agent=user_agent,
        metadata=meta,
    )

    logger.info(f'Done writing audit log event - {event} for email - {email}')
