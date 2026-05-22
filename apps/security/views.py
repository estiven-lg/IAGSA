from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import HttpRequest
from .models import Usuario, AuditoriaAcceso
from .forms import LoginForm, CrearUsuarioForm


def obtener_ip_cliente(request: HttpRequest) -> str:
    """Obtiene la IP del cliente desde el request"""
    # Intenta obtener IP desde X-Forwarded-For (para proxies)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


class LoginView(FormView):
    """Vista para autenticar usuarios en el sistema"""
    template_name = 'security/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('core:index')

    def dispatch(self, request, *args, **kwargs):
        """Redirige a dashboard si el usuario ya está autenticado"""
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Procesa login exitoso"""
        # Obtiene el usuario autenticado desde el formulario
        user = form.user
        
        # Registra la IP del cliente
        ip_origen = obtener_ip_cliente(self.request)
        
        # Actualiza último acceso
        user.ultimo_acceso = __import__('django.utils.timezone', fromlist=['now']).now()
        user.save()

        # Registra auditoría de acceso exitoso
        AuditoriaAcceso.objects.create(
            id_usuario=user,
            accion='LOGIN',
            ip_origen=ip_origen,
            resultado='exitoso'
        )

        # Autentica al usuario en la sesión
        login(self.request, user)

        # Mensaje de éxito
        messages.success(
            self.request,
            f'¡Bienvenido {user.get_full_name() or user.username}!'
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        """Procesa login fallido"""
        ip_origen = obtener_ip_cliente(self.request)
        
        # Obtiene el username del formulario para registrarlo
        username = form.cleaned_data.get('username', 'desconocido')
        
        # Intenta obtener el usuario para registrar auditoría
        try:
            user = Usuario.objects.get(username=username)
            AuditoriaAcceso.objects.create(
                id_usuario=user,
                accion='LOGIN',
                ip_origen=ip_origen,
                resultado='fallido'
            )
        except Usuario.DoesNotExist:
            # Si el usuario no existe, no registra en auditoría
            pass

        # Mensaje de error
        messages.error(
            self.request,
            'Usuario o contraseña incorrectos. Intente nuevamente.'
        )

        return super().form_invalid(form)


class LogoutView(View):
    """Vista para cerrar sesión del usuario"""
    
    def get(self, request):
        """Maneja el cierre de sesión"""
        if request.user.is_authenticated:
            # Registra auditoría de logout
            ip_origen = obtener_ip_cliente(request)
            AuditoriaAcceso.objects.create(
                id_usuario=request.user,
                accion='LOGOUT',
                ip_origen=ip_origen,
                resultado='exitoso'
            )

            # Mensaje de despedida
            messages.success(request, 'Ha cerrado sesión correctamente.')

            # Cierra la sesión
            logout(request)

        return redirect('security:login')


@method_decorator(login_required(login_url='security:login'), name='dispatch')
@method_decorator(
    user_passes_test(lambda u: u.is_superuser, login_url='core:index'),
    name='dispatch'
)
class CrearUsuarioView(FormView):
    """Vista para crear nuevos usuarios (solo superusuarios)"""
    template_name = 'security/crear_usuario.html'
    form_class = CrearUsuarioForm
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        """Procesa la creación del usuario"""
        usuario = form.save()
        
        messages.success(
            self.request,
            f'Usuario "{usuario.username}" creado exitosamente.'
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        """Procesa errores en la creación del usuario"""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')

        return super().form_invalid(form)

