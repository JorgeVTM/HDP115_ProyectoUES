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
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nombres = ('ofertaslaborales', 'categorias', 'facultades', 'sedes')
        index = 0
        for objeto in self.object_list:
            context[nombres[index]] = objeto.objects.all()
            index +=1
        return context
    