from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from common.throttle import EmailOTPThrottle, IPOTPThrottle
from account.v1.serializers import (
    RequestOtpSerializer, VerifyOtpSerializer, OTPResponseSerializer, VerifyOTPResponseSerializer
)


class AuthViewSet(viewsets.GenericViewSet):
    @extend_schema(responses=OTPResponseSerializer, description="Request an email-based OTP")
    @action(methods=['POST'], detail=False, serializer_class=RequestOtpSerializer, url_path='request',
            permission_classes=[AllowAny], throttle_classes=[EmailOTPThrottle, IPOTPThrottle])
    def request_otp(self, request):
        """ Used to request for an otp """
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        response_data = {
            "success": True,
            "message": "OTP requested successfully.",
            "data": data,
        }

        response_serializer = OTPResponseSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_202_ACCEPTED)

    @extend_schema(responses=VerifyOTPResponseSerializer, description="Verify an email-based OTP")
    @action(methods=['POST'], detail=False, serializer_class=VerifyOtpSerializer, url_path='verify',
            permission_classes=[AllowAny])
    def verify_otp(self, request):
        """ Used to verify for an otp against email """
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        response_data = {
            "success": True,
            "message": "OTP verified and account created successfully.",
            "data": data,
        }

        response_serializer = VerifyOTPResponseSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
