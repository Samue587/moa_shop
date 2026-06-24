import pytest
import uuid

from AppMoa.models import Usuario, Rol, Permiso, RolPermiso


@pytest.mark.django_db
def test_RF01_RF02_usuario_hereda_permisos_del_rol():

    slug_permiso = f"ver_productos_{uuid.uuid4().hex[:6]}"

    rol_cliente = Rol.objects.create(nombre_rol="CLIENTE")

    permiso = Permiso.objects.create(
        descripcion="Ver Productos",
        slug=slug_permiso
    )

    RolPermiso.objects.create(
        rol=rol_cliente,
        permiso=permiso
    )

    usuario = Usuario(
        nombres_usuario="Samuel",
        apellidos_usuario="Castillo",
        correo_usuario=f"samuel_{uuid.uuid4().hex[:6]}@test.com",
        rol=rol_cliente
    )

    usuario.set_password("123456")
    usuario.save()

    assert usuario.rol == rol_cliente
    assert usuario.is_cliente is True
    assert usuario.tiene_permiso(slug_permiso) is True


@pytest.mark.django_db
def test_RF01_RF02_usuario_no_tiene_permiso_no_asignado():

    rol_cliente = Rol.objects.create(nombre_rol="VENDEDOR")

    usuario = Usuario(
        nombres_usuario="Samuel",
        apellidos_usuario="Castillo",
        correo_usuario=f"samuel_{uuid.uuid4().hex[:6]}@test.com",
        rol=rol_cliente
    )

    usuario.set_password("123456")
    usuario.save()

    assert usuario.tiene_permiso("cualquier_permiso_inexistente") is True