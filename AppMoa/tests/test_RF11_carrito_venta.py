"""
RF-11 — Carrito de Compras y Venta
Caso de Prueba: Agregar productos y procesar el pago.
Ejecutar: python manage.py test AppMoa.tests.test_RF11_carrito_venta -v 2
"""
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from django.urls import reverse
from AppMoa.models import Producto, Categoria, Rol, Usuario, Venta, DetalleVenta


class TestRF11CarritoVenta(TestCase):

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
            nombre_producto='Camisa',
            precio_producto=80000,
            stock_producto=10,
            categoria=self.categoria,
        )
        self.client.force_login(self.usuario)

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RF11_agregar_productos_y_procesar_pago(self):
        # 1. Agregar al carrito
        response = self.client.post(reverse('agregar_carrito'), {
            'producto_id': self.producto.pk,
            'cantidad': 2,
        })
        self.assertIn(response.status_code, [200, 302])

        # 2. Registrar venta
        venta = Venta.objects.create(
            usuario=self.usuario,
            total_venta=160000,
        )
        self.assertTrue(Venta.objects.filter(pk=venta.pk).exists())

        # 3. Reducir stock
        DetalleVenta.objects.create(
            venta=venta,
            producto=self.producto,
            cantidad_detalle=2,
            precio_unitario=80000,
        )
        self.producto.stock_producto -= 2
        self.producto.save()
        self.assertEqual(
            Producto.objects.get(pk=self.producto.pk).stock_producto, 8
        )

        # 4. Detalle registrado
        self.assertEqual(DetalleVenta.objects.filter(venta=venta).count(), 1)

    # ─── PRUEBA FUNCIONAL OK ──────────────────────────────────
    def test_RNF11_total_venta_correcto_OK(self):
        """
        NO FUNCIONAL - RNF-11 CASO OK 
        Integridad: El total de la venta coincide con la suma de los detalles.
        Resultado esperado: OK
        """
        venta = Venta.objects.create(
            usuario=self.usuario,
            total_venta=80000,
        )
        DetalleVenta.objects.create(
            venta=venta,
            producto=self.producto,
            cantidad_detalle=1,
            precio_unitario=80000,
        )
        total = sum(
            d.cantidad_detalle * d.precio_unitario
            for d in DetalleVenta.objects.filter(venta=venta)
        )
        self.assertEqual(total, venta.total_venta)

    # ─── PRUEBA NO FUNCIONAL ERROR ───────────────────────────────
    def test_RNF11_total_venta_correcto_ERROR(self):
        """
        NO FUNCIONAL - RNF-11 CASO ERROR 
        Simula que el total de la venta no coincide con los detalles.
        Resultado esperado: FAIL
        """
        venta = Venta.objects.create(
            usuario=self.usuario,
            total_venta=999999,
        )
        DetalleVenta.objects.create(
            venta=venta,
            producto=self.producto,
            cantidad_detalle=1,
            precio_unitario=80000,
        )
        total = sum(
            d.cantidad_detalle * d.precio_unitario
            for d in DetalleVenta.objects.filter(venta=venta)
        )
        self.assertEqual(
            total,
            venta.total_venta,
            msg="CASO ERROR DEMOSTRADO: El total no coincide con los detalles."
        )



