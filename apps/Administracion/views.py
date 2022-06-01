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
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
@method_decorator(permission_required('is_staff'), name='get')
class Administracion(TemplateView):
    
    template_name = 'Administracion/administracion.html'
    model = User
    
    def get(self, request):
        return render(request, self.template_name)    
    
@method_decorator(permission_required('is_staff'), name='get')  
class PerfilAdmin(UpdateView):
    
    model = User
    form_class = UsuarioForm
    template_name = 'Administracion/perfiladmin.html'
    
    def post(self, request, pk):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos actualizados correctamente')
        return render(request, self.template_name, {'form': form}) 
    
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objeto"] = self.objeto
        context["titulo"] = self.titulo
        return context

@method_decorator(permission_required('is_staff'), name='get')
class ObjetoUpdate(UpdateView):
    
    template_name = 'Administracion/gestionregistros.html'
    
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
    
class OfertaCrear(SuccessMessageMixin, ObjetoCreate):
    
    model = OfertaLaboral
    objeto = 'OfertaLaboral'
    titulo = 'Registrar una nueva oferta Laboral'
    form_class = OfertasLaboralesForm
    success_url = reverse_lazy('ofertaslaborales_all')
    success_message = "Se ha creado un nuevo registro %(area_de_trabajo)s"
    
class OfertaUpdate(SuccessMessageMixin, ObjetoUpdate):
    
    model = OfertaLaboral
    objeto = 'OfertaLaboral'
    titulo = 'Actualizar datos de Ofertas Laborales'
    form_class = OfertasLaboralesForm
    success_url = reverse_lazy('ofertaslaborales_all')
    success_message = "%(area_de_trabajo)s fue modificado correctamente"
            
class OfertaDelete(SuccessMessageMixin, ObjetoDelete):
    
    model = OfertaLaboral
    objeto = 'OfertaLaboral'
    titulo = 'Eliminar una Ofertas Laborales'
    success_url = reverse_lazy('ofertaslaborales_all')
    success_message = "El registro fue eliminado"

class CategoriasAll(ObjetosAll):
    
    model = Categoria
    paginate_by = 20
    objeto = 'Categoria'
    titulo = 'Listado de Categorias'
    
class CategoriaCrear(SuccessMessageMixin, ObjetoCreate):
    
    model = Categoria
    objeto = 'Categoria'
    titulo = 'Registrar una nueva Categoria'
    form_class = CategoriaForm
    success_url = reverse_lazy('categorias_all')
    success_message = "Se ha creado un nuevo registro %(nombre)s"
    
class CategoriaUpdate(SuccessMessageMixin, ObjetoUpdate):
    
    model = Categoria
    objeto = 'Categoria'
    titulo = 'Actualizar datos de Categoria'
    form_class = CategoriaForm
    success_url = reverse_lazy('categorias_all')
    success_message = "%(nombre)s fue modificado correctamente"
            
class CategoriaDelete(SuccessMessageMixin, ObjetoDelete):
    
    model = Categoria
    objeto = 'Categoria'
    titulo = 'Eliminar una Categoria'
    success_url = reverse_lazy('categorias_all')
    success_message = "El registro fue eliminado"

class FacultadesAll(ObjetosAll):
    
    model = Facultad
    paginate_by = 20
    objeto = 'Facultad'
    titulo = 'Listado de Facultades'
    
class FacultadCrear(SuccessMessageMixin, ObjetoCreate):
    
    model = Facultad
    objeto = 'Facultad'
    titulo = 'Registrar una nueva Facultad'
    form_class = FacultadForm
    success_url = reverse_lazy('facultades_all')
    success_message = "Se ha creado un nuevo registro %(nombre)s"
    
class FacultadUpdate(SuccessMessageMixin, ObjetoUpdate):
    
    model = Facultad
    objeto = 'Facultad'
    titulo = 'Actualizar datos de Facultad'
    form_class = FacultadForm
    success_url = reverse_lazy('facultades_all')
    success_message = "%(nombre)s fue modificado correctamente"
            
class FacultadDelete(SuccessMessageMixin, ObjetoDelete):
    
    model = Facultad
    objeto = 'Facultad'
    titulo = 'Eliminar una Facultad'
    success_url = reverse_lazy('facultades_all')
    success_message = "El registro fue eliminado"

class SedesAll(ObjetosAll):
    
    model = Sede
    paginate_by = 20
    objeto = 'Sede'
    titulo = 'Listado de Sedes'
    
class SedeCrear(SuccessMessageMixin,ObjetoCreate):
    
    model = Sede
    objeto = 'Sede'
    titulo = 'Registrar una nueva Sede'
    form_class = SedeForm
    success_url = reverse_lazy('sedes_all')
    success_message = "Se ha creado un nuevo registro %(nombre)s"
    
class SedeUpdate(SuccessMessageMixin, ObjetoUpdate):
    
    model = Sede
    objeto = 'Sede'
    titulo = 'Actualizar datos de Sede'
    form_class = SedeForm
    success_url = reverse_lazy('sedes_all')
    success_message = "%(nombre)s fue modificado correctamente"
            
class SedeDelete(SuccessMessageMixin, ObjetoDelete):
    
    model = Sede
    objeto = 'Sede'
    titulo = 'Eliminar una Sede'
    success_url = reverse_lazy('sedes_all')
    success_message = "El registro fue eliminado"