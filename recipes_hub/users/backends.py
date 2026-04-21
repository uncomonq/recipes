from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(get_user_model().USERNAME_FIELD)
        if username is None or password is None:
            return None

        user_model = get_user_model()
        lookup_value = username.strip()

        try:
            user = user_model.objects.get(email__iexact=lookup_value)
        except user_model.DoesNotExist:
            user = user_model.objects.filter(
                username__iexact=lookup_value
            ).first()

        if (
            user
            and user.check_password(password)
            and self.user_can_authenticate(user)
        ):
            return user
        return None
