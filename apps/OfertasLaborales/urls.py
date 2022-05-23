from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from . import views

"""Escriba las urls de las vistas de su aplicación aqui!!!"""

urlpatterns = [
    path('', views.Inicio.as_view(), name='inicio'),
    path('iniciarsesion/', LoginView.as_view(template_name='OfertasLaborales/iniciarsesion.html'), name='iniciarsesion'),
    path('cerrarsesion/', LogoutView.as_view(template_name='OfertasLaborales/cerrarsesion.html'), name='cerrarsesion'),
    path('busqueda/<str:busqueda>/', views.Busqueda.as_view(), name='busqueda'),
]