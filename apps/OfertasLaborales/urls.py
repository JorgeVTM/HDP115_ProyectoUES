from django.urls import path
from . import views

"""Escriba las urls de las vistas de su aplicación aqui!!!"""

urlpatterns = [
    path('', views.Inicio.as_view(), name='inicio'),
    # path('busqueda/<busqueda>', views.Busqueda.as_view(), name='busqueda'),
    # path('categoria/<busqueda>', views.CategoriaSeach.as_view(), name='categoria'),
    path('<str:busqueda>', views.Seach.as_view(), name='buscar'),
    path('Seach/<str:filtro>', views.FiltroSeach.as_view(), name='Seach'),
    # path('<str:categoria>/<str:facultad>/', views.FacultadSeach.as_view(), name='facultad'),
    # path('<str:categoria>/<str:facultad>/<str:sede>', views.SedeSeach.as_view(), name='sede'),
]