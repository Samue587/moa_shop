from .models import Rol, Permiso, RolPermiso


MODULOS = [

    'productos',
    'usuarios',
    'ventas',
    'clientes',
    'proveedores',
    'compras',
    'roles',
    'permisos',
    'envios',
    'catalogos',
    'categorias',
    'variaciones',
    'entradas'
]


ACCIONES = [

    ('ver', 'Ver'),
    ('crear', 'Crear'),
    ('editar', 'Editar'),
    ('eliminar', 'Eliminar'),
]


ROLES = [

    'Administrador',
    'Cliente'
]


def crear_permisos():

    for modulo in MODULOS:

        for accion_slug, accion_texto in ACCIONES:

            slug = f'{accion_slug}_{modulo}'

            descripcion = f'{accion_texto} {modulo}'

            Permiso.objects.get_or_create(

                slug=slug,

                defaults={
                    'descripcion': descripcion
                }
            )


def crear_roles():

    for nombre in ROLES:

        Rol.objects.get_or_create(
            nombre_rol=nombre
        )


def asignar_permisos():

    # =========================
    # ADMINISTRADOR
    # =========================

    admin = Rol.objects.get(
        nombre_rol='Administrador'
    )

    permisos_admin = Permiso.objects.all()

    for permiso in permisos_admin:

        RolPermiso.objects.get_or_create(

            rol=admin,
            permiso=permiso
        )

    # =========================
    # CLIENTE
    # =========================

    cliente = Rol.objects.get(
        nombre_rol='Cliente'
    )

    permisos_cliente = Permiso.objects.filter(
        slug__startswith='ver_'
    )

    for permiso in permisos_cliente:

        RolPermiso.objects.get_or_create(

            rol=cliente,
            permiso=permiso
        )


