from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='menu'),  
    path('mapa/', views.mapa_baches, name='mapa_baches'),
    path('reportar/', views.formulario_reporte, name='reportar_bache'),
    path('comentar/<int:bache_id>/', views.guardar_comentario, name='guardar_comentario'),
    path('<int:id>/', views.detalle_bache, name='detalle_bache'),
    path('<int:id>/editar/', views.actualizar_bache, name='editar_bache'),
    path('<int:id>/eliminar/', views.eliminar_bache, name='eliminar_bache'),
]