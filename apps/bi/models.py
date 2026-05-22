from django.db import models
from django.utils import timezone
from apps.security.models import Usuario


class KPIDefinicion(models.Model):
    """Modelo para definiciones de KPIs"""
    id_kpi = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, null=False)
    descripcion = models.TextField(blank=True, null=True)
    formula = models.TextField(blank=True, null=True)
    unidad = models.CharField(max_length=50, blank=True, null=True)
    modulo = models.CharField(max_length=50, blank=True, null=True)
    frecuencia = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'kpi_definiciones'
        verbose_name = 'Definición de KPI'
        verbose_name_plural = 'Definiciones de KPI'

    def __str__(self):
        return self.nombre


class KPIValor(models.Model):
    """Modelo para valores registrados de KPIs"""
    id_valor = models.AutoField(primary_key=True)
    id_kpi = models.ForeignKey(
        KPIDefinicion,
        on_delete=models.CASCADE,
        db_column='id_kpi',
        related_name='valores'
    )
    periodo = models.CharField(max_length=20, blank=True, null=True)
    valor = models.DecimalField(max_digits=14, decimal_places=4, blank=True, null=True)
    meta = models.DecimalField(max_digits=14, decimal_places=4, blank=True, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'kpi_valores'
        verbose_name = 'Valor de KPI'
        verbose_name_plural = 'Valores de KPI'

    def __str__(self):
        return f"{self.id_kpi.nombre} - {self.periodo}"


class Reporte(models.Model):
    """Modelo para reportes del sistema"""
    id_reporte = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    modulo = models.CharField(max_length=50, blank=True, null=True)
    query_base = models.TextField(blank=True, null=True)
    id_creador = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_creador',
        related_name='reportes_creados'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reportes'
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'

    def __str__(self):
        return self.nombre


class AuditoriaOperacion(models.Model):
    """Modelo para auditoría de operaciones CRUD"""
    OPERACION_CHOICES = (
        ('INSERT', 'Inserción'),
        ('UPDATE', 'Actualización'),
        ('DELETE', 'Eliminación'),
    )
    
    id_auditoria = models.AutoField(primary_key=True)
    tabla_afectada = models.CharField(max_length=80, blank=True, null=True)
    operacion = models.CharField(max_length=10, choices=OPERACION_CHOICES, blank=True, null=True)
    id_registro = models.IntegerField(blank=True, null=True)
    datos_anteriores = models.JSONField(blank=True, null=True)
    datos_nuevos = models.JSONField(blank=True, null=True)
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='auditorias_operaciones'
    )
    fecha_hora = models.DateTimeField(default=timezone.now)
    ip_origen = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'auditoria_operaciones'
        verbose_name = 'Auditoría de Operación'
        verbose_name_plural = 'Auditorías de Operaciones'

    def __str__(self):
        return f"{self.operacion} - {self.tabla_afectada}"


class Alerta(models.Model):
    """Modelo para alertas del sistema"""
    id_alerta = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    mensaje = models.TextField(blank=True, null=True)
    modulo = models.CharField(max_length=50, blank=True, null=True)
    id_usuario_destino = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario_destino',
        related_name='alertas'
    )
    leida = models.BooleanField(default=False)
    fecha_generacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'alertas'
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'

    def __str__(self):
        return f"{self.tipo} - {self.modulo}"
