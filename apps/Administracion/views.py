from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.list import MultipleObjectMixin

# Create your views here.

class Administracion(ListView):
    
    template_name = 'administracion.html'
    
    def get(self, request):
        return render(request, self.template_name)