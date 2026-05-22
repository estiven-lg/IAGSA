from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Subgerencia(models.Model):
    """Modelo para subgerencias de la organización"""
    id_subgerencia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'subgerencias'
        verbose_name = 'Subgerencia'
        verbose_name_plural = 'Subgerencias'

    def __str__(self):
        return self.nombre


class Departamento(models.Model):
    """Modelo para departamentos de la organización"""
    id_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=False)
    id_subgerencia = models.ForeignKey(
        Subgerencia,
        on_delete=models.CASCADE,
        db_column='id_subgerencia',
        related_name='departamentos'
    )

    class Meta:
        db_table = 'departamentos'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.nombre


class Rol(models.Model):
    """Modelo para roles del sistema"""
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50, null=False)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre_rol


class Permiso(models.Model):
    """Modelo para permisos del sistema"""
    id_permiso = models.AutoField(primary_key=True)
    modulo = models.CharField(max_length=50, null=False)
    accion = models.CharField(max_length=50, null=False)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'permisos'
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'
        unique_together = ('modulo', 'accion')

    def __str__(self):
        return f"{self.modulo} - {self.accion}"


class RolPermiso(models.Model):
    """Modelo para relación muchos a muchos entre roles y permisos"""
    id_rol = models.ForeignKey(
        Rol,
        on_delete=models.CASCADE,
        db_column='id_rol'
    )
    id_permiso = models.ForeignKey(
        Permiso,
        on_delete=models.CASCADE,
        db_column='id_permiso'
    )

    class Meta:
        db_table = 'rol_permiso'
        unique_together = ('id_rol', 'id_permiso')
        verbose_name = 'Rol-Permiso'
        verbose_name_plural = 'Rol-Permisos'

    def __str__(self):
        return f"{self.id_rol.nombre_rol} - {self.id_permiso.modulo}"


class Usuario(AbstractUser):
    """Modelo de usuario personalizado que extiende AbstractUser"""
    id_usuario = models.AutoField(primary_key=True)
    id_rol = models.ForeignKey(
        Rol,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_rol',
        related_name='usuarios'
    )
    id_departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_departamento',
        related_name='usuarios'
    )
    ultimo_acceso = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.get_full_name() or self.username


class AuditoriaAcceso(models.Model):
    """Modelo para registrar auditoría de accesos al sistema"""
    id_log = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        related_name='auditorias_acceso'
    )
    accion = models.CharField(max_length=100, blank=True, null=True)
    ip_origen = models.CharField(max_length=50, blank=True, null=True)
    fecha_hora = models.DateTimeField(default=timezone.now)
    resultado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'auditoria_accesos'
        verbose_name = 'Auditoría de Acceso'
        verbose_name_plural = 'Auditorías de Acceso'

    def __str__(self):
        return f"{self.id_usuario.nombre_completo} - {self.fecha_hora}"
