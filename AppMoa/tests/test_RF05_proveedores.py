"""
RF-05 — Creación de Proveedores
Caso de Prueba: Registrar un nuevo proveedor mediante formulario.
Ejecutar: python manage.py test AppMoa.tests.test_RF05_proveedores -v 2
"""
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from AppMoa.models import Proveedor, Rol, Usuario


class TestRF05Proveedores(TestCase):

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
        self.client.force_login(self.admin)

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RF05_registrar_proveedor_formulario(self):
        # 1. Registrar proveedor
        proveedor = Proveedor.objects.create(
            nombre_proveedor='Distribuidora MOA',
            nit_proveedor='900123456',
            telefono_proveedor='3001234567',
            correo_proveedor='moa@prov.com',
        )
        self.assertTrue(Proveedor.objects.filter(nit_proveedor='900123456').exists())

        # 2. Datos correctos
        p = Proveedor.objects.get(nit_proveedor='900123456')
        self.assertEqual(p.nombre_proveedor, 'Distribuidora MOA')

        # 3. NIT duplicado rechazado
        with self.assertRaises(Exception):
            Proveedor.objects.create(
                nombre_proveedor='Otro',
                nit_proveedor='900123456',
            )

    # ─── PRUEBA FUNCIONAL OK ──────────────────────────────────
    def test_RNF05_proveedor_datos_persisten_OK(self):
        """
        NO FUNCIONAL - RNF-05 CASO OK 
        Integridad: Los datos del proveedor persisten en la BD.
        Resultado esperado: OK
        """
        proveedor = Proveedor.objects.create(
            nombre_proveedor='Proveedor Integro',
            nit_proveedor='800999111',
            correo_proveedor='integro@prov.com',
        )
        p = Proveedor.objects.get(pk=proveedor.pk)
        self.assertEqual(p.correo_proveedor, 'integro@prov.com')

    # ─── PRUEBA NO FUNCIONAL ERROR ───────────────────────────────
    def test_RNF05_proveedor_datos_persisten_ERROR(self):
        """
        NO FUNCIONAL - RNF-05 CASO ERROR 
        Simula que los datos del proveedor no persisten.
        Resultado esperado: FAIL
        """
        proveedor = Proveedor.objects.create(
            nombre_proveedor='Proveedor Error',
            nit_proveedor='700888222',
            correo_proveedor='error@prov.com',
        )
        proveedor.nombre_proveedor = 'CambioSinGuardar'
        p = Proveedor.objects.get(pk=proveedor.pk)
        self.assertEqual(
            p.nombre_proveedor,
            'CambioSinGuardar',
            msg="CASO ERROR DEMOSTRADO: El cambio no se guardó en la BD."
        )



