"""
RF-14 — Auditoría
Caso de Prueba: Registrar movimientos críticos del sistema.
Ejecutar: python manage.py test AppMoa.tests.test_RF14_auditoria -v 2
"""
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from AppMoa.models import Auditoria, Rol, Usuario


class TestRF14Auditoria(TestCase):

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

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RF14_registrar_movimientos_criticos(self):
        # 1. Registrar movimiento crítico
        registro = Auditoria.objects.create(
            usuario=self.admin,
            accion='LOGIN',
            descripcion='El admin inició sesión',
        )
        self.assertTrue(Auditoria.objects.filter(pk=registro.pk).exists())

        # 2. Datos correctos
        r = Auditoria.objects.get(pk=registro.pk)
        self.assertEqual(r.accion, 'LOGIN')
        self.assertEqual(r.usuario, self.admin)

        # 3. Múltiples movimientos
        Auditoria.objects.create(
            usuario=self.admin,
            accion='MODIFICAR_PRODUCTO',
            descripcion='Cambió el precio del producto 1',
        )
        self.assertEqual(Auditoria.objects.filter(usuario=self.admin).count(), 2)

    # ─── PRUEBA FUNCIONAL OK ──────────────────────────────────
    def test_RNF14_auditoria_registro_integro_OK(self):
        """
        NO FUNCIONAL - RNF-14 CASO OK 
        Integridad: Los registros de auditoría persisten correctamente.
        Resultado esperado: OK
        """
        registro = Auditoria.objects.create(
            usuario=self.admin,
            accion='ELIMINAR_USUARIO',
            descripcion='Se eliminó el usuario 5',
        )
        r = Auditoria.objects.get(pk=registro.pk)
        self.assertEqual(r.descripcion, 'Se eliminó el usuario 5')

    # ─── PRUEBA NO FUNCIONAL ERROR ───────────────────────────────
    def test_RNF14_auditoria_registro_integro_ERROR(self):
        """
        NO FUNCIONAL - RNF-14 CASO ERROR 
        Simula que se busca un movimiento que no existe.
        Resultado esperado: FAIL
        """
        self.assertTrue(
            Auditoria.objects.filter(accion='ACCION_INEXISTENTE').exists(),
            msg="CASO ERROR DEMOSTRADO: Se buscó una acción que no existe en auditoría."
        )




