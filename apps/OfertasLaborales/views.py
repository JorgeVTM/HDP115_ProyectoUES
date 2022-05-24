from os import system
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.models import User
from django.core import serializers
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.

class Inicio(ListView, MultipleObjectMixin):
    
    template_name = 'OfertasLaborales/inicio.html'
    object_list= (Categoria, Facultad, Sede)
    
    def get(self, request):
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

class Perf(TemplateView):
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

decorators = [never_cache, login_required, csrf_protect]
@method_decorator(decorators, name='get')
@method_decorator(decorators, name='post')
class PerfilUsuario(ListView, MultipleObjectMixin):
    
    template_name = 'OfertasLaborales/perfilusuario.html'
    object_list = (User,Persona,Perfil)
    
    def get(self, request):
        user = request.user
   
        datos = self.get_queryset(user)
        context = self.get_context_data(datos)
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        #recibimos la información del modelo objeto
        user = request.user    
        persona = request.user.persona
        perfil = request.user.persona.perfil
        
        #Enviamos los datos del formulario con la instacia objeto modelo
        formuser = UsuarioForm(request.POST, instance=user)
        formperfil = PersonaForm(request.POST, instance=persona)
        formperfilaboral = PerfilForm(request.POST, instance=perfil)

        # Validación para el formulario con los datos del usuario
        if formuser.is_valid():
            formuser.save()
            return self.get(request)
        # Validación para el formulario con los datos de persona de usuario
        if formperfil.is_valid():
            formperfil.save()
            return self.get(request)
        # Validación para el formulario con los datos de persona laboral del usuario
        if formperfilaboral.is_valid():
            formperfilaboral.save()
            return self.get(request)
    
    def get_context_data(self, datos, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context["formUsuario"] = UsuarioForm(datos['usuario'])
        context['formPersona'] = PersonaForm(datos['persona'])
        context['formPerfil'] = PerfilForm(datos['perfil'])
        return context
    
    def get_queryset(self, user):
        usuario = json.loads(serializers.serialize('jsonl',User.objects.filter(id=user.id)))
        persona = json.loads(serializers.serialize('jsonl',Persona.objects.all().filter(pk=user.persona.pk)))
        perfil = json.loads(serializers.serialize('jsonl',Perfil.objects.all().filter(pk=user.persona.perfil.pk)))
        
        fields = { 'usuario' : usuario['fields'], 'persona': persona['fields'], 'perfil' : perfil['fields']}
        return fields