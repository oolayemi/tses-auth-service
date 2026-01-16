import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def send_otp_email(email, otp):
    logger.info(f"Sending OTP of '{otp}' to {email}")
