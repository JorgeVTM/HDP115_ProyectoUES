from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
#Aquí crearemos nuestros formularios

#perqueño formulario para realizar busquedas de ofertas laborales
class BusquedaForm(forms.Form):
    
    busqueda = forms.CharField(label=False,max_length=250, widget=forms.TextInput(attrs={'placeholder': 'buscar area de trabajo...'}))

#formulario para registrar una nueva cuenta de usuario
class RegistrarUsuarioForm(UserCreationForm):
    
    class Meta:
        
        model = User   
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
        
#formulario para gestionar los datos de usuario 
class UsuarioForm(forms.ModelForm):
    
    class Meta:
        
        model = User   
        fields = ('first_name', 'last_name', 'email',)
        labels = { 'email': 'Correo electronico'}
        widgets = {
            'first_name' : forms.TextInput(attrs={'placeholder': 'Escriba su nombre completo...'}),
            'last_name' : forms.TextInput(attrs={'placeholder': 'Escriba su apellido...'}),
            'email' : forms.EmailInput(attrs={'placeholder': 'Escriba su correo electronico...'}),  
        }
        
#formulario para gestionar los datos personales de usuario
class PersonaForm(forms.ModelForm):
        
    class Meta:
        
        model = Persona
        fields = ('fecha_nacimiento','genero','edad','telefono','dui','direccion')
        labels = {'fecha_nacimiento' : 'Fecha de nacimiento'}
        widgets = {  
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'genero': forms.Select(choices=((None,'Seleccione un genero'),('Masculino','Masculino'),('Femenino','Femenino'),('No binario','No binario'))),
            'edad': forms.NumberInput(attrs={'placeholder': 'Escriba su edad actual...'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Escriba su telefono de contacto...'}),
            'dui': forms.TextInput(attrs={'placeholder': 'Escriba su numero unitario de identidad...'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Escriba su direccion de residencia...'}),
            }
    
    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        self.fields['fecha_nacimiento'].required = False
        self.fields['genero'].required = False
        self.fields['edad'].required = False
        self.fields['telefono'].required = False
        self.fields['dui'].required = False
        self.fields['direccion'].required = False
        
#formulario para gestionar el perfil de usuario
class PerfilForm(forms.ModelForm):
    
    class Meta:
        
        model = Perfil
        atributos = {'placeholder': 'Agrege una descripción...', 'cols' : 50, 'rows': 10,}

        fields = ('formacion_academica', 'experiencia_laboral', 'cursos_realizados', 'idiomas','conocimientos_adicionales')
   
        widgets = {
            'formacion_academica' : forms.Textarea(attrs=atributos),
            'experiencia_laboral' : forms.Textarea(attrs=atributos),
            'cursos_realizados' : forms.Textarea(attrs=atributos),
            'idiomas' : forms.Textarea(attrs=atributos),  
            'conocimientos_adicionales' : forms.Textarea(attrs=atributos),  
        }
    
    def __init__(self, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)
        self.fields['formacion_academica'].required = False
        self.fields['experiencia_laboral'].required = False
        self.fields['cursos_realizados'].required = False
        self.fields['idiomas'].required = False
        self.fields['conocimientos_adicionales'].required = False

#formulario para las solicitudes laborales
class SolicitudLaboralForm(forms.ModelForm):
    
    class Meta:  
        model =   SolicitudLaboral
        fields = '__all__'