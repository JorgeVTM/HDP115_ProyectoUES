from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from apps.OfertasLaborales.models import *
from .models import *
#Aquí crearemos nuestros formularios
        
#formulario para las ofertas laborales
class OfertasLaboralesForm(forms.ModelForm):
    
    class Meta:
        
        model = OfertaLaboral   
        fields = '__all__'
        widgets = {
            'area_de_trabajo' : forms.TextInput(attrs={'placeholder': 'Area de trabajo para la oferta laboral...'}),  
            'cargo_solicitado' : forms.TextInput(attrs={'placeholder': 'Cargo solicitad...'}),  
            'vacantes' : forms.NumberInput(attrs={'placeholder': 'Vacantes disponibles...'}),  
            'tipo_contratacion' : forms.TextInput(attrs={'placeholder': 'Tipo de contratación...'}),  
            'nivel_experiencia' : forms.TextInput(attrs={'placeholder': 'Nivel de experiencia...'}),  
            'generos' : forms.TextInput(attrs={'placeholder': 'Generos solicitados...'}),  
            'edad_solicitada' : forms.TextInput(attrs={'placeholder': 'Edad mínima solicitada...'}), 
            'salario_minimo' : forms.NumberInput(),  
            'salario_maximo' : forms.NumberInput(),    
            'descripcion' : forms.Textarea(attrs={'placeholder': 'Escriba la descripción de la oferta laboral...'}),  
        }
    
    def __init__(self, *args, **kwargs):
        super(OfertasLaboralesForm, self).__init__(*args, **kwargs)
        self.fields['salario_maximo'].required = False
        self.fields['descripcion'].required = False
         
#formulario para las categorias
class CategoriaForm(forms.ModelForm):
    
    class Meta:
        
        model = Categoria   
        fields = '__all__'

#formulario para las facultades
class FacultadForm(forms.ModelForm):
    
    class Meta:
        
        model = Facultad   
        fields = '__all__'

#formulario para las sedes
class SedeForm(forms.ModelForm):
    
    class Meta:
        
        model = Sede   
        fields = '__all__'