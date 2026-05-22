from django.db import models
from django.utils import timezone
from apps.security.models import Usuario
from apps.erp.models import ModeloVehiculo


class Cliente(models.Model):
    """Modelo para clientes"""
    TIPO_CHOICES = (
        ('persona', 'Persona Natural'),
        ('empresa', 'Empresa'),
    )
    
    id_cliente = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, null=False)
    nombre = models.CharField(max_length=150, null=False)
    nit = models.CharField(max_length=30, unique=True, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    pais = models.CharField(max_length=80, blank=True, null=True)
    ciudad = models.CharField(max_length=80, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nombre


class Distribuidor(models.Model):
    """Modelo para distribuidores"""
    id_distribuidor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, null=False)
    region = models.CharField(max_length=80, blank=True, null=True)
    pais = models.CharField(max_length=80, blank=True, null=True)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        db_table = 'distribuidores'
        verbose_name = 'Distribuidor'
        verbose_name_plural = 'Distribuidores'

    def __str__(self):
        return self.nombre


class Cotizacion(models.Model):
    """Modelo para cotizaciones"""
    ESTADO_CHOICES = (
        ('borrador', 'Borrador'),
        ('enviada', 'Enviada'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
        ('expirada', 'Expirada'),
    )
    
    id_cotizacion = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        db_column='id_cliente',
        related_name='cotizaciones'
    )
    id_distribuidor = models.ForeignKey(
        Distribuidor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_distribuidor',
        related_name='cotizaciones'
    )
    fecha = models.DateField(default=timezone.now)
    vigencia_hasta = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='borrador')
    total = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='cotizaciones'
    )

    class Meta:
        db_table = 'cotizaciones'
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'

    def __str__(self):
        return f"Cotización {self.id_cotizacion} - {self.id_cliente.nombre}"


class DetalleCotizacion(models.Model):
    """Modelo para detalles de cotizaciones"""
    id_detalle = models.AutoField(primary_key=True)
    id_cotizacion = models.ForeignKey(
        Cotizacion,
        on_delete=models.CASCADE,
        db_column='id_cotizacion',
        related_name='detalles'
    )
    id_modelo = models.ForeignKey(
        ModeloVehiculo,
        on_delete=models.PROTECT,
        db_column='id_modelo',
        related_name='detalles_cotizacion'
    )
    cantidad = models.IntegerField(null=False)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        db_table = 'detalle_cotizacion'
        verbose_name = 'Detalle de Cotización'
        verbose_name_plural = 'Detalles de Cotización'

    def __str__(self):
        return f"{self.id_cotizacion} - {self.id_modelo.nombre}"


class Venta(models.Model):
    """Modelo para ventas"""
    ESTADO_CHOICES = (
        ('activa', 'Activa'),
        ('entregada', 'Entregada'),
        ('cancelada', 'Cancelada'),
        ('anulada', 'Anulada'),
    )
    
    id_venta = models.AutoField(primary_key=True)
    id_cotizacion = models.ForeignKey(
        Cotizacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_cotizacion',
        related_name='ventas'
    )
    id_cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        db_column='id_cliente',
        related_name='ventas'
    )
    fecha_venta = models.DateField(default=timezone.now)
    total = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='activa')
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='ventas'
    )

    class Meta:
        db_table = 'ventas'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def __str__(self):
        return f"Venta {self.id_venta} - {self.id_cliente.nombre}"


class InteraccionCliente(models.Model):
    """Modelo para interacciones con clientes"""
    TIPO_CHOICES = (
        ('llamada', 'Llamada'),
        ('email', 'Email'),
        ('reunion', 'Reunión'),
        ('seguimiento', 'Seguimiento'),
        ('otros', 'Otros'),
    )
    
    id_interaccion = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        db_column='id_cliente',
        related_name='interacciones'
    )
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(default=timezone.now)
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='interacciones_cliente'
    )

    class Meta:
        db_table = 'interacciones_cliente'
        verbose_name = 'Interacción de Cliente'
        verbose_name_plural = 'Interacciones de Clientes'

    def __str__(self):
        return f"{self.id_cliente.nombre} - {self.tipo} ({self.fecha})"
