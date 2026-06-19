"""
RF-02 — Gestión de Roles y Permisos
Caso de Prueba: Crear, asignar y modificar roles (Admin, Vendedor, etc).
Ejecutar: python manage.py test AppMoa.tests.test_RF02_roles_permisos -v 2
"""
import uuid
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from AppMoa.models import Rol, Permiso, RolPermiso, Usuario


class TestRF02RolesPermisos(TestCase):

    def setUp(self):
        self.client = Client()
        self.rol = Rol.objects.create(nombre_rol=f'Vendedor_{uuid.uuid4().hex[:4]}')
        self.permiso = Permiso.objects.create(
            descripcion='Ver Productos',
            slug=f'ver-productos-{uuid.uuid4().hex[:4]}'
        )

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RF02_crear_asignar_modificar_roles(self):
        # 1. Rol creado
        self.assertTrue(Rol.objects.filter(pk=self.rol.pk).exists())

        # 2. Asignar permiso al rol
        RolPermiso.objects.create(rol=self.rol, permiso=self.permiso)
        self.assertTrue(
            RolPermiso.objects.filter(rol=self.rol, permiso=self.permiso).exists()
        )

        # 3. Usuario hereda permiso
        usuario = Usuario.objects.create(
            nombres_usuario='Test',
            correo_usuario=f'{uuid.uuid4().hex[:6]}@test.com',
            contrasena=make_password('Pass1234!'),
            rol=self.rol,
        )
        self.assertTrue(usuario.tiene_permiso(self.permiso.slug))

        # 4. Modificar el rol
        self.rol.nombre_rol = 'Admin'
        self.rol.save()
        self.assertEqual(Rol.objects.get(pk=self.rol.pk).nombre_rol, 'Admin')

    # ─── PRUEBA FUNCIONAL OK ──────────────────────────────────
    def test_RNF02_usuario_sin_permiso_bloqueado_OK(self):
        """
        NO FUNCIONAL - RNF-02 CASO OK 
        Seguridad: Usuario sin permiso asignado es bloqueado.
        Resultado esperado: OK
        """
        usuario = Usuario.objects.create(
            nombres_usuario='SinPermiso',
            correo_usuario=f'{uuid.uuid4().hex[:6]}@test.com',
            contrasena=make_password('Pass1234!'),
            rol=self.rol,
        )
        self.assertFalse(usuario.tiene_permiso(self.permiso.slug))

    # ─── PRUEBA NO FUNCIONAL ERROR ───────────────────────────────
    def test_RNF02_usuario_sin_permiso_bloqueado_ERROR(self):
        """
        NO FUNCIONAL - RNF-02 CASO ERROR 
        Simula que un usuario sin permiso puede acceder.
        Resultado esperado: FAIL
        """
        usuario = Usuario.objects.create(
            nombres_usuario='SinPermiso',
            correo_usuario=f'{uuid.uuid4().hex[:6]}@test.com',
            contrasena=make_password('Pass1234!'),
            rol=self.rol,
        )
        self.assertTrue(
            usuario.tiene_permiso(self.permiso.slug),
            msg="CASO ERROR DEMOSTRADO: El usuario no tiene permiso "
                "pero se esperaba que lo tuviera."
        )


