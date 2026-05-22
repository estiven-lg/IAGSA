from django.db import models
from django.utils import timezone
from apps.security.models import Usuario


class SistemaInformatico(models.Model):
    """Modelo para sistemas informáticos"""
    CRITICIDAD_CHOICES = (
        ('critico', 'Crítico'),
        ('alto', 'Alto'),
        ('medio', 'Medio'),
        ('bajo', 'Bajo'),
    )
    
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('mantenimiento', 'Mantenimiento'),
        ('descontinuado', 'Descontinuado'),
    )
    
    id_sistema = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, null=False)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    plataforma = models.CharField(max_length=80, blank=True, null=True)
    version = models.CharField(max_length=30, blank=True, null=True)
    ubicacion_servidor = models.CharField(max_length=100, blank=True, null=True)
    id_responsable = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_responsable',
        related_name='sistemas_responsable'
    )
    tiene_codigo_fuente = models.BooleanField(default=False)
    tiene_backup = models.BooleanField(default=False)
    criticidad = models.CharField(max_length=20, choices=CRITICIDAD_CHOICES, blank=True, null=True)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='activo')

    class Meta:
        db_table = 'sistemas_informaticos'
        verbose_name = 'Sistema Informático'
        verbose_name_plural = 'Sistemas Informáticos'

    def __str__(self):
        return self.nombre


class Servidor(models.Model):
    """Modelo para servidores"""
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('mantenimiento', 'Mantenimiento'),
        ('fuera_servicio', 'Fuera de Servicio'),
    )
    
    id_servidor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    ip = models.CharField(max_length=50, blank=True, null=True)
    sistema_operativo = models.CharField(max_length=80, blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    nivel_datacenter = models.CharField(max_length=10, blank=True, null=True)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='activo')

    class Meta:
        db_table = 'servidores'
        verbose_name = 'Servidor'
        verbose_name_plural = 'Servidores'

    def __str__(self):
        return self.nombre


class Backup(models.Model):
    """Modelo para backups"""
    TIPO_CHOICES = (
        ('completo', 'Completo'),
        ('incremental', 'Incremental'),
        ('diferencial', 'Diferencial'),
    )
    
    id_backup = models.AutoField(primary_key=True)
    id_sistema = models.ForeignKey(
        SistemaInformatico,
        on_delete=models.CASCADE,
        db_column='id_sistema',
        related_name='backups'
    )
    id_servidor = models.ForeignKey(
        Servidor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_servidor',
        related_name='backups'
    )
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, blank=True, null=True)
    fecha_backup = models.DateTimeField(blank=True, null=True)
    ubicacion_fisica = models.CharField(max_length=200, blank=True, null=True)
    verificado = models.BooleanField(default=False)
    resultado = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'backups'
        verbose_name = 'Backup'
        verbose_name_plural = 'Backups'

    def __str__(self):
        return f"Backup {self.id_sistema.nombre} - {self.fecha_backup}"


class IncidenteTI(models.Model):
    """Modelo para incidentes de TI"""
    IMPACTO_CHOICES = (
        ('critico', 'Crítico'),
        ('alto', 'Alto'),
        ('medio', 'Medio'),
        ('bajo', 'Bajo'),
    )
    
    ESTADO_CHOICES = (
        ('abierto', 'Abierto'),
        ('en_progreso', 'En Progreso'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado'),
    )
    
    id_incidente = models.AutoField(primary_key=True)
    id_sistema = models.ForeignKey(
        SistemaInformatico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_sistema',
        related_name='incidentes'
    )
    tipo = models.CharField(max_length=80, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_resolucion = models.DateTimeField(blank=True, null=True)
    impacto = models.CharField(max_length=30, choices=IMPACTO_CHOICES, blank=True, null=True)
    causa_raiz = models.TextField(blank=True, null=True)
    id_usuario_reporte = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario_reporte',
        related_name='incidentes_reportados'
    )
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='abierto')

    class Meta:
        db_table = 'incidentes_ti'
        verbose_name = 'Incidente TI'
        verbose_name_plural = 'Incidentes TI'

    def __str__(self):
        return f"Incidente {self.id_incidente} - {self.tipo}"


class RiesgoTI(models.Model):
    """Modelo para riesgos de TI"""
    PROBABILIDAD_CHOICES = (
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    )
    
    IMPACTO_CHOICES = (
        ('alto', 'Alto'),
        ('medio', 'Medio'),
        ('bajo', 'Bajo'),
    )
    
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('mitigado', 'Mitigado'),
        ('resuelto', 'Resuelto'),
        ('inactivo', 'Inactivo'),
    )
    
    id_riesgo = models.AutoField(primary_key=True)
    descripcion = models.TextField(null=False)
    categoria = models.CharField(max_length=80, blank=True, null=True)
    probabilidad = models.CharField(max_length=20, choices=PROBABILIDAD_CHOICES, blank=True, null=True)
    impacto = models.CharField(max_length=20, choices=IMPACTO_CHOICES, blank=True, null=True)
    nivel_riesgo = models.CharField(max_length=20, blank=True, null=True)
    plan_mitigacion = models.TextField(blank=True, null=True)
    id_responsable = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_responsable',
        related_name='riesgos_responsable'
    )
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='activo')

    class Meta:
        db_table = 'riesgos_ti'
        verbose_name = 'Riesgo TI'
        verbose_name_plural = 'Riesgos TI'

    def __str__(self):
        return f"Riesgo {self.id_riesgo} - {self.categoria}"


class PlanContinuidad(models.Model):
    """Modelo para planes de continuidad de negocio"""
    ESTADO_CHOICES = (
        ('vigente', 'Vigente'),
        ('en_revision', 'En Revisión'),
        ('obsoleto', 'Obsoleto'),
        ('archivado', 'Archivado'),
    )
    
    id_plan = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    version = models.CharField(max_length=10, blank=True, null=True)
    fecha_elaboracion = models.DateField(blank=True, null=True)
    fecha_ultima_prueba = models.DateField(blank=True, null=True)
    id_responsable = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_responsable',
        related_name='planes_continuidad'
    )
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='vigente')

    class Meta:
        db_table = 'plan_continuidad'
        verbose_name = 'Plan de Continuidad'
        verbose_name_plural = 'Planes de Continuidad'

    def __str__(self):
        return self.nombre


class ProcedimientoRecuperacion(models.Model):
    """Modelo para procedimientos de recuperación"""
    id_procedimiento = models.AutoField(primary_key=True)
    id_plan = models.ForeignKey(
        PlanContinuidad,
        on_delete=models.CASCADE,
        db_column='id_plan',
        related_name='procedimientos'
    )
    id_sistema = models.ForeignKey(
        SistemaInformatico,
        on_delete=models.CASCADE,
        db_column='id_sistema',
        related_name='procedimientos_recuperacion'
    )
    nombre = models.CharField(max_length=150, blank=True, null=True)
    pasos = models.TextField(blank=True, null=True)
    rto_horas = models.IntegerField(blank=True, null=True)
    rpo_horas = models.IntegerField(blank=True, null=True)
    responsable = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'procedimientos_recuperacion'
        verbose_name = 'Procedimiento de Recuperación'
        verbose_name_plural = 'Procedimientos de Recuperación'

    def __str__(self):
        return f"{self.nombre} - {self.id_plan.nombre}"
