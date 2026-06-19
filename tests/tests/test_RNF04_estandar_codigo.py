"""
RNF-04 — Estándar de Código - PEP 8
Caso de Prueba: El código sigue lineamientos de limpieza y profesionalismo PEP 8.
Herramienta: PEP 8 (Linter - flake8).
Ejecutar: python manage.py test AppMoa.tests.test_RNF04_estandar_codigo -v 2
"""
import subprocess
import tempfile
import os
from django.test import TestCase


class TestRNF04EstandarCodigo(TestCase):

    # ─── PRUEBA FUNCIONAL ────────────────────────────────────────
    def test_RNF04_flake8_disponible(self):
        """
        FUNCIONAL - RNF-04
        Verifica que flake8 esté instalado y disponible en el entorno.
        Resultado esperado: OK
        """
        resultado = subprocess.run(
            ['flake8', '--version'],
            capture_output=True,
            text=True
        )
        self.assertEqual(
            resultado.returncode, 0,
            msg="flake8 no está instalado en el entorno."
        )

    # ─── PRUEBA NO FUNCIONAL - CASO OK ───────────────────────────
    def test_RNF04_appMoa_cumple_pep8_OK(self):
        """
        NO FUNCIONAL - RNF-04 CASO OK
        El módulo AppMoa cumple con PEP 8 (0 errores de linting).
        Resultado esperado: OK
        """
        resultado = subprocess.run(
            ['flake8', 'AppMoa/', '--max-line-length=120', '--exclude=migrations'],
            capture_output=True,
            text=True
        )
        self.assertEqual(
            resultado.returncode, 0,
            msg=f"Errores PEP 8 encontrados:\n{resultado.stdout}"
        )

    # ─── PRUEBA NO FUNCIONAL - CASO ERROR ────────────────────────
    def test_RNF04_archivo_con_violaciones_pep8_ERROR(self):
        """
        NO FUNCIONAL - RNF-04 CASO ERROR
        Analiza un archivo con violaciones PEP 8 intencionales y afirma que no hay errores.
        Resultado esperado: FAIL (intencional)
        """
        codigo_malo = """x=1+2
def funcion_mal_formateada(a,b,c):
    return a+b+c
y=x*3
"""
        with tempfile.NamedTemporaryFile(
            suffix='.py', mode='w', delete=False
        ) as f:
            f.write(codigo_malo)
            tmp = f.name

        resultado = subprocess.run(
            ['flake8', tmp],
            capture_output=True,
            text=True
        )
        os.unlink(tmp)

        # FAIL intencional: afirmamos que no hay errores en código con violaciones
        self.assertEqual(
            resultado.returncode, 0,
            msg=f"CASO ERROR DEMOSTRADO: violaciones PEP 8 detectadas:\n{resultado.stdout}"
        )
