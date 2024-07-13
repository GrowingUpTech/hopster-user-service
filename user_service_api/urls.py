from django.urls import path, include
from .views.google_views import google_login, google_callback
from .views.user_nutrition_views import add_new_nutrition
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('user/api/v1/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('user/api/v1/token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('user/api/v1/google/social/auth/login/google-oauth2/', google_login, name='google-login'),
    path('user/api/v1/google/social/auth/complete/google-oauth2/', google_callback, name='google-callback'),
    path('user/api/v1/meal/data', add_new_nutrition)
]