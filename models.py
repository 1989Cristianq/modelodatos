"""
Modelos para la aplicación de formularios.
Define los modelos para el registro de accidentes de tránsito y sus detalles.
"""
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from usuarios.models import Usuario

class Agente(models.Model):
    """
    Modelo para almacenar información de los agentes responsables.
    """
    AGENTE_CHOICES = [
        ('WILSON SAIZ', 'Wilson Saiz'),
        ('ANDREA GUAVITA', 'Andrea Guavita'),
        ('SANDRA LOPEZ', 'Sandra Lopez'),
        ('ANGEL FORERO', 'Angel Forero'),
        ('MAURICIO MORALES', 'Mauricio Morales'),
        ('DIEGO PEREZ', 'Diego Perez'),
        ('CARLOS VARON', 'Carlos Varon'),
        ('NESTOR VALBUENA', 'Nestor Valbuena'),
        ('MIGUEL HERNANDEZ', 'Miguel Hernandez'),
        ('LEONARDO RAMIREZ', 'Leonardo Ramirez'),
        ('EDER PERILLA', 'Eder Perilla'),
        ('EDIXON MANCERA', 'Edixon Mancera'),
        ('RICARDO SANCHEZ', 'Ricardo Sanchez'),
        ('MARCELA MARTINEZ', 'Marcela Martinez'),
        ('VIANY NOVA', 'Viany Nova'),
        ('JAVIER TIMOTE', 'Javier Timote'),
        ('YAMPIER RUIZ', 'Yampier Ruiz'),
        ('CAMILO GUASCA', 'Camilo Guasca'),
        ('CRISTIAN REY', 'Cristian Rey'),
        ('DUVAN SANCHEZ', 'Duvan Sanchez'),
        ('POLCA', 'Polca'),
    ]
    
    nombre = models.CharField(max_length=50, choices=AGENTE_CHOICES)
    
    def __str__(self):
        return self.nombre

class ZAT(models.Model):
    """
    Modelo para almacenar las Zonas de Análisis de Tránsito (ZAT).
    """
    nombre = models.CharField(max_length=10)
    
    def __str__(self):
        return self.nombre

class Barrio(models.Model):
    """
    Modelo para almacenar los barrios de la ciudad.
    """
    nombre = models.CharField(max_length=100)
    zat = models.ForeignKey(ZAT, on_delete=models.CASCADE, related_name='barrios')
    
    def __str__(self):
        return self.nombre

class CentroPobladoVereda(models.Model):
    """
    Modelo para almacenar los centros poblados y veredas para áreas rurales.
    """
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class HipotesisConductor(models.Model):
    """
    Modelo para almacenar las hipótesis relacionadas con el conductor.
    """
    descripcion = models.CharField(max_length=255)
    
    def __str__(self):
        return self.descripcion

class HipotesisVehiculo(models.Model):
    """
    Modelo para almacenar las hipótesis relacionadas con el vehículo.
    """
    descripcion = models.CharField(max_length=255)
    
    def __str__(self):
        return self.descripcion

class HipotesisVia(models.Model):
    """
    Modelo para almacenar las hipótesis relacionadas con la vía.
    """
    descripcion = models.CharField(max_length=255)
    
    def __str__(self):
        return self.descripcion

class HipotesisPeaton(models.Model):
    """
    Modelo para almacenar las hipótesis relacionadas con el peatón.
    """
    descripcion = models.CharField(max_length=255)
    
    def __str__(self):
        return self.descripcion

class Accidente(models.Model):
    """
    Modelo principal para almacenar la información de accidentes de tránsito.
    """
    # Opciones para campos de selección
    VIA_CHOICES = [
        ('CALLE', 'Calle'),
        ('CARRERA', 'Carrera'),
        ('DIAGONAL', 'Diagonal'),
        ('CASA', 'Casa'),
        ('LOTE', 'Lote'),
        ('MANZANA', 'Manzana'),
        ('AVENIDA', 'Avenida'),
        ('VEREDA', 'Vereda'),
        ('KILOMETRO', 'Kilometro'),
        ('TRANSVERSAL', 'Transversal'),
        ('VÍA', 'Vía'),
    ]
    
    AREA_CHOICES = [
        ('URBANA', 'Urbana'),
        ('RURAL', 'Rural'),
    ]
    
    COMPLEMENTO_2_CHOICES = [
        ('-', '-'),
        ('CARRERA', 'Carrera'),
        ('DIAGONAL', 'Diagonal'),
        ('CALLE', 'Calle'),
        ('TRANSVERSAL', 'Transversal'),
        ('ENTRE', 'Entre'),
    ]
    
    ACCIDENT_CLASS_CHOICES = [
        ('ATROPELLO', 'Atropello'),
        ('CAIDA', 'Caída'),
        ('COLISIÓN', 'Colisión'),
        ('CHOQUE', 'Choque'),
        ('VOLCAMIENTO', 'Volcamiento'),
        ('OTRO', 'Otro')
    ]
    
    ROAD_TYPE_CHOICES = [
        ('RURAL', 'Rural'),
        ('URBANA', 'Urbana'),
        ('NACIONAL', 'Nacional'),
        ('DEPARTAMENTAL', 'Departamental'),
        ('MUNICIPAL', 'Municipal')
    ]
    
    COLLISION_TYPE_CHOICES = [
        ('VEHICULO', 'Vehículo'),
        ('SEMOVIENTE', 'Semoviente'),
        ('OBJETO FIJO', 'Objeto Fijo')
    ]
    
    FIXED_OBJECT_CHOICES = [
        ('MURO', 'Muro'),
        ('POSTE', 'Poste'),
        ('ARBOL', 'Árbol'),
        ('BARANDA', 'Baranda'),
        ('SEMAFORO', 'Semáforo'),
        ('INMUEBLE', 'Inmueble'),
        ('HIDRANTE', 'Hidrante'),
        ('VALLA', 'Valla'),
        ('SEÑAL', 'Señal'),
        ('TARIMA', 'Tarima'),
        ('CASETA', 'Caseta'),
        ('VEHICULO ESTACIONADO', 'Vehículo Estacionado'),
        ('OTRO', 'Otro')
    ]
    
    REMITIDO_A_CHOICES = [
        ('FISCALIA', 'Fiscalía'),
        ('TRANSITO', 'Tránsito'),
        ('TRANSITO Y FISCALIA', 'Tránsito y Fiscalía'),
        ('OTRO', 'Otro'),
    ]
    
    # Usuario que registra el accidente
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='accidentes_registrados')
    
    # Información básica del accidente
    numero_ipat = models.CharField(max_length=50, unique=True, verbose_name='Número IPAT')
    agente_responsable = models.ForeignKey(Agente, on_delete=models.PROTECT, verbose_name='Agente Responsable')
    fecha_accidente = models.DateField(verbose_name='Fecha del Accidente')
    hora_accidente = models.TimeField(verbose_name='Hora del Accidente')
    dias_establecidos_entrega = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], 
                                                           verbose_name='Días Establecidos para Entrega')
    fecha_real_entrega = models.DateField(blank=False, null=False, verbose_name='Fecha Real de Entrega')
    fecha_registro = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Registro')
    
    # Tipo de accidente
    total_vehiculos_involucrados = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)], 
                                                              verbose_name='Total Vehículos Involucrados')
    con_heridos = models.BooleanField(default=False, verbose_name='Con Heridos')
    con_muertos = models.BooleanField(default=False, verbose_name='Con Muertos')
    con_danos_materiales = models.BooleanField(default=False, verbose_name='Con Daños Materiales')
    
    # Ubicación
    via = models.CharField(max_length=20, choices=VIA_CHOICES, verbose_name='Tipo de Vía')
    numero_via = models.CharField(max_length=20, verbose_name='Número Vía')
    complemento1 = models.CharField(max_length=50, blank=True, null=True, verbose_name='Complemento 1')
    complemento2 = models.CharField(max_length=20, choices=COMPLEMENTO_2_CHOICES, blank=True, null=True, verbose_name='Complemento 2')
    otra_informacion_direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name='Otra información de dirección')
    
    area = models.CharField(max_length=10, choices=AREA_CHOICES, verbose_name='Área')
    zat = models.ForeignKey(ZAT, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='ZAT')
    barrio = models.ForeignKey(Barrio, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Barrio')
    centro_poblado_vereda = models.ForeignKey(CentroPobladoVereda, on_delete=models.SET_NULL, blank=True, null=True, 
                                             verbose_name='Centro Poblado/Vereda')
    
    # Detalles del accidente
    clase_accidente = models.CharField(max_length=20, choices=ACCIDENT_CLASS_CHOICES, verbose_name='Clase de Accidente')
    otro_clase_accidente = models.CharField(max_length=50, blank=True, null=True, verbose_name='Otra Clase de Accidente')
    tipo_via = models.CharField(max_length=20, choices=ROAD_TYPE_CHOICES, verbose_name='Tipo de Vía')
    
    choque_con = models.CharField(max_length=20, choices=COLLISION_TYPE_CHOICES, blank=True, null=True, verbose_name='Choque Con')
    objeto_fijo = models.CharField(max_length=30, choices=FIXED_OBJECT_CHOICES, blank=True, null=True, verbose_name='Objeto Fijo')
    otro_objeto_fijo = models.CharField(max_length=50, blank=True, null=True, verbose_name='Otro Objeto Fijo')
    
    # Hipótesis
    hipotesis_conductor1 = models.ForeignKey(HipotesisConductor, on_delete=models.SET_NULL, blank=True, null=True, 
                                           related_name='accidentes_hipotesis_principal', verbose_name='Hipótesis Principal Conductor')
    hipotesis_conductor2 = models.ForeignKey(HipotesisConductor, on_delete=models.SET_NULL, blank=True, null=True, 
                                           related_name='accidentes_hipotesis_secundaria', verbose_name='Hipótesis Secundaria Conductor')
    hipotesis_conductor3 = models.ForeignKey(HipotesisConductor, on_delete=models.SET_NULL, blank=True, null=True, 
                                           related_name='accidentes_hipotesis_terciaria', verbose_name='Hipótesis Terciaria Conductor')
    hipotesis_conductor4 = models.ForeignKey(HipotesisConductor, on_delete=models.SET_NULL, blank=True, null=True, 
                                           related_name='accidentes_hipotesis_cuaternaria', verbose_name='Hipótesis Cuaternaria Conductor')
    
    hipotesis_vehiculo1 = models.ForeignKey(HipotesisVehiculo, on_delete=models.SET_NULL, blank=True, null=True, 
                                          related_name='accidentes_hipotesis_principal', verbose_name='Hipótesis Principal Vehículo')
    hipotesis_vehiculo2 = models.ForeignKey(HipotesisVehiculo, on_delete=models.SET_NULL, blank=True, null=True, 
                                          related_name='accidentes_hipotesis_secundaria', verbose_name='Hipótesis Secundaria Vehículo')
    
    hipotesis_via1 = models.ForeignKey(HipotesisVia, on_delete=models.SET_NULL, blank=True, null=True, 
                                     related_name='accidentes_hipotesis_principal', verbose_name='Hipótesis Principal Vía')
    hipotesis_via2 = models.ForeignKey(HipotesisVia, on_delete=models.SET_NULL, blank=True, null=True, 
                                     related_name='accidentes_hipotesis_secundaria', verbose_name='Hipótesis Secundaria Vía')
    
    hipotesis_peaton1 = models.ForeignKey(HipotesisPeaton, on_delete=models.SET_NULL, blank=True, null=True, 
                                        related_name='accidentes_hipotesis_principal', verbose_name='Hipótesis Principal Peatón')
    hipotesis_peaton2 = models.ForeignKey(HipotesisPeaton, on_delete=models.SET_NULL, blank=True, null=True, 
                                        related_name='accidentes_hipotesis_secundaria', verbose_name='Hipótesis Secundaria Peatón')
    
    # Información adicional
    remitido_a = models.CharField(max_length=30, choices=REMITIDO_A_CHOICES, blank=True, null=True, verbose_name='Remitido a')
    croquis_pdf = models.FileField(upload_to='croquis/', blank=True, null=True, verbose_name='Croquis (PDF)')
    
    class Meta:
        verbose_name = 'Accidente'
        verbose_name_plural = 'Accidentes'
        ordering = ['-fecha_accidente', '-hora_accidente']
    
    def __str__(self):
        return f"Accidente #{self.numero_ipat} - {self.fecha_accidente}"
    
    def get_direccion_completa(self):
        """Retorna la dirección completa del accidente."""
        direccion = f"{self.via} {self.numero_via}"
        if self.complemento1:
            direccion += f" {self.complemento1}"
        if self.complemento2 and self.complemento2 != '-':
            direccion += f" {self.complemento2}"
        if self.otra_informacion_direccion:
            direccion += f" {self.otra_informacion_direccion}"
        return direccion
    
    def get_ubicacion(self):
        """Retorna la ubicación (barrio o centro poblado) del accidente."""
        if self.area == 'URBANA' and self.barrio:
            return self.barrio.nombre
        elif self.area == 'RURAL' and self.centro_poblado_vereda:
            return self.centro_poblado_vereda.nombre
        return "No especificado"
    
    @property
    def dias_retraso(self):
        """
        Calcula los días de retraso en la entrega del informe.
        Retorna 0 si no hay retraso o si aún no se ha entregado.
        """
        if not self.fecha_real_entrega:
            return 0
        
        fecha_establecida = self.fecha_accidente + timezone.timedelta(days=self.dias_establecidos_entrega)
        
        if self.fecha_real_entrega > fecha_establecida.date():
            return (self.fecha_real_entrega - fecha_establecida.date()).days
        return 0

class VehiculoInvolucrado(models.Model):
    """
    Modelo para almacenar información de los vehículos involucrados en un accidente.
    """
    # Opciones para campos de selección
    SERVICE_TYPE_CHOICES = [
        ('PARTICULAR', 'Particular'),
        ('PUBLICO', 'Público'),
        ('OFICIAL', 'Oficial'),
        ('DIPLOMATICO', 'Diplomático')
    ]
    
    VEHICLE_CLASS_CHOICES = [
        ('AUTOMOVIL', 'Automóvil'),
        ('BUS', 'Bus'),
        ('BUSETA', 'Buseta'),
        ('BICICLETA', 'Bicicleta'),
        ('CAMION', 'Camión'),
        ('CAMIONETA', 'Camioneta'),
        ('CAMPERO', 'Campero'),
        ('TRACTOCAMION', 'Tractocamión - Camión Tractor'),
        ('CUATRIMOTO', 'Cuatrimoto'),
        ('MICROBUS', 'Microbus'),
        ('MOTOCARRO', 'Motocarro'),
        ('MOTOCICLETA', 'Motocicleta'),
        ('MOTOTRICICLO', 'Mototriciclo'),
        ('VOLQUETA', 'Volqueta'),
        ('VEHICULO TRACCION ANIMAL', 'Vehículo de Tracción Animal'),
        ('FUGA DE VEHICULO', 'Fuga de Vehículo'),
        ('VEHICULO FANTASMA', 'Vehículo Fantasma')
    ]
    
    GENDER_CHOICES = [
        ('MASCULINO', 'Masculino'),
        ('FEMENINO', 'Femenino')
    ]
    
    AGE_RANGE_CHOICES = [
        ('PRIMERA INFANCIA', 'Primera Infancia (0-5 años)'),
        ('INFANCIA', 'Infancia (6-11 años)'),
        ('ADOLESCENCIA', 'Adolescencia (12-18 años)'),
        ('JUVENTUD', 'Juventud (14-26 años)'),
        ('ADULTEZ', 'Adultez (27-59 años)'),
        ('PERSONA MAYOR', 'Persona Mayor (60 años o más)')
    ]
    
    INJURED_TYPE_CHOICES = [
        ('PEATON', 'Peatón'),
        ('CONDUCTOR', 'Conductor'),
        ('ACOMPAÑANTE', 'Acompañante'),
        ('PASAJERO', 'Pasajero'),
        ('NO APLICA', 'No Aplica')
    ]
    
    BOOLEAN_CHOICES = [
        ('SI', 'Sí'),
        ('NO', 'No'),
        ('NO APLICA', 'No Aplica')
    ]
    
    INTOXICATION_LEVEL_CHOICES = [
        ('GRADO 1', 'Grado 1'),
        ('GRADO 2', 'Grado 2'),
        ('GRADO 3', 'Grado 3')
    ]
    
    # Relación con el accidente
    accidente = models.ForeignKey(Accidente, on_delete=models.CASCADE, related_name='vehiculos')
    
    # Información del vehículo
    tipo_servicio = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, verbose_name='Tipo de Servicio')
    clase_vehiculo = models.CharField(max_length=30, choices=VEHICLE_CLASS_CHOICES, verbose_name='Clase de Vehículo')
    
    # Información del conductor
    genero_involucrado = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='Género Involucrado')
    rango_edad_involucrado = models.CharField(max_length=20, choices=AGE_RANGE_CHOICES, verbose_name='Rango de Edad Involucrado')
    
    # Información de heridos y fallecidos
    heridos = models.CharField(max_length=20, choices=INJURED_TYPE_CHOICES, verbose_name='Heridos')
    fallecidos = models.CharField(max_length=20, choices=INJURED_TYPE_CHOICES, verbose_name='Fallecidos')
    
    # Información de embriaguez
    embriaguez_conductor = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, verbose_name='Embriaguez del Conductor')
    grado_embriaguez = models.CharField(max_length=10, choices=INTOXICATION_LEVEL_CHOICES, blank=True, null=True, 
                                       verbose_name='Grado de Embriaguez')
    
    # Conteo de víctimas
    numero_heridos = models.PositiveIntegerField(default=0, verbose_name='Número de Heridos')
    numero_fallecidos = models.PositiveIntegerField(default=0, verbose_name='Número de Fallecidos')
    
    # Información de heridos que fallecen después
    herido1_fallece_despues = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, blank=True, null=True, 
                                              verbose_name='Herido 1 Fallece Después')
    herido2_fallece_despues = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, blank=True, null=True, 
                                              verbose_name='Herido 2 Fallece Después')
    herido3_fallece_despues = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, blank=True, null=True, 
                                              verbose_name='Herido 3 Fallece Después')
    herido4_fallece_despues = models.CharField(max_length=10, choices=BOOLEAN_CHOICES, blank=True, null=True, 
                                              verbose_name='Herido 4 Fallece Después')
    
    class Meta:
        verbose_name = 'Vehículo Involucrado'
        verbose_name_plural = 'Vehículos Involucrados'
        ordering = ['accidente', 'id']
    
    def __str__(self):
        return f"Vehículo {self.id} - {self.clase_vehiculo} ({self.accidente.numero_ipat})"

class Fallecido(models.Model):
    """
    Modelo para almacenar información de las personas fallecidas en un accidente.
    """
    vehiculo = models.ForeignKey(VehiculoInvolucrado, on_delete=models.CASCADE, related_name='ocupantes_fallecidos')
    nombre_apellidos = models.CharField(max_length=100, verbose_name='Nombre y Apellidos')
    direccion = models.CharField(max_length=255, verbose_name='Dirección')
    
    class Meta:
        verbose_name = 'Fallecido'
        verbose_name_plural = 'Fallecidos'
    
    def __str__(self):
        return f"{self.nombre_apellidos} - {self.vehiculo.accidente.numero_ipat}"