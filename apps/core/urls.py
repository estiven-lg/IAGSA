from django.urls import path
from .views import base

app_name = 'core'

urlpatterns = [
    path('', base, name='index'),
]