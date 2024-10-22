# config/middleware.py
from urllib.parse import urljoin

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django_creta_auth.gateway import validate_session
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class AutoLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.GET.get("token")
        if token:
            user = self.authenticate_with_token(token)
            if user is not None:
                if user.is_staff or user.is_superuser:
                    self.login_with_backend(request, user)
                else:
                    return None
        return None

    def authenticate_with_token(self, token):
        try:
            user = User.objects.get(token_creta=token, token_creta_expired_at__gte=timezone.now())
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # 명시적으로 backend 설정
            return user
        except User.DoesNotExist:
            session_data, status_code = validate_session(token)
            if status_code != 200 or not session_data.get("isValid", False):
                raise AuthenticationFailed(session_data.get("error", "Invalid session"))
            return self.get_user_from_session(session_data, token)

    def get_user_from_session(self, session_data, token):
        user_info = session_data.get("sessionUser")
        expired_at = session_data.get("expiresAt")
        if not user_info:
            raise AuthenticationFailed("Invalid session data")

        user_id_creta = user_info.get("id")
        email = user_info.get("email")
        is_two_factor = user_info.get("isTwoFactor")

        try:
            user = User.objects.get(id_creta=user_id_creta)
            user.token_creta = token
            user.token_creta_expired_at = expired_at
            user.is_two_factor = is_two_factor
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # 명시적으로 backend 설정
            user.save()

            if not user.is_active:
                raise AuthenticationFailed("User is inactive")

            return user
        except User.DoesNotExist:
            # Fetch user details from Superclub server if user does not exist locally
            user = self.fetch_user_from_superclub(token)
            if user:
                user.token_creta = token
                user.token_creta_expired_at = expired_at
                user.is_two_factor = is_two_factor
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                user.save()
                return user
            raise AuthenticationFailed("User does not exist")

    def fetch_user_from_superclub(self, token):
        url = urljoin(settings.SUPERCLUB_SERVER_HOST, f"/api/{settings.SUPERCLUB_API_VERSION}/user/me")
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(token)
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise AuthenticationFailed("Failed to retrieve user data from Superclub server")

        data = response.json()
        user_data = data.get("data", None)
        if not user_data:
            raise AuthenticationFailed("Invalid user data from Superclub server")

        # Filter user_data to include only fields that exist in the User model
        user_fields = {field.name for field in User._meta.get_fields()}
        filtered_user_data = {k: v for k, v in user_data.items() if k in user_fields}

        # Create the user locally
        user = User.objects.create(**filtered_user_data)
        return user

    def login_with_backend(self, request, user):
        user.backend = 'django.contrib.auth.backends.ModelBackend'  # 명시적으로 backend 설정
        login(request, user)
