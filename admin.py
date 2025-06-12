"""
Configuración del administrador de Django para la aplicación de formularios.
Define cómo se muestran y gestionan los formularios en el panel de administración.
"""
from django.contrib import admin
from .models import (
    Accidente, VehiculoInvolucrado, Fallecido, Agente, ZAT, Barrio, 
    CentroPobladoVereda, HipotesisConductor, HipotesisVehiculo, 
    HipotesisVia, HipotesisPeaton
)

class VehiculoInvolucradoInline(admin.TabularInline):
    """
    Configuración para mostrar vehículos involucrados en línea con el accidente.
    """
    model = VehiculoInvolucrado
    extra = 1

class FallecidoInline(admin.TabularInline):
    """
    Configuración para mostrar fallecidos en línea con el vehículo.
    """
    model = Fallecido
    extra = 1

@admin.register(Accidente)
class AccidenteAdmin(admin.ModelAdmin):
    """
    Configuración del administrador para el modelo Accidente.
    """
    list_display = ('numero_ipat', 'fecha_accidente', 'hora_accidente', 'agente_responsable', 
                    'area', 'clase_accidente', 'total_vehiculos_involucrados')
    list_filter = ('fecha_accidente', 'area', 'clase_accidente', 'con_heridos', 'con_muertos')
    search_fields = ('numero_ipat', 'agente_responsable__nombre')
    date_hierarchy = 'fecha_accidente'
    inlines = [VehiculoInvolucradoInline]
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_ipat', 'agente_responsable', 'fecha_accidente', 'hora_accidente', 
                      'dias_establecidos_entrega', 'fecha_real_entrega', 'usuario')
        }),
        ('Tipo de Accidente', {
            'fields': ('total_vehiculos_involucrados', 'con_heridos', 'con_muertos', 'con_danos_materiales')
        }),
        ('Ubicación', {
            'fields': ('via', 'numero_via', 'complemento1', 'complemento2', 'otra_informacion_direccion', 
                      'area', 'zat', 'barrio', 'centro_poblado_vereda')
        }),
        ('Detalles del Accidente', {
            'fields': ('clase_accidente', 'otro_clase_accidente', 'tipo_via', 'choque_con', 
                      'objeto_fijo', 'otro_objeto_fijo')
        }),
        ('Hipótesis', {
            'fields': ('hipotesis_conductor1', 'hipotesis_conductor2', 'hipotesis_conductor3', 'hipotesis_conductor4',
                      'hipotesis_vehiculo1', 'hipotesis_vehiculo2', 'hipotesis_via1', 'hipotesis_via2',
                      'hipotesis_peaton1', 'hipotesis_peaton2')
        }),
        ('Información Adicional', {
            'fields': ('remitido_a', 'croquis_pdf')
        }),
    )

@admin.register(VehiculoInvolucrado)
class VehiculoInvolucradoAdmin(admin.ModelAdmin):
    """
    Configuración del administrador para el modelo VehiculoInvolucrado.
    """
    list_display = ('accidente', 'clase_vehiculo', 'tipo_servicio', 'numero_heridos', 'numero_fallecidos')
    list_filter = ('clase_vehiculo', 'tipo_servicio', 'embriaguez_conductor')
    search_fields = ('accidente__numero_ipat',)
    inlines = [FallecidoInline]

# Registrar los modelos adicionales
admin.site.register(Agente)
admin.site.register(ZAT)
admin.site.register(Barrio)
admin.site.register(CentroPobladoVereda)
admin.site.register(HipotesisConductor)
admin.site.register(HipotesisVehiculo)
admin.site.register(HipotesisVia)
admin.site.register(HipotesisPeaton)