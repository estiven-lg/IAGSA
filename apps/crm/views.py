from django.shortcuts import render

def crm_home(request):
    return render(request, 'crm/index.html')
