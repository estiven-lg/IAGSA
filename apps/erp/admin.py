from django.contrib import admin
from .models import (
    Planta,
    LineaEnsamblaje,
    ModeloVehiculo,
    OrdenProduccion,
    Material,
    Proveedor,
    OrdenCompra,
    DetalleCompra,
    RobotIndustrial,
)


@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = ('id_planta', 'nombre', 'ubicacion', 'tipo', 'id_gerente')
    search_fields = ('nombre', 'ubicacion')
    list_filter = ('tipo',)
    ordering = ('nombre',)


@admin.register(LineaEnsamblaje)
class LineaEnsamblajeAdmin(admin.ModelAdmin):
    list_display = ('id_linea', 'nombre', 'id_planta', 'estado')
    search_fields = ('nombre',)
    list_filter = ('estado', 'id_planta')
    ordering = ('nombre',)


@admin.register(ModeloVehiculo)
class ModeloVehiculoAdmin(admin.ModelAdmin):
    list_display = ('id_modelo', 'nombre', 'tipo', 'motor', 'year_inicio', 'year_fin')
    search_fields = ('nombre', 'tipo')
    list_filter = ('tipo', 'year_inicio')
    ordering = ('nombre',)


@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(admin.ModelAdmin):
    list_display = ('id_orden', 'id_modelo', 'id_linea', 'cantidad_planificada', 'cantidad_producida', 'estado', 'fecha_inicio')
    search_fields = ('id_modelo__nombre',)
    list_filter = ('estado', 'fecha_inicio', 'id_linea')
    readonly_fields = ('id_orden',)
    ordering = ('-fecha_inicio',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id_material', 'codigo', 'descripcion', 'unidad_medida', 'stock_actual', 'stock_minimo')
    search_fields = ('codigo', 'descripcion')
    list_filter = ('unidad_medida', 'origen')
    readonly_fields = ('id_material',)
    ordering = ('codigo',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('id_proveedor', 'nombre', 'pais', 'contacto', 'email')
    search_fields = ('nombre', 'contacto', 'email')
    list_filter = ('pais',)
    ordering = ('nombre',)


class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 1


@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ('id_compra', 'id_proveedor', 'fecha_emision', 'fecha_entrega', 'estado', 'monto_total')
    search_fields = ('id_proveedor__nombre',)
    list_filter = ('estado', 'fecha_emision')
    inlines = [DetalleCompraInline]
    readonly_fields = ('id_compra',)
    ordering = ('-fecha_emision',)


@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ('id_detalle', 'id_compra', 'id_material', 'cantidad', 'precio_unitario')
    search_fields = ('id_material__codigo',)
    list_filter = ('id_compra',)
    readonly_fields = ('id_detalle',)


@admin.register(RobotIndustrial)
class RobotIndustrialAdmin(admin.ModelAdmin):
    list_display = ('id_robot', 'fabricante', 'modelo', 'version_software', 'id_planta', 'ultima_actualizacion')
    search_fields = ('fabricante', 'modelo')
    list_filter = ('id_planta', 'ultima_actualizacion')
    readonly_fields = ('id_robot',)
    ordering = ('fabricante', 'modelo')
