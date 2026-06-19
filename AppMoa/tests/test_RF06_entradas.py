"""
RF-06 — Registro de Entradas e Historial
Caso de Prueba: Ingresar mercancía al sistema.
Ejecutar: python manage.py test AppMoa.tests.test_RF06_entradas -v 2
"""
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from AppMoa.models import Producto, Proveedor, EntradaInventario, Rol, Usuario, Categoria


class TestRF06Entradas(TestCase):

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
            nit_proveedor='111222333',
        )
        self.categoria = Categoria.objects.create(nombre_categoria='Ropa')
        self.producto = Producto.objects.create(
            nombre_producto='Camiseta',
            precio_producto=50000,
            stock_producto=10,
            categoria=self.categoria,
        )

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RF06_ingresar_mercancia_al_sistema(self):
        # 1. Registrar entrada
        entrada = EntradaInventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            cantidad_entrada=20,
            usuario=self.admin,
        )
        self.assertTrue(EntradaInventario.objects.filter(pk=entrada.pk).exists())

        # 2. Log creado
        self.assertEqual(
            EntradaInventario.objects.filter(producto=self.producto).count(), 1
        )

        # 3. Datos correctos
        e = EntradaInventario.objects.get(pk=entrada.pk)
        self.assertEqual(e.cantidad_entrada, 20)
        self.assertEqual(e.proveedor, self.proveedor)

    # ─── PRUEBA FUNCIONAL OK ──────────────────────────────────
    def test_RNF06_entrada_historial_integro_OK(self):
        """
        NO FUNCIONAL - RNF-06 CASO OK 
        Integridad: El historial de entradas persiste correctamente.
        Resultado esperado: OK
        """
        EntradaInventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            cantidad_entrada=5,
            usuario=self.admin,
        )
        self.assertEqual(
            EntradaInventario.objects.filter(producto=self.producto).count(), 1
        )

    # ─── PRUEBA NO FUNCIONAL ERROR ───────────────────────────────
    def test_RNF06_entrada_historial_integro_ERROR(self):
        """
        NO FUNCIONAL - RNF-06 CASO ERROR 
        Simula que el historial no registró la entrada.
        Resultado esperado: FAIL
        """
        EntradaInventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            cantidad_entrada=5,
            usuario=self.admin,
        )
        self.assertEqual(
            EntradaInventario.objects.filter(producto=self.producto).count(),
            99,
            msg="CASO ERROR DEMOSTRADO: El conteo del historial no coincide."
        )


