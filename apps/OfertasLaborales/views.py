from os import system
from django.db.models import *
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy, reverse, resolve
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import *
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
class OfertaView(DetailView):
    model = OfertaLaboral
    template_name = 'OfertasLaborales/solicitudoferta.html'
    
    def post(self, request, pk):
        solicitud = SolicitudLaboral
        try:
            solicitud = SolicitudLaboral.objects.get(user=request.user,ofertalaboral_id=pk)
            messages.success(request, 'Ya has enviado una solicitud laboral para esta oferta!!!')
            return render(request, self.template_name, {'ofertalaboral': self.get_object() })
        except solicitud.DoesNotExist:
            solicitud = SolicitudLaboral.objects.create(user=request.user,ofertalaboral_id=pk)
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
class PerfilUsuario(UpdateView):
    
    model = User
    form_class = UsuarioForm
    template_name = 'OfertasLaborales/perfilusuario.html'
    
    def post(self, request, pk):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos actualizados correctamente')
        return render(request, self.template_name, {'form': form})

@method_decorator(decorators, name='get')
class InfoPersonal(UpdateView):
    
    model = Persona
    form_class = PersonaForm
    template_name = 'OfertasLaborales/perfilusuario.html'
    
    def post(self, request, pk):
        form = self.form_class(request.POST, instance=request.user.persona)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos actualizados correctamente')
        return render(request, self.template_name, {'form': form})

@method_decorator(decorators, name='get')
class DatoLaboral(UpdateView):
    
    model = Perfil
    form_class = PerfilForm
    template_name = 'OfertasLaborales/perfilusuario.html'
    success_url = reverse_lazy('informacion')
    
    def post(self, request, pk):
        form = self.form_class(request.POST, instance=request.user.persona.perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos actualizados correctamente')
        return render(request, self.template_name, {'form': form})
    
@method_decorator(decorators, name='get')
class Informacion(TemplateView):
    
    template_name = 'OfertasLaborales/informacion.html'
    
    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)