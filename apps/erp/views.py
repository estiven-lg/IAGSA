from django.shortcuts import render

def erp_home(request):
    return render(request, 'erp/index.html')
