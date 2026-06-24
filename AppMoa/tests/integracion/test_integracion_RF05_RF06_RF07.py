import pytest
from django.utils import timezone

from AppMoa.models import (
    Proveedor,
    Categoria,
    Producto,
    VariacionProducto,
    Entrada,
    DetalleEntrada
)


@pytest.mark.django_db
def test_integracion_inventario_actualiza_stock_y_catalogo():

    proveedor = Proveedor.objects.create(
        nit_proveedor=123456789,
        nombre_proveedor="Nike",
        telefono_proveedor=3001234567,
        correo_proveedor="nike@test.com"
    )

    categoria = Categoria.objects.create(
        nombre="Tenis"
    )

    producto = Producto.objects.create(
        proveedor=proveedor,
        categoria=categoria,
        nombre_producto="Air Max"
    )

    variacion = VariacionProducto.objects.create(
        producto=producto,
        talla="42",
        color="Negro",
        sku_unico="AIRMAX42",
        precio_compra=100000,
        precio_base=150000,
        stock_actual=0,
        stock_minimo=5
    )

    producto.refresh_from_db()

    assert producto.estado == "NO_DISPONIBLE"

    entrada = Entrada.objects.create(
        proveedor=proveedor,
        fecha_entrada=timezone.now()
    )

    detalle = DetalleEntrada.objects.create(
        entrada=entrada,
        variacion=variacion,
        cantidades=10,
        precio_comprado=100000
    )

    detalle.aplicar_stock()

    variacion.refresh_from_db()
    producto.refresh_from_db()

    assert variacion.stock_actual == 10

    assert producto.estado == "DISPONIBLE"
    
    
@pytest.mark.django_db
def test_integracion_no_debe_actualizar_stock_si_cantidad_es_cero():

    proveedor = Proveedor.objects.create(
        nit_proveedor=123456789,
        nombre_proveedor="Nike",
        telefono_proveedor=3001234567,
        correo_proveedor="nike@test.com"
    )

    categoria = Categoria.objects.create(
        nombre="Tenis"
    )

    producto = Producto.objects.create(
        proveedor=proveedor,
        categoria=categoria,
        nombre_producto="Air Max"
    )

    variacion = VariacionProducto.objects.create(
        producto=producto,
        talla="42",
        color="Negro",
        sku_unico="AIRMAX43",
        precio_compra=100000,
        precio_base=150000,
        stock_actual=0,
        stock_minimo=5
    )

    entrada = Entrada.objects.create(
        proveedor=proveedor,
        fecha_entrada=timezone.now()
    )

    with pytest.raises(Exception):

        DetalleEntrada.objects.create(
            entrada=entrada,
            variacion=variacion,
            cantidades=0,
            precio_comprado=100000
        )