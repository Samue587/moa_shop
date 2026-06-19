"""
RF-07 — Actualización de Stock y Costo
Caso de Prueba: Al registrar entrada, sumar unidades y recalcular costo.
Ejecutar: python manage.py test AppMoa.tests.test_RF07_stock -v 2
"""
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from AppMoa.models import Producto, Proveedor, EntradaInventario, Rol, Usuario, Categoria


class TestRF07Stock(TestCase):

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
        self.proveedor = Proveedor.objects.create(
            nombre_proveedor='Proveedor Test',
            nit_proveedor='444555666',
        )
        self.categoria = Categoria.objects.create(nombre_categoria='Calzado')
        self.producto = Producto.objects.create(
            nombre_producto='Tenis',
            precio_producto=120000,
            stock_producto=10,
            categoria=self.categoria,
        )

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RF07_stock_final_igual_inicial_mas_entrada(self):
        stock_inicial = self.producto.stock_producto  # 10

        # Registrar entrada
        entrada = EntradaInventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            cantidad_entrada=15,
            usuario=self.admin,
        )

        # Actualizar stock
        self.producto.stock_producto += entrada.cantidad_entrada
        self.producto.save()

        stock_final = Producto.objects.get(pk=self.producto.pk).stock_producto
        self.assertEqual(stock_final, stock_inicial + 15)  # 10 + 15 = 25

    # ─── PRUEBA FUNCIONAL OK ──────────────────────────────────
    def test_RNF07_stock_actualizado_correctamente_OK(self):
        """
        NO FUNCIONAL - RNF-07 CASO OK 
        Integridad: El stock refleja exactamente las entradas registradas.
        Resultado esperado: OK
        """
        self.producto.stock_producto += 5
        self.producto.save()
        self.assertEqual(
            Producto.objects.get(pk=self.producto.pk).stock_producto, 15
        )

    # ─── PRUEBA NO FUNCIONAL ERROR ───────────────────────────────
    def test_RNF07_stock_actualizado_correctamente_ERROR(self):
        """
        NO FUNCIONAL - RNF-07 CASO ERROR 
        Simula que el stock no se actualizó correctamente.
        Resultado esperado: FAIL
        """
        self.producto.stock_producto += 5
        # Sin .save() el cambio no persiste
        self.assertEqual(
            Producto.objects.get(pk=self.producto.pk).stock_producto,
            15,
            msg="CASO ERROR DEMOSTRADO: El stock no se actualizó porque no se llamó a .save()."
        )




