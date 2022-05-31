from django.urls import path
from . import views

"""Escriba las urls de las vistas de su aplicación aqui!!!"""

urlpatterns = [
    path('inicio/', views.Administracion.as_view(), name='administracion'),
    path('inicio/ofertaslaborales/', views.OfertaCrear.as_view(), name='ofertaslaborales'),
    path('inicio/categorias/', views.CategoriaCrear.as_view(), name='categorias'),
    path('inicio/facultades/', views.FacultadCrear.as_view(), name='facultades'),
    path('inicio/sedes/', views.SedeCrear.as_view(), name='sedes'),
    path('inicio/all-ofertaslaborales', views.OfertasAll.as_view(), name='ofertaslaborales_all'),
    path('inicio/all-categorias', views.CategoriasAll.as_view(), name='categorias_all'),
    path('inicio/all-facultades', views.FacultadesAll.as_view(), name='facultades_all'),
    path('inicio/all-sedes', views.SedesAll.as_view(), name='sedes_all'),
    path('inicio/update-ofertaslaborales/<int:pk>', views.OfertaUpdate.as_view(), name='ofertaslaborales_update'),
    path('inicio/update-categorias/<int:pk>^', views.CategoriaUpdate.as_view(), name='categorias_update'),
    path('inicio/update-facultades/<int:pk>^', views.FacultadUpdate.as_view(), name='facultades_update'),
    path('inicio/update-sedes/<int:pk>^', views.SedeUpdate.as_view(), name='sedes_update'),
    path('inicio/delete-ofertalaboral/<int:pk>^', views.OfertaDelete.as_view(), name='ofertalaboral_delete'),
    path('inicio/delete-categoria/<int:pk>^', views.CategoriaDelete.as_view(), name='categoria_delete'),
    path('inicio/delete-facultad/<int:pk>^', views.FacultadDelete.as_view(), name='facultad_delete'),
    path('inicio/delete-sede/<int:pk>^', views.SedeDelete.as_view(), name='sede_delete'),
]