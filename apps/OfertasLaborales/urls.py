from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from . import views

"""Escriba las urls de las vistas de su aplicación aqui!!!"""

urlpatterns = [
    path('', views.Inicio.as_view(), name='inicio'),
    path('busqueda/<str:busqueda>/', views.Busqueda.as_view(), name='busqueda'),
    path('solicitud/<int:pk>', views.OfertaView.as_view(), name='solicitud'),
    path('iniciarsesion/', LoginView.as_view(template_name='OfertasLaborales/iniciarsesion.html'), name='iniciarsesion'),
    path('cerrarsesion/', LogoutView.as_view(template_name='OfertasLaborales/cerrarsesion.html'), name='cerrarsesion'),
    path('registrarse/', views.Registrarse.as_view(), name='registrarse'),
    path('perfil-usuario/<int:pk>', views.PerfilUsuario.as_view(), name='perfil-usuario'),
    path('info/<int:pk>/personal', views.InfoPersonal.as_view(), name='info-personal'),
    path('datos-laboral/<int:pk>', views.DatoLaboral.as_view(), name='datos-laboral'),
    path('cambiar-contraseña/', PasswordChangeView.as_view(template_name='OfertasLaborales/perfilusuario.html'), name='cambiar-contraseña'),
    path('informacion/', views.Informacion.as_view(), name='informacion'),
]