from os import system
from django.urls import reverse_lazy, reverse, resolve
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DetailView
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import *
from django.db.models import *
from apps.OfertasLaborales.models import *
from apps.OfertasLaborales.forms import *
from .models import *
from .forms import *

# Create your views here.
@method_decorator(permission_required('is_staff'), name='get')
class Administracion(TemplateView):
    
    template_name = 'Administracion/administracion.html'
    model = User
    
    def get(self, request):
        return render(request, self.template_name)     
    
@method_decorator(permission_required('is_staff'), name='get')  
class ObjetosAll(ListView):
    
    template_name = 'Administracion/gestionTabla.html'
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objeto"] = self.objeto
        context["titulo"] = self.titulo
        return context

@method_decorator(permission_required('is_staff'), name='get')  
class ObjetoCreate(CreateView):
    
    template_name = 'Administracion/gestionregistros.html'
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objeto"] = self.objeto
        context["titulo"] = self.titulo
        return context

@method_decorator(permission_required('is_staff'), name='get')
class ObjetoUpdate(UpdateView):
    
    template_name = 'Administracion/gestionregistros.html'
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objeto"] = self.objeto
        context["titulo"] = self.titulo
        return context

@method_decorator(permission_required('is_staff'), name='get')
class ObjetoDelete(DeleteView):
    
    template_name = 'Administracion/eliminarregistros.html'
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objeto"] = self.objeto
        context["titulo"] = self.titulo
        if self.objeto == 'Categoria' or self.objeto == 'Facultad' or self.objeto == 'Sede':
            context["relacionados"] = self.model.objects.get(pk=self.object.pk).ofertalaboral_set.all()
        return context

class OfertasAll(ObjetosAll):
    
    model = OfertaLaboral
    paginate_by = 20
    objeto = 'OfertaLaboral'
    titulo = 'Listado de Ofertas Laborales'
    
class OfertaCrear(ObjetoCreate):
    
    model = OfertaLaboral
    objeto = 'OfertaLaboral'
    titulo = 'Registrar una nueva oferta Laboral'
    get_form = OfertasLaboralesForm
    success_url = reverse_lazy('ofertaslaborales_all')
    
class OfertaUpdate(ObjetoUpdate):
    
    model = OfertaLaboral
    objeto = 'OfertaLaboral'
    titulo = 'Actualizar datos de Ofertas Laborales'
    get_form = OfertasLaboralesForm
    success_url = reverse_lazy('ofertaslaborales_all')
            
class OfertaDelete(ObjetoDelete):
    
    model = OfertaLaboral
    objeto = 'OfertaLaboral'
    titulo = 'Eliminar una Ofertas Laborales'
    success_url = reverse_lazy('ofertaslaborales_all')

class CategoriasAll(ObjetosAll):
    
    model = Categoria
    paginate_by = 20
    objeto = 'Categoria'
    titulo = 'Listado de Categorias'
    
class CategoriaCrear(ObjetoCreate):
    
    model = Categoria
    objeto = 'Categoria'
    titulo = 'Registrar una nueva Categoria'
    get_form = CategoriaForm
    success_url = reverse_lazy('categorias_all')
    
class CategoriaUpdate(ObjetoUpdate):
    
    model = Categoria
    objeto = 'Categoria'
    titulo = 'Actualizar datos de Categoria'
    get_form = CategoriaForm
    success_url = reverse_lazy('categorias_all')
            
class CategoriaDelete(ObjetoDelete):
    
    model = Categoria
    objeto = 'Categoria'
    titulo = 'Eliminar una Categoria'
    success_url = reverse_lazy('categorias_all')

class FacultadesAll(ObjetosAll):
    
    model = Facultad
    paginate_by = 20
    objeto = 'Facultad'
    titulo = 'Listado de Facultades'
    
class FacultadCrear(ObjetoCreate):
    
    model = Facultad
    objeto = 'Facultad'
    titulo = 'Registrar una nueva Facultad'
    get_form = FacultadForm
    success_url = reverse_lazy('facultades_all')
    
class FacultadUpdate(ObjetoUpdate):
    
    model = Facultad
    objeto = 'Facultad'
    titulo = 'Actualizar datos de Facultad'
    get_form = FacultadForm
    success_url = reverse_lazy('facultades_all')
            
class FacultadDelete(ObjetoDelete):
    
    model = Facultad
    objeto = 'Facultad'
    titulo = 'Eliminar una Facultad'
    success_url = reverse_lazy('facultades_all')

class SedesAll(ObjetosAll):
    
    model = Sede
    paginate_by = 20
    objeto = 'Sede'
    titulo = 'Listado de Sedes'
    
class SedeCrear(ObjetoCreate):
    
    model = Sede
    objeto = 'Sede'
    titulo = 'Registrar una nueva Sede'
    get_form = SedeForm
    success_url = reverse_lazy('sedes_all')
    
class SedeUpdate(ObjetoUpdate):
    
    model = Sede
    objeto = 'Sede'
    titulo = 'Actualizar datos de Sede'
    get_form = SedeForm
    success_url = reverse_lazy('sedes_all')
            
class SedeDelete(ObjetoDelete):
    
    model = Sede
    objeto = 'Sede'
    titulo = 'Eliminar una Sede'
    success_url = reverse_lazy('sedes_all')