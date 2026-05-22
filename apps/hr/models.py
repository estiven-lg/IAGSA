from django.db import models
from django.utils import timezone
from apps.security.models import Departamento
from apps.erp.models import Planta


class Empleado(models.Model):
    """Modelo para empleados"""
    GENERO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    )
    
    TIPO_CHOICES = (
        ('operario', 'Operario'),
        ('administrativo', 'Administrativo'),
        ('mercadeo', 'Mercadeo'),
        ('ejecutivo', 'Ejecutivo'),
    )
    
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('licencia', 'Licencia'),
        ('jubilado', 'Jubilado'),
    )
    
    id_empleado = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=150, null=False)
    dpi = models.CharField(max_length=20, unique=True, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, blank=True, null=True)
    email_corporativo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    id_departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_departamento',
        related_name='empleados'
    )
    id_planta = models.ForeignKey(
        Planta,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_planta',
        related_name='empleados'
    )
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, null=False)
    fecha_ingreso = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')

    class Meta:
        db_table = 'empleados'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return self.nombre_completo


class Puesto(models.Model):
    """Modelo para puestos de trabajo"""
    id_puesto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=False)
    nivel = models.CharField(max_length=50, blank=True, null=True)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'puestos'
        verbose_name = 'Puesto'
        verbose_name_plural = 'Puestos'

    def __str__(self):
        return self.nombre


class HistorialPuesto(models.Model):
    """Modelo para historial de puestos de empleados"""
    id_historial = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        db_column='id_empleado',
        related_name='historial_puestos'
    )
    id_puesto = models.ForeignKey(
        Puesto,
        on_delete=models.PROTECT,
        db_column='id_puesto',
        related_name='historial_empleados'
    )
    fecha_inicio = models.DateField(null=False)
    fecha_fin = models.DateField(blank=True, null=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'historial_puestos'
        verbose_name = 'Historial de Puesto'
        verbose_name_plural = 'Historial de Puestos'

    def __str__(self):
        return f"{self.id_empleado.nombre_completo} - {self.id_puesto.nombre}"


class Capacitacion(models.Model):
    """Modelo para capacitaciones"""
    id_capacitacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    proveedor = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    duracion_horas = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'capacitaciones'
        verbose_name = 'Capacitación'
        verbose_name_plural = 'Capacitaciones'

    def __str__(self):
        return self.nombre


class EmpleadoCapacitacion(models.Model):
    """Modelo para relación entre empleados y capacitaciones"""
    id_empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        db_column='id_empleado'
    )
    id_capacitacion = models.ForeignKey(
        Capacitacion,
        on_delete=models.CASCADE,
        db_column='id_capacitacion'
    )
    completado = models.BooleanField(default=False)
    fecha_completado = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'empleado_capacitacion'
        unique_together = ('id_empleado', 'id_capacitacion')
        verbose_name = 'Empleado-Capacitación'
        verbose_name_plural = 'Empleado-Capacitaciones'

    def __str__(self):
        return f"{self.id_empleado.nombre_completo} - {self.id_capacitacion.nombre}"


class Planilla(models.Model):
    """Modelo para planillas de pago"""
    id_planilla = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        db_column='id_empleado',
        related_name='planillas'
    )
    periodo = models.CharField(max_length=20, null=False)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    bonificaciones = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deducciones = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_neto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_pago = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'planilla'
        verbose_name = 'Planilla'
        verbose_name_plural = 'Planillas'

    def __str__(self):
        return f"Planilla {self.periodo} - {self.id_empleado.nombre_completo}"
