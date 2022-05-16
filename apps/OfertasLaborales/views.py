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
        nombres = ('ofertaslaborales', 'categorias', 'facultades', 'sedes')
        index = 0
        for objeto in self.object_list:
            context[nombres[index]] = objeto.objects.all()
            index +=1
        return context
    
class Busqueda(ListView, MultipleObjectMixin):
    
    template_name = 'OfertasLaborales/inicio.html'
    object_list= (OfertaLaboral, Categoria, Facultad, Sede)
    
    def get(self, request, busqueda):
        print(busqueda)

        context = self.get_context_data(form = BusquedaForm())
        context['ofertaslaborales'] = self.get_queryset(busqueda)
        return render(request, self.template_name, context)
    
    def post(self, request, busqueda):
        form = BusquedaForm(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data['busqueda']
        return redirect('busqueda', busqueda)
    
    def get_queryset(self, busqueda):
        ofertaslaborales = OfertaLaboral.objects.filter(area_de_trabajo__contains=busqueda)
        return ofertaslaborales

    
#Para buscar LIKE contiene una palabra o caracter...
 # context['ofertaslaborales'] = OfertaLaboral.objects.filter(area_de_trabajo__contains='Limpieza')
# print(OfertaLaboral.objects.filter(area_de_trabajo__contains='Limpieza'))