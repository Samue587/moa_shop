"""
RF-04 — Gestión de Perfil e Inactivación
Caso de Prueba: Editar datos personales o marcar usuario como "Inactivo".
Ejecutar: python manage.py test AppMoa.tests.test_RF04_perfil_inactivacion -v 2
"""
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from django.urls import reverse
from AppMoa.models import Usuario, Rol


class TestRF04PerfilInactivacion(TestCase):

    def setUp(self):
        self.client = Client()
        rol = Rol.objects.create(nombre_rol='cliente')
        self.usuario = Usuario.objects.create(
            nombres_usuario='Carlos',
            apellidos_usuario='Mora',
            correo_usuario='carlos@test.com',
            contrasena=make_password('Pass1234!'),
            rol=rol,
        )

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RF04_editar_datos_y_marcar_inactivo(self):
        # 1. Editar datos
        self.usuario.nombres_usuario = 'CarlosEditado'
        self.usuario.save()
        self.assertEqual(
            Usuario.objects.get(pk=self.usuario.pk).nombres_usuario,
            'CarlosEditado'
        )

        # 2. Marcar como INACTIVO
        self.usuario.estado_usuario = 'INACTIVO'
        self.usuario.save()
        self.assertEqual(
            Usuario.objects.get(pk=self.usuario.pk).estado_usuario,
            'INACTIVO'
        )

        # 3. Inactivo no puede hacer login
        response = self.client.post(reverse('login'), {
            'email': 'carlos@test.com',
            'password': 'Pass1234!',
        })
        self.assertNotEqual(response.status_code, 302)

        # 4. Reactivar
        self.usuario.estado_usuario = 'ACTIVO'
        self.usuario.save()
        self.assertEqual(
            Usuario.objects.get(pk=self.usuario.pk).estado_usuario,
            'ACTIVO'
        )

    # ─── PRUEBA FUNCIONAL OK ──────────────────────────────────
    def test_RNF04_cambio_estado_persiste_OK(self):
        """
        NO FUNCIONAL - RNF-04 CASO OK 
        Integridad: Los cambios al perfil persisten en la BD.
        Resultado esperado: OK
        """
        self.usuario.nombres_usuario = 'NuevoNombre'
        self.usuario.save()
        u = Usuario.objects.get(pk=self.usuario.pk)
        self.assertEqual(u.nombres_usuario, 'NuevoNombre')

    # ─── PRUEBA NO FUNCIONAL ERROR ───────────────────────────────
    def test_RNF04_cambio_estado_persiste_ERROR(self):
        """
        NO FUNCIONAL - RNF-04 CASO ERROR 
        Simula que los cambios no se guardan en la BD.
        Resultado esperado: FAIL
        """
        self.usuario.nombres_usuario = 'CambioSinGuardar'
        # Sin .save() el cambio no persiste
        u = Usuario.objects.get(pk=self.usuario.pk)
        self.assertEqual(
            u.nombres_usuario,
            'CambioSinGuardar',
            msg="CASO ERROR DEMOSTRADO: El cambio no persiste porque no se llamó a .save()."
        )




