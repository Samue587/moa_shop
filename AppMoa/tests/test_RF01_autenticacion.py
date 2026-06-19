"""
RF-01 — Autenticación de Usuario Nuevo
Caso de Prueba: Registrar un usuario con datos válidos.
Ejecutar: python manage.py test AppMoa.tests.test_RF01_autenticacion -v 2
"""
import time
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from django.urls import reverse
from AppMoa.models import Usuario, Rol


class TestRF01Autenticacion(TestCase):

    def setUp(self):
        self.client = Client()
        Rol.objects.create(nombre_rol='cliente')

    # PRUEBA FUNCIONAL
    def test_RF01_registrar_usuario_datos_validos(self):
        response = self.client.post(reverse('registro'), {
            'nombre':   'Juan', 
            'apellido': 'Pérez',
            'email':    'juan@test.com',
            'password': 'Pass1234!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Usuario.objects.filter(correo_usuario='juan@test.com').exists()
        )

    # ─── PRUEBA FUNCIONAL OK ──────────────────────────────────
    def test_RNF01_registro_responde_menos_2_segundos_OK(self):
        """
        NO FUNCIONAL - RNF-01 CASO OK 
        El sistema responde en máximo 2 segundos.
        Resultado esperado: OK
        """
        inicio = time.time()
        self.client.post(reverse('registro'), {
            'nombre':   'Maria',
            'apellido': 'Lopez',
            'email':    'maria_ok@test.com',
            'password': 'Pass1234!',
        })
        tiempo_total = time.time() - inicio
        self.assertLess(
            tiempo_total, 2.0,
            msg=f"Tardó {tiempo_total:.2f}s — supera el límite de 2 segundos."
        )

    # ─── PRUEBA NO FUNCIONAL ERROR ───────────────────────────────
    def test_RNF01_registro_supera_limite_tiempo_ERROR(self):
        """
        NO FUNCIONAL - RNF-01 CASO ERROR 
        Simula que el sistema supera el límite de tiempo.
        Resultado esperado: FAIL
        """
        inicio = time.time()
        self.client.post(reverse('registro'), {
            'nombre':   'Pedro',
            'apellido': 'García',
            'email':    'pedro_error@test.com',
            'password': 'Pass1234!',
        })
        tiempo_total = time.time() - inicio
        self.assertLess(
            tiempo_total, 0.0,
            msg=f"CASO ERROR DEMOSTRADO: tardó {tiempo_total:.2f}s, "
                f"se esperaba menos de 0 segundos."
        )


