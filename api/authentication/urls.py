from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# JWT Auth Endpoints
urlpatterns = [
    path("tokens/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("tokens/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
