def tiene_permiso(usuario, slug):

    if not usuario.is_authenticated:
        return False

    if not usuario.rol:
        return False

    return usuario.rol.permisos.filter(
        slug=slug
    ).exists()