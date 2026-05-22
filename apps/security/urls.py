from django.urls import path
from . import views

app_name = 'security'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('usuarios/crear/', views.CrearUsuarioView.as_view(), name='crear_usuario'),
]
