from django.db import models
from usuarios.models import Usuario

class Bache(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, default='Bache sin título')
    descripcion = models.TextField(blank=True)
    foto = models.ImageField(upload_to='baches/', blank=True, null=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    aprobado_por_municipalidad = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Bache'
        verbose_name_plural = 'Baches'
        ordering = ['-fecha_creacion']


class Comentario(models.Model):
    bache = models.ForeignKey(Bache, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField()
    calificacion = models.IntegerField(default=3)  # 1 a 5
    peligro = models.IntegerField(default=3)       # 1 a 5
    activo = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.usuario.username} sobre {self.bache.titulo}'

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['-fecha']