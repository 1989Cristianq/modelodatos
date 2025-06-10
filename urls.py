"""
Configuración de URLs para la aplicación de formularios.
Define las rutas para las diferentes vistas relacionadas con la gestión de formularios.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Listar y ver detalles de accidentes
    path('', views.ListaAccidentesView.as_view(), name='lista_accidentes'),
    path('<int:pk>/', views.DetalleAccidenteView.as_view(), name='detalle_accidente'),
    path('api/barrios-por-zat/<int:zat_id>/', views.barrios_por_zat, name='barrios_por_zat'),
    
    # Crear, editar y eliminar accidentes
    path('crear/', views.crear_accidente, name='crear_accidente'),
    path('editar/<int:pk>/', views.editar_accidente, name='editar_accidente'),
    path('eliminar/<int:pk>/', views.EliminarAccidenteView.as_view(), name='eliminar_accidente'),
    
    # Reportes
    path('reportes/', views.reportes_view, name='reportes'),
]