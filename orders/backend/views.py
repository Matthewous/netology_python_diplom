from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import UserRegistrationForm
from .models import Product, Category, ProductInfo, Shop

# Create your views here.
  
def index(request):
    return render(request, 'backend/index.html')

def all_products(request):
    products_list = Product.objects.all()
    return render(request, 'backend/products_list.html', {'products_list': products_list})

def all_categories(request):
    categories_list = Category.objects.all()
    return render(request, 'backend/categories_list.html', {'categories_list': categories_list})

def all_shops(request):
    shops_list = Shop.objects.all()
    return render(request, 'backend/shops_list.html', {'shops_list': shops_list})

# def show_product(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     info = ProductInfo.objects.get(pk=product_id)
#     return render(request, 'backend/product.html', {'product': product,'info':info})
    
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_infos = ProductInfo.objects.filter(product=product)

    context = {
        'product': product,
        'product_infos': product_infos,
    }

    return render(request, 'backend/product_detail.html', context)

def add_to_cart(request, product_info_id):
    product_info = get_object_or_404(ProductInfo, pk=product_info_id)
    # Реализуйте здесь логику добавления товара в корзину
    # ...

    # Перенаправление пользователя на страницу продукта после добавления в корзину
    return redirect('backend/product_detail', product_id=product_info.product.id)

def shop_detail(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    shop_infos = ProductInfo.objects.filter(shop=shop)

    context = {
        'shop': shop,
        'shop_infos': shop_infos,
    }
