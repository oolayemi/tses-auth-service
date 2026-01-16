from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from common.throttle import EmailOTPThrottle, IPOTPThrottle
from account.v1.serializers import (
    RequestOtpSerializer, VerifyOtpSerializer
)


class AuthViewSet(viewsets.GenericViewSet):
    @action(methods=['POST'], detail=False, serializer_class=RequestOtpSerializer, url_path='request',
            permission_classes=[AllowAny], throttle_classes=[EmailOTPThrottle, IPOTPThrottle])
    def request_otp(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response({'success': True, 'message': 'OTP requested successfully.', 'data': data},
                        status=status.HTTP_202_ACCEPTED)

    @action(methods=['POST'], detail=False, serializer_class=VerifyOtpSerializer, url_path='verify',
            permission_classes=[AllowAny])
    def verify_otp(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response({'success': True, 'message': 'OTP verified and account created successfully', 'data': data},
                        status=status.HTTP_200_OK)
