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