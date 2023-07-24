from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import UserRegistrationForm
from .models import Order, Product, Category, ProductInfo, Shop
from django.core.mail import send_mail
from django.db.models import Q, Min
from django.http import HttpResponseRedirect

# Create your views here.
  
def index(request):
    return render(request, 'backend/index.html')

# def all_products(request):
#     products_list = Product.objects.all()
#     return render(request, 'backend/products_list.html', {'products_list': products_list})

# def products_list(request):
#     products = Product.objects.all()

#     name = request.GET.get('name')
#     model = request.GET.get('model')
#     price = request.GET.get('price')

#     if name:
#         products = products.filter(name__icontains=name)    
#     if model:
#         products = products.filter(product_infos__model__icontains=model)
#     if price:
#         products = products.filter(product_infos__price=price)

#     context = {
#         'products': products
#     }
#     return render(request, 'backend/products_list.html', context)

def products_list(request):
    products = Product.objects.all()

    # Получаем значения фильтров из GET-параметров
    name = request.GET.get('name')
    category = request.GET.get('category')
    model = request.GET.get('model')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Применяем фильтры
    if name:
        products = products.filter(name__icontains=name)
    if category:
        products = products.filter(category__name=category)
    if model:
        products = products.filter(product_infos__model__icontains=model)
    if min_price:
        products = products.filter(product_infos__price__gte=min_price)
    if max_price:
        products = products.filter(product_infos__price__lte=max_price)

    products = products.annotate(min_price=Min('product_infos__price'))

    context = {
        'products': products
    }
    return render(request, 'backend/products_list.html', context)

def all_categories(request):
    categories_list = Category.objects.all()
    return render(request, 'backend/categories_list.html', {'categories_list': categories_list})

def all_shops(request):
    shops_list = Shop.objects.all()
    return render(request, 'backend/shops_list.html', {'shops_list': shops_list})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_infos = product.product_infos.all()

    context = {
        'product': product,
        'product_infos': product_infos
    }
    return render(request, 'backend/product_detail.html', context)

# def add_to_cart(request, product_info_id):
#     if request.method == 'POST':
#         product_info = ProductInfo.objects.get(id=product_info_id)
#         quantity = request.POST.get('quantity')
        
#         order = Order.objects.get_or_create(
#             user=request.user, 
#             product_name=product_info.product,
#             quantity=quantity, 
#             price=product_info.price, 
#             shop=product_info.shop,
#             status='editing',
#         )

#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_to_cart(request, product_info_id):
    if request.method == 'POST':
        product_info = get_object_or_404(ProductInfo, id=product_info_id)
        quantity = request.POST.get('quantity')
        
        try:
            order = Order.objects.get(user=request.user, status='editing')
            order.add_product(product_info, quantity)
        except Order.DoesNotExist:
            order = Order.objects.create(user=request.user, status='editing')
            order.add_product(product_info, quantity)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'backend/orders.html', {'orders': orders})