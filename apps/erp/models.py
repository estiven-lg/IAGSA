from django.db import models
from django.utils import timezone
from apps.security.models import Usuario


class Planta(models.Model):
    """Modelo para plantas de producción"""
    id_planta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=False)
    ubicacion = models.CharField(max_length=150, blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    id_gerente = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_gerente',
        related_name='plantas_gerenciadas'
    )

    class Meta:
        db_table = 'plantas'
        verbose_name = 'Planta'
        verbose_name_plural = 'Plantas'

    def __str__(self):
        return self.nombre


class LineaEnsamblaje(models.Model):
    """Modelo para líneas de ensamblaje"""
    id_linea = models.AutoField(primary_key=True)
    id_planta = models.ForeignKey(
        Planta,
        on_delete=models.CASCADE,
        db_column='id_planta',
        related_name='lineas_ensamblaje'
    )
    nombre = models.CharField(max_length=100, null=False)
    estado = models.CharField(max_length=30, default='activa')

    class Meta:
        db_table = 'lineas_ensamblaje'
        verbose_name = 'Línea de Ensamblaje'
        verbose_name_plural = 'Líneas de Ensamblaje'

    def __str__(self):
        return f"{self.nombre} - {self.id_planta.nombre}"


class ModeloVehiculo(models.Model):
    """Modelo para modelos de vehículos"""
    id_modelo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=False)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    motor = models.CharField(max_length=50, blank=True, null=True)
    year_inicio = models.IntegerField(blank=True, null=True)
    year_fin = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'modelos_vehiculo'
        verbose_name = 'Modelo de Vehículo'
        verbose_name_plural = 'Modelos de Vehículos'

    def __str__(self):
        return self.nombre


class OrdenProduccion(models.Model):
    """Modelo para órdenes de producción"""
    id_orden = models.AutoField(primary_key=True)
    id_linea = models.ForeignKey(
        LineaEnsamblaje,
        on_delete=models.CASCADE,
        db_column='id_linea',
        related_name='ordenes_produccion'
    )
    id_modelo = models.ForeignKey(
        ModeloVehiculo,
        on_delete=models.PROTECT,
        db_column='id_modelo',
        related_name='ordenes_produccion'
    )
    cantidad_planificada = models.IntegerField(null=False)
    cantidad_producida = models.IntegerField(default=0)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=30, default='pendiente')
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario',
        related_name='ordenes_produccion'
    )

    class Meta:
        db_table = 'ordenes_produccion'
        verbose_name = 'Orden de Producción'
        verbose_name_plural = 'Órdenes de Producción'

    def __str__(self):
        return f"Orden {self.id_orden} - {self.id_modelo.nombre}"


class Material(models.Model):
    """Modelo para materiales e inventario"""
    id_material = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50, unique=True, null=False)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    unidad_medida = models.CharField(max_length=20, blank=True, null=True)
    origen = models.CharField(max_length=50, blank=True, null=True)
    stock_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_minimo = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'materiales'
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


class Proveedor(models.Model):
    """Modelo para proveedores"""
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, null=False)
    pais = models.CharField(max_length=80, blank=True, null=True)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        db_table = 'proveedores'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return self.nombre


class OrdenCompra(models.Model):
    """Modelo para órdenes de compra"""
    id_compra = models.AutoField(primary_key=True)
    id_proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        db_column='id_proveedor',
        related_name='ordenes_compra'
    )
    fecha_emision = models.DateField(default=timezone.now)
    fecha_entrega = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=30, default='pendiente')
    monto_total = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'ordenes_compra'
        verbose_name = 'Orden de Compra'
        verbose_name_plural = 'Órdenes de Compra'

    def __str__(self):
        return f"Compra {self.id_compra} - {self.id_proveedor.nombre}"


class DetalleCompra(models.Model):
    """Modelo para detalles de órdenes de compra"""
    id_detalle = models.AutoField(primary_key=True)
    id_compra = models.ForeignKey(
        OrdenCompra,
        on_delete=models.CASCADE,
        db_column='id_compra',
        related_name='detalles'
    )
    id_material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        db_column='id_material',
        related_name='detalles_compra'
    )
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, null=False)

    class Meta:
        db_table = 'detalle_compra'
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalles de Compra'

    def __str__(self):
        return f"{self.id_compra} - {self.id_material.codigo}"


class RobotIndustrial(models.Model):
    """Modelo para robots industriales"""
    id_robot = models.AutoField(primary_key=True)
    id_planta = models.ForeignKey(
        Planta,
        on_delete=models.CASCADE,
        db_column='id_planta',
        related_name='robots_industriales'
    )
    fabricante = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    version_software = models.CharField(max_length=50, blank=True, null=True)
    ultima_actualizacion = models.DateField(blank=True, null=True)
    contacto_soporte = models.CharField(max_length=150, blank=True, null=True)
    notas_versiones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'robots_industriales'
        verbose_name = 'Robot Industrial'
        verbose_name_plural = 'Robots Industriales'

    def __str__(self):
        return f"{self.fabricante} {self.modelo}"
