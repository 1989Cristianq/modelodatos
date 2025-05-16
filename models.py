from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# Definimos los tipos de roles
class Role(models.TextChoices):
    ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
    SUPERVISOR = "SUPERVISOR", "Supervisor"
    AGENTE = "AGENTE", "Agente"

class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=15,
        choices=Role.choices,
        default=Role.AGENTE,  # El rol por defecto será "Agente"
    )

    def is_administrador(self):
        return self.role == Role.ADMINISTRADOR

    def is_supervisor(self):
        return self.role == Role.SUPERVISOR

    def is_agente(self):
        return self.role == Role.AGENTE
    
    # modelo principal del formulario
class Agente(models.Model):
    """Modelo para los agentes responsables de atender accidentes"""
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class ZAT(models.Model):
    """Zonas de Atención de Tránsito"""
    numero = models.PositiveSmallIntegerField(unique=True)
    nombre = models.CharField(max_length=10)  # ZAT1, ZAT2, etc.

    def __str__(self):
        return self.nombre


class Barrio(models.Model):
    """Barrios de la ciudad"""
    nombre = models.CharField(max_length=100)
    zat = models.ForeignKey(ZAT, on_delete=models.PROTECT, related_name='barrios')

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class CentroPobladoVereda(models.Model):
    """Centros poblados o veredas para áreas rurales"""
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class HipotesisDelConductor(models.Model):
    """Hipótesis relacionadas con el conductor"""
    codigo = models.CharField(max_length=5, unique=True)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


class HipotesisDelVehiculo(models.Model):
    """Hipótesis relacionadas con el vehículo"""
    codigo = models.CharField(max_length=5, unique=True)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


class HipotesisDeLaVia(models.Model):
    """Hipótesis relacionadas con la vía"""
    codigo = models.CharField(max_length=5, unique=True)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


class HipotesisDelPeaton(models.Model):
    """Hipótesis relacionadas con el peatón"""
    codigo = models.CharField(max_length=5, unique=True)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


class Accidente(models.Model):
    """Modelo principal para registro de accidentes de tránsito"""
    MESES_CHOICES = [
        ('ENERO', 'ENERO'),
        ('FEBRERO', 'FEBRERO'),
        ('MARZO', 'MARZO'),
        ('ABRIL', 'ABRIL'),
        ('MAYO', 'MAYO'),
        ('JUNIO', 'JUNIO'),
        ('JULIO', 'JULIO'),
        ('AGOSTO', 'AGOSTO'),
        ('SEPTIEMBRE', 'SEPTIEMBRE'),
        ('OCTUBRE', 'OCTUBRE'),
        ('NOVIEMBRE', 'NOVIEMBRE'),
        ('DICIEMBRE', 'DICIEMBRE'),
    ]
    
    VIA_CHOICES = [
        ('CALLE', 'CALLE'),
        ('CARRERA', 'CARRERA'),
        ('DIAGONAL', 'DIAGONAL'),
        ('CASA', 'CASA'),
        ('LOTE', 'LOTE'),
        ('MANZANA', 'MANZANA'),
        ('AVENIDA', 'AVENIDA'),
        ('VEREDA', 'VEREDA'),
        ('KILOMETRO', 'KILOMETRO'),
        ('TRANSVERSAL', 'TRANSVERSAL'),
        ('VÍA', 'VÍA'),
    ]
    
    COMPLEMENTO2_CHOICES = [
        ('-', '-'),
        ('CARRERA', 'CARRERA'),
        ('DIAGONAL', 'DIAGONAL'),
        ('CALLE', 'CALLE'),
        ('TRANSVERSAL', 'TRANSVERSAL'),
        ('ENTRE', 'ENTRE'),
    ]
    
    AREA_CHOICES = [
        ('URBANA', 'URBANA'),
        ('RURAL', 'RURAL'),
    ]
    
    CLASE_ACCIDENTE_CHOICES = [
        ('ATROPELLO', 'ATROPELLO'),
        ('CAIDA', 'CAIDA'),
        ('COLISIÓN', 'COLISIÓN'),
        ('CHOQUE', 'CHOQUE'),
        ('VOLCAMIENTO', 'VOLCAMIENTO'),
        ('OTRO', 'OTRO'),
    ]
    
    TIPO_VIA_CHOICES = [
        ('RURAL', 'RURAL'),
        ('URBANA', 'URBANA'),
        ('NACIONAL', 'NACIONAL'),
        ('DEPARTAMENTAL', 'DEPARTAMENTAL'),
        ('MUNICIPAL', 'MUNICIPAL'),
    ]
    
    CHOQUE_CON_CHOICES = [
        ('VEHICULO', 'VEHICULO'),
        ('SEMOVIENTE', 'SEMOVIENTE'),
        ('OBJETO FIJO', 'OBJETO FIJO'),
    ]
    
    OBJETO_FIJO_CHOICES = [
        ('MURO', 'MURO'),
        ('POSTE', 'POSTE'),
        ('ARBOL', 'ARBOL'),
        ('BARANDA', 'BARANDA'),
        ('SEMAFORO', 'SEMAFORO'),
        ('INMUEBLE', 'INMUEBLE'),
        ('HIDRANTE', 'HIDRANTE'),
        ('VALLA', 'VALLA'),
        ('SEÑAL', 'SEÑAL'),
        ('TARIMA', 'TARIMA'),
        ('CASETA', 'CASETA'),
        ('VEHICULO ESTACIONADO', 'VEHICULO ESTACIONADO'),
        ('OTRO', 'OTRO'),
    ]
    
    REMITIDO_A_CHOICES = [
        ('FISCALIA LOCAL', 'FISCALIA LOCAL'),
        ('FISCALIA SECCIONAL', 'FISCALIA SECCIONAL'),
        ('INFANCIA Y ADOLESCENCIA', 'INFANCIA Y ADOLESCENCIA'),
    ]

    # Campos básicos del accidente
    numero_accidente = models.AutoField(primary_key=True)
    numero_ipat = models.CharField(max_length=15)
    agente_responsable = models.ForeignKey(Agente, on_delete=models.PROTECT)
    fecha_accidente = models.DateField()
    mes_accidente = models.CharField(max_length=20, choices=MESES_CHOICES)
    dias_establecidos_entrega = models.PositiveSmallIntegerField(default=1)
    fecha_establecida_entrega = models.DateField()
    fecha_real_entrega = models.DateField(null=True, blank=True)
    dias_reales_entrega = models.IntegerField(null=True, blank=True)
    entrega_dentro_terminos = models.BooleanField(null=True, blank=True)
    hora_accidente = models.TimeField()
    
    # Dirección del accidente
    via = models.CharField(max_length=20, choices=VIA_CHOICES)
    numero_via = models.CharField(max_length=3)
    complemento1 = models.CharField(max_length=100, blank=True)
    complemento2 = models.CharField(max_length=20, choices=COMPLEMENTO2_CHOICES, blank=True)
    otra_informacion_direccion = models.CharField(max_length=200, blank=True)
    direccion_concatenada = models.CharField(max_length=300, blank=True)
    area = models.CharField(max_length=10, choices=AREA_CHOICES)
    zat = models.ForeignKey(ZAT, on_delete=models.PROTECT, null=True, blank=True)
    barrio = models.ForeignKey(Barrio, on_delete=models.PROTECT, null=True, blank=True)
    centro_poblado_vereda = models.ForeignKey(CentroPobladoVereda, on_delete=models.PROTECT, null=True, blank=True)
    
    # Información del accidente
    total_vehiculos_involucrados = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    con_heridos = models.BooleanField(default=False)
    con_muertos = models.BooleanField(default=False)
    con_danos_materiales = models.BooleanField(default=False)
    clase_accidente = models.CharField(max_length=20, choices=CLASE_ACCIDENTE_CHOICES)
    otro_clase_accidente = models.CharField(max_length=100, blank=True)
    tipo_via = models.CharField(max_length=20, choices=TIPO_VIA_CHOICES)
    choque_con = models.CharField(max_length=20, choices=CHOQUE_CON_CHOICES, null=True, blank=True)
    objeto_fijo = models.CharField(max_length=30, choices=OBJETO_FIJO_CHOICES, null=True, blank=True)
    otro_objeto_fijo = models.CharField(max_length=100, blank=True)
    
    # Totales
    total_heridos = models.PositiveSmallIntegerField(default=0)
    total_fallecidos = models.PositiveSmallIntegerField(default=0)
    
    # Hipótesis del accidente
    hipotesis_conductor1 = models.ForeignKey(HipotesisDelConductor, on_delete=models.PROTECT, related_name='accidentes_hipotesis1', null=True, blank=True)
    hipotesis_conductor2 = models.ForeignKey(HipotesisDelConductor, on_delete=models.PROTECT, related_name='accidentes_hipotesis2', null=True, blank=True)
    hipotesis_conductor3 = models.ForeignKey(HipotesisDelConductor, on_delete=models.PROTECT, related_name='accidentes_hipotesis3', null=True, blank=True)
    hipotesis_conductor4 = models.ForeignKey(HipotesisDelConductor, on_delete=models.PROTECT, related_name='accidentes_hipotesis4', null=True, blank=True)
    
    hipotesis_vehiculo1 = models.ForeignKey(HipotesisDelVehiculo, on_delete=models.PROTECT, related_name='accidentes_hipotesis1', null=True, blank=True)
    hipotesis_vehiculo2 = models.ForeignKey(HipotesisDelVehiculo, on_delete=models.PROTECT, related_name='accidentes_hipotesis2', null=True, blank=True)
    
    hipotesis_via1 = models.ForeignKey(HipotesisDeLaVia, on_delete=models.PROTECT, related_name='accidentes_hipotesis1', null=True, blank=True)
    hipotesis_via2 = models.ForeignKey(HipotesisDeLaVia, on_delete=models.PROTECT, related_name='accidentes_hipotesis2', null=True, blank=True)
    
    hipotesis_peaton1 = models.ForeignKey(HipotesisDelPeaton, on_delete=models.PROTECT, related_name='accidentes_hipotesis1', null=True, blank=True)
    hipotesis_peaton2 = models.ForeignKey(HipotesisDelPeaton, on_delete=models.PROTECT, related_name='accidentes_hipotesis2', null=True, blank=True)
    
    # Remisión y adjuntos
    remitido_a = models.CharField(max_length=30, choices=REMITIDO_A_CHOICES, null=True, blank=True)
    croquis_pdf = models.FileField(upload_to='croquis/', null=True, blank=True)
    
    # Metadatos
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Asignar automáticamente el mes basado en la fecha del accidente
        if self.fecha_accidente:
            self.mes_accidente = self.fecha_accidente.strftime('%B').upper()
        
        # Calcular fecha establecida de entrega (fecha accidente + 1 día)
        if self.fecha_accidente and not self.fecha_establecida_entrega:
            self.fecha_establecida_entrega = self.fecha_accidente + timezone.timedelta(days=self.dias_establecidos_entrega)
        
        # Calcular días reales de entrega y verificar si está dentro de términos
        if self.fecha_real_entrega and self.fecha_establecida_entrega:
            delta = self.fecha_real_entrega - self.fecha_establecida_entrega
            self.dias_reales_entrega = delta.days
            self.entrega_dentro_terminos = delta.days <= self.dias_establecidos_entrega
        
        # Concatenar dirección
        direccion_parts = [self.via, self.numero_via]
        if self.complemento1:
            direccion_parts.append(self.complemento1)
        if self.complemento2:
            direccion_parts.append(self.complemento2)
        if self.otra_informacion_direccion:
            direccion_parts.append(self.otra_informacion_direccion)
        self.direccion_concatenada = " ".join(direccion_parts)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Accidente #{self.numero_accidente} - {self.fecha_accidente}"


class Vehiculo(models.Model):
    """Modelo para los vehículos involucrados en un accidente"""
    TIPO_SERVICIO_CHOICES = [
        ('PARTICULAR', 'PARTICULAR'),
        ('PUBLICO', 'PUBLICO'),
        ('OFICIAL', 'OFICIAL'),
        ('DIPLOMATICO', 'DIPLOMATICO'),
    ]
    
    CLASE_VEHICULO_CHOICES = [
        ('AUTOMOVIL', 'AUTOMOVIL'),
        ('BUS', 'BUS'),
        ('BUSETA', 'BUSETA'),
        ('BICICLETA', 'BICICLETA'),
        ('CAMION', 'CAMION'),
        ('CAMIONETA', 'CAMIONETA'),
        ('CAMPERO', 'CAMPERO'),
        ('TRACTOCAMION-CAMION TRACTOR', 'TRACTOCAMION-CAMION TRACTOR'),
        ('CUATRIMOTO', 'CUATRIMOTO'),
        ('MICROBUS', 'MICROBUS'),
        ('MOTOCARRO', 'MOTOCARRO'),
        ('MOTOCILETA', 'MOTOCILETA'),
        ('MOTOTRICICLO', 'MOTOTRICICLO'),
        ('VOLQUETA', 'VOLQUETA'),
        ('VEHICULO DE TRACCION ANIMAL', 'VEHICULO DE TRACCION ANIMAL'),
        ('FUGA DE VEHICULO', 'FUGA DE VEHICULO'),
        ('VEHICULO FANTASMA', 'VEHICULO FANTASMA'),
    ]
    
    GENERO_CHOICES = [
        ('MASCULINO', 'MASCULINO'),
        ('FEMENINO', 'FEMENINO'),
    ]
    
    RANGO_EDAD_CHOICES = [
        ('PRIMERRA INFANCIA 0-5 AÑOS', 'PRIMERRA INFANCIA 0-5 AÑOS'),
        ('INFANCIA DE 6-11 AÑOS', 'INFANCIA DE 6-11 AÑOS'),
        ('ADOLESCENCIA 12-18 AÑOS', 'ADOLESCENCIA 12-18 AÑOS'),
        ('JUVENTUD 14-26 AÑOS', 'JUVENTUD 14-26 AÑOS'),
        ('ADULTEZ 27-59 AÑOS', 'ADULTEZ 27-59 AÑOS'),
        ('PERSONA MAYOR A 60 AÑOS O MAS', 'PERSONA MAYOR A 60 AÑOS O MAS'),
    ]
    
    HERIDOS_CHOICES = [
        ('PEATÓN', 'PEATÓN'),
        ('CONDUCTOR', 'CONDUCTOR'),
        ('ACOMPAÑANTE', 'ACOMPAÑANTE'),
        ('PASAJERO', 'PASAJERO'),
        ('NO APLICA', 'NO APLICA'),
    ]
    
    FALLECIDOS_CHOICES = [
        ('PEATON', 'PEATON'),
        ('CONDUCTOR', 'CONDUCTOR'),
        ('ACOMPAÑANTE', 'ACOMPAÑANTE'),
        ('PASAJEROS', 'PASAJEROS'),
        ('NO APLICA', 'NO APLICA'),
    ]
    
    EMBRIAGUEZ_CHOICES = [
        ('SI', 'SI'),
        ('NO', 'NO'),
        ('NO APLICA', 'NO APLICA'),
    ]
    
    GRADO_EMBRIAGUEZ_CHOICES = [
        ('GRADO 1', 'GRADO 1'),
        ('GRADO 2', 'GRADO 2'),
        ('GRADO 3', 'GRADO 3'),
    ]
    
    FALLECE_DESPUES_CHOICES = [
        ('SI', 'SI'),
        ('NO', 'NO'),
        ('NO APLICA', 'NO APLICA'),
    ]

    accidente = models.ForeignKey(Accidente, on_delete=models.CASCADE, related_name='vehiculos')
    numero_vehiculo = models.PositiveSmallIntegerField()  # 1, 2, 3, 4...
    
    tipo_servicio = models.CharField(max_length=20, choices=TIPO_SERVICIO_CHOICES)
    clase_vehiculo = models.CharField(max_length=50, choices=CLASE_VEHICULO_CHOICES)
    genero_involucrado = models.CharField(max_length=20, choices=GENERO_CHOICES)
    rango_edad_involucrado = models.CharField(max_length=50, choices=RANGO_EDAD_CHOICES)
    
    heridos = models.CharField(max_length=20, choices=HERIDOS_CHOICES)
    numero_fallecidos = models.CharField(max_length=20, choices=FALLECIDOS_CHOICES)
    
    embriaguez_conductor = models.CharField(max_length=10, choices=EMBRIAGUEZ_CHOICES)
    grado_embriaguez = models.CharField(max_length=10, choices=GRADO_EMBRIAGUEZ_CHOICES, null=True, blank=True)
    
    numero_heridos = models.PositiveSmallIntegerField(default=0)
    numero_fallecidos = models.PositiveSmallIntegerField(default=0)
    
    herido1_fallece_despues = models.CharField(max_length=10, choices=FALLECE_DESPUES_CHOICES, default='NO')
    herido2_fallece_despues = models.CharField(max_length=10, choices=FALLECE_DESPUES_CHOICES, default='NO APLICA')
    herido3_fallece_despues = models.CharField(max_length=10, choices=FALLECE_DESPUES_CHOICES, default='NO APLICA')

    class Meta:
        unique_together = ['accidente', 'numero_vehiculo']
        ordering = ['accidente', 'numero_vehiculo']

    def __str__(self):
        return f"Vehículo {self.numero_vehiculo} - Accidente #{self.accidente.numero_accidente}"

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        # Actualizar los totales del accidente
        self._actualizar_totales_accidente()
        return result

    def delete(self, *args, **kwargs):
        accidente = self.accidente
        result = super().delete(*args, **kwargs)
        # Actualizar los totales del accidente
        self._actualizar_totales_accidente()
        return result

    def _actualizar_totales_accidente(self):
        """Actualiza los totales de heridos y fallecidos en el accidente"""
        accidente = self.accidente
        vehiculos = accidente.vehiculos.all()
        
        total_heridos = sum(v.numero_heridos for v in vehiculos)
        total_fallecidos = sum(v.numero_fallecidos for v in vehiculos)
        
        accidente.total_heridos = total_heridos
        accidente.total_fallecidos = total_fallecidos
        accidente.con_heridos = total_heridos > 0
        accidente.con_muertos = total_fallecidos > 0
        
        accidente.save(update_fields=['total_heridos', 'total_fallecidos', 'con_heridos', 'con_muertos'])


class Fallecido(models.Model):
    """Modelo para los fallecidos en un accidente"""
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='fallecidos')
    nombre_apellidos = models.CharField(max_length=200)
    direccion = models.CharField(max_length=300)
    numero_fallecido = models.PositiveSmallIntegerField()  # 1, 2, 3...

    class Meta:
        unique_together = ['vehiculo', 'numero_fallecido']
        ordering = ['vehiculo', 'numero_fallecido']

    def __str__(self):
        return f"Fallecido {self.nombre_apellidos} - Vehículo {self.vehiculo.numero_vehiculo}"
