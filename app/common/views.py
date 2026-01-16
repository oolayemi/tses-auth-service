import logging
from urllib.parse import urlparse

import jwt
import redis
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db import OperationalError, connections
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from account.v1.serializers import UserSerializer
from common.decorators import jwt_required
from account.v1.serializers import (
    TokenDecodeSerializer,
)


@api_view(["GET"])
def readiness_check(request):
    response = {"database": "unknown", "redis": "unknown"}

    # Check database connection
    try:
        db_conn = connections["default"]
        db_conn.cursor()
        response["database"] = "ready"
    except OperationalError:
        response["database"] = "not ready"

    # Check Redis connection
    try:
        redis_url = urlparse(settings.REDIS_URL)
        r = redis.StrictRedis(
            host=redis_url.hostname,
            port=redis_url.port,
            password=redis_url.password,
            decode_responses=True,
        )
        r.ping()
        response["redis"] = "ready"
    except redis.ConnectionError:
        response["redis"] = "not ready"

    return Response(response)


@api_view(["GET"])
def health_check(request):
    response = {"status": True}
    return Response(response)






CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)
logger = logging.getLogger(__name__)


class DecodeJwtTokenView(APIView):
    serializer_class = TokenDecodeSerializer

    @jwt_required  # only a valid token can access this view
    def post(self, request):
        # print("META", request.META)
        # print("PAYLOAD", request.data)
        token = request.data.get("token", None)
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            except jwt.ExpiredSignatureError as e:
                logger.error(e)
                raise AuthenticationFailed("Unauthenticated")

            user = get_user_model().objects.get(id=payload["user_id"])
            serializer = UserSerializer(instance=user)
            return Response(
                {
                    **serializer.data,
                    # "tenant_id": payload["id"],
                    # "permissions": user.permission_list(),
                }
            )
        raise AuthenticationFailed("Unauthenticated")






