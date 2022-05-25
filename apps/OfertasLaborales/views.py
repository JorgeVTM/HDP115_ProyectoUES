import json
from os import system
from django.db.models import *
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

decorators = [never_cache, login_required, csrf_protect]

# Create your views here.

class Inicio(ListView):
    
    template_name = 'OfertasLaborales/inicio.html'
    model = OfertaLaboral
    object_list= (Categoria, Facultad, Sede)
    
    def get(self, request):
        user = request.user
        if user.is_staff:
            return redirect('administracion')
        context = self.get_context_data(form=BusquedaForm())
        return render(request, self.template_name, context)

    def post(self, request):
        form = BusquedaForm(request.POST)
        context = self.get_context_data(form=BusquedaForm())
        
        if form.is_valid():
            busqueda = form.cleaned_data['busqueda']
            context = self.get_context_data(form=BusquedaForm({'busqueda':busqueda}))
            context['ofertaslaborales'] = OfertaLaboral.objects.filter(area_de_trabajo__icontains=busqueda)
        return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ofertaslaborales'] = OfertaLaboral.objects.all()
        context['resultados'] = OfertaLaboral.objects.count()
        
        for objeto in self.object_list:
            context[objeto.__name__] = objeto.objects.annotate(Count('ofertalaboral'))
        return context
    
class Busqueda(Inicio):
    
    def get(self, request, busqueda):
        context = self.get_context_data(busqueda, form=BusquedaForm())   
        return render(request, self.template_name, context)
    
    def post(self, request, busqueda):
        form = BusquedaForm(request.POST)
        context = self.get_context_data(busqueda, form=BusquedaForm())
        
        if form.is_valid():
            dato = form.cleaned_data['busqueda']
            context = self.get_context_data(busqueda, form=BusquedaForm({'busqueda':dato}))
            context['ofertaslaborales'] = self.get_queryset(busqueda).filter(area_de_trabajo__icontains=dato)
        return render(request, self.template_name, context)
    
    def get_context_data(self, busqueda, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['ofertaslaborales'] = self.get_queryset(busqueda)
        context['filtro'] = busqueda
        context['regresar'] = 'Borrar filtros'
        for objeto in self.object_list:
            context[objeto.__name__] = objeto.objects.annotate(Count('ofertalaboral')).exclude(nombre = busqueda)      
        return context
    
    def get_queryset(self, busqueda):
        for objeto in self.object_list:
            try:
                query = objeto.objects.get(nombre=busqueda).ofertalaboral_set.all()
                return query
            except objeto.DoesNotExist:
                query = None
        return query

@method_decorator(decorators, name='post')
class Solicitud(TemplateView):
    
    model = OfertaLaboral
    template_name = 'OfertasLaborales/solicitudoferta.html'
     
    def get(self, request, idoferta, nombre):
        user = request.user
        if user.is_staff:
            return redirect('administracion')
        context = self.get_context_data(idoferta)   
        return render(request, self.template_name, context)
    
    def get_context_data(self, idoferta, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ofertalaboral"] = self.model.objects.get(pk=idoferta)
        context["solicitud"] = SolicitudLaboral.objects.all()
        context["categoria"] = Categoria.objects.get(ofertalaboral__pk=idoferta)
        context["facultad"] = Facultad.objects.get(ofertalaboral__pk=idoferta)
        context["sede"] = Sede.objects.get(ofertalaboral__pk=idoferta)
        return context
    
    def post(self, request, idoferta, nombre):
        user = request.user
        oferta = OfertaLaboral.objects.get(id=idoferta)
        solicitudlaboral = SolicitudLaboral
        try:
            solicitudlaboral = SolicitudLaboral.objects.get(user=user,ofertalaboral=oferta)
            return redirect('inicio')
        except solicitudlaboral.DoesNotExist:
            solicitudlaboral = SolicitudLaboral.objects.create(user=user,ofertalaboral=oferta)
        return redirect('inicio')
    
    
class Registrarse(TemplateView):
    model = User
    template_name = 'OfertasLaborales/registrarse.html'
    
    def get(self, request):
        context = self.get_context_data(form=RegistrarUsuarioForm)
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            
            # # Tambien creamos un persona para el usuario
            persona = Persona.objects.create(user_id = user.id)
            
            # # Tambien creamos un persona laboral
            persona = Perfil.objects.create(persona_id = persona.id)
            
            login(request, user)
            return redirect('/')
        else:
            context = self.get_context_data(form=RegistrarUsuarioForm(request.POST))
            return render(request, self.template_name, context)

@method_decorator(decorators, name='get')
@method_decorator(decorators, name='post')
class PerfilUsuario(TemplateView):
    
    model = User
    template_name = 'OfertasLaborales/perfilusuario.html'
    
    def get(self, request):
        user = request.user
        context = self.get_context_data(user)
        return render(request, self.template_name, context)
    
    def post(self, request):
        #recibimos la información del modelo objeto
        user = request.user    
        #Enviamos los datos del formulario con la instacia objeto modelo
        form = UsuarioForm(request.POST, instance=user)
        # Validación para el formulario con los datos de persona de usuario
        if form.is_valid():
            form.save()
            return self.get(request)
    
    def get_context_data(self, user,**kwargs):
        context = super().get_context_data(**kwargs)
        usuario = json.loads(serializers.serialize('jsonl',User.objects.filter(id=user.id)))
        context['form'] = UsuarioForm(usuario['fields'])
        context['title'] = "Datos de cuenta"
        return context

@method_decorator(decorators, name='get')
@method_decorator(decorators, name='post')
class InfoPersonal(TemplateView):
    
    model = Persona
    template_name = 'OfertasLaborales/perfilusuario.html'
    
    def get(self, request):
        user = request.user
        context = self.get_context_data(user)
        return render(request, self.template_name, context)
    
    def post(self, request):
        #recibimos la información del modelo objeto
        user = request.user    
        persona = request.user.persona
        #Enviamos los datos del formulario con la instacia objeto modelo
        form = PersonaForm(request.POST, instance=persona)
        # Validación para el formulario con los datos de persona de usuario
        if form.is_valid():
            form.save()
            return self.get(request)
    
    def get_context_data(self, user,**kwargs):
        context = super().get_context_data(**kwargs)
        persona = json.loads(serializers.serialize('jsonl',Persona.objects.all().filter(pk=user.persona.pk)))
        context['form'] = PersonaForm(persona['fields'])
        context['title'] = "Información Personal"
        return context
    
@method_decorator(decorators, name='get')
@method_decorator(decorators, name='post')
class DatoLaboral(TemplateView):
    
    model = Perfil
    template_name = 'OfertasLaborales/perfilusuario.html'
    
    def get(self, request):
        user = request.user
        context = self.get_context_data(user)
        return render(request, self.template_name, context)
    
    def post(self, request):
        #recibimos la información del modelo objeto
        user = request.user    
        perfil = request.user.persona.perfil
        #Enviamos los datos del formulario con la instacia objeto modelo
        form = PerfilForm(request.POST, instance=perfil)
        # Validación para el formulario con los datos de persona de usuario
        if form.is_valid():
            form.save()
            return self.get(request)
    
    def get_context_data(self, user,**kwargs):
        context = super().get_context_data(**kwargs)
        perfil = json.loads(serializers.serialize('jsonl',Perfil.objects.all().filter(pk=user.persona.perfil.pk)))
        context['form'] = PerfilForm(perfil['fields'])
        context['title'] = "Información Laboral"
        return context

class Informacion(TemplateView):
    
    model = User
    template_name = 'OfertasLaborales/informacion.html'
    
    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)