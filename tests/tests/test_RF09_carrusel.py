"""
RF-09 — Carrusel y Elementos Móviles
Caso de Prueba: El carrusel cambia de imagen cada 3 segundos.
Ejecutar: python manage.py test AppMoa.tests.test_RF09_carrusel -v 2
"""
import time
from django.test import TestCase, Client
from django.urls import reverse


class TestRF09Carrusel(TestCase):

    def setUp(self):
        self.client = Client()

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RF09_carrusel_intervalo_3_segundos(self):
        # 1. Tienda carga
        response = self.client.get(reverse('tienda'))
        self.assertEqual(response.status_code, 200)

        # 2. Carrusel presente en el HTML
        self.assertContains(response, 'carousel')

        # 3. Intervalo de 3 segundos en el código
        self.assertContains(response, '3000')

    # ─── PRUEBA FUNCIONAL OK ──────────────────────────────────
    def test_RNF09_carrusel_carga_menos_2_segundos_OK(self):
        """
        NO FUNCIONAL - RNF-09 CASO OK 
        La tienda carga en menos de 2 segundos con el carrusel.
        Resultado esperado: OK
        """
        inicio = time.time()
        self.client.get(reverse('tienda'))
        tiempo_total = time.time() - inicio
        self.assertLess(
            tiempo_total, 2.0,
            msg=f"La tienda tardó {tiempo_total:.2f}s en cargar."
        )

    # ─── PRUEBA NO FUNCIONAL ERROR ───────────────────────────────
    def test_RNF09_carrusel_intervalo_correcto_ERROR(self):
        """
        NO FUNCIONAL - RNF-09 CASO ERROR 
        Simula que el carrusel no tiene el intervalo correcto.
        Resultado esperado: FAIL
        """
        response = self.client.get(reverse('tienda'))
        self.assertContains(
            response,
            '9999',
            msg_prefix="CASO ERROR DEMOSTRADO: El intervalo 9999ms no existe en el carrusel."
        )




