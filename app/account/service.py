from datetime import timedelta

from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from django.core.cache import cache
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from common.exceptions import CustomThrottled
from account.tasks import send_otp_email
from audit.tasks import write_audit_log
from account.utils import generate_verification_code

FAILED_LIMIT = 5
FAILED_WINDOW = 900  # 15 minutes
OTP_TTL_SECONDS = 300  # 5 minutes


class OtpService:

    @staticmethod
    def generate_and_send_otp(email: str, ip: str, user_agent: str | None):
        otp = generate_verification_code(6)

        otp_key = f"otp:{email}"
        cache.set(otp_key, otp, timeout=OTP_TTL_SECONDS)

        send_otp_email.delay(email=email, otp=otp)

        write_audit_log.delay(
            event="OTP_REQUESTED",
            email=email,
            ip=ip,
            meta={"expires_in": OTP_TTL_SECONDS},
            user_agent=user_agent,
        )

        return {
            "expires_in": OTP_TTL_SECONDS,
            "expires_at": timezone.now() + timedelta(seconds=OTP_TTL_SECONDS),
        }

    @staticmethod
    def verify_otp(email: str, otp: str, ip: str, user_agent: str | None) -> dict:
        otp_key = f"otp:{email}"
        failed_key = f"otp:failed:{email}"

        failed_count = cache.get(failed_key, 0)
        if failed_count >= FAILED_LIMIT:
            retry_after = cache.ttl(failed_key)
            raise CustomThrottled(
                message="OTP verification locked",
                retry_after=retry_after
            )

        stored_otp = cache.get(otp_key)
        if not stored_otp or stored_otp != otp:
            try:
                failed = cache.incr(failed_key)
            except ValueError:
                cache.set(failed_key, 1, timeout=FAILED_WINDOW)
                failed = 1

            write_audit_log.delay(
                event="OTP_FAILED",
                email=email,
                ip=ip,
                meta={"attempts": failed},
                user_agent=user_agent,
            )

            raise ValidationError("The provided OTP is invalid or expired")

        cache.delete(otp_key)
        cache.delete(failed_key)

        user, _ = get_user_model().objects.get_or_create(
            email=email,
            defaults={"username": email},
        )

        refresh = RefreshToken.for_user(user)

        write_audit_log.delay(
            event="OTP_VERIFIED",
            email=email,
            ip=ip,
            meta={},
            user_agent=user_agent,
        )

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
