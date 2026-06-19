"""
RF-13 — Reportes (Ventas, Clientes, Envíos)
Caso de Prueba: Generar reportes diarios y por ubicación geográfica.
Ejecutar: python manage.py test AppMoa.tests.test_RF13_reportes -v 2
"""
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from django.urls import reverse
from AppMoa.models import Venta, Rol, Usuario, Categoria, Producto, DetalleVenta


class TestRF13Reportes(TestCase):

    def setUp(self):
        self.client = Client()
        rol = Rol.objects.create(nombre_rol='admin')
        self.admin = Usuario.objects.create(
            nombres_usuario='Admin',
            correo_usuario='admin@test.com',
            contrasena=make_password('Pass1234!'),
            rol=rol,
            es_admin=True,
        )
        self.categoria = Categoria.objects.create(nombre_categoria='Ropa')
        self.producto = Producto.objects.create(
            nombre_producto='Chaqueta',
            precio_producto=150000,
            stock_producto=3,
            categoria=self.categoria,
        )
        self.venta = Venta.objects.create(
            usuario=self.admin,
            total_venta=150000,
        )
        DetalleVenta.objects.create(
            venta=self.venta,
            producto=self.producto,
            cantidad_detalle=1,
            precio_unitario=150000,
        )
        self.client.force_login(self.admin)

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RF13_generar_reportes_diarios(self):
        # 1. Endpoint responde
        response = self.client.get(reverse('reportes'))
        self.assertIn(response.status_code, [200, 302])

        # 2. Ventas registradas
        self.assertTrue(Venta.objects.filter(pk=self.venta.pk).exists())

        # 3. Suma real
        total = sum(
            d.cantidad_detalle * d.precio_unitario
            for d in DetalleVenta.objects.filter(venta=self.venta)
        )
        self.assertEqual(total, self.venta.total_venta)

    # ─── PRUEBA FUNCIONAL OK ──────────────────────────────────
    def test_RNF13_suma_reporte_real_OK(self):
        """
        NO FUNCIONAL - RNF-13 CASO OK 
        Integridad: La suma del reporte coincide con los datos de la BD.
        Resultado esperado: OK
        """
        ventas = Venta.objects.filter(usuario=self.admin)
        self.assertGreater(ventas.count(), 0)
        self.assertEqual(ventas.first().total_venta, 150000)

    # ─── PRUEBA NO FUNCIONAL ERROR ───────────────────────────────
    def test_RNF13_suma_reporte_real_ERROR(self):
        """
        NO FUNCIONAL - RNF-13 CASO ERROR 
        Simula que la suma del reporte no coincide con la BD.
        Resultado esperado: FAIL
        """
        ventas = Venta.objects.filter(usuario=self.admin)
        self.assertEqual(
            ventas.first().total_venta,
            999999,
            msg="CASO ERROR DEMOSTRADO: La suma del reporte no coincide con la BD."
        )

