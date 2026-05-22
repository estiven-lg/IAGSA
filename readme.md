# IAGSA - Integrated Administrative and Management System

Un sistema empresarial integral desarrollado con Django para la gestión completa de operaciones administrativas, recursos humanos, finanzas, CRM y más.

## Descripción del Proyecto

IAGSA es una plataforma empresarial completa que integra múltiples módulos para administrar diversos aspectos de una organización. Proporciona herramientas centralizadas para gestionar recursos, procesos y datos críticos del negocio.

## Características Principales

- **Módulo BI** - Inteligencia de Negocios y análisis de datos
- **Módulo Core** - Funcionalidades principales y gestión general
- **CRM** - Gestión de relaciones con clientes
- **ERP** - Planificación de recursos empresariales
- **Finance** - Gestión financiera y contabilidad
- **HR** - Gestión de recursos humanos
- **IT Management** - Gestión de infraestructura TI
- **Security** - Autenticación y seguridad del sistema

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- SQLite3 (incluido en Python)
- Navegador web moderno

## Instalación

### 1. Clonar o descargar el proyecto

```bash
# Navega al directorio del proyecto
cd IAGSA
```

### 2. Crear un entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Configuración

### 1. Variables de entorno

Edita `config/settings.py` para configurar:

- `SECRET_KEY`: Clave secreta de Django (cambiar en producción)
- `DEBUG`: Modo de depuración (False en producción)
- `ALLOWED_HOSTS`: Hosts permitidos
- `DATABASES`: Configuración de base de datos

### 2. Migraciones de base de datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Crear superusuario (administrador)

Opción A: Crear superusuario por defecto (admin / 12345)

```bash
python manage.py create_default_superuser
```

Opción B: Crear superusuario personalizado

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear una cuenta de administrador.

## Uso

### Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

### Acceder al administrador

Navega a: `http://127.0.0.1:8000/admin/`

Inicia sesión con las credenciales del superusuario creado.

### Crear aplicaciones estáticas

```bash
python manage.py collectstatic
```

## Estructura del Proyecto

```
IAGSA/
├── apps/                      # Aplicaciones principales
│   ├── bi/                    # Módulo de Inteligencia de Negocios
│   ├── core/                  # Funcionalidades principales
│   ├── crm/                   # Gestión de clientes
│   ├── erp/                   # Planificación de recursos
│   ├── finance/               # Finanzas y contabilidad
│   ├── hr/                    # Recursos humanos
│   ├── it_management/         # Gestión de IT
│   └── security/              # Autenticación y seguridad
├── config/                    # Configuración del proyecto
│   ├── settings.py            # Configuración principal
│   ├── urls.py                # Rutas principales
│   ├── asgi.py                # Configuración ASGI
│   └── wsgi.py                # Configuración WSGI
├── templates/                 # Plantillas HTML
│   └── base/                  # Plantillas base
├── static/                    # Archivos estáticos (CSS, JS, imágenes)
├── media/                     # Archivos multimedia subidos
├── manage.py                  # Script de gestión de Django
├── requirements.txt           # Dependencias del proyecto
└── db.sqlite3                 # Base de datos (SQLite)
```

## Aplicaciones por Módulo

### Core
- Funcionalidades base del sistema
- Modelos principales compartidos

### Security
- Autenticación de usuarios
- Gestión de permisos y roles
- Sistema de login

### ERP
- Gestión de inventario
- Órdenes de compra/venta
- Planificación de producción

### CRM
- Gestión de contactos
- Seguimiento de oportunidades
- Historial de interacciones

### HR
- Gestión de empleados
- Nómina y salarios
- Evaluaciones de desempeño

### Finance
- Contabilidad general
- Gestión de pagos
- Reportes financieros

### IT Management
- Gestión de activos TI
- Tickets de soporte
- Administración de infraestructura

### BI
- Análisis de datos
- Reportes personalizados
- Dashboards

## Comandos Útiles

```bash
# Ejecutar tests
python manage.py test

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Borrar usuario
python manage.py shell

# Limpiar archivos estáticos
python manage.py collectstatic --clear
```

## Tecnologías Utilizadas

- **Django** 6.0.5 - Framework web
- **Python** 3.x - Lenguaje principal
- **SQLite** - Base de datos
- **django-extensions** - Extensiones útiles para desarrollo

## Consideraciones de Seguridad

**En Producción:**

1. Cambiar `DEBUG` a `False`
2. Generar nueva `SECRET_KEY`
3. Configurar `ALLOWED_HOSTS`
4. Usar una base de datos robusta (PostgreSQL, MySQL)
5. Implementar HTTPS
6. Configurar CORS si es necesario
7. Usar variables de entorno para datos sensibles

## Notas de Desarrollo

- Las migraciones se encuentran en cada aplicación bajo la carpeta `migrations/`
- Los templates se organizan por aplicación en la carpeta `templates/`
- Los modelos de datos se definen en `models.py` de cada aplicación
- Las vistas se encuentran en `views.py` de cada aplicación

## Contribuciones

Para contribuir al proyecto:

1. Crea una rama para tu feature
2. Realiza los cambios necesarios
3. Prueba tu código
4. Envía un pull request

## Documentación

Para más información sobre Django:
- [Documentación Oficial de Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)

## Licencia

Este proyecto es de código propietario. Todos los derechos reservados.

## Autor

Desarrollado como solución empresarial integral.

---

**Última actualización:** Mayo 2026
