from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserToken
import requests

@api_view(['GET'])
def google_login(request):
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?client_id={client_id}"
        "&response_type=code"
        "&scope=openid%20email%20profile"
        "&redirect_uri={redirect_uri}"
        "&state={state}"
        "&prompt=select_account"
    ).format(
        client_id=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        redirect_uri=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI,
        state=request.session.session_key
    )
    return redirect(google_auth_url)

@api_view(['GET'])
def google_callback(request):
    code = request.GET.get('code')
    if not code:
        return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)

    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        'code': code,
        'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
        'redirect_uri': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()

    if 'error' in token_json:
        return Response({'error': token_json['error']}, status=status.HTTP_400_BAD_REQUEST)

    access_token = token_json.get('access_token')
    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    user_info_response = requests.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'})
    user_info = user_info_response.json()

    if 'error' in user_info:
        return Response({'error': user_info['error']}, status=status.HTTP_400_BAD_REQUEST)

    email = user_info.get('email')
    first_name = user_info.get('given_name')
    last_name = user_info.get('family_name')

    user, created = User.objects.get_or_create(username=email, defaults={
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
    })

    if created:
        user.set_unusable_password()
        user.save()

    # Invalidate old tokens
    UserToken.objects.filter(user=user).delete()

    # Generate new tokens
    refresh = RefreshToken.for_user(user)

    # Store the new refresh token
    UserToken.objects.create(user=user, refresh_token=str(refresh))

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })
