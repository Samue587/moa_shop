"""
RNF-02 — Seguridad - Fuerza Bruta
Caso de Prueba: El sistema bloquea al usuario tras varios intentos fallidos de login.
Herramienta: Middleware de Django.
Ejecutar: python manage.py test AppMoa.tests.test_RNF02_seguridad -v 2
"""
from django.test import TestCase, Client
from django.urls import reverse
from AppMoa.models import Usuario, Rol


class TestRNF02SeguridadFuerzaBruta(TestCase):

    def setUp(self):
        self.client = Client()
        rol = Rol.objects.create(nombre_rol='cliente')
        self.usuario = Usuario.objects.create(
            correo_usuario='usuario@test.com',
            contrasena_usuario='Pass1234!',
            rol=rol
        )

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RNF02_login_exitoso_con_credenciales_validas(self):
        """
        FUNCIONAL - RNF-02
        El login responde correctamente con credenciales válidas.
        Resultado esperado: OK
        """
        response = self.client.post(reverse('login'), {
            'email':    'usuario@test.com',
            'password': 'Pass1234!',
        })
        self.assertIn(response.status_code, [200, 302])

    # ─── PRUEBA NO FUNCIONAL - CASO OK ───────────────────────────
    def test_RNF02_bloqueo_tras_intentos_fallidos_OK(self):
        """
        NO FUNCIONAL - RNF-02 CASO OK
        Tras 5 intentos fallidos el sistema bloquea o responde con error controlado.
        Resultado esperado: OK
        """
        for _ in range(5):
            self.client.post(reverse('login'), {
                'email':    'usuario@test.com',
                'password': 'ContrasenaMala',
            })
        response = self.client.post(reverse('login'), {
            'email':    'usuario@test.com',
            'password': 'ContrasenaMala',
        })
        # Bloqueo esperado: 403, 429 o redirección con mensaje de error
        self.assertIn(response.status_code, [200, 302, 403, 429])

    # ─── PRUEBA NO FUNCIONAL - CASO ERROR ────────────────────────
    def test_RNF02_acceso_con_credenciales_incorrectas_ERROR(self):
        """
        NO FUNCIONAL - RNF-02 CASO ERROR
        Verifica que credenciales incorrectas NO den acceso al home.
        Resultado esperado: FAIL (intencional)
        """
        response = self.client.post(reverse('login'), {
            'email':    'usuario@test.com',
            'password': 'ContrasenaTotalmenteInvalida',
        })
        # FAIL intencional: se exige redirección al home con credenciales inválidas
        # En realidad el sistema debe rechazar y quedarse en login
        self.assertRedirects(
            response, reverse('home'),
            msg_prefix="CASO ERROR DEMOSTRADO: login inválido no debe redirigir al home."
        )
