"""
RF-10 — Creación de Productos y Descuentos
Caso de Prueba: Registrar productos y asignarles % de descuento.
Ejecutar: python manage.py test AppMoa.tests.test_RF10_productos -v 2
"""
from django.test import TestCase, Client
from AppMoa.models import Producto, Categoria


class TestRF10Productos(TestCase):

    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(nombre_categoria='Accesorios')

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RF10_registrar_producto_con_descuento(self):
        # 1. Crear producto con descuento
        producto = Producto.objects.create(
            nombre_producto='Bolso',
            precio_producto=200000,
            descuento_producto=10,
            stock_producto=8,
            categoria=self.categoria,
        )
        self.assertTrue(Producto.objects.filter(nombre_producto='Bolso').exists())

        # 2. Descuento guardado
        p = Producto.objects.get(pk=producto.pk)
        self.assertEqual(p.descuento_producto, 10)

        # 3. Lógica matemática correcta
        precio_final = p.precio_producto * (1 - p.descuento_producto / 100)
        self.assertEqual(precio_final, 180000)  # 200000 - 10% = 180000

    # ─── PRUEBA FUNCIONAL OK ──────────────────────────────────
    def test_RNF10_descuento_logica_correcta_OK(self):
        """
        NO FUNCIONAL - RNF-10 CASO OK 
        Integridad: El precio con descuento es menor al precio original.
        Resultado esperado: OK
        """
        producto = Producto.objects.create(
            nombre_producto='Gorra',
            precio_producto=50000,
            descuento_producto=20,
            stock_producto=10,
            categoria=self.categoria,
        )
        precio_final = producto.precio_producto * (1 - producto.descuento_producto / 100)
        self.assertLess(precio_final, producto.precio_producto)

    # ─── PRUEBA NO FUNCIONAL ERROR ───────────────────────────────
    def test_RNF10_descuento_logica_correcta_ERROR(self):
        """
        NO FUNCIONAL - RNF-10 CASO ERROR 
        Simula que el descuento calculado es incorrecto.
        Resultado esperado: FAIL
        """
        producto = Producto.objects.create(
            nombre_producto='Gorra Error',
            precio_producto=50000,
            descuento_producto=20,
            stock_producto=10,
            categoria=self.categoria,
        )
        precio_final = producto.precio_producto * (1 - producto.descuento_producto / 100)
        self.assertEqual(
            precio_final,
            50000,  # Incorrecto: debería ser 40000
            msg="CASO ERROR DEMOSTRADO: El precio con descuento no es correcto."
        )



