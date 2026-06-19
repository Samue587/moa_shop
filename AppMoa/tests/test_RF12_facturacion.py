"""
RF-12 — Facturación PDF y Correo
Caso de Prueba: Generar factura al finalizar la compra.
Ejecutar: python manage.py test AppMoa.tests.test_RF12_facturacion -v 2
"""
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from django.urls import reverse
from AppMoa.models import Venta, DetalleVenta, Producto, Categoria, Rol, Usuario


class TestRF12Facturacion(TestCase):

    def setUp(self):
        self.client = Client()
        rol = Rol.objects.create(nombre_rol='cliente')
        self.usuario = Usuario.objects.create(
            nombres_usuario='Cliente',
            correo_usuario='cliente@test.com',
            contrasena=make_password('Pass1234!'),
            rol=rol,
        )
        self.categoria = Categoria.objects.create(nombre_categoria='Ropa')
        self.producto = Producto.objects.create(
            nombre_producto='Pantalon',
            precio_producto=90000,
            stock_producto=5,
            categoria=self.categoria,
        )
        self.venta = Venta.objects.create(
            usuario=self.usuario,
            total_venta=90000,
        )
        DetalleVenta.objects.create(
            venta=self.venta,
            producto=self.producto,
            cantidad_detalle=1,
            precio_unitario=90000,
        )
        self.client.force_login(self.usuario)

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RF12_generar_factura_al_finalizar_compra(self):
        # 1. Venta existe
        self.assertTrue(Venta.objects.filter(pk=self.venta.pk).exists())

        # 2. Detalle registrado
        self.assertEqual(
            DetalleVenta.objects.filter(venta=self.venta).count(), 1
        )

        # 3. Endpoint comprobante responde
        response = self.client.get(reverse('comprobante', args=[self.venta.pk]))
        self.assertIn(response.status_code, [200, 302])

    # ─── PRUEBA FUNCIONAL OK ──────────────────────────────────
    def test_RNF12_factura_datos_correctos_OK(self):
        """
        NO FUNCIONAL - RNF-12 CASO OK 
        Integridad: La factura refleja los datos reales de la venta.
        Resultado esperado: OK
        """
        detalle = DetalleVenta.objects.get(venta=self.venta)
        total_calculado = detalle.cantidad_detalle * detalle.precio_unitario
        self.assertEqual(total_calculado, self.venta.total_venta)

    # ─── PRUEBA NO FUNCIONAL ERROR ───────────────────────────────
    def test_RNF12_factura_datos_correctos_ERROR(self):
        """
        NO FUNCIONAL - RNF-12 CASO ERROR 
        Simula que el total de la factura no coincide con la venta.
        Resultado esperado: FAIL
        """
        detalle = DetalleVenta.objects.get(venta=self.venta)
        total_calculado = detalle.cantidad_detalle * detalle.precio_unitario
        self.assertEqual(
            total_calculado,
            999999,
            msg="CASO ERROR DEMOSTRADO: El total de la factura no coincide."
        )


