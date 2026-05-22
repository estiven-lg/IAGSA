"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin

# Importar security para activar el admin personalizado
import apps.security.admin  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('security/', include('apps.security.urls')),
    path('', include('apps.core.urls')),
    path('erp/', include('apps.erp.urls')),
    path('crm/', include('apps.crm.urls')),
    path('hr/', include('apps.hr.urls')),
    path('finance/', include('apps.finance.urls')),
    path('it_management/', include('apps.it_management.urls')),
    path('bi/', include('apps.bi.urls')),
]
