from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bache
from .forms import BacheForm

def inicio(request):

    return render(request, "baches/menu.html")

def mapa_baches(request):
    baches = Bache.objects.all()
    context = {
        'baches': baches
    }
    return render(request, "baches/mapa.html", context)

def formulario_reporte(request):

    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        latitud = request.POST.get('lat')
        longitud = request.POST.get('lng')
        foto = request.FILES.get('foto')
        
        if not descripcion or not latitud or not longitud:
            messages.error(request, "Todos los campos son obligatorios excepto la foto")
            return render(request, "baches/mapa.html")
        
        bache = Bache.objects.create(
            descripcion=descripcion,
            latitud=float(latitud),
            longitud=float(longitud),
            foto=foto,
        )
        
        messages.success(request, "Bache reportado exitosamente")
        return redirect('mapa_baches')
    
    return render(request, "baches/mapa.html")

def detalle_bache(request, id):

    bache = get_object_or_404(Bache, id=id)
    context = {
        'bache': bache
    }
    return render(request, "baches/detalle.html", context)

def actualizar_bache(request, id):
    bache = get_object_or_404(Bache, id=id)
    
    if request.method == 'POST':
        bache.descripcion = request.POST.get('descripcion', bache.descripcion)
        if 'foto' in request.FILES:
            bache.foto = request.FILES['foto']
        
        bache.save()
        messages.success(request, "Bache actualizado exitosamente")
        return redirect('detalle_bache', id=id)
    
    context = {
        'bache': bache
    }
    return render(request, "baches/editar.html", context)


def eliminar_bache(request, id):
    bache = get_object_or_404(Bache, id=id)
    
    if bache.usuario != request.user:
        messages.error(request, "No tienes permiso para eliminar este reporte")
        return redirect('detalle_bache', id=id)
    
    if request.method == 'POST':
        bache.delete()
        messages.success(request, "Bache eliminado exitosamente")
        return redirect('mapa_baches')
    
    context = {
        'bache': bache
    }
    return render(request, "baches/confirmar_eliminar.html", context)