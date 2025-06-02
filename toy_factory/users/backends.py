from django.contrib.auth.backends import ModelBackend
from .models import User
from django.db.models import Q

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(username__iexact=username) | 
                Q(email__iexact=username)
            )
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None