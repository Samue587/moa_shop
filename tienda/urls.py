from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Panel admin de Django (opcional, puedes quitarlo)
    path('django-admin/', admin.site.urls),

    # Todas las URLs de la app AppMoa
    path('', include('AppMoa.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)