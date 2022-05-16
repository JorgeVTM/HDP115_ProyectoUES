from django.urls import path
from . import views

"""Escriba las urls de las vistas de su aplicación aqui!!!"""

urlpatterns = [
    path('', views.Inicio.as_view(), name='inicio'),
    path('busqueda/<busqueda>', views.Busqueda.as_view(), name='busqueda'),
]