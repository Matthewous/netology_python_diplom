from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegistrationForm
from .models import Product, Category

# Create your views here.
  
def index(request):
    return render(request, 'backend/index.html')

def all_products(request):
    products_list = Product.objects.all()
    return render(request, 'backend/products_list.html', {'products_list': products_list})

def all_categories(request):
    categories_list = Category.objects.all()
    return render(request, 'backend/categories_list.html', {'categories_list': categories_list})