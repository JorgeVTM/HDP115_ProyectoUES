from django.urls import path
from . import views

"""Escriba las urls de las vistas de su aplicación aqui!!!"""

urlpatterns = [
    path('administracion/', views.Administracion.as_view(), name='administracion')
]