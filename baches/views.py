from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required  
from django.contrib import messages
from .models import Bache, Comentario
from .forms import BacheForm, ComentarioForm

def inicio(request):
    return render(request, "baches/menu.html")

def mapa_baches(request):
    # Usamos prefetch_related para traer los comentarios eficientemente
    baches = Bache.objects.all().select_related('usuario').prefetch_related('comentarios__usuario')
    
    context = {
        'baches': baches,
        'form_comentario': ComentarioForm() # Pasamos el formulario vacío para usarlo en el modal
    }
    return render(request, "baches/mapa.html", context)

@login_required(login_url='login')
def formulario_reporte(request):
    if request.method == 'POST':
        try:
            descripcion = request.POST.get('descripcion')
            latitud = request.POST.get('lat')
            longitud = request.POST.get('lng')
            foto = request.FILES.get('foto')
            titulo = request.POST.get('titulo', 'Bache reportado')
            
            if not descripcion or not latitud or not longitud:
                messages.error(request, "Descripción y ubicación son obligatorios")
                return redirect('mapa_baches')
            
            Bache.objects.create(
                usuario=request.user,
                titulo=titulo,
                descripcion=descripcion,
                latitud=latitud,
                longitud=longitud,
                foto=foto
            )
            messages.success(request, "Reporte creado exitosamente")
            return redirect('mapa_baches')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('mapa_baches')
    
    return redirect('mapa_baches')

@login_required(login_url='login')
def guardar_comentario(request, bache_id):
    bache = get_object_or_404(Bache, id=bache_id)
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.bache = bache
            comentario.usuario = request.user
            # Aseguramos que se guarde la calificación de peligro
            comentario.peligro = request.POST.get('peligro', 3) 
            comentario.save()
            messages.success(request, "Comentario agregado")
        else:
            messages.error(request, "Error al agregar comentario")
            
    return redirect('mapa_baches')

# ... (mantener el resto de las vistas: detalle_bache, actualizar_bache, eliminar_bache igual que antes) ...
def detalle_bache(request, id):
    bache = get_object_or_404(Bache, id=id)
    return render(request, "baches/detalle.html", {'bache': bache})

@login_required(login_url='login')
def actualizar_bache(request, id):
    bache = get_object_or_404(Bache, id=id)
    if bache.usuario != request.user:
        return redirect('mapa_baches')
    
    if request.method == 'POST':
        bache.titulo = request.POST.get('titulo', bache.titulo)
        bache.descripcion = request.POST.get('descripcion', bache.descripcion)
        if 'foto' in request.FILES:
            bache.foto = request.FILES['foto']
        bache.save()
        return redirect('mapa_baches')
    
    return render(request, "baches/editar.html", {'bache': bache})

@login_required(login_url='login')
def eliminar_bache(request, id):
    bache = get_object_or_404(Bache, id=id)
    if bache.usuario == request.user and request.method == 'POST':
        bache.delete()
        return redirect('mapa_baches')
    return render(request, "baches/confirmar_eliminar.html", {'bache': bache})