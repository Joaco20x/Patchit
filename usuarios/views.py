from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario

def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        telefono = request.POST.get('telefono', '')
        
        # Validaciones
        if not username or not email or not password1 or not password2:
            messages.error(request, 'Todos los campos obligatorios deben ser completados')
            return render(request, 'usuarios/registro.html')
        
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'usuarios/registro.html')
        
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
            return render(request, 'usuarios/registro.html')
        
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return render(request, 'usuarios/registro.html')
        
        # Crear usuario
        try:
            usuario = Usuario.objects.create_user(
                username=username,
                email=email,
                password=password1,
                telefono=telefono
            )
            messages.success(request, 'Usuario registrado exitosamente')
            login(request, usuario)
            return redirect('mapa_baches')
        except Exception as e:
            messages.error(request, f'Error al crear usuario: {str(e)}')
            return render(request, 'usuarios/registro.html')
    
    return render(request, 'usuarios/registro.html')


def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Usuario y contraseña son requeridos')
            return render(request, 'usuarios/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}')
            next_url = request.GET.get('next', 'mapa_baches')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return render(request, 'usuarios/login.html')
    
    return render(request, 'usuarios/login.html')


@login_required
def cerrar_sesion(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login')


@login_required
def perfil(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.telefono = request.POST.get('telefono', user.telefono)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        
        # Cambiar contraseña si se proporciona
        new_password = request.POST.get('new_password')
        if new_password:
            user.set_password(new_password)
        
        user.save()
        messages.success(request, 'Perfil actualizado exitosamente')
        
        # Re-autenticar si cambió la contraseña
        if new_password:
            login(request, user)
        
        return redirect('perfil')
    
    return render(request, 'usuarios/perfil.html')