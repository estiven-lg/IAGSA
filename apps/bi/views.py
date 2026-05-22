from django.shortcuts import render

def bi_home(request):
    return render(request, 'bi/index.html')
