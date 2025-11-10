from django.urls import path
from . import views

urlpatterns = [
    path('mapa/', views.mapa_baches, name='mapa_baches'),
    path('reportar/', views.reportar_bache, name='reportar_bache'),
    path('menu/',views.menu,name="menu"),
    path('<int:id>/', views.detalle_bache, name='detalle_bache'),
    path('<int:id>/editar/', views.editar_bache, name='editar_bache'),
    path('<int:id>/eliminar/', views.eliminar_bache, name='eliminar_bache'),
]
