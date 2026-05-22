from django.contrib import admin
from .models import (
    SistemaInformatico,
    Servidor,
    Backup,
    IncidenteTI,
    RiesgoTI,
    PlanContinuidad,
    ProcedimientoRecuperacion,
)


@admin.register(SistemaInformatico)
class SistemaInformaticoAdmin(admin.ModelAdmin):
    list_display = ('id_sistema', 'nombre', 'tipo', 'plataforma', 'criticidad', 'estado', 'id_responsable')
    search_fields = ('nombre', 'plataforma')
    list_filter = ('criticidad', 'estado', 'tipo')
    readonly_fields = ('id_sistema',)
    ordering = ('nombre',)


@admin.register(Servidor)
class ServidorAdmin(admin.ModelAdmin):
    list_display = ('id_servidor', 'nombre', 'ip', 'sistema_operativo', 'ubicacion', 'estado')
    search_fields = ('nombre', 'ip')
    list_filter = ('estado', 'sistema_operativo')
    readonly_fields = ('id_servidor',)
    ordering = ('nombre',)


@admin.register(Backup)
class BackupAdmin(admin.ModelAdmin):
    list_display = ('id_backup', 'id_sistema', 'id_servidor', 'tipo', 'fecha_backup', 'verificado', 'resultado')
    search_fields = ('id_sistema__nombre',)
    list_filter = ('tipo', 'verificado', 'fecha_backup')
    readonly_fields = ('id_backup',)
    ordering = ('-fecha_backup',)


@admin.register(IncidenteTI)
class IncidenteTIAdmin(admin.ModelAdmin):
    list_display = ('id_incidente', 'id_sistema', 'tipo', 'impacto', 'estado', 'fecha_inicio')
    search_fields = ('tipo', 'descripcion')
    list_filter = ('estado', 'impacto', 'fecha_inicio')
    readonly_fields = ('id_incidente',)
    ordering = ('-fecha_inicio',)


@admin.register(RiesgoTI)
class RiesgoTIAdmin(admin.ModelAdmin):
    list_display = ('id_riesgo', 'categoria', 'probabilidad', 'impacto', 'nivel_riesgo', 'estado')
    search_fields = ('descripcion', 'categoria')
    list_filter = ('probabilidad', 'impacto', 'estado')
    readonly_fields = ('id_riesgo',)
    ordering = ('nivel_riesgo',)


class ProcedimientoRecuperacionInline(admin.TabularInline):
    model = ProcedimientoRecuperacion
    extra = 1


@admin.register(PlanContinuidad)
class PlanContinuidadAdmin(admin.ModelAdmin):
    list_display = ('id_plan', 'nombre', 'version', 'fecha_elaboracion', 'fecha_ultima_prueba', 'estado')
    search_fields = ('nombre',)
    list_filter = ('estado', 'fecha_elaboracion')
    inlines = [ProcedimientoRecuperacionInline]
    readonly_fields = ('id_plan',)
    ordering = ('nombre',)


@admin.register(ProcedimientoRecuperacion)
class ProcedimientoRecuperacionAdmin(admin.ModelAdmin):
    list_display = ('id_procedimiento', 'nombre', 'id_plan', 'id_sistema', 'rto_horas', 'rpo_horas')
    search_fields = ('nombre', 'id_sistema__nombre')
    list_filter = ('id_plan',)
    readonly_fields = ('id_procedimiento',)
    ordering = ('nombre',)
