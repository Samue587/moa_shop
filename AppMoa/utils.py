from .models import VariacionProducto


def actualizar_estado_producto(producto):

    variaciones = VariacionProducto.objects.filter(
        producto=producto
    )

    stock_total = 0
    stock_minimo_total = 0

    for variacion in variaciones:

        stock_total += variacion.stock

        stock_minimo_total += variacion.stock_minimo

    # Si no tiene stock suficiente
    if stock_total <= stock_minimo_total:

        producto.estado = 'NO_DISPONIBLE'

    else:

        producto.estado = 'DISPONIBLE'

    producto.save()