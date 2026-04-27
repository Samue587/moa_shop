from django.contrib.auth.backends import BaseBackend
from AppMoa.models import Usuario


class EmailBackend(BaseBackend):
    """
    Backend de autenticación personalizado.
    Permite login con correo_usuario + contrasena (hash).
    Se registra en settings.py → AUTHENTICATION_BACKENDS.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # username aquí es el email que viene del formulario
        try:
            usuario = Usuario.objects.select_related('rol').get(correo_usuario=username)
        except Usuario.DoesNotExist:
            return None

        from django.contrib.auth.hashers import check_password
        if check_password(password, usuario.contrasena):
            return usuario
        return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.select_related('rol').get(pk=user_id)
        except Usuario.DoesNotExist:
            return None