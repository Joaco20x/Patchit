from django import forms
from .models import Bache

class BacheForm(forms.ModelForm):
    class Meta:
        model = Bache
        fields = ['descripcion', 'foto', 'latitud', 'longitud']
