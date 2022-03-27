from django.contrib.auth.backends import BaseBackend
from boox_app.models import User

class CustomAuthBackend(BaseBackend):

    def authenticate(self, request, email, password):

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None