from django.shortcuts import render
from django.http import HttpResponse


# def home(request):
#     return HttpResponse('<h3> Hello world! </h3>')

def home(request):
    return render(request, 'home.html')
