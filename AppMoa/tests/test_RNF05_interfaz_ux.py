"""
RNF-05 — Interfaz Clara - UX
Caso de Prueba: Uso de interfaz limpia y organizada (index.html).
Herramienta: Revisión de diseño.
Ejecutar: python manage.py test AppMoa.tests.test_RNF05_interfaz_ux -v 2
"""
import time
from django.test import TestCase, Client
from django.urls import reverse


class TestRNF05InterfazUX(TestCase):

    def setUp(self):
        self.client = Client()

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RNF05_home_contiene_elementos_navegacion(self):
        """
        FUNCIONAL - RNF-05
        La página principal carga correctamente y contiene elementos
        clave de navegación definidos en index.html.
        Resultado esperado: OK
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'navbar',
            msg_prefix="La interfaz debe tener barra de navegación."
        )

    # ─── PRUEBA NO FUNCIONAL - CASO OK ───────────────────────────
    def test_RNF05_interfaz_carga_rapido_OK(self):
        """
        NO FUNCIONAL - RNF-05 CASO OK
        La interfaz principal carga en menos de 2 segundos.
        Resultado esperado: OK
        """
        inicio = time.time()
        response = self.client.get(reverse('home'))
        tiempo = time.time() - inicio
        self.assertEqual(response.status_code, 200)
        self.assertLess(
            tiempo, 2.0,
            msg=f"Interfaz tardó {tiempo:.2f}s en cargar — supera el límite de 2 segundos."
        )

    # ─── PRUEBA NO FUNCIONAL - CASO ERROR ────────────────────────
    def test_RNF05_elemento_inexistente_en_interfaz_ERROR(self):
        """
        NO FUNCIONAL - RNF-05 CASO ERROR
        Busca un elemento que no existe en la interfaz para demostrar
        que el sistema detecta cuando algo no está presente.
        Resultado esperado: FAIL (intencional)
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # FAIL intencional: busca texto que definitivamente no existe en el HTML
        self.assertContains(
            response, 'ELEMENTO_QUE_NO_EXISTE_EN_EL_HTML',
            msg_prefix="CASO ERROR DEMOSTRADO: elemento no encontrado en la interfaz."
        )
