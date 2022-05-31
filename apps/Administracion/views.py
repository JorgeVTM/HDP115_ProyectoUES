import json
from django.core import serializers
from os import system
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import DeleteView
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
    def __init__(self, template_name, model, form, title, objeto, url):
        self.objeto = objeto
        self.title = title
        self.template_name = template_name
        self.model = model
        self.form = form
        self.url = url
    
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
            return redirect(self.url)
        else:
            context = self.get_context_data()
            context['form'] = nuevo_form
            return render(request, self.template_name, context)

class RegistroUpdate(Registros):
    
    def __init__(self, template_name, model, form, title, objeto, url):
        Registros.__init__(self, template_name, model, form, title, objeto, url)
        self.pk = None
    
    def get(self, request, pk):
        self.pk = pk
        context = self.get_context_data(titulo = self.title, objeto = self.objeto)
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        #Enviamos los datos del formulario con la instacia objeto modelo
        objeto = self.model.objects.get(pk=pk)
        nuevo_form = self.form(request.POST, instance=objeto)
        # Validación para el formulario con los datos de persona de usuario
        if nuevo_form.is_valid():
            nuevo_form.save()
            return redirect(self.url)
        else:
            context = self.get_context_data()
            context['form'] = nuevo_form
            return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objeto = json.loads(serializers.serialize('jsonl',self.model.objects.filter(pk=self.pk)))
        context['form'] = self.form(objeto['fields'])
        return context

class RegistroDelete(DeleteView):
    
    def __init__(self, template_name, model, objeto, success_url):
        self.objeto = objeto
        self.model = model
        self.template_name = template_name
        self.success_url = reverse_lazy(success_url)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objeto"] = self.objeto
        return context
    
class OfertasLaborales(Registros):
    
    def __init__(self):
        template_name = 'Administracion/gestionregistros.html'
        title = 'Registrar una nueva Oferta Laboral'
        objeto = 'OfertaLaboral'
        url = 'ofertaslaborales_all'
        
        Registros.__init__(self, template_name, OfertaLaboral, OfertasLaboralesForm, title, objeto, url)

class OfertasLaboralesAll(Registros):
    
    def __init__(self):
        template_name = 'Administracion/gestionTabla.html'
        title = None
        objeto = 'OfertaLaboral'
        url = 'ofertaslaborales_all'
        Registros.__init__(self, template_name, OfertaLaboral, OfertasLaboralesForm, title, objeto, url)
        
class OfertasLaboralesUpdate(RegistroUpdate):
    
    def __init__(self):
        template_name = 'Administracion/gestionregistros.html'
        title = 'Modificar campos de la Oferta Laboral'
        objeto = 'OfertaLaboral'
        url = 'ofertaslaborales_all'
        RegistroUpdate.__init__(self, template_name, OfertaLaboral, OfertasLaboralesForm, title, objeto, url)
        
class OfertasLaboralesDelete(RegistroDelete):
    
    def __init__(self):
        objeto = 'OfertaLaboral'
        template_name = 'Administracion/eliminar.html'
        success_url = 'ofertaslaborales_all'
        RegistroDelete.__init__(self, template_name, OfertaLaboral, objeto, success_url)
     
class Categorias(Registros):
    
    def __init__(self):
        template_name = 'Administracion/gestionregistros.html'
        title = 'Registrar una nueva Categoria'
        objeto = 'Categoria'
        url = 'categorias_all'
        Registros.__init__(self, template_name, Categoria, CategoriaForm, title, objeto, url)

class CategoriasAll(Registros):
    
    def __init__(self):
        template_name = 'Administracion/gestionTabla.html'
        title = None
        objeto = 'Categoria'
        url = 'categorias_all'
        Registros.__init__(self, template_name, Categoria, CategoriaForm, title, objeto, url)
        
class CategoriasUpdate(RegistroUpdate):
    
    def __init__(self):
        template_name = 'Administracion/gestionregistros.html'
        title = 'Modificar campos de la Categoria'
        objeto = 'Categoria'
        url = 'categorias_all'
        RegistroUpdate.__init__(self, template_name, Categoria, CategoriaForm, title, objeto, url)

class CategoriasDelete(RegistroDelete):
    
    def __init__(self):
        objeto = 'Categoria'
        template_name = 'Administracion/eliminar.html'
        success_url = 'categorias_all'
        RegistroDelete.__init__(self, template_name, Categoria, objeto, success_url)

class Facultades(Registros):
    
    def __init__(self):
        template_name = 'Administracion/gestionregistros.html'
        title = 'Registrar una nueva Facultad de la Universidad'
        objeto = 'Facultad'
        url = 'facultades_all'
        Registros.__init__(self, template_name, Facultad, FacultadForm, title, objeto, url)

class FacultadesAll(Registros):
    
    def __init__(self):
        template_name = 'Administracion/gestionTabla.html'
        title = None
        objeto = 'Facultad'
        url = 'facultades_all'
        Registros.__init__(self, template_name, Facultad, FacultadForm, title, objeto, url)

class FacultadesUpdate(RegistroUpdate):
    
    def __init__(self):
        template_name = 'Administracion/gestionregistros.html'
        title = 'Modificar campos de la Facultad'
        objeto = 'Facultad'
        url = 'facultades_all'
        RegistroUpdate.__init__(self, template_name, Facultad, FacultadForm, title, objeto, url)

class FacultadesDelete(RegistroDelete):
    
    def __init__(self):
        objeto = 'Facultad'
        template_name = 'Administracion/eliminar.html'
        success_url = 'facultades_all'
        RegistroDelete.__init__(self, template_name, Facultad, objeto, success_url)
        
class Sedes(Registros):
    
    def __init__(self):
        template_name = 'Administracion/gestionregistros.html'
        title = 'Registrar una nueva Sede de la Universidad'
        objeto = 'Sede'
        url = 'sedes_all'
        Registros.__init__(self, template_name, Sede, SedeForm, title, objeto, url)

class SedesAll(Registros):
    
    def __init__(self):
        template_name = 'Administracion/gestionTabla.html'
        title = 'Registrar una nueva Oferta Laboral'
        objeto = 'Sede'
        url = 'sedes_all'
        Registros.__init__(self, template_name, Sede, SedeForm, title, objeto, url)
        
class SedesUpdate(RegistroUpdate):
    
    def __init__(self):
        template_name = 'Administracion/gestionregistros.html'
        title = 'Modificar campos de la Sede'
        objeto = 'Sede'
        url = 'sedes_all'
        RegistroUpdate.__init__(self, template_name, Sede, SedeForm, title, objeto, url)

class SedesDelete(RegistroDelete):
    
    def __init__(self):
        objeto = 'Sede'
        template_name = 'Administracion/eliminar.html'
        success_url = 'sedes_all'
        RegistroDelete.__init__(self, template_name, Sede, objeto, success_url)