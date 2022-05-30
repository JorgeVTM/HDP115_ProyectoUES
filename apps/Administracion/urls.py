from django.urls import path
from . import views

"""Escriba las urls de las vistas de su aplicación aqui!!!"""

urlpatterns = [
    path('administracion/', views.Administracion.as_view(), name='administracion'),
    path('administracion/ofertaslaborales/', views.OfertasLaborales.as_view(), name='ofertaslaborales'),
    path('administracion/categorias/', views.Categorias.as_view(), name='categorias'),
    path('administracion/facultades/', views.Facultades.as_view(), name='facultades'),
    path('administracion/sedes/', views.Sedes.as_view(), name='sedes'),
    path('administracion/ofertaslaborales/ofertaslaborales_all', views.OfertasLaboralesAll.as_view(), name='ofertaslaborales_all'),
    path('administracion/categorias/categorias_all', views.CategoriasAll.as_view(), name='categorias_all'),
    path('administracion/facultades/facultades_all', views.FacultadesAll.as_view(), name='facultades_all'),
    path('administracion/sedes/sedes_all', views.SedesAll.as_view(), name='sedes_all'),
]