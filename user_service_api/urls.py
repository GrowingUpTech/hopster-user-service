from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('user/api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/api/v1/google/social/auth/login/google-oauth2/', views.google_login, name='google_login'),
    path('user/api/v1/google/social/auth/complete/google-oauth2/', views.google_callback, name='google-callback'),
]