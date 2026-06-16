from django.apps import AppConfig


class AppmoaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "AppMoa"

    def ready(self):
        import AppMoa.signals
