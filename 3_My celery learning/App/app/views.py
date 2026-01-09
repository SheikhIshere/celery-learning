from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    print("Result")
    return HttpResponse('<h1>Hello nigga</h1>')    
