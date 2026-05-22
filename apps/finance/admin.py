from django.contrib import admin
from .models import (
    CuentaContable,
    CentroCosto,
    Transaccion,
    DetalleTransaccion,
    Presupuesto,
    ActivoFijo,
)


@admin.register(CuentaContable)
class CuentaContableAdmin(admin.ModelAdmin):
    list_display = ('id_cuenta', 'codigo', 'nombre', 'tipo', 'id_cuenta_padre')
    search_fields = ('codigo', 'nombre')
    list_filter = ('tipo',)
    readonly_fields = ('id_cuenta',)
    ordering = ('codigo',)


@admin.register(CentroCosto)
class CentroCostoAdmin(admin.ModelAdmin):
    list_display = ('id_centro', 'nombre', 'id_departamento')
    search_fields = ('nombre',)
    list_filter = ('id_departamento',)
    readonly_fields = ('id_centro',)
    ordering = ('nombre',)


class DetalleTransaccionInline(admin.TabularInline):
    model = DetalleTransaccion
    extra = 1


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('id_transaccion', 'fecha', 'id_centro', 'id_usuario', 'created_at')
    search_fields = ('descripcion', 'id_usuario__username')
    list_filter = ('fecha', 'id_centro')
    inlines = [DetalleTransaccionInline]
    readonly_fields = ('id_transaccion', 'created_at')
    ordering = ('-fecha',)


@admin.register(DetalleTransaccion)
class DetalleTransaccionAdmin(admin.ModelAdmin):
    list_display = ('id_detalle', 'id_transaccion', 'id_cuenta', 'debe', 'haber')
    search_fields = ('id_cuenta__codigo', 'id_cuenta__nombre')
    list_filter = ('id_transaccion',)
    readonly_fields = ('id_detalle',)


@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ('id_presupuesto', 'id_centro', 'anio', 'mes', 'monto_planificado', 'monto_ejecutado')
    search_fields = ('id_centro__nombre',)
    list_filter = ('anio', 'mes', 'id_centro')
    readonly_fields = ('id_presupuesto',)
    ordering = ('-anio', '-mes')


@admin.register(ActivoFijo)
class ActivoFijoAdmin(admin.ModelAdmin):
    list_display = ('id_activo', 'nombre', 'categoria', 'id_planta', 'valor_compra', 'fecha_compra', 'estado')
    search_fields = ('nombre', 'categoria')
    list_filter = ('estado', 'fecha_compra', 'id_planta')
    readonly_fields = ('id_activo',)
    ordering = ('nombre',)
