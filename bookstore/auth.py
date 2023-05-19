import base64
import hashlib
import hmac
import json
import time

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header



class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'custom':
            return None
        token = auth[1].decode()
        if "." not in token:
            raise exceptions.AuthenticationFailed("token topilmadi")
        data, user_hash = token.split(".", 2)
        data = base64.b64decode(data)

        sign = hmac.new(settings.SECRET_KEY.encode(), data, hashlib.sha256).hexdigest()

        if sign != user_hash:
            raise exceptions.AuthenticationFailed("sign invalid")

        data = json.loads(data.decode())

        if data["expire"] < time.time():
            raise exceptions.AuthenticationFailed("Timeout")

        try:
            user = User.objects.get(id=data["user_id"])
        except:
            raise exceptions.AuthenticationFailed("ID topilmadi")

        return (user, None)
