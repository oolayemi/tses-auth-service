from django.contrib.auth import get_user_model
from email_validator import EmailNotValidError, validate_email
from rest_framework import serializers

from account.service import OtpService

User = get_user_model()


class OTPResponseDataSerializer(serializers.Serializer):
    expires_in = serializers.IntegerField(help_text="OTP validity duration in seconds")
    expires_at = serializers.DateTimeField(help_text="OTP expiration timestamp (UTC)")


class OTPResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    message = serializers.CharField()
    data = OTPResponseDataSerializer()


class VerifyOTPResponseDataSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class VerifyOTPResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    message = serializers.CharField()
    data = VerifyOTPResponseDataSerializer()


class RequestOtpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        email = attrs.get("email").strip().lower()

        try:
            validated_email = validate_email(email)
            attrs['email'] = validated_email.normalized
        except EmailNotValidError as e:
            raise serializers.ValidationError(e)

        if get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'The provided email is already registered'})

        return attrs

    def create(self, validated_data):
        otp_service = OtpService()
        email = validated_data.get("email")

        request = self.context.get("request")

        ip = request.META.get("REMOTE_ADDR")
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        result = otp_service.generate_and_send_otp(email, ip, user_agent)
        return result


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        email = attrs.get("email").strip().lower()

        try:
            validated_email = validate_email(email)
            attrs['email'] = validated_email.normalized
        except EmailNotValidError as e:
            raise serializers.ValidationError(e)

        return attrs

    def create(self, validated_data):
        otp_service = OtpService()
        email = validated_data.get("email")
        otp = validated_data.get("otp")

        request = self.context.get("request")

        ip = request.META.get("REMOTE_ADDR")
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        result = otp_service.verify_otp(email, otp, ip, user_agent)
        return result
