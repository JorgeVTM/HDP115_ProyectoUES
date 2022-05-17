from os import system
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.models import User
from .models import *
from .forms import *

# Create your views here.

class Inicio(ListView, MultipleObjectMixin):
    
    template_name = 'OfertasLaborales/inicio.html'
    object_list= (OfertaLaboral, Categoria, Facultad, Sede)
    
    def get(self, request):
        context = self.get_context_data(form=BusquedaForm())
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = BusquedaForm(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data['busqueda']
        return redirect('busqueda', busqueda)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ofertaslaborales'] = OfertaLaboral.objects.all()
        context['resultados'] = OfertaLaboral.objects.count()
        context['categorias'] = Categoria.objects.annotate(Count('ofertalaboral'))
        context['facultades'] = Facultad.objects.annotate(Count('ofertalaboral'))
        context['sedes'] = Sede.objects.annotate(Count('ofertalaboral'))
        return context

class Busqueda(ListView, MultipleObjectMixin):
    
    template_name = 'OfertasLaborales/inicio.html'
    object_list= (Categoria, Facultad, Sede)
    
    def get(self, request, busqueda):
        
        context = self.get_context_data(busqueda)
        return render(request, self.template_name,context)

    def get_context_data(self, busqueda, **kwargs):
        context = super().get_context_data(**kwargs)

        for objeto in self.object_list:
            resultado = self.get_queryset(busqueda, objeto)
            if resultado is not None:
                context['ofertaslaborales'] = resultado
                context['resultados'] = resultado.count()

                return context
              
        return context
    
    def get_queryset(self, busqueda, objeto):
        try:
            resultado = objeto.objects.get(nombre=busqueda).ofertalaboral_set.all()
        except objeto.DoesNotExist:
            resultado = None
        return resultado
