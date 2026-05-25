from .models import RolPermiso


def permisos_usuario(request):

    permisos = []

    if request.user.is_authenticated:

        if hasattr(request.user, 'rol'):

            permisos = RolPermiso.objects.filter(

                rol=request.user.rol

            ).values_list(

                'permiso__slug',

                flat=True
            )

    return {

        'permisos_usuario': permisos
    }