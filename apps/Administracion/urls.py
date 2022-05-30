from django.urls import path
from . import views

"""Escriba las urls de las vistas de su aplicación aqui!!!"""

urlpatterns = [
    path('administracion/', views.Administracion.as_view(), name='administracion'),
    path('administracion/ofertaslaborales/', views.OfertasLaborales.as_view(), name='ofertaslaborales'),
    path('administracion/categorias/', views.Categorias.as_view(), name='categorias'),
    path('administracion/facultades/', views.Facultades.as_view(), name='facultades'),
    path('administracion/sedes/', views.Sedes.as_view(), name='sedes'),
]