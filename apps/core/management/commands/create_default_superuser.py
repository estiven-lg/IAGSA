from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crear un superusuario por defecto'

    def handle(self, *args, **options):
        # Verificar si el usuario admin ya existe
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('El usuario admin ya existe'))
            return

        # Crear el superusuario
        User.objects.create_superuser(
            username='admin',
            email='admin@iagsa.com',
            password='12345'
        )
        self.stdout.write(self.style.SUCCESS('Superusuario admin creado exitosamente'))
        self.stdout.write(self.style.SUCCESS('Usuario: admin'))
        self.stdout.write(self.style.SUCCESS('Contraseña: 12345'))
