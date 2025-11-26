from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirigir la ruta raíz al mapa
    path('', lambda request: redirect('mapa_baches')),

    path('baches/', include('baches.urls')),
    path('usuarios/', include('usuarios.urls')),
]

# Servir archivos media y estáticos en desarrollo
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
