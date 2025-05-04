from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailBackend(ModelBackend):
    """
    自訂 Email 登入的 Backend，同時也允許 username。
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        
        UserModel = get_user_model()
        user = None

        if username:
            if '@' in username:
                try:
                    user = UserModel.objects.get(email=username)
                except UserModel.DoesNotExist:
                    return None
            else:
                try:
                    user = UserModel.objects.get(username=username)
                except UserModel.DoesNotExist:
                    return None

        if user and password and user.check_password(password):
            return user
        
        return None