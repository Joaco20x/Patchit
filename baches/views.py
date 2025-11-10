from django.shortcuts import render
def menu(request):
    return render(request,"baches/menu.html")
def mapa_baches(request):
    return render(request,"baches/mapa.html")
def reportar_bache(request):
    pass
def detalle_bache(request):
    pass
def editar_bache(request,id):
    pass
def eliminar_bache(request,id): #solo si el reporte es del mismo usuario
    pass
# Create your views here.
