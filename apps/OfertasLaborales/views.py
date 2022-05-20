from os import system
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.models import User
from .models import *
from .forms import *

# Create your views here.

class Inicio(ListView, MultipleObjectMixin):
    
    template_name = 'OfertasLaborales/inicio.html'
    object_list= (Categoria, Facultad, Sede)
    guardados = {}  
    
    def get(self, request):
        self.guardados.clear()
        context = self.get_context_data(form=BusquedaForm())
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = BusquedaForm(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data['busqueda']
        return redirect('buscar', busqueda)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ofertaslaborales'] = OfertaLaboral.objects.all()
        context['resultados'] = OfertaLaboral.objects.count()
        
        for objeto in self.object_list:
            context[objeto.__name__] = objeto.objects.annotate(Count('ofertalaboral'))
        return context
    
    def filtros(self, objeto, **kwargs):
        filtro = {}
        for key,value in kwargs.items():
            filtro[key] = value
        return objeto.objects.filter(**filtro) 
    
class Seach(Inicio):
     
    def get(self, request, busqueda):
        context = self.get_context_data(busqueda, form=BusquedaForm())
        return render(request, self.template_name, context)
    
    def post(self, request, busqueda):
        form = BusquedaForm(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data['busqueda']
        return redirect('buscar', busqueda)

    def get_context_data(self, busqueda, **kwargs):
        context = super().get_context_data(**kwargs)
        ofertas = self.get_queryset(busqueda)
        context["ofertaslaborales"] = ofertas
        return context
    
    def get_queryset(self, busqueda):
        resultado = OfertaLaboral.objects.filter(area_de_trabajo__icontains=busqueda)
        return resultado
        
class Categorias(Inicio):
    
    
    def get(self, request, busqueda):
        context = self.get_context_data(busqueda, form=BusquedaForm())    
        return render(request, self.template_name, context)
       
    def get_context_data(self, busqueda, **kwargs):
        context = super().get_context_data(**kwargs)
        
        self.guardados['categoria__nombre'] = busqueda

        
        context['ofertaslaborales'] = self.filtros(OfertaLaboral,**self.guardados)

        return context
           
class Facultades(Inicio):
    
    def get(self, request, busqueda):
        context = self.get_context_data(busqueda, form=BusquedaForm())    
        return render(request, self.template_name, context)

    def get_context_data(self, busqueda, **kwargs):
        context = super().get_context_data(**kwargs)
        
        self.guardados['facultad__nombre'] = busqueda
        print(self.guardados)
        context['ofertaslaborales'] = self.filtros(OfertaLaboral,**self.guardados)

        return context

class Sedes(Inicio):
    
    def get(self, request, busqueda):
        context = self.get_context_data(busqueda, form=BusquedaForm())    
        return render(request, self.template_name, context)

    def get_context_data(self, busqueda, **kwargs):
        context = super().get_context_data(**kwargs)
        
        self.guardados['sede__nombre'] = busqueda
        context['ofertaslaborales'] = self.filtros(OfertaLaboral,**self.guardados)

        return context