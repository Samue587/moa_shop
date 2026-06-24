import pytest

from AppMoa.models import (
    Rol,
    Usuario,
    Proveedor,
    Categoria,
    Producto,
    VariacionProducto,
    Venta,
    DetalleVenta
)


@pytest.mark.django_db
def test_RF11_RF12_no_permite_vender_sin_stock():

    rol = Rol.objects.create(nombre_rol="cliente")

    usuario = Usuario(
        nombres_usuario="Juan",
        apellidos_usuario="Perez",
        correo_usuario="juan_error@test.com",
        rol=rol
    )
    usuario.set_password("123456")
    usuario.save()

    proveedor = Proveedor.objects.create(
        nit_proveedor=900123457,
        nombre_proveedor="Nike",
        telefono_proveedor=3001234567,
        correo_proveedor="nike_error@test.com"
    )

    categoria = Categoria.objects.create(
        nombre="Tenis"
    )

    producto = Producto.objects.create(
        proveedor=proveedor,
        categoria=categoria,
        nombre_producto="Air Max Error"
    )

    variacion = VariacionProducto.objects.create(
        producto=producto,
        talla="42",
        color="Negro",
        sku_unico="AIRMAX_ERROR",
        precio_compra=100000,
        precio_base=150000,
        stock_actual=2,   # solo hay 2 unidades
        stock_minimo=1
    )

    venta = Venta.objects.create(
        usuario=usuario
    )

    detalle = DetalleVenta.objects.create(
        venta=venta,
        variacion=variacion,
        cantidad=5,       # intenta comprar 5
        precio_unitario=150000
    )

    with pytest.raises(ValueError):
        detalle.descontar_stock()

    variacion.refresh_from_db()

    assert variacion.stock_actual == 2
    
    
@pytest.mark.django_db
def test_RF11_RF12_error_stock_insuficiente():

    rol = Rol.objects.create(nombre_rol="cliente")

    usuario = Usuario(
        nombres_usuario="Juan",
        apellidos_usuario="Perez",
        correo_usuario="juanerror@test.com",
        rol=rol
    )
    usuario.set_password("123456")
    usuario.save()

    proveedor = Proveedor.objects.create(
        nit_proveedor=999999999,
        nombre_proveedor="Nike",
        telefono_proveedor=3001234567,
        correo_proveedor="nikeerror@test.com"
    )

    categoria = Categoria.objects.create(
        nombre="Tenis"
    )

    producto = Producto.objects.create(
        proveedor=proveedor,
        categoria=categoria,
        nombre_producto="Air Max Error"
    )

    variacion = VariacionProducto.objects.create(
        producto=producto,
        talla="42",
        color="Negro",
        sku_unico="ERROR42",
        precio_compra=100000,
        precio_base=150000,
        stock_actual=1,  # Solo hay 1 unidad
        stock_minimo=1
    )

    venta = Venta.objects.create(usuario=usuario)

    detalle = DetalleVenta.objects.create(
        venta=venta,
        variacion=variacion,
        cantidad=1,  # Quiere comprar 5
        precio_unitario=150000
    )

    # Esperamos el error
    with pytest.raises(ValueError):
        detalle.descontar_stock()

    variacion.refresh_from_db()

    # El stock NO debe modificarse
    assert variacion.stock_actual == 9999