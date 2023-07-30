from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from orders.settings import EMAIL_HOST_USER
from .forms import UserRegistrationForm
from .forms import ShopRegistrationForm
from .models import Order, OrderItem, Product, Category, ProductInfo, Shop
from django.core.mail import send_mail
from django.db.models import Q, Min
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib import messages

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

        # отправка email

        # создание PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="order_confirmation.pdf"'
        
        pdfmetrics.registerFont(TTFont('ArialUnicode', 'backend/fonts/ArialUnicode.ttf'))

        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        styles = {
            'Heading1': ParagraphStyle(
                'Heading1',
                fontSize=16,
                fontName='ArialUnicode',
                spaceAfter=12
            ),
            'Heading2': ParagraphStyle(
                'Heading2',
                fontSize=14,
                fontName='ArialUnicode',
                spaceAfter=6
            ),
        }

        # Добавляем детали заказа
        elements.append(Paragraph('Ваш заказ:', styles['Heading1']))
        elements.append(Paragraph('', styles['Heading1']))
        elements.append(Paragraph(f'ID заказа: {order.id}', styles['Heading2']))
        elements.append(Paragraph(f'ID получателя: {user.id}', styles['Heading2']))
        elements.append(Paragraph('', styles['Heading1']))        
        elements.append(Paragraph(f'Получатель: {user.first_name} {user.last_name}', styles['Heading2']))
        elements.append(Paragraph(f'Адрес доставки: {order.delivery_address}', styles['Heading2']))
        elements.append(Paragraph(f'Ожидаемая дата доставки: {order.delivery_date}', styles['Heading2']))
        elements.append(Paragraph(f'Общая сумма заказа: {total_price}', styles['Heading2']))
        elements.append(Paragraph('', styles['Heading1']))
        # Добавляем позиции по заказу
        data = [['Наименование', 'Количество', 'Цена', 'Дистрибъютор']]
        for item in order_items:
            data.append([item.product_name, 
                         item.quantity, 
                         item.price, 
                         item.shop])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'ArialUnicode'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (-1, -1), 'ArialUnicode'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)

        # отправка email
        email = EmailMessage(
            subject='Ваш заказ оформлен',
            body=f'Ваш заказ по адресу будет доставлен {delivery_date} по адресу {delivery_address}. Сумма заказа: {total_price}',
            from_email=EMAIL_HOST_USER,
            to=[user.email],
        )
        email.attach('order_confirmation.pdf', response.getvalue(), 'application/pdf')
        email.send()


        return redirect('thank_you_page')

    context = {
        'order': order,
        'order_items': order_items,
        'total_price': total_price
    }
    return render(request, 'backend/cart.html', context)

def delete_order_item(request, item_id):
    item = OrderItem.objects.get(id=item_id)
    item.delete()
    return redirect('cart')

def update_order_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        item.quantity = quantity
        item.save()
    return redirect('cart')

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

def thank_you_page(request):
    user = request.user

    context = {
        'user': user
    }

    return render(request, 'backend/thank_you_page.html', context)

def register_shop(request):
    if request.method == 'POST':
        form = ShopRegistrationForm(request.POST)
        if form.is_valid():
            user = request.user
            if not Shop.objects.filter(user=user).exists():
                shop = form.save(commit=False)
                shop.user = request.user
                shop.save()
                messages.success(request, 'Магазин зарегистрирован.')
                return redirect('home')
            else:
                form.add_error(None, "Вы уже являетесь менеджером другого магазина")
    else:
        form = ShopRegistrationForm()

    return render(request, 'backend/register_shop.html', {'form': form})

