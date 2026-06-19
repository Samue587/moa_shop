"""
RNF-01 — Tiempo de Respuesta de Validaciones
Caso de Prueba: El sistema debe responder en máximo 2 segundos.
Herramienta: Locust (Pruebas de carga).
Ejecutar: python manage.py test AppMoa.tests.test_RNF01_tiempo_respuesta -v 2
"""
import time
from django.test import TestCase, Client
from django.urls import reverse
from AppMoa.models import Rol


class TestRNF01TiempoRespuesta(TestCase):

    def setUp(self):
        self.client = Client()
        Rol.objects.create(nombre_rol='cliente')

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RNF01_endpoint_registro_disponible(self):
        """
        FUNCIONAL - RNF-01
        Verifica que el endpoint de registro existe y responde correctamente.
        Resultado esperado: OK
        """
        response = self.client.get(reverse('registro'))
        self.assertIn(response.status_code, [200, 302])

    # ─── PRUEBA NO FUNCIONAL - CASO OK ───────────────────────────
    def test_RNF01_tiempo_respuesta_menor_2s_OK(self):
        """
        NO FUNCIONAL - RNF-01 CASO OK
        El sistema responde en menos de 2 segundos.
        Resultado esperado: OK
        """
        inicio = time.time()
        self.client.post(reverse('registro'), {
            'nombre':   'Test',
            'apellido': 'User',
            'email':    'test_ok@test.com',
            'password': 'Pass1234!',
        })
        tiempo = time.time() - inicio
        self.assertLess(
            tiempo, 2.0,
            msg=f"Tardó {tiempo:.2f}s — supera el límite de 2 segundos."
        )

    # ─── PRUEBA NO FUNCIONAL - CASO ERROR ────────────────────────
    def test_RNF01_tiempo_respuesta_imposible_ERROR(self):
        """
        NO FUNCIONAL - RNF-01 CASO ERROR
        Exige que el sistema responda en menos de 0 segundos: condición imposible.
        Resultado esperado: FAIL (intencional)
        """
        inicio = time.time()
        self.client.post(reverse('registro'), {
            'nombre':   'Error',
            'apellido': 'User',
            'email':    'test_error@test.com',
            'password': 'Pass1234!',
        })
        tiempo = time.time() - inicio
        self.assertLess(
            tiempo, 0.0,
            msg=f"CASO ERROR DEMOSTRADO: tardó {tiempo:.2f}s, se esperaba < 0s."
        )
