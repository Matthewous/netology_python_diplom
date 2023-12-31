from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Category)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    ordering = ('name',)
    search_fields = ('name', 'category')

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'state')
    ordering = ('id',)
    search_fields = ('id', 'name', 'user', 'state')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','status','created_at','delivery_address','delivery_date','order_date')
    ordering = ('created_at',)
    search_fields = ('user', 'status')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order','product_name','quantity','price','shop')
    # ordering = ('created_at',)
    # search_fields = ('product_name')

@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('external_id','product','quantity','price','shop','price_rrc')