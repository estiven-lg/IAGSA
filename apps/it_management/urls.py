from django.urls import path
from . import views

app_name = 'it_management'

urlpatterns = [
    path('', views.it_management_home, name='home'),
]
