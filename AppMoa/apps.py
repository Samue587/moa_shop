from django.apps import AppConfig


class AppmoaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AppMoa'

    def ready(self):

        try:
            from .Seeds import crear_roles, crear_permisos, asignar_permisos

            crear_roles()
            crear_permisos()
            asignar_permisos()

            print("SEEDS EJECUTADOS")

        except Exception as e:
            print(e)