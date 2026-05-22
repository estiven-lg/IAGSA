from django.urls import path
from . import views

app_name = 'bi'

urlpatterns = [
    path('', views.bi_home, name='home'),
]
