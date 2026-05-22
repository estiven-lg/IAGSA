from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='security:login')
def base(request):
    """Vista base protegida"""
    return render(request, 'base/base.html')


@login_required(login_url='security:login')
def index(request):
    """Vista de índice/dashboard protegida"""
    return render(request, 'core/index.html')