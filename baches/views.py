from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required  
from django.contrib import messages
from .models import Bache
from .forms import BacheForm

def inicio(request):
    return render(request, "baches/menu.html")

@login_required
def mapa_baches(request):
    baches = Bache.objects.all().select_related('usuario')
    context = {
        'baches': baches
    }
    return render(request, "baches/mapa.html", context)


@login_required
def formulario_reporte(request):
    if request.method == 'POST':
        try:
            descripcion = request.POST.get('descripcion')
            latitud = request.POST.get('lat')
            longitud = request.POST.get('lng')
            foto = request.FILES.get('foto')
            titulo = request.POST.get('titulo', 'Bache reportado')
            
            # Validaciones
            if not descripcion or not latitud or not longitud:
                messages.error(request, "Descripción, latitud y longitud son obligatorios")
                baches = Bache.objects.all()
                context = {'baches': baches}
                return render(request, "baches/mapa.html", context)
            
            # Crear el bache
            bache = Bache.objects.create(
                usuario=request.user,
                titulo=titulo,
                descripcion=descripcion,
                latitud=float(latitud),
                longitud=float(longitud),
                foto=foto if foto else None,
            )
            
            messages.success(request, f"Bache '{bache.titulo}' reportado exitosamente con ID: {bache.id}")
            return redirect('mapa_baches')
            
        except ValueError as e:
            messages.error(request, "Error en los valores de latitud o longitud")
            baches = Bache.objects.all()
            context = {'baches': baches}
            return render(request, "baches/mapa.html", context)
        except Exception as e:
            messages.error(request, f"Error al crear el reporte: {str(e)}")
            baches = Bache.objects.all()
            context = {'baches': baches}
            return render(request, "baches/mapa.html", context)
    
    baches = Bache.objects.all()
    context = {'baches': baches}
    return render(request, "baches/mapa.html", context)


def detalle_bache(request, id):
    bache = get_object_or_404(Bache, id=id)
    comentarios = bache.comentarios.filter(activo=True).select_related('usuario')
    context = {
        'bache': bache,
        'comentarios': comentarios
    }
    return render(request, "baches/detalle.html", context)


@login_required 
def actualizar_bache(request, id):
    bache = get_object_or_404(Bache, id=id)
    
    # Verificar que el usuario sea el propietario
    if bache.usuario != request.user:
        messages.error(request, "No tienes permiso para editar este reporte")
        return redirect('mapa_baches')
    
    if request.method == 'POST':
        try:
            # Actualizar campos
            bache.titulo = request.POST.get('titulo', bache.titulo)
            bache.descripcion = request.POST.get('descripcion', bache.descripcion)
            
            # Foto nueva
            if 'foto' in request.FILES:
                bache.foto = request.FILES['foto']
            
            bache.save()
            messages.success(request, "Bache actualizado exitosamente")
            
            # Redirigir al mapa para evitar error de detalle.html
            return redirect('mapa_baches')
        
        except Exception as e:
            messages.error(request, f"Error al actualizar: {str(e)}")
    
    context = {
        'bache': bache
    }
    return render(request, "baches/editar.html", context)


@login_required 
def eliminar_bache(request, id):
    bache = get_object_or_404(Bache, id=id)
    
    # Verificar que el usuario sea el propietario
    if bache.usuario != request.user:
        messages.error(request, "No tienes permiso para eliminar este reporte")
        return redirect('mapa_baches') 
    
    if request.method == 'POST':
        titulo = bache.titulo
        bache.delete()
        messages.success(request, f"Bache '{titulo}' eliminado exitosamente")
        return redirect('mapa_baches')
    
    context = {
        'bache': bache
    }
    return render(request, "baches/confirmar_eliminar.html", context)