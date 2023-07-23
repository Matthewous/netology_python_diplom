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
    path('shops', views.all_shops, name='shops_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product_detail/<int:product_info_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('orders/', views.orders, name='orders'),
]
