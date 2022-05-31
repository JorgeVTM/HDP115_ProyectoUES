from django.urls import path
from . import views

"""Escriba las urls de las vistas de su aplicación aqui!!!"""

urlpatterns = [
    path('inicio/', views.Administracion.as_view(), name='administracion'),
    path('inicio/ofertaslaborales/', views.OfertasLaborales.as_view(), name='ofertaslaborales'),
    path('inicio/categorias/', views.Categorias.as_view(), name='categorias'),
    path('inicio/facultades/', views.Facultades.as_view(), name='facultades'),
    path('inicio/sedes/', views.Sedes.as_view(), name='sedes'),
    path('inicio/ofertaslaborales_all', views.OfertasLaboralesAll.as_view(), name='ofertaslaborales_all'),
    path('inicio/categorias_all', views.CategoriasAll.as_view(), name='categorias_all'),
    path('inicio/facultades_all', views.FacultadesAll.as_view(), name='facultades_all'),
    path('inicio/sedes_all', views.SedesAll.as_view(), name='sedes_all'),
    path('inicio/ofertaslaborales_update/<int:pk>^', views.OfertasLaboralesUpdate.as_view(), name='ofertaslaborales_update'),
    path('inicio/categorias_update/<int:pk>^', views.CategoriasUpdate.as_view(), name='categorias_update'),
    path('inicio/facultades_update/<int:pk>^', views.FacultadesUpdate.as_view(), name='facultades_update'),
    path('inicio/sedes_update/<int:pk>^', views.SedesUpdate.as_view(), name='sedes_update'),
    path('inicio/delete-ofertalaboral/<int:pk>^', views.OfertasLaboralesDelete.as_view(), name='ofertalaboral_delete'),
    path('inicio/delete-categoria/<int:pk>^', views.CategoriasDelete.as_view(), name='categoria_delete'),
    path('inicio/delete-facultad/<int:pk>^', views.FacultadesDelete.as_view(), name='facultad_delete'),
    path('inicio/delete-sede/<int:pk>^', views.SedesDelete.as_view(), name='sede_delete'),
]