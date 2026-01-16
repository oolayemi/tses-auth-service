from django.core.cache import cache
from rest_framework.throttling import BaseThrottle

from common.exceptions import CustomThrottled


class CacheThrottle(BaseThrottle):
    key_prefix = None
    rate = None  # e.g. "3"
    period = None  # e.g. "10m" or "1h"
    error_message = 'Too many requests'
    scope = "global"

    def parse_rate(self):
        num = int(self.rate)
        period = self.period

        if period.endswith("m"):
            duration = int(period[:-1]) * 60
        elif period.endswith("h"):
            duration = int(period[:-1]) * 3600
        else:
            duration = int(period)

        return num, duration

    def allow_request(self, request, view):
        self.num_requests, self.duration = self.parse_rate()

        key = self.get_cache_key(request, view)
        if not key:
            return True

        try:
            current = cache.incr(key)
        except ValueError:
            # key does not exist
            cache.set(key, 1, timeout=self.duration)
            current = 1

        if current > self.num_requests:
            retry_after = cache.ttl(key)
            raise CustomThrottled(
                message=self.error_message,
                retry_after=retry_after,
                attr=None,
            )

        return True

    def wait(self):
        return self.wait


class EmailOTPThrottle(CacheThrottle):
    scope = "otp_email"

    # Max 3 OTP requests per email per 10 minutes
    rate = "3"
    period = "10m"

    @staticmethod
    def get_cache_key(request, view):
        email = request.data.get("email")
        if not email:
            return None
        return f"otp:rate:email:{email}"


class IPOTPThrottle(CacheThrottle):
    scope = "otp_ip"

    # Max 10 OTP requests per IP per 1 hour
    rate = "10"
    period = "1h"

    @staticmethod
    def get_cache_key(request, view):
        ip = request.META.get("REMOTE_ADDR")
        if not ip:
            return None
        return f"otp:rate:ip:{ip}"
