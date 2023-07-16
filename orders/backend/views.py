from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegistrationForm
from .models import Product, Category

# Create your views here.
  
def index(request):
    return HttpResponse("Страница домой")

# def registration(request):
#     return HttpResponse("Страница регистрации")

def login(request):
    return HttpResponse("Страница входа")

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'backend/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'backend/register.html', {'user_form': user_form})

def all_products(request):
    products_list = Product.objects.all()
    return render(request, 'backend/products_list.html', {'products_list': products_list})

def all_categories(request):
    categories_list = Category.objects.all()
    return render(request, 'backend/categories_list.html', {'categories_list': categories_list})