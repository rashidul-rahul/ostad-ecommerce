from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class PhoneBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, *args, **kwargs):
        User = get_user_model()
        # If phone_number is not provided, fall back to 'username' from kwargs.
        if phone_number is None:
            phone_number = kwargs.get('username', None)
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
