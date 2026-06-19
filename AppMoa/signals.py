from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Permiso
from .permisos_base import MODULOS, ACCIONES


@receiver(post_migrate)
def crear_permisos(sender, **kwargs):

    for modulo in MODULOS:

        for accion_slug, accion_texto in ACCIONES:

            slug = f'{accion_slug}_{modulo}'

            descripcion = f'{accion_texto} {modulo}'

            Permiso.objects.get_or_create(
                slug=slug,
                defaults={
                    'descripcion': descripcion
                }
            )