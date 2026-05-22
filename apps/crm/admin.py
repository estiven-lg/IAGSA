from django.contrib import admin
from .models import (
    Cliente,
    Distribuidor,
    Cotizacion,
    DetalleCotizacion,
    Venta,
    InteraccionCliente,
)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id_cliente', 'nombre', 'tipo', 'nit', 'email', 'telefono', 'pais', 'created_at')
    search_fields = ('nombre', 'nit', 'email')
    list_filter = ('tipo', 'pais', 'created_at')
    readonly_fields = ('id_cliente', 'created_at')
    ordering = ('-created_at',)


@admin.register(Distribuidor)
class DistribuidorAdmin(admin.ModelAdmin):
    list_display = ('id_distribuidor', 'nombre', 'region', 'pais', 'contacto', 'email')
    search_fields = ('nombre', 'contacto', 'email')
    list_filter = ('region', 'pais')
    readonly_fields = ('id_distribuidor',)
    ordering = ('nombre',)


class DetalleCotizacionInline(admin.TabularInline):
    model = DetalleCotizacion
    extra = 1


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ('id_cotizacion', 'id_cliente', 'fecha', 'vigencia_hasta', 'estado', 'total', 'id_usuario')
    search_fields = ('id_cliente__nombre',)
    list_filter = ('estado', 'fecha', 'vigencia_hasta')
    inlines = [DetalleCotizacionInline]
    readonly_fields = ('id_cotizacion',)
    ordering = ('-fecha',)


@admin.register(DetalleCotizacion)
class DetalleCotizacionAdmin(admin.ModelAdmin):
    list_display = ('id_detalle', 'id_cotizacion', 'id_modelo', 'cantidad', 'precio_unitario', 'descuento')
    search_fields = ('id_modelo__nombre',)
    list_filter = ('id_cotizacion',)
    readonly_fields = ('id_detalle',)


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id_venta', 'id_cliente', 'fecha_venta', 'estado', 'total', 'id_usuario')
    search_fields = ('id_cliente__nombre',)
    list_filter = ('estado', 'fecha_venta')
    readonly_fields = ('id_venta',)
    ordering = ('-fecha_venta',)


@admin.register(InteraccionCliente)
class InteraccionClienteAdmin(admin.ModelAdmin):
    list_display = ('id_interaccion', 'id_cliente', 'tipo', 'fecha', 'id_usuario')
    search_fields = ('id_cliente__nombre', 'descripcion')
    list_filter = ('tipo', 'fecha')
    readonly_fields = ('id_interaccion',)
    ordering = ('-fecha',)
