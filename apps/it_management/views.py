from django.shortcuts import render

def it_management_home(request):
    return render(request, 'it_management/index.html')
