"""
URL configuration for orders project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from backend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
    path('products/', views.products_list, name='products_list'),
    path('categories', views.all_categories, name='categories'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product_detail/<int:product_info_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('orders/', views.orders, name='orders'),
    path('cart/', views.cart, name='cart'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('thank_you_page', views.thank_you_page, name='thank_you_page'),
    path('cart/delete/<int:item_id>/', views.delete_order_item, name='delete_order_item'),
    path('update_order_item/<int:item_id>/', views.update_order_item, name='update_order_item'),
    
    path('register_shop/', views.register_shop, name='register_shop'),
    path('shop_catalog/', views.shop_catalog, name='shop_catalog'),
    path('update_product_quantity/<int:product_id>/', views.update_product_quantity, name='update_product_quantity'),
    path('update_product_price/<int:product_id>/', views.update_product_price, name='update_product_price'),
    path('update_product_price_rrc/<int:product_id>/', views.update_product_price_rrc, name='update_product_price_rrc'),
    # path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
]
