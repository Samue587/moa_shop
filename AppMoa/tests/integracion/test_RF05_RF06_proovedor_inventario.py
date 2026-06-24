import pytest
from django.utils import timezone

from AppMoa.models import Proveedor, Entrada


@pytest.mark.django_db
def test_RF05_RF06_proveedor_registra_entrada_inventario():

    # RF-05: Crear proveedor
    proveedor = Proveedor.objects.create(
        nit_proveedor=900123456,
        nombre_proveedor="Adidas",
        telefono_proveedor=3001112222,
        correo_proveedor="adidas@test.com"
    )

    assert Proveedor.objects.filter(id=proveedor.id).exists()

    # RF-06: Registrar entrada de inventario asociada al proveedor
    entrada = Entrada.objects.create(
        proveedor=proveedor,
        fecha_entrada=timezone.now()
    )

    assert entrada.id is not None
    assert entrada.proveedor == proveedor
    assert Entrada.objects.filter(proveedor=proveedor).count() == 1