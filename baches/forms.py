from django import forms
from .models import Bache, Comentario

class BacheForm(forms.ModelForm):
    class Meta:
        model = Bache
        fields = ['descripcion', 'foto', 'latitud', 'longitud']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto', 'peligro']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu opinión aquí...'}),
            'peligro': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)])
        }