"""
RF-08 — Catálogos y Menú Desplegable
Caso de Prueba: Visualizar productos divididos por categorías en el menú.
Ejecutar: python manage.py test AppMoa.tests.test_RF08_catalogos -v 2
"""
from django.test import TestCase, Client
from django.urls import reverse
from AppMoa.models import Categoria, Producto


class TestRF08Catalogos(TestCase):

    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(nombre_categoria='Zapatos')
        Producto.objects.create(
            nombre_producto='Tenis',
            precio_producto=120000,
            stock_producto=5,
            categoria=self.categoria,
        )

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RF08_visualizar_categorias_en_menu(self):
        # 1. Tienda responde
        response = self.client.get(reverse('tienda'))
        self.assertEqual(response.status_code, 200)

        # 2. Categoría existe
        self.assertTrue(Categoria.objects.filter(nombre_categoria='Zapatos').exists())

        # 3. Productos vinculados a categoría
        productos = Producto.objects.filter(categoria=self.categoria)
        self.assertEqual(productos.count(), 1)

    # ─── PRUEBA FUNCIONAL OK ──────────────────────────────────
    def test_RNF08_relacion_categoria_producto_OK(self):
        """
        NO FUNCIONAL - RNF-08 CASO OK 
        Integridad: Los productos están correctamente relacionados a su categoría.
        Resultado esperado: OK
        """
        producto = Producto.objects.get(nombre_producto='Tenis')
        self.assertEqual(producto.categoria.nombre_categoria, 'Zapatos')

    # ─── PRUEBA NO FUNCIONAL ERROR ───────────────────────────────
    def test_RNF08_relacion_categoria_producto_ERROR(self):
        """
        NO FUNCIONAL - RNF-08 CASO ERROR 
        Simula que se busca una categoría inexistente.
        Resultado esperado: FAIL
        """
        self.assertTrue(
            Categoria.objects.filter(nombre_categoria='CategoriaInexistente').exists(),
            msg="CASO ERROR DEMOSTRADO: La categoría no existe en la BD."
        )




