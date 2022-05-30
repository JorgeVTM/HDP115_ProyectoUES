from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from apps.OfertasLaborales.models import *
from apps.OfertasLaborales.forms import *
from .models import *
from .forms import *

decorators = [never_cache, login_required, csrf_protect]

# Create your views here.
@method_decorator(permission_required('is_staff'), name='get')
class Administracion(TemplateView):
    
    template_name = 'Administracion/administracion.html'
    model = User
    
    def get(self, request):
        return render(request, self.template_name)
    
@method_decorator(permission_required('is_staff'), name='get')
@method_decorator(decorators, name='get')
@method_decorator(decorators, name='post')
class Registros(TemplateView):
    # template_name = 'Administracion/ofertaslaborales.html'
    def __init__(self, template_name, model, form, title, objeto):
        self.objeto = objeto
        self.title = title
        self.template_name = template_name
        self.model = model
        self.form = form
    
    def get(self, request):
        context = self.get_context_data(titulo = self.title, objeto = self.objeto)
        context['model'] = self.model.objects.all().values()
        context['form'] = self.form()
        return render(request, self.template_name, context)
    
    def post(self, request):
        #Enviamos los datos del formulario con la instacia objeto modelo
        nuevo_form = self.form(request.POST)
        # Validación para el formulario con los datos de persona de usuario
        if nuevo_form.is_valid():
            nuevo_form.save()
            return self.get(request)
        else:
            context = self.get_context_data()
            context['form'] = nuevo_form
            return render(request, self.template_name, context)
    
class OfertasLaborales(Registros):
    
    def __init__(self):
        template_name = 'Administracion/gestionregistros.html'
        title = 'Registrar una nueva Oferta Laboral'
        objeto = 'OfertaLaboral'
        
        Registros.__init__(self, template_name, OfertaLaboral, OfertasLaboralesForm, title, objeto)

class OfertasLaboralesAll(Registros):
    
    def __init__(self):
        template_name = 'Administracion/gestionTabla.html'
        title = None
        objeto = 'OfertaLaboral'
        Registros.__init__(self, template_name, OfertaLaboral, OfertasLaboralesForm, title,objeto)
        
class Categorias(Registros):
    
    def __init__(self):
        template_name = 'Administracion/gestionregistros.html'
        title = 'Registrar una nueva Categoria'
        objeto = 'Categoria'
        Registros.__init__(self, template_name, Categoria, CategoriaForm, title, objeto)

class CategoriasAll(Registros):
    
    def __init__(self):
        template_name = 'Administracion/gestionTabla.html'
        title = None
        objeto = 'Categoria'
        Registros.__init__(self, template_name, Categoria, OfertasLaboralesForm, title, objeto)

class Facultades(Registros):
    
    def __init__(self):
        template_name = 'Administracion/gestionregistros.html'
        title = 'Registrar una nueva Facultad de la Universidad'
        objeto = 'Facultad'
        Registros.__init__(self, template_name, Facultad, FacultadForm, title, objeto)

class FacultadesAll(Registros):
    
    def __init__(self):
        template_name = 'Administracion/gestionTabla.html'
        title = None
        objeto = 'Facultad'
        Registros.__init__(self, template_name, Facultad, OfertasLaboralesForm, title, objeto)
        
class Sedes(Registros):
    
    def __init__(self):
        template_name = 'Administracion/gestionregistros.html'
        title = 'Registrar una nueva Sede de la Universidad'
        objeto = 'Sede'
        Registros.__init__(self, template_name, Sede, SedeForm, title, objeto)

class SedesAll(Registros):
    
    def __init__(self):
        template_name = 'Administracion/gestionTabla.html'
        title = 'Registrar una nueva Oferta Laboral'
        objeto = 'Sede'
        Registros.__init__(self, template_name, Sede, OfertasLaboralesForm, title, objeto)