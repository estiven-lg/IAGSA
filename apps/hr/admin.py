from django.contrib import admin
from .models import (
    Empleado,
    Puesto,
    HistorialPuesto,
    Capacitacion,
    EmpleadoCapacitacion,
    Planilla,
)


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id_empleado', 'nombre_completo', 'dpi', 'email_corporativo', 'tipo', 'estado', 'fecha_ingreso')
    search_fields = ('nombre_completo', 'dpi', 'email_corporativo')
    list_filter = ('tipo', 'estado', 'fecha_ingreso', 'id_departamento', 'id_planta')
    readonly_fields = ('id_empleado',)
    ordering = ('-fecha_ingreso',)


@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
    list_display = ('id_puesto', 'nombre', 'nivel', 'salario_base')
    search_fields = ('nombre',)
    list_filter = ('nivel',)
    readonly_fields = ('id_puesto',)
    ordering = ('nombre',)


@admin.register(HistorialPuesto)
class HistorialPuestoAdmin(admin.ModelAdmin):
    list_display = ('id_historial', 'id_empleado', 'id_puesto', 'fecha_inicio', 'fecha_fin', 'salario')
    search_fields = ('id_empleado__nombre_completo',)
    list_filter = ('fecha_inicio', 'id_puesto')
    readonly_fields = ('id_historial',)
    ordering = ('-fecha_inicio',)


@admin.register(Capacitacion)
class CapacitacionAdmin(admin.ModelAdmin):
    list_display = ('id_capacitacion', 'nombre', 'proveedor', 'fecha', 'duracion_horas')
    search_fields = ('nombre', 'proveedor')
    list_filter = ('fecha', 'proveedor')
    readonly_fields = ('id_capacitacion',)
    ordering = ('-fecha',)


@admin.register(EmpleadoCapacitacion)
class EmpleadoCapacitacionAdmin(admin.ModelAdmin):
    list_display = ('id_empleado', 'id_capacitacion', 'completado', 'fecha_completado')
    search_fields = ('id_empleado__nombre_completo', 'id_capacitacion__nombre')
    list_filter = ('completado', 'fecha_completado')
    ordering = ('-fecha_completado',)


@admin.register(Planilla)
class PlanillaAdmin(admin.ModelAdmin):
    list_display = ('id_planilla', 'id_empleado', 'periodo', 'salario_base', 'bonificaciones', 'deducciones', 'total_neto', 'fecha_pago')
    search_fields = ('id_empleado__nombre_completo', 'periodo')
    list_filter = ('periodo', 'fecha_pago')
    readonly_fields = ('id_planilla',)
    ordering = ('-fecha_pago',)
