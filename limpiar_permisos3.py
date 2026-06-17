"""
limpiar_permisos3.py
Elimina el patron:
    {% if not permisos_usuario|tiene_permiso:"..." %}
        <div class="alert ...">No tienes permiso...</div>
    {% else %}
        ...contenido real...
    {% endif %}
y deja solo el contenido real (lo que estaba en el {% else %}).
Tambien limpia el patron inverso:
    {% if permisos_usuario|tiene_permiso:"..." %}
        ...contenido real...
    {% endif %}
Uso: python limpiar_permisos3.py
"""

import os
import re

TEMPLATES_DIR = "templates/admin"


def limpiar_template(contenido):
    cambios = 0

    # Patron 1: {% if not permisos_usuario|tiene_permiso:"..." %} ... {% else %} CONTENIDO {% endif %}
    # Nos quedamos solo con CONTENIDO (lo del else)
    patron1 = re.compile(
        r'\{%[-\s]*if\s+not\s+permisos_usuario\|tiene_permiso:[\'"][^\'\"]+[\'"]\s*[-\s]*%\}'
        r".*?"
        r"\{%[-\s]*else\s*[-\s]*%\}"
        r"(.*?)"
        r"\{%[-\s]*endif\s*[-\s]*%\}",
        re.DOTALL,
    )
    contenido, n = patron1.subn(r"\1", contenido)
    cambios += n

    # Patron 2: {% if permisos_usuario|tiene_permiso:"..." %} CONTENIDO {% endif %}  (sin else)
    patron2 = re.compile(
        r'\{%[-\s]*if\s+permisos_usuario\|tiene_permiso:[\'"][^\'\"]+[\'"]\s*[-\s]*%\}'
        r"(.*?)"
        r"\{%[-\s]*endif\s*[-\s]*%\}",
        re.DOTALL,
    )
    contenido, n = patron2.subn(r"\1", contenido)
    cambios += n

    # Patron 3: {% if not permisos_usuario|tiene_permiso:"..." %} CONTENIDO {% endif %}  (sin else, negado)
    # Aqui lo correcto es ELIMINAR ese contenido (es el mensaje de "no tienes permiso")
    patron3 = re.compile(
        r'\{%[-\s]*if\s+not\s+permisos_usuario\|tiene_permiso:[\'"][^\'\"]+[\'"]\s*[-\s]*%\}'
        r".*?"
        r"\{%[-\s]*endif\s*[-\s]*%\}",
        re.DOTALL,
    )
    contenido, n = patron3.subn("", contenido)
    cambios += n

    # Quitar {% load permisos_tags %} sueltos
    contenido, n = re.subn(r"\{%[-\s]*load permisos_tags\s*[-\s]*%\}\n?", "", contenido)
    cambios += n

    # Limpiar lineas en blanco multiples
    contenido = re.sub(r"\n{3,}", "\n\n", contenido)

    return contenido, cambios


def procesar_directorio(directorio):
    archivos_procesados = []
    for root, dirs, files in os.walk(directorio):
        for archivo in files:
            if archivo.endswith(".html"):
                ruta = os.path.join(root, archivo)
                with open(ruta, "r", encoding="utf-8") as f:
                    original = f.read()

                limpio, cambios = limpiar_template(original)

                if limpio != original:
                    with open(ruta, "w", encoding="utf-8") as f:
                        f.write(limpio)
                    archivos_procesados.append(ruta)
                    print(f"  ✅ Limpiado ({cambios} bloque(s)): {ruta}")
                else:
                    print(f"  ⏭  Sin cambios: {ruta}")

    return archivos_procesados


if __name__ == "__main__":
    print(f"\n🧹 Limpiando bloques if/else de permisos en: {TEMPLATES_DIR}\n")

    if not os.path.exists(TEMPLATES_DIR):
        print(f"❌ No se encontró el directorio: {TEMPLATES_DIR}")
        print("   Ejecuta el script desde la raíz del proyecto (donde está manage.py)")
    else:
        procesados = procesar_directorio(TEMPLATES_DIR)
        print(f"\n✅ Listo. {len(procesados)} archivo(s) modificado(s).")
