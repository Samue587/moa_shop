"""
RF-03 — Recuperación de Cuentas
Caso de Prueba: Solicitar recuperación por correo.
Ejecutar: python manage.py test AppMoa.tests.test_RF03_recuperacion_cuentas -v 2
"""
from django.contrib.auth.hashers import make_password, check_password
from django.test import TestCase, Client
from django.urls import reverse
from AppMoa.models import Usuario, Rol, TokenReset


class TestRF03RecuperacionCuentas(TestCase):

    def setUp(self):
        self.client = Client()
        rol = Rol.objects.create(nombre_rol='cliente')
        self.usuario = Usuario.objects.create(
            nombres_usuario='Reset',
            apellidos_usuario='Test',
            correo_usuario='reset@test.com',
            contrasena=make_password('OldPass!'),
            rol=rol,
        )

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RF03_solicitar_recuperacion_por_correo(self):
        # 1. Solicitar recuperación
        response = self.client.post(reverse('password_reset'), {
            'email': 'reset@test.com'
        })
        self.assertIn(response.status_code, [200, 302])

        # 2. Token creado correctamente
        token = TokenReset.objects.create(usuario=self.usuario)
        self.assertIsNotNone(token.token)
        self.assertFalse(token.usado)

        # 3. Token vigente
        self.assertTrue(token.esta_vigente())

        # 4. Nueva contraseña hasheada
        self.usuario.set_password('NewPass1234!')
        self.usuario.save()
        u = Usuario.objects.get(pk=self.usuario.pk)
        self.assertTrue(check_password('NewPass1234!', u.contrasena))

    # ─── PRUEBA FUNCIONAL OK ──────────────────────────────────
    def test_RNF03_token_usado_no_vigente_OK(self):
        """
        NO FUNCIONAL - RNF-03 CASO OK 
        Integridad: Token ya usado no puede volver a usarse.
        Resultado esperado: OK
        """
        token = TokenReset.objects.create(usuario=self.usuario, usado=True)
        self.assertFalse(token.esta_vigente())

    # ─── PRUEBA NO FUNCIONAL ERROR ───────────────────────────────
    def test_RNF03_token_usado_no_vigente_ERROR(self):
        """
        NO FUNCIONAL - RNF-03 CASO ERROR 
        Simula que un token ya usado sigue vigente.
        Resultado esperado: FAIL
        """
        token = TokenReset.objects.create(usuario=self.usuario, usado=True)
        self.assertTrue(
            token.esta_vigente(),
            msg="CASO ERROR DEMOSTRADO: El token está usado "
                "pero se esperaba que siguiera vigente."
        )




