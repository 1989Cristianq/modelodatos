"""
Vistas para la aplicación de formularios.
Define las vistas para la gestión de formularios de accidentes.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count, Q
from django.utils import timezone
import pandas as pd
import io
import os
from .models import Accidente, VehiculoInvolucrado, Fallecido, Agente, ZAT, Barrio, CentroPobladoVereda
from .forms import AccidenteForm, VehiculoFormSet, FallecidoFormSet, ReporteForm
from django.http import JsonResponse
from .models import Barrio

# Mixin para verificar permisos según el rol
class SupervisorRequiredMixin(UserPassesTestMixin):
    """
    Mixin que verifica que el usuario actual sea un supervisor o administrador.
    Restringe el acceso a las vistas que lo utilizan.
    """
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.rol == 'ADMINISTRADOR' or self.request.user.rol == 'SUPERVISOR'
        )

# Vistas para listar y ver detalles de accidentes
class ListaAccidentesView(LoginRequiredMixin, ListView):
    """
    Vista para listar todos los accidentes registrados.
    """
    model = Accidente
    template_name = 'formularios/lista_accidentes.html'
    context_object_name = 'accidentes'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar si hay parámetros de búsqueda
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(numero_ipat__icontains=search_query) |
                Q(agente_responsable__nombre__icontains=search_query) |
                Q(barrio__nombre__icontains=search_query) |
                Q(centro_poblado_vereda__nombre__icontains=search_query)
            )
        return queryset.order_by('-fecha_accidente', '-hora_accidente')

class DetalleAccidenteView(LoginRequiredMixin, DetailView):
    """
    Vista para ver los detalles de un accidente específico.
    """
    model = Accidente
    template_name = 'formularios/detalle_accidente.html'
    context_object_name = 'accidente'

# Vistas para crear, editar y eliminar accidentes
@login_required
def crear_accidente(request):
    """
    Vista para crear un nuevo accidente.
    """
    if request.method == 'POST':
        form = AccidenteForm(request.POST, request.FILES)
        if form.is_valid():
            accidente = form.save(commit=False)
            accidente.usuario = request.user
            accidente.save()
            
            # Procesar formsets de vehículos
            vehiculo_formset = VehiculoFormSet(request.POST, instance=accidente)
            if vehiculo_formset.is_valid():
                vehiculos = vehiculo_formset.save()
                
                # Procesar datos de fallecidos para cada vehículo
                for vehiculo in vehiculos:
                    num_fallecidos = vehiculo.numero_fallecidos
                    if num_fallecidos > 0:
                        # Extraer datos de fallecidos del POST
                        for i in range(1, num_fallecidos + 1):
                            nombre_key = f"fallecidos[{vehiculo.id}][{i}][nombre_apellidos]"
                            direccion_key = f"fallecidos[{vehiculo.id}][{i}][direccion]"
                            
                            if nombre_key in request.POST and direccion_key in request.POST:
                                nombre = request.POST.get(nombre_key)
                                direccion = request.POST.get(direccion_key)
                                
                                if nombre and direccion:
                                    Fallecido.objects.create(
                                        vehiculo=vehiculo,
                                        nombre_apellidos=nombre,
                                        direccion=direccion
                                    )
                
                messages.success(request, '¡Accidente registrado exitosamente!')
                return redirect('lista_accidentes')
            else:
                messages.error(request, 'Error en los datos de vehículos involucrados.')
        else:
            messages.error(request, 'Error en el formulario. Por favor revise los datos ingresados.')
    else:
        form = AccidenteForm()
        vehiculo_formset = VehiculoFormSet()
    
    # Obtener datos para los selectores
    agentes = Agente.objects.all()
    zats = ZAT.objects.all()
    barrios = Barrio.objects.all()
    centro_poblados_veredas = CentroPobladoVereda.objects.all()
    
    context = {
        'form': form,
        'vehiculo_formset': vehiculo_formset,
        'agentes': agentes,
        'zats': zats,
        'barrios': barrios,
        'centro_poblados_veredas': centro_poblados_veredas,
        'via_choices': Accidente.VIA_CHOICES,
        'complemento2_choices': Accidente.COMPLEMENTO_2_CHOICES,
        'area_choices': Accidente.AREA_CHOICES,
        'clase_accidente_choices': Accidente.ACCIDENT_CLASS_CHOICES,
        'tipo_via_choices': Accidente.ROAD_TYPE_CHOICES,
        'choque_con_choices': Accidente.COLLISION_TYPE_CHOICES,
        'objeto_fijo_choices': Accidente.FIXED_OBJECT_CHOICES,
        'remitido_a_choices': Accidente.REMITIDO_A_CHOICES,
        'tipo_servicio_choices': VehiculoInvolucrado.SERVICE_TYPE_CHOICES,
        'clase_vehiculo_choices': VehiculoInvolucrado.VEHICLE_CLASS_CHOICES,
        'genero_choices': VehiculoInvolucrado.GENDER_CHOICES,
        'rango_edad_choices': VehiculoInvolucrado.AGE_RANGE_CHOICES,
        'heridos_choices': VehiculoInvolucrado.INJURED_TYPE_CHOICES,
        'fallecidos_choices': VehiculoInvolucrado.INJURED_TYPE_CHOICES,
        'embriaguez_choices': VehiculoInvolucrado.BOOLEAN_CHOICES,
        'grado_embriaguez_choices': VehiculoInvolucrado.INTOXICATION_LEVEL_CHOICES,
        'fallece_despues_choices': VehiculoInvolucrado.BOOLEAN_CHOICES,
    }
    
    return render(request, 'formularios/crear_accidente.html', context)

@login_required
def editar_accidente(request, pk):
    """
    Vista para editar un accidente existente.
    """
    accidente = get_object_or_404(Accidente, pk=pk)
    
    # Verificar permisos según el rol
    if request.user.rol == 'USUARIO' and request.user != accidente.usuario:
        messages.error(request, 'No tiene permisos para editar este accidente.')
        return redirect('lista_accidentes')
    
    if request.method == 'POST':
        form = AccidenteForm(request.POST, request.FILES, instance=accidente)
        if form.is_valid():
            accidente = form.save()
            
            # Procesar formsets de vehículos
            vehiculo_formset = VehiculoFormSet(request.POST, instance=accidente)
            if vehiculo_formset.is_valid():
                vehiculos = vehiculo_formset.save()
                
                # Procesar datos de fallecidos para cada vehículo
                for vehiculo in vehiculos:
                    # Limpiar fallecidos existentes
                    vehiculo.fallecidos.all().delete()
                    
                    num_fallecidos = vehiculo.numero_fallecidos
                    if num_fallecidos > 0:
                        # Extraer datos de fallecidos del POST
                        for i in range(1, num_fallecidos + 1):
                            nombre_key = f"fallecidos[{vehiculo.id}][{i}][nombre_apellidos]"
                            direccion_key = f"fallecidos[{vehiculo.id}][{i}][direccion]"
                            
                            if nombre_key in request.POST and direccion_key in request.POST:
                                nombre = request.POST.get(nombre_key)
                                direccion = request.POST.get(direccion_key)
                                
                                if nombre and direccion:
                                    Fallecido.objects.create(
                                        vehiculo=vehiculo,
                                        nombre_apellidos=nombre,
                                        direccion=direccion
                                    )
                
                messages.success(request, '¡Accidente actualizado exitosamente!')
                return redirect('detalle_accidente', pk=accidente.pk)
            else:
                messages.error(request, 'Error en los datos de vehículos involucrados.')
        else:
            messages.error(request, 'Error en el formulario. Por favor revise los datos ingresados.')
    else:
        form = AccidenteForm(instance=accidente)
        vehiculo_formset = VehiculoFormSet(instance=accidente)
    
    # Obtener datos para los selectores
    agentes = Agente.objects.all()
    zats = ZAT.objects.all()
    barrios = Barrio.objects.all()
    centro_poblados_veredas = CentroPobladoVereda.objects.all()
    
    context = {
        'form': form,
        'vehiculo_formset': vehiculo_formset,
        'accidente': accidente,
        'agentes': agentes,
        'zats': zats,
        'barrios': barrios,
        'centro_poblados_veredas': centro_poblados_veredas,
        'via_choices': Accidente.VIA_CHOICES,
        'complemento2_choices': Accidente.COMPLEMENTO_2_CHOICES,
        'area_choices': Accidente.AREA_CHOICES,
        'clase_accidente_choices': Accidente.ACCIDENT_CLASS_CHOICES,
        'tipo_via_choices': Accidente.ROAD_TYPE_CHOICES,
        'choque_con_choices': Accidente.COLLISION_TYPE_CHOICES,
        'objeto_fijo_choices': Accidente.FIXED_OBJECT_CHOICES,
        'remitido_a_choices': Accidente.REMITIDO_A_CHOICES,
        'tipo_servicio_choices': VehiculoInvolucrado.SERVICE_TYPE_CHOICES,
        'clase_vehiculo_choices': VehiculoInvolucrado.VEHICLE_CLASS_CHOICES,
        'genero_choices': VehiculoInvolucrado.GENDER_CHOICES,
        'rango_edad_choices': VehiculoInvolucrado.AGE_RANGE_CHOICES,
        'heridos_choices': VehiculoInvolucrado.INJURED_TYPE_CHOICES,
        'fallecidos_choices': VehiculoInvolucrado.INJURED_TYPE_CHOICES,
        'embriaguez_choices': VehiculoInvolucrado.BOOLEAN_CHOICES,
        'grado_embriaguez_choices': VehiculoInvolucrado.INTOXICATION_LEVEL_CHOICES,
        'fallece_despues_choices': VehiculoInvolucrado.BOOLEAN_CHOICES,
    }
    
    return render(request, 'formularios/editar_accidente.html', context)

class EliminarAccidenteView(LoginRequiredMixin, SupervisorRequiredMixin, DeleteView):
    """
    Vista para eliminar un accidente.
    Solo accesible para supervisores y administradores.
    """
    model = Accidente
    template_name = 'formularios/eliminar_accidente.html'
    success_url = reverse_lazy('lista_accidentes')
    
    def delete(self, request, *args, **kwargs):
        accidente = self.get_object()
        messages.success(request, f'Accidente #{accidente.numero_ipat} eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

# Vistas para reportes
@login_required
def reportes_view(request):
    """
    Vista para generar reportes de accidentes.
    Solo accesible para supervisores y administradores.
    """
    if request.user.rol not in ['ADMINISTRADOR', 'SUPERVISOR']:
        messages.error(request, 'No tiene permisos para acceder a esta sección.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            # Obtener filtros del formulario
            fecha_desde = form.cleaned_data.get('fecha_desde')
            fecha_hasta = form.cleaned_data.get('fecha_hasta')
            ano = form.cleaned_data.get('ano')
            mes = form.cleaned_data.get('mes')
            agente = form.cleaned_data.get('agente')
            area = form.cleaned_data.get('area')
            
            # Construir filtros para la consulta
            filtros = Q()
            
            if fecha_desde and fecha_hasta:
                filtros &= Q(fecha_accidente__gte=fecha_desde, fecha_accidente__lte=fecha_hasta)
            
            if ano:
                filtros &= Q(fecha_accidente__year=ano)
            
            if mes:
                filtros &= Q(fecha_accidente__month=mes)
            
            if agente:
                filtros &= Q(agente_responsable=agente)
            
            if area:
                filtros &= Q(area=area)
            
            # Obtener accidentes filtrados
            accidentes = Accidente.objects.filter(filtros).select_related(
                'agente_responsable', 'zat', 'barrio', 'centro_poblado_vereda'
            ).prefetch_related('vehiculos', 'vehiculos__fallecidos')
            
            # Preparar datos para el archivo Excel
            data = []
            for accidente in accidentes:
                vehiculos = accidente.vehiculos.all()
                
                # Datos básicos del accidente
                accidente_data = {
                    'Número IPAT': accidente.numero_ipat,
                    'Fecha Accidente': accidente.fecha_accidente,
                    'Hora Accidente': accidente.hora_accidente,
                    'Agente Responsable': accidente.agente_responsable.nombre,
                    'Área': accidente.area,
                    'Ubicación': accidente.get_ubicacion(),
                    'Dirección': accidente.get_direccion_completa(),
                    'Clase Accidente': accidente.clase_accidente,
                    'Tipo Vía': accidente.tipo_via,
                    'Con Heridos': 'Sí' if accidente.con_heridos else 'No',
                    'Con Muertos': 'Sí' if accidente.con_muertos else 'No',
                    'Con Daños Materiales': 'Sí' if accidente.con_danos_materiales else 'No',
                    'Total Vehículos': accidente.total_vehiculos_involucrados,
                    'Fecha Registro': accidente.fecha_registro,
                    'Registrado Por': accidente.usuario.get_full_name() or accidente.usuario.username,
                }
                
                # Datos de vehículos
                for i, vehiculo in enumerate(vehiculos, 1):
                    accidente_data[f'Vehículo {i} - Tipo'] = vehiculo.clase_vehiculo
                    accidente_data[f'Vehículo {i} - Servicio'] = vehiculo.tipo_servicio
                    accidente_data[f'Vehículo {i} - Heridos'] = vehiculo.numero_heridos
                    accidente_data[f'Vehículo {i} - Fallecidos'] = vehiculo.numero_fallecidos
                    accidente_data[f'Vehículo {i} - Embriaguez'] = vehiculo.embriaguez_conductor
                
                data.append(accidente_data)
            
            # Crear DataFrame con los datos
            if data:
                df = pd.DataFrame(data)
                
                # Crear archivo Excel en memoria
                output = io.BytesIO()
                writer = pd.ExcelWriter(output, engine='openpyxl')
                df.to_excel(writer, index=False, sheet_name='Accidentes')
                
                # Ajustar anchos de columna
                worksheet = writer.sheets['Accidentes']
                for i, col in enumerate(df.columns):
                    max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
                    worksheet.column_dimensions[chr(65 + i)].width = max_length
                
                writer.close()
                output.seek(0)
                
                # Preparar respuesta HTTP con el archivo Excel
                response = HttpResponse(
                    output.read(),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                
                # Nombre del archivo
                filename = f"reporte_accidentes_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                
                return response
            else:
                messages.warning(request, 'No se encontraron accidentes con los filtros seleccionados.')
    else:
        form = ReporteForm()
    
    return render(request, 'formularios/reportes.html', {'form': form})

@login_required
def dashboard_view(request):
    """
    Vista para el dashboard que une las aplicaciones.
    """
    # Estadísticas para el dashboard
    total_accidentes = Accidente.objects.count()
    
    # Accidentes del mes actual
    now = timezone.now()
    accidentes_mes = Accidente.objects.filter(
        fecha_accidente__year=now.year,
        fecha_accidente__month=now.month
    ).count()
    
    # Total de usuarios (solo para administradores)
    total_usuarios = 0
    if request.user.rol == 'ADMINISTRADOR':
        from usuarios.models import Usuario
        total_usuarios = Usuario.objects.count()
    
    # Accidentes recientes
    accidentes_recientes = Accidente.objects.order_by('-fecha_accidente', '-hora_accidente')[:5]
    
    context = {
        'total_accidentes': total_accidentes,
        'accidentes_mes': accidentes_mes,
        'total_usuarios': total_usuarios,
        'accidentes_recientes': accidentes_recientes,
    }
    
    return render(request, 'dashboard.html', context)