from django.urls import include, path
from rest_framework.routers import DefaultRouter
from account.v1.views import AuthViewSet

app_name = "auth"

router = DefaultRouter()
router.register("otp", AuthViewSet, basename="auth")

urlpatterns = [
    path("", include(router.urls)),
]
