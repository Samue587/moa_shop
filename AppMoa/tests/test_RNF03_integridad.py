"""
RNF-03 — Integridad de Datos
Caso de Prueba: Relaciones sólidas entre tablas (Productos/Ventas) con constraints de BD.
Herramienta: MariaDB (Constraints).
Ejecutar: python manage.py test AppMoa.tests.test_RNF03_integridad -v 2
"""
from django.test import TestCase
from django.db import IntegrityError
from AppMoa.models import Producto, Venta, DetalleVenta, Usuario, Rol, Categoria


class TestRNF03IntegridadDatos(TestCase):

    def setUp(self):
        self.rol = Rol.objects.create(nombre_rol='cliente')
        self.usuario = Usuario.objects.create(
            correo_usuario='cli@test.com',
            rol=self.rol
        )
        self.cat = Categoria.objects.create(nombre_categoria='Ropa')
        self.producto = Producto.objects.create(
            nombre_producto='Camiseta',
            precio=30000,
            stock=10,
            categoria=self.cat
        )
        self.venta = Venta.objects.create(
            usuario=self.usuario,
            total=30000
        )

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RNF03_detalle_venta_con_relaciones_validas(self):
        """
        FUNCIONAL - RNF-03
        DetalleVenta se crea correctamente con venta y producto válidos.
        Resultado esperado: OK
        """
        detalle = DetalleVenta.objects.create(
            venta=self.venta,
            producto=self.producto,
            cantidad=1,
            subtotal=30000
        )
        self.assertIsNotNone(detalle.pk)
        self.assertEqual(detalle.venta, self.venta)

    # ─── PRUEBA NO FUNCIONAL - CASO OK ───────────────────────────
    def test_RNF03_integridad_al_eliminar_venta_OK(self):
        """
        NO FUNCIONAL - RNF-03 CASO OK
        Al eliminar una venta, sus detalles se eliminan en cascada (no quedan huérfanos).
        Resultado esperado: OK
        """
        DetalleVenta.objects.create(
            venta=self.venta,
            producto=self.producto,
            cantidad=1,
            subtotal=30000
        )
        self.venta.delete()
        self.assertEqual(
            DetalleVenta.objects.filter(venta=self.venta).count(), 0,
            msg="Los detalles deben eliminarse en cascada con la venta."
        )

    # ─── PRUEBA NO FUNCIONAL - CASO ERROR ────────────────────────
    def test_RNF03_detalle_sin_venta_viola_integridad_ERROR(self):
        """
        NO FUNCIONAL - RNF-03 CASO ERROR
        Intenta crear un DetalleVenta sin venta: viola integridad referencial.
        Resultado esperado: FAIL (intencional)
        """
        try:
            DetalleVenta.objects.create(
                venta=None,
                producto=self.producto,
                cantidad=1,
                subtotal=30000
            )
        except IntegrityError:
            pass
        # FAIL intencional: afirmamos que el objeto sin venta SÍ existe (incorrecto)
        self.assertTrue(
            DetalleVenta.objects.filter(venta=None).exists(),
            msg="CASO ERROR DEMOSTRADO: no debe existir DetalleVenta sin venta."
        )
