from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
  
def index(request):
    return HttpResponse("Страница регистрации")

def registration(request):
    return HttpResponse("Страница регистрации")

def login(request):
    return HttpResponse("Страница входа")