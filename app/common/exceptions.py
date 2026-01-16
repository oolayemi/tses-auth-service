from rest_framework.exceptions import Throttled


class CustomThrottled(Throttled):
    default_code = "rate_limit_exceeded"

    def __init__(self, *, message: str, retry_after: int, attr: str = None):
        self.attr = attr  # maps to field_name
        super().__init__(
            detail=message,
            wait=retry_after,
        )
