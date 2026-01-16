from rest_framework import status
from rest_framework.exceptions import Throttled


class CustomThrottled(Throttled):
    default_code = "rate_limit_exceeded"
    status_code = status.HTTP_429_TOO_MANY_REQUESTS

    def __init__(self, *, message: str, retry_after: int, attr: str = None, status_code=status.HTTP_429_TOO_MANY_REQUESTS):
        self.attr = attr
        self.status_code = status_code
        super().__init__(
            detail=message,
            wait=retry_after,
        )
