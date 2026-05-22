from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import (
    Subgerencia,
    Departamento,
    Rol,
    Permiso,
    RolPermiso,
    Usuario,
    AuditoriaAcceso,
)


# Personalizar el AdminSite default
class AdminSiteProtegido(admin.AdminSite):
    """AdminSite personalizado que solo permite acceso a superusuarios"""
    site_header = 'Administración IAGSA'
    site_title = 'Admin IAGSA'
    index_title = 'Panel de Administración'

    def has_permission(self, request):
        """Verifica que el usuario sea superusuario"""
        return request.user.is_active and request.user.is_superuser


# Reemplazar el admin.site default con nuestro AdminSite personalizado
admin.site.__class__ = AdminSiteProtegido
admin.site.site_header = 'Administración IAGSA'
admin.site.site_title = 'Admin IAGSA'
admin.site.index_title = 'Panel de Administración'
admin.site.has_permission = lambda self, request: request.user.is_active and request.user.is_superuser


@admin.register(Subgerencia)
class SubgerenciaAdmin(admin.ModelAdmin):
    list_display = ('id_subgerencia', 'nombre')
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('id_departamento', 'nombre', 'id_subgerencia')
    search_fields = ('nombre',)
    list_filter = ('id_subgerencia',)
    ordering = ('nombre',)


@admin.register(Permiso)
class PermisoAdmin(admin.ModelAdmin):
    list_display = ('id_permiso', 'modulo', 'accion')
    search_fields = ('modulo', 'accion')
    list_filter = ('modulo',)
    ordering = ('modulo', 'accion')


class RolPermisoInline(admin.TabularInline):
    model = RolPermiso
    extra = 1


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id_rol', 'nombre_rol')
    search_fields = ('nombre_rol',)
    inlines = [RolPermisoInline]
    ordering = ('nombre_rol',)


class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('id_rol', 'id_departamento', 'ultimo_acceso')
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'id_rol', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'id_rol', 'id_departamento', 'date_joined')
    ordering = ('username',)


admin.site.register(Usuario, UsuarioAdmin)


@admin.register(AuditoriaAcceso)
class AuditoriaAccesoAdmin(admin.ModelAdmin):
    list_display = ('id_log', 'id_usuario', 'accion', 'ip_origen', 'fecha_hora', 'resultado')
    search_fields = ('id_usuario__username', 'ip_origen')
    list_filter = ('fecha_hora', 'resultado')
    readonly_fields = ('id_log', 'fecha_hora')
    ordering = ('-fecha_hora',)
