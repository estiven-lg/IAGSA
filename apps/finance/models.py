from django.db import models
from django.utils import timezone
from apps.security.models import Usuario, Departamento
from apps.erp.models import Planta


class CuentaContable(models.Model):
    """Modelo para cuentas contables"""
    TIPO_CHOICES = (
        ('activo', 'Activo'),
        ('pasivo', 'Pasivo'),
        ('capital', 'Capital'),
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    )
    
    id_cuenta = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20, unique=True, null=False)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, null=False)
    id_cuenta_padre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_cuenta_padre',
        related_name='cuentas_hijas'
    )

    class Meta:
        db_table = 'cuentas_contables'
        verbose_name = 'Cuenta Contable'
        verbose_name_plural = 'Cuentas Contables'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class CentroCosto(models.Model):
    """Modelo para centros de costo"""
    id_centro = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    id_departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_departamento',
        related_name='centros_costo'
    )

    class Meta:
        db_table = 'centros_costo'
        verbose_name = 'Centro de Costo'
        verbose_name_plural = 'Centros de Costo'

    def __str__(self):
        return self.nombre


class Transaccion(models.Model):
    """Modelo para transacciones contables"""
    id_transaccion = models.AutoField(primary_key=True)
    fecha = models.DateField(default=timezone.now)
    descripcion = models.TextField(blank=True, null=True)
    id_centro = models.ForeignKey(
        CentroCosto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_centro',
        related_name='transacciones'
    )
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='transacciones'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'transacciones'
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'

    def __str__(self):
        return f"Transacción {self.id_transaccion} - {self.fecha}"


class DetalleTransaccion(models.Model):
    """Modelo para detalles de transacciones contables"""
    id_detalle = models.AutoField(primary_key=True)
    id_transaccion = models.ForeignKey(
        Transaccion,
        on_delete=models.CASCADE,
        db_column='id_transaccion',
        related_name='detalles'
    )
    id_cuenta = models.ForeignKey(
        CuentaContable,
        on_delete=models.PROTECT,
        db_column='id_cuenta',
        related_name='detalles_transaccion'
    )
    debe = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    haber = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        db_table = 'detalle_transaccion'
        verbose_name = 'Detalle de Transacción'
        verbose_name_plural = 'Detalles de Transacción'

    def __str__(self):
        return f"{self.id_transaccion} - {self.id_cuenta.nombre}"


class Presupuesto(models.Model):
    """Modelo para presupuestos"""
    id_presupuesto = models.AutoField(primary_key=True)
    id_centro = models.ForeignKey(
        CentroCosto,
        on_delete=models.CASCADE,
        db_column='id_centro',
        related_name='presupuestos'
    )
    anio = models.IntegerField(null=False)
    mes = models.IntegerField(null=False)
    monto_planificado = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    monto_ejecutado = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        db_table = 'presupuestos'
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'
        constraints = [
                models.CheckConstraint(condition=models.Q(mes__gte=1, mes__lte=12), name='mes_valid')
            ]

    def __str__(self):
        return f"Presupuesto {self.anio}-{self.mes:02d}"


class ActivoFijo(models.Model):
    """Modelo para activos fijos"""
    ESTADO_CHOICES = (
        ('en_uso', 'En Uso'),
        ('depreciado', 'Depreciado'),
        ('dado_baja', 'Dado de Baja'),
        ('mantenimiento', 'Mantenimiento'),
    )
    
    id_activo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    categoria = models.CharField(max_length=80, blank=True, null=True)
    id_planta = models.ForeignKey(
        Planta,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_planta',
        related_name='activos_fijos'
    )
    valor_compra = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    fecha_compra = models.DateField(blank=True, null=True)
    vida_util_anios = models.IntegerField(blank=True, null=True)
    depreciacion_acumulada = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='en_uso')

    class Meta:
        db_table = 'activos_fijos'
        verbose_name = 'Activo Fijo'
        verbose_name_plural = 'Activos Fijos'

    def __str__(self):
        return self.nombre
