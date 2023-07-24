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

def products_list(request):
    products = Product.objects.all()

    # Получаем значения фильтров из GET-параметров
    name = request.GET.get('name')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Применяем фильтры
    if name:
        products = products.filter(name__icontains=name)
    if category:
        products = products.filter(category__name=category)
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
    user = request.user
    orders = Order.objects.filter(user=user)
    context = {
        'orders': orders
    }
    return render(request, 'backend/orders.html', context)

def cart(request):
    user = request.user
    order = Order.objects.filter(user=user, status='editing').first()
    
    if order:
        order_items = order.orderitem_set.all()
        total_price = sum(item.quantity * item.price for item in order_items)
    else:
        order_items = {}
        total_price = 0
    
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address')
        delivery_date = request.POST.get('delivery_date')

        order.delivery_address = delivery_address
        order.delivery_date = delivery_date
        order.status = 'confirmed'
        order.save()

        return redirect('orders')

    context = {
        'order': order,
        'order_items': order_items,
        'total_price': total_price
    }
    return render(request, 'backend/cart.html', context)

def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    order_items = order.orderitem_set.all()
    total_price = sum(item.quantity * item.price for item in order_items)
    context = {
        'order': order,
        'order_items': order_items,
        'total_price': total_price
    }
    return render(request, 'backend/order_detail.html', context)