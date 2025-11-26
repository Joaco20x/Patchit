from django.contrib import admin
from .models import Bache, Comentario

@admin.register(Bache)
class BacheAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'latitud', 'longitud', 'fecha_creacion', 'aprobado_por_municipalidad']
    list_filter = ['aprobado_por_municipalidad', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion', 'usuario__username']
    readonly_fields = ['fecha_creacion']
    list_editable = ['aprobado_por_municipalidad']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('usuario', 'titulo', 'descripcion')
        }),
        ('Ubicación', {
            'fields': ('latitud', 'longitud')
        }),
        ('Multimedia', {
            'fields': ('foto',)
        }),
        ('Estado', {
            'fields': ('aprobado_por_municipalidad', 'fecha_creacion')
        }),
    )

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['bache', 'usuario', 'calificacion', 'peligro', 'activo', 'fecha']
    list_filter = ['activo', 'calificacion', 'peligro', 'fecha']
    search_fields = ['texto', 'usuario__username', 'bache__titulo']
    readonly_fields = ['fecha']
    list_editable = ['activo']