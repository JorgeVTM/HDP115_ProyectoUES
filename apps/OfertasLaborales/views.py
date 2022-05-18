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
    
    def get(self, request):
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
    
class Seach(Inicio):
     
    def get(self, request, busqueda):
        context = self.get_context_data(busqueda, form=BusquedaForm())
        return render(request, self.template_name, context)
    
    def get_queryset(self, busqueda):
        resultado = OfertaLaboral.objects.filter(area_de_trabajo__icontains=busqueda)
        return resultado
    
    def post(self, request, busqueda):
        context = self.get_context_data(busqueda, form=BusquedaForm(request.POST))
        print(busqueda)
        return self.get(request,busqueda)

    def get_context_data(self, busqueda, **kwargs):
        context = super().get_context_data(**kwargs)
        ofertas = self.get_queryset(busqueda)
        context["ofertaslaborales"] = ofertas
        context['resultados'] = ofertas.count()
        return context
    
       
class FiltroSeach(Inicio):
            
    def get(self, request, filtro):
        context = self.get_context_data(filtro, form=BusquedaForm())
         
        return render(request, self.template_name, context)
    
    def post(self, request, filtro):
        form = BusquedaForm(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data['busqueda']
        return redirect('buscar', busqueda)
    
    def get_context_data(self, filtro, **kwargs):
        context = super().get_context_data(**kwargs)
        
        ofertas = self.get_queryset(filtro)
        context['ofertaslaborales'] = ofertas
        context['resultados'] = ofertas.count()
        context['filtro'] = filtro
        
        for objeto in self.object_list:
            context[objeto.__name__] = objeto.objects.annotate(Count('ofertalaboral')).exclude(nombre=filtro)
            
        return context
                                                       
    def get_queryset(self, busqueda):
        for objeto in self.object_list:
            try: 
                resultado = objeto.objects.get(nombre=busqueda).ofertalaboral_set.all()
                return resultado
            except objeto.DoesNotExist:
                resultado = None
        return resultado