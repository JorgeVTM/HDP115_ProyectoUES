from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from . import views

"""Escriba las urls de las vistas de su aplicación aqui!!!"""

urlpatterns = [
    path('inicio/', views.Administracion.as_view(), name='administracion'),
    path('inicio/<int:pk>/perfil/', views.PerfilAdmin.as_view(), name='perfil-admin'),
    path('inicio/cambiar-contraseña/', PasswordChangeView.as_view(template_name='Administracion/perfiladmin.html'), name='cambiar-contraseña-admin'),
    path('inicio/ofertaslaborales/', views.OfertaCrear.as_view(), name='ofertaslaborales'),
    path('inicio/categorias/', views.CategoriaCrear.as_view(), name='categorias'),
    path('inicio/facultades/', views.FacultadCrear.as_view(), name='facultades'),
    path('inicio/sedes/', views.SedeCrear.as_view(), name='sedes'),
    path('inicio/all-ofertaslaborales', views.OfertasAll.as_view(), name='ofertaslaborales_all'),
    path('inicio/all-categorias', views.CategoriasAll.as_view(), name='categorias_all'),
    path('inicio/all-facultades', views.FacultadesAll.as_view(), name='facultades_all'),
    path('inicio/all-sedes', views.SedesAll.as_view(), name='sedes_all'),
    path('inicio/update/<int:pk>^/ofertaslaborales/', views.OfertaUpdate.as_view(), name='ofertaslaborales_update'),
    path('inicio/update/<int:pk>^/categorias/', views.CategoriaUpdate.as_view(), name='categorias_update'),
    path('inicio/update/<int:pk>^/facultades', views.FacultadUpdate.as_view(), name='facultades_update'),
    path('inicio/update/<int:pk>^/sedes', views.SedeUpdate.as_view(), name='sedes_update'),
    path('inicio/delete/<int:pk>^/ofertalaboral/', views.OfertaDelete.as_view(), name='ofertalaboral_delete'),
    path('inicio/delete/<int:pk>^/categoria/', views.CategoriaDelete.as_view(), name='categoria_delete'),
    path('inicio/delete/<int:pk>^/facultad/', views.FacultadDelete.as_view(), name='facultad_delete'),
    path('inicio/delete/<int:pk>^/sede/', views.SedeDelete.as_view(), name='sede_delete'),
]