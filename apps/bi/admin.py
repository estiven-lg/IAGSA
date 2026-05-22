from django.contrib import admin
from .models import (
    KPIDefinicion,
    KPIValor,
    Reporte,
    AuditoriaOperacion,
    Alerta,
)


@admin.register(KPIDefinicion)
class KPIDefinicionAdmin(admin.ModelAdmin):
    list_display = ('id_kpi', 'nombre', 'modulo', 'unidad', 'frecuencia')
    search_fields = ('nombre', 'modulo')
    list_filter = ('modulo', 'frecuencia')
    readonly_fields = ('id_kpi',)
    ordering = ('nombre',)


@admin.register(KPIValor)
class KPIValorAdmin(admin.ModelAdmin):
    list_display = ('id_valor', 'id_kpi', 'periodo', 'valor', 'meta', 'fecha_registro')
    search_fields = ('id_kpi__nombre', 'periodo')
    list_filter = ('periodo', 'fecha_registro')
    readonly_fields = ('id_valor', 'fecha_registro')
    ordering = ('-fecha_registro',)


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('id_reporte', 'nombre', 'modulo', 'id_creador', 'created_at')
    search_fields = ('nombre', 'modulo')
    list_filter = ('modulo', 'created_at')
    readonly_fields = ('id_reporte', 'created_at')
    ordering = ('-created_at',)


@admin.register(AuditoriaOperacion)
class AuditoriaOperacionAdmin(admin.ModelAdmin):
    list_display = ('id_auditoria', 'tabla_afectada', 'operacion', 'id_usuario', 'fecha_hora', 'ip_origen')
    search_fields = ('tabla_afectada', 'id_usuario__username')
    list_filter = ('operacion', 'tabla_afectada', 'fecha_hora')
    readonly_fields = ('id_auditoria', 'fecha_hora', 'datos_anteriores', 'datos_nuevos')
    ordering = ('-fecha_hora',)


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('id_alerta', 'tipo', 'modulo', 'id_usuario_destino', 'leida', 'fecha_generacion')
    search_fields = ('tipo', 'modulo')
    list_filter = ('leida', 'fecha_generacion', 'tipo')
    readonly_fields = ('id_alerta', 'fecha_generacion')
    ordering = ('-fecha_generacion',)
