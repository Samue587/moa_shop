from functools import wraps
from django.shortcuts import redirect
import logging

from .models import Usuario, RolPermiso

logger = logging.getLogger(__name__)


# =====================================================
# DECORADOR ADMIN
# =====================================================

def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        usuario_id = request.session.get(
            'usuario_id'
        )

        if not usuario_id:

            return redirect('login')

        try:

            usuario = Usuario.objects.select_related(
                'rol'
            ).get(
                id=usuario_id
            )

        except Usuario.DoesNotExist:

            return redirect('login')

        if not usuario.rol:

            return redirect('login')

        if usuario.rol.nombre_rol != 'Administrador':

            return redirect('admin_dashboard')

        request.usuario = usuario

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper



# ╔══════════════════════════════════════════════════════════════════════╗
# ║                          DECORADOR DE PERMISOS                                     ║
# ╚══════════════════════════════════════════════════════════════════════╝
def permiso_requerido(slug_permiso):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            usuario = getattr(
                request,
                'usuario',
                None
            )

            if not usuario:

                usuario_id = request.session.get(
                    'usuario_id'
                )

                if not usuario_id:

                    return redirect('login')

                try:

                    usuario = Usuario.objects.select_related(
                        'rol'
                    ).get(
                        id=usuario_id
                    )

                    request.usuario = usuario

                except Usuario.DoesNotExist:

                    return redirect('login')

            tiene_permiso = RolPermiso.objects.filter(

                rol=usuario.rol,

                permiso__slug=slug_permiso

            ).exists()

            if not tiene_permiso:
                rol_nombre = usuario.rol.nombre_rol if getattr(usuario, 'rol', None) else "SIN_ROL"
                logger.warning(
                    "Acceso denegado: permiso=%s, rol=%s, usuario_id=%s",
                    slug_permiso,
                    rol_nombre,
                    getattr(usuario, 'id', None),
                )
                return redirect('admin_dashboard')

            return view_func(
                request,
                *args,
                **kwargs
            )

        return wrapper

    return decorator