from django.urls import path
from . import views

urlpatterns = [
    path('mapa/', views.mapa_baches, name='mapa_baches'),
    path('reportar/', views.formulario_reporte, name='reportar_bache'),
    path('menu/',views.inicio,name="menu"),
    path('<int:id>/', views.detalle_bache, name='detalle_bache'),
    path('<int:id>/editar/', views.actualizar_bache, name='editar_bache'),
    path('<int:id>/eliminar/', views.eliminar_bache, name='eliminar_bache'),
]
