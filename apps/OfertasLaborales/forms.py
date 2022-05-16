from django import forms
from .models import *
#Aquí crearemos nuestros formularios

class BusquedaForm(forms.Form):
    
    busqueda = forms.CharField(label=False,max_length=250, widget=forms.TextInput(attrs={'placeholder': 'buscar area de trabajo...'}))
