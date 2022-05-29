from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

# Create your views here.
@method_decorator(permission_required('is_staff'), name='get')
class Administracion(TemplateView):
    
    template_name = 'Administracion/administracion.html'
    model = User
    
    def get(self, request):
        return render(request, self.template_name)
    
@method_decorator(permission_required('is_staff'), name='get')
class OfertasLaborales(TemplateView):
    
    template_name = 'Administracion/ofertaslaborales.html'
    model = User
    
    def get(self, request):
        return render(request, self.template_name)